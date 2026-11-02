from pathlib import Path
import json,urllib.request,concurrent.futures,subprocess,hashlib
r=Path('F:/Dropshipping/team/reports/T037');queue=json.loads((r/'PRODUCT-QUEUE.json').read_text(encoding='utf-8'))
def work(p):
 folder=Path(p['folder']); product=folder/'SUPPLIER-PRODUCT.json'
 if not product.exists(): return {'index':p['index'],'status':'NO_RESOLVED_SUPPLIER_PRODUCT'}
 sid=str(json.loads(product.read_text(encoding='utf-8'))['id'])
 url=f'https://cdn-consumer.whatmore.live/v2/brand/78232846646/product-events?client_product_id={sid}&status=live,upcoming&event_type=video,image'
 result={'supplier_product_id':sid,'source_api':url,'permission_source':'https://deodap.in/blogs/news/earn-passive-income-online-in-india-with-deodap-dropshipping','rights':'SUPPLIER_REUSE_STATEMENT_PRESENT_MUSIC_AND_THIRD_PARTY_RIGHTS_NOT_VERIFIED','videos':[]}
 try:
  data=json.load(urllib.request.urlopen(url,timeout=25));(folder/'SUPPLIER-VIDEO-FEED.json').write_text(json.dumps(data,indent=2)+'\n')
  events=[e for e in data.get('events',[]) if e.get('event_type')=='video' and any(str(x.get('client_product_id'))==sid for x in e.get('products',[]))]
  for e in events[:1]:
   media=e.get('event_hls_url') or ''
   if '.mp4' not in media.lower():continue
   dest=folder/'videos';dest.mkdir(exist_ok=True);file=dest/f'supplier-{e["event_id"]}.mp4'
   with urllib.request.urlopen(media,timeout=35) as response:
    if int(response.headers.get('Content-Length','0'))>60*1024*1024:continue
    content=response.read(60*1024*1024+1)
    if len(content)>60*1024*1024:continue
   file.write_bytes(content)
   probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=width,height,codec_name,codec_type','-of','json',str(file)],capture_output=True,text=True)
   metadata=json.loads(probe.stdout) if probe.returncode==0 else {'error':probe.stderr[:250]}
   duration=float(metadata.get('format',{}).get('duration',0));interval=max(1,duration/8)
   sheet=dest/f'supplier-{e["event_id"]}-frames.jpg'
   extract=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(file),'-vf',f'fps=1/{interval},scale=240:-1,tile=4x2','-frames:v','1','-y',str(sheet)],capture_output=True,text=True)
   result['videos'].append({'event_id':e['event_id'],'video_url':media,'downloadPath':str(file),'contactSheet':str(sheet) if sheet.exists() else None,'sha256':hashlib.sha256(content).hexdigest(),'metadata':metadata,'supplier_event_active':e.get('is_active'),'matchStatus':'PENDING_FRAME_REVIEW','source_product_url':next((x.get('product_link') for x in e.get('products',[]) if str(x.get('client_product_id'))==sid),None)})
  result['status']='DOWNLOADED_PENDING_IDENTITY_REVIEW' if result['videos'] else 'NO_TAGGED_DIRECT_MP4'
 except Exception as exc:result['status']='ERROR';result['error']=str(exc)
 (folder/'SUPPLIER-DOWNLOAD.json').write_text(json.dumps(result,indent=2)+'\n')
 return {'index':p['index'],'status':result['status'],'downloads':len(result['videos'])}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(work,queue))
(r/'SUPPLIER-DOWNLOAD-SUMMARY.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
