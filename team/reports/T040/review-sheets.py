from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
r=Path('F:/Dropshipping/team/reports/T040')
for lane in ('creative-a','creative-b'):
 for d in (r/lane).iterdir():
  if not d.is_dir():continue
  files=sorted(d.glob('0[1-5]-*.png'))
  if len(files)!=5:continue
  sheet=Image.new('RGB',(1800,1260),'#ddd9d0');draw=ImageDraw.Draw(sheet)
  for i,p in enumerate(files):
   im=Image.open(p).convert('RGB');im.thumbnail((590,590));x=(i%3)*600;y=(i//3)*630;sheet.paste(im,(x+(600-im.width)//2,y+30));draw.text((x+10,y+8),p.name,fill='black')
  out=r/(d.name+'-review.jpg');sheet.save(out,quality=94);print(str(out))
