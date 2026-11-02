from pathlib import Path
import json,hashlib,difflib,datetime
root=Path('F:/Dropshipping');out=root/'team/reports/T022';src=root/'rozmiso-studio-theme/assets/studio.css';dest=out/'theme-candidate/assets/studio.css'
hashof=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((out/'SOURCE-INTEGRATION.json').read_text())
# The earlier verification explicitly marked CSS unchanged; preserve its original candidate bytes by removing only the new fix.
original=dest.read_text().replace('/* Let the PDP grid shrink around its scrollable thumbnail row. */\n.pdp > *{min-width:0}.pdp .thumbs{min-width:0;max-width:100%}\n','')
assert original.replace('\r\n','\n')==src.read_text().replace('\r\n','\n'),'Unexpected CSS change outside minimal fix'
for row in manifest['files']:
 assert hashof(root/'rozmiso-studio-theme'/row['path'])==row['candidate_sha256'],'Integrated source drift '+row['path']
 assert hashof(out/'theme-candidate'/row['path'])==row['candidate_sha256'],'Candidate drift '+row['path']
(out/'MOBILE-CSS.patch').write_text(''.join(difflib.unified_diff(src.read_text().splitlines(True),dest.read_text().splitlines(True),fromfile='authoritative/assets/studio.css',tofile='candidate/assets/studio.css')),encoding='utf-8')
data={'prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'changed_path':'assets/studio.css','source_sha256':hashof(src),'candidate_sha256':hashof(dest),'prior_eight_candidate_files_unchanged':True,'prior_eight_integrated_files_unchanged':True,'source_css_unchanged':True,'new_candidate_declarations':'.pdp > *{min-width:0}.pdp .thumbs{min-width:0;max-width:100%}','live_qa_evidence_reported_by_codex':{'client_width':375,'pdp_child_width':726,'scroll_width':746,'screenshot':'team/reports/T024/theme-product-mobile.png'},'layout_result':'Pending Codex actual browser390px verification','integration':'Not integrated'}
(out/'MOBILE-CSS-RESULTS.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data,indent=2))
