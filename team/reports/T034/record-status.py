from pathlib import Path
import json

root = Path('F:/Dropshipping')
board_path = root / 'team/TASK-BOARD.json'
board = json.loads(board_path.read_text(encoding='utf-8-sig'))
board['updated'] = '2026-10-22'
task = {
    'id': 'T034',
    'goal': 'Clean reconstruction of selected 05 Modern Bento product-page styling',
    'owner_lane': 'Codex + bento_rebuild + bento_rebuild_review',
    'reviewer': 'Codex and independent reviewer',
    'status': 'WAITING',
    'inputs': ['team/reports/T034/TASK.md', 'team/reports/T032/concepts/05-modern-bento.png'],
    'deliverables': ['team/reports/T034/WORK-REPORT.md'],
    'current_priority': 'Clean stylesheet saved to existing unpublished draft; actual browser comparison remains required',
    'runtime': 'Official Theme Check clean; corrected product media and native commerce retained. Browser tool reports disabled after owner enabled reply and runtime reset.',
    'next_steps': ['Capture draft at desktop, tablet and phone sizes when browser tool is available', 'Compare with selected 05 including outer margins and column balance', 'Resolve visible findings, verify native flows, then publish']
}
board['tasks'] = [t for t in board['tasks'] if t['id'] != 'T034'] + [task]
for item in board['tasks']:
    if item['id'] == 'T033':
        item['current_priority'] = 'Product section and six corrected media retained; rejected stylesheet superseded by clean reconstruction T034'
board_path.write_text(json.dumps(board, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

log_path = root / 'WORK-LOG.md'
log = log_path.read_text(encoding='utf-8-sig')
start = log.index('**Current work:**')
end = log.index('\n\n**Social status:**', start)
log = log[:start] + '**Current work:** T034 clean reconstruction of selected 05 Modern Bento. Replaced accumulated CSS overrides with one coherent stylesheet; retained six corrected soap images, native product data and stock guards. Existing unpublished draft159555977408 updated through Shopify CLI and pulled back for integrity verification. Official Theme Check clean. Live159552962752 remains unchanged. Actual desktop/mobile/tablet comparison is WAITING: browser tool still reports Local browser use is disabled in Work settings after owner confirmation and tool reset. Do not claim visual acceptance or publish until rendered comparison passes. See team/reports/T034/WORK-REPORT.md and rozmiso-studio-theme/design-qa.md.' + log[end:]
log += '''\n\n### 22 October 2026 — Clean reconstruction saved; visual verification blocked\n\n- T034 replaced all accumulated product stylesheet overrides with one coherent stylesheet. Desktop title34px/body14px, controls46px; main image fills its gallery track using natural proportions. Six corrected product images and native commerce code retained. Independent source review found and corrected inherited oversized policy labels. Column balance and outer gutters still require actual visual comparison with selected05; source calculations are not acceptance.\n- Official Theme Check clean. Shopify CLI verified theme159552962752 remains live and159555977408 unpublished; clean CSS synced only to draft and pulled back for integrity verification. No inventory, payment or domain changes.\n- Owner again confirmed browser enabled, but browser tool still returns disabled in Work settings, including after runtime reset. No bypass attempted. Design QA remains blocked, no implementation screenshot available and no new public publication claimed. Resume actual desktop/tablet/phone capture, compare selected05, resolve visible findings and publish only after acceptance. Evidence team/reports/T034/, theme-root design-qa.md.\n'''
log_path.write_text(log, encoding='utf-8')
