const fs=require('node:fs');
const path=require('node:path');
const root='F:/Dropshipping';
const file=rel=>path.join(root,rel);
const board=JSON.parse(fs.readFileSync(file('team/TASK-BOARD.json'),'utf8'));
for(const t of board.tasks) t.dependency_condition=t.id==='T007'?'ANY_SUBMITTED':'ALL_ACCEPTED';
board.tasks.find(t=>t.id==='T007').allowed_actions=['Review each submitted artifact independently; a blocked other lane does not prevent review. Return corrections or acceptance recommendation and record pending reports.'];
fs.writeFileSync(file('team/TASK-BOARD.json'),JSON.stringify(board,null,2)+'\n');
const template=JSON.parse(fs.readFileSync(file('team/templates/TASK.json'),'utf8'));
template.dependency_condition='ALL_ACCEPTED';
fs.writeFileSync(file('team/templates/TASK.json'),JSON.stringify(template,null,2)+'\n');
const charterFile=file('TEAM_ROSTER_AND_RULES.md');
let charter=fs.readFileSync(charterFile,'utf8');
const rule='Dependency readiness is explicit: downstream execution requires ACCEPTED dependencies and resolution of required blockers. Review tasks can start when a report is SUBMITTED; they never wait for that report to be accepted. T007 uses ANY_SUBMITTED: review either lane\'s submission independently, record which reports remain pending, and do not let a blocked lane prevent the other review. Codex updates readiness manually; this board is not an automated scheduler.';
if(!charter.includes('Dependency readiness is explicit:')) {
  charter=charter.replace('## Evidence and business decisions',rule+'\n\n## Evidence and business decisions');
  fs.writeFileSync(charterFile,charter);
}
fs.appendFileSync(file('operations/team-2026-10-06/SETUP-RESULTS.md'),'\nIndependent review resolved a dependency ambiguity: review begins on submitted evidence; downstream work waits for accepted dependencies. Either external lane can be reviewed independently.\n');
console.log('Dependency readiness clarified; no task executed.');
