from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json
out=Path(__file__).parent
base=Path(r'F:\Dropshipping\team\reports\T029\social\carousels')
refs=Path(r'F:\Dropshipping\team\reports\T028\reference-review')
ps=json.loads((base/'manifest.json').read_text(encoding='utf-8-sig'))['products']
for group in range(3):
    sheet=Image.new('RGB',(1400,1400),'#eeeeee')
    for i,p in enumerate(ps[group*7:(group+1)*7]):
        pid=p['productId']; source=next(iter(sorted((refs/pid).glob('reference-1.*'))))
        im=Image.open(source).convert('RGB'); im=ImageOps.contain(im,(330,650))
        x=(i%4)*350;y=(i//4)*700
        sheet.paste(im,(x+(350-im.width)//2,y+35))
        ImageDraw.Draw(sheet).text((x+5,y+5),pid,fill='black')
    sheet.save(out/f'references-{group+1}.jpg',quality=93)
