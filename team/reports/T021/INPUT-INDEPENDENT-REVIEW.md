# T021 input independent review

Reviewer: csv_chat_review, separate agent from T021 CSV author
Date: 8 October 2026
Result: PASS for the reviewed input file. No Shopify action performed.

Read `prepare_import.py` and independently compared `demo-reviewed-draft.csv` directly against every original XLSX data cell, rather than relying on the author's assertions. Checked `import-changes.json` against the calculated differences, ignoring only changelog entry ordering.

- One source sheet; all 49 headers remain unchanged.
- All 70 data rows and 3,430 data cells were compared after explicit CSV serialization of booleans, empty cells and integral numeric values.
- Exactly 25 cell changes: 8 Published TRUE to FALSE, 8 Status active to draft, 8 Variant Inventory Qty values to zero, and AL13 Google Shopping / Condition lone backtick to an empty field.
- All 8 product/variant rows retain inventory tracker shopify, policy deny, and now have zero inventory, draft status and unpublished state. Tracker/policy required no changes because those safe values already existed in the source.
- The change log exactly matches every calculated change and contains no additional change.
- All other cells, including all 70 image URLs, handles, SKUs, descriptions, multiline HTML, options, prices, compare-at values, costs, weights, tax flags and third-party vendor/alt text are preserved.
- Source contains no formulas, so the builder's data_only=True does not lose formula contents in this particular workbook. UTF-8 with BOM is readable by the independent CSV parser.

Reviewed CSV SHA-256: `80c6784bbd451a24d7d2623d3ecc8931dcba84ce61d429f87f83000a44ea979f`

This PASS authorizes the bounded input handoff. Current Shopify column acceptance, existing-handle behavior, image fetching, location inventory and persisted draft/unpublished status must still be verified by Codex during/after the import. The source content and commercial uncertainties recorded in T020 remain unresolved and do not affect this successful scope-preservation check.
