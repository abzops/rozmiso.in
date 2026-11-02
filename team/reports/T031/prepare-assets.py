from pathlib import Path
from PIL import Image
import json,hashlib
root=Path('F:/Dropshipping'); assets=root/'rozmiso-studio-theme/assets'
generated=root/'team/reports/T028/generated'
mapping={
'landing-category-home':generated/'10252037357760/04-use-context.png',
'landing-category-kitchen':generated/'10257843355840/context.png',
'landing-category-travel':generated/'10252037390528/04-use-context.png',
'landing-category-personal':generated/'10252037324992/10252037324992-studio.png',
'landing-category-other':generated/'10253181845696/usecase.png',
'landing-product-soap':root/'team/reports/T031/generated/soap-corrected.png',
'landing-product-lid':generated/'10253181681856/studio.png',
'landing-product-brush':generated/'10252037357760/01-studio-no-cable.png',
'landing-product-cable':generated/'10253181845696/usecase.png'}
for key in ['hero','home','travel']:
    p=root/f'team/reports/T031/generated/{key}.png'
    if p.exists():mapping['landing-'+key]=p
records=[]
for name,path in mapping.items():
    im=Image.open(path).convert('RGB'); im.thumbnail((2200,1200) if name in ['landing-hero','landing-home','landing-travel'] else (800,800))
    out=assets/(name+'.webp');im.save(out,'WEBP',quality=88,method=6)
    records.append({'asset':out.name,'source':str(path),'dimensions':im.size,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(root/'team/reports/T031/ASSETS.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(records)} optimized assets; {sum(x["bytes"] for x in records)} bytes')
