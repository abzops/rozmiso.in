from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,html,hashlib
base=Path('F:/Dropshipping/team/reports/T032')
styles=['Editorial Classic','Quiet Gallery','Warm Lifestyle','Precision Utility','Modern Bento','Botanical Calm','Heritage Catalogue','Studio Contrast','Story-led Split','Minimal Conversion']
files=[]
for n,title in enumerate(styles,1):
    found=list((base/'concepts').glob(f'{n:02d}-*.png'))
    if len(found)!=1:raise RuntimeError(f'Expected one concept{n:02d}, found{len(found)}')
    files.append((n,title,found[0]))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
for start in [0,5]:
    sheet=Image.new('RGB',(1900,760),'#eae5da');draw=ImageDraw.Draw(sheet)
    for col,(n,title,p) in enumerate(files[start:start+5]):
        draw.text((col*380+14,14),f'{n:02d}  {title}',font=font,fill='#173e33')
        im=Image.open(p).convert('RGB'); im.thumbnail((352,668))
        x=col*380+14+(352-im.width)//2;y=57
        sheet.paste(im,(x,y));draw.text((col*380+14,730),'Open full-size image to inspect details',font=small,fill='#4e5349')
    sheet.save(base/f'comparison-{start+1:02d}-{start+5:02d}.jpg',quality=94)
manifest=[]
cards=[]
for n,title,p in files:
    rel=p.relative_to(base).as_posix();escaped=html.escape(title)
    manifest.append({'number':n,'name':title,'path':str(p),'dimensions':Image.open(p).size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'OWNER_APPROVAL_CONCEPT_NOT_LIVE'})
    cards.append(f'<article><a href="{rel}" target="_blank"><h2>{n:02d} · {escaped}</h2><img src="{rel}" alt="Style {n:02d}: {escaped}" loading="lazy"></a><button data-style="{n:02d} · {escaped}">Select {n:02d}</button></article>')
(base/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rozmiso · Product page approval</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f0e7;color:#173e33;font:15px Arial,sans-serif}header{padding:36px 5%;border-bottom:1px solid #cfc9bb}h1{font:40px Georgia;margin:10px 0}p{max-width:900px;line-height:1.6}main{padding:30px 4%;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:22px}article{background:white;padding:12px;border:1px solid #d5d0c5;border-radius:10px}h2{font-size:16px;line-height:1.4}a{color:inherit;text-decoration:none}img{display:block;width:100%;height:auto}button{border:0;border-radius:6px;background:#173e33;color:white;padding:12px;width:100%;cursor:pointer;margin-top:14px}button:focus-visible,a:focus-visible{outline:3px solid #8eac78;outline-offset:4px}#selection{position:sticky;top:0;background:#173e33;color:white;padding:16px 5%;z-index:2}details{padding:22px 5%}details img{max-width:1000px}footer{padding:25px 5%}@media(max-width:1100px){main{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:650px){main{grid-template-columns:repeat(2,minmax(0,1fr))}h1{font-size:30px}}</style><header><small>ROZMISO / PRODUCT PAGE DESIGN REVIEW / 22 OCTOBER 2026</small><h1>Choose your product-page direction.</h1><p>Ten generated full-page desktop concepts using the same product and ivory/forest brand family. Click any image for full size. These are approval mockups; no live product-page or stock changes. Proposed purchase buttons illustrate layout only. Final copy, media accuracy, available variants and delivery/policy details require implementation verification.</p></header><div id="selection" role="status">Choose a style below, then tell Codex its number in chat.</div><details><summary>View the current product page screenshot</summary><a href="screenshots/current-product-full-clean.png" target="_blank"><img src="screenshots/current-product-full-clean.png" alt="Current product page full screenshot"></a></details><main>'''+''.join(cards)+'''</main><footer>Original product geometry remains authoritative. Generated details must be reviewed before publication. Prompts and sources are retained in the lane reports. Selecting here is local only; send the chosen number in chat.</footer><script>document.querySelectorAll('button[data-style]').forEach(b=>b.onclick=()=>{document.getElementById('selection').textContent='Your selection: '+b.dataset.style+'. Tell Codex this number in chat; no live changes have been made.';});</script></html>'''
(base/'APPROVAL.html').write_text(doc,encoding='utf-8')
print('Built10-concept manifest, approval gallery and2 comparison sheets.')
