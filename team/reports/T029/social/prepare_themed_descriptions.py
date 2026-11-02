"""Prepare consistent local product copy from already reviewed facts; no live writes."""
from pathlib import Path
import json, html

base=Path('F:/Dropshipping/team/reports/T029/social/carousels')
manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
items=[]
care_by_id={
 '10252037324992':'Test a discreet area first and follow the product guidance.',
 '10252037357760':'Test a discreet surface area first. Keep the charging connection dry and follow the included instructions.',
 '10252037390528':'Wipe gently with a soft, damp cloth. Leave open to air-dry before storing. Store empty in a dry place.',
 '10252037456064':'Rinse the bristles after use and let them air-dry. Test suitability on a small area first.',
 '10253181026496':'Rinse after use, let the cloth air-dry and store in a dry place.',
 '10253181092032':'Release the lock gently. Wipe clean when needed and dry before storing.',
 '10253181255872':'Wind cables gently, wipe with a soft cloth and store dry. Cable not included.',
 '10253181321408':'Test a discreet area first. Rinse the cleaning pad and allow it to air-dry.',
 '10253181419712':'Remove debris from the bristles and store clean and dry. Check fabric suitability before use.',
 '10253181518016':'Wipe gently, allow to dry and avoid overfilling. Styling contents are not included.',
 '10253181583552':'Check drain fit before use. Empty and rinse regularly. This catcher is not a watertight plug.',
 '10253181681856':'Use gently and test on a hidden area first. Rinse and air-dry after use.',
 '10253181845696':'Use on a clean, dry surface and check surface compatibility. Wipe gently with a soft cloth.',
 '10253181944000':'Rinse after use and air-dry thoroughly. Keep cloths for separate tasks.',
 '10253182009536':'Close the zipper before washing and follow garment care labels. Air-dry after use.',
 '10257843060928':'Check keyboard fit, wipe with a soft cloth and allow to dry before use.',
 '10257843159232':'Place on a level surface and distribute items evenly. Wipe and dry after cleaning.',
 '10257843224768':'Follow the product instructions. Unplug and allow to cool after use. Keep away from water.',
 '10257843257536':'Wash before first use. Rinse and dry after use. Check lid closure before carrying.',
 '10257843355840':'Rinse after use, clean the strainer slots and dry before storing.',
 '10257843454144':'Keep contents dry, wipe gently with a damp cloth and air-dry before storing. Prints may vary.'
}
for product in manifest['products']:
    pid=product['productId']
    caption=(base/pid/'caption.txt').read_text(encoding='utf-8')
    paragraphs=[p.strip() for p in caption.split('\n\n') if p.strip()]
    facts=paragraphs[1]
    prefix=f'Meet the {product["title"]}. '
    if facts.startswith(prefix): facts=facts[len(prefix):]
    sentences=[s.strip() for s in facts.split('. ') if s.strip()]
    overview=sentences[0].rstrip('.')+'.'
    care=care_by_id[pid]
    if not care.endswith('.'): care+='.'
    url=product['productUrl']
    content=(f'<div class="rozmiso-product-copy"><p>{html.escape(facts)}</p>'
             f'<h3>Use &amp; care</h3><p>{html.escape(care)}</p>'
             f'<h3>Product details</h3><p><a href="{html.escape(url)}">Explore {html.escape(product["title"])} at rozmiso.in</a></p></div>')
    (base/pid/'description.html').write_text(content,encoding='utf-8')
    items.append({'productId':pid,'title':product['title'],'productUrl':url,'descriptionHtml':content,'source':'Reviewed product caption','state':'LOCAL_COPY_REVIEW_PENDING'})
(base/'themed-product-descriptions.json').write_text(json.dumps({'theme':'Rozmiso Everyday Edit','domain':'rozmiso.in','liveWrites':False,'products':items},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'products':len(items),'domain':'rozmiso.in','liveWrites':False}))
