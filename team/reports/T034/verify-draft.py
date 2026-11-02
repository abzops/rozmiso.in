from pathlib import Path
import json, hashlib

root = Path('F:/Dropshipping')
source = root / 'rozmiso-studio-theme'
remote = root / 'team/reports/T033/remote-verified'
directories = {'assets', 'config', 'layout', 'locales', 'sections', 'snippets', 'templates'}

def normalize(path):
    if path.suffix in {'.json', '.liquid', '.js', '.css', '.svg'}:
        value = path.read_text(encoding='utf-8-sig')
        if path.suffix == '.json':
            if value.lstrip().startswith('/*'):
                value = value.split('*/', 1)[1]
            return json.loads(value)
        return '\n'.join(value.splitlines())
    return path.read_bytes()

files, missing, mismatches = [], [], []
for path in source.rglob('*'):
    if not path.is_file():
        continue
    relative = path.relative_to(source)
    if relative.parts[0] not in directories:
        continue
    pulled = remote / relative
    if not pulled.exists():
        missing.append(relative.as_posix())
    elif normalize(path) != normalize(pulled):
        mismatches.append(relative.as_posix())
    files.append({'path': relative.as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
result = {'themeId':159555977408, 'state':'UNPUBLISHED', 'files':len(files), 'missing':missing, 'mismatches':mismatches, 'scope':'Existing T033 full pull plus T034 CSS pulled again after strict push; local design-qa.md excluded as non-theme report'}
for name, data in [('REMOTE-INTEGRITY.json', result), ('SOURCE-HASHES.json', files)]:
    (root / 'team/reports/T034' / name).write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps(result))
assert not missing and not mismatches
