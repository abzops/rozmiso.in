# Work report — T034

Status: SUBMITTED (source reconstruction complete; rendered visual acceptance pending)
Author and lane: bento_rebuild, bounded CSS engineer
Date: 22 October 2026, Windows/PowerShell

## Result

Replaced the entire product-bento.css with a single coherent stylesheet based on selected concept 05 Modern Bento. Removed all appended sizing/override history, independent image max-width centering, fixed-height related-image boxes, main-photo wide aspect ratios and !important declarations. Retained the existing Liquid section and JavaScript unchanged.

The gallery and thumbnail row now occupy exactly the same grid track. Main images use native proportions at full track width. All six corrected soap assets are square, giving a square fully filled frame without letterboxing or product-part cropping. Generic images retain their own natural ratio. Related images and how-to images also retain their natural proportions.

Hierarchy: 34px desktop serif title, 26px price, 14px body, 46px action controls, 20px card radii, dark forest accents, warm ivory panels. Mobile uses 28px title and 14px body; how-to steps stack into image-and-copy rows to avoid tiny paragraphs.

## Artifacts and scope

Changed source: F:/Dropshipping/rozmiso-studio-theme/assets/product-bento.css
Own report: F:/Dropshipping/team/reports/T034/implementation/WORK-REPORT.md
Reference: F:/Dropshipping/team/reports/T032/concepts/05-modern-bento.png
Prior rejected source: F:/Dropshipping/team/reports/T034/rejected-overrides.css
No section, JavaScript, config, commerce, live theme, account, log or board writes.

## Evidence and validation

Viewed the exact 1024x1536 selected concept. Approximate measured positions: main gallery x38–604 (566px), summary x632–988 (356px), 28px gap. Main concept photograph is approximately566x456. Its rectangular crop is intentionally adapted to a square frame for actual square product assets, per task brief. Retained the composition of left gallery/right summary, lower left how-to/right policy and contact modules, then related cards.

The reference's 58/42 column preference conflicts arithmetically with a 560–620px gallery across a 1180–1280px desktop inner width. The reconstruction prioritizes the explicit620px photo cap and balanced text scale. At desktop widths >=1200 the first track is620px and the summary fills remaining width. At tablet widths the proportion is1.3:1 (56.5/43.5), preserving the reference relationship without excessive photo size. Root/reviewer should verify this deliberate choice visually.

Calculated source geometry (not browser measurements):

| Viewport | Inner width | Gallery/photo | Summary | Gap | Title | Body | Outer gutter |
|---|---:|---:|---:|---:|---:|---:|---:|
|390|342|342|342 stacked|24 vertical|28|14|24|
|820|756|413.74|318.26|24|30|14|32|
|1024|960|529.04|406.96|24|30|14|32|
|1440|1280|620|632|28|34|14|80|
|1920|1280|620|632|28|34|14|320|

At1920 the content deliberately stops growing to avoid the rejected giant images and typography; natural outside whitespace is expected from the capped1280px content width. Unlike the previous implementation, none of this whitespace appears between the gallery and image.

Before, the final appended rules produced a648.8px gallery column at1440 but centered a480px image inside it, leaving84.4px artificial whitespace on each side. At1920 a712px column held the same480px image, leaving116px per side. The new620px desktop gallery contains a620px photo, with0px artificial side gutters. Before mobile image was independently capped340px within354px content at390, with27px title and11px how-to paragraphs; now image342px fills342px content, title28px, paragraphs14px.

Read all inherited studio.css and existing section/snippet markup. Scoped selectors override sticky summary positioning, native70px thumb dimensions, generic global heading scale, native form margins and card image transforms. Existing hidden state, variant handling, gallery selection, zoom, quantities, stock guard, disabled CTA, enquiry and policy links remain intact.

Validation executed: `node team/reports/T033/implementation/render.test.cjs` — 4/4 passed, covering corrected soap-gallery source, native variant/commerce guard, generic product content, and quantity min/step/max behavior. These are retained behavior checks, not visual acceptance.

## Missing inputs and dependencies

Root reports browser use disabled. This lane made no browser screenshots and does not claim rendered size verification or final visual acceptance. Root must compare actual1440 desktop,1024 tablet and390 mobile screenshots with the reference, including unavailable-state extra vertical content and generic long descriptions.

## Proposed handoff

Independent reviewer: examine column-balance tradeoff, natural image sizing, inheritance specificity and390/820/1024/1440/1920 breakpoints. Root: run Shopify validation, sync only approved theme files into the existing unpublished draft, visually verify, then decide publication.

## Independent review

Pending separate reviewer.

## Codex acceptance

Pending. Only Codex completes acceptance and updates the task board.
