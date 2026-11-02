import json, re, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

root = Path('F:/Dropshipping/team/reports/T035')
base = 'https://rozmiso.myshopify.com'
def fetch(route):
    req = urllib.request.Request(base + route, headers={'User-Agent':'RozmisoLaunchReview/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            return {'status':response.status, 'body':response.read().decode('utf-8'), 'url':response.url}
    except Exception as exc:
        return {'status':getattr(exc,'code',None), 'error':str(exc)}

catalog = fetch('/products.json?limit=250')
products = []
if catalog.get('status') == 200:
    for p in json.loads(catalog['body']).get('products',[]):
        products.append({'id':p['id'], 'handle':p['handle'], 'title':p['title'], 'images':len(p.get('images',[])), 'description_chars':len(re.sub('<[^>]+>', '',p.get('body_html') or '')), 'variants':[{'id':v['id'],'available':v.get('available'),'price':v.get('price')} for v in p['variants']]})

routes = ['/', '/collections/all', '/search?q=brush&type=product', '/pages/contact', '/policies/shipping-policy', '/policies/refund-policy', '/policies/privacy-policy', '/policies/terms-of-service', '/cart.js']
checks=[]
for route in routes:
    r=fetch(route)
    body=r.get('body','')
    checks.append({'route':route,'status':r.get('status'),'bytes':len(body.encode()),'error':r.get('error'), 'title':(re.search(r'<title>(.*?)</title>',body,re.S).group(1).strip() if re.search(r'<title>(.*?)</title>',body,re.S) else None), 'placeholder_markers':sorted(set(re.findall(r'\[(?:INSERT|YOUR|ADD|STORE|EMAIL|ADDRESS)[^\]]*\]|orders are not open|collection preview|coming soon',body,re.I)))[:10]})
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'kind':'Anonymous public HTTP read-only diagnostics, not rendered UI or checkout verification','catalog_status':catalog.get('status'),'product_count':len(products),'available_product_count':sum(any(v['available'] for v in p['variants']) for p in products),'products':products,'routes':checks}
(root/'PUBLIC-CHECK.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'product_count':len(products),'available_products':result['available_product_count'],'fewer_than_six_images':[p['title'] for p in products if p['images']<6],'routes':checks},indent=2))
