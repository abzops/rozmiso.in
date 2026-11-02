from pathlib import Path
import json, hashlib

root=Path('F:/Dropshipping')
source=root/'rozmiso-studio-theme'
backup=root/'team/reports/T030/backups/before-customer-fixes'
digest=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
changed=[]
for p in source.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(source); old=backup/rel
    if not old.exists() or p.read_bytes()!=old.read_bytes():
        changed.append({'path':rel.as_posix(),'sha256':digest(p),'beforeSha256':digest(old) if old.exists() else None})
(root/'team/reports/T030/CHANGED-FILES.json').write_text(json.dumps(changed,indent=2)+'\n',encoding='utf-8')

p=root/'team/reports/T029/social/published-carousels.json'
data=json.loads(p.read_text(encoding='utf-8-sig'))
for rev in data.get('revisions',[]):
    entry=next(e for e in data['entries'] if e['productId']==rev['productId'])
    if entry['metaContentId']!=rev['metaContentId']:
        entry.setdefault('previousVersions',[]).append({k:entry[k] for k in ('metaContentId','instagramUrl') if k in entry})
        entry.pop('instagramUrl',None)
        entry.update({k:rev[k] for k in ('metaContentId','plannerTime','status','domain','instagramUrl') if k in rev})
p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

p=root/'team/TASK-BOARD.json'; board=json.loads(p.read_text(encoding='utf-8-sig'))
def walk(value):
    if isinstance(value,dict):
        if value.get('id')=='T030':
            value.update(current_priority='Theme 159259001024 LIVE via CLI; catalog API approval pending',runtime='Theme Check clean; 11/11 regression tests PASS; 40-file remote integrity PASS; mobile customer checks completed',next_steps=['Obtain pending CLI Connector installation approval, then restart catalog authorization','Upload and verify 21 six-image galleries and themed descriptions','Verify genuine stock, fulfillment, policies and payment/order flow before purchase-readiness acceptance'])
        if value.get('id')=='T029':
            value['next_steps']=['Update remaining Facebook Page website field to .in','Complete Shopify galleries/descriptions through T030; connector approval pending']
            value['facebook']['mobileVerification']='Owner confirmed auto-sharing enabled; all21 product posts verified as paired Planner publications'
        for child in value.values(): walk(child)
    elif isinstance(value,list):
        for child in value: walk(child)
walk(board);p.write_text(json.dumps(board,indent=2)+'\n',encoding='utf-8')

p=root/'WORK-LOG.md'; log=p.read_text(encoding='utf-8-sig')
start=log.index('**Current work:**'); end=log.index('**Store readiness:**',start)
log=log[:start]+'''**Current work:** T030 customer website review. Revised theme159259001024 is LIVE, independently confirmed by Shopify CLI on14 October. Theme Check clean;11/11 regression fixtures PASS; all40 source files matched the remote draft before publication. Source, mobile discovery/search/filter/gallery/menu/contact checks and desktop visual review completed within stated limits. Detailed report: team/reports/T030/WORK-REPORT.md.

**Social status:** All21 active referenced products have current six-slide carousels on Instagram and Facebook, paired Planner publications verified. Instagram profile21 posts verified. Original two Instagram single-image posts and four superseded Instagram carousels deleted; four superseded Facebook versions moved to recoverable recycle bin. New versions use rozmiso.in. Instagram bio corrected. Facebook Page website field still needs .in; Instagram clickable website field requires mobile edit. Manual AI toggle remains off; platform automatic provenance labeling may apply.

**Catalog handoff:** All21 product-specific six-image sets (126 images, shared social CTA excluded) and21 matching HTML descriptions are ready locally at team/reports/T030/catalog-ready/manifest.json, NOT uploaded by T030. Correct pouch hero and new upholstery/organizer studio frames included. Older live galleries remain partially updated/mixed. Shopify theme CLI authentication works. Product CLI needs the Shopify CLI Connector App installation: read/write Products and displayed store-owner data access, accepting API Terms. Explicit approval question pending; old OAuth callback timed out, so restart authorization only after approval. No connector installation completed.

''' + log[end:]
log=log.replace('| Current published theme | rozmiso-studio-brand-2026-10-06, ID 158950424768 |','| Current published theme | Rozmiso Studio - Customer Review 2026-10-14, ID159259001024; previous158950424768 retained unpublished for rollback |')
log+='''
### 14 October 2026 — CLI website review published and verified

- Used official Shopify CLI4.9.3 through npx as requested. Pulled previous live39-file backup; integrated bounded reviewer fixes into authoritative source. Published new theme159259001024 after strict pushes, Theme Check and full40-file remote comparison. Fresh CLI theme list confirms role live; previous158950424768 retained unpublished. This supersedes the earlier journal's UNPUBLISHED draft state.
- Fixed native submitted search, overlapping supplier-category filters (including comma punctuation), coherent variant/quantity/gallery states, guarded navigation, mobile gallery fit, visible focus, common ivory/forest serif styling and factual final public copy. Removed unsupported preview/orders-not-open wording without inventing stock or disabling commerce protections. Mobile card title adjusted14px. No payment, inventory, domain or policy commercial facts changed.
- Root reran11 regression fixtures: PASS. Theme Check output[]; remote integrity40 files, missing0, mismatches0. Tested390px/320px mobile search/filter/sort/reset, gallery/zoom, menu/bag Escape, enquiry prefill and empty contact required-field validation; no real message or order sent. Fresh live homepage screenshot inspected and saved. Full checkout/payment/delivery/refund and contact delivery are not verified; no claim of perfect website or WCAG certification.
- Consolidated four current social publication IDs into primary records while preserving superseded metadata. All21 current posts on both destinations; old social cleanup complete. Facebook Page website field remains pending.
- Product catalog126 images +21 descriptions ready locally, not uploaded. CLI Connector approval pending due new application access/API Terms; authorization callback expired without installation. Restart only after owner answer. Owner retains domain purchase/setup. T029/T030 remain IN_PROGRESS for these outstanding scopes.
- Evidence: team/reports/T030/WORK-REPORT.md, CHANGED-FILES.json, DRAFT-INTEGRITY.json, live-baseline/, draft-verification/, screenshots/01-live-home-desktop.png, screenshots/03-contact-mobile-390.png, catalog-ready/manifest.json; T029/social/published-carousels.json.
'''
p.write_text(log,encoding='utf-8')
