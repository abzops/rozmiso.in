from pathlib import Path
import json,hashlib
r=Path('F:/Dropshipping');s=r/'rozmiso-studio-theme';d=r/'team/reports/T033/remote-verified'
def normalized(p):
    if p.suffix in ['.json','.liquid','.js','.css','.svg']:
        v=p.read_text(encoding='utf-8-sig')
        if p.suffix=='.json':
            if v.lstrip().startswith('/*'):v=v.split('*/',1)[1]
            return json.loads(v)
        return '\n'.join(v.splitlines())
    return p.read_bytes()
missing=[];mismatches=[];files=[]
for p in s.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(s);q=d/rel
    if not q.exists():missing.append(rel.as_posix())
    elif normalized(p)!=normalized(q):mismatches.append(rel.as_posix())
    files.append({'path':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
result={'themeId':159555977408,'state':'UNPUBLISHED','files':len(files),'missing':missing,'mismatches':mismatches}
(r/'team/reports/T033/REMOTE-INTEGRITY.json').write_text(json.dumps(result,indent=2)+'\n')
(r/'team/reports/T033/SOURCE-HASHES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps(result))
