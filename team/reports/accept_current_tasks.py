import json
from pathlib import Path
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[2]
path = root / 'team/TASK-BOARD.json'
board = json.loads(path.read_text(encoding='utf-8-sig'))
now = datetime.now(timezone.utc).isoformat()
for task in board['tasks']:
    if task['id'] in {'T019','T020','T021','T022','T023'}:
        task['status'] = 'ACCEPTED'
        task['accepted_at'] = now
        task['acceptance_scope'] = {
            'T019': 'Inventory and bounded text audit; metadata-only exclusions explicit.',
            'T020': 'Workbook and text-only chat ZIP analysis; source claims unverified.',
            'T021': 'Eight unpublished zero-stock tracked DENY products;55images saved,15dead sourceURLs.',
            'T022': 'Nine reviewed source fixes integrated/backed up and saved to unpublished Shopify draft159016681664; no live publication.',
            'T023': 'Sanitized settings input review and prioritized owner actions.'
        }[task['id']]
    if task['id'] == 'T024':
        task['status'] = 'BLOCKED'
        task['completed_scope'] = '20top-level category audit; selected subsettings; phoneRequired and factual SEO saved; drafttheme QA and checksum verification.'
        task['blockers'] = ['Owner billing/payment activation','Approved legal seller and public support/address','Supplier stock/media/weights/shipping/returns evidence','Assessed tax treatment','Owner decision on reviewed theme publication and later sales launch']
        task['evidence'] = ['team/reports/T024/RESULTS.md','team/reports/T024/FINAL-INDEPENDENT-REVIEW.md','team/reports/T023/OWNER-ACTIONS.md']
board['updated'] = '2026-10-08'
path.write_text(json.dumps(board,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Codex accepted T019-T023; T024 blocked on listed owner inputs. Previous tasks preserved.')
