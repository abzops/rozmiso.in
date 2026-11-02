# Independent work report - T034

Status: SUBMITTED; source review PASS after one scoped correction; rendered design QA BLOCKED
Reviewer: bento_rebuild_review, independent review lane
Date: 22 October 2026, Windows PowerShell

## Result

Read the selected Modern Bento concept 05, the rebuilt complete product-bento.css, inherited studio.css, product section and product-card markup. The clean stylesheet removes prior appended override history and independent centered-image sizing. Main images occupy their entire gallery track at natural proportions, so square product assets have neither containment sidebars nor product cropping. Native form, variant, quantity, image selection, availability guard, enquiry and all three related items remain present.

One inherited conflict was found and corrected under Root's explicit exception to report-only scope. Base studio.css sets summary span to 22px, which overrode the policy summary's intended 14px text through explicit child sizing. Added exactly this rule to assets/product-bento.css:

    .bento-policies summary > span:not(.bento-chevron) { font-size: inherit; }

The policy label now inherits 14px while the chevron keeps its 22px size. No other source changes by this lane.

## Evidence and validation

Reference: F:/Dropshipping/team/reports/T032/concepts/05-modern-bento.png, 1024x1536, visually inspected. Its approximate gallery is x38-604 (566px), summary x632-988 (356px), separated by 28px. The concept's rectangular main-photo crop is intentionally adapted to the true square product assets so the actual product remains intact.

Source: F:/Dropshipping/rozmiso-studio-theme/assets/product-bento.css. The following dimensions are CSS-derived, not browser measurements. They assume the stated CSS viewport and exclude any scrollbar difference.

| Viewport width | Inner width | Main photo / gallery | Summary | Horizontal gap | Outer gutter | Title / body |
|---|---:|---:|---:|---:|---:|---|
|390|342|342|342 stacked|not applicable|24|28 / 14|
|820|756|413.74|318.26|24|32|30 / 14|
|1024|960|529.04|406.96|24|32|30 / 14|
|1440|1280|620|632|28|80|34 / 14|
|1920|1280|620|632|28|320|34 / 14|

The 1280px cap prevents the rejected giant-media scaling but makes the summary slightly wider than the gallery at large desktop sizes. This differs from the reference's gallery-dominant composition and the approximate 58/42 preference. The implementation report explicitly documents that tradeoff against the 560-620px image target. At 1920 the outside gutters reach 320px, relevant to the owner's earlier margin complaint. These are pending rendered review decisions, not visual acceptance. There is no artificial whitespace between gallery track and image in source.

Inheritance checks: scoped width and zero shell padding override base shell and responsive padding; natural image height overrides base fixed-height gallery/card rules; grid thumbnails override base 70px dimensions; summary position resets sticky; scoped title, price, form and action rules override base product-page styles; related-grid breakpoint retains all three cards. Hidden-state enforcement and commerce logic are unchanged. Related cards use natural image heights; mixed product image ratios therefore need screenshot review for uneven card heights. The real unavailable notice and enquiry add legitimate height relative to the conceptual shopping-state image.

Executed independently:

- node team/reports/T033/implementation/render.test.cjs: 4/4 PASS.
- node team/reports/T030/theme-review/regression.test.cjs: 11/11 PASS.

These prove fixture behavior, not rendered visual fidelity or successful checkout. Root must execute final Shopify syntax/validation checks and verify draft/live theme identity before syncing.

## Artifacts and scope

This report: F:/Dropshipping/team/reports/T034/review/WORK-REPORT.md.
Authorized narrow source exception: one policy label inheritance rule in F:/Dropshipping/rozmiso-studio-theme/assets/product-bento.css.
No browser control, live theme, log, board, account, inventory or commerce edits.

## Missing inputs and dependencies

Root reports browser access still disabled in Work settings despite the owner's enabled reply. No desktop/mobile screenshots were available for this review. Therefore no claim of rendered scale, absence of overflow, exact theme match, final customer appearance or visual approval is made. Keep public theme unchanged until actual browser comparison against concept05 is complete.

## Proposed handoff

Sync validated source only to the existing unpublished draft. Compare actual 1440 desktop, 1024 tablet, 390 mobile and a wide desktop view. Inspect gallery/summary balance, outside gutters, policy label size, unavailable-state stacking, generic long descriptions, mixed related-image ratios, thumbnail selection and zoom. Root decides whether the cap or column balance needs adjustment from that evidence.

## Codex acceptance

Pending. Only Root accepts and updates the shared board.
