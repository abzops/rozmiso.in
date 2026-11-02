from pathlib import Path
import json, urllib.request, concurrent.futures,re
root=Path('F:/Dropshipping/team/reports/T037')
queue=json.loads((root/'PRODUCT-QUEUE.json').read_text(encoding='utf-8'))
def check(p):
 folder=Path(p['folder'])
 urls=[x['url'] for x in p['supplier_leads'] if x['url'] and x['title_similarity']>.85]
 if p['index']<=6: urls=['https://deodap.in/products/'+p['handle']]
 found=[]
 for url in list(dict.fromkeys(urls)):
  try:
   req=urllib.request.Request(url+'.js',headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=25) as res: data=json.load(res)
   (folder/'SUPPLIER-PRODUCT.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
   media=[m for m in data.get('media',[]) if m.get('media_type') in ('video','external_video')]
   links=re.findall(r'https?://[^\s"<>]+',data.get('description') or '')
   found.append({'url':url,'status':'READ','title':data.get('title'),'media':media,'descriptionVideoLinks':[x for x in links if any(s in x.lower() for s in ['youtu','video','drive.google','instagram','facebook','tiktok'])]})
  except Exception as e: found.append({'url':url,'status':'ERROR','error':str(e)})
 result={'productId':p['id'],'supplierReads':found,'downloadOrReuseRights':'NOT_ESTABLISHED'}
 (folder/'SUPPLIER-MEDIA-SCAN.json').write_text(json.dumps(result,indent=2)+'\n')
 return {'index':p['index'],'videos':sum(len(x.get('media',[])) for x in found),'sources':len(found)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 result=list(pool.map(check,queue))
(root/'SUPPLIER-SCAN-SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
