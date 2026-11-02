# T031 independent corrected soap-product QA

Reviewer: chrome_build. Date:22 October2026.

## Product identity: PASS within visible evidence

Viewed the three owner-reference files `product-reference/soap-use.png`, `soap-side.png`, `soap-studio.png` and corrected output `generated/soap-corrected.png` at full displayed detail.

The corrected output follows the supplied soap-use pose closely: yellow glove over the same rounded pink animal-shaped shell, grey bristle underside on the sink, face/eye/cheek graphics partly exposed, raised ear/paw details, shell seam/ribbed lower edge, and matching rear lobes. The white cap at image left is consistent with the top cap on the upright studio reference after rotating the brush into the supplied use pose. It is not an added lateral cap. I do not see the rejected invented rear plane or a new feature. The warm sink background and lighting change, while the visible physical identity remains supported by the owner references.

This is visual acceptance of visible product identity and pose, not a measurement-level certification or confirmation of hidden geometry. Output bristle rendering/water droplets naturally differ from the source, without an evident functional part change. No product-image edit was performed by this reviewer.

## Landing CSS read-only review: CHANGES_REQUIRED for intermediate-width check

Root's renamed featured anchor `landing-featured` avoids the inherited `#the-edit` style collision. The new width overrides and mobile hero fade are coherent in source. No obvious unrelated commerce-control mutation was found.

One concrete responsive risk remains at761–1100 CSS pixels: `.rl-home-banner` keeps aspect-ratio4.55 and overflow:hidden; its height at761px is approximately154px, while the tablet home-copy stack (padding, heading, paragraph, margins and button) needs roughly185px. The CTA may be clipped. The travel banner similarly removes min-height and uses24.4vw (approximately186px at761px), while the tablet three-line heading and copy/button stack can need roughly265px. It may overlap the following footer. This is a source-calculated risk, not a verified browser defect; root should inspect820px plus the reference941px view and adjust banner height/content sizing if visible. Main desktop1440 and mobile390 endpoint checks alone would not cover this band.

No source changes, live writes or log/board edits were made for this review.

## Root resolution
820px preview confirmed clipping. Added intermediate-width minimum heights260/300px. Fresh measurements home229.1px copy within260px and travel270.6px within300px. Source/remote integrity matched after publication. Root accepts responsive concern as resolved.
