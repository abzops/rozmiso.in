const fs=require('node:fs');const path=require('node:path');const root='F:/Dropshipping';
const file=path.join(root,'team/TASK-BOARD.json');const board=JSON.parse(fs.readFileSync(file,'utf8'));const task=board.tasks.find(t=>t.id==='T001');
if(task.status==='IN_PROGRESS' && !fs.existsSync(path.join(root,'team/reports/T001/NATIVE-RESULT.json'))){
  task.dispatch_history=[{date:new Date().toISOString(),result:'Local spawn ENAMETOOLONG; no worker started. Replaced argument payload with documented stdin JSON transport.'}];
  task.status='READY';task.execution_evidence=null;task.blockers=[];
  fs.writeFileSync(file,JSON.stringify(board,null,2)+'\n');
}
console.log('Task readiness reconciled with observed local dispatch outcome.');
