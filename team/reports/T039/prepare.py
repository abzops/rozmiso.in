from pathlib import Path
import json,subprocess,hashlib,urllib.request
root=Path('F:/Dropshipping');out=root/'team/reports/T039';src=Path('C:/Users/Abhinand/Downloads/final-v5')
records=[]
for p in sorted(src.glob('*.mp4')):
 d=out/'frames'/p.stem;d.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',str(p)],capture_output=True,text=True,check=True)
 meta=json.loads(r.stdout);duration=float(meta['format']['duration'])
 interval=max(1,duration/12)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-vf',f'fps=1/{interval},scale=270:-1,tile=4x3','-frames:v','1','-y',str(d/'contact-sheet.jpg')],check=True)
 records.append({'name':p.name,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'metadata':meta,'contactSheet':str(d/'contact-sheet.jpg')})
(out/'VIDEO-INVENTORY.json').write_text(json.dumps(records,indent=2)+'\n')
products=json.load(urllib.request.urlopen('https://rozmiso.myshopify.com/products.json?limit=250',timeout=30))['products']
public=[{'id':p['id'],'title':p['title'],'handle':p['handle'],'body_html':p.get('body_html'),'images':p.get('images'),'variants':[{'id':v['id'],'sku':v.get('sku'),'title':v.get('title'),'price':v.get('price'),'available':v.get('available')} for v in p['variants']]} for p in products]
(out/'PUBLIC-CATALOG.json').write_text(json.dumps(public,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps([{'name':p['name'],'metadata':p['metadata']} for p in records],indent=2))
