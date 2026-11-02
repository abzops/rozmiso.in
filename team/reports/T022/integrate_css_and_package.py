from pathlib import Path
import json,hashlib,shutil,zipfile,datetime
root=Path('F:/Dropshipping');out=root/'team/reports/T022';source=root/'rozmiso-studio-theme';candidate=out/'theme-candidate';backup=out/'source-backup';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mobile=json.loads((out/'MOBILE-CSS-RESULTS.json').read_text());original_manifest=json.loads((out/'CHANGED-FILES.json').read_text())
assert len(original_manifest)==8
css=source/'assets/studio.css';newcss=candidate/'assets/studio.css';oldcss=backup/'assets/studio.css'
assert sha(css)==mobile['source_sha256'],'Source CSS drift'
assert sha(newcss)==mobile['candidate_sha256'],'Candidate CSS drift'
assert not oldcss.exists(),'CSS backup already exists'
for row in original_manifest:
 assert sha(source/row['path'])==row['candidate_sha256'],'Integrated source drift '+row['path']
 assert sha(candidate/row['path'])==row['candidate_sha256'],'Candidate drift '+row['path']
before={p.relative_to(source).as_posix():sha(p) for p in source.rglob('*') if p.is_file()}
shutil.copy2(css,oldcss);assert sha(oldcss)==mobile['source_sha256']
shutil.copy2(newcss,css);assert sha(css)==mobile['candidate_sha256']
after={p.relative_to(source).as_posix():sha(p) for p in source.rglob('*') if p.is_file()}
assert set(after)==set(before)
assert {k for k in before if before[k]!=after[k]}=={'assets/studio.css'}
for rel in after:assert sha(candidate/rel)==after[rel],'Candidate/source mismatch '+rel
final=original_manifest+[{'path':'assets/studio.css','source_sha256':mobile['source_sha256'],'candidate_sha256':mobile['candidate_sha256']}]
assert len({row['path'] for row in final})==9
for row in final:assert sha(backup/row['path'])==row['source_sha256']
(out/'CHANGED-FILES-FINAL.json').write_text(json.dumps(sorted(final,key=lambda x:x['path']),indent=2),encoding='utf-8')
bundle=out/'rozmiso-reviewed-theme.zip'
with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(after):z.write(source/rel,rel)
with zipfile.ZipFile(bundle) as z:
 assert len(z.namelist())==39 and set(z.namelist())==set(after)
 assert z.testzip() is None
 for rel in z.namelist():assert hashlib.sha256(z.read(rel)).hexdigest()==after[rel]
data={'integrated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'total_source_files':39,'total_changed_files_from_original':9,'this_integration_changed_only':'assets/studio.css','all_source_files_match_final_candidate':True,'all_nine_original_backups_verified':True,'zip':str(bundle),'zip_sha256':sha(bundle),'zip_files':39,'zip_crc_and_per_file_sha256_pass':True,'changed_file_manifest':'CHANGED-FILES-FINAL.json','live_qa_reported_by_codex':{'draft_theme_id':'159016681664','viewport':'390x844','document_client_width':375,'document_scroll_width':375,'gallery_and_thumbs_width':335.2,'thumbnail_internal_scroll_width':726,'screenshot':'team/reports/T024/theme-product-mobile-fixed.png'},'worker_live_actions':False,'scope_limit':'Current 15 published products observed by Codex. Search beyond 50 and large-catalog filtering tested only in fixtures; no corresponding live claim.'}
(out/'FINAL-INTEGRATION.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data,indent=2))
