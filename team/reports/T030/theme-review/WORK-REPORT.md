# Work report - T030 / Lane A

Status: SUBMITTED
Author and lane: Codex website_theme_review / Lane A
Date/time and environment: 14 October 2026; Windows PowerShell; F:/Dropshipping
Department and worker role: Store engineering / Theme developer, read-only reviewer

## Result

Reviewed all 27 text source files in the authoritative `rozmiso-studio-theme` (Liquid, JavaScript, CSS, JSON), plus task/charter/worker instructions and the historical T022 implementation report. No theme or account changes were made. Findings below concern current local source, not a verified live theme. Root must compare live state before integration. The current source still contains explicit preview/prelaunch copy that contradicts the latest owner direction; removing that copy must not fabricate inventory or payment readiness.

## Artifacts and scope

- This report: `team/reports/T030/theme-review/WORK-REPORT.md`.
- Read-only source root: `F:/Dropshipping/rozmiso-studio-theme`.
- No browser, account, network, dependency installation, customer form submission, theme editing, log editing or board editing.
- RTK availability check returned no command; ordinary PowerShell used under the project exception.

## Evidence and validation

### 1. P1: Replace hardcoded prelaunch statements throughout the theme

**Evidence:** `config/settings_data.json:4` enables `prelaunch_mode`; `config/settings_schema.json:23` labels it a preview notice even though it also blocks cart actions. `locales/en.default.json:32` says “Collection preview · Orders are not open yet”; `:76`, `:98`, `:118` also assume a future ordering launch. `templates/index.json:78`, `:89`, `:96` contain the same assumption in story and FAQ copy. `sections/studio-product.liquid:6` renders `launch_note` for *every unavailable variant*, including stock outages independent of prelaunch mode.

**Effect:** A customer sees preview/future-launch claims even after the owner requests final public content. A normal sold-out item is incorrectly described as never open for orders.

**Recommended patch:** Replace public strings with current, neutral stock/support statements (for example, “Currently unavailable. Contact us about this product.”); replace the story with a factual product-discovery statement. Delivery/payment FAQ must not claim setup completed, methods accepted, COD, dispatch speed or return periods. Decouple the announcement text from a commerce guard, or rename the setting clearly. Preserve tracked-zero inventory and DENY unless root obtains actual stock evidence. Do not simply disable the guard to make the storefront appear ready.

**Checks:** Root compares published theme and actual product availability; search all customer-facing sources for `preview`, `not open`, `not available yet`, `once ordering`, `first collection`, `payment setup`. Check home, unavailable PDP, fabric-shaver FAQ and nonempty cart. Test that unavailable variants remain disabled after copy changes.

### 2. P1/P2: Submitted search bypasses Shopify search and disagrees with suggestions

**Evidence:** `templates/search.liquid:1` ignores `search.results` and loops `collections.all.products limit: 50`, requiring literal substring matches for every word against only title/type/description. By comparison, `assets/studio.js:17-36` retains native predictive-search products, including records outside that first-50 local index.

**Effect:** A customer can see an item in suggestions, press Enter or “View all results”, and get no result because Shopify's native matching/search grammar is discarded. Products beyond the first 50 cannot appear in submitted search. The 50-product cap is a scaling defect; the semantic mismatch can occur at the current catalog size for native matching such as variant/SKU/tag queries or supported search grammar.

**Recommended patch:** Use Shopify's paginated `search.results` for submitted results, keep `type=product`, and render only products. If a local substring fallback is retained to compensate for indexing delay, label/merge it deliberately and deduplicate; do not replace native results. Add pagination and total count from the same source as the rendered items.

**Checks:** Root tests a known exact title, an ordinary partial term, no results, a native SKU/variant/tag match only if present, and a supported quoted query. Ensure suggestion click and Enter agree. A fixture with 51+ products is useful for the cap; do not claim it is currently live.

### 3. P2: Variant changes leave stale purchase guidance and quantity constraints

**Evidence:** `sections/studio-product.liquid:7` renders quantity min/step/max from the initially selected variant only. Its option data lacks quantity-rule fields. `assets/studio.js:2` updates price, comparison, add-button state, URL and image, but not quantity rules or the availability note/enquiry link rendered conditionally at `sections/studio-product.liquid:6-7`.

**Effect:** With differing variant rules, changing options leaves the first variant's permitted quantity. Starting on an unavailable variant then selecting an available one can retain unavailable messaging and enquiry CTA; starting available then selecting unavailable omits that explanation. These are conditional multi-variant defects; no claim that current products have differing rules.

**Recommended patch:** Expose each option's min/increment/max and update/reset/clamp Quantity on change. Render a reusable availability region and enquiry link that JS toggles from current variant + the explicit store guard. Keep button, note and enquiry state derived from one function. Update image alt from the selected variant image or clear product-specific alt to the product title.

**Checks:** Test initial and changed available/unavailable states in both directions; min1/step1 → min2/step2/max6 → no max; confirm old max is removed. Verify zero stock remains unpurchasable. Native server validation remains necessary.

### 4. P2: Contact enquiry fields lose submitted custom data after an error

**Evidence:** `templates/page.contact.liquid:1` rehydrates name, email and body but supplies no submitted-value state for custom `contact[Topic]` and `contact[Product]`. The JS prefill at `assets/studio.js:130` reads only the URL query, and unconditionally forces “Product availability” when that query exists.

**Effect:** On a server-side form error/re-render, the topic resets to General question and a typed product can disappear. A URL-prefilled product can force the topic back to availability even if the user selected another topic.

**Recommended patch:** Preserve custom form values where supported by Shopify's form object; otherwise keep only these non-secret custom fields in the form across the validation flow, and initialize query prefill only when there is no submitted value. Never store message, email or private customer details in a shared report or log.

**Checks:** Root may use a local rendered fixture or controlled invalid submission without sending a real support message; confirm product/topic preservation after an error and correct query prefill. Actual email delivery cannot be inferred from rendering.

### 5. P2: Header collection links have no missing-collection fallback

**Evidence:** `sections/studio-header.liquid:1` always renders home-care, kitchen-essentials and travel-essentials URLs in both navs. `sections/studio-hero.liquid:5` already guards the same collections against blank values, showing the inconsistency.

**Effect:** If a collection is removed/unpublished/renamed, the header can render empty href values and reload the current page instead of navigating. Current collection existence needs live verification.

**Recommended patch:** Use the same nonblank guard as hero, or use a verified all-products URL fallback with an appropriate category query if that exact client-filter category exists. Avoid blindly assuming collection handles are permanent.

**Checks:** Verify the three live category destinations desktop/mobile and test a missing-collection fixture. This is conditional resilience, not proof that current links are broken.

### 6. P2: Theme typography/color differs from the newly requested common creative theme

**Evidence:** `assets/studio.css:4` uses ink `#26342e`, paper `#fbfaf6`, accent orange `#b75132`; `:6` uses Manrope sans-serif for h1/h2. The current creative standard `team/reports/T029/social/ROZMISO-THEME-STANDARD.md` calls for ivory `#F5F0E7`, forest `#173E33` and premium serif headings. Existing PDP description CSS does not style h3s as that common hierarchy.

**Effect:** Social products and the storefront visibly change identity despite the user's consistency request. This is a design mismatch, not a technical failure.

**Recommended patch:** Root should compare actual live desktop/mobile to the accepted creative pack and then apply one agreed token/heading system globally, including `.rte` description headings, rather than adding per-product inline styles. Preserve accessible contrast and product image legibility. Do not replace an accepted live theme based solely on source defaults.

**Checks:** Screenshot home/catalog/PDP/contact at 390px and desktop, compare with final carousel references, inspect heading wrapping and keyboard-focus contrast.

### Additional verification targets, not confirmed defects

- `assets/studio.css:27` makes the entire product-info block sticky at desktop widths although it includes long descriptions and details. Confirm all content remains reachable at short desktop heights and zoom200%; if awkward, limit sticky behavior to the gallery or small purchase panel.
- `sections/studio-product.liquid:4` gives the zoomable div a tabindex and keyboard handler; the custom focus-visible rule at `assets/studio.css:6` does not include that div. Browser defaults may show focus; verify before calling it invisible. Add `[data-zoom-image]:focus-visible` if needed. Thumbnail selected state is not exposed by aria-current/aria-pressed; add a single selected-state model if revising the gallery.
- `layout/theme.liquid:11` loads two TTF variable fonts totaling404,864 bytes (DM Sans240,164; Manrope164,700). `font-display:swap` already helps. WOFF2 conversion/subsetting is an optimization opportunity, not a measured performance diagnosis. Measure real LCP/CLS before prioritizing; above-the-fold product cards are all lazy-loaded, so check actual home LCP.
- Native `<dialog>` cart and zoom, Escape handling, native contact forms, safe textContent predictive results, responsive srcset images, reduced-motion handling, semantic labels and stock-derived disabled state are useful existing foundations. Preserve them during fixes.

## Missing inputs and dependencies

Live theme identity/saved source, genuine stock and dispatch capabilities, legal seller/policy/support facts, enabled payment methods, actual customer contact delivery and checkout outcomes remain root/owner verification. This worker neither assessed nor certified them. Historical T022 tests establish prior fixture coverage only; they are not fresh live evidence.

## Proposed handoff

Prioritize the stale copy and native submitted search, then the common theme update and only the variant/form resilience justified by actual usage. Root independently checks each proposed fix against current live state, backs up changed files, implements within authorized scope and tests desktop/mobile customer flows. No “100% perfect”, completed order or WCAG-conformance claim is supported by this source review.

## Independent review - completed by a different person/agent

Reviewer: Codex pending
PASS / CHANGES_REQUIRED / BLOCKED: Pending
Reasons and evidence: Root retains independent integration and live verification.

## Codex acceptance

Pending. Only Codex completes this section and updates the task board.

## Implementation extension - 14 October 2026

Root subsequently authorized bounded production-source changes after fresh public source comparison and a full backup at `team/reports/T030/backups/before-customer-fixes`. Under that extension, four files were changed: `assets/studio.js`, `templates/search.liquid`, `sections/studio-product.liquid`, `sections/studio-header.liquid`. Earlier read-only statements describe the initial review, not this subsequent implementation.

- Submitted search now paginates native `search.results` by24, renders product matches and native total, with empty/unperformed states and pagination. Internal requests retain `type=product`; a manually constructed mixed-content search URL is outside that normal flow and its native total may include nonproduct objects skipped by this product grid.
- Variant changes update price, comparison, disabled button, shared unavailable note/enquiry visibility, min/increment/max quantity rules, a valid quantity, URL, image alt and selected thumbnail. A removed maximum no longer sticks from the previous option. The existing commerce guard and Shopify availability remain authoritative.
- Gallery thumbnails expose initial/current `aria-pressed` state and preserve actual image alt text with the product title fallback.
- Both header menus omit missing category collections instead of rendering empty URLs.
- Query prefill avoids overwriting existing product/topic values. `templates/page.contact.liquid` is unchanged: arbitrary custom Shopify form-field rehydration is not established by supplied documentation, so no unsupported `form[Topic]` assumption or private browser storage was introduced. Full server-error custom-field preservation remains unresolved.

Evidence: `SOURCE.patch` contains the exact four-file diff; `CHANGED-FILES.json` binds before/after SHA256 to the root backup. `regression.test.cjs` ran7 meaningful jsdom/LiquidJS fixture tests, all PASS; `node --check rozmiso-studio-theme/assets/studio.js` exited0. The tests cover stock transition in both directions, changed quantity rules/removal of max, commerce-guard submission protection, gallery alt/selection, nonoverwriting prefill, native result outside the local index, empty/unperformed/pagination search and missing collection guards. Tests stub Shopify-only render/paginate plumbing; they do not exercise Shopify backend search, actual pagination or contact delivery. Root retains official theme check, independent code review, sync and live desktop/mobile verification. No deployment/account action was performed by this worker.

## Mobile category implementation extension - 14 October 2026

Root authorized `sections/studio-collection.liquid`, `snippets/studio-card.liquid` and then explicitly authorized the additional shared `snippets/studio-category.liquid`. The small-catalog facet now uses a single captured mapping for both category chips and product card data/category labels. Home care/Home Improvement→home-care; Kitchen/Kitchen essentials/Kitchen Storage Container & Rack→kitchen-essentials; Travel essentials→travel-essentials; Beauty Health & Personal Care→personal-care; blank and every unknown supplier type→other-essentials. Matching strips whitespace and case. Existing home-care/kitchen-essentials/travel-essentials URL keys remain. Only represented categories appear; the All products control always remains. Larger-than24 catalogs retain the existing native server-filter branch unchanged. No backend product taxonomy was changed, and no products are excluded from All products.

`MOBILE-CATEGORY.patch` and `MOBILE-CATEGORY-CHANGED-FILES.json` record these three files against the root backup (new snippet has no prior hash). The expanded suite passes10/10 tests. Added fixtures represent21 products across all eight supplied live type strings plus a22nd unknown type; they are a synthetic coverage set, not an independently fetched live inventory. Actual shared Liquid snippet renders in both facets and cards. Checks assert every card remains, unknown/blank fallback, six maximum controls including All/Other, only represented groups for a category collection, native filters for a60-product fixture, existing kitchen URL query selecting exactly its nine fixture matches, and Clear filters restoring all21. The first expanded run found a missing test-fixture label global; the fixture was corrected, then all10 passed. No production fix was needed for that fixture error.

Independent review of root's typography changes: forest/ivory tokens now match the creative standard; headings use Georgia and root's `.rte h2,.rte h3` rule provides forest23px serif headings,1.3 line-height and25px section spacing. This resolves the source-level description-heading mismatch identified above. Root also added visible selected-thumbnail borders and zoom focus. These are coherent source changes; acceptance still needs the root's fresh mobile/desktop visual comparisons. Mobile card titles remain13px serif as before the latest size adjustment; assess readability at390px. No styles/locales/config were edited by this worker. The source snapshot's retained `Manrope` font definition may now be unused; removal is optional and should follow font-usage verification rather than assume a performance regression.

### Supplier punctuation correction

Root's actual uploaded preview exposed a missed supplier punctuation difference: `Beauty, Health & Personal Care` and `Kitchen Storage, Container & Rack` contain commas, unlike the initial supplied fixture strings. The first mapping incorrectly placed those products under Other essentials. Corrected only `snippets/studio-category.liquid` to remove commas before strip/downcase matching. Added exact punctuated live strings and mixed-case/space coverage;11/11 tests now PASS. Regenerated the mobile diff/hash manifest. Earlier ten-test coverage did not establish exact live-string equivalence; the current eleven-test result supersedes it. Root retains snippet sync and fresh Personal care/Kitchen verification.

### Codex scoped acceptance — 14 October 2026
ACCEPTED for bounded implementation. Root independently reran11/11 tests, official Theme Check clean, full40-file remote integrity matched, and verified live theme159259001024 after publication with sampled mobile/desktop flows. Latest source has14px mobile card titles. Full transactions/contact delivery and remaining catalog upload are outside this acceptance. See ../WORK-REPORT.md.
