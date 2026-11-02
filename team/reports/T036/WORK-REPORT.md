# T036 — Touch gallery navigation

22 October2026. Codex accepted scoped implementation and deployment.

Added horizontal touch/pen swipes on the main product image. Left selects next; right selects previous; first/last wrap. Uses existing thumbnail clicks, so native image source, alt text, variant gallery selection and pressed thumbnail state stay synchronized. Applies to both current live product markup and the unpublished Modern Bento markup.

Vertical scroll and pinch remain browser-owned via touch-action:pan-y pinch-zoom. Short/mostly vertical gestures do not change images; cancel or additional pointers cancel the swipe. Completed swipes suppress accidental compatibility clicks opening zoom; a fresh deliberate tap immediately afterward can still zoom. Mouse and keyboard behavior unchanged. Zero/one-image galleries are untouched.

Independent reviewer wrote15 gesture fixtures, exposed two suppression defects, and confirmed all15 pass after correction. Root reran these15 plus11 existing regressions, allPASS. Node syntax check and official Shopify Theme Check clean. Tests simulate pointer events; they are not physical iPad/Safari certification.

Freshly pulled live159552962752 assets/studio.js before change. Scoped strict CLI push uploaded only that JS file to existing draft159555977408 and current live159552962752. Live file pulled back and exact SHA256 matches authoritative source; INTEGRITY.json records proof. Initial minimal-directory push rejected without uploading; reran from authoritative theme with --only. No full draft publication, layout/style/config or commerce changes.

Browser access is now available. IAB showed live touchAction active and thumbnail selection changing index0to1 without zoom; clicking main image opened zoom, close restored it. Tablet820/phone390 viewport inspected; no phone horizontal overflow (document375px in390px viewport). Actual touch input could not be injected: IAB does not support Input.dispatchTouchEvent; Chrome CDP was unavailable while resolving document response. Physical iPad/Safari swipe remains unverified. Normal live screenshot live-gallery.png retained; live-phone.png has capture scaling artifact and is not accepted visual-layout evidence. Temporary viewport/emulation overrides reset.

Rollback: push only team/reports/T036/live-before/assets/studio.js to live theme if needed. WORK-LOG.md and task board updated. T034 full Modern Bento comparison remains pending; launch-commerce blockers unchanged.
