# T039 independent integration review

Reviewer: Lane B catalog researcher. Date: 1 November 2026.
Status: CHANGES_REQUIRED for complete catalog readiness; factual copy/local preparation PASS. Public publication remains held.

Reviewed PRODUCT-PLAN.json, SOCIAL-PUBLISH-PACK.json and SHOPIFY-VERIFIED.json against catalog/RESULTS.json and the previously inspected exact supplier reference images. No external state was changed. This is an independent artifact comparison of root-provided saved live readbacks, not a new authenticated store read.

## Material findings

1. Existing astronaut draft retains the unverified legacy pair variant1899INR with title “2 Pieces (Bedroom + Gift Bundle - Save ₹300!)”. Single is now1299INR: two singles2598 minus pair1899 equals699, so retained saving300 is false even on the current draft's own prices. Neither bundle pricing nor packed contents were verified. Remove the savings statement or disable/review the bundle before any publication; do not simply replace it with a new unverified discount claim.
2. Astronaut retains legacy inventory90single+60pair,total150. Root plan says preservezero inventory; saved draft still has150. This is not evidence of supplier fulfilment. Keep DRAFT and explicitly report the historical quantities; either zero them within authorized cleanup or ensure the release gate cannot treat them as stock. The other four new drafts havezero inventory. No availability promise should rely on this snapshot.
3. Astronaut retains “bestseller” tag without sales evidence. Remove before release or establish genuine sales provenance. No current customer-facing bestseller claim was observed in the new HTML itself.

These are retained metadata findings, not evidence of public publication: all five products are DRAFT, no images uploaded, and the social pack correctly records published:false/metaDraftSaved:false.

## Passed checks

All five product titles, source filenames and first-variant retail prices match the supplied creatives: heatingbelt999, scalp999, tyre899, standingastronaut1299, pinkblender749INR. All source files exist. ProductIDs in the social pack match verified saved records. Four new variants have exact supplierSKU; astronaut deliberately keeps existingROZ-ASTRO-01/02 identifiers, with supplier4530 mapping recorded in the plan. Existingastronaut reused; no duplicate created.

The saved HTML matches PRODUCT-PLAN.json after whitespace normalization. Claims stay within reference/listing evidence: no medical relief/hairgrowth claim, no contradictory waterproof rating, no500kg load claim, no exact projection mode count or rechargeableprojector promise, no blendericecrushing/materialcertification/runtime. Removing blenderbladecount is conservative and accurate.380ml is supplier-listed, not physically measured. Brand vendorRozmiso denotes storefront branding, not evidence of manufacture.

Captions accurately state CODcurrentlyunavailable and omit a live purchaseCTA. They make no stock/discount/medicalperformance claim. All original videos advertiseCOD; an accurate caption cannot remove that conflicting embedded offer. PublicationHold correctly prevents publishing these originals. Await corrected creatives/owner direction and verified intended social account. Do not simulate delivery/PINfailures.

Retailprices are extracted from ownervideoevidence, not new marginapproval. Suppliercurrentprices remain indicative and exactSKUstock, samples and landedcosts unresolved. Source model imagery establishes reference identity, not suppliedquality or fulfilment.

## Scope and handoff

Only catalog/INTEGRATION-REVIEW.md written. Root should resolve/document the three legacyastronaut metadata findings and continue holding publication. Root alone accepts and mutates external state.
