import json
from pathlib import Path
p=Path('team/TASK-BOARD.json')
b=json.loads(p.read_text(encoding='utf-8-sig'))
for n,goal,lane in [(19,'Audit workspace files and operational evidence','Codex worker A'),(20,'Analyze demo workbook and WhatsApp ZIP','Codex worker B'),(21,'Import reviewed demo products as unpublished drafts and verify Shopify saved state','Codex'),(22,'Prepare isolated theme fixes for prelaunch and catalog discovery','Codex worker A'),(23,'Review business inputs for Shopify settings','Codex worker B'),(24,'Inspect all Shopify settings and complete supported changes','Codex')]:
    task=next((t for t in b['tasks'] if t['id']==f'T{n:03}'),None)
    if task is None:
        task={'id':f'T{n:03}','goal':goal,'owner_lane':lane,'reviewer':'Codex / independent workers','inputs':[f'team/reports/T{n:03}/TASK.md'],'allowed_write_paths':[f'team/reports/T{n:03}/**'],'depends_on':[],'deliverables':[f'team/reports/T{n:03}/WORK-REPORT.md']}
        b['tasks'].append(task)
    task['status']='SUBMITTED' if n in (19,20,23) else 'IN_PROGRESS'
b['updated']='2026-10-08'
p.write_text(json.dumps(b,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
