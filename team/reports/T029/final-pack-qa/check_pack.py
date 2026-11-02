import json, re, hashlib
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
base=Path(r'F:\Dropshipping\team\reports\T029\social\carousels')
out=Path(__file__).parent
manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8-sig'))
issues=[]
texts=[]
for product in manifest['products']:
    pid=product['productId']
    for kind in ['caption.txt','description.html']:
        path=base/pid/kind
        body=path.read_text(encoding='utf-8-sig')
        texts.append({'id':pid,'title':product['title'],'kind':kind,'text':body})
        for forbidden in ['myshopify.com','AI-generated','AI generated','collection preview','orders are not open','orders not open']:
            if forbidden.lower() in body.lower(): issues.append({'id':pid,'text':kind,'issue':forbidden})
        if 'https://rozmiso.in/products/' not in body: issues.append({'id':pid,'text':kind,'issue':'missing .in product URL'})
    tiles=[]
    for slide in product['slides']:
        path=Path(slide['path'])
        im=Image.open(path).convert('RGB')
        if im.width!=im.height: issues.append({'id':pid,'slide':slide['order'],'issue':'non-square','size':im.size})
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=slide['sha256']: issues.append({'id':pid,'slide':slide['order'],'issue':'manifest hash drift'})
        tile=Image.new('RGB',(450,480),'#eeeeee')
        thumb=ImageOps.contain(im,(450,450))
        tile.paste(thumb,((450-thumb.width)//2,30+(450-thumb.height)//2))
        ImageDraw.Draw(tile).text((8,8),f'{pid} / {slide["order"]}',fill='black')
        tiles.append(tile)
    sheet=Image.new('RGB',(1350,960),'white')
    for i,tile in enumerate(tiles): sheet.paste(tile,((i%3)*450,(i//3)*480))
    sheet.save(out/f'{pid}.jpg',quality=94)
(out/'structural-results.json').write_text(json.dumps({'products':len(manifest['products']),'issues':issues},indent=2),encoding='utf-8')
(out/'all-copy.json').write_text(json.dumps(texts,indent=2),encoding='utf-8')
print(json.dumps({'products':len(manifest['products']),'issues':issues},indent=2))
