# T039 catalog research results

Status: SUBMITTED. Accessed 1 November 2026. Author: Lane B catalog researcher. External activity was read-only.

All five creatives have a high-confidence visual reference match to specific DeoDap SKUs, including repeated source scenes. This establishes visual identity, not sample quality or fulfilment. `RESULTS.json` contains conservative catalog titles/HTML, supplier URLs, selected clean image URLs, excluded claims and duplicate instructions.

| Creative | Exact supplier SKU | Fresh public JSON INR | Owner video INR | Catalog action |
|---|---|---:|---:|---|
| Heating belt | 13483_smart_warm_belt_1pc | 332 | 999 | New record; no match among28 |
| Scalp massager | 13556_smart_scalp_massager_1pc | 377 | 999 | New record; no match among28 |
| Tyre booster | 1683_emergency_wheel_puller | 298 | 899 | New record; no match among28 |
| Astronaut projector | 4530_astronaut_star_projector | 528 | 1299 | Reuse existing draft10249095086272 |
| Pink USB blender | 0133_usb_juicer_6blade | 240, alternate URL269 | 749 | New record; manual citrus juicer is different |

Supplier costs above are indicative public prices, not exact-SKU quotes or landed costs. Search index prices differed from direct JSON; direct downloaded JSON is the current observation. Same-SKU blender URLs also disagree; quote required before margin acceptance. Customer shipping70INR per order is not evidence of the supplier fulfilment cost. No supplier stock quantity was exposed in these JSONs, and a visible Add to Cart is insufficient to establish availability for Rozmiso.

The supplied owner creatives state retail prices, so candidate prices were extracted rather than invented. Root decides how the owner instruction authorizes these prices. Projector legacy draft has1099INR single and1899INR pair, incompatible with video1299INR; explicitly resolve rather than silently import legacy price. Existing draft quantities90/60 are unverified historical values, not stock evidence. Draft media is null, so draft model identity is supported by astronaut title/handle only; do not claim an image comparison of the old draft.

## Exact visual checks

- Belt: lavender rounded rectangle, black upper-center display, outline pattern, grey strap. Supplier isolated image4 and sofa scene0 match video. Different pink alternate illustrations exist on the same listing; do not promise exact supplied colour without confirmation.
- Scalp: white rounded triangular shell, silver perimeter band, grey top button and four grey heads.13556 montage exactly matches video/table scene.22683 red MZ model rejected. Source13556 contradicts itself: textIPX6, graphicIPX7. Catalog omits waterproof/wet-use promises.
- Tyre: silver galvanized cradle, white wheels with pink hubs, end caster; same marble-floor image6. Supplier500kg and4wheel text are not adopted; imagery and text disagree about wheel arrangements. No riding or3km capability claim.
- Astronaut: standing suit, visor, hose, moon base and table/pencil scene match4530.14523 is a seated astronaut with a helmet light and is rejected. Rich cosmic scenes are illustrative, not measured projection fidelity. No unqualified power-source spec included because4530 text says typicallyUSB.
- Blender: pink base/flat lid/strap, clear jar, black ON/OFF panel and outlined horizontal charging port.0133 imagery repeats the woman's cardigan scene.0131 blue model/control label differs and is rejected. Supplier380ml and six blades supported; certification, ice crushing and battery endurance omitted.

## Sources and limits

Every product's exact `supplierUrl`, rawJSON and imageURLs are in RESULTS.json. RawJSON is saved beside this report under the supplier handle, truncated to65characters. JPG montages are observation evidence generated from publicly served supplier images, not proposed product media. Prefer original imageSource URLs for integration. All accessed1November2026.

../PUBLIC-CATALOG.json:21active products, none matches these five. ../ADMIN-CATALOG.json:28total products, seven drafts; astronaut draft is the one existing candidate. Snapshot was supplied by root in this session. Reads prove recorded catalog state at snapshot time only.

Remaining fulfilment, physical sample, accurate supplied colours/accessories, COD, checkout and total cost inputs are unresolved. Keep unverified stock unavailable; do not import supplier MRP, discount badges, reviews, customer counts or historical inventory.
