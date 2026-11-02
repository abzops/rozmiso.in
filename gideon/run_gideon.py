"""
Main Launcher for Gideon Agentic OS.
Modes:
  python run_gideon.py        -> Starts Interactive Terminal Shell
  python run_gideon.py --web  -> Starts Web Dashboard on http://127.0.0.1:8080
  python run_gideon.py --test -> Runs Automated Kernel Verification Test
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Gideon Agentic Operating System")
    parser.add_argument("--web", action="store_true", help="Launch the Web Telemetry Dashboard on port 8080")
    parser.add_argument("--test", action="store_true", help="Run automated kernel diagnostics and tests")
    args = parser.parse_args()

    if args.web:
        import uvicorn
        from config import config
        print(f"[Gideon OS] Launching Web Telemetry Dashboard on http://{config.HOST}:{config.PORT} ...")
        uvicorn.run("gideon.server:app", host=config.HOST, port=config.PORT, reload=False)
    elif args.test:
        from test_kernel import run_diagnostics
        run_diagnostics()
    else:
        from gideon.shell import run_shell
        run_shell()

if __name__ == "__main__":
    main()
