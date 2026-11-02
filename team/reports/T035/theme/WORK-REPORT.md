# Work report — T035 theme launch review

Status: SUBMITTED; launch acceptance BLOCKED on required live/commercial evidence
Author and lane: launch_theme_review, Lane A
Date and environment: 22 October 2026, Windows/PowerShell, F:/Dropshipping
Department and worker role: Store engineering / independent theme reviewer

## Result

Read current WORK-LOG.md, TEAM_ROSTER_AND_RULES.md and complete T035 brief. Reviewed authoritative theme's configuration, product, collection, search, cart, header/footer, layout metadata and browser scripts. No theme changes, live changes, browser use, log/board writes or credential access. RTK lookup produced no available command; ordinary PowerShell used.

The source preserves native product data and order controls, but it is explicitly configured to pause ordering. No source-only change can certify commercial readiness. No new definite source defect justified an immediate theme patch in this bounded review.

## Findings and exact handoff

| Priority | Finding / evidence | Required action |
|---|---|---|
| P0 before order launch | `config/settings_data.json:4` has `prelaunch_mode: true`. `sections/studio-product.liquid:4` sets can_order false; product CTA disabled at line42. `templates/cart.liquid:1` and `sections/studio-header.liquid:40` disable checkout; `assets/studio.js:113-119` prevents theme-managed submits. | Keep until current genuine inventory, payment, shipping, fulfillment and policies pass. After those facts and checkout evidence are verified, exact activation patch is current.prelaunch_mode=false, not deletion of the guards. Verify both server-rendered and JavaScript paths plus live cart/checkout after publication. Default schema true may remain as safe new-theme default. |
| P1 catalog requirement | Six corrected soap images are hardcoded only in `sections/studio-product.liquid:13-28`. `snippets/studio-card.liquid:7` uses item.featured_image; `layout/theme.liquid:11` uses page_image for sharing and line14 native featured image for predictive search; `sections/studio-header.liquid:40` uses native cart/suggestion images. `sections/studio-product.liquid:67` uses native product structured_data. Generic PDPs use native product.images. | Finish actual reviewed product media uploads and gallery cleanup, then verify collection, search, cart, OG and product JSON image coverage. Theme-only image override does not update catalog media, social share image or JSON-LD. Do not publish held incorrect soap assets from old126-image batch. The corrected six T033 soap assets are the current candidate; root has their identity review. |
| P1 rendered design | Current clean Bento CSS has no current rendered screenshot. `design-qa.md` explicitly blocked. Wide desktop cap/gutters and gallery/summary balance remain unresolved against selected05. | Obtain real desktop/tablet/phone browser screenshots, compare with05, fix visible issues and retest before theme publication. Source syntax or tests do not prove design acceptance. |
| P1 operational policy evidence | Footer renders only nonblank native shop.policies (`sections/studio-footer.liquid:20`). PDP shipping/returns at line60 use real policy URLs only when nonblank, otherwise generic contact fallback. The theme contains no definitive shipping SLA, refund window or seller policy terms. | Root must inspect current policy records and contact delivery. Empty-policy fallback avoids invented promises but is not launch-complete policy publication. Do not synthesize owner terms from a template. |
| P1 actual checkout evidence | All visible cart/search links use Shopify routes and native forms; order controls depend on real variant availability plus pause mode. No reviewed source fact proves payment capture, rates, taxes, notification delivery or refunds. | Record authorized test checkout and resulting order/payment/notification evidence after commercial setup. Keep no-real-orders claim until then. |
| P2 stale inherited SEO | Root's fresh HTTP inspection reports old orders-not-open copy in search HTML. `layout/theme.liquid:8` takes page_description for every route except index, so search inherits Shopify's global store description. This is distinct from factual stock labels. | Safe scoped patch: use settings.brand_description for index/search/cart/list-collections/404 only, which have no owner-authored per-page SEO description. Preserve native page_description for product, collection and page so custom descriptions survive. Recheck draft metadata with fresh HTML; do not broadly remove availability copy or alter commercial guards. |
| P2 owner domain | No hardcoded myshopify.com customer link exists in reviewed Liquid/JS source. Navigation uses routes and actual canonical_url. | Domain/canonical and SSL need fresh verification after owner connects rozmiso.in. Do not hardcode the pending domain into Shopify route paths. |

## Evidence and validation

Created and ran `team/reports/T035/theme/static-audit.py`, recording STATIC-AUDIT.json.161 literal locale references resolve; missing literal snippets0 and missing literal assets0. This checks local literal references only, not dynamic references, store pages, external URLs or browser behavior.

Current source has native contact form (`templates/page.contact.liquid`) with required email/message, success and native errors, product enquiry prefill and no marketing signup assertion. Relative contact route still requires root's live HTTP check. Blank default variant label omitted in drawer; quantity/variants preserve native product min/step/max at PDP. Native structured data retained. No fabricated reviews, ratings, sale counters, COD, shipping promises or unsupported launch-preview copy were found in current selected landing/product source.

Root subsequently supplied fresh HTTP observations:21 public products,0 available,10 galleries below6 images, and shipping/refund/terms routes404. These are parent-provided observations, not independent network checks by this lane; root retains their response evidence. Parent also flagged `[email]` while inspecting contact HTML: the exact source uses `name="contact[email]"`, a required Shopify native form parameter. That field name is not an example seller email or unfilled contact placeholder. No seller-email placeholder was found in current theme.

Existing T033 four behavior fixtures and T030 eleven regressions were already recorded passing in T034. CSS/source reference auditing here did not justify rerunning unchanged fixtures. This report does not promote their older pass into current live checkout evidence.

## Artifacts and scope

- F:/Dropshipping/team/reports/T035/theme/WORK-REPORT.md
- F:/Dropshipping/team/reports/T035/theme/static-audit.py
- F:/Dropshipping/team/reports/T035/theme/STATIC-AUDIT.json

Only the assigned report folder changed. No patches proposed that invent missing business inputs or bypass browser access.

## Missing inputs and dependencies

Root current live inventory/catalog verification, current payment and fulfillment state, owner policy facts, successful test checkout, catalog app authorization if still required, and actual browser access for T034 comparison. Prior logs are historical evidence; this lane made no fresh remote-state assertion.

## Proposed handoff

Root integrates current CLI/HTTP evidence with operations lane. Complete catalog upload from reviewed assets when supported authorization exists; verify every surface. Resolve actual design comparison. Enable ordering only after commercial evidence is complete. Theme source review is not acceptance of the whole launch.

## Independent review / Codex acceptance

Pending root acceptance. Only Codex updates shared board and log.
