"""
Web Telemetry Dashboard and HTTP API for Gideon Agentic OS.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Dict, Any, List
from gideon.kernel import kernel
from config import config

app = FastAPI(title="Gideon Agentic OS - Web Dashboard", version=config.OS_VERSION)

@app.on_event("startup")
def on_startup():
    kernel.boot()

@app.get("/api/telemetry")
def get_telemetry():
    return kernel.get_system_telemetry()

@app.get("/api/processes")
def get_processes():
    return kernel.list_processes()

@app.post("/api/spawn")
def spawn_process(payload: Dict[str, Any]):
    name = payload.get("name", "Worker_Agent")
    prompt = payload.get("system_prompt", "You are an AI worker agent.")
    task = payload.get("task", "Perform computation.")
    proc = kernel.spawn(name=name, system_prompt=prompt, task=task)
    return {"ok": True, "process": proc.to_dict()}

@app.post("/api/step/{pid}")
def step_process(pid: int):
    res = kernel.step_process(pid)
    return res

@app.post("/api/kill/{pid}")
def kill_process(pid: int):
    ok = kernel.kill(pid)
    return {"ok": ok}

@app.post("/api/pipeline")
def trigger_pipeline():
    specs = [
        {
            "name": "Hunter_Agent",
            "system_prompt": "You are Hunter-Dot, sourcing specialist for Indian dropshipping. Be concise.",
            "task": "Scout a viral high-margin kitchen gadget for Indian homes under ₹300."
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
    res = kernel.run_pipeline("Web_Triggered_Dropshipping_Pipeline", specs)
    return res

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gideon Agentic OS - Command Center</title>
        <style>
            :root {
                --bg: #090d16;
                --card-bg: #111827;
                --border: #1f2937;
                --accent: #f59e0b;
                --accent-blue: #38bdf8;
                --accent-green: #10b981;
                --text: #f3f4f6;
                --text-muted: #9ca3af;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
            body { background: var(--bg); color: var(--text); padding: 24px; }
            .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }
            .logo { font-size: 24px; font-weight: 800; letter-spacing: 2px; color: var(--accent); display: flex; align-items: center; gap: 8px; }
            .badge { background: #374151; color: var(--accent-blue); padding: 4px 8px; border-radius: 4px; font-size: 12px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px; }
            .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }
            .card h3 { font-size: 13px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px; }
            .card .val { font-size: 26px; font-weight: 700; color: var(--accent-blue); }
            .table-container { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 24px; overflow-x: auto; }
            table { width: 100%; border-collapse: collapse; text-align: left; }
            th, td { padding: 12px 14px; border-bottom: 1px solid var(--border); font-size: 13px; }
            th { color: var(--text-muted); text-transform: uppercase; font-size: 11px; }
            .status-tag { padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
            .status-RUNNING { background: #064e3b; color: #34d399; }
            .status-READY { background: #1e3a8a; color: #93c5fd; }
            .status-TERMINATED { background: #374151; color: #9ca3af; }
            .status-FAILED { background: #7f1d1d; color: #f87171; }
            .btn { background: var(--accent); color: #000; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 700; cursor: pointer; transition: 0.2s; }
            .btn:hover { opacity: 0.9; }
            .btn-blue { background: var(--accent-blue); }
            .btn-danger { background: #ef4444; color: #fff; padding: 4px 8px; font-size: 11px; }
            .btn-step { background: var(--accent-green); color: #fff; padding: 4px 8px; font-size: 11px; }
            .actions-bar { display: flex; gap: 12px; margin-bottom: 24px; }
            .log-box { background: #030712; border: 1px solid var(--border); border-radius: 8px; padding: 16px; font-family: monospace; font-size: 12px; height: 200px; overflow-y: auto; color: #a7f3d0; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">
                ⚡ GIDEON <span class="badge">AGENTIC OS POC</span>
            </div>
            <div>
                <button class="btn btn-blue" onclick="runPipeline()">🚀 Run Dropshipping Agent Pipeline</button>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Kernel Uptime</h3>
                <div class="val" id="uptime">0s</div>
            </div>
            <div class="card">
                <h3>Compute Model</h3>
                <div class="val" style="font-size: 15px; color: var(--accent);" id="model">Loading...</div>
            </div>
            <div class="card">
                <h3>Total Processes</h3>
                <div class="val" id="total_procs">0</div>
            </div>
            <div class="card">
                <h3>Tokens Consumed</h3>
                <div class="val" id="tokens">0</div>
            </div>
        </div>

        <div class="table-container">
            <h2 style="font-size: 16px; margin-bottom: 12px;">Active Agent Process Table (PCB)</h2>
            <table>
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Name</th>
                        <th>State</th>
                        <th>Cycles</th>
                        <th>Tokens</th>
                        <th>Task Preview</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="proc_rows">
                    <tr><td colspan="7">Loading processes...</td></tr>
                </tbody>
            </table>
        </div>

        <h2 style="font-size: 16px; margin-bottom: 12px;">Kernel Live Telemetry & Output Stream</h2>
        <div class="log-box" id="log_stream">[Gideon OS] Telemetry feed connected.</div>

        <script>
            async function refresh() {
                try {
                    const tel = await fetch('/api/telemetry').then(r => r.json());
                    document.getElementById('uptime').innerText = tel.uptime_seconds + 's';
                    document.getElementById('model').innerText = tel.active_model;
                    document.getElementById('total_procs').innerText = tel.processes_total;
                    document.getElementById('tokens').innerText = tel.total_tokens_consumed;

                    const procs = await fetch('/api/processes').then(r => r.json());
                    const tbody = document.getElementById('proc_rows');
                    tbody.innerHTML = '';
                    procs.forEach(p => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td><b>${p.pid}</b></td>
                            <td>${p.name}</td>
                            <td><span class="status-tag status-${p.state}">${p.state}</span></td>
                            <td>${p.cpu_cycles}</td>
                            <td>${p.token_usage}</td>
                            <td style="color: var(--text-muted);">${p.task_preview}</td>
                            <td>
                                <button class="btn btn-step" onclick="stepProc(${p.pid})">Step</button>
                                ${p.pid > 1 ? `<button class="btn btn-danger" onclick="killProc(${p.pid})">Kill</button>` : ''}
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                } catch(e) {
                    console.error(e);
                }
            }

            async function stepProc(pid) {
                log('Executing compute step on PID ' + pid + '...');
                const res = await fetch('/api/step/' + pid, {method: 'POST'}).then(r => r.json());
                if (res.ok) {
                    log('[PID ' + pid + ' Output]:\\n' + res.output);
                } else {
                    log('[PID ' + pid + ' Error]: ' + res.error);
                }
                refresh();
            }

            async function killProc(pid) {
                await fetch('/api/kill/' + pid, {method: 'POST'});
                log('Process PID ' + pid + ' terminated.');
                refresh();
            }

            async function runPipeline() {
                log('[Gideon OS] Launching multi-agent dropshipping pipeline (Hunter -> Creative -> Shield)...');
                const res = await fetch('/api/pipeline', {method: 'POST'}).then(r => r.json());
                if (res.success) {
                    log('\\n=== PIPELINE EXECUTION COMPLETED ===\\n' + res.final_output);
                } else {
                    log('Pipeline execution interrupted or failed.');
                }
                refresh();
            }

            function log(msg) {
                const el = document.getElementById('log_stream');
                el.innerText += '\\n' + msg;
                el.scrollTop = el.scrollHeight;
            }

            setInterval(refresh, 2500);
            refresh();
        </script>
    </body>
    </html>
    """
