# T001 - Antigravity audit

Status: CHANGES_REQUIRED
Runtime: Antigravity CLI / current cached sign-in
Independent reviewer: Codex - pending

# Storefront Audit Report: Rozmiso Brand & Theme Source
**Task ID:** T001  
**Department:** Store + Creative (Lane A)  
**Auditor:** Bounded Storefront Worker  
**Reviewer:** Codex / Shield Evidence Auditor  
**Methodology:** Bounded static inspection of supplied source snapshots only. No external tools, live browser runtime, checkout executions, or unsupplied files were accessed.

---

## 1. Acceptance Criteria Verification & Storefront Assessment

### AC1: Architecture, Storefront Surfaces & Brand Consistency
* **Homepage (`studio-hero.liquid`, `studio.css`):**
  * *Structure:* Implements hero grid with kicker, H1, dual CTAs, spotlight card, value props bar, and category grid (`home-care`, `kitchen-essentials`, `travel-essentials`).
  * *Brand Alignment:* Accurately applies palette (`--ink: #26342e`, `--paper: #fbfaf6`, `--brand-clay: #b75132`, `--sage: #e8ece1`) and typography (`Manrope` headings, `DM Sans` body) per [BRAND-GUIDE.md](F:/Dropshipping/outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/BRAND-GUIDE.md).
* **Navigation (`studio-header.liquid`, `studio.css`):**
  * *Desktop:* Sticky header (`z-index: 40`), inline SVG brand mark, instant search bar, bag link with item counter, and dedicated sub-navigation band.
  * *Limitation:* Hardcodes URLs (`collections['home-care'].url`, `pages/contact`, `#our-approach`) directly in Liquid rather than binding to `linklists[section.settings.menu]`.
* **Product Surfaces (`studio-card.liquid`, `studio.css`):**
  * *Card Component:* Renders product type eyebrow, title, formatted price with `price_varies` support, lazy-loaded responsive imagery (`widths: 250, 400, 700`), and out-of-stock badges (`item.available`).
  * *PDP (CSS source only):* Defines `.pdp`, `.main-photo`, `.thumbs`, and `.howto-grid`, but the underlying Liquid template (`sections/studio-product.liquid` or `templates/product.json`) was omitted from snapshots.
* **Mobile Usability (`studio.css`):**
  * Includes breakpoints at `1050px`, `1000px`, and `700px`. At `<=700px`, converts desktop navigation into `<details class="mobile-menu">`, scales down typography (`clamp(40px, 10.2vw, 54px)`), stacks category cards to a single column, and ensures touch targets meet >=44px min-height (e.g., `.bag-link`, `.mobile-menu summary`, `.card-shop-link`).
* **Accessibility (`studio.css`, `theme.liquid`, `studio-header.liquid`):**
  * *Strengths:* Implements `#MainContent` skip link, `aria-current="page"`, `aria-label` attributes on icon triggers, and `prefers-reduced-motion` overrides disabling transitions and transforms.
  * *Weaknesses:* `<details class="mobile-menu">` lacks standard ARIA disclosure synchronizations; visual search status relies entirely on deferred JS.

---

### AC2: Favicon Declarations, Asset Paths & Fallback Coverage
*Source inspection vs. browser observation:* Source analysis can verify tags and paths, but cannot observe browser tab rendering, caching, or visual fidelity.

* **Source Findings in [theme.liquid](F:/Dropshipping/rozmiso-studio-theme/layout/theme.liquid):**
  * When `settings.favicon != blank`: Emits PNG 32x32 and Apple touch icon 180x180 via `image_url`. It omits standard 16x16 PNG and SVG vectors.
  * When `settings.favicon == blank` (Fallback): Declares an embedded data URI for 32x32, `{{ 'rozmiso-mark.svg' | asset_url }}` for SVG, and an embedded data URI for 180x180 Apple touch icon.
* **Coverage Deficiencies:**
  * [BRAND-GUIDE.md](F:/Dropshipping/outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/BRAND-GUIDE.md) documents `rozmiso-brand-16.png`, `rozmiso-brand-32.png`, `rozmiso-brand-180.png`, and `rozmiso-brand-512.png`, but `theme.liquid` bypasses the static PNG asset files in favor of raw embedded data URIs.
  * No `manifest.json` declaration exists for PWA or Android icon support.

---

## 2. Five Prioritized Storefront Improvement Recommendations

| Priority | Title | Impact | Evidence (Source References) | Effort |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | **Dynamic Navigation & Catalog Handle Decoupling** | High (Robustness & Operations) | Hardcoded handles in [studio-header.liquid](F:/Dropshipping/rozmiso-studio-theme/sections/studio-header.liquid:28) (`collections['home-care']`) and [studio-hero.liquid](F:/Dropshipping/rozmiso-studio-theme/sections/studio-hero.liquid:1) (`all_products['usb-rechargeable-fabric-shaver']`). Any handle rename breaks the spotlight and navigation. | Medium |
| **P2** | **Remove Layout Payload Bloat (`data-search-catalog`)** | High (Performance & TTFB) | In [theme.liquid](F:/Dropshipping/rozmiso-studio-theme/layout/theme.liquid:13), `<template data-search-catalog>` iterates up to 50 products inline with descriptions on every single page render. | Low |
| **P3** | **Standardize Favicon & Touch Icon Link Architecture** | Medium (Standards & Cacheability) | In [theme.liquid](F:/Dropshipping/rozmiso-studio-theme/layout/theme.liquid:5), inline base64 data URIs inflate the `<head>` and bypass CDN caching instead of referencing `asset_url` (`rozmiso-brand-32.png`, etc.). | Low |
| **P4** | **Consolidate Cascading CSS Redundancies** | Medium (Maintainability) | [studio.css](F:/Dropshipping/rozmiso-studio-theme/assets/studio.css) contains 3 successive historical append blocks (base, 6 Oct nav, 6 Oct brand refinement), repeatedly re-declaring `:root`, `.header-row`, `.hero h1`, and media queries. | Medium |
| **P5** | **Accessible Drawer Dialog Trapping & Escape Controls** | Medium (WCAG Compliance) | [studio-header.liquid](F:/Dropshipping/rozmiso-studio-theme/sections/studio-header.liquid:36) uses native `<dialog class="cart-drawer">`, but lacks fallback focus trapping and explicit `aria-modal="true"`. | Low |

---

## 3. Evidence Gaps & Non-Verifiable Surface Areas

Because this audit is strictly bounded to the supplied text snapshot strings, the following cannot be verified:

1. **Missing Input Artifact:** `outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/BRAND-REFRESH-VALIDATION.md` was specified in the contract inputs but was omitted from the prompt snapshot payload.
2. **Missing Javascript Runtime (`studio.js`):** Script behaviors (e.g., instant search debouncing, cart drawer open/close events, zoom dialog listeners) cannot be audited without the script content.
3. **Missing Section Templates:** Product detail page Liquid (`sections/studio-product.liquid`), cart page Liquid, and collection page templates were omitted.
4. **Live Shopify Environment:** The presence of referenced collections (`home-care`, `kitchen-essentials`, `travel-essentials`), the existence of handle `'usb-rechargeable-fabric-shaver'`, real inventory status, payment gateways, and checkout functionality cannot be verified.
5. **Browser Tab/Favicon Rendering:** Static strings cannot confirm OS/browser compatibility, favicon scaling, or sharp rendering in browser address bars.


## Codex acceptance

Pending. A SUCCESS CLI envelope alone does not establish that acceptance criteria passed.

## Codex independent review - 6 October 2026

CHANGES_REQUIRED for the full T001 contract. A substantive terminal worker report was received, but not all requested source inputs were supplied. Missing JavaScript, product/cart/collection templates and prior validation prevent full acceptance.

Do not adopt the unsupported accessibility claims as defects: native details/summary has disclosure semantics without manually duplicating aria-expanded; a native dialog opened with showModal has implicit modal behavior and browser-managed focus handling. Without studio.js and runtime observation, a claim that trapping or Escape behavior is absent is unproven. Lack of a PWA manifest or 16px link is not itself a broken Shopify favicon. Embedded PNGs may increase head size, but their existence is not a standards failure. With four products, the suggested search-payload performance priority needs measurements rather than an assumed TTFB impact.

Useful supported observations: scattered CSS override blocks, fixed product/collection handles and current identity tokens. Codex's separate current mobile observation and T009 audit establish the concrete brand priorities: 7px descriptor, product grid around y2076, repetitive hero copy and missing reusable logo variants. Those informed the prepared local review kit. No live runtime, sales-readiness or full audit acceptance is claimed.
