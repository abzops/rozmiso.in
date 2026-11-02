# Work report - T021

Status: SUBMITTED
Author and lane: Codex, root integration; worker B independent CSV/media review
Date: 8 October 2026; live Rozmiso Shopify store

## Result

Imported all eight supplied demo products through Shopify's native CSV importer with overwrite and all-channel publication unchecked. Source is Files/Demo_CSV (1).xlsx, converted to CSV; Files originals are unchanged. Catalog increased from 20 to 28 products. Eight new products are DRAFT, unpublished, zero inventory, tracked with DENY overselling. Existing 15 active zero-stock products and five drafts retained.

## Artifacts and scope

demo-reviewed-draft.csv; import-changes.json; INPUT-INDEPENDENT-REVIEW.md; saved-products.json; saved-inventory-publication.json; imported-drafts.png; MEDIA-URL-STATUS.json; MEDIA-IMPORT-REVIEW.md.

25 source-cell changes: eight Published FALSE, eight Status draft, eight inventory quantities zero, one malformed Google Shopping condition cleared. Other source values preserved, including unverified product descriptions/prices/weights/costs. No selling launch or supplier purchase.

## Evidence and validation

Independent review compared all 3430 cells against original workbook and confirmed the exact delta. Import preview identified 8 products, 8 SKUs, 70 image references. Post-import API checks confirm saved handles/SKUs/prices/default variants and inventory/publication controls. Every new product has null publishedAt and onlineStoreUrl. Shopify saved 55 images: keyboard8, rack11, straightener9, bottle8, juicer9, earphones0, laundry10, warmer0. Independent checks found all 15 omitted source URLs return HTTP404; 55 accessible images decoded successfully. Preview count is not a saved-media count.

## Missing inputs and dependencies

Supplier media replacements/rights; stock, exact variants, physical and packed weights, safe accurate claims and commercial terms. Products remain drafts until these are resolved. No alternative image or inventory invented.

## Independent review

csv_chat_review: PASS bounded import; media incomplete due unavailable source links. See INPUT-INDEPENDENT-REVIEW.md and MEDIA-IMPORT-REVIEW.md.

## Codex acceptance

ACCEPTED for draft import with explicit 15-image source limitation. Commercial product approval remains pending.
