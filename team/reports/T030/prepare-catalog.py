from pathlib import Path
import json, shutil, hashlib
from PIL import Image

base=Path('F:/Dropshipping')
social=base/'team/reports/T029/social/carousels'
generated=base/'team/reports/T028/generated'
dest=base/'team/reports/T030/catalog-ready'
data=json.loads((social/'manifest.json').read_text(encoding='utf-8'))
special={
 '10252037324992':'10252037324992-studio.png',
 '10252037357760':'01-studio-no-cable.png',
 '10252037390528':'01-studio-v2.png',
}
out=[]
for product in data['products']:
    pid=product['productId']; folder=dest/pid; folder.mkdir(parents=True,exist_ok=True)
    if pid in ('10253181419712','10253181518016'):
        studio=social/pid/'00-studio-v4.png'
    else:
        studio=generated/pid/special.get(pid,'01-studio.png' if int(pid)<10253181583552 else 'studio.png')
    selected=[studio]+[social/pid/f'{n:02d}-slide.png' for n in (2,3,4,1,5)]
    record={'productId':pid,'title':product['title'],'productUrl':product['productUrl'],'images':[],'missing':[],'state':'LOCAL_READY_NOT_UPLOADED'}
    for index,source in enumerate(selected,1):
        if not source.exists():record['missing'].append(str(source));continue
        target=folder/f'{index:02d}-product.png';shutil.copy2(source,target)
        with Image.open(target) as image: dimensions=list(image.size)
        record['images'].append({'order':index,'path':str(target),'source':str(source),'dimensions':dimensions,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    description=social/pid/'description.html'
    shutil.copy2(description,folder/'description.html')
    record['descriptionHtml']=str(folder/'description.html')
    if record['missing']:record['state']='LOCAL_INCOMPLETE'
    out.append(record)
dest.mkdir(exist_ok=True)
(dest/'manifest.json').write_text(json.dumps({'date':'2026-10-14','boundary':'Six product-specific images per gallery; shared social CTA excluded. AI-generated imagery based on supplied references. No live edits performed by this script.','products':out},indent=2),encoding='utf-8')
print(json.dumps({'products':len(out),'complete':sum(len(x['images'])==6 for x in out),'missing':[(x['productId'],x['missing']) for x in out if x['missing']]}))
