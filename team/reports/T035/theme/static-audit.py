from pathlib import Path
import re,json

root=Path('F:/Dropshipping/rozmiso-studio-theme')
locale=json.loads((root/'locales/en.default.json').read_text())
keys={f'{group}.{key}' for group,values in locale.items() for key in values}
missing_keys=[];missing_renders=[];missing_assets=[];references=0
for p in root.rglob('*.liquid'):
    text=p.read_text(encoding='utf-8')
    for match in re.finditer(r"['\"]([\w.]+)['\"]\s*\|\s*t\b",text):
        references+=1
        if match[1] not in keys:missing_keys.append({'file':str(p.relative_to(root)),'key':match[1]})
    for name in re.findall(r"{%[-\s]*render\s+['\"]([^'\"]+)['\"]",text):
        if not (root/'snippets'/f'{name}.liquid').exists():missing_renders.append({'file':str(p.relative_to(root)),'snippet':name})
    for name in re.findall(r"['\"]([^'\"]+)['\"]\s*\|\s*asset_url",text):
        if not (root/'assets'/name).exists():missing_assets.append({'file':str(p.relative_to(root)),'asset':name})
result={'scope':'Local source only; excludes dynamic locale/render/asset expressions and external routes. Not live or browser acceptance.','literalTranslationReferences':references,'missingLocaleKeys':missing_keys,'missingLiteralSnippets':missing_renders,'missingLiteralAssets':missing_assets}
Path(__file__).with_name('STATIC-AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
