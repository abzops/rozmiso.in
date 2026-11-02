# T019 - Rozmiso workspace evidence audit

Status: SUBMITTED for independent Codex review. Prepared 8 October 2026 by worker A, Store/Shield evidence auditor. Scope: local files only; no live Shopify, supplier, payment or service-state assertions were refreshed by this worker.

The workspace contains a reviewed storefront and a useful team process, but also substantial historical material whose launch, supplier, health, margin and runtime claims conflict with the accepted evidence. The immediate import risk is that the theme's `prelaunch_mode` controls the announcement, not ordering. Product availability is the actual button gate. A positive or untracked inventory import can make products orderable even while the announcement says orders are closed.

## Coverage and exclusions

`INVENTORY.csv` enumerates every file reachable under F:/Dropshipping, including hidden paths, with path, size, extension, category and inspection status. `COVERAGE.json` is the exact point-in-time count; it changes while the other worker and orchestrator add artifacts. Enumeration reported no access errors. The initial snapshot contained 49,157 files and 1,626,447,189 bytes; refreshed inventory supersedes that initial count. Most files are dependencies, build outputs or browser state, rather than business files.

The audit script fully decodes eligible UTF-8 text files under 2 MB; JSON files receive parsing checks, first-party Python receives AST parsing, and the authoritative theme receives literal asset/snippet/section/translation and schema/template-reference checks. `TEXT-STRUCTURE.json` records eligible first-party text paths and structural results; `STATIC-CHECKS.json` records defects. Whole-file machine scanning is not equivalent to independent semantic verification of every assertion.

Human semantic review concentrated on the charter, board, operating plan, launch handoff, T001/T008/T018 reports, supplier/media readiness evidence, current theme product/cart/search/catalog/contact/layout/locales/settings, representative historical supplier/legal/domain/product/marketing claims, Gideon tooling, Open Dots documentation/seeding and Antigravity dispatch source. All other eligible text was structurally scanned and inventoried, not exhaustively fact-checked claim by claim. Historical theme snapshots were text-scanned and classified; they are not production authority. Fonts, images, executable tools, archives, spreadsheets and databases were inventoried, not executed or visually inspected by this worker. T020 separately owns the complete workbook and WhatsApp ZIP analysis.

Credentials, `.env` contents, browser profiles and database contents were excluded from reading. Browser-state filenames and sizes were inventoried only. Dependencies and `.next` build artifacts receive metadata coverage only. `operations/brand-direction-2026-10-06/tools` is the bundled third-party font tool installation. Large text and opaque/binary files remain explicitly labeled metadata-only. Existing automation, seeders, services and business scripts were not run. No database reset, model call, account change, message, purchase or production source edit occurred.

## Workspace map and authority

| Area | What it contains | How to use it |
|---|---|---|
| `rozmiso-studio-theme` | 39 authoritative theme files in the snapshot, including native cart/search/product templates and reviewed assets | Current implementation source; compare against freshly fetched Shopify state before deployment |
| `rozmiso-shopify-store` | 24 historical files, old theme/import/prototype | Historical only; do not deploy or import as current production |
| `team`, `.agents` | Department/worker cards, board, task reports, native runtime adapter and 22 profile definitions | Bounded on-demand roles with Codex as orchestrator; profiles do not establish running services |
| `operations` | Source generators, snapshots, supplier research, catalog/gallery manifests, media, third-party tools | Dated evidence and reproducible preparation; old generators can overwrite newer work |
| `outputs` | Dated deliverables and business/supplier/launch/tracker artifacts | Read their dates and limits; they are not current account state |
| `knowledge` | Nine research/playbook documents | Historical hypotheses; validate actual claims and business applicability before reuse |
| `automation` | Many one-off Shopify browser/import/publish scripts plus dependencies | Not an unattended production import service; review actual target and every mutation before any reuse |
| `open-dots` | Next.js/FastAPI application, dependencies/build output and local state | Separate historical software project; no current running connector or order-processing service proved |
| `gideon` | Agentic runtime proof of concept, drivers, tests and local memory database | Prototype; simulated logistics and incomplete economics cannot approve fulfillment |
| `Files` | Demo workbook and WhatsApp ZIP | T020 analyses them and prepares lossless conversion; local existence is not proof of Shopify import success |
| `.chrome-data`, `.chrome-session` | Private browser profile state | Excluded from content review; never include in portable business packs |

Active authority is `AGENTS.md`, `TEAM_ROSTER_AND_RULES.md`, complete assigned briefs, department cards and worker contracts. `INDIA_DROPSHIPPING_OPERATIONS_MANUAL.md`, `SHOPIFY_DEPLOYMENT_GUIDE.md`, old personas and legacy-redacted snapshots are historical inputs, not instructions. `READ_ME_FIRST_ORCHESTRATOR.md` correctly identifies https://rozmiso.myshopify.com and the studio theme source. The old guide's example `rozmiso-india` store and partner dashboard are not target-store identity evidence.

## Findings requiring action

### P0: preview mode does not enforce a commerce lock

`rozmiso-studio-theme/config/settings_data.json:4` has `prelaunch_mode: true`. Its only runtime use is `sections/studio-header.liquid:1`, which selects announcement text. `sections/studio-product.liquid:6` enables Add to bag when `chosen.available`; `assets/studio.js:1` follows variant availability, and `templates/cart.liquid:1` supplies checkout whenever the bag is nonempty. Source inspection cannot prove checkout is currently open, but it proves the preview flag alone does not close it.

For the requested import, inspect workbook status/publication/inventory values and actual target-store inventory behavior. Do not allow an import's inferred availability to become an accidental selling launch. Verify saved tracker, quantities, sell-when-out-of-stock, channel publication and storefront controls after import. If intentional draft/unavailable treatment changes source values, preserve the original lossless CSV and record the explicit adjustment separately.

### P0: historical import caused untracked inventory

`team/reports/T018/WORK-REPORT.md`, section Result and Artifacts, records that the eleven-product CSV imported untracked inventory despite quantity zero. Codex corrected all eleven to tracked zero stock and disabled sell-when-out-of-stock. `operations/catalog-expansion-2026-10-06/research/rozmiso-11-products-import.csv` omits tracker/policy columns. Re-importing it unchanged can undo the accepted availability correction. Treat it as evidence of a past import, not a ready-to-use current import file.

The saved `team/reports/T018/live-gallery-audit.json` reconciles fifteen PDP records, 80 images, at least four per PDP, fifteen disabled Add buttons and zero videos. Those are 6 October observations, not an 8 October live refresh. The independently reviewed count result remains useful; supplier allocation, legal stock, channel publication, payments and direct checkout enforcement do not follow from gallery counts.

### P0: real business and fulfillment inputs remain unresolved in reviewed evidence

`outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/LAUNCH-PREP-RESULTS.md`, Live blockers, records no configured primary provider, inactive PayPal, no pixels, unset customer policies, privacy address placeholder, domestic INR 379/international INR 1,800 shipping and unverified supplier/sample/fulfillment. These are dated unresolved observations; none should be presented as freshly checked current settings. `team/reports/T004/OWNER-HANDOFF.md` assigns genuine seller/support details, supplier terms/sample, payment verification and budgets to accountable humans. A WhatsApp discussion can add evidence but cannot stand in for actual activation, physical sample inspection or supplier-allocated stock.

Source contact form validation and its success message do not establish a monitored inbox: the launch report explicitly states no message was submitted and delivery remained untested. Current legal/tax applicability must be assessed from the real seller and transaction facts; this audit does not resolve it from old playbooks.

### P1: historical readiness and product claims are unsupported

`operations/winning_product_brief_ems_foot_massager.md:4` says Ready for Production & Ad Launch; line 23 says STRONGLY APPROVED; line 39 asserts 10x circulation and relief claims. It also drafts COD, free delivery, replacement and discounts without the contract/payment evidence now required by the active charter. No accepted sample/clinical/fulfillment evidence in this audit supports these statements. Do not recycle them into imported descriptions or advertising.

`knowledge/top_winning_products_india_2026.md:33` says all products were strictly vetted; line 22 states a 24–48-hour supplier SLA. This workspace does not establish a SKU-specific written SLA, tested samples or measured demand for those historical candidates. These are historical claims awaiting verification, not demonstrated winning products. `operations/master_marketing_and_funnel_playbook.md` prescribes daily test budgets and makes generalized algorithm/behavior claims; it is neither a campaign report nor spending authorization. The current catalog research deliberately uses qualitative rationale and uncertainty markers instead of winning percentages.

`knowledge/BRAND_IDENTITY_AND_DOMAINS.md` claims domains are 100% available, without a fresh registry check in this audit. Availability is transient; do not purchase based on that file. `knowledge/legal_gst_and_payments.md:20` supplies a categorical GST answer; it cannot replace current primary-source and fact-specific legal assessment. This finding concerns reliance on stale categorical text, not a new legal ruling.

### P1: obsolete deployment guide and mutation scripts can regress the store

`SHOPIFY_DEPLOYMENT_GUIDE.md` points to the old theme and five-product catalog, describes publication at line 39 and COD activation at line 64, and proposes payment/discount/paid-app setup. Those actions conflict with current source authority and unresolved commerce gates. The guide must not be followed automatically.

`automation` contains separate `publish_theme.js`, `publish_and_import_products.js`, `upload_and_publish_new_theme.js`, multiple retry/import/upload scripts and local browser connection helpers. File existence is not an idempotent pipeline or saved-state verification. Import retries may create or overwrite catalog state, and theme-upload helpers may publish old source. None was run here. Use the actual installed plugin/verified current UI/API for this task, with fresh identity, bounded mutation and saved-state reconciliation.

### P1: expanded-catalog mobile review is explicitly unfinished

`team/reports/T018/WORK-REPORT.md` and `INDEPENDENT-REVIEW.md` say the mobile screenshot did not reliably match intended viewport and must not be accepted as a visual PASS. Desktop screenshot coverage was partial. Earlier T011/T015 responsive checks were for earlier states. A fresh reliable mobile/desktop review of the expanded catalog and new imported PDPs is required before reporting visual completion.

### P2: catalog growth exceeds current discovery assumptions

`sections/studio-collection.liquid:5` paginates 24 products. Category/price/availability controls are generated only on a single-page collection; once a collection exceeds 24 items, those controls disappear by design. Existing category links still navigate, but customers lose refinements within that collection.

`layout/theme.liquid:13` builds a maximum 50-product local search index. `assets/studio.js:23` discards native predictive-search matches absent from that index, so a catalog beyond 50 can return no suggestion for a genuine native hit. Enter/full results remain a fallback. `templates/page.contact.liquid:1` also limits enquiry options to 50; imports exceeding that scope can prevent exact-product prefill. Current fifteen-product evidence does not trigger these capacity limits; the requested import may, depending on T020 counts. Review them when total eligible products crosses the limits.

### P2: runtime capability and finance prototypes must remain clearly bounded

`team/reports/T008/CLI-RUNTIME-RESULTS.md` proves cached headless Antigravity execution and a bounded supplied-text review, but not simultaneous account isolation or complete native file/browser tooling. `team/scripts/run-antigravity-task.cjs` enables only T001 and requires READY/dependency checks; it is not a general worker scheduler. The board retains T001 CHANGES_REQUIRED because the initial worker omitted full requested source coverage; T018 remains CHANGES_REQUIRED for broader media/mobile/readiness scope. Accepted bounded research does not erase those separate blockers.

`open-dots/README.md` describes configurable API inference, a default fake computer provider, no scheduled routine engine and one local owner. `seed_agents.py` defines old Director-as-master personas that contradict current Codex authority and would mutate the legacy database if run. No running service or provider entitlement was verified here. `.agents` profile count and Antigravity advertised tools are definitions/capability advertisements, not successful business operations.

`gideon/gideon/drivers/tool_driver.py` labels postcode risk simulated, deriving COD eligibility/courier recommendations from prefixes with no courier serviceability lookup. Its economics omits multiple actual costs and divides by delivery ratio without protecting RTO=1.0. It cannot validate logistics or margins. `operations/launch-2026-10-05/build-margins.mjs` is more explicit about assumptions, including CAC, shipping, recovery and tax, but still models estimates rather than agreed supplier/payment charges. Neither prototype output authorizes sales or profit claims.

### P2: status documents drift from the latest catalog

`ROZMISO-OPERATING-PLAN.md`, Current position, still discusses the existing four-product assortment; later T018 records fifteen. `READ_ME_FIRST_ORCHESTRATOR.md` highlights T011 and the earlier launch snapshot without the latest expansion limitation. The source/theme authority remains coherent, but the summary entry points lag behind the task reports. Codex should reconcile concise status references after fresh import verification, with explicit dates rather than rewriting old evidence as current.

## Structural verification outcome

`STATIC-CHECKS.json` recorded no first-party Python AST syntax errors, no eligible first-party JSON parsing errors, no missing literal authoritative-theme asset/snippet/section targets, no missing literal translations, no Liquid schema JSON errors and no missing JSON-template section source. This is useful integrity evidence, not a full Shopify Theme Check, accessibility certification, browser render, dependency-security audit or checkout test. Dynamic translation/asset names are outside the literal-reference checker. No existing tests or business scripts were executed.

Current source includes native route helpers, product structured data, quantity rules, product media render support, genuine unavailable-state labels and native contact/cart fallbacks. These are implementation positives; they do not supply actual supplier demonstrations, buyer reviews, delivered orders or legal policies. The shaver contents wording (`locales/en.default.json:114`) still needs physical-model/packed-contents confirmation before selling.

## Prioritized handoff

1. Codex reconciles T020's workbook/chat findings with the current connected Shopify store and imports the exact authorized scope with duplication/inventory/publication protection and saved-state evidence.
2. Verify new product/variant/image counts, exact SKUs, inventory tracker/policy, channels, active theme and actual mobile/desktop behavior; retain original source plus adjusted import artifact if adjustments are necessary.
3. Shiva supplies written exact-SKU fulfillment/stock/cost/returns/media terms and sample inspection; Abhinand supplies genuine business/support/provider facts and budgets; Roshan prepares monitored enquiry/support workflow.
4. Codex fixes or explicitly gates the preview/orderability mismatch and addresses 24/50-item discovery limits if import size warrants it, under a separate bounded source assignment.
5. Reconcile status entry points and fence obsolete playbooks/scripts so they cannot be mistaken for approved production instructions. Keep historical evidence intact, and record accepted evidence separately.

No full selling launch, confirmed profits, exact demo completion, live supplier connection or continuously running team is established by this local audit.
