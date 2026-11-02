# Work report - T030 / Lane B

Status: SUBMITTED
Author and lane: website_research, Lane B
Date and environment: 14 October 2026; F:/Dropshipping; PowerShell; RTK unavailable (Get-Command returned no command).
Department and worker role: Shield / Evidence auditor, research scope

## Result

Researched current official Shopify, W3C and Google web.dev guidance and translated it into the customer tests below. These are verification criteria, not findings about the current live store. No browser accounts, website files, catalog records or settings were modified. Local WORK-LOG history informed prioritization only; root must verify current remote state.

The strongest customer test is whether a visitor can identify the right item, understand exactly what is included and what it costs, find genuine support/fulfillment information, and complete the supported buying flow without errors. A polished homepage or a high automated score cannot establish that whole outcome.

## Artifacts and scope

Only this report was written: `team/reports/T030/research/WORK-REPORT.md`. No code changes or deployments. Sources below were accessed on 14 October 2026. Suggested test cases are this lane's application of that guidance to Rozmiso, not claims that the sources prescribe these exact store-specific cases.

## Evidence and validation

### Prioritized customer test matrix

| Priority | Customer question and practical test | Acceptance / evidence root should retain | Basis |
|---|---|---|---|
| P0 | Can I actually buy what this page offers? Cross-check selected variant, displayed availability, button state and saved inventory policy. Exercise unavailable products without changing stock. | UI matches actual variant availability. No enabled purchase action that silently fails; do not turn on overselling merely to remove a sold-out state. Historical zero-stock evidence needs fresh verification. | [Shopify inventory behavior](https://help.shopify.com/en/manual/inventory-and-locations/setup/selling-when-out-of-stock) explains the explicit option needed to sell tracked out-of-stock items; it does not prove supplier stock. |
| P0 | What will I receive? For each of the 21 referenced products compare title, selected variant, package quantity, image geometry, product use, dimensions/materials where verified, and text against the exact supplier source. | Save an item-by-item discrepancy list. Six real product views per gallery is the user's requirement; a shared social link/CTA card does not count as a sixth product photo. Do not invent measurements or performance claims. | [Shopify product descriptions](https://help.shopify.com/en/manual/products/details/product-descriptions) lists specifications and uses; [writing guidance](https://help.shopify.com/en/manual/products/details/product-descriptions/write) calls for factual, supported benefits and scannable content. Exact six-view count and AI-only production are user requirements. |
| P0 | What is the full cost, where do you deliver, and what happens if it is unsuitable? Open shipping/returns/contact links from both PDP and footer. Check the displayed currency, applicable shipping information and checkout totals against approved business facts. | Clear reachable information; no fabricated delivery promise, free-shipping threshold, COD option, return window or seller details. An unknown owner fact remains a dependency, not plausible marketing copy. | [Shopify trust research](https://www.shopify.com/blog/customer-trust-checklist) highlights product, cost and business transparency. It reports an older North American study; it is directional evidence, not an India-specific conversion guarantee. |
| P0 | Does the transaction work? Root should distinguish empty cart, unavailable item, valid item, failed/successful payment, order processing and notification checks. | Record exactly which flow was exercised. A product/cart screenshot is not a successful order. Full payment/order tests remain deferred until the authorized configuration and stock/provider prerequisites exist. | [Shopify launch testing](https://help.shopify.com/en/manual/intro-to-shopify/initial-setup/setup-prepare-for-launch) recommends test orders to check checkout, processing, stock, shipping and taxes. This is guidance, not authorization for this lane to activate a gateway or place orders. |
| P1 | Can I find the right category or item? Follow Home → Home care/Kitchen/Travel → product; search “brush”, “juicer”, a partial title and a nonsense term; sort/filter and clear all. | Correct titles, images, INR prices and destinations; search/no-results/empty-filter states give a useful next step; browser Back works. Navigation remains usable on phone. | [Shopify store design checklist](https://help.shopify.com/en/manual/intro-to-shopify/store-design) supports clear menus, product media, About/Contact, mobile testing and complete purchase testing. These particular queries are proposed local cases. |
| P1 | Can I operate the store without a mouse? Tab through header, search, menu, product gallery, cart and contact form. Open drawers, use Escape, then continue. | Visible logical focus, keyboard operation, drawer focus containment and return to opener, announced changes/errors and labeled controls. Retain a short manual test record rather than relying on an automated score. | [Shopify theme accessibility](https://shopify.dev/docs/storefronts/themes/best-practices/accessibility). It explicitly warns its practices alone do not establish complete accessibility. |
| P1 | Can I read and tap this on a small phone? Test 320, 375/390 and 768 CSS-pixel widths and desktop; zoom/reflow; inspect gallery strip, long titles, filters, sticky header and form errors. | No whole-page sideways scrolling or clipped text/action. At 320 CSS pixels reflow is required for ordinary content, with exceptions for genuinely two-dimensional content. Scrollable thumbnail strips must not expand the page. Focus must not be entirely hidden by sticky UI. | [W3C Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html). Passing these samples does not establish WCAG conformance. |
| P1 | Are controls comfortably tappable and readable? Measure close/search/cart/filter/thumbnail/quantity controls and actual text/background pairs. | Use Shopify's 44×44 CSS-pixel recommendation for primary controls. WCAG 2.2 AA target minimum is 24×24 or qualifying spacing/exceptions, not universally 44×44. Normal text contrast ≥4.5:1; large text ≥3:1, subject to criterion exceptions. Test muted text and text over images separately from base brand colors. | [Shopify accessibility](https://shopify.dev/docs/storefronts/themes/best-practices/accessibility), [W3C Target Size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [W3C Contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). |
| P1 | Can I understand product details if the poster text is too small or unavailable? Check live text beside the six images, image alternative text and image-link/button names. | Keep important specifications/use/care in readable HTML; image-only headings/details must not be the sole source. Describe product images concisely; functional image alternatives express the action/destination. Decorative images can use empty alt. | [W3C Images of Text](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html), [Functional Images](https://www.w3.org/WAI/tutorials/images/functional/), [Shopify accessibility](https://shopify.dev/docs/storefronts/themes/best-practices/accessibility). |
| P1 | Does it load and respond well on mobile? Measure homepage, dense collection and heavy product page with real content, same device/network settings and recorded tool versions. Interact with search, filters and gallery. | Compare before/after lab results and record largest image transfer sizes. Field “good” targets: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, all at the 75th percentile, separately mobile/desktop. Absence of field data is unknown, not a pass. | [Google Web Vitals](https://web.dev/articles/vitals), [Shopify performance testing](https://shopify.dev/docs/storefronts/themes/best-practices/performance/testing-for-performance). A single lab run cannot certify actual customer performance or field INP. |
| P2 | Do the new image galleries degrade speed? Inspect image URLs/sizes, dimensions, eager/lazy behavior and layout shift. | Responsive Shopify image derivatives; explicit dimensions; prioritize the actual initial LCP image and do not lazy-load it; lazy-load offscreen media. Avoid downloading six full-resolution originals immediately. | [Shopify performance practices](https://shopify.dev/docs/storefronts/themes/best-practices/performance). These practices support improvement, not a guaranteed score. |

### Store-specific interpretation

Keep the agreed ivory/forest visual system consistent, while checking every functional contrast pair. Category wording should reflect the actual home/kitchen/travel items. India/INR context means check actual configured market and checkout currency; it does not establish nationwide serviceability, COD, tax correctness or any particular customer payment preference.

The owner's future domain is `rozmiso.in`; the owner explicitly retains purchase/setup. Root can test the actual internal storefront host and separately record final .in link validation as pending until DNS/store connection exists. Do not describe an unresolved domain as working, or substitute invented contact information to make pages appear finished.

Public copy should follow the latest final-product direction and remove obsolete editorial preview language where present. The customer-facing availability state must remain factual. A launch-style headline cannot override real zero inventory or unavailable payments. Likewise, synthetic product photography needs exact-object review: plausible but incorrect handles, compartments, accessories or scale would undermine the factual product presentation.

## Missing inputs and dependencies

Fresh live state and exact-product image review belong to root. Genuine seller/support details, approved shipping/serviceability, returns terms, verified supplier stock and payment readiness cannot be derived from these UX sources. This report does not provide legal or tax approval. No real customer message or form submission was sent.

## Proposed handoff

Root should reproduce the P0/P1 cases, fix observed code/copy defects in the authoritative source with backup, and retain before/after responsive evidence. Use PASS, FAIL, NOT TESTED and OWNER INPUT NEEDED per case. Keep local code acceptance, published-theme verification and commercial readiness distinct. Report actual remaining gaps; do not promise “100% perfect”, comprehensive WCAG conformance, validated India operations or complete checkout unless the corresponding evidence exists.

## Independent review - completed by a different person/agent

Reviewer: Codex pending.
PASS / CHANGES_REQUIRED / BLOCKED: Pending.
Reasons and evidence: Await root review of source relevance and live test results.

## Codex acceptance

Pending. Only Codex updates this section and the shared task board.

### Codex scoped acceptance — 14 October 2026
ACCEPTED for primary-source research and explicit verification limits. Applied to sampled live/preview customer tests in ../WORK-REPORT.md. Research does not establish complete accessibility, field performance or commercial readiness.
