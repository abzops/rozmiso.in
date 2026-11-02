from pathlib import Path
import json,shutil,hashlib
from PIL import Image
r=Path('F:/Dropshipping'); task=r/'team/reports/T033'; records=json.loads((task/'media-prompts.json').read_text())
rows=[{'name':'use','source':str(r/'team/reports/T031/generated/soap-corrected.png'),'review':'ROOT_AND_INDEPENDENT_VISIBLE_IDENTITY_PASS'}]+records
for row in rows:
    original=Path(row['source']); dest=task/'generated'/(row['name']+'.png')
    shutil.copy2(original,dest)
    im=Image.open(dest).convert('RGB');im.thumbnail((1400,1400))
    out=r/'rozmiso-studio-theme/assets'/('bento-soap-'+row['name']+'.webp');im.save(out,'WEBP',quality=89,method=6)
    row.update(saved=str(dest),asset=out.name,dimensions=im.size,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest())
(task/'MEDIA.json').write_text(json.dumps(rows,indent=2)+'\n')
print(f'{len(rows)} product-specific images saved and optimized.')
