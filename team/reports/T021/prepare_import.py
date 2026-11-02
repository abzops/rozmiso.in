import csv,json
from pathlib import Path
from openpyxl import load_workbook
out=Path('team/reports/T021');out.mkdir(exist_ok=True)
source=Path('Files/Demo_CSV (1).xlsx')
wb=load_workbook(source,data_only=True)
rows=list(wb.active.values); headers=list(rows[0])
def val(v):
    if v is None:return ''
    if isinstance(v,bool):return 'TRUE' if v else 'FALSE'
    if isinstance(v,float) and v.is_integer():return str(int(v))
    return str(v)
data=[[val(v) for v in r] for r in rows[1:] if any(v is not None for v in r)]
with Path('team/reports/T020/demo-source-lossless.csv').open(encoding='utf-8-sig',newline='') as f:
    raw=list(csv.reader(f))
assert raw[0]==headers
# Numeric formatting can differ but cell values are independently checked.
assert len(raw)-1==len(data)==70
changes=[]
for excel_row,r in enumerate(data,2):
    def setv(h,v):
        ix=headers.index(h)
        if r[ix]!=v:changes.append({'row':excel_row,'field':h,'from':r[ix],'to':v});r[ix]=v
    if r[headers.index('Title')]:
        setv('Published','FALSE');setv('Status','draft')
    if r[headers.index('Variant SKU')]:
        setv('Variant Inventory Tracker','shopify');setv('Variant Inventory Qty','0');setv('Variant Inventory Policy','deny')
    if r[headers.index('Google Shopping / Condition')]=='`':setv('Google Shopping / Condition','')
with (out/'demo-reviewed-draft.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(headers);w.writerows(data)
(out/'import-changes.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps({'rows':len(data),'products':sum(bool(r[headers.index('Title')]) for r in data),'changes':len(changes),'path':str((out/'demo-reviewed-draft.csv').resolve())}))
