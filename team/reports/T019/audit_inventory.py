import os,csv,json,collections,hashlib,re,datetime
from pathlib import Path
root=Path('F:/Dropshipping'); out=root/'team/reports/T019'
text_ext={'.md','.txt','.json','.js','.cjs','.mjs','.py','.ps1','.html','.css','.liquid','.yml','.yaml','.toml','.csv','.ts','.tsx','.jsx','.sql'}
rows=[]; texts={}; errors=[]
def classify(rel):
 p=rel.lower(); parts=p.split('/')
 if any(s.startswith('.env') or s in {'credentials.json','secrets.json','.auth-token','login data','cookies','local state','preferences'} for s in parts) or Path(p).suffix in {'.sqlite3','.sqlite','.db'}: return 'sensitive-excluded'
 if any(s in {'.chrome-data','.chrome-session'} for s in parts) or any('browser' in s and ('profile' in s or 'state' in s) for s in parts): return 'browser-state-excluded'
 if any(s in {'node_modules','.git','__pycache__','.venv','venv','site-packages','fonttools','tools','.next'} or s.endswith('.dist-info') for s in parts): return 'dependency-metadata-only'
 if p.startswith('team/reports/t019/'): return 'audit-output'
 if any(s in {'theme-before','theme-prepared','theme-approved','theme-before-approved','legacy-redacted'} for s in parts): return 'historical-copy'
 if p.startswith('rozmiso-shopify-store/'): return 'historical-theme'
 if Path(p).suffix in text_ext: return 'first-party-text'
 return 'binary-or-generated-asset'
for d,dirs,files in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
 for name in files:
  p=Path(d)/name; rel=p.relative_to(root).as_posix(); category=classify(rel)
  try: st=p.stat(); size=st.st_size
  except OSError as e: errors.append(rel+': '+str(e)); continue
  row={'path':rel,'size_bytes':size,'extension':p.suffix.lower() or '(none)','category':category,'content_check':'metadata-only','lines':0}
  if category in {'first-party-text','historical-theme','historical-copy'} and p.suffix.lower() in text_ext and size<2000000:
   try:
    t=p.read_text(encoding='utf-8-sig'); texts[rel]=t
    row['content_check']='full-text-scanned';row['lines']=len(t.splitlines());row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
   except (UnicodeError,OSError): row['content_check']='not-utf8-or-unreadable'
  elif category in {'first-party-text','historical-theme','historical-copy'}: row['content_check']='large-text-metadata-only'
  rows.append(row)
with (out/'INVENTORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['path','size_bytes','extension','category','content_check','lines','sha256'],extrasaction='ignore');w.writeheader();w.writerows(rows)
summary={'snapshot_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(root),'files':len(rows),'bytes':sum(r['size_bytes'] for r in rows),'category_counts':dict(collections.Counter(r['category'] for r in rows)),'content_counts':dict(collections.Counter(r['content_check'] for r in rows)),'top_level':dict(collections.Counter(r['path'].split('/')[0] for r in rows)),'errors':errors}
(out/'COVERAGE.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
# Emit safe structural metadata for human audit; never write arbitrary matching content.
structures=[]
for rel,t in texts.items():
 if classify(rel)=='first-party-text':
  structures.append({'path':rel,'lines':len(t.splitlines()),'heading_count':sum(l.startswith('#') for l in t.splitlines()),'json_valid':None if not rel.endswith('.json') else False})
  if rel.endswith('.json'):
   try: json.loads(t);structures[-1]['json_valid']=True
   except Exception: pass
(out/'TEXT-STRUCTURE.json').write_text(json.dumps(structures,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
import ast
checks={'python_syntax_errors':[],'json_errors':[x['path'] for x in structures if x['json_valid'] is False], 'theme_missing_assets':[], 'theme_missing_snippets':[], 'theme_missing_sections':[], 'theme_missing_literal_translations':[], 'liquid_schema_errors':[],'json_template_missing_sections':[]}
for rel,t in texts.items():
 if rel.endswith('.py') and classify(rel)=='first-party-text':
  try: ast.parse(t,filename=rel)
  except SyntaxError as e: checks['python_syntax_errors'].append({'path':rel,'line':e.lineno,'reason':e.msg})
theme=root/'rozmiso-studio-theme';locale=json.loads((theme/'locales/en.default.json').read_text())
for rel,t in texts.items():
 if not rel.startswith('rozmiso-studio-theme/'): continue
 for schema in re.findall(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}',t,re.S):
  try:json.loads(schema)
  except Exception as e:checks['liquid_schema_errors'].append({'path':rel,'reason':str(e)})
 if rel.startswith('rozmiso-studio-theme/templates/') and rel.endswith('.json'):
  for section in json.loads(t).get('sections',{}).values():
   if not (theme/'sections'/(section.get('type','')+'.liquid')).exists():checks['json_template_missing_sections'].append({'path':rel,'target':section.get('type')})
 for kind,pattern,directory,suffix in [('assets',r"['\"]([^'\"]+)['\"]\s*\|\s*asset_url",'assets',''),('snippets',r"render\s+['\"]([^'\"]+)['\"]",'snippets','.liquid'),('sections',r"section\s+['\"]([^'\"]+)['\"]",'sections','.liquid')]:
  for name in re.findall(pattern,t):
   if not (theme/directory/(name+suffix)).exists():checks['theme_missing_'+kind].append({'path':rel,'target':name})
 for key in re.findall(r"['\"]([^'\"]+)['\"]\s*\|\s*t(?:\s|[}:|])",t):
  current=locale
  for part in key.split('.'):current=current.get(part,{}) if isinstance(current,dict) else {}
  if not current:checks['theme_missing_literal_translations'].append({'path':rel,'key':key})
(out/'STATIC-CHECKS.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
