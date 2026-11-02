# Rozmiso Reel ads report: 31 Oct 2026

## Files to upload

Folder: `C:\StacknStock\Research\Rozmiso\Research\ad-videos\final\`

Every Reel is 30 seconds, 1080×1920, about 12–17 MB, and ready to upload to Instagram or Meta Ads. Each product has **two hook versions**. The video is identical in both; only the first 3 seconds of text differ. Run both and keep the one with the cheaper cost per click.

| # | Product | Price | Hook A file | Hook B file |
|---|---|---|---|---|
| 1 | Heating belt | ₹999 COD | `1-heating-belt-hookA.mp4`: "Hot water bottle ka zamana gaya!" | `1-heating-belt-hookB.mp4`: "Ladkiyon ka naya favourite gadget" |
| 2 | Scalp massager | ₹999 COD | `2-scalp-massager-hookA.mp4`: "10 minute mein salon jaisa head massage?" | `2-scalp-massager-hookB.mp4`: "Papa ne wapas hi nahi diya!" |
| 3 | Tyre booster | ₹899 COD (MRP ₹1,999) | `3-tyre-booster-hookA.mp4`: "Puncture hua? Ye jugaad jaan lo" | `3-tyre-booster-hookB.mp4`: "Har bike wale ke paas ye hona chahiye" |
| 4 | Galaxy projector | ₹1,299 COD (MRP ₹2,999) | `4-galaxy-projector-hookA.mp4`: "Bachche ne kaha space jaana hai..." | `4-galaxy-projector-hookB.mp4`: "Pura kamra galaxy ban gaya!" |
| 5 | USB juicer | ₹749 COD (MRP ₹826) | `5-usb-juicer-hookA.mp4`: "Breakfast skip karte ho?" | `5-usb-juicer-hookB.mp4`: "Office mein fresh smoothie? Ye dekho" |

The older single-version files without "hook" in the name (`1-heating-belt.mp4` and so on) are the first, simpler edit. Use the hookA/hookB files instead.

## How each Reel is built

| Time | What's on screen |
|---|---|
| 0–3 s | Yellow **hook headline** with a bass hit, over the problem shot (leaking hot water bag, flat tyre, tired man, bored kid, skipped breakfast) |
| 3–24 s | A new shot every 3 s with a slow push-in and a whoosh on each cut. Big Hinglish captions in white and yellow, timed to the Hindi voiceover, with a pop on each caption |
| 24–30 s | Riser into a hit, then a **price slam** (big yellow ₹ price, red MRP strike-through where MRP is higher), a "CASH ON DELIVERY" badge and a blinking call to action ("Neeche link pe order karo") |

- **Voiceovers:** natural Hindi/Hinglish from ElevenLabs, with a different voice per product: Aisiri, Supriya, Ballu, Karan and Chandni.
- **Video:** 25 AI clips from Google Flow (Omni 1.1 Flash), each started from the real DeoDap product photo or using it as a reference. Indian people, homes and streets, phone-camera look.
- **Look:** light colour grade, vignette and fine grain so the clips look shot on one phone.
- **Sound effects:** made in code following the reel editing skill's rules. No music, so you can add trending audio inside Instagram.

## Checked
- I looked at frames from every clip. The product's shape and colour match the DeoDap photos in the clips used.
- **Rejected:** Flow's clip named "scalp-s2" actually showed the belt, with a massage-node back side the real product doesn't have, so it's not used. The booster night clip turned into an electric kick-scooter after 3 seconds, so only its first 3 seconds are used.
- Durations and sizes were confirmed. ₹ prices render correctly.

## Before you spend on ads
1. **Watch each Reel once to the end on your phone.** I checked sample frames, not every frame.
2. **Google's AI watermark:** a small ✦ sparkle shows in a corner of the AI shots. Google requires it in your region; leave it.
3. **Claims:** the voiceovers say "kuch hi seconds mein garmi", "10 minute" and "steel body". Confirm these on a real unit from DeoDap. If a product doesn't match, buyers will return it.
4. **Meta policy for the heating belt:** the ad copy must not say "your period pain". The current Reel and captions are written to stay inside that rule.
5. **Projector:** the CTA says "order before 18 Dec". Change it after Christmas.
6. **DeoDap photo rights:** confirm DeoDap lets resellers use their photos in ads.

## Suggested test (from the earlier research)
- One campaign per product, Advantage+ audience, ₹500–700 a day for 3 days, with both hook versions running.
- Pause an ad if cost per click is above ₹25, or if ₹600 is spent with no add-to-cart. Scale a product when ROAS stays above 3.
- Launch order: heating belt and scalp massager now, tyre booster with a small budget, galaxy projector from 1 Dec, juicer from 26 Dec.

## Costs today
- **Google Flow:** about 270 credits used in total, about 720 left (resets 21 Nov).
- **ElevenLabs:** 5 voiceovers, about 1,900 credits.

## To change anything later
Edit the text in `ad-videos\build-reels-v2.ps1` (hooks, captions, prices, shots) and run:
`powershell -ExecutionPolicy Bypass -File build-reels-v2.ps1`
All 10 Reels re-render in about 10 minutes.
