# T022 final source and package evidence

Status: SUBMITTED for Codex acceptance. Author: worker A. Date: 8 October 2026.

Codex accepted the minimal mobile CSS after real draft-theme browser QA at 390 × 844. Reported document client width and scrollWidth both equal 375px; gallery/thumbs are 335.2px, while internal thumbnail scrollWidth remains 726px. This demonstrates page containment with thumbnail scrolling retained in that observation. Screenshot: `team/reports/T024/theme-product-mobile-fixed.png`. This worker did not perform the browser observation or any live mutation.

Only `assets/studio.css` was changed during the final source integration. Its original was backed up at `source-backup/assets/studio.css` and verified before replacement. All 39 authoritative files now match the final candidate byte for byte. The complete change set relative to the original source contains exactly nine files: the initial eight plus CSS. Original versions of all nine are present and hash-verified in `source-backup`.

`CHANGED-FILES-FINAL.json` is the authoritative final nine-file source/candidate hash manifest. `CHANGED-FILES.json`, `SOURCE-INTEGRATION.json` and `VERIFIED-RESULTS.json` retain their historical eight-file/pre-CSS evidence; use the final manifest for packaging/review. `FINAL-INTEGRATION.json` records exact final checks.

`rozmiso-reviewed-theme.zip` contains exactly the 39 Shopify theme files at their proper root paths, with no report/scripts/browser content. CRC inspection and per-entry SHA256 comparisons against final authoritative source passed. The ZIP hash is in `FINAL-INTEGRATION.json`.

The thirteen regression tests passed after the CSS candidate change; the seven changed Liquid files remain identical to those that passed full Shopify validation. Actual large-catalog filtering and search beyond 50 remain fixture-tested only: the current storefront scope is fifteen published products. Do not claim those larger-catalog cases were live-tested, or that native filters are configured merely because the theme supports them. Theme-level preview controls still do not enforce a backend lock on direct cart/checkout endpoints.

Codex owns actual remote draft/publication evidence, broader visual QA and task acceptance. No other source edits or board mutations occurred.
