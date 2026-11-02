"""Prepare local Instagram handoff assets; never publishes or schedules posts."""
from pathlib import Path
import json, shutil, hashlib
import html
from PIL import Image, ImageOps, ImageDraw

ROOT = Path('F:/Dropshipping')
SOCIAL = ROOT / 'team/reports/T029/social'
GEN = ROOT / 'team/reports/T028/generated'
PACK = SOCIAL / 'instagram-publishing-pack'
PACK.mkdir(exist_ok=True)
products = [
('10252037324992','USB Rechargeable Fabric Shaver','usb-rechargeable-fabric-shaver','A little care for the fabrics you use every day.','A handheld rechargeable fabric shaver for fabric-care routines. Test a discreet area first and follow the product guidance.','HomeCare','05-premium-instagram.png'),
('10252037357760','5-in-1 Rechargeable Cleaning Brush','5-in-1-rechargeable-cleaning-brush','An everyday cleaning essential.','A handheld design with interchangeable heads for kitchen and bathroom routines. Test a discreet area first and keep the charging connection dry.','HomeCare','05-premium-poster.png'),
('10252037390528','Everyday Travel Organizer Pouch','everyday-travel-organizer-pouch','Keep your small essentials together.','A soft zip pouch with a carry handle across the top lid. Use it to gather everyday travel essentials.','TravelEssentials','05-title-features.png'),
('10252037456064','2-in-1 Soap Dispensing Cleaning Brush','2-in-1-soap-dispensing-cleaning-brush','A practical addition to the sink.','A handheld brush with a soap reservoir for everyday cleaning routines. Test a discreet area before use.','KitchenEssentials','05-title-features.png'),
('10253181026496','Microfiber Cleaning Cloth','microfiber-cleaning-cloth-40x40','A cloth for your everyday cleaning routine.','A reusable cleaning cloth for home-care tasks. Rinse after use and let it dry between routines.','HomeCare','05-title-features.png'),
('10253181092032','Reusable Bag Locking Ties, Set of 3','reusable-bag-locking-ties-set-of-3','Keep opened bags gathered together.','Three reusable bag ties for gathering bag openings. Choose a tie that fits the bag and keep it clean between uses.','KitchenEssentials','05-title-features.png'),
('10253181255872','Compact Cable Winder Case','compact-cable-winder-case','Give loose cables a place.','A compact hinged case with a central winding hub. Wind your own cable gently and keep the case dry.','EverydayEssentials','05-title-features-v2.png'),
('10253181321408','Window Groove Cleaning Brush','window-groove-cleaning-brush','Care for the small spaces.','A handheld grip with a folded cleaning pad for window-track cleaning. Check surface suitability before use.','HomeCare','05-premium-instagram.png'),
('10253181419712','Handheld Upholstery Cleaning Brush','handheld-upholstery-cleaning-brush','A brush for your fabric-care routine.','A handheld brush with a long bristled head. Use gentle strokes and test a discreet area on your upholstery first.','HomeCare','05-premium-instagram.png'),
('10253181518016','Foldable Hanging Travel Organizer','foldable-hanging-travel-organizer','Unfold your travel routine.','A foldable organizer with a hanging hook, clear pocket and mesh storage sections for your travel essentials.','TravelEssentials','05-premium-instagram-v2.png'),
('10253181583552','Flexible Flower-Shaped Drain Catcher','flexible-flower-shaped-drain-catcher','A small detail for your sink routine.','A perforated drain catcher with a lifting knob. Check the fit of your drain and clear collected debris regularly. It is not a watertight plug.','KitchenEssentials','features.png'),
('10253181681856','3-in-1 Bottle Lid Cleaning Tool','3-in-1-bottle-lid-cleaning-tool','Care for the corners of your bottle lid.','A compact tool with a brush, narrow cleaning tip and fold-out hook. Check each lid component and clean gently.','KitchenEssentials','features.png'),
('10253181845696','Adhesive Cable Organizer Strips, Set of 20','adhesive-cable-organizer-clips-set-of-20','A place for the cables on your desk.','A set of 20 organizer strips. Each strip has five flower-shaped cable guides; one representative strip is shown. Check the surface before applying.','EverydayEssentials','features.png'),
('10253181944000','Household Wiping Cloths, Set of 3','household-wiping-cloths-set-of-3','Keep a cloth close to your daily routines.','Three patterned wiping cloths for household tasks. Rinse after use and let them dry between routines.','HomeCare','features.png'),
('10253182009536','Structured Mesh Laundry Wash Bag','structured-mesh-laundry-wash-bag','A little structure for laundry day.','A cylindrical wash bag with a mesh lid and zip closure. Follow your garment care instructions and avoid overfilling.','HomeCare','features.png'),
('10257843060928','Keyboard Cover','6187-keyboard-cover-for-computer-pc-for-desktop-computer','Care for the keyboard on your desk.','A flexible translucent film for a desktop keyboard. Check keyboard fit and keep the cover clean.','EverydayEssentials','features.png'),
('10257843159232','Two-Tier Kitchen Storage Rack','2796-2-layer-kitchen-rack-for-holding-and-placing-types-of-things','Two levels for your kitchen essentials.','A compact rack with two slatted shelves. Place it on a stable surface and arrange everyday items with care.','KitchenEssentials','features.png'),
('10257843224768','Electric Hair Straightening Brush','6168-hqt-909b-hair-straightener-used-while-massaging-hair-scalps-and-head-1','A brush for your styling routine.','An electric styling brush with a corded design. Follow the operating instructions, keep it dry and allow it to cool before storing.','PersonalCare','features.png'),
('10257843257536','Stainless Steel Water Bottle','6422-stainless-steel-bottle-used-in-all-households-and-official-purposes-for-storing-water-and-beverages-etc-1','Keep your daily water routine close.','A compact stainless steel bottle with a screw cap. Wash it before first use and let it dry between refills.','EverydayEssentials','features.png'),
('10257843355840','Manual Citrus Juicer with Strainer','2793-manual-hand-juicer-for-making-juices-and-beverages-by-using-hands','A fresh squeeze, by hand.','A manual citrus juicer with a removable strainer and pouring spout. Prepare your citrus by hand and rinse after use.','KitchenEssentials',None),
('10257843454144','Foldable Canvas Laundry and Storage Bag','6186-canvas-laundry-bag-toy-storage-laundry-storage','A place to gather everyday things.','A foldable storage bag with carry handles and a zippered lid. Prints may vary; the illustrated print does not establish a selectable variant.','HomeCare','features.png'),
]
published = {'10252037357760':'https://www.instagram.com/rozmiso.in/p/DebRiNBEyxC/', '10257843355840':'https://www.instagram.com/rozmiso.in/p/DebOPBZk5xo/'}
entries=[]
for number,(pid,title,handle,hook,body,tag,poster) in enumerate(products,1):
    source = (GEN / pid / poster) if poster else SOCIAL / 'juicer-premium-poster.png'
    folder = PACK / f'{number:02d}-{handle}'
    folder.mkdir(exist_ok=True)
    dest = folder / 'poster.png'
    url = 'https://rozmiso.myshopify.com/products/' + handle
    caption = f'{hook}\n\nMeet the {title}. {body}\n\nExplore the product details:\n{url}\n\nStyling props are not included.\n\n#Rozmiso #{tag} #EverydayEdit'
    alt = f'Rozmiso product presentation for {title}, with product photography, a heading and feature labels on an ivory background. Context props are not included.'
    (folder/'caption.txt').write_text(caption,encoding='utf-8')
    (folder/'alt-text.txt').write_text(alt,encoding='utf-8')
    entry=dict(productId=pid,title=title,productUrl=url,sourcePoster=str(source),poster=str(dest),caption=str(folder/'caption.txt'),altText=str(folder/'alt-text.txt'),status='PREVIOUSLY_VERIFIED_PUBLISHED' if pid in published else 'UNPUBLISHED',publishedUrl=published.get(pid),visualReview='PENDING',turnOnAiLabel=False,crosspostPersonalFacebook=False)
    if source.exists():
        shutil.copy2(source,dest)
        entry['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
        with Image.open(dest) as im: entry['dimensions']=list(im.size)
    else:
        entry['missingPoster']=True
    entries.append(entry)
manifest=dict(date='2026-10-13',account='https://www.instagram.com/rozmiso.in/',boundary='Local preparation only. Published URLs are earlier session evidence, not refreshed live verification. No scheduling or new live publication performed.',bio='Thoughtful finds for home, kitchen & travel.\nDiscover your everyday essentials.\nrozmiso.myshopify.com',websiteField='Still requires mobile editing; plaintext caption URLs are not clickable product tags.',entries=entries)
(PACK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# Review thumbnails only. Final posters are unmodified byte-for-byte copies.
available=[e for e in entries if not e.get('missingPoster')]
for start in range(0,len(available),4):
    batch=available[start:start+4]
    sheet=Image.new('RGB',(1400,1500),'#dddddd')
    draw=ImageDraw.Draw(sheet)
    for j,e in enumerate(batch):
        x=(j%2)*700; y=(j//2)*750
        with Image.open(e['poster']) as im:
            im=ImageOps.contain(im.convert('RGB'),(680,700))
            sheet.paste(im,(x+(700-im.width)//2,y+30))
        draw.text((x+10,y+8),e['productId']+' '+e['title'],fill='black')
    sheet.save(PACK/f'review-{start//4+1}.jpg',quality=92)
print(json.dumps({'entries':len(entries),'posters':len(available),'previouslyPublished':len(published),'unpublished':len(entries)-len(published),'missing':[e['productId'] for e in entries if e.get('missingPoster')]}))
cards=[]
for e in entries:
    rel=Path(e['poster']).parent.name
    image=f'<img src="{html.escape(rel)}/poster.png" alt="{html.escape(e["title"])}">' if not e.get('missingPoster') else '<p>Poster pending</p>'
    caption=Path(e['caption']).read_text(encoding='utf-8')
    cards.append(f'<article><h2>{html.escape(e["title"])}</h2><p class="state">{e["status"]}</p>{image}<pre>{html.escape(caption)}</pre><a href="{html.escape(e["productUrl"])}">Product details</a></article>')
(PACK/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Rozmiso Instagram publishing pack</title><style>body{margin:32px;background:#f6f2e9;color:#183c32;font:16px system-ui}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:24px}article{background:white;padding:24px;border-radius:12px}img{width:100%;height:460px;object-fit:contain}pre{white-space:pre-wrap;font:15px system-ui;color:#333}.state{font-size:12px}</style><h1>Rozmiso Instagram publishing pack</h1><p>Local content pack. Two posts previously verified live. Remaining entries are unpublished. Caption URLs are plain text on Instagram; they are not clickable product tags. Keep AI label on and personal Facebook crossposting off.</p><main>'+''.join(cards)+'</main>',encoding='utf-8')

