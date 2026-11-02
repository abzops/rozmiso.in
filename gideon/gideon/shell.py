"""
Interactive CLI Shell for Gideon Agentic OS.
"""

import sys
import shlex
from typing import List
from gideon.kernel import kernel
from gideon.process import ProcessState

def print_banner():
    banner = r"""
   _____ _____ _____  ______ ____  _   _ 
  / ____|_   _|  __ \|  ____/ __ \| \ | |
 | |  __  | | | |  | | |__ | |  | |  \| |
 | | |_ | | | | |  | |  __|| |  | | . ` |
 | |__| |_| |_| |__| | |___| |__| | |\  |
  \_____|_____|_____/|______\____/|_| \_|
       AGENTIC OPERATING SYSTEM (POC)
    """
    print(banner)
    telemetry = kernel.get_system_telemetry()
    print(f" Kernel Version : {telemetry['version']}")
    print(f" Compute Engine : {telemetry['active_model']}")
    print(f" Kernel Memory  : SQLite Tier 2 active ({telemetry['memory_stats']['db_path']})")
    print(f" Type 'help' to view system commands or 'pipeline' to run a multi-agent test.\n")

def run_shell():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    kernel.boot()
    print_banner()

    while True:
        try:
            raw_in = input("gideon:/> ").strip()
            if not raw_in:
                continue

            parts = shlex.split(raw_in)
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ("exit", "quit", "shutdown"):
                print("[Gideon OS] Halting kernel... Goodbye.")
                break

            elif cmd == "help":
                print("\nGideon Agentic OS Commands:")
                print("  ps                - List all active agent processes")
                print("  spawn <name> <task> - Create and register a new agent process")
                print("  step <pid>        - Execute one compute cycle on process <pid>")
                print("  kill <pid>        - Terminate process <pid>")
                print("  ipc               - Inspect IPC bus message history")
                print("  mem               - Show tiered memory status and recent records")
                print("  sysinfo           - Display kernel uptime, token counters & hardware")
                print("  tool <tool_name>  - Execute a peripheral tool syscall (e.g. unit_economics, pincode_risk_check)")
                print("  pipeline          - Execute an autonomous multi-agent sprint pipeline")
                print("  exit              - Shutdown Gideon OS\n")

            elif cmd == "ps":
                procs = kernel.list_processes()
                print("\nPID  PPID  NAME             STATE       CYCLES  TOKENS  TASK PREVIEW")
                print("-" * 75)
                for p in procs:
                    print(f"{p['pid']:<4} {p['ppid']:<5} {p['name']:<16} {p['state']:<11} {p['cpu_cycles']:<7} {p['token_usage']:<7} {p['task_preview']}")
                print()

            elif cmd == "sysinfo":
                t = kernel.get_system_telemetry()
                print("\n=== GIDEON KERNEL TELEMETRY ===")
                for k, v in t.items():
                    print(f"  {k:<24}: {v}")
                print()

            elif cmd == "spawn":
                if len(args) < 2:
                    print("Usage: spawn <name> <task_description>")
                    continue
                name = args[0]
                task = " ".join(args[1:])
                proc = kernel.spawn(name=name, system_prompt="You are a specialized agent.", task=task)
                print(f"[Gideon OS] Spawned process PID {proc.pid}: '{name}' in state READY.")

            elif cmd == "step":
                if not args:
                    print("Usage: step <pid>")
                    continue
                try:
                    pid = int(args[0])
                except ValueError:
                    print("Error: PID must be an integer.")
                    continue
                print(f"[Gideon OS] Stepping compute on PID {pid}...")
                res = kernel.step_process(pid)
                if res.get("ok"):
                    print(f"\n[PID {pid} Output]:\n{res.get('output')}\n")
                else:
                    print(f"[Error]: {res.get('error')}")

            elif cmd == "kill":
                if not args:
                    print("Usage: kill <pid>")
                    continue
                pid = int(args[0])
                if kernel.kill(pid):
                    print(f"[Gideon OS] Process {pid} terminated.")
                else:
                    print(f"[Error] Failed to terminate PID {pid} (PID 1 is protected).")

            elif cmd == "ipc":
                history = kernel.ipc.get_history()
                print(f"\nIPC Bus Activity ({len(history)} messages):")
                for msg in history[-10:]:
                    print(f"  [{msg['timestamp'][11:19]}] PID {msg['sender_pid']} -> PID {msg['target_pid']} ({msg['msg_type']}): {str(msg['payload'])[:60]}")
                print()

            elif cmd == "mem":
                stats = kernel.memory.get_stats()
                print("\n=== MEMORY SUBSYSTEM ===")
                print(f"  Volatile RAM Pool Keys : {stats['ram_keys_count']}")
                print(f"  Episodic SQLite Records: {stats['episodic_records_count']}")
                print(f"  Database Path          : {stats['db_path']}")
                recent = kernel.memory.query_episodic()[:5]
                if recent:
                    print("\n  Recent Episodic Memory Traces:")
                    for r in recent:
                        print(f"   - [PID {r['pid']}][{r['category']}]: {r['key']}")
                print()

            elif cmd == "tool":
                if not args:
                    print("Usage: tool <tool_name> [args] (e.g. tool unit_economics, tool pincode_risk_check pincode=560001)")
                    continue
                tool_name = args[0]
                kw = {}
                for a in args[1:]:
                    if "=" in a:
                        k, v = a.split("=", 1)
                        kw[k] = v
                res = kernel.syscall("SYS_TOOL_CALL", caller_pid=1, tool=tool_name, args=kw)
                print(f"[Syscall Result]:\n{res}\n")

            elif cmd == "pipeline":
                # Execute sample autonomous dropshipping launch pipeline inside the OS
                print("\n[Gideon OS] Executing Autonomous Dropshipping Launch Pipeline...")
                specs = [
                    {
                        "name": "Hunter_Agent",
                        "system_prompt": "You are Hunter-Dot, sourcing specialist for Indian dropshipping. Be concise.",
                        "task": "Analyze a viral 2-in-1 Car Vacuum Cleaner (Cost: ₹270 on Roposo). State retail price, target audience, and why it's a winner."
                    },
                    {
                        "name": "Creative_Agent",
                        "system_prompt": "You are Creative-Dot, Hinglish copywriter for Meta ads. Write catchy hooks.",
                        "task": "Write 2 high-CTR Hinglish hooks and a 20-second UGC video script for this product."
                    },
                    {
                        "name": "Shield_Agent",
                        "system_prompt": "You are Shield-Dot, COD and RTO protector. Focus on Indian logistics.",
                        "task": "Write an automated WhatsApp order confirmation template and COD recovery offer for this product."
                    }
                ]
                res = kernel.run_pipeline("Dropshipping_Launch_Alpha", specs)
                print(f"\n[Pipeline Finished! Total Stages: {len(res['stages'])}, Success: {res['success']}]\n")

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")

        except (KeyboardInterrupt, EOFError):
            print("\n[Gideon OS] Interrupt signal received. Exiting.")
            break
        except Exception as e:
            print(f"[Kernel Trap]: {e}")

if __name__ == "__main__":
    run_shell()
