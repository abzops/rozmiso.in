import json
from pathlib import Path
from datetime import datetime, timezone

folder = Path('F:/Dropshipping/team/reports/T025')
saved = json.loads(Path('F:/Dropshipping/team/reports/T021/saved-products.json').read_text(encoding='utf-8-sig'))
by_sku = {p['result']['variants'][0]['sku'].split('_')[0]:p['result'] for p in saved}
sources = {p['sku']:p for p in json.loads((folder/'PRIMARY-FETCH.json').read_text())}
now = datetime.now(timezone.utc).isoformat()
copy = {
 '6187': {
  'title':'Keyboard Cover',
  'descriptionHtml':'<p>A keyboard cover for placing over the keys of a compatible keyboard.</p><p>Check the shape and key layout against your keyboard before choosing this cover. The keyboard pictured is for illustration and is not included.</p>',
  'uncertainties':['Original DeoDap product endpoint currently returns 404; the public predictive-search endpoint for 6187 returned no products. Current exact supplier availability and compatibility could not be confirmed.','Imported product image visibly identifies a keyboard protector/cover and supplier code 6187. Imported prose describing 108 keys, hand rest, double-injection lettering and mixed lighting is inconsistent with a cover and has been removed.','Material, waterproofing, exact dimensions, supported keyboard models and layout are unverified and omitted. No universal-fit claim.'],
  'evidence':['Imported SKU 6187_laptop_keyboard_cover and supplier-coded product image identify a cover, not an electronic keyboard.','Existing merchant image opened successfully and visually inspected in Chrome: blue keyboard protector package over a keyboard background, code 6187.','Primary public lookup attempted on 2026-10-08; root product .js returned 404; /search/suggest.json?q=6187&resources[type]=product&resources[limit]=10 returned an empty product array.'],
  'images':[]
 },
 '2796': {
  'title':'Two-Tier Kitchen Storage Rack',
  'descriptionHtml':'<p>Arrange jars, bottles and other everyday kitchen items on two raised shelves. The freestanding rack adds storage levels above a counter or shelf.</p><p>Place on a level surface and keep items evenly distributed. Storage items shown in the photos are for illustration.</p>',
  'uncertainties':['Imported exact SKU is 2796_2layer_kitchen_rack. A currently indexed DeoDap page using the old numeric handle describes 2796_4layer_kitchen_rack; this is a different configuration and must not replace the imported two-tier product.','Current exact two-tier supplier page/stock and replacement images could not be verified; root legacy product .js returned 404.','Imported copy says steel, but imagery shows shelf grids and metal-looking legs without proving all components are steel. Material, load capacity, assembled dimensions and weight omitted. Imported 26x26x11 dimensions may describe packaging and do not establish assembled size.','Existing image 1 shows two separate shelf units/box; image 2 depicts two raised platforms. The flat surface below is not counted as an included third shelf.'],
  'evidence':['Imported exact SKU 2796_2layer_kitchen_rack and title establish the original two-tier identity.','Merchant images 1 and 2 opened and visually inspected in Chrome on 2026-10-08; two platforms and metal-looking supports are visible.','DeoDap indexed Gujarati legacy URL describes four layers and a different SKU. This conflicting primary listing was evaluated but its copy/media were excluded.'],
  'images':[]
 },
 '6168': {
  'title':'Electric Hair Straightening Brush',
  'descriptionHtml':'<p>An electric straightening brush with a bristled styling head and handle-mounted temperature adjustment buttons.</p><p>Follow the instructions supplied with the appliance when choosing a heat setting. Unplug and allow the brush to cool fully before cleaning, then wipe with a soft cloth. Store in a dry place.</p>',
  'uncertainties':['Current exact primary SKU matches imported SKU, but supplier stock is not merchant inventory or a dispatch commitment.','Keratin treatment, Seroprotect technology, scalp circulation, guaranteed frizz-free results, minimum heat damage, 50-second heat-up and daily-use safety are unverified marketing claims and omitted.','Imported product weight differs from the current listing; weight and dimensions omitted. Electrical rating, voltage, plug type, maximum temperature, certification and warranty are not established.'],
  'evidence':['Current primary product .js returned HTTP 200 at '+sources['6168']['accessedAt']+' with exact SKU 6168_hqt_909b_hair_straightner.','Supplier image 01_d6c9b631-b50a-4d1f-9957-e2150aea1eba.jpg visually inspected in Chrome: black bristled straightening brush, handle controls and numeric supplier code 6168. Same image filename is present in imported merchant images.','Temperature adjustment and unplug/cool cleaning guidance are described by the exact matched primary supplier listing.'],
  'images':[{'url':'https:'+sources['6168']['images'][1], 'altText':'Black electric hair straightening brush with handle controls', 'exactMatchEvidence':'Exact supplier SKU 6168_hqt_909b_hair_straightner; current supplier image filename matches imported merchant image; Chrome visibly rendered the black brush and supplier code 6168 on 2026-10-08.'}]
 },
 '6422': {
  'title':'Stainless Steel Water Bottle — Approx. 360 ml',
  'descriptionHtml':'<p>A stainless steel water bottle with an approximate 360 ml capacity and a cylindrical design for everyday use.</p><p>Clean with mild dishwashing liquid and a bottle brush, rinse thoroughly and allow to dry. Check the lid is securely closed before carrying.</p>',
  'uncertainties':['Exact supplier SKU matched, but supplier listing currently reports unavailable; this does not change merchant zero stock or prove fulfillment availability.','Approximate 360 ml is corroborated by SKU and visibly labelled supplier image; actual capacity has not been measured.','Leakproof, rust-free, odour-free, 100% food grade, nutrient retention, universal bag/car-holder fit and hot/cold insulation duration are unverified and omitted.','Dimensions/weight may include packing and have not been independently measured; omitted.'],
  'evidence':['AMD DeoDap primary product .js returned HTTP 200 at '+sources['6422']['accessedAt']+' with exact SKU 6422_ss_fancy_btl_360ml_approx.','Primary supplier image 1_b02c8f7a-8e68-4034-9e25-b090d98c3b26.jpg rendered in Chrome and visually inspected: gray cylindrical bottle with lid and label 360 ML Approx, code 6422. Filename exactly matches imported merchant image.','Primary description identifies stainless steel and advises mild detergent and bottle-brush cleaning.'],
  'images':[{'url':'https:'+sources['6422']['images'][1], 'altText':'Gray stainless steel water bottle with lid, approximately 360 ml', 'exactMatchEvidence':'Exact SKU 6422_ss_fancy_btl_360ml_approx; supplier and imported merchant image filenames match; Chrome visibly rendered bottle, code 6422 and 360 ML Approx on 2026-10-08.'}]
 }
}
result=[]
for sku,c in copy.items():
 original=by_sku[sku]
 result.append({'id':original['id'],'originalTitle':original['title'],'title':c['title'],'descriptionHtml':c['descriptionHtml'],'sourceUrl':sources[sku]['url'],'sourceEvidence':{'accessDate':'2026-10-08','preparedAt':now,'sku':original['variants'][0]['sku'],'observations':c['evidence'],'evidenceFiles':['PRIMARY-FETCH.json','T021/saved-products.json'],'visualUrls':[original['images'][0]['url']] if sku in ['6187','2796'] else [c['images'][0]['url']]},'uncertainties':c['uncertainties'],'imageCandidates':c['images']})
(folder/'products.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert len(result)==4 and len({p['id'] for p in result})==4
assert all('price' not in p and 'inventory' not in p and 'status' not in p for p in result)
print(json.dumps({'entries':len(result),'titles':[p['title'] for p in result],'replacementCandidates':sum(len(p['imageCandidates']) for p in result)},indent=2))
