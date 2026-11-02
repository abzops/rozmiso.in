# Rozmiso launch status — 5 October 2026

The storefront design is built and saved in Shopify. Shopify currently labels **Rozmiso Studio — Launch Preview** as Active. The business is not ready to accept orders: checkout explicitly says “This store can’t accept payments right now.”

Theme editor: https://admin.shopify.com/store/rozmiso/themes/158905270464/editor

## Delivered

- A responsive cream, pine and sage storefront, original brand copy, real supplier product photography, editable homepage sections, product/gallery/variant forms, collection sorting, search, cart and contact templates.
- No fabricated testimonials, reset countdowns, fake postcode checks or unsupported fulfillment claims in the new theme. Removed the registered trademark symbol because registration was not verified.
- Four visible DeoDap-sourced products with supplier SKUs, descriptions, shop-hosted images and zero tracked stock. Five older products with unrelated stock photography and unsupported stock/specifications are preserved as drafts, hidden from sales channels.
- Formula-driven margin workbook: Product decisions, Unit economics and Sources. Reconciled calculated results; no formula errors found.
- A standalone theme ZIP containing the 24 new theme files. It does not contain the older unused sections retained in the Shopify duplicate.

## Product decisions

| Product | Observed supplier price | Proposed price | Estimated profit per placed order | Decision |
|---|---:|---:|---:|---|
| USB Rechargeable Fabric Shaver | ₹177 | ₹799 | ₹38.16 | Primary sample / controlled test candidate |
| 5-in-1 Rechargeable Cleaning Brush | ₹239 | ₹649 | −₹105.13 | Organic or very low acquisition cost only |
| Everyday Travel Organizer Pouch | ₹117 | ₹349 | −₹230.20 | Recalculate as combined-shipment add-on |
| 2-in-1 Soap Dispensing Cleaning Brush | ₹119 | ₹299 | −₹228.77 | Recalculate as combined-shipment add-on |

These are candidates, not proven winning products. Supplier public availability is not a confirmed inventory count or a dropshipping agreement. Observed prices are not contracted landed costs.

The base model uses ₹180 acquisition cost per placed order, 5% pre-dispatch cancellation, 18% RTO of dispatched orders, 3% refunds of delivered orders, 70% COD, shipping/reverse shipping, handling, packaging, payment charges, stock losses, overhead and an illustrative 18% output-GST allowance without input credits. The fabric shaver's estimated margin is 7.46% of expected net retained revenue, with break-even acquisition cost ₹218.16. This is planning contribution, not an audited final tax profit. Supplier subscription costs, actual fee quotes and applicable tax treatment must replace assumptions before spending.

## Supplier assessment

**DeoDap** is the initial sourcing candidate because exact product listings, public prices, weights, SKUs and images could be inspected. Its Shopify/CSV fulfillment offerings require a current quote and agreement: https://dropshipping.deodap.com/pricing.php . Confirm image-use rights, current inventory, variant assortment, invoice/GST treatment, dispatch, COD settlement, RTO charges and integration costs.

**vFulfill** is a managed sourcing alternative requiring RFQ and landed-cost comparison: https://vfulfill.io/pricing/ . **Baapstore** is another quote-based alternative: https://baapstore.com/pages/pricing . Neither is connected or purchased.

**Roposo Clout** is excluded because its official page reports closure from 1 April 2026: https://app.roposoclout.com/b2b/login .

Exact product sources and observed metadata are retained in `operations/launch-2026-10-05/catalog.json` and the workbook Sources sheet.

## Verified shopping flow

- Homepage and supplier images rendered in Shopify.
- Existing product variant selection changed displayed price and URL from ₹799 to ₹1,399 for the two-unit option.
- Add-to-bag created the correct cart line and subtotal.
- Checkout opened with the correct item and total; payment was disabled. No order was placed and no personal checkout data was entered.
- The test item was removed; cart returned to zero.
- Theme Liquid/schema validation passed all 24 files; subsequent header/footer branding changes passed validation separately.
- Mobile appearance inspected in Shopify's mobile preview. This is visual inspection, not a completed cross-device checkout test.

## Remaining launch requirements

1. Connect a supplier under confirmed current terms, obtain real inventory and shipping fees, and approve samples. No supplier account, paid subscription or binding agreement was created.
2. Configure an online payment provider or confirmed COD fulfillment arrangement. Shopify shows no configured online provider, inactive PayPal and no enabled manual method. Payment onboarding may require the owner's business/bank/KYC details.
3. Align Shopify shipping with the supplier service and planned offer. Current domestic rate is ₹379 with a 3–5-business-day label; the workbook models merchant-paid shipping with no customer shipping revenue. The existing international zone lists ₹1,800. Do not advertise these delivery times without supplier confirmation.
4. Confirm the real business/return address and contact details. The current location/policy contains a placeholder-like `123456` address component. Shipping, refund and terms policies are absent; the existing privacy policy must also be reviewed against actual operations.
5. Recalculate margins from contracted costs; enable only approved products, synchronize inventory, and select them in the homepage product blocks or a curated collection. The four supplier-based products are now Active and published for browsing, with zero tracked stock. Homepage cards link to their product pages; Shop all shows all four products, category filters and automatic sorting. Purchase buttons correctly remain disabled until real stock is confirmed.
6. Complete one controlled paid checkout and fulfillment test, check mobile checkout, verify taxes/invoices and policy links, then remove store password protection for the launch. Password protection was not changed during this work.

The theme ZIP is a design deliverable. Uploading or activating it does not resolve supplier fulfillment or checkout readiness.
