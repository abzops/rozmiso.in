from pathlib import Path
import json, hashlib
root=Path('F:/Dropshipping')
report=root/'team/reports/T035'
checks=json.loads((report/'PUBLIC-CHECK.json').read_text())
config={
 'status':'PREPARATION_ONLY_NOT_LAUNCH_READY',
 'owner_shipping_instruction':{'amount_inr':70,'basis':None,'status':'Owner confirmed70rupees for every product; two-item order total70 versus140 question pending','applied_to_shopify':False},
 'payment_activation':'NOT_VERIFIED',
 'dispatch_time':None,'return_terms':None,
 'products':[{'id':p['id'],'handle':p['handle'],'title':p['title'],'publicly_available':any(v['available'] for v in p['variants']),'supplier_confirmed_quantity':None,'native_images':p['images'],'launch_approved':None} for p in checks['products']],
 'access':{'theme_cli':'WORKING','admin_api':'No stored app authentication on read-only CLI query','browser':'Disabled tool response','shopify_plugin':'Directory reports installed:false; suggested to owner'},
 'publication':'Modern Bento remains unpublished; no stock or shipping changes applied'
}
(report/'LAUNCH-CONFIG.json').write_text(json.dumps(config,indent=2)+'\n')
source=root/'rozmiso-studio-theme/layout/theme.liquid'
pulled=root/'team/reports/T033/remote-verified/layout/theme.liquid'
normalize=lambda p:'\n'.join(p.read_text(encoding='utf-8-sig').splitlines())
integrity={'themeId':159555977408,'state':'UNPUBLISHED','file':'layout/theme.liquid','normalized_match':normalize(source)==normalize(pulled),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pulled_sha256':hashlib.sha256(pulled.read_bytes()).hexdigest(),'official_strict_theme_check':'No findings'}
assert integrity['normalized_match']
(report/'DRAFT-INTEGRITY.json').write_text(json.dumps(integrity,indent=2)+'\n')
board_path=root/'team/TASK-BOARD.json';board=json.loads(board_path.read_text(encoding='utf-8-sig'))
for task in board['tasks']:
 if task['id']=='T035':
  task['status']='WAITING'
  task['current_priority']='Bounded preparation complete; await shipping basis, genuine stock/payment/policy facts and admin/browser access'
  task['runtime']='Public21products/0available;10native galleries below6;3policy404.126local image hashes verified; obsolete soap held with6corrected replacements. Draft SEO fix strict-check/pullback PASS. No launch claimed.'
board_path.write_text(json.dumps(board,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
log_path=root/'WORK-LOG.md';log=log_path.read_text(encoding='utf-8-sig')
start=log.index('**Current work:**');end=log.index('\n\n**Social status:**',start)
log=log[:start]+'**Current work:** T035 launch preparation completed within available access; launch WAITING. Current public read-only check:21products/0available,10native galleries below6; shipping/refund/terms404. Two independent workers reviewed source and operations.126local image hashes/21descriptions verified; obsolete soap set held and6corrected replacements referenced. Safe system-page SEO correction strict-pushed to unpublished159555977408 and pulled back matching. Live159552962752 unchanged. Owner confirms shipping70INR; per-order versus per-item clarification pending. Stock, fulfillment, payment activation and policy facts still needed. Browser disabled and CLI Admin app auth absent; plugin directory reports Shopify not installed for current integration, suggestion issued. See T035/WORK-REPORT.md and LAUNCH-CONFIG.json. T034 rendered comparison remains pending.'+log[end:]
log+='\n\n### 22 October2026 — Launch preparation evidence and shipping instruction\n\n- Bounded workers completed source/operations review;126image hashes and21description files verified. Six corrected soap references prepared; obsolete soap gallery HOLD retained. Native catalog media still require Admin upload.\n- Fixed stale system-page metadata fallback for index/search/cart/list-collections/404 while preserving custom product/collection/page SEO. Shopify CLI strict check clean; uploaded only layout/theme.liquid to unpublished159555977408, pulled back matching. No new public theme publication.\n- Owner states shipping70rupees for every product. Asked whether two-item order totals70 or140; amount recorded but basis pending, no rate applied.\n- Fresh read-only Admin query failed: no stored app auth. Integration directory reports Shopify installed:false; suggestion issued. Browser still disabled. Public contact[email] marker was legitimate form input, not a content defect. Missing policies and0available are current public findings; old billing/provider/rate observations remain historical and need fresh admin verification.\n- Launch not complete: no invented stock/policies, no guard removal, no payment or order sent. Exact current owner inputs and access blockers saved in T035.\n'
log_path.write_text(log,encoding='utf-8')
print(json.dumps(integrity))
