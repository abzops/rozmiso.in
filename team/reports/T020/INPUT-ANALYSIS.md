# Demo workbook and chat evidence

Read on 8 October 2026. Inputs: `Files/Demo_CSV (1).xlsx` and `Files/Drop shipping Committee.zip`. No live Shopify action, supplier contact, or source edit was performed by  this worker.

## Workbook

The supplied demo is an XLSX workbook containing real-looking supplier catalog records in a legacy Shopify product CSV layout. It is neither an empty format template nor the promised full 7,000-product catalog. One sheet, `Sheet1`, covers A1:AW71: 49 headers, 70 data rows, 8 distinct product handles and 8 default variants. All 70 rows contain distinct image URLs; repeated handles are intentional gallery continuation rows. No duplicate full rows, duplicate variant SKUs, empty handles, formulas, or non-HTTPS image values were found.

| SKU | Product | Source price | Compare-at | Source cost | Source qty | Images |
|---|---|---:|---:|---:|---:|---:|
| 6187_laptop_keyboard_cover | Keyboard cover | 40 | 199 | 20 | 500 | 8 |
| 2796_2layer_kitchen_rack | Two-layer kitchen rack | 496 | 1199 | 248 | 180 | 11 |
| 6168_hqt_909b_hair_straightner | Hair straightener | 770 | 3999 | 385 | 23 | 10 |
| 6422_ss_fancy_btl_360ml_approx | Stainless steel bottle | 416 | 999 | 208 | 68 | 8 |
| 2793_manual_hand_juicer | Hand juicer | 46 | 299 | 23 | 432 | 9 |
| 7271_cnh_sport_earphone_no1 | Earphones | 78 | 399 | 39 | 620 | 7 |
| 6186_15in_foldable_laundry_bag | Laundry bag | 270 | 799 | 135 | 60 | 10 |
| 2792_coffee_mug_and_warmer | Mug and warmer | 896 | 2999 | 448 | 30 | 7 |

These are source values, not verified current inventory, retail pricing, commercial costs or profit. Currency is not specified in the workbook. Every price is exactly twice source `Cost per item`; that arithmetic does not account for delivery, payment fees, returns or advertising.

All eight source product rows contain `Published=TRUE`, `Status=active`, inventory tracker `shopify`, policy `deny`, fulfillment service `manual`, shipping required TRUE, and an inventory quantity. Source inventory sums to 1,913 units. Seven products have taxable TRUE and the straightener FALSE; no tax rationale is supplied. Seven vendors are `ediscountshops.com`, one `Simply Smart`; neither proves the present contract partner. Barcode fields repeat the textual SKUs. Every image alt text contains third-party store branding. SEO title/description and most Google Shopping fields are empty. `Standardized Product Type` and `Custom Product Type` are legacy headers whose current acceptance must be checked in Shopify's preview rather than assumed.

The descriptions and images are specific catalog content. No literal TODO/TBD/demo placeholders were detected. Structural completeness does not establish product accuracy or publication rights.

## Import risks and recommended handling

1. Raw active/published status plus unverified positive inventory risks presenting sample records as buyable products. Import the authorized demo into draft/unpublished state and avoid inventory claims until supplier stock and fulfillment are confirmed. Keep any source-preserving CSV distinct from a transformed upload CSV and record the transformations.
2. Check the current target store and all eight source handles/SKUs before import. Avoid overwriting existing products. This worker did not inspect live handles.
3. Row 13, column `Google Shopping / Condition` (AL13), contains a lone backtick on a gallery continuation row. Preserve it in the raw export; remove it only in a documented import copy if Shopify rejects the value.
4. The straightener description ends in three literal quote characters. Its title refers to scalp/head massage while the body describes a heated straightening brush. The keyboard-cover description discusses keyboard lighting and molding features. These need supplier/model review before public use.
5. The earphone body describes Lightning, 3.5mm and Type-C choices, but only one Default Title variant is provided. An import must not invent those options or imply a choice exists.
6. `Variant Grams` often contains volumetric/shipping weight rather than physical item weight: laundry bag 9,320g versus body item weight 185g; keyboard cover 327g versus 30g; rack 1497g versus 715g; juicer 548g versus 80g. Straightener variant 280g conflicts with body physical/ship 350g. Determine the intended packed/shipping weight before rates rely on these fields.
7. Compare-at values and claims such as food-grade, waterproof, protective heating and leak-proof need evidence before public sale. Source values remain in the lossless artifact, with no claim of current discounts or verified performance.
8. Shopify-hosted image URL syntax is valid. Network availability, exact-model imagery and permission remain unverified in this worker scope. Source image query timestamps refer to 2022; this is a historical clue rather than proof of current stock.
9. Validate source tax flags, barcode expectations, target currency and legacy column mapping in Shopify preview. Product inventory behavior may depend on target locations; verify saved state after import.

## WhatsApp ZIP

All two members were read: `chat.txt` and `chat.md`, covering 7–8 October 2026. These are two renderings of the same conversation, not two independent confirmations. No images, videos, audio or listed documents are included in the ZIP. Omitted attachments include Hot Selling.pdf, All products 21-04-2026.pdf, Dropshipping plan pdf.pdf, L135 DISTRIBUTOR AND SUPER STOKEIST.xlsx, images, voice and the CSV-plan video. The workbook was supplied separately in Files.

The supply-chain owner forwarded the demo and a Shopify import-help link, proposed choosing the CSV plan, and asked the store owner to upload the demo and report back. Another team member acknowledged; the store owner replied okay. These support the current user instruction to test the demo import. They do not prove a purchased plan, signed terms or fulfillment activation.

Forwarded marketing messages claim a Shopify plan with 6,000+ products/training, three months without hosting charges followed by  $29, and a 7,000-product CSV for an existing website. Another message says orders must be submitted through a software order panel and packing/shipping would be handled through DeoDap using the merchant's name without DeoDap branding. These are claims from forwarded text, not verified current Shopify pricing, a quote, or proof that white-label service is configured.

No chat evidence establishes an exact plan fee, payment, contract, product-specific stock, dispatch SLA, shipping charges, COD, RTO/returns/refunds terms, stock synchronization, panel access, packaging costs, tax invoices or media license. The advertised manual order-panel workflow does not establish automatic order forwarding or stock synchronization. No supplier contact details or private chat text were copied into these reports.

## Artifacts and validation

`demo-source-lossless.csv` preserves every source cell value in its single sheet as UTF-8 CSV, with empty cells as empty fields, booleans TRUE/FALSE and integral numeric values serialized without `.0`. All 49 headers and 70 rows, multiline HTML, Unicode and quote characters survive a CSV reader round-trip. This is lossless for the cell values, not workbook styles or cell types. `workbook-rows.json` also retains original typed values and records any non-General numeric formats. `validation.json` records all products, image positions, counts, anomalies and SHA-256. `chat-archive-validation.json` records archive members and confirms all included text was read. The source files were opened read-only and their hashes recorded.

Reviewer handoff: review the raw CSV and JSON, reconcile a documented safe upload derivative, verify the live target and duplicates, check Shopify's import preview, then independently verify all eight saved products and galleries. Commercial launch readiness is outside this demo import.
