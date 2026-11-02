from pathlib import Path
import json,re,hashlib
r=Path('F:/Dropshipping');folder=r/'Brand Guidelines';guide=folder/'ROZMISO-BRAND-GUIDELINES.md'
s=guide.read_text(encoding='utf-8');links=re.findall(r'\]\(([^)]+)\)',s)
missing=[x for x in links if not x.startswith(('https://','http://')) and not (folder/x).is_file()]
assert not missing,missing
files=[{'path':p.relative_to(folder).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in folder.rglob('*') if p.is_file()]
report=r/'team/reports/T038';(report/'ASSET-MANIFEST.json').write_text(json.dumps({'guide':str(guide),'missing_links':missing,'files':files},indent=2)+'\n')
p=r/'WORK-LOG.md';log=p.read_text(encoding='utf-8-sig');log=log.replace('Last updated: 29 October 2026.','Last updated: 31 October 2026.')
a=log.index('**Current work:**');b=log.index('\n\n**Social status:**',a)
log=log[:a]+'**Current work:** T038 owner-requested Markdown brand guide saved at Brand Guidelines/ROZMISO-BRAND-GUIDELINES.md with portable11SVG/PNG logo variants, favicons and font licenses. Existing identity/theme consolidated, logo/website colors and typography distinguished, practical new-layout recommendations labeled. Independent asset/link review recorded in T038. No live/store/social changes. T037 video research remains incomplete; its earlier execution journal is preserved and must not be treated as finished or running in the background. T034/T035 launch scopes remain pending.'+log[b:]
log+='\n\n### 31 October2026 — Markdown brand guide T038\n\nOwner requestsbrand/theme/guidelines/logos asMarkdown. Created Brand Guidelines/ROZMISO-BRAND-GUIDELINES.md with brandpositioning,existingcopy,voice,palette,Georgia/DM Sans/outlinedManrope roles, ModernBento direction, logo usage, exactproductimagery, common socialcarousel/video rules andpublicationchecklist. Copiedexisting11SVG+PNGvariants/favicons andManrope/DM Sanslicenses; mainSVGmastersfromauthoritativetheme. Reviewerverifiedall11vector/rasterpairs pixelmatch and existingthemeassetsmatch. AllMarkdownlocalfilelinksresolve; ASSET-MANIFEST.json saved. Sourcebasedguide, notnewliveaudit; proposedpracticalproductionrules distinguished. No brandingredesign orstorepublication. T037video discoverystillincomplete, no backgroundworkerclaimed.\n'
p.write_text(log,encoding='utf-8')
p=r/'team/TASK-BOARD.json';board=json.loads(p.read_text(encoding='utf-8-sig'));board['updated']='2026-10-31'
board['tasks']=[t for t in board['tasks'] if t['id']!='T038']+[{'id':'T038','goal':'Deliver Markdown brand theme/guidelines with portable logos','owner_lane':'Codex + brand_guide_review','reviewer':'brand_guide_review and Codex','status':'ACCEPTED','deliverables':['Brand Guidelines/ROZMISO-BRAND-GUIDELINES.md','team/reports/T038/ASSET-MANIFEST.json'],'runtime':'Existing identity consolidated;11SVG/PNG pairs verified; all local links resolve; no live changes'}]
p.write_text(json.dumps(board,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'guide':str(guide),'local_links_checked':len([x for x in links if not x.startswith('http')]),'missing':missing,'packaged_files':len(files)}))
