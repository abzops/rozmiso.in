from pathlib import Path
import json
root = Path('F:/Dropshipping')
path = root/'team/reports/T035/LAUNCH-CONFIG.json'
data = json.loads(path.read_text())
data['owner_shipping_instruction'] = {
 'amount_inr':70,
 'basis':'FLAT_PER_ORDER',
 'status':'Latest owner correction22October2026: total70INR per order; supersedes previous per-item answer',
 'calculation':'70 per order regardless of item quantity',
 'examples':[{'items':1,'shipping_inr':70},{'items':2,'shipping_inr':70},{'items':3,'shipping_inr':70}],
 'applied_to_shopify':False
}
path.write_text(json.dumps(data,indent=2)+'\n')
path=root/'WORK-LOG.md'
log=path.read_text(encoding='utf-8-sig')
log=log.replace('Owner confirms shipping70INR per item:2items140INR,3items210INR. Basis resolved; Shopify rate not yet configured.', 'Latest owner correction: shipping70INR total per order regardless of item quantity; supersedes previous per-item answer. Shopify rate not yet configured.')
log+='\n\n### 22 October2026 — Shipping corrected to flat70INR per order\n\nLatest owner message "no total70" supersedes the earlier per-item answer. Authoritative rule:70INR total shipping per order, regardless of item quantity. One, two or three items each have70INR total shipping. Corrected T035/LAUNCH-CONFIG.json and task board. Previous dated per-item journal entries are preserved as superseded history. No Shopify rate had been changed, so no live rate rollback was needed. Configure flat70INR rate and verify one-item and multi-item carts after Admin access is available.\n'
path.write_text(log,encoding='utf-8')
path=root/'team/TASK-BOARD.json'
board=json.loads(path.read_text(encoding='utf-8-sig'))
for task in board['tasks']:
 if task['id']=='T035':
  task['current_priority']='Latest shipping correction:70INR flat per order; await genuine stock/payment/policy facts and Admin/browser access'
  task['next_steps']=['Configure flat70INR per order and verify single/multiple-item carts after Admin access','Obtain genuine supplier stock/shipping/returns/payment activation evidence','Rendered review and test ordering before launch acceptance']
path.write_text(json.dumps(board,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
path=root/'team/reports/T035/WORK-REPORT.md'
report=path.read_text(encoding='utf-8-sig')
report=report.replace('Update22October2026: owner resolved shipping basis after this report was written. Shipping is70INR per item quantity;2items140INR and3items210INR. LAUNCH-CONFIG.json and WORK-LOG.md updated. Earlier pending-basis statements below are historical. No Shopify rate has been applied; verify one-item, repeated-quantity and mixed-product carts after Admin access is available.', 'Latest correction22October2026: owner states total70INR shipping. Use flat70INR per order regardless of item quantity; this supersedes the previous per-item answer. LAUNCH-CONFIG.json, WORK-LOG.md and task board corrected. Earlier shipping-basis statements below are historical. No Shopify rate has been applied; verify single-item and multiple-item carts after Admin access is available.')
path.write_text(report,encoding='utf-8')
print('Saved flat70INR per order; applied_to_shopify=False.')
