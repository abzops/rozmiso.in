"""
Process Control Block (PCB) and execution state for Gideon Agentic OS.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

class ProcessState(str, Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING_IO = "WAITING_IO"
    WAITING_IPC = "WAITING_IPC"
    TERMINATED = "TERMINATED"
    FAILED = "FAILED"

class AgentProcess:
    """
    Process Control Block (PCB) representing an active agent thread inside the Gideon OS kernel.
    """
    def __init__(
        self,
        pid: int,
        name: str,
        system_prompt: str,
        task: str,
        ppid: int = 1,
        priority: int = 5,
        model: Optional[str] = None,
        tools: Optional[List[str]] = None
    ):
        self.pid: int = pid
        self.ppid: int = ppid
        self.name: str = name
        self.system_prompt: str = system_prompt
        self.task: str = task
        self.priority: int = priority  # 0 (Kernel/High) to 10 (Background/Low)
        self.model: Optional[str] = model
        self.tools: List[str] = tools or []
        
        self.state: ProcessState = ProcessState.NEW
        self.created_at: str = datetime.now(timezone.utc).isoformat()
        self.updated_at: str = self.created_at
        
        # Memory & Context Registers
        self.context: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]
        self.registers: Dict[str, Any] = {}
        
        # Telemetry & Accounting
        self.cpu_cycles: int = 0  # Number of LLM inference steps taken
        self.token_usage: int = 0
        self.exit_code: Optional[int] = None
        self.error: Optional[str] = None
        self.last_output: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pid": self.pid,
            "ppid": self.ppid,
            "name": self.name,
            "state": self.state.value,
            "priority": self.priority,
            "cpu_cycles": self.cpu_cycles,
            "token_usage": self.token_usage,
            "tools": self.tools,
            "model": self.model,
            "task_preview": self.task[:80] + ("..." if len(self.task) > 80 else ""),
            "last_output": self.last_output[:120] + ("..." if len(self.last_output) > 120 else ""),
            "created_at": self.created_at,
            "exit_code": self.exit_code
        }

    def append_message(self, role: str, content: str):
        self.context.append({"role": role, "content": content})
        self.updated_at = datetime.now(timezone.utc).isoformat()
