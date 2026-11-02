from pathlib import Path
import json

root=Path('F:/Dropshipping')
pack=root/'team/reports/T029/social/instagram-publishing-pack'
path=pack/'manifest.json'
manifest=json.loads(path.read_text(encoding='utf-8'))
for entry in manifest['entries']:
    entry['visualReview']='PASS_LOCAL_ROOT_POSTER_REVIEW'
    entry['captionReview']='PASS_LOCAL_FACTUAL_COPY'
    entry['publishingDependency']='Fresh authenticated Instagram browser access; verify product URL before sharing'
manifest['localStatus']='21 product posters and captions prepared; no additional live publication this session'
path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
board_path=root/'team/TASK-BOARD.json'
board=json.loads(board_path.read_text(encoding='utf-8-sig'))
board['updated']='2026-10-13'
task=next(t for t in board['tasks'] if t['id']=='T029')
task['status']='WAITING'
task['current_priority']='Finish Instagram, per latest user instruction'
task['runtime']='Workers stopped with credit errors; Computer Use native pipe missing after retry/reset. No working authenticated Instagram publishing connector confirmed.'
task['instagram']={'localProductPosters':21,'previouslyVerifiedPublished':2,'remainingUnpublished':19,'websiteField':'Mobile edit still needed; caption URLs are plain text','evidence':'team/reports/T029/social/instagram-publishing-pack/manifest.json'}
task['next_steps']=['Restore authenticated browser/computer access; verify Instagram account and two existing posts','Publish the 19 remaining approved posters with captions/URLs/alt text and AI label; verify each permalink','Complete clickable profile website field in mobile editor; inspect highlights and pinned content','Resume bottle-tool unsaved picker and replace rejected pouch hero in Shopify','Facebook Page final policy acceptance remains pending']
board_path.write_text(json.dumps(board,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review_path=root/'team/reports/T029/root-review-progress.json'
review=json.loads(review_path.read_text(encoding='utf-8-sig'))
for p in review['products']:
    if p['id']=='10252037357760': p['details']='Six public thumbnails and all six alt texts saved in prior same-day session; not refreshed this session.'
    if p['id']=='10252037390528':
        p.update(result='CHANGES_REQUIRED_LIVE_HERO_REPLACEMENT',gallery='PREVIOUSLY_SAVED_SIX_WITH_REJECTED_HERO',selected=['01-studio-v2','02-detail-v2','03-usecase','04-use-context','05-title-features','06-care-v2'],details='Root reviewed corrected local hero: top-lid handle accurate, front sidewall clear. Upload-ready copy replaced. Live attachment replacement pending browser restoration.')
    if p['id']=='10253181583552': p.update(gallery='PREVIOUSLY_SAVED_LIVE_SIX',details='Six public thumbnails verified in prior same-day session; not refreshed this session.')
    if p['id']=='10253181681856': p.update(gallery='FILE_PICKER_UPLOAD_DONE_SAVE_PENDING',details='Four new files uploaded to picker before connection loss; Done/product Save/public verification unconfirmed.')
review_path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=root/'WORK-LOG.md'
with log.open('a',encoding='utf-8') as f:
    f.write('\n\n### 13 October 2026 — Instagram priority and connection handoff\n\nUser explicitly prioritizes finishing Instagram. Read startup log/charter/task board; RTK remains unavailable. No live mutations made in this resumed session: native Computer Use pipe failed, retried once, reset/reinitialized runtime and failed again. Earlier extension browser tools absent. Shopify schema request timed out after 300 seconds. Plugin discovery found unconnected browser alternatives, but none supplies confirmed authenticated Instagram access. Worker sessions reported workspace-credit errors and are not running.\n\nPrepared all 21 referenced-product Instagram entries, including 19 unpublished entries and 2 earlier verified live posts. Reused 17 accepted AI posters and generated four missing premium matching posters through built-in imagegen; reviewed typography, composition and product geometry. Corrected hanging-organizer suspension to use the actual S-hook. Captions contain product URLs, factual care notes, preview/orders-closed wording and AI/prop disclosures; alt text supplied. Caption URLs are plain text and do not establish shopping tags. Seven unreferenced drafts excluded. Evidence: team/reports/T029/social/instagram-publishing-pack/index.html, manifest.json and root-instagram-generation.json.\n\nEarlier live evidence remains: juicer DebOPBZk5xo and cleaning brush DebRiNBEyxC; logo, bio and Business conversion. No fresh verification this session. Remaining: publish 19, verify permalinks/profile, mobile website field, highlights/pinned content. Task board T029 set WAITING for authenticated browser access.\n\nCatalog correction: reviewed corrected pouch 01-studio-v2.png and replaced local upload-ready hero copy, but live replacement is still pending. Prior pouch hero acceptance is superseded. Bottle-tool picker uploads remain unsaved/unverified. Root-review-progress.json corrected accordingly. Resume Instagram first after restoring access, then these Shopify actions. Facebook prepared Page still awaits specific policy-acceptance confirmation.\n')
print(json.dumps({'packEntries':len(manifest['entries']),'unpublished':19,'boardStatus':task['status'],'liveMutationsThisSession':0}))
