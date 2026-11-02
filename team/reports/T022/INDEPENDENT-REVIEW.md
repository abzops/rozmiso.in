# T022 independent source and behavior review

Reviewer: csv_chat_review, independent of author
Date: 8 October 2026
Result: PASS for local candidate integration/upload preparation. Shopify preview and visual acceptance remain required before a deployment-complete claim.

Read the task, author work report, deterministic builder, exact eight-file manifest, changed Liquid/JavaScript, regression fixtures and reported validation. Independently reran `node --test team/reports/T022/regression.test.cjs`: all 13 tests passed, zero failures. Recomputed authoritative/candidate hashes and all file differences: exactly the eight reported files differ, every manifest hash matches, no authoritative drift detected. Other theme files, including CSS/config/locales/assets, remain byte-identical.

The implementation establishes prelaunch state on the body, uses it in rendered PDP/card/checkout controls and checks it before JavaScript add submission. Available variants remain unavailable to theme-managed addition during preview; variant switching/finally handlers preserve that guard. The submission guard precedes the optional dialog early return. Checkout buttons are disabled with descriptive note IDs that remain distinct between full bag and drawer. Cart update/removal remains operable; this is appropriate cleanup behavior. Controls remain theme UX protection, not a backend sales lock or guarantee against direct requests.

Native predictive results absent from the first 50 local records are retained after ID/title/URL/finite-price checks, with same-origin product URL and textContent title rendering. Existing local records retain local metadata. The current suite covers beyond-index discovery, malformed/offsite rejection, currency amounts and async ordering. Native currency responses still need actual Shopify verification during preview, as acknowledged by author.

Enquiry now uses a bounded text input/datalist so a beyond-index product title can prefill. It accepts ordinary customer text rather than claiming verified product identity. Native form submission, required email/message fields and escaping remain present.

Large-collection native filters use real collection.filters, GET parameters and preserved selected values while sorting. They persist through fewer/zero results by evaluating all_products_count. When native configuration is absent, no fabricated filter capability is displayed. Small catalogs retain original local filters. Native catalog filtering and pagination remain dependent on Shopify execution/configuration, rather than mocked fixture acceptance alone.

No blocking implementation issue found in the bounded patch. Author's official Liquid-validator success is recorded in WORK-REPORT.md; this reviewer independently reran behavioral/Liquid fixture tests but did not rerun the official validator. Their fixtures intentionally replace Shopify form/render/pagination plumbing and cannot establish live visual or backend acceptance.

Handoff: Codex may integrate only these eight reviewed files after preserving rollback and verifying unchanged source hashes. Then check Shopify-rendered desktop/mobile layout, native search/currency, PDP/cart preview disablement and enquiry prefill. Preserve tracked-zero/DENY and publication controls; do not describe preview UX as backend checkout locking or infer selling launch.
