# Work report — T011 regression constraints

Status: SUBMITTED  
Author: Codex independent source reviewer; Shield/Store specialist  
Date/environment: 6 October 2026, Windows, F:\Dropshipping  
Scope: Read-only review of current authoritative theme and approved direction. Only this report was written; no theme/board changes, browser operation, deployment or commerce mutation.

## Result

The approved compact, product-led direction can be implemented without replacing the commerce JavaScript. Preserve the existing DOM and native form contracts while refactoring visual markup. The highest risks are incomplete search markup, breaking the static header section used for cart refresh, duplicating IDs across desktop/mobile headers, and hiding controls or popovers through compact-header CSS.

I read the current AGENTS.md, TEAM_ROSTER_AND_RULES.md, task board, Store/Shield role cards, work-report template, current JS and the relevant header/layout/product/collection/search/cart/contact source. I also read CEO-PLAN.md and the approved review kit README. Codex supplied the approval and bounded T011 review assignment; the board snapshot still contained its earlier waiting status, which this worker did not change. RTK remains unavailable; ordinary PowerShell was used.

## Preserve these source contracts

| Area | Evidence in current source | Implementation constraint |
|---|---|---|
| Search initialization | `assets/studio.js:7–12,42–44` initializes each `[data-instant-search]` once and directly uses its input, results and status children | Every search box must contain `[data-search-input]`, `[data-search-results]` and `[data-search-status]`, plus the existing loading/no-results/unavailable/currency attributes. An incomplete box can throw before cart/filter initialization. Prefer one responsive search form over duplicated desktop/mobile forms. |
| Search identity and fallback | `sections/studio-header.liquid:1`; `layout/theme.liquid`; JS `:4–6,18–38` | Keep unique `HeaderSearch`/`HeaderSuggestions` IDs and correct label/aria-controls references. Preserve native GET action `routes.search_url`, `name=q`, hidden `type=product`, submit control and status announcement. Enter must continue to work when suggestions fail or JS is unavailable. |
| Search catalog safety | JS `:23–26` matches indexed suggestions against `[data-search-catalog]`; layout renders current `collections.all.products limit:50` | Retain the current-product allowlist and its id/title/price/availability/URL/image/keywords fields. Do not swap it for a decorative product preview or expose stale indexed drafts. Preserve actual current price/status rather than the native index's older values. Existing 50-product limit remains a documented limitation, not a catalog-growth solution. |
| Route localization | JS `:4,19,37,83,91,104` uses `Shopify.routes.root`; header/native templates use Shopify routes | Do not replace localized routes with hard-coded `/cart`, `/search` or English-only product URLs. Logo home link and category/product links must continue using actual routes/objects. |
| Cart refresh | JS `:76–86` fetches `?section_id=studio-header`, parses `[data-cart-content]`, replaces that block and updates badges from `data-count` | Keep the static `studio-header` section identity and server-rendered cart markup. Preserve one `[data-cart-dialog]`, `[data-cart-error]`, `[data-cart-content data-count]` and all `[data-cart-badge]` hooks. Moving the dialog into another section requires an explicit coordinated JS change and renewed tests; a visual refactor alone must not do this. |
| Cart controls | JS `:89–106`; header drawer contains line keys, native removal URLs, quantities, totals, discounts and checkout form | Preserve `[data-open-cart]`, `[data-close-cart]`, `[data-cart-remove data-key]`, `[data-cart-quantity data-key]`, `aria-busy`, errors and focus return. Keep line-item keys rather than product IDs for changes. Keep native full-bag links and server totals/discounts; never replace them with static mockup values. |
| Add/variant form | JS `:1,101–106`; `sections/studio-product.liquid:3–6` | Preserve `ProductForm`, `name=id`, quantity names/rules, `[data-add]` labels/disabled state, `[data-variants]` option metadata, `[data-product]`, `[data-price]` and `[data-compare]`. The approved homepage is a browsing page; do not add quick-buy controls or fake availability to make it match a mockup. |
| Gallery/zoom | JS `:1,70–74`; product section and layout image dialog | Keep `ProductImage`, thumbnail `[data-image]/[data-alt]`, `[data-zoom-image]`, `[data-image-dialog]`, `[data-close-image]` and `[data-zoom-target]`. Do not reuse these data attributes on brand logos or unrelated icons: thumbnail handling assumes a surrounding `[data-product]`. SVG refactoring must preserve parent controls and keyboard behavior. |
| Mobile menu | JS `:110–111`; header `.mobile-menu` details/summary | Retain native details/summary unless replacement behavior is deliberately implemented and tested. Current code selects the first `.mobile-menu`, closes it with Escape and restores summary focus; outside clicks close it. Avoid duplicate menu instances. |
| Enquiry | JS `:113–114`; contact template and unavailable product link | Preserve `ContactForm`, native contact field names, required email/message, `[data-enquiry-product]` and `[data-enquiry-topic]`. Product query is accepted only when it exactly matches a current option; topic value is currently literal `Product availability`. Keep that value or coordinate the JS change. Product links must stay URL-encoded and must not place orders. |
| Collection cards | JS `:47–68`; `studio-collection.liquid`; `snippets/studio-card.liquid` | Keep `.product-card` and category/price/availability data, `[data-catalog-grid]`, result/empty hooks and filter state if card markup changes globally. Price data stays in minor currency units. New homepage category navigation should be actual collection links; don't attach incomplete catalog filtering hooks to it. Preserve sort form and no-JS Apply fallback. Existing client filters are only rendered for a single collection page of up to 24 products. |

## Compact responsive UI constraints

- Keep header/search/menu/cart popovers unclipped. Current suggestions are absolutely positioned within `.instant-search`; menu is absolutely positioned under the header. Applying `overflow:hidden` to the compact header or its wrapper can clip these working interfaces.
- Keep one visible accessible control for each action. A large logo graphic must not shrink bag/menu/search hit areas or overlap them. At minimum inspect 320, 360, 390 and 430px, plus desktop. Long titles, prices and unavailable labels must fit without hiding essential information.
- Preserve native form semantics when replacing text glyphs with SVG icons: existing `type=submit` search control, `type=button` non-submit controls, accessible names and keyboard focus. Decorative SVGs are hidden from assistive technology. Icon geometry is not the control's hit area.
- Preserve the skip link, `MainContent`, focus outlines, status/error announcements and reduced-motion behavior. New visual ordering must not make keyboard reading order incoherent.
- A shorter sticky header requires reconciling existing `scroll-padding-top` and product sticky offsets (`assets/studio.css:35,37`). Verify anchored category/story/contact sections and product controls remain visible. A constant old offset is not evidence of the new header's correct behavior.
- Product-led hero must use actual Shopify product title/image/price/URL/availability. Keep unavailable status and enquiry clear. Preserve eager/high-priority hero loading and declared image dimensions; later card images can remain lazy. The static concept's y≈764 catalog position is a reference for composition, not an invariant for every device or text scale.
- The floating support control is fixed at the bottom right. Check it does not cover card actions, hero labels, dialog controls or contact submit controls after rearrangement. Moving support to normal flow is acceptable if its destination remains available.

## Reusable logo/icon constraints

- Use the CEO-approved outlined vector assets and existing Rozmiso spelling/R. Do not rebuild the wordmark using another font or add the removed tiny descriptor on mobile.
- Current `.brand-mark` width/height rules are for a square compact mark. A full horizontal logo needs a separate selector and explicit aspect ratio/dimensions; assigning it `.brand-mark` would squeeze it into the 34–46px square rules.
- Header/footer home links should announce Rozmiso once. Inline SVG paths or `<use>` content within an already-labelled link should be decorative. Keep current search/bag/menu control labels when changing icon geometry.
- Shared snippets/sprite integration must preserve viewBoxes, stroke inheritance and actual rendered icons on the theme preview. A successfully exported icon sheet does not prove a referenced sprite works on the storefront.
- Preserve the custom favicon image setting and both blank/default and custom-image branches in `layout/theme.liquid:5–6`. Verify SVG/32px fallback/touch-icon URLs after changing masters. Check the actual storefront tab, not only Shopify's theme editor. Reusing the new favicon family must not leave references to missing filenames.
- Preserve title, canonical, description, Open Graph metadata, `content_for_header`, deferred script loading and `window.rozmisoLabels` initialization. If adding the reviewed share-card fallback, retain product/page images when available rather than overwriting every social image with the brand card.

## Baseline validation performed

Ran the existing source-loaded JSDOM test file with the bundled Node runtime:

`operations/launch-2026-10-05/theme-tools/commerce-flow.test.cjs`

Result: **4 passed, 0 failed** against the current authoritative `assets/studio.js`. Covered:

1. Excluding stale indexed drafts and using current product price/availability.
2. A late older search response not overwriting the newer query.
3. Duplicate submissions sending one add request and displaying server totals.
4. Inventory rejection restoring server quantity without retrying the mutation.

These tests use synthetic DOM/network fixtures. They do not test the real theme markup, mobile layout, focus behavior, gallery, filters, enquiry, favicon or actual Shopify checkout. No customer cart/order/network mutation was performed. This is a baseline, not acceptance of the pending implementation.

## Small required regression set after implementation

| Check | Acceptance evidence |
|---|---|
| Search | One complete search UI; query a current product; actual price/unavailable status; ArrowDown/Up and Escape; outside click; Enter fallback; network failure; no stale draft. Re-run the four existing tests if JS changes. |
| Navigation | Menu open/close/Escape at 320–430px; active category links; logo home link; no clipped menu/suggestions; keyboard focus visible. |
| Product/enquiry | Real gallery/zoom and unavailable CTA; no enabled purchase due to visual change; enquiry prefill exact current product and topic; required-field validation without sending customer messages. |
| Empty cart | Bag opens, server refresh succeeds, closes and restores focus; native bag link works with JS disabled/unavailable. |
| Populated/error cart | Use existing synthetic fixtures or an explicitly authorized isolated test environment. Check quantity/remove, busy state, errors, discounts, badge and server subtotal. Do not alter production inventory merely to test styling. |
| Responsive visual | Actual local/theme preview compared with approved boards at 320/360/390/430px and desktop; 200% text enlargement, no horizontal overflow, no covered actions or image labels. |
| Identity | Primary/reversed logo rendering, actual 16/32px favicon, valid asset references and coherent icons; store tab observation distinct from theme-editor observation. |

## Missing inputs and proposed handoff

No new identity-dependent facts are needed for this visual implementation. The parent-provided CEO approval covers the reviewed direction; ordering, supplier, inventory, payments and policy terms are outside this report. A theme preview or local render must provide the visual/interactive evidence that source inspection and baseline mocks cannot.

Codex should provide these constraints to the implementing worker, review the scoped diff and collect preview screenshots/interaction evidence. Do not report commercial launch or successful checkout based on this review.

## Independent review and Codex acceptance

This reviewer did not author the pending theme implementation. That implementation remains unreviewed until its artifacts exist. Report acceptance and task-board updates are reserved for Codex.
