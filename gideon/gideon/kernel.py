"""
Gideon Agentic OS Kernel Core.
Coordinates process scheduling, syscall dispatch, memory tiers, IPC, and driver abstractions.
"""

import time
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from gideon.process import AgentProcess, ProcessState
from gideon.ipc import IPCBus
from gideon.memory import MemorySubsystem
from gideon.drivers.llm_driver import LLMDriver
from gideon.drivers.fs_driver import FilesystemDriver
from gideon.drivers.tool_driver import ToolDriver
from config import config

class GideonKernel:
    """
    The Gideon Agentic Operating System Kernel.
    """
    def __init__(self):
        self.os_name = config.OS_NAME
        self.version = config.OS_VERSION
        self.boot_time = time.time()
        
        # Subsystems
        self.ipc = IPCBus(max_queue_size=config.IPC_MAX_QUEUE_SIZE)
        self.memory = MemorySubsystem(config.DATA_DIR / "gideon_memory.sqlite3")
        
        # Drivers
        self.llm_driver = LLMDriver(
            api_key=config.NVIDIA_API_KEY,
            base_url=config.NVIDIA_BASE_URL,
            default_model=config.DEFAULT_MODEL
        )
        self.fs_driver = FilesystemDriver(config.WORKSPACE_DIR)
        self.tool_driver = ToolDriver()
        
        # Process Table
        self.processes: Dict[int, AgentProcess] = {}
        self._next_pid: int = 1
        
        # Audit Log & Syscall History
        self.syscall_log: List[Dict[str, Any]] = []

    def boot(self) -> bool:
        """
        Initializes drivers and brings up PID 1 (gideon_init).
        """
        print(f"[{self.os_name}] Booting Kernel {self.version}...")
        self.llm_driver.initialize()
        self.fs_driver.initialize()
        self.tool_driver.initialize()
        
        # Spawn Init Process (Gideon Executive Daemon)
        init_proc = self.spawn(
            name="gideon_init",
            system_prompt=(
                "You are Gideon, the master artificial intelligence operating system. "
                "You oversee autonomous agent threads, schedule tasks, and ensure optimal execution."
            ),
            task="System kernel watchdog and process orchestrator.",
            ppid=0,
            priority=0
        )
        init_proc.state = ProcessState.RUNNING
        print(f"[{self.os_name}] Kernel initialized. PID 1 (gideon_init) is active.")
        return True

    # -------------------------------------------------------------
    # Process Management (Process Table & Lifecycle)
    # -------------------------------------------------------------
    def spawn(
        self,
        name: str,
        system_prompt: str,
        task: str,
        ppid: int = 1,
        priority: int = 5,
        model: Optional[str] = None,
        tools: Optional[List[str]] = None
    ) -> AgentProcess:
        pid = self._next_pid
        self._next_pid += 1

        process = AgentProcess(
            pid=pid,
            name=name,
            system_prompt=system_prompt,
            task=task,
            ppid=ppid,
            priority=priority,
            model=model or config.DEFAULT_MODEL,
            tools=tools
        )
        self.processes[pid] = process
        self.ipc.register_process(pid)
        process.state = ProcessState.READY
        
        self._log_syscall("SYS_SPAWN", ppid, {"child_pid": pid, "name": name})
        return process

    def kill(self, pid: int, caller_pid: int = 1) -> bool:
        if pid in self.processes and pid != 1:  # Protect PID 1
            proc = self.processes[pid]
            proc.state = ProcessState.TERMINATED
            proc.exit_code = 137  # SIGKILL equivalent
            self.ipc.unregister_process(pid)
            self._log_syscall("SYS_KILL", caller_pid, {"target_pid": pid})
            return True
        return False

    def list_processes(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.processes.values()]

    # -------------------------------------------------------------
    # Scheduler & Execution Engine
    # -------------------------------------------------------------
    def step_process(self, pid: int) -> Dict[str, Any]:
        """
        Executes one compute cycle / time slice for the specified process.
        """
        if pid not in self.processes:
            return {"ok": False, "error": f"PID {pid} not found"}

        proc = self.processes[pid]
        if proc.state not in (ProcessState.READY, ProcessState.RUNNING):
            return {"ok": False, "error": f"Process {pid} is not executable (State: {proc.state})"}

        proc.state = ProcessState.RUNNING
        
        # Check if the process has pending IPC messages to ingest
        incoming = self.ipc.receive(pid)
        if incoming:
            ipc_note = f"[IPC Message from PID {incoming.sender_pid}]: {incoming.payload}"
            proc.append_message("user", ipc_note)

        # Dispatch inference to the LLM compute driver
        res = self.llm_driver.execute(
            command="chat",
            messages=proc.context,
            model=proc.model
        )

        proc.cpu_cycles += 1
        
        if res.get("ok"):
            output = res.get("content", "")
            proc.last_output = output
            proc.token_usage += res.get("tokens", 0)
            proc.append_message("assistant", output)
            proc.state = ProcessState.READY  # Completed slice, back to ready
            
            # Persist episode to durable memory
            self.memory.store_episodic(
                pid=proc.pid,
                category="execution_log",
                key=f"cycle_{proc.cpu_cycles}",
                value={"task": proc.task, "output": output}
            )

            return {"ok": True, "pid": pid, "output": output, "tokens": proc.token_usage}
        else:
            proc.error = res.get("error")
            proc.state = ProcessState.FAILED
            return {"ok": False, "pid": pid, "error": proc.error}

    # -------------------------------------------------------------
    # Syscall Dispatcher
    # -------------------------------------------------------------
    def syscall(self, syscall_name: str, caller_pid: int, **kwargs) -> Dict[str, Any]:
        """
        Standard syscall gate for agent processes.
        """
        self._log_syscall(syscall_name, caller_pid, kwargs)

        if syscall_name == "SYS_IPC_SEND":
            target = kwargs.get("target_pid")
            payload = kwargs.get("payload")
            success = self.ipc.send(caller_pid, target, payload)
            return {"ok": success}

        elif syscall_name == "SYS_IPC_RECV":
            msg = self.ipc.receive(caller_pid)
            return {"ok": True, "message": msg.to_dict() if msg else None}

        elif syscall_name == "SYS_MEM_STORE":
            category = kwargs.get("category", "general")
            key = kwargs.get("key", "val")
            val = kwargs.get("value")
            self.memory.store_episodic(caller_pid, category, key, val)
            return {"ok": True}

        elif syscall_name == "SYS_MEM_QUERY":
            category = kwargs.get("category")
            key = kwargs.get("key")
            records = self.memory.query_episodic(category, key)
            return {"ok": True, "records": records}

        elif syscall_name == "SYS_FS_READ":
            return self.fs_driver.execute("read", path=kwargs.get("path"))

        elif syscall_name == "SYS_FS_WRITE":
            return self.fs_driver.execute("write", path=kwargs.get("path"), content=kwargs.get("content"))

        elif syscall_name == "SYS_TOOL_CALL":
            tool_name = kwargs.get("tool")
            args = kwargs.get("args", {})
            return self.tool_driver.execute(tool_name, **args)

        return {"ok": False, "error": f"Unknown syscall: {syscall_name}"}

    def _log_syscall(self, name: str, caller_pid: int, args: Dict[str, Any]):
        entry = {
            "timestamp": time.time(),
            "syscall": name,
            "caller_pid": caller_pid,
            "args": str(args)[:100]
        }
        self.syscall_log.append(entry)
        if len(self.syscall_log) > 500:
            self.syscall_log.pop(0)

    # -------------------------------------------------------------
    # High-Level Autonomous Pipeline (Kernel Orchestrator)
    # -------------------------------------------------------------
    def run_pipeline(self, pipeline_name: str, agent_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Spawns a cooperative multi-agent team, pipes results through IPC, and returns synthesized output.
        """
        print(f"\n[Gideon OS] Initiating Agent Pipeline: '{pipeline_name}' ({len(agent_specs)} steps)...")
        spawned_pids = []
        pipeline_results = []
        last_output = ""

        for spec in agent_specs:
            name = spec.get("name")
            prompt = spec.get("system_prompt")
            task = spec.get("task")
            if last_output:
                task = f"{task}\n\n[Input from Previous Agent Process]:\n{last_output}"

            proc = self.spawn(name=name, system_prompt=prompt, task=task, ppid=1)
            spawned_pids.append(proc.pid)
            print(f" -> Spawning PID {proc.pid}: '{name}'...")

            # Run compute step
            step_result = self.step_process(proc.pid)
            if step_result.get("ok"):
                last_output = step_result.get("output", "")
                proc.state = ProcessState.TERMINATED
                proc.exit_code = 0
                pipeline_results.append({
                    "pid": proc.pid,
                    "agent": name,
                    "output": last_output,
                    "tokens": step_result.get("tokens", 0)
                })
                print(f"    ✓ PID {proc.pid} ({name}) completed. Tokens: {step_result.get('tokens')}")
            else:
                print(f"    ✗ PID {proc.pid} ({name}) FAILED: {step_result.get('error')}")
                proc.state = ProcessState.FAILED
                break

        return {
            "pipeline": pipeline_name,
            "success": len(pipeline_results) == len(agent_specs),
            "stages": pipeline_results,
            "final_output": last_output
        }

    def get_system_telemetry(self) -> Dict[str, Any]:
        uptime_sec = round(time.time() - self.boot_time, 2)
        total_procs = len(self.processes)
        active_procs = sum(1 for p in self.processes.values() if p.state == ProcessState.RUNNING)
        total_tokens = sum(p.token_usage for p in self.processes.values())
        total_cycles = sum(p.cpu_cycles for p in self.processes.values())
        
        return {
            "os_name": self.os_name,
            "version": self.version,
            "uptime_seconds": uptime_sec,
            "active_model": config.DEFAULT_MODEL,
            "processes_total": total_procs,
            "processes_active": active_procs,
            "total_cpu_cycles": total_cycles,
            "total_tokens_consumed": total_tokens,
            "memory_stats": self.memory.get_stats(),
            "syscalls_logged": len(self.syscall_log)
        }

# Global Kernel Singleton
kernel = GideonKernel()
