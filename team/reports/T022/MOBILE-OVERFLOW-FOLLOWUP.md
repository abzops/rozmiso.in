# T022 mobile PDP overflow follow-up

Status: SUBMITTED, candidate-only correction awaiting Codex visual/DOM review. Date: 8 October 2026. Author: worker A; reviewer: Codex.

Codex observed a 390px viewport, document client width 375, scrollWidth 746 and PDP gallery/main-photo/thumbs/product-info width 726. The supplied `T024/theme-product-mobile.png` visibly clips product text and full-width controls at the right edge. This is actual browser evidence reported by Codex, not a successful visual result.

Static diagnosis matches those dimensions: the actual class is `.pdp`, a grid with default minimum sizing on its direct `.gallery`/`.product-info` children. The `.thumbs` flex row contains nine fixed 70px thumbnails with 12px gaps; its intrinsic size is about 726px (9 × 70 + 8 × 12). Mobile changes the grid to 1fr, but without min-width:0 on grid children, the thumbnail intrinsic size expands that track and product text with it. The row already has overflow:auto; scroll containment alone does not remove the parent grid item's intrinsic minimum.

The candidate adds only:

```css
.pdp > *{min-width:0}
.pdp .thumbs{min-width:0;max-width:100%}
```

This lets grid children shrink inside the assigned track while retaining native thumbnail horizontal scrolling. No body overflow hiding, paragraph truncation, image deletion, font/palette/grid-ratio change or fixed width was introduced. The rule also supports the desktop grid's existing proportions.

Artifacts: `MOBILE-CSS.patch`, `MOBILE-CSS-RESULTS.json` and updated candidate `assets/studio.css`. The prior eight reviewed candidate/source files remain unchanged. Authoritative CSS was not edited. Its SHA256 is 41ba922bc87e1f431567fa834bfaefe28f93ba48ce25b17bf572c1e04796f0d4; candidate SHA256 is 8f70eb5ee689ccecaa1e985773f1146b750bdb7784221f92b77d9e04fceb5ad9.

The existing meaningful thirteen-test behavioral/render suite was rerun against this candidate; output is `MOBILE-FOLLOWUP-TESTS.txt`. All thirteen passed. These tests verify product/search/cart/filter/enquiry behavior. jsdom does not perform actual CSS layout, so they do not prove the overflow is corrected. Codex should upsert candidate CSS to the reviewed draft, verify 375/390 client bounds, thumbnail scrolling, full paragraph/button containment and desktop layout. No additional source integration occurs before that review. The eight-file integration had completed before Codex's pause message arrived; that state is preserved in `SOURCE-INTEGRATION.json`.
