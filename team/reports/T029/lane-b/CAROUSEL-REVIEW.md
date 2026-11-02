# T029 independent carousel staging review

Reviewer: carousel_missing, reviewing root staging (not its author)
Date: 13 October 2026
Overall: CHANGES_REQUIRED
Scope: full 21-product file/caption inventory; visual review of juicer six frames and both exact original references. Other products did not receive full visual acceptance in this review.

## Inventory

18 of 21 products have six existing staged PNGs and six unique file hashes each. Three sets remain incomplete. Total staged frames: 115. Unique hashes establish separate files, not meaningful visual distinction. All 21 caption files contain their manifest's exact product URL, orders-not-open preview boundary and AI disclosure. This is a local string comparison, not a live URL availability check. Instagram caption links remain plain text.

| Product ID | Product | Existing frames | Result |
|---|---|---:|---|
| 10252037324992 | Fabric shaver | 6 | File/count PASS |
| 10252037357760 | Rechargeable cleaning brush | 6 | File/count PASS |
| 10252037390528 | Travel pouch | 6 | File/count PASS |
| 10252037456064 | Soap dispensing brush | 6 | File/count PASS |
| 10253181026496 | Microfiber cloth | 6 | File/count PASS |
| 10253181092032 | Bag locking ties | 6 | File/count PASS |
| 10253181255872 | Cable winder | 6 | File/count PASS |
| 10253181321408 | Window groove brush | 5 | Missing care guidance |
| 10253181419712 | Upholstery brush | 1 | Missing detail, primary use, second context, care and sixth frame |
| 10253181518016 | Hanging organizer | 1 | Missing detail, primary use, second context, care and sixth frame |
| 10253181583552 | Drain catcher | 6 | File/count PASS |
| 10253181681856 | Bottle lid tool | 6 | File/count PASS |
| 10253181845696 | Cable organizer strips | 6 | File/count PASS |
| 10253181944000 | Wiping cloths | 6 | File/count PASS |
| 10253182009536 | Mesh wash bag | 6 | File/count PASS |
| 10257843060928 | Keyboard cover | 6 | File/count PASS |
| 10257843159232 | Two-tier rack | 6 | File/count PASS |
| 10257843224768 | Hair straightening brush | 6 | File/count PASS |
| 10257843257536 | Water bottle | 6 | File/count PASS |
| 10257843355840 | Manual citrus juicer | 6 | File/count PASS; visual CHANGES_REQUIRED |
| 10257843454144 | Canvas storage bag | 6 | File/count PASS |

Sixth-frame CTA remains unresolved: currently the manifest uses Studio view instead of the specified product-details/store CTA. Do not report required CTA slides as generated. Root may revise this fallback only with a clearly recorded scope decision.

## Juicer visual findings

Inspected original reference-1.jpg and reference-2.jpg under T028/reference-review/10257843355840, then every 01-slide.png through 06-slide.png under T029/social/carousels/10257843355840.

Geometry PASS: red bowl/central ridged cone, white slotted strainer, opposing side handle/spout consistently match the red original product. No motors, cables or fabricated attachments appear. Original collage also shows a different all-white product in use; generated assets consistently preserve the red SKU instead. Cover feature text (manual operation, removable strainer, pouring spout) is supported by visible product features and prior selected product brief. Care guidance is short and conservative; no unsafe or exaggerated numerical claims appear.

CHANGES_REQUIRED:

- Slide 03 is an idle assembled juicer next to oranges. It does not depict primary operation, despite being labeled Primary use. Caption should not imply an operational demonstration is shown. A proper use frame would show citrus pressed/rotated on the cone by hand.
- Slides 02 and 06 are very similar assembled studio angles. Their hashes differ, but their informational purpose is repetitive. Slide 06 lacks the required product-details/store CTA. A CTA replacement solves this repetition.
- Slide 05 uses an older black bold sans-serif care graphic. It is legible and factual, but visibly differs from the cover's premium forest-green serif design. It should receive the common design treatment to satisfy the user's premium consistent carousel request.
- Only the cover and care frame currently have detailed graphics/text. The other images are professional-looking product scenes, not explanatory detail posters. Do not label the entire pack as six designed informational posters.

## Crop risk

16 of the 18 six-file packs mix aspect ratios according to the manifest; only shaver and cleaning brush are uniform square. Juicer cover is portrait 4:5 (1122x1402) and the other five frames are square (1254x1254). Forcing cover to square can remove heading/footer; forcing square frames to 4:5 can remove approximately 20% of their width. Actual Instagram composer behavior is not verified here. Preserve full text and critical handles/spouts when choosing crop; do not claim crop acceptance until the composer is reviewed. No image editing was performed.

## Dependencies and acceptance

Missing artwork generation is blocked by the earlier built-in imagegen connection failure. Per root instruction no retry was made. Upholstery/organizer eight planned prompts are preserved in CAROUSEL-MISSING-SLIDES-PROMPTS.json; no generated outputs exist. All publication/deletion remains root's responsibility. No live changes, log writes or shared board writes occurred. Codex acceptance remains pending.
