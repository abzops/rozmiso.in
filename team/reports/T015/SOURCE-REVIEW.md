# T015 — Independent source review

**Result: PASS for the reviewed local source change.** This is not live deployment, product-media permission, playable-video or checkout acceptance.

Reviewer: direct_supplier_research (independent of Codex/theme author)
Review date: 6 October 2026
Compared: `operations/product-media-2026-10-06/theme-before` against `theme-prepared` in the same folder.
Writer scope: this report only. No source, account, browser, catalog, board or commerce mutation performed.

## Scope verified

Byte comparison finds exactly six changed/added files:

- `assets/studio.css`
- `locales/en.default.json`
- `sections/studio-hero.liquid`
- `sections/studio-product.liquid`
- `templates/index.json`
- `snippets/studio-product-videos.liquid` (new)

All other theme files are byte-identical, including `studio.js`, header, product cards, collection/search/cart/contact templates, layout, configuration and existing brand/media assets. No new copied supplier or AI asset is introduced by this patch. `settings_data.current.prelaunch_mode` remains `true`.

## Catalog discoverability

PASS. The index enables `catalog_first: true`; the hero renders a short introduction and normal all-products link instead of the large single-product image. The existing four product blocks remain immediately after the intro, before story/FAQ. Ordering places fabric shaver, pouch and soap brush first and the supplier-sold-out cleaning brush last. The reusable hero's previous branch remains available when the setting is false; the new schema checkbox defaults false, while this storefront's index explicitly opts in.

The mobile category strip gains an ordinary Shop all link, alongside collection links only when their objects exist. Its new nowrap rule avoids broken words; the actual 320px/mobile layout still requires root's UI inspection. Description promises only details/care guidance, without inventing demonstrations, stock or supplier approvals. Card objects continue to determine actual titles/prices/availability and links through unchanged `studio-edit` and `studio-card`; the retained fallback image/text cannot be mistaken for an orderable native product when a product object is missing because the fallback remains coming-soon and unlinked.

## Product and commerce contracts

PASS. Removing only the inserted `{% render 'studio-product-videos', item: product %}` from the updated product section yields byte-identical original content. Thus these existing contracts are preserved:

- Selected/default variant and featured-image handling.
- Product images/thumbnails and `data-image`, `data-alt`, `ProductImage`, `data-product`, zoom hook.
- Native product form, variant/quantity inputs, `ProductForm`, `data-add`, unavailable disabled state and actual product/variant prices.
- Availability enquiry, genuine Shopify policy links, descriptions and structured data.
- Existing shaver educational copy and related products.
- JavaScript search, cart server-section refresh and fallback forms/links (unchanged).

The patch does not set inventory, alter payment/checkout configuration, enable ordering or claim a connected supplier. Existing hard-coded prelaunch copy will need a separate coordinated review when commercial ordering is approved; this patch correctly retains today's state.

## Native video branches

PASS against the current Shopify primary documentation, accessed 6 October 2026:

- [video_tag](https://shopify.dev/docs/api/liquid/filters/video_tag): hosted product video rendered with the Shopify filter; controls enabled, autoplay/loop disabled, preload none and 900x poster size.
- [external_video_url](https://shopify.dev/docs/api/liquid/filters/external_video_url): attached external-video media passes through the URL filter with autoplay zero.
- [external_video_tag](https://shopify.dev/docs/api/liquid/filters/external_video_tag): URL feeds the native iframe filter; lazy loading and class attributes are supported. Shopify supplies the iframe title from media alt/product title.

The snippet counts only `video` and `external_video` media; heading/container appear only when at least one is attached. Images and 3D model objects are excluded from its loop. Optional captions escape media alt text. No scraped URL, made-up demo, placeholder player, downloader or external lookup exists. CSS scopes width/background/radius to the new video class; external iframe has 16:9 aspect ratio. Hosted vertical media is not forcibly made landscape.

Important interpretation: attachment to a Shopify product is a technical rendering condition, **not proof of authenticity, permission or performance**. Catalog administrators/reviewers must attach only approved exact-model assets. The snippet's explanatory comment does not establish a media license. No actual current video is added by this source patch.

## Bounded fixture validation

Ran inline Node/LiquidJS render checks against the actual snippet, stripping only the Shopify doc tag. Shopify media filters were replaced with observing stubs, so these checks validate template branching/escaping and filter selection; they do not claim Shopify's actual generated markup or video playback:

| Fixture | Observed result |
|---|---|
| Empty media | No video section, no figures, no video-filter calls |
| Images only | No video section, no figures, no video-filter calls |
| Image + hosted video + external video + model | One video section, exactly two figures; correct hosted and external URL/tag filter paths |
| Caption containing `<Demo>` | Caption escaped to `&lt;Demo&gt;` |

File comparison, PDP insertion-only comparison and prelaunch checks passed in the same run. Root reports six files passed the official validator; this review independently assessed source and fixtures rather than representing that validator as browser evidence.

## Remaining acceptance boundaries

Root should verify actual mobile/desktop first-screen findability, all four links, galleries, search, empty bag and unavailable enquiry behavior after Shopify renders the prepared theme. Existing one-photo catalog remains a media-content gap. Supplier permission, physical sample/product geometry and genuine demo inspection remain T014/supplier gates; actual playback requires an eligible attached video. No new unsupported media should be imported to make the player appear. Public-ordering readiness is a separate task.

## Handoff

Codex can integrate the six local source changes after root's UI checks and existing approved deployment process. Source acceptance does not authorize spending, supplier messages, opening inventory or publishing unreviewed product media.
