# Work report — T028 reference review

Status: SUBMITTED (reference audit complete; assigned generation continues)
Author/lane: workspace_audit, A
Reviewer: Codex
Date/environment: 8 October 2026, Windows F:\Dropshipping

## Result and scope

All 28 original product records reviewed; 47 reference images downloaded using ordinary public HTTP and individually inspected with view_image. 21 active products have usable physical references with per-product invariants/constraints. Seven drafts blocked: five unrelated generic photographs, two empty galleries. `manifest.json` and `download-evidence.json` retain original URL, media ID, local path, HTTP status, decoded dimensions and SHA-256. No image editing/generation or live writes were performed for this reference-audit result; generation is a subsequent expanded assignment.

## Evidence and validation

All 47 downloads returned HTTP 200 and decoded successfully; no more than two original images per product. Audit records all 28 unique IDs, including empty galleries. Source is parent's live snapshot `products-before.json`, not an independent live audit. All local image files are inside `reference-review/<numericid>/`; full physical observations are in manifest.json. The five draft photos show respectively motorcycle, yoga silhouette, full-size HP office printer, laundry basket, galaxy sky. They cannot establish the exact listed products.

Color alternatives/props and inconsistent views are explicitly limited: one cloth color, one bottle color, a single coherent laundry pattern, exactly two rack shelves, clear flat keyboard sheet, three bag ties and three wiping cloths, twenty whole cable-retainer strips rather than individual flowers. A cable-retainer strip has five flower-shaped retainers. Material appearance is not certified composition, physical size or performance. Generation must remove supplier claims/text/collages and preserve identified geometry.

## Missing inputs and handoff

Seven blocked drafts need authentic exact-product images before faithful generation; do not invent from title. Product media rights, exact supply terms and samples are outside visual audit. Root owns acceptance and Shopify replacement. Original media remain rollback evidence. B has been notified complete ten-product reference paths/invariants. Parent accepted 21 usable references and seven blockers in team message.

## Independent review / Codex acceptance

Parent review accepted reference classifications; task board and live work remain Codex-owned.
