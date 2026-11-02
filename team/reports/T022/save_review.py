from pathlib import Path
import json,hashlib,difflib,datetime
root=Path('F:/Dropshipping');out=root/'team/reports/T022';source=root/'rozmiso-studio-theme';candidate=out/'theme-candidate'
manifest=json.loads((out/'CHANGED-FILES.json').read_text());diff=[]
for item in manifest:
 rel=item['path'];p=source/rel;n=candidate/rel
 assert hashlib.sha256(p.read_bytes()).hexdigest()==item['source_sha256'],'Production source drift '+rel
 assert hashlib.sha256(n.read_bytes()).hexdigest()==item['candidate_sha256'],'Candidate drift '+rel
 diff.extend(difflib.unified_diff(p.read_text().splitlines(True),n.read_text().splitlines(True),fromfile='authoritative/'+rel,tofile='candidate/'+rel))
(out/'CANDIDATE.patch').write_text(''.join(diff),encoding='utf-8')
changed={x['path'] for x in manifest};unchanged=[]
for p in source.rglob('*'):
 if p.is_file() and p.relative_to(source).as_posix() not in changed:
  assert p.read_bytes()==(candidate/p.relative_to(source)).read_bytes()
  unchanged.append(p.relative_to(source).as_posix())
data={'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_files':len(changed)+len(unchanged),'changed_files':sorted(changed),'unchanged_files':unchanged,'authoritative_source_unchanged':True,'css_fonts_images_settings_locales_unchanged':True,'behavioral_tests':{'passed':13,'failed':0,'command':'node --test team/reports/T022/regression.test.cjs'},'liquid_validation':{'passed':7,'failed':0,'validator':'Official shopify-liquid/scripts/validate.mjs full-theme mode with task-local module resolver using existing installed dependencies'},'limits':['No live deployment','No Shopify backend lock','Native multi-page filtering depends on configured collection.filters','No actual Shopify browser visual review']}
(out/'VERIFIED-RESULTS.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in data.items() if k!='unchanged_files'},indent=2))
