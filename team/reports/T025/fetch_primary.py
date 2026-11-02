import urllib.request,json,concurrent.futures,datetime
from pathlib import Path
out=Path('F:/Dropshipping/team/reports/T025')
urls={
'6187':'https://deodap.in/products/6187-keyboard-cover-for-computer-pc-for-desktop-computer',
'2796':'https://deodap.in/products/2796-2-layer-kitchen-rack-for-holding-and-placing-types-of-things-1',
'6168':'https://deodap.in/products/hair-straightener-keratin-ceramic-scalp-massager',
'6422':'https://amd.deodap.com/products/6422-stainless-steel-bottle-used-in-all-households-and-official-purposes-for-storing-water-and-beverages-etc-1'}
def fetch(item):
 sku,url=item
 try:
  req=urllib.request.Request(url+'.js',headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
  with urllib.request.urlopen(req,timeout=25) as r:status=r.status; data=json.loads(r.read());resolved=r.url
  (out/(sku+'-primary.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
  return {'sku':sku,'url':url,'endpoint':url+'.js','resolved':resolved,'httpStatus':status,'accessedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'title':data.get('title'),'variants':[{'sku':v.get('sku'),'title':v.get('title'),'available':v.get('available')} for v in data.get('variants',[])],'images':data.get('images',[]),'description':data.get('description')}
 except Exception as e:return {'sku':sku,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:results=list(executor.map(fetch,urls.items()))
(out/'PRIMARY-FETCH.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2))
