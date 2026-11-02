from pathlib import Path
import json

source=Path('F:/Dropshipping/rozmiso-studio-theme')
remote=Path('F:/Dropshipping/team/reports/T030/draft-verification')
def normalized(path):
    if path.suffix in ('.json','.liquid','.js','.css','.svg','.txt'):
        text=path.read_text(encoding='utf-8-sig')
        if path.suffix=='.json':
            if text.lstrip().startswith('/*'):
                text=text.split('*/',1)[1]
            return json.loads(text)
        return '\n'.join(text.splitlines())
    return path.read_bytes()

missing=[];mismatch=[];files=0
for path in source.rglob('*'):
    if not path.is_file():continue
    files+=1;other=remote/path.relative_to(source)
    if not other.exists():missing.append(str(path.relative_to(source)))
    elif normalized(path)!=normalized(other):mismatch.append(str(path.relative_to(source)))
report={'remoteTheme':159259001024,'localFiles':files,'missing':missing,'mismatches':mismatch}
Path('F:/Dropshipping/team/reports/T030/DRAFT-INTEGRITY.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
raise SystemExit(1 if missing or mismatch else 0)
