# Work report — T009: Rozmiso brand and mobile design audit

Status: SUBMITTED  
Author: Codex brand review worker; bounded Creative specialist  
Date and environment: 6 October 2026, Windows, F:\Dropshipping  
Reviewer: Codex / independent reviewer; acceptance pending

## Result

Rozmiso has a usable visual foundation: a legible R monogram, forest/cream palette, real supplier product images and working source declarations for favicon fallbacks. The next improvement should make the mobile page more product-led and turn the existing identity into a complete, reusable vector kit. It does not require a different name or an invented premium reputation.

This is a source audit plus inspection of previously saved screenshots. I did not inspect a live browser, edit the theme, generate logos, publish, contact suppliers or change business settings. The impression that the page feels generic is a design inference from its composition and wording, not a measured customer finding. This report is the only file written.

## Evidence inspected

- Authoritative source: `rozmiso-studio-theme/`; the historical store folder was not used.
- Current guide: `outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/BRAND-GUIDE.md`.
- Existing evidence: `BRAND-REFRESH-VALIDATION.md`, `brand-home-mobile.png`, `brand-catalog-desktop.png` and `rozmiso-brand-512.png` in that output folder. The validation document reports a previous 360px visual check and public favicon asset check; those are prior observations, not a new live test performed by this worker.
- Asset inventory: the theme's `assets/rozmiso-mark.svg` and the entries of `Rozmiso-Brand-Kit.zip` were inspected.
- Rules: `TEAM_ROSTER_AND_RULES.md`, `team/TASK-BOARD.json`, Creative and brand designer cards, Director card and work-report template were read. T009's bounded brief came from Codex. RTK availability was checked; it is unavailable, so ordinary PowerShell was used.

## What exists and what is missing

| Item | Existing evidence | Remaining need |
|---|---|---|
| Compact mark | `assets/rozmiso-mark.svg`: cream R on rounded forest tile | Preserve this master; inspect its counter and leg at actual 16/32px sizes. |
| Full website logo | Header and footer render the mark with HTML `shop.name` in Manrope; story renders the same mark | No standalone horizontal vector wordmark/lockup file was found. Produce reusable exported logos with controlled spacing. |
| Reversed identity | Story CSS changes the inline mark's forest rectangle to transparent | No standalone reversed full-logo file was found. Export cream mark + wordmark for dark surfaces. |
| Small-size icons | Existing output PNGs at 16, 32, 180 and 512px; SVG master | This is already covered. Re-export consistently if the master is deliberately changed. |
| Favicon integration | `layout/theme.liquid:5–6`: theme color, optional custom image, 32px embedded PNG fallback, SVG favicon and 180px embedded touch icon. `config/settings_schema.json:27–28`: custom favicon setting | A new live browser check is needed for the owner's reported visibility issue. Do not report that favicon source is absent. Check the storefront tab rather than Shopify's theme editor. |
| UI icons | Search, bag, menu and some arrows are inline 24×24 SVGs; some arrows and close controls remain text glyphs | A documented icon set/sprite or shared snippet, consistent optical sizing and close/chevron variants. |
| Brand documentation | Existing guide has voice, colors, fonts and basic rules | Add clear space, minimum logo use, permitted backgrounds, no-descriptor mobile logo, asset naming and examples. |
| Share artwork | Open Graph uses `page_image` when present in `layout/theme.liquid` | No dedicated brand share-image fallback was found. Prepare a 1200×630 brand card as a separate optional asset. It must not imply product results or reputation. |

Shopify recommends a 16×16 or 32×32 favicon, and its documentation explains that the theme editor does not show the storefront favicon. This supports the inspection method, not a claim that the owner's browser currently displays the icon. [Shopify favicon guidance](https://help.shopify.com/en/manual/online-store/images/add-favicon) (accessed 6 October 2026).

## Prioritized weaknesses and fixes

| Priority | Source-backed issue | Proposed change and impact | Effort / review evidence |
|---|---|---|---|
| 1 | The archived mobile screenshot places a large three-line slogan, paragraph, two actions and category note before the featured image. `sections/studio-hero.liquid:2–4` orders copy before art; `assets/studio.css:37,40` still compresses actions and type to make the row fit. | Lead with one short, specific everyday-use headline, a shorter supporting sentence and the real product image much earlier. Use one clearly dominant collection action; category navigation can follow as a separate compact row. Preserve the truthful prelaunch notice. This reduces the amount a visitor must read before recognizing what is offered. | Medium. Compare 360×800 and 390×844 first-screen mockups. Show the product and primary action without requiring multiple screens of copy. Do not turn a unavailable product into an orderable one. |
| 2 | `assets/studio.css:37` sets the mobile brand descriptor to **7px** and the hero note to 10px; `:40` reduces the secondary CTA to 11px. The archived screenshot shows a dense header plus search row and very small supporting identity text. | Use the monogram + wordmark without a tiny descriptor in the mobile header. Keep the descriptor for larger brand uses. Use a consistent mobile text scale: approximately 15–16px body, 14px controls, 12px optional metadata and 32–38px hero heading, subject to visual review. Keep search, menu and bag obvious and comfortably operable. | Small/medium. Inspect actual size, 200% text scaling, 320px reflow and long text. These proposed font values are design choices, not WCAG's prescribed font sizes. |
| 3 | The guide's core line is followed by supporting slogans; `templates/index.json` uses “Good finds. Great little upgrades.” and “A little useful. A lot to love.”; `sections/studio-story.liquid:3` defaults to “A little more ease. A little more you.” Sparkle motifs appear twice in `studio-hero.liquid:2`. | Keep **Little upgrades. Everyday possibilities.** as the one main brand line. Replace other abstract headings with concrete navigation or use: “Home, kitchen and travel essentials”, “Explore the collection” or a product-specific fabric-care heading. Limit the sparkle motif to one optional brand detail; it should not compete with products and actions. | Small. CEO reviews a single page of before/after headings and one mobile screen. The objective is clearer, more specific content rather than a claim that every slogan is wrong. |
| 4 | The supplied asset kit contains the monogram and PNG exports but no standalone wordmark variants. The same mark path is copied in header, footer and story. HTML typography depends on a Google Fonts `@import` at `assets/studio.css:1`. | Finish the vector kit described below and use one canonical mark/logo component. Maintain the present spelling and selected R. Create a controlled wordmark export with deliberate kerning; do not use AI raster text as a logo master. Test font fallback/slow loading so the header remains stable. | Medium. Review a logo sheet at real header size, small icon size and reversed on forest. Asset inventory must distinguish editable master, web export and screenshot. |
| 5 | `brand-catalog-desktop.png` shows different supplier composition styles: close-up cleaning scene, a multi-panel brush image, open pouch and fabric-shaver scene. `studio-hero.liquid:3` and category cards use `object-fit:cover`; product cards use contain. This can crop instructional composites and make imagery feel inconsistent. | Define one primary-image standard per card: clearly visible exact product, consistent crop and calm background; keep instructional composites as later gallery images. Use real licensed supplier images until matching samples and original photography exist. Do not crop away material information or reconstruct the product with generated visuals. | Medium, dependent on image rights/source quality. Review four cards together and full product galleries; check that color, dimensions, parts and accessories still match the actual supplied item. |

The archive is evidence of that saved design, not proof of current layout on every phone. In particular, no new 320px, zoom, landscape, touch-target or device test was performed in this audit.

## Proposed consistent brand kit

Preserve the existing R as the primary compact mark. The wordmark should be **Rozmiso**, using the selected Manrope direction with deliberate spacing. A more professional result comes from consistent use and a complete asset set; changing the brand on every surface would reduce consistency.

| Proposed asset | Construction | Intended use |
|---|---|---|
| `rozmiso-logo-primary.svg` | R tile + forest Rozmiso wordmark, transparent canvas, no tiny tagline | Website header, documents and light backgrounds |
| `rozmiso-logo-wordmark.svg` | Forest wordmark only | Narrow layouts where a separate mark already appears; secondary identity |
| `rozmiso-logo-stacked.svg` | Existing R tile over the wordmark | Square compositions; optional if an actual use exists |
| `rozmiso-logo-reversed.svg` | Cream R + cream wordmark, transparent canvas | Forest backgrounds and dark creative |
| `rozmiso-logo-mono-forest.svg` / `mono-cream.svg` | One-color mark and full lockup variants | Single-color reproduction; avoid gradients/shadows |
| Existing mark/favicons | Current SVG and 16/32/180/512 PNG family | Browser, touch icon and compact identity |
| `rozmiso-icons.svg` + contact sheet | One 24×24 outline system, selected 1.5–2px stroke, controlled round joins/caps | Search, bag, menu, close, chevron, directional arrows, enquiry; avoid decorative icons presented as certifications |
| `rozmiso-brand-share-1200x630.png` | Brand name, main line and calm forest/cream layout | Optional social-share fallback; original brand artwork rather than product evidence |
| `BRAND-GUIDE.md` extension | Existing palette plus spacing, sizing, background rules and examples | Single reference for future workers |

Proposed production rules to review: clear space of at least half the mark's height; no descriptor below comfortable readable size; no stretching; no gradients inside logos; no effects needed to make the mark visible. SVG logos should have correct viewBoxes and accessible usage guidance. Web logo links should announce Rozmiso once; decorative SVGs within them stay hidden from assistive technology. Logo masters are vector source, with transparent PNG exports only when needed. These are proposals, not assets already delivered or approved.

Keep forest `#26342e`, cream `#fbfaf6`, sage `#e8ece1`, clay `#b75132`, muted ink `#65706a` and pale sage `#c3ccc5`. Use clay sparingly for active/focus states, not as an extra background for every card. Keep one card radius and one control radius rather than accumulating new rounded treatments.

Use a 44px touch-target design standard for primary controls, while testing actual width, spacing and hit area. WCAG 2.2 AA's target-size criterion uses a 24px baseline with listed exceptions; a 44px design standard is intentionally more generous, not a claim that AA mandates every control be 44px. [W3C target-size guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) (accessed 6 October 2026). Text should remain usable at 200% scaling, and normal vertical content should reflow at 320 CSS pixels without two-dimensional scrolling. [W3C resize-text guidance](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html), [W3C reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) (accessed 6 October 2026). These sources establish evaluation criteria; they do not certify this storefront.

## Mobile composition proposed for review

1. Truthful collection-preview announcement; compact logo/bag/menu row; a clear search field without the microscopic descriptor.
2. Short category/use headline, one sentence, real featured-product visual and one dominant collection action. Product price and actual unavailable status remain legible; labels should not cover the product.
3. Compact Home care / Kitchen / Travel category navigation. Avoid repeating three full image cards before showing a very small four-product assortment unless the mockup proves it helps browsing.
4. Four consistently composed product cards. At 320px, consider a single-column/list option or larger image-led cards if long product names become cramped; retain two columns only when legibility is demonstrated.
5. A short specific brand paragraph or restrained forest story panel, then useful availability/support answers. Remove repetitive philosophical statements.
6. Compact footer with the full logo, shop/contact links and only real finalized business/policy information. A floating help control must not cover product labels, form actions or the mobile keyboard area; move support into normal flow if it does.

Product-page composition should use the same typography, icons and surfaces. Put title, price, actual availability and enquiry action in a coherent block near the gallery; keep long care/FAQ text below it. Do not add a sticky Buy button while ordering is unavailable.

## Imagery and AI boundaries

Create vector brand artwork directly. AI can be considered for non-product decorative backgrounds only when it does not suggest a product characteristic or result. Never replace exact products with generated lookalikes, add missing accessories, improve apparent material quality, fabricate before/after cleaning results or present generated sample demonstrations as real tests. Supplier image permission and physical sample evidence remain unresolved by this design audit. Original photographed/video demonstrations require the actual inspected item.

## What the CEO can review visually

Codex can prepare these concrete review boards without a public deployment:

- **Identity sheet:** primary, wordmark-only, reversed and compact mark at actual proposed sizes; 16/32px favicons alongside larger marks; icon sheet and color/type samples.
- **Mobile concept:** homepage first screen and full flow at 360×800 and 390×844, plus one 320px stress view. Show actual product imagery, availability and actions; include menu/search open states.
- **Commerce consistency sheet:** the same four cards together, one product page, enquiry screen and footer. Side-by-side current archived evidence and proposed local preview makes the difference inspectable.

CEO review should answer: Can I identify Rozmiso? Can I tell what is sold immediately? Is one next action obvious? Are products and prices easy to read? Are the same identity and icon rules used throughout? Does any image or promise imply evidence we do not have? These are design decisions; payment, stock, supplier and policy approval remain separate.

Existing visual reference:

![Previously saved mobile homepage; not a fresh live observation](F:/Dropshipping/outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6/brand-home-mobile.png)

## Missing inputs and dependencies

- No fresh live/device observation in this worker's scope; Codex or the assigned Store worker must verify the current storefront and favicon visibility.
- Product image rights, written supplier terms and physical sample demonstrations are not established by theme source or a visual guide.
- Brand direction can be refined locally and reviewed without identity documents or business spending. No business owner facts were invented.

## Proposed handoff

Codex should review the five priorities and assign a bounded local implementation task with the asset sheet and mobile concept as first deliverables. Consolidate repeated SVG/icon source and CSS overrides during that task, then verify current products, enquiry, search/cart behavior and mobile states independently. Local design acceptance, live deployment and opening orders must be recorded separately.

## Independent review

Reviewer: Pending  
PASS / CHANGES_REQUIRED / BLOCKED: Pending  
Evidence: Pending

## Codex acceptance

Pending. Only Codex accepts the task and changes the shared board.
