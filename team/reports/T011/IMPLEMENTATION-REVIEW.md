# Work report — T011 implementation review

Status: SUBMITTED  
Review result: **PASS — source review only; visual/interactive acceptance pending**  
Author: Codex independent source reviewer, distinct from implementation author  
Date/environment: 6 October 2026, Windows, F:\Dropshipping

## Result and scope

Reviewed `operations/brand-direction-2026-10-06/theme-approved` against `REGRESSION-CONSTRAINTS.md`, the approved review-kit README and MOBILE-CONCEPT.png. The current AGENTS.md, TEAM_ROSTER_AND_RULES.md and T011 task-board entry were read. RTK is unavailable; ordinary PowerShell was used.

The isolated implementation preserves the important search/cart/product/enquiry contracts and follows the approved product-led direction: compact outlined logo, no tiny mobile descriptor, category navigation, short fabric-care headline, real featured image, current price/availability, one collection action, earlier four-product grid, simpler story and reusable SVG icon/logo snippets. No source change enabling ordering was found.

Only this report was written. I did not edit source/board, operate a browser, upload a theme or mutate commerce state. This PASS permits continued draft-preview verification; it is not a visual pass, deployment confirmation or commercial launch approval.

## Concrete issue found and resolved

The first inspected CSS applied `filter:brightness(0) invert(1)` to `.footer .brand-logo` even though `studio-footer.liquid` renders the supplied reversed asset. That asset has a cream tile and forest R; filtering all nontransparent pixels to white would erase the R within the tile.

I reported the issue to Codex. A subsequent read confirmed the implementing author removed the filter from `assets/studio.css:12`. The footer now uses the asset's own colors. This is **resolved in the reviewed source**; the actual footer appearance still needs preview verification. The reviewer did not perform the repair.

## Evidence checked

| Requirement | Observed source evidence | Result |
|---|---|---|
| Complete responsive search | `sections/studio-header.liquid:1` retains one search form, unique HeaderSearch/HeaderSuggestions IDs, labels, GET action, q/type fields, all data hooks and status span | PASS source |
| Current-product search safety | `layout/theme.liquid:13` retains the current catalog template and metadata; `assets/studio.js` is byte-identical to authoritative baseline | PASS source; prior 50-product limitation remains |
| Static cart-section contract | Layout still renders `studio-header`; header retains dialog/error/content/count/badge, line keys, native links/forms, totals/discounts and close hook | PASS source |
| Product/variant/gallery/enquiry | Hash comparisons show `studio.js`, product section, collection section, search/cart/contact templates are unchanged | PASS source; no claim these flows were browser-tested in this review |
| Menu behavior | One `.mobile-menu` details/summary remains; menu icon is inside the existing accessible summary; Escape/outside-click script is unchanged | PASS source |
| Category navigation | `studio-hero.liquid:2–5` uses actual collection anchors rather than incomplete JS filter hooks; category navigation is visible on mobile through CSS | PASS source |
| Real featured product | Hero still reads the actual fabric-shaver product object; title/price/image/URL/available values are not copied from the static concept. Image uses contain with eager/high-priority loading | PASS source |
| Earlier catalog and truthful status | `templates/index.json` shortens headings, removes edit description and keeps four actual product selections. `studio-card.liquid:5` preserves category/price/availability data and displays unavailable status below price | PASS source |
| Reusable logos | `snippets/studio-logo.liquid:5–6` selects primary/reversed SVG assets with explicit dimensions. CSS uses `.brand-logo`, distinct from prior square `.brand-mark` rules | PASS source |
| Reusable icons | `snippets/studio-icon.liquid:5` uses one 24px grid, 1.75px strokes, round ends and decorative accessibility attributes. All names used by changed header/card/hero markup are implemented | PASS source |
| Favicon/default/custom coverage | `layout/theme.liquid:6` retains custom-image branch and adds existing 16/32 PNG, SVG and 180px default assets. Files referenced by layout exist locally | PASS source; actual tab/touch behavior pending |
| Metadata and fonts | Existing canonical/title/description/page-image priority and Shopify content hooks remain. Share-card fallback and local variable font declarations were added, with font-display swap | PASS source; asset delivery/rendering pending |
| Configuration | Prelaunch mode is explicitly true in isolated settings_data. Settings schema is byte-identical to baseline; all four JSON files parse | PASS source |
| Responsive/focus foundation | CSS preserves focus-visible, skip link, hidden handling, reduced motion, menu/search layers, native controls and mobile media rules. Sticky/anchor offsets were updated | PASS source structure; actual sizing/focus/overlap pending |

The source comparison identified 13 changed/new text theme files, plus new/updated logo/favicon/share/font assets. The parent reports all 13 text files passed its source validator; this reviewer independently parsed JSON, checked asset references, compared unchanged behavior files and examined markup/CSS. I did not rerun the parent's validator or claim its output as my own test.

The prior review ran the four existing synthetic search/cart tests successfully against the authoritative JS. Since isolated JS is byte-identical, repeating those tests adds no new coverage at this stage. They do not validate the changed header/card markup or CSS.

## Required preview checks before final acceptance

1. **Search focus visibility:** `assets/studio.css:7` newly clips the form with `overflow:hidden`, while the global input focus outline extends outside its boundaries. Inspect keyboard focus on the field and submit button. If the focus indicator is clipped or unclear, add an explicit form focus-within indicator or adjust clipping; do not simply remove focus styling.
2. **Actual compact header:** inspect 320/360/390/430px and desktop. Confirm the horizontal logo, bag count and menu fit, search text is legible, expanded suggestions/menu are not clipped, and anchor destinations remain visible below the sticky header. Source dimensions alone cannot establish this.
3. **Product-led composition:** compare actual rendered first screen/catalog start with the approved concept. The category strip uses plain links rather than the concept's boxed controls; story/FAQ remain after the grid rather than the concept's single contact panel. These are visible differences to inspect, not proven functional failures. Actual product names are longer than the concept's shortened card labels.
4. **Cards and product pages:** check long titles, unavailable labels, prices and 44px view links at 320px; confirm image contain does not produce misleading crops. The same card snippet affects collections/search/related products, so inspect those views as well as the homepage.
5. **Interactions:** menu Escape/outside click; search current product, keyboard results and Enter fallback; empty cart server refresh, close and focus return; gallery/zoom; enquiry exact-product prefill and required-field validation without sending customer messages. Retain synthetic fixtures for populated/error cart behavior rather than changing production stock.
6. **Assets:** verify primary and reversed logos, font and share-image delivery from Shopify's draft CDN; browser storefront favicon at actual 16/32px; page/product social-image priority. The local asset existence check is not a CDN response check.
7. **Accessibility/resize:** 200% text enlargement, no horizontal overflow and no covered actions; visible focus; natural reading/keyboard order. Ensure the new logo link announces Rozmiso once.

## Missing inputs, handoff and acceptance

No source-blocking issue remains in the snapshot reviewed after the footer correction. Shopify draft upload and actual visual/interactive evidence are still pending in this worker's scope. Codex should collect those results before accepting the complete implementation or deploying. Inventory, supplier, payments, policies and commercial readiness were not audited here and are not implied by the design approval.

Reviewer verdict: PASS for source contracts and approved direction, with the preview checks above required for final acceptance.  
Codex acceptance: Pending; only Codex records acceptance and updates the board.
