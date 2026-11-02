from pathlib import Path
import json
root=Path('F:/Dropshipping')
path=root/'team/reports/T035/LAUNCH-CONFIG.json'
data=json.loads(path.read_text())
data['owner_shipping_instruction']={'amount_inr':70,'basis':'PER_ITEM_QUANTITY','status':'Owner confirmed22October2026: two items cost140INR shipping','calculation':'70 * total shippable item quantity','examples':[{'items':1,'shipping_inr':70},{'items':2,'shipping_inr':140},{'items':3,'shipping_inr':210}],'applied_to_shopify':False}
path.write_text(json.dumps(data,indent=2)+'\n')
path=root/'WORK-LOG.md';text=path.read_text(encoding='utf-8-sig')
text=text.replace('Owner confirms shipping70INR; per-order versus per-item clarification pending.','Owner confirms shipping70INR per item:2items140INR,3items210INR. Basis resolved; Shopify rate not yet configured.')
text+='\n\n### 22 October2026 — Shipping basis confirmed\n\nOwner explicitly confirms two products in one order cost140INR shipping:70INR per item quantity, not a70INR flat order rate. Recorded formula70 × total shippable item quantity and1/2/3item examples in T035/LAUNCH-CONFIG.json. No Shopify rate changed; Admin access remains pending. Configure and verify single-item, repeated-quantity and mixed-product carts before launch. Other stock/payment/policy/browser dependencies remain unresolved.\n'
path.write_text(text,encoding='utf-8')
path=root/'team/TASK-BOARD.json';data=json.loads(path.read_text(encoding='utf-8-sig'))
for task in data['tasks']:
 if task['id']=='T035':
  task['current_priority']='Shipping basis confirmed70INR per item; await genuine stock/payment/policy facts and Admin/browser access'
  task['next_steps']=['Configure70INR × shippable item quantity shipping and verify single/multiple/mixed-item carts after Admin access','Obtain genuine supplier stock/shipping/returns/payment activation evidence','Rendered review and test ordering before launch acceptance']
path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
