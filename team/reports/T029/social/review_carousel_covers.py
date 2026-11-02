"""Build review-only contact sheets; never modifies final media."""
from pathlib import Path
import json
from PIL import Image, ImageOps, ImageDraw
p=Path('F:/Dropshipping/team/reports/T029/social/carousels')
products=json.loads((p/'manifest.json').read_text(encoding='utf-8'))['products']
out=p/'review-only'; out.mkdir(exist_ok=True)
for start in range(0,len(products),4):
    canvas=Image.new('RGB',(1200,1540),'#eee9e0'); d=ImageDraw.Draw(canvas)
    for j,entry in enumerate(products[start:start+4]):
        im=ImageOps.contain(Image.open(entry['slides'][0]['path']),(590,730))
        x=(j%2)*600; y=(j//2)*770
        canvas.paste(im,(x+(590-im.width)//2,y))
        d.text((x+8,y+733),f"{entry['productId']} / {entry['title']}",fill='black')
    canvas.save(out/f'covers-{start//4+1}.jpg')
print('Six review-only cover sheets saved.')
