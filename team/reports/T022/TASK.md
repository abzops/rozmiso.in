# T022 - Isolated discovery and preview-controls theme fixes

Owner: Codex worker A, Store theme developer. Reviewer: Codex, independent of implementation.
Date: 8 October 2026. Assignment: prepare bounded local fixes requested by Codex while Shopify settings review proceeds.

Inputs: authoritative `rozmiso-studio-theme`, T019 audit, active charter/board and theme-developer contract.
Allowed writes: `team/reports/T022/**` only. Production source and live Shopify are read-only for this worker. No deployment, settings mutations, messages, spending, invented seller/policy terms or further delegation.

Scope: copy authoritative theme to `theme-candidate`; preserve design, copy, existing prelaunch setting and native fallback routes. Make prelaunch mode explicitly disable product addition and cart checkout links/forms in theme markup and JavaScript. This is theme-level UX enforcement, not a Shopify backend checkout lock. Repair predictive search so valid native results outside the first 50 local records are retained. Evaluate scalable refinements and exact-product enquiry prefill; implement only bounded supported fixes, without misrepresenting page-local filters as catalog-wide. Record remaining needs.

Acceptance: meaningful regression tests for prelaunch true/false and available/unavailable variants, native predictive results beyond local index, cart interactions and no unintended source changes; Liquid validation; exact changed-file/hash manifest; report limitations and reviewer handoff.

Deliverables: isolated candidate, meaningful tests/results, change manifest and WORK-REPORT.md. Only Codex accepts and updates board.

## Integration assignment - 8 October 2026

Codex authorizes integration of exactly the eight paths in `CHANGED-FILES.json` into authoritative `rozmiso-studio-theme`, after hash verification and before-copy backup in `team/reports/T022/source-backup`. No other production writes. Verify all other authoritative files remain unchanged and record local integration evidence. Codex reports that draft theme 159016681664 received these files; the integration worker does not verify or mutate live state. Codex performs actual storefront visual QA. Board stays Codex-owned.

## Mobile overflow follow-up - 8 October 2026

Codex's live QA observed client width375 and PDP grid children width726/scrollWidth746, with nine fixed-width thumbnails. Additional authorization: candidate-only minimal CSS correction in `theme-candidate/assets/studio.css`, evidence and regression rerun. Do not integrate CSS or other changes before Codex review. The prior eight-file source integration completed before this pause was delivered; no additional source writes follow. Actual390px visual/DOM verification remains with Codex.
