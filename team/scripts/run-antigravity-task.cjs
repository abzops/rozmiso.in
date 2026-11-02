// Run from Codex through the terminal. No secret handling or account switching.
const fs=require('node:fs');
const path=require('node:path');
const {spawn}=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const id=process.argv[2];
if(!/^T\d{3}$/.test(id||'')) throw new Error('Usage: node team/scripts/run-antigravity-task.cjs T001');
const boardFile=path.join(root,'team/TASK-BOARD.json');
const board=JSON.parse(fs.readFileSync(boardFile,'utf8'));
const task=board.tasks.find(t=>t.id===id);
function persistTask(){
  const latest=JSON.parse(fs.readFileSync(boardFile,'utf8'));
  const index=latest.tasks.findIndex(t=>t.id===id);
  if(index<0)throw new Error('Task disappeared from authoritative board.');
  latest.tasks[index]=task;
  fs.writeFileSync(boardFile,JSON.stringify(latest,null,2)+'\n');
}
if(!task) throw new Error('Unknown task');
if(task.status!=='READY') throw new Error('Task must be READY; Codex owns reassignment and readiness.');
if(task.depends_on.length && task.dependency_condition==='ALL_ACCEPTED' && !task.depends_on.every(dep=>board.tasks.find(t=>t.id===dep)?.status==='ACCEPTED')) throw new Error('Dependencies not accepted');
if(task.blockers?.length) throw new Error('Task has unresolved blockers');
// Initial runtime is one cached account. Logical A/B labels never select an account.
// Limit this launcher to source/report audits. No external business actions permitted.
const enabled=new Set(['T001']);
if(!enabled.has(id)) throw new Error('This task is not enabled for terminal dispatch yet. Codex must verify its tools and scope first.');
const cli=path.join(process.env.LOCALAPPDATA,'agy/bin/agy.exe');
if(!fs.existsSync(cli)) throw new Error('Supported agy CLI is not installed.');
const dir=path.join(root,'team/reports',id);
fs.mkdirSync(dir,{recursive:true});
if(fs.existsSync(path.join(dir,'NATIVE-RESULT.json'))) throw new Error('Existing native result; review or reassign rather than overwrite evidence.');
// Supply bounded text snapshots directly. Never send image data URLs, credential
// documents or the whole workspace to an audit model. File tools are not required.
const sourceFiles=['rozmiso-studio-theme/assets/studio.css','rozmiso-studio-theme/sections/studio-header.liquid','rozmiso-studio-theme/sections/studio-hero.liquid','rozmiso-studio-theme/snippets/studio-card.liquid','rozmiso-studio-theme/layout/theme.liquid','outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/BRAND-GUIDE.md'];
const snapshots=sourceFiles.map(rel=>({path:rel,content:fs.readFileSync(path.join(root,rel),'utf8').replace(/data:image\/[^"'\s<>]+/g,'[embedded image data omitted]').slice(0,50000)}));
const prompt=`You are a bounded Rozmiso storefront audit worker reporting to Codex. The human has authorized this task. Inspect ONLY the source snapshots supplied here. Do not call tools, read other files, write, run commands, browse, spawn agents, modify settings or deploy. Codex will save your report. Keep the report under 1000 words.\n\nTask contract:\n${JSON.stringify(task,null,2)}\n\nSource snapshots captured by Codex:\n${JSON.stringify(snapshots)}\n\nReturn five prioritized findings with actual supplied file references, acceptance criterion results and gaps. This is an audit of supplied text, not a fresh file, browser, favicon-tab or checkout test. No invented reviews, stock, delivery promises, brand reputation, supplier verification or sales results. Be explicit about anything these snapshots cannot verify.`;
task.status='IN_PROGRESS';
task.execution_evidence={started_at:new Date().toISOString(),runtime:'Antigravity CLI',account_selection:'Current cached sign-in; identity/Pro entitlement not verified',agent:'Bounded evidence auditor role; supplied text snapshots',source_files:sourceFiles};
persistTask();
let child;
try{child=spawn(cli,['--input-format','stream-json','--output-format','stream-json','--mode','plan','--sandbox','--print-timeout','90s'],{cwd:path.join(root,'operations/team-2026-10-06/cli-setup'),shell:false,windowsHide:true});}
catch(e){task.status='BLOCKED';task.blockers=['Terminal dispatch failed before worker execution: '+e.code];persistTask();throw e;}
let stdout='',stderr='',settled=false,buffer='',streamResult=null,initSummary=null;
child.stdout.on('data',d=>{
  buffer+=d.toString();
  const lines=buffer.split(/\r?\n/);buffer=lines.pop();
  for(const line of lines){try{const event=JSON.parse(line);if(event.event==='result'){streamResult=event.result;child.stdin.end();}else if(event.event==='init'){initSummary={tools:event.init?.tools,permission_mode:event.init?.permission_mode};}}catch{stdout+=line+'\n';}}
});
child.stderr.on('data',d=>stderr+=d.toString());
child.stdin.on('error',e=>{stderr+='stdin: '+e.message+'\n';});
child.stdin.write(JSON.stringify({event:'user',message:{content:prompt}})+'\n');
const redact=s=>s.replace(/nvapi-[\w-]{15,}|sk-[\w-]{15,}|AIza[\w-]{25,}/g,'[REDACTED]');
function finish(code,error){
  if(settled)return;settled=true;clearTimeout(deadline);
  let result=streamResult;if(!result){try{result=JSON.parse(stdout.trim());}catch{result={status:'ERROR',error:error||'No valid result envelope',response:redact(stdout)};}}
  fs.writeFileSync(path.join(dir,'NATIVE-RESULT.json'),redact(JSON.stringify({exit_code:code,init:initSummary,result},null,2))+'\n');
  fs.writeFileSync(path.join(dir,'CLI-DIAGNOSTICS.txt'),redact(stderr));
  const submitted=code===0 && result.status==='SUCCESS' && Boolean(result.response?.trim());
  task.status=submitted?'SUBMITTED':'BLOCKED';
  task.execution_evidence.finished_at=new Date().toISOString();
  task.execution_evidence.result_path='team/reports/'+id+'/NATIVE-RESULT.json';
  if(!submitted)task.blockers=['Native execution failed or returned no usable report; inspect diagnostics.'];
  persistTask();
  fs.writeFileSync(path.join(dir,'WORK-REPORT.md'),`# ${id} - Antigravity audit\n\nStatus: ${task.status}\nRuntime: Antigravity CLI / current cached sign-in\nIndependent reviewer: Codex - pending\n\n${redact(result.response||result.error||'No response')}\n\n## Codex acceptance\n\nPending. A SUCCESS CLI envelope alone does not establish that acceptance criteria passed.\n`);
  console.log(JSON.stringify({task:id,status:task.status,result_path:task.execution_evidence.result_path,accepted:false}));
  process.exitCode=submitted?0:1;
}
const deadline=setTimeout(()=>{child.kill();finish(null,'Parent deadline exceeded');},160000);
child.on('error',e=>finish(null,e.message));child.on('close',code=>finish(code));
