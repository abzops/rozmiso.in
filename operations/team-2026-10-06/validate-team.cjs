const fs = require('node:fs');
const path = require('node:path');
const root = 'F:/Dropshipping';
const read = rel => fs.readFileSync(path.join(root,rel),'utf8');
const board = JSON.parse(read('team/TASK-BOARD.json'));
const manifest = JSON.parse(read('operations/team-2026-10-06/MANIFEST.json'));
const errors=[];
const check = (test, message) => { if (!test) errors.push(message); };
check(board.orchestrator==='Codex' && board.board_writer==='Codex only','Board authority');
check(board.tasks.length===7,'Task count');
check(new Set(board.tasks.map(t=>t.id)).size===7,'Duplicate task IDs');
const statuses=new Set(['READY','IN_PROGRESS','WAITING','SUBMITTED','CHANGES_REQUIRED','BLOCKED','ACCEPTED','CANCELLED']);
const taskById=new Map(board.tasks.map(t=>[t.id,t]));
for (const task of board.tasks) {
  check(statuses.has(task.status),'Unknown status '+task.id);
  check(task.execution_evidence===null && task.accepted_at===null,'False execution evidence '+task.id);
  check(task.dependency_condition===(task.id==='T007'?'ANY_SUBMITTED':'ALL_ACCEPTED'),'Dependency readiness '+task.id);
  check(task.allowed_write_paths.every(p=>p==='team/reports/'+task.id+'/**'),'Overbroad initial writer scope '+task.id);
  for (const input of task.inputs) {
    if (!input.startsWith('team/reports/')) check(fs.existsSync(path.join(root,input)), 'Missing input '+task.id+': '+input);
  }
  for (const dep of task.depends_on) check(taskById.has(dep),'Unknown dependency '+task.id);
  for (const output of task.deliverables) check(output.startsWith('team/reports/'+task.id+'/'),'Wrong deliverable scope '+task.id);
}
function visit(id,stack=[]) {
  check(!stack.includes(id),'Dependency cycle '+id);
  if (stack.includes(id)) return;
  for (const dep of taskById.get(id).depends_on) visit(dep,[...stack,id]);
}
board.tasks.forEach(t=>visit(t.id));
const profileNames=[];
for (const name of manifest.profiles) {
  const text=read('.agents/agents/'+name+'.md');
  const meta=text.split(/^---\s*$/m)[1];
  check(Boolean(meta),'Frontmatter missing '+name);
  check(meta.includes('name: '+name+'\n'),'Profile name mismatch '+name);
  check(meta.includes('model: inherit'),'Model changed '+name);
  check(meta.includes('mainAgent: false') && meta.includes('subagent: true'),'Worker runtime flags '+name);
  check(meta.includes('commandExecutionPolicy: sandbox'),'Command policy '+name);
  const toolLines=meta.match(/^  - .*$/gm)||[];
  check(toolLines.length===3 && toolLines.every(t=>['  - view_file','  - grep_search','  - run_command'].includes(t)),'Unmapped template tool '+name);
  const description=meta.match(/^description: (.*)$/m);
  try { check(typeof JSON.parse(description[1])==='string','Description type '+name); } catch { errors.push('Invalid description quoting '+name); }
  profileNames.push(name);
}
check(profileNames.length===22 && new Set(profileNames).size===22,'Profile count or duplicate');
let checked=0;
for (const rel of manifest.files) {
  check(fs.existsSync(path.join(root,rel)),'Missing created artifact '+rel);
  if (!rel.endsWith('.md') && !rel.endsWith('.json')) continue;
  const text=read(rel);
  check(!/nvapi-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{20,}/.test(text),'Credential pattern in active artifact '+rel);
  check(!/50,000\+\s*Happy|100% Cash on Delivery|Free Delivery across India/.test(text),'Legacy fabricated promise '+rel);
  checked++;
}
const result = {status:errors.length?'FAIL':'PASS',checked_artifacts:checked,profiles:profileNames.length,tasks:board.tasks.length,dependency_cycles:false,external_runtime:'NOT TESTED',errors};
fs.writeFileSync(path.join(root,'operations/team-2026-10-06/VALIDATION.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
if(errors.length) process.exitCode=1;
