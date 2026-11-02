# T035 — Launch preparation

Latest correction22October2026: owner states total70INR shipping. Use flat70INR per order regardless of item quantity; this supersedes the previous per-item answer. LAUNCH-CONFIG.json, WORK-LOG.md and task board corrected. Earlier shipping-basis statements below are historical. No Shopify rate has been applied; verify single-item and multiple-item carts after Admin access is available.

22 October2026. Codex status: WAITING; bounded technical preparation accepted, store launch not accepted.

## Completed

Codex coordinated two bounded specialists, reviewed their source and operations evidence, verified current Shopify theme roles, and ran anonymous public read-only catalog/route diagnostics. Theme159552962752 remains live; selected Modern Bento159555977408 remains unpublished.

Current public diagnostics:21 products, none available to buy;10 native galleries have fewer than6 images. Homepage, collection, search, contact and anonymous cart JSON respond200. Shipping, refund and terms policy endpoints respond404; privacy responds200. This does not verify payment/provider, shipping configuration, inventory quantities, taxes, notification delivery or browser experience. The contact `[email]` marker is a legitimate Shopify form field, not an unfilled seller detail.

Theme reviewer checked161 locale references and literal asset/snippet references with no missing entries. Operations reviewer verified126 prepared image hashes,21 description files and6 corrected soap WebPs. The obsolete soap image set is explicitly held; CATALOG-PREFLIGHT.json provides corrected replacement references. Native catalog uploads remain pending and affect collection/search/cart/sharing surfaces beyond the theme-only soap gallery.

Codex implemented one safe metadata fix in layout/theme.liquid: system routes index/search/cart/list-collections/404 use the neutral brand description instead of stale inherited store SEO. Product, collection and page descriptions remain native. Official Shopify CLI strict check returned no findings; uploaded only layout/theme.liquid to the existing unpublished draft and pulled it back with exact matching SHA256. Original saved as theme-before.liquid. This fix is saved in draft, not publicly deployed.

## Owner instruction and unresolved facts

Owner confirmed shipping70INR for every product. Asked whether an order with2 products totals70 or140 in shipping. Amount recorded in LAUNCH-CONFIG.json; rate basis remains pending and no rate was applied. This instruction does not supply dispatch time, return terms, supplier availability or payment activation.

The complete remaining owner outcomes are in operations/LAUNCH-HANDOFF.md. Need genuine launch SKU quantities/fulfillment, approved shipping/returns/seller/tax facts, active payment/provider evidence and monitored support/contact delivery. Historical8October billing/provider observations were not promoted to current facts.

## Access and launch boundary

Browser control still reports disabled; no alternate automation workaround used. T034 image comparison therefore remains blocked under its existing design-qa.md. A read-only Shopify Admin CLI query with --no-input failed with no stored app authentication. Plugin directory separately reports Shopify installed:false for the current integration; installation/connection suggestion issued. Working theme CLI access does not grant shipping/catalog/payment administration.

No product stock, payment settings, policy terms, shipping rates or ordering guards changed; no real order/message/payment sent. No claim of visual perfection or order readiness. WORK-LOG.md and task board updated; preserved all prior entries.

## Resume

1. Resolve the pending70-versus140 shipping answer and save the intended basis.
2. Restore supported browser access and/or install/connect the Shopify integration to provide Admin access, then freshly verify settings and perform authorized catalog/rate changes.
3. Supply genuine commerce facts, publish accurate policies and verify product media across all catalog surfaces.
4. Compare desktop/tablet/mobile Modern Bento renders, resolve visual issues and publish the chosen theme only after acceptance.
5. Verify checkout rates/payment and order/notification outcomes before enabling and declaring order readiness. An approved test order/payment scope is required if money or a real commitment is involved.

Evidence: PUBLIC-CHECK.json; DRAFT-INTEGRITY.json; LAUNCH-CONFIG.json; theme/WORK-REPORT.md; operations/WORK-REPORT.md; operations/CATALOG-PREFLIGHT.json. Internal administrative checks use the Shopify domain; customer brand domain remains rozmiso.in with setup retained by owner.
