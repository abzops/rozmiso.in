from pathlib import Path
import json,hashlib,shutil,datetime
root=Path('F:/Dropshipping');report=root/'team/reports/T022';source=root/'rozmiso-studio-theme';candidate=report/'theme-candidate';backup=report/'source-backup'
manifest=json.loads((report/'CHANGED-FILES.json').read_text());expected={'assets/studio.js','layout/theme.liquid','sections/studio-collection.liquid','sections/studio-header.liquid','sections/studio-product.liquid','snippets/studio-card.liquid','templates/cart.liquid','templates/page.contact.liquid'}
assert {row['path'] for row in manifest}==expected and len(manifest)==8
assert not backup.exists(),'Integration backup already exists; refusing overwrite'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={p.relative_to(source).as_posix():digest(p) for p in source.rglob('*') if p.is_file()}
for row in manifest:
 rel=row['path'];assert before[rel]==row['source_sha256'],'Authoritative source drift: '+rel
 assert digest(candidate/rel)==row['candidate_sha256'],'Candidate drift: '+rel
# Complete every before-copy backup before touching source.
for row in manifest:
 rel=row['path'];b=backup/rel;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/rel,b)
 assert digest(b)==row['source_sha256']
for row in manifest:
 rel=row['path'];shutil.copy2(candidate/rel,source/rel)
after={p.relative_to(source).as_posix():digest(p) for p in source.rglob('*') if p.is_file()}
assert before.keys()==after.keys(),'Authoritative file set changed'
actual={rel for rel in before if before[rel]!=after[rel]};assert actual==expected
for row in manifest:assert after[row['path']]==row['candidate_sha256']
evidence={'integrated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authoritative_file_count':len(after),'changed_paths':sorted(actual),'unchanged_paths_count':len(after)-len(actual),'backup':'team/reports/T022/source-backup','all_backup_hashes_match_previous_source':True,'all_integrated_hashes_match_reviewed_candidate':True,'all_other_authoritative_files_unchanged':True,'css_fonts_images_settings_locales_unchanged':True,'files':manifest,'live_actions':False,'live_draft_id_reported_by_codex':'159016681664','live_draft_verified_by_worker':False}
(report/'SOURCE-INTEGRATION.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence,indent=2))
