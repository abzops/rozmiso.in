# T021 media import independent review

Reviewer: csv_chat_review, separate from Shopify import executor
Checked: 8 October 2026, exact source URL GET checks completed 06:30 UTC / 12:00 IST
Result: product import counts verified; media shortfall is explained by dead source URLs.

Compared saved-products.json to the original XLSX row evidence retained in T020. The supplied saved snapshot has all 8 source handles, titles, SKUs and prices, each with one Default Title variant, DRAFT status and total inventory zero. This snapshot alone does not expose publication objects or per-variant inventory tracker/policy, so those require Codex's separate verification.

| Product | Source images | Saved images | Missing source positions | HTTP result for absent sources |
|---|---:|---:|---|---|
| Keyboard cover | 8 | 8 | None | — |
| Two-layer kitchen rack | 11 | 11 | None | — |
| Hair straightener | 10 | 9 | 9 | 404 |
| Stainless steel bottle | 8 | 8 | None | — |
| Hand juicer | 9 | 9 | None | — |
| Earphones | 7 | 0 | 1–7 | 404 for all 7 |
| Laundry bag | 10 | 10 | None | — |
| Mug and warmer | 7 | 0 | 1–7 | 404 for all 7 |
| Total | 70 | 55 | 15 | 15 unavailable source files |

Performed read-only HTTP GET requests to all 70 exact HTTPS URLs from the workbook, following server redirects, without removing query strings or guessing alternative paths. The 55 source URLs corresponding to saved filenames returned HTTP200 and all decoded successfully as image files. All 15 absent files returned HTTP404. No successful source URL is absent from the saved snapshot. Because Shopify changes the source store path and version query during import, file correspondence uses the exact source/saved URL path filename.

The unavailable straightener file is source position 9, filename `010_1a62e811-f4b8-4214-9a19-21800488aa6e.jpg`. All seven earphone and all seven warmer URLs are unavailable. The full exact URLs, timestamps, HTTP status, byte counts and hashes of accessible files are recorded in MEDIA-URL-STATUS.json. Responses were inspected in memory; no media file was written, uploaded, replaced or displayed.

Byte and decoded-pixel hashes were compared across accessible source files as a duplicate-content check. Dead URLs have no downloadable image bytes to compare, so this cannot prove whether their historical contents duplicated another file. However, their current404responses completely explain why the importer cannot fetch them. There is no evidence here of importer loss of accessible images.

Recommended result wording: 8 draft products imported, 55 images saved; 15 source image links are dead. Obtain actual replacement/original exact-model supplier files if complete galleries are needed. Do not invent imagery or use guessed alternate URLs, and keep affected products unpublished until their catalog evidence is reviewed.

## Final saved inventory and publication review

Independently read the later saved-inventory-publication.json GraphQL snapshot and matched all eight demo handles to original source records. All 8 are DRAFT, publishedAt null, onlineStoreUrl null, with every variant quantity 0, inventoryItem.tracked true and inventoryPolicy DENY. No imported variant violates this condition. All 15 ACTIVE products in the same snapshot also have every variant tracked, quantity zero and DENY; sales remain unavailable through this inventory configuration. Older unrelated drafts with positive inventory are separate from these imported/active records and were not changed by this worker.

Final result: PASS for the bounded demo import and saved prelaunch state, with an explicit 55/70 media result caused by 15 HTTP404 source links. This does not accept supplier terms, product claims, policies, payments or commercial launch.
