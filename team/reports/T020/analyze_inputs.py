from pathlib import Path
import csv, json, hashlib, zipfile, collections, re
import openpyxl

root = Path('F:/Dropshipping')
out = root / 'team/reports/T020'
source = root / 'Files/Demo_CSV (1).xlsx'
archive = root / 'Files/Drop shipping Committee.zip'
wb = openpyxl.load_workbook(source, data_only=False)
sheets = []
for ws in wb:
    values = list(ws.values)
    headers = list(values[0])
    rows = [dict(zip(headers, row)) for row in values[1:]]
    sheets.append({'sheet':ws.title,'headers':headers,'rows':rows,'dimensions':ws.calculate_dimension(),
                   'formulas':[c.coordinate for row in ws for c in row if c.data_type == 'f'],
                   'non_general_number_formats':{c.coordinate:c.number_format for row in ws for c in row if c.value is not None and c.number_format != 'General'}})
headers = sheets[0]['headers']
rows = sheets[0]['rows']
def csvvalue(value):
    if value is None: return ''
    if isinstance(value, bool): return 'TRUE' if value else 'FALSE'
    if isinstance(value, float) and value.is_integer(): return str(int(value))
    return str(value)
with (out/'demo-source-lossless.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows([[csvvalue(row[h]) for h in headers] for row in rows])
with (out/'demo-source-lossless.csv').open(encoding='utf-8', newline='') as f:
    roundtrip = list(csv.reader(f))
expected = [headers] + [[csvvalue(r[h]) for h in headers] for r in rows]
assert roundtrip == expected
(out/'workbook-rows.json').write_text(json.dumps({'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sheets':sheets}, ensure_ascii=False,indent=2),encoding='utf-8')
products = [r for r in rows if r['Title']]
grouped = collections.defaultdict(list)
for r in rows: grouped[r['Handle']].append(r)
summary = []
for p in products:
    group = grouped[p['Handle']]
    summary.append({k:p[k] for k in ['Handle','Title','Vendor','Variant SKU','Variant Price','Variant Compare At Price','Cost per item','Variant Inventory Qty','Variant Grams','Variant Taxable','Status','Published']} | {'image_count':len(group),'image_positions':[r['Image Position'] for r in group]})
unusual = []
for i,r in enumerate(rows,2):
    for h,v in r.items():
        if isinstance(v,str) and v.strip() in ['`','"""','TODO','TBD','N/A']:
            unusual.append({'excel_row':i,'header':h,'value':v})
validation = {
    'source_file':str(source),'source_size':source.stat().st_size,'sheet_count':len(sheets),
    'data_rows':len(rows),'header_count':len(headers),'unique_product_handles':len(grouped),
    'product_rows':len(products),'variant_rows':sum(bool(r['Variant SKU']) for r in rows),
    'image_rows':sum(bool(r['Image Src']) for r in rows),
    'unique_image_urls':len(set(r['Image Src'] for r in rows if r['Image Src'])),
    'inventory_total':sum(p['Variant Inventory Qty'] for p in products),
    'duplicate_skus':[k for k,n in collections.Counter(p['Variant SKU'] for p in products).items() if n>1],
    'duplicate_full_rows':len(rows)-len(set(tuple(r[h] for h in headers) for r in rows)),
    'empty_handle_rows':[i for i,r in enumerate(rows,2) if not r['Handle']],
    'non_https_image_rows':[i for i,r in enumerate(rows,2) if r['Image Src'] and not r['Image Src'].startswith('https://')],
    'unexpected_literal_cells':unusual,'formulas':sheets[0]['formulas'],
    'csv_roundtrip_equal':roundtrip == expected,
    'csv_sha256':hashlib.sha256((out/'demo-source-lossless.csv').read_bytes()).hexdigest(),
    'products':summary,
    'limitations':['No supplier stock or current prices confirmed','Currency absent from source; applies target-store currency on import','Image URLs syntactically valid; network availability and media rights not tested','Legacy headers require current Shopify import-preview acceptance','All source products active and published; do not import raw values as commercially ready','No existing target handles checked by this worker'],
}
(out/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(archive) as z:
    texts={n:z.read(n).decode('utf-8-sig') for n in z.namelist() if n.lower().endswith(('.txt','.md'))}
    zip_summary={'source':str(archive),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                 'members':[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size} for i in z.infolist()],
                 'all_chat_text_read':list(texts),'attachments_included':False,
                 'chat_txt_lines':len(texts['chat.txt'].splitlines()),'chat_md_lines':len(texts['chat.md'].splitlines())}
    (out/'chat-archive-validation.json').write_text(json.dumps(zip_summary,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=True,indent=2))
