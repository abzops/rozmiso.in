# Work report - T022

Status: SUBMITTED
Author and lane: Codex worker A, Store theme developer
Date/time and environment: 8 October 2026, Windows/PowerShell, F:/Dropshipping
Department and worker role: Store engineering / Theme developer

## Result

Prepared an isolated candidate at `team/reports/T022/theme-candidate` with eight scoped file changes. Authoritative source remains unchanged. CSS, fonts, images, theme configuration, translations, product copy and brand styling are byte-identical to the copied source. No live actions occurred.

Preview mode now explicitly disables product addition and full-bag/drawer checkout controls, even when Shopify marks a variant available. JavaScript variant switching cannot re-enable preview addition, and submission guards operate without the optional cart drawer. Bag updates/removal remain usable. This is enforcement in theme markup and JavaScript only: direct Shopify cart/checkout endpoints, other channels, apps and modified browser requests remain outside its scope. Preserve proper stock/publication settings; do not claim a backend checkout lock.

Predictive search now keeps valid native Shopify results outside the local 50-item index. Same-ID local results still supply current local title/availability/price; external/malformed non-product URLs are excluded. Native decimal amounts remain major currency amounts, while existing Liquid data is converted from minor units as before. INR and zero-decimal JPY presentation are tested. Native result titles are inserted with textContent. The former behavior deliberately discarded every native hit absent from local records; it therefore could not support a larger catalog. The candidate trusts Shopify's same-origin published search results rather than treating the first 50 as an exhaustive allowlist. Stale search-index publication must still be checked live.

Collections with an unfiltered total above 24 can render native Shopify GET refinements when configured filters are exposed in `collection.filters`. Selected list/price values persist through sorting; native refinements remain when filtering narrows to one page or zero results. Small collections retain existing client filters. No native filter configuration was fabricated or enabled: a larger collection with empty `collection.filters` still lacks refinements. Codex must inspect Search & Discovery filter configuration before reporting catalog-wide filtering complete. This is intentionally not page-local filtering disguised as full-catalog filtering.

Product enquiry becomes a bounded text field with the existing first-50 datalist suggestions. Products beyond 50 can prefill their title without needing an option in a capped select. The field accepts ordinary text up to 200 characters and retains the native contact form. A prefilled title is customer input, not verified product identity or an order.

## Artifacts and scope

- `team/reports/T022/TASK.md`: bounded owner/reviewer contract prepared before edits.
- `theme-candidate/**`: complete isolated 39-file theme; eight changes below.
- `CHANGED-FILES.json`: source/candidate SHA256 per changed file.
- `CANDIDATE.patch`: recoverable unified diff against authoritative source.
- `VERIFIED-RESULTS.json`: evidence summary and all unchanged-file paths.
- `regression.test.cjs`, `TEST-RESULTS.txt`: meaningful behavioral and Liquid-render tests and passing output.
- `build_candidate.py`: deterministic single-use candidate preparation; refuses an existing destination.
- `save_review.py`: compares production hashes and untouched files; creates patch/evidence.
- `resolve-deps.mjs`: task-local fallback module resolver for the official Shopify validator.

Changed candidate files: `assets/studio.js`, `layout/theme.liquid`, `sections/studio-collection.liquid`, `sections/studio-header.liquid`, `sections/studio-product.liquid`, `snippets/studio-card.liquid`, `templates/cart.liquid`, `templates/page.contact.liquid`.

All worker writes are within T022. No board edits, production modification, deployment, external messages, spending, account settings or invented terms.

## Evidence and validation

Thirteen tests passed, zero failed, in `TEST-RESULTS.txt`. The tests exercise:

- Native result beyond the local index, INR decimal amount, JPY amount, local override, offsite/malformed rejection and stale async response ordering.
- Preview available-variant disablement and an attempted add after removing the disabled attribute.
- Preview add/checkout prevention without a drawer and permitted cart updates.
- Normal available/unavailable variant transitions, duplicate-add suppression, server totals and preview cart removal.
- Product 51 enquiry prefill as safe text.
- Rendered PDP matrix for preview true/false and available/unavailable variants.
- Rendered full/drawer checkout with an existing cart for preview true/false.
- Native refinement persistence across three pages, one filtered page and zero matches; selected price/list and sort preservation.
- Missing-filter configuration remains absent, while the small catalog retains controls.

Liquid-render tests use LiquidJS fixtures and replace Shopify-only form/render/paginate plumbing with deterministic harness markup. They verify branch/output contracts, not Shopify backend behavior, actual pagination/filter execution, or visual appearance. JavaScript tests use jsdom with mocked network responses, not live account data.

The official `shopify-liquid/scripts/validate.mjs` full-theme validator passed all seven changed Liquid files with success=true and no findings. Initial invocation failed with ERR_MODULE_NOT_FOUND because the plugin helper lacks bundled theme-check packages. A task-local resolver reused the already installed workspace packages; no dependency install or plugin/source modification was required. Reinvocation then succeeded. JavaScript is executed by the behavioral suite and parses without errors.

`save_review.py` confirmed all changed authoritative hashes still match the pre-edit originals, and all other source files match the candidate byte for byte. This includes CSS/config/locales and assets. Local structural/behavioral PASS does not establish Shopify preview/render or desktop/mobile visual PASS.

Documentation consulted on 8 October 2026:

- https://shopify.dev/docs/api/ajax/reference/predictive-search — decimal price/native response fields and locale-aware requests.
- https://shopify.dev/docs/storefronts/themes/navigation-search/filtering/storefront-filtering — native filter URL handling.
- https://shopify.dev/docs/api/liquid/objects/filter — active list/price filter properties and parameter names.
- https://shopify.dev/docs/api/liquid/objects/collection — total versus filtered count semantics.
- https://shopify.dev/docs/storefronts/themes/tools/theme-check — validation scope.

## Missing inputs and dependencies

Native Search & Discovery filter configuration and a fresh Shopify-rendered mobile/desktop check are pending. Native price/currency and search-index results should be verified with actual store responses after integration. Shopify inventory/channel controls remain essential for preventing sales outside theme UX. Seller/payment/supplier/policy facts remain other workstreams; this candidate cannot invent or resolve them.

## Proposed handoff

Codex independently reviews the patch, test fixtures and exact scope. If accepted, integrate only the eight changed files after confirming source hashes have not drifted, validate the combined theme, and obtain actual Shopify preview/mobile/desktop functional/visual evidence before deployment. Record backend availability and configured native filters separately. No live permission or selling launch is inferred from this submission.

## Independent review - completed by a different person/agent

Reviewer: Codex pending
PASS / CHANGES_REQUIRED / BLOCKED: Pending
Reasons and evidence: Author does not approve implementation.

## Codex acceptance

Pending. Only Codex completes this section and updates the task board.

## Later local source integration - 8 October 2026

Under Codex's subsequent explicit assignment, exactly the eight reviewed files were integrated into authoritative `rozmiso-studio-theme` at 06:40:03 UTC. Originals were backed up before any source write in `source-backup`. All eight new hashes match the reviewed candidate; all 31 other files are unchanged. See `SOURCE-INTEGRATION.md` and `SOURCE-INTEGRATION.json` for later-state evidence. Earlier source-unchanged statements above describe preparation, not the later integration state. No live/browser or board action occurred; remote draft verification and storefront visual QA remain with Codex.

## Final CSS acceptance and integration

Codex subsequently accepted the two-rule mobile CSS correction after observing draft theme 159016681664 at 390 × 844 with document clientWidth = scrollWidth = 375 and internal thumbnail scrolling retained. The CSS original was backed up, and only candidate CSS was integrated. The final source has exactly nine changed files relative to the original, all nine backups verified, and all 39 source files match the final candidate. The validated 39-file ZIP is `rozmiso-reviewed-theme.zip`; final evidence is `FINAL-INTEGRATION.md`, `FINAL-INTEGRATION.json` and `CHANGED-FILES-FINAL.json`. Earlier eight-file evidence remains historical. Larger-catalog filters/search beyond 50 are fixture-tested only; current live scope is fifteen published products. No worker live/browser or board action occurred.
