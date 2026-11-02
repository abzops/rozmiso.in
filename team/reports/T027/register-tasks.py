from pathlib import Path
import json
root=Path(__file__).resolve().parents[3]
p=root/'team/TASK-BOARD.json'
b=json.loads(p.read_text(encoding='utf-8'))
for n,lane,goal in [('T025','A','Verify four DeoDap source products and prepare public copy'),('T026','B','Verify four DeoDap source products and restore missing media'),('T027','Codex','Correct and publish eight new product listings with verified media')]:
    if not any(t['id']==n for t in b['tasks']):
        b['tasks'].append({'id':n,'goal':goal,'owner_lane':lane,'reviewer':'Codex and independent lane','status':'IN_PROGRESS','inputs':[f'team/reports/{n}/TASK.md'],'allowed_write_paths':[f'team/reports/{n}/**'],'depends_on':[],'deliverables':[f'team/reports/{n}/WORK-REPORT.md'],'authorization':'User8October2026 explicitly requests public copy/media and publication of8newproducts; preserve zero inventory/no selling launch.'})
b['updated']='2026-10-08'
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('T025-T027 registered as running.')
