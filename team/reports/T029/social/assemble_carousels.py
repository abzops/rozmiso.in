"""Stage unmodified AI slide assets and accurate captions. No live writes."""
from pathlib import Path
import json, shutil, hashlib, html
from PIL import Image
root=Path('F:/Dropshipping')
social=root/'team/reports/T029/social'
gen=root/'team/reports/T028/generated'
dest=social/'carousels'
dest.mkdir(exist_ok=True)
source=json.loads((social/'instagram-publishing-pack/manifest.json').read_text(encoding='utf-8'))
variants={
'10252037324992':['02-detail.png','03-usecase.png','04-use-context.png','06-care.png','10252037324992-studio.png'],
'10252037357760':['02-macro-detail.png','04-use-context.png','03-usecase-no-cable.png','06-care-no-cable.png','01-studio-no-cable.png'],
'10252037390528':['02-detail-v2.png','03-usecase.png','04-use-context.png','06-care-v2.png','01-studio-v2.png'],
'10252037456064':['02-detail.png','03-usecase-v2.png','04-use-context-v2.png','06-care.png','01-studio.png'],
'10253181255872':['02-detail-v2.png','03-usecase.png','04-use-context.png','06-care.png','01-studio.png'],
'10253181321408':['02-detail.png','03-usecase.png','04-use-context.png',None,'01-studio.png'],
}
labels=['Cover and features','Product detail','Primary use','Second context','Care guidance','Product link']
published_path=social/'published-carousels.json'
published=json.loads(published_path.read_text(encoding='utf-8-sig')) if published_path.exists() else {'entries':[]}
published_ids={x['productId'] for x in published['entries']}
footer_fix_ids={'10252037390528','10252037456064','10253181026496','10253181092032','10253181255872','10253181583552','10253181681856','10253181845696','10253181944000','10253182009536','10257843060928','10257843159232','10257843224768','10257843257536','10257843454144'}
items=[]; cards=[]
for e in source['entries']:
    pid=e['productId']; folder=dest/pid; folder.mkdir(exist_ok=True)
    e['productUrl']=e['productUrl'].replace('rozmiso.myshopify.com','rozmiso.in')
    if pid in ['10253181419712','10253181518016']:
        rest=[folder/'02-details.png',folder/'03-usecase.png',folder/'04-context.png',folder/'05-care.png',None]
    elif pid in variants:
        rest=[gen/pid/x if x else folder/'05-care.png' for x in variants[pid]]
    elif int(pid)<10253181583552:
        rest=[gen/pid/x for x in ['02-detail.png','03-usecase.png','04-use-context.png','06-care.png','01-studio.png']]
    else:
        rest=[gen/pid/x for x in ['details.png','usecase.png','context.png','care.png','studio.png']]
    if (dest/'shared/06-product-link.png').exists(): rest[4]=dest/'shared/06-product-link.png'
    cover=Path(e['poster'])
    if pid=='10257843355840' and (folder/'01-cover-v2.png').exists():
        cover=folder/'01-cover-v2.png'
        rest[1]=folder/'03-use-v2.png'
        rest[3]=folder/'05-care-v2.png'
    if (folder/'01-cover-v3.png').exists(): cover=folder/'01-cover-v3.png'
    if (gen/pid/'features-v3.png').exists(): cover=gen/pid/'features-v3.png'
    if (folder/'05-care-v3.png').exists(): rest[3]=folder/'05-care-v3.png'
    if pid=='10252037324992': rest[1],rest[2]=rest[2],rest[1]
    if (folder/'05-care-v4.png').exists(): rest[3]=folder/'05-care-v4.png'
    if (folder/'01-cover-square-v4.png').exists(): cover=folder/'01-cover-square-v4.png'
    if (dest/'shared/06-product-link-in.png').exists(): rest[4]=dest/'shared/06-product-link-in.png'
    inputs=[cover]+rest
    inputs=[folder/f'{n:02d}-square-v4.png' if (folder/f'{n:02d}-square-v4.png').exists() else p for n,p in enumerate(inputs,1)]
    slides=[]; missing=[]
    for n,p in enumerate(inputs,1):
        if p is None or not p.exists(): missing.append(labels[n-1]); continue
        target=folder/f'{n:02d}-slide.png'
        if p.resolve()!=target.resolve(): shutil.copy2(p,target)
        with Image.open(target) as im: dimensions=list(im.size)
        slides.append({'order':n,'role':labels[n-1],'path':str(target),'source':str(p),'dimensions':dimensions,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'altText':f'{e["title"]}: {labels[n-1].lower()}. Context props are not included.'})
    caption=Path(e['caption']).read_text(encoding='utf-8')
    caption=caption.replace('rozmiso.myshopify.com','rozmiso.in')
    caption=caption.replace('Explore the product details:','Swipe through the product details, use contexts and care guidance.\n\nExplore the product details:')
    (folder/'caption.txt').write_text(caption,encoding='utf-8')
    ratios={round(s['dimensions'][0]/s['dimensions'][1],3) for s in slides}
    footer_pending=pid in footer_fix_ids and not (folder/'05-care-v4.png').exists()
    status='MISSING_SLIDES' if missing else 'CARE_FOOTER_CORRECTION_PENDING' if footer_pending else 'ASSETS_COMPLETE_CROP_REVIEW_PENDING'
    item={'productId':pid,'title':e['title'],'productUrl':e['productUrl'],'replacesPost':e.get('publishedUrl'),'status':status,'slides':slides,'missing':missing,'mixedAspectRatios':len(ratios)>1,'caption':str(folder/'caption.txt'),'aiLabel':False,'facebookPersonalCrosspost':False,'facebookPageCrosspostRequired':True,'facebookPageId':'61595107991994','livePublished':pid in published_ids,'publishedVersionMayDiffer':pid in published_ids,'theme':'Rozmiso Everyday Edit / ivory and forest green'}
    (folder/'carousel.json').write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8')
    items.append(item)
    images=''.join(f'<figure><img src="{pid}/{Path(s["path"]).name}" alt="{html.escape(s["altText"])}"><figcaption>{s["order"]}. {html.escape(s["role"])}</figcaption></figure>' for s in slides)
    cards.append(f'<section><h2>{html.escape(e["title"])}</h2><p>{item["status"]}. {len(slides)} / 6 slides. Missing: {html.escape(", ".join(missing))}</p><div class="slides">{images}</div><pre>{html.escape(caption)}</pre><a href="{html.escape(e["productUrl"])}">Product details</a></section>')
manifest={'date':'2026-10-14','account':source['account'],'boundary':'Current local creative revision uses the owner-confirmed future domain rozmiso.in. Owner will purchase/connect domain. Four earlier versions published; inspect publication evidence separately. All remaining slides require footer and crop QA before publishing. Instagram caption URLs are plain text.','products':items}
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(dest/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Rozmiso carousel replacements</title><style>body{margin:32px;background:#f5f0e7;color:#173e33;font:16px system-ui}section{padding:24px;background:white;margin:24px 0;border-radius:12px}.slides{display:flex;gap:16px;overflow:auto}figure{flex:0 0 320px;margin:0}img{width:320px;height:400px;object-fit:contain}figcaption{padding:10px 0}pre{white-space:pre-wrap;font:15px system-ui;max-width:900px}</style><h1>Rozmiso carousel replacements</h1><p>Six ordered slides per product in the Rozmiso Everyday Edit theme. Current domain: rozmiso.in. Local revision; published versions tracked separately. Mixed aspect ratios require composer crop review.</p>'+''.join(cards),encoding='utf-8')
print(json.dumps({'products':len(items),'sixSlideSets':sum(len(x['slides'])==6 for x in items),'partial':[{ 'id':x['productId'],'slides':len(x['slides']),'missing':x['missing']} for x in items if x['missing']]}))

