from pathlib import Path
import json,hashlib
from PIL import Image
r=Path('F:/Dropshipping'); task=r/'team/reports/T031'; src=r/'rozmiso-studio-theme'; remote=task/'remote-verified'
def norm(p):
    if p.suffix in ['.json','.liquid','.css','.js','.svg']:
        s=p.read_text(encoding='utf-8-sig')
        if p.suffix=='.json':
            if s.lstrip().startswith('/*'):s=s.split('*/',1)[1]
            return json.loads(s)
        return '\n'.join(s.splitlines())
    return p.read_bytes()
missing=[];mismatches=[];files=[]
for p in src.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(src); q=remote/rel
    if not q.exists():missing.append(str(rel))
    elif norm(p)!=norm(q):mismatches.append(str(rel))
    files.append({'path':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
proof={'themeId':159552962752,'date':'2026-10-22','files':len(files),'missing':missing,'mismatches':mismatches}
(task/'REMOTE-INTEGRITY.json').write_text(json.dumps(proof,indent=2)+'\n')
(task/'SOURCE-HASHES.json').write_text(json.dumps(files,indent=2)+'\n')
for p in (task/'screenshots').glob('*.jpg'):Image.open(p).save(p.with_suffix('.png'))
board=r/'team/TASK-BOARD.json';d=json.loads(board.read_text(encoding='utf-8-sig'))
for item in d['tasks']:
    if item.get('id')=='T031':item.update(status='ACCEPTED',current_priority='Reference landing published and visually reviewed; actual stock/payment unchanged',runtime='Theme159552962752 live; clean Theme Check,14/14 fixtures, remote integrity; corrected soap identity PASS; tablet clipping fixed',evidence=['team/reports/T031/WORK-REPORT.md','team/reports/T031/REMOTE-INTEGRITY.json'])
board.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
log=r/'WORK-LOG.md';s=log.read_text(encoding='utf-8-sig').replace('Last updated: 14 October 2026.','Last updated: 22 October 2026.')
start=s.index('**Current work:**');end=s.index('**Social status:**',start)
s=s[:start]+'''**Current work:** T031 reference landing page rebuild completed and published via Shopify CLI22 October2026. Current live theme159552962752, Rozmiso Reference Landing2026-10-22. Full photographic hero, five category tiles, four native featured products, home/benefits/travel sections, single-row header and forest footer. Desktop/mobile visual review,14 fixtures PASS, Theme Check clean;820px clipping caught and fixed. Corrected soap-brush photo uses new owner reference with face-up shell, flat rear bristles and cap between ears; root +independent visible identity PASS. No product stock/price/payment mutations. Full report team/reports/T031/WORK-REPORT.md.

''' +s[end:]
s=s.replace('| Current published theme | Rozmiso Studio - Customer Review 2026-10-14, ID159259001024; previous158950424768 retained unpublished for rollback |','| Current published theme | Rozmiso Reference Landing2026-10-22, ID159552962752; previous159259001024 retained unpublished for rollback |')
s+='''
### 22 October2026 — Reference landing page live and reviewed

- Live-before-change verified159259001024 with official Shopify CLI; pulled baseline and saved authoritative local backup. Two bounded workers built content and chrome; root integrated, generated/optimized imagery and independently compared reference/layout. Published159552962752; previous159259001024 retained rollback.
-12 WebP theme assets total953972bytes. Four new built-in image_gen outputs saved in T031/generated; prompt/reference mapping in generation-prompts.json. Corrected soap use image follows three owner originals; obsolete wrong bristle/cap image not used. Product identity is visible-reference acceptance, not measurement certification. Other21-product catalog replacement still pending separate approval and soap set requires correction/re-review.
- Official Theme Check clean,3 landing render fixtures +11 retained regression fixtures PASS. Mobile390px page375px (scrollbar), carousel scroll175.2px after Next, bag opens/Escape closes, juicer search returns1. Desktop original1536 and fresh live1265 visually checked. Tablet820 page805; home copy229.1 fits260px banner, travel copy270.6 fits300px after fixing actual clipping. No real orders/messages/payment tests performed. Chrome disconnected; in-app browser completed remaining checks.
- Fresh live screenshot screenshots/live-home.png. Earlier desktop full screenshot contains sticky/focus capture artifacts and is intermediate evidence, not final clean-page screenshot. Fresh live published theme visually confirmed and remote pulled for normalized hash comparison; REMOTE-INTEGRITY.json records result.
- No fabricated ratings/review counts or pan-India delivery promises copied from visual reference. Native title/price/availability retained. Header/footer real policy/social links only. .in purchase/setup stays owner task. T031 accepted for design scope; T029/T030 catalog/commercial dependencies remain open.
'''
log.write_text(s,encoding='utf-8')
print(json.dumps(proof))
