"""
Automated Kernel Verification and Diagnostic Test Suite for Gideon Agentic OS.
"""

import sys
from pathlib import Path

# UTF-8 console output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure gideon directory is on path
base_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(base_dir))

from gideon.kernel import kernel
from gideon.process import ProcessState

def run_diagnostics():
    print("=" * 65)
    print("      GIDEON AGENTIC OS: KERNEL DIAGNOSTIC TEST SUITE")
    print("=" * 65)
    
    # 1. Boot Test
    print("\n[1/7] Testing Kernel Boot...")
    boot_ok = kernel.boot()
    assert boot_ok, "Kernel failed to boot!"
    assert 1 in kernel.processes, "PID 1 (gideon_init) was not registered!"
    print("  ✓ Kernel boot successful. PID 1 is active.")

    # 2. Process Spawning Test
    print("\n[2/7] Testing Process Spawning & Control Block...")
    p2 = kernel.spawn(name="test_worker_1", system_prompt="Test agent", task="Sample task", ppid=1)
    p3 = kernel.spawn(name="test_worker_2", system_prompt="Test agent 2", task="Sample task 2", ppid=1)
    assert p2.pid == 2 and p3.pid == 3, f"Unexpected PIDs: {p2.pid}, {p3.pid}"
    assert p2.state == ProcessState.READY, f"Process state should be READY, got: {p2.state}"
    print(f"  ✓ Process table operational: Spawned PID {p2.pid} ('{p2.name}') and PID {p3.pid} ('{p3.name}').")

    # 3. IPC Bus Message Passing Test
    print("\n[3/7] Testing Inter-Process Communication (IPC) Bus...")
    sent = kernel.syscall("SYS_IPC_SEND", caller_pid=p2.pid, target_pid=p3.pid, payload={"status": "TASK_READY", "data": "Gadget_X"})
    assert sent["ok"], "IPC send failed!"
    
    received = kernel.syscall("SYS_IPC_RECV", caller_pid=p3.pid)
    assert received["ok"] and received["message"] is not None, "IPC receive failed!"
    assert received["message"]["payload"]["data"] == "Gadget_X", f"IPC payload mismatch: {received}"
    print(f"  ✓ IPC Bus validated: Message delivered from PID {p2.pid} -> PID {p3.pid}.")

    # 4. Tiered Memory Subsystem Test
    print("\n[4/7] Testing Tiered Memory (RAM & SQLite Episodic)...")
    kernel.memory.ram_set("sys_flag", 42)
    assert kernel.memory.ram_get("sys_flag") == 42, "RAM get/set mismatch!"
    
    kernel.syscall("SYS_MEM_STORE", caller_pid=p2.pid, category="dropshipping", key="winning_product", value={"name": "Car Vacuum", "margin": 320})
    query = kernel.syscall("SYS_MEM_QUERY", caller_pid=p2.pid, category="dropshipping", key="winning_product")
    assert query["ok"] and len(query["records"]) > 0, "Episodic query returned no records!"
    print(f"  ✓ Tiered Memory validated: SQLite stored and queried record ({query['records'][0]['value']['name']}).")

    # 5. Tool & Peripheral Drivers Test
    print("\n[5/7] Testing Peripheral Tool Syscalls...")
    # Math tool
    calc_res = kernel.syscall("SYS_TOOL_CALL", caller_pid=1, tool="calculate", args={"expression": "999 - (270 + 65 + 280)"})
    assert calc_res["ok"] and calc_res["result"] == 384, f"Math tool failed: {calc_res}"
    
    # Dropshipping Unit Economics tool
    econ_res = kernel.syscall("SYS_TOOL_CALL", caller_pid=1, tool="unit_economics", args={"sourcing_cost": 270, "selling_price": 999, "ad_cac": 280, "rto_rate": 0.18})
    assert econ_res["ok"] and econ_res["viable_for_india"], f"Unit economics tool failed: {econ_res}"
    
    # Pin Code Risk Tool
    pin_res = kernel.syscall("SYS_TOOL_CALL", caller_pid=1, tool="pincode_risk_check", args={"pincode": "560001"})
    assert pin_res["ok"] and pin_res["cod_eligible"], f"Pincode risk tool failed: {pin_res}"
    print(f"  ✓ Peripheral drivers validated: Unit Economics, Pincode Risk, Math calculation passed.")

    # 6. Sandboxed Filesystem Driver Test
    print("\n[6/7] Testing Virtual Filesystem (VFS) Sandbox...")
    write_res = kernel.syscall("SYS_FS_WRITE", caller_pid=p2.pid, path="test_trace.txt", content="Gideon OS Kernel Trace Log")
    assert write_res["ok"], f"VFS write failed: {write_res}"
    read_res = kernel.syscall("SYS_FS_READ", caller_pid=p2.pid, path="test_trace.txt")
    assert read_res["ok"] and "Gideon OS Kernel" in read_res["content"], f"VFS read failed: {read_res}"
    print("  ✓ VFS Driver validated: Sandboxed file write & read verified.")

    # 7. Live Neural Compute Step (NVIDIA NIM)
    print("\n[7/7] Testing Live Compute Cycle on NVIDIA NIM...")
    compute_proc = kernel.spawn(
        name="gideon_live_test",
        system_prompt="You are Gideon OS live probe. Respond concisely in under 10 words.",
        task="Confirm that Gideon Agentic OS compute cycle is online."
    )
    step_res = kernel.step_process(compute_proc.pid)
    assert step_res.get("ok"), f"Compute cycle failed: {step_res.get('error')}"
    print(f"  ✓ Live compute cycle passed! Output from PID {compute_proc.pid}:\n    \"{step_res.get('output').strip()}\"")
    print(f"    Tokens used: {step_res.get('tokens')}")

    # Process Cleanup
    kernel.kill(p2.pid)
    kernel.kill(p3.pid)
    kernel.kill(compute_proc.pid)

    print("\n" + "=" * 65)
    print("   ALL 7 GIDEON AGENTIC OS SUBSYSTEMS PASSED WITH 100% HEALTH!")
    print("=" * 65)
    return True

if __name__ == "__main__":
    success = run_diagnostics()
    if not success:
        sys.exit(1)
