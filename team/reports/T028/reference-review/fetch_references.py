import json, urllib.request, concurrent.futures, hashlib, datetime
from pathlib import Path
from PIL import Image
root=Path('F:/Dropshipping/team/reports/T028/reference-review')
data=json.loads(Path('F:/Dropshipping/team/reports/T028/products-before.json').read_text(encoding='utf-8-sig'))
products=[p['result'] for p in data]
jobs=[]
for p in sorted(products,key=lambda p:p['status']!='ACTIVE'):
 for i,im in enumerate(p['images'][:2]):jobs.append((p,i,im))
def get(job):
 p,i,im=job; folder=root/p['id'].split('/')[-1]; folder.mkdir(parents=True,exist_ok=True)
 entry={'id':p['id'],'index':i,'url':im['url'],'originalMediaId':im['mediaId'],'accessedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(im['url'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=30) as r: b=r.read();entry['httpStatus']=r.status
  ext='.png' if b.startswith(b'\x89PNG') else '.jpg';path=folder/('reference-'+str(i+1)+ext);path.write_bytes(b)
  with Image.open(path) as img:entry['dimensions']=list(img.size);entry['format']=img.format;img.verify()
  entry.update(localPath=str(path),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
 except Exception as e:entry['error']=str(e)
 return entry
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(get,jobs))
(root/'download-evidence.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({'products':len(products),'downloaded':sum('localPath'in r for r in results),'errors':[r for r in results if'error'in r]},indent=2))
