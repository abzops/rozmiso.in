from pathlib import Path
import json,urllib.request,re,difflib
root=Path('F:/Dropshipping');out=root/'team/reports/T037';out.mkdir(parents=True,exist_ok=True)
products=json.load(urllib.request.urlopen('https://rozmiso.myshopify.com/products.json?limit=250',timeout=35))['products']
(out/'CATALOG-SNAPSHOT.json').write_text(json.dumps(products,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
refs=json.loads((root/'team/reports/T028/reference-review/manifest.json').read_text(encoding='utf-8-sig'))['products']
suppliers=[]
for filename in ['operations/launch-2026-10-05/catalog.json','operations/catalog-expansion-2026-10-06/research/products.json']:
 suppliers+=json.loads((root/filename).read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
queue=[]
for index,p in enumerate(products,1):
 folder=out/f'{index:02d}-{p["handle"][:85]}';folder.mkdir(exist_ok=True)
 ref=next((r for r in refs if str(r.get('numericId'))==str(p['id'])),{})
 ranked=sorted(suppliers,key=lambda s:difflib.SequenceMatcher(None,norm(p['title']),norm(s['title'])).ratio(),reverse=True)
 leads=[{'title':s['title'],'url':s.get('supplier_url') or s.get('source'),'sku':s.get('supplier_sku') or s.get('sku'),'title_similarity':round(difflib.SequenceMatcher(None,norm(p['title']),norm(s['title'])).ratio(),3)} for s in ranked[:2]]
 local=ref.get('localPaths',[])
 if p['handle']=='2-in-1-soap-dispensing-cleaning-brush': local=[str(root/'team/reports/T031/product-reference'/x) for x in ['soap-studio.png','soap-side.png','soap-use.png']]
 item={'index':index,'id':p['id'],'title':p['title'],'handle':p['handle'],'variant_skus':[v.get('sku') for v in p['variants']],'source_reference_images':local,'physical_invariants':ref.get('physicalInvariants'),'supplier_leads':leads,'live_image_urls':[im['src'] for im in p['images']],'folder':str(folder),'status':'READY'}
 (folder/'PRODUCT.json').write_text(json.dumps(item,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');queue.append(item)
(out/'PRODUCT-QUEUE.json').write_text(json.dumps(queue,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps([{'index':p['index'],'title':p['title'],'folder':p['folder']} for p in queue],ensure_ascii=False,indent=2))
