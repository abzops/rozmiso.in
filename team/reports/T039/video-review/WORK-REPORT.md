# Work report - T039 Lane A

Status: SUBMITTED
Author and lane: final_v5_video_review / Lane A
Date/time and environment: 1 November 2026, Windows PowerShell, F:\Dropshipping
Department and worker role: Brand & Creative / video evidence reviewer

## Result

Inspected all five contact sheets (12 sampled images each) and supplied metadata. Identified the depicted product types, visible variants, embedded subtitle claims, prices, branding, COD and CTA. Prepared five factual description drafts and five matching social-caption drafts in RESULTS.json. Exact supplier/manufacturer model cannot be established from the sampled images.

All are 30-second, 1080 × 1920, 24 fps H.264 portrait videos, with AAC streams according to inventory. They consistently end in Rozmiso branding, rozmiso.in, “Cash on Delivery” and “Tap Shop Now”. Prices are ₹999 heat belt, ₹999 scalp massager, ₹899 flat-tyre booster, ₹1,299 astronaut projector and ₹749 blender bottle. These are observed embedded offers, not independently approved live selling terms.

## Artifacts and scope

- F:/Dropshipping/team/reports/T039/video-review/RESULTS.json
- F:/Dropshipping/team/reports/T039/video-review/WORK-REPORT.md
- Five full-resolution proof frames: video-review/1-heating-belt-26s.jpg through video-review/5-usb-juicer-26s.jpg, extracted at 26 seconds from original videos and visually inspected.

Source originals at C:/Users/Abhinand/Downloads/final-v5 remained unchanged. No external actions or shared-file mutations. Work is a local review submission; Codex acceptance pending.

## Evidence and validation

Read team/reports/T039/VIDEO-INVENTORY.json and visually opened all five referenced contact-sheet.jpg files under team/reports/T039/frames. Source hashes copied into RESULTS.json for root reconciliation. This lane did not independently recompute hashes.

Independently extracted one full-resolution 26-second offer/product frame from each original using ffmpeg and viewed all five. Product labels, prices, COD and Shop Now wording match the contact sheets. Juicer close-up shows four exposed blade arms despite earlier subtitle claiming six: flag for exact SKU reconciliation before repeating that specification.

Visual identity findings:

- Lavender digital heat belt: no temperature/battery or clinical efficacy established.
- White four-head scalp massager: four clusters visible; silicone, removal and rotating operation are creative claims requiring supplier confirmation.
- Four-wheel metal tyre cradle: a support trolley for pushing, not an inflator or repair kit. The 3 km setup does not prove a safe operating distance. One early subtitle could imply riding; later text explicitly describes pushing.
- White astronaut projector: detailed galaxy/planet imagery is illustrative and cannot establish actual projection output. Child scenes do not establish certification or safe unsupervised use.
- Pink portable blender bottle: fruit-blending scenes, not pulp extraction. Six blades/USB charging are stated visually; capacity and other specifications unknown.

All sampled brand end cards are consistent. Several lifestyle shots contain small sparkle/diamond marks; provenance was not determined. Original labels should remain. The contact sheets establish sampled composition and legibility, not smooth motion, transition quality, lip sync, sound or complete frame-by-frame correctness.

Audio was **not listened to**. The AAC stream proves only an audio track is present. Audible content, music rights, pronunciation, levels and sync remain unverified.

RTK availability checked; unavailable, ordinary PowerShell used.

## Missing inputs and dependencies

Root must validate exact SKU, prices, actual COD availability and domain/CTA destination before deciding on unchanged publication. The cautious caption drafts do not remove embedded offers or performance representations. No exact model is legible; supplier evidence and physical instructions remain necessary for catalog specifications. Audio and rights require actual listening/source review. This lane has no external publication authority.

## Proposed handoff

Root can integrate observed identity cues and factual draft copy after catalog reconciliation. Keep claimed specifications distinct from verified facts. Preserve original video bytes and required provenance. Check projector scene realism and tyre-support operating language carefully before publication.

## Independent review - completed by a different person/agent

Reviewer: Pending root review.
PASS / CHANGES_REQUIRED / BLOCKED: Pending.
Reasons and evidence: Inspect RESULTS.json against the five source contact sheets and root's catalog/link/commerce evidence.

## Codex acceptance

Pending. Only Codex completes this section and updates the task board.

## Gallery extraction follow-up — 1 November 2026

Root requested six accurate frames per owner video, excluding COD end cards and unsupported effects. Reviewed dense 1-second candidate sheets, extracted and inspected 26 exact 1080×1920 source frames. GALLERY-FRAMES.json records timestamps, paths, retained subtitle claims and quality limits. Four products have six candidates each; the astronaut projector has only one clear product scene plus one partial unboxing image. Six distinct high-quality projector views are unavailable under these exclusions.

New full-resolution massager finding: a green/white supplier box reads SMART SCALP MASSAGER and has Blueide… brand lettering with ambiguous final characters. This corrects earlier small-contact-sheet observation that no other brand was legible. No exact supplier brand/model accepted from this partial evidence.

Extracted files are under video-review/gallery-proof/. Originals unchanged; no upload or video editing. Many frames retain original subtitles/diamond marks, and repeated camera setups are identified. Parent decides catalog use; this is evidence preparation only.

Root then prioritized one hero plus useful distinct secondaries rather than six per product. Saved five 1080×1920 heroes to gallery-final/<key>/hero.jpg, with eight selected secondary frames across four products. GALLERY-FINAL.json records absolute paths, hero timestamps and SHA-256 hashes. Galaxy projector has only the one clear hero; its partial unboxing scene was not retained as a secondary. Heroes exclude COD/end cards and unsupported projection effects. Belt/scalp/projector retain original subtitles; tyre/blender heroes contain no subtitle text. These are exact source extracts copied without further image changes.
