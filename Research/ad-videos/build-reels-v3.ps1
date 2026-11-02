# Rozmiso Reels v3: brand "Everyday Edit" treatment (ivory #F5F0E7, forest #173E33, sage #E7ECDF,
# Georgia headlines, DM Sans body). Reuses the 10-shot cuts from v2 (work2\*-joined.mp4) and the
# brand-voice voiceovers in vo3\. Script text: REELS-BRAND-SCRIPTS.md. Usage: build-reels-v3.ps1 [-Only belt]
param([string]$Only = "")

$ErrorActionPreference = "Stop"
$bin  = "C:\Users\asus\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
$ff   = "$bin\ffmpeg.exe"; $fp = "$bin\ffprobe.exe"
$root = "C:\StacknStock\Research\Rozmiso\Research\ad-videos"
$work = "$root\work3"; $out = "$root\final-brand"; $sfx = "$root\work2\sfx"
New-Item -ItemType Directory -Force $work, $out | Out-Null
$serif = "C\:/Windows/Fonts/georgia.ttf"
$sans  = "C\:/StacknStock/Research/Rozmiso/Research/ad-videos/fonts/DMSans.ttf"
$IVORY = "0xF5F0E7"; $FOREST = "0x173E33"; $SAGE = "0xE7ECDF"

function Run($argList) {
  & $ff -hide_banner -loglevel error -y @argList
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed: $($argList -join ' ')" }
}
function TextFile($name, $text) {
  $p = "$work\$name.txt"
  [IO.File]::WriteAllText($p, $text, (New-Object Text.UTF8Encoding $false))
  return ($p -replace '\\', '/' -replace ':', '\:')
}
function Wrap($s, $max) {
  if ($s.Length -le $max) { return $s }
  $mid = [int]($s.Length / 2)
  for ($d = 0; $d -lt $mid; $d++) {
    if ($s[$mid + $d] -eq ' ') { return $s.Substring(0, $mid + $d) + "`n" + $s.Substring($mid + $d + 1) }
    if ($s[$mid - $d] -eq ' ') { return $s.Substring(0, $mid - $d) + "`n" + $s.Substring($mid - $d + 1) }
  }
  return $s
}

$reels = [ordered]@{
  "1-heating-belt" = @{ vo = "1-belt.mp3"; price = "₹999"
    hook  = "No more hot water bottle"
    cards = @(@(2.6, "Rechargeable heat belt"), @(5.6, "No water. No leak."), @(8.8, "Charge, wrap, switch on"), @(12.0, "Gentle heat and vibration"), @(15.6, "Wear it under your kurta"))
    lines = @("Hot water bottle bharna band karo.", "Ye ₹999 ka rechargeable heat belt use karo.", "Isme paani nahi hai, toh leak bhi nahi.", "USB se charge karo, kamar pe lapeto.", "Button dabao, garmi shuru.", "Saath mein halki vibration bhi.", "Kapdon ke neeche aaram se pehen sakte ho.", "Office, college, ya ghar ka kaam, chalta rahe.", "Rozmiso pe ₹999, Cash on Delivery.", "Shop Now dabao. Hot water bottle ko chhutti do.") }
  "2-scalp-massager" = @{ vo = "2-scalp.mp3"; price = "₹999"
    hook  = "Your ₹999 head massage"
    cards = @(@(2.6, "4 soft silicone heads"), @(6.0, "One button"), @(8.8, "Detachable, easy to clean"), @(14.4, "Scalp, neck and shoulders"), @(17.6, "USB rechargeable"))
    lines = @("Aapka ₹999 ka head massage.", "4 silicone heads ke saath.", "Haath mein pakdo, button dabao.", "Chaaron heads dheere dheere ghoomte hain.", "Soft silicone, scalp pe aaram se chalta hai.", "Heads nikal jaate hain, saaf karna easy.", "Sir ke baad gardan aur kandhe pe bhi.", "USB se charge, koi cord nahi.", "TV dekhte hue bhi use kar lo.", "Rozmiso pe ₹999, Cash on Delivery.", "Shop Now dabao. Ghar pe head massage, ek button se.") }
  "3-tyre-booster" = @{ vo = "3-booster.mp3"; price = "₹899"
    hook  = "Flat tyre, 3 km to go"
    cards = @(@(4.0, "Flat-tyre booster"), @(6.8, "Galvanized steel frame"), @(8.8, "Slide it under the tyre"), @(11.2, "Adjustable fit"), @(13.2, "Push, don't drag"))
    lines = @("Flat tyre, mechanic 3 km door?", "Bike phir bhi chalegi.", "Ye hai ₹899 ka flat tyre booster.", "Galvanized steel frame, chhote wheels.", "Flat tyre ke neeche fit karo.", "Size adjust ho jaata hai.", "Ab bike ko dhakka do, ghaseeto mat.", "Rim zameen se upar rehta hai.", "Bike ke saath rakh lo, kaam aayega.", "Rozmiso pe ₹899, Cash on Delivery.", "Shop Now dabao. Flat tyre ho, bike chalti rahe.") }
  "4-galaxy-projector" = @{ vo = "4-projector.mp3"; price = "₹1,299"
    hook  = "Skip the night lamp"
    cards = @(@(2.6, "Astronaut galaxy projector"), @(6.8, "Stars and nebula overhead"), @(12.4, "Remote control"), @(17.6, "A gift for Christmas"))
    lines = @("Night lamp mat lo.", "Ye ₹1,299 ka astronaut galaxy dikhata hai.", "Bedside table pe rakho, button dabao.", "Ceiling pe stars aur nebula aa jaate hain.", "Light dheere dheere ghoomti rehti hai.", "Remote se colours badal sakte ho.", "Bachchon ka bedtime thoda alag lagta hai.", "Christmas ya birthday gift ke liye bhi achha hai.", "Rozmiso pe ₹1,299, Cash on Delivery.", "Shop Now dabao. Night lamp nahi, ceiling pe galaxy.") }
  "5-usb-juicer" = @{ vo = "5-juicer.mp3"; price = "₹749"
    hook  = "Don't skip breakfast"
    cards = @(@(2.6, "Blend it at your desk"), @(6.0, "Fruit, milk, lid on"), @(8.4, "6 blades, one button"), @(11.2, "Drink from the bottle"), @(15.6, "Charges over USB"))
    lines = @("Breakfast skip mat karo.", "Desk pe blend karo, ₹749 mein.", "Ye portable USB juicer hai.", "Fruit daalo, thoda doodh, dhakkan band.", "Button dabao, 6 blades ghoomne lagte hain.", "Smoothie ready, glass ki zaroorat nahi.", "Seedha isi bottle se piyo.", "Laptop ya power bank se charge karo.", "Office bag ya gym bag mein rakh lo.", "Rozmiso pe ₹749, Cash on Delivery.", "Shop Now dabao. Kal se breakfast desk pe.") }
}

foreach ($name in $reels.Keys) {
  if ($Only -and $name -notlike "*$Only*") { continue }
  $r = $reels[$name]; $joined = "$root\work2\$name-joined.mp4"; $voFile = "$root\vo3\$($r.vo)"
  $vdur = [double](& $fp -v error -show_entries format=duration -of csv=p=0 $voFile)
  $delay = 0.25; $tempo = if ($vdur -gt 29.4) { [math]::Round($vdur / 29.4, 3) } else { 1.0 }
  $span = $vdur / $tempo
  $draw = @(); $events = @()

  # Hook card, frame 0: ivory card, forest Georgia.
  $hf = TextFile "$name-hook" $r.hook
  $draw += "drawtext=fontfile='$serif':textfile='$hf':fontsize=68:fontcolor=$($FOREST):box=1:boxcolor=$($IVORY)@0.96:boxborderw=30:x=(w-text_w)/2:y=290:enable='lt(t,2.5)'"

  # Feature cards: DM Sans on ivory, same spot, each until the next card (before 21 s).
  for ($i = 0; $i -lt $r.cards.Count; $i++) {
    $a = $r.cards[$i][0]; $b = if ($i + 1 -lt $r.cards.Count) { $r.cards[$i + 1][0] - 0.05 } else { [math]::Min($a + 3.2, 21) }
    $cf = TextFile "$name-card$i" $r.cards[$i][1]
    $draw += "drawtext=fontfile='$sans':textfile='$cf':fontsize=54:fontcolor=$($FOREST):box=1:boxcolor=$($IVORY)@0.94:boxborderw=24:x=(w-text_w)/2:y=300:alpha='min(1,(t-$a)/0.15)':enable='between(t,$a,$b)'"
    $events += ,@($a, "pop", 0.025)
  }

  # Spoken-line captions, timed across the voiceover by word count. Hidden once the price card is up.
  $wc = $r.lines | ForEach-Object { ($_ -split '\s+').Count }; $tot = ($wc | Measure-Object -Sum).Sum
  $t = $delay
  for ($i = 0; $i -lt $r.lines.Count; $i++) {
    $d = $span * $wc[$i] / $tot; $a = [math]::Round($t, 2); $b = [math]::Round([math]::Min($t + $d - 0.05, 23.9), 2)
    if ($a -lt 23.9) {
      $lf = TextFile "$name-line$i" (Wrap $r.lines[$i] 26)
      $draw += "drawtext=fontfile='$sans':textfile='$lf':text_align=C:fontsize=60:fontcolor=white:line_spacing=8:shadowx=0:shadowy=3:shadowcolor=black@0.65:borderw=2:bordercolor=black@0.35:x=(w-text_w)/2:y=1240:enable='between(t,$a,$b)'"
    }
    $t += $d
  }

  # Price card, 24 s on: ivory panel, Georgia price, sage COD strip, DM Sans next step.
  $pf = TextFile "$name-price" $r.price; $cod = TextFile "$name-cod" "Cash on Delivery"; $nx = TextFile "$name-next" "Tap Shop Now"; $sh = TextFile "$name-shop" "Shop on Rozmiso"
  $draw += "drawbox=x=110:y=600:w=860:h=560:color=$($IVORY)@0.97:t=fill:enable='gte(t,24)'"
  $draw += "drawtext=fontfile='$sans':textfile='$sh':fontsize=40:fontcolor=0x59685E:x=(w-text_w)/2:y=650:enable='gte(t,24)'"
  $draw += "drawtext=fontfile='$serif':textfile='$pf':fontsize=150:fontcolor=$($FOREST):x=(w-text_w)/2:y=720:alpha='min(1,(t-24.1)/0.25)':enable='gte(t,24.1)'"
  $draw += "drawbox=x=200:y=930:w=680:h=96:color=$($SAGE):t=fill:enable='gte(t,24.3)'"
  $draw += "drawtext=fontfile='$sans':textfile='$cod':fontsize=50:fontcolor=$($FOREST):x=(w-text_w)/2:y=953:enable='gte(t,24.3)'"
  $draw += "drawtext=fontfile='$sans':textfile='$nx':fontsize=46:fontcolor=$($FOREST):x=(w-text_w)/2:y=1070:alpha='min(1,(t-25)/0.3)':enable='gte(t,25)'"

  # Quiet SFX: soft air on cuts, light pops on cards, one gentle hit on the price.
  for ($c = 1; $c -lt 10; $c++) { $events += ,@(($c * 3 - 0.18), "air", 0.06) }
  $events += ,@(24.0, "hit", 0.30)
  $in = @(); $fl = @(); $j = 0
  foreach ($e in $events) { $in += @("-i", "$sfx\$($e[1]).wav"); $ms = [int]($e[0] * 1000); $fl += "[$($j):a]volume=$($e[2]),adelay=$ms|$ms[s$j]"; $j++ }
  $sfxWav = "$work\$name-sfx.wav"
  Run (@($in) + @("-filter_complex", (($fl -join ";") + ";" + ((0..($j - 1) | ForEach-Object { "[s$_]" }) -join "") + "amix=inputs=$($j):duration=longest:normalize=0,apad=whole_dur=30[x]"), "-map", "[x]", "-t", "30", "-ar", "48000", $sfxWav))

  $look = "eq=contrast=1.02:saturation=1.03,colorbalance=rm=0.02:bm=-0.02,noise=alls=2:allf=t,format=yuv420p"
  $vchain = "[0:v]$look," + ($draw -join ",") + "[v]"
  $dms = [int]($delay * 1000)
  $achain = "[1:a]atempo=$tempo,adelay=$dms|$dms,volume=1.7[vo];[0:a]volume=0.7[amb];[amb][vo][2:a]amix=inputs=3:duration=first:normalize=0,afade=t=out:st=29.4:d=0.6,alimiter=limit=0.95[a]"
  Run @("-i", $joined, "-i", $voFile, "-i", $sfxWav, "-filter_complex", "$vchain;$achain", "-map", "[v]", "-map", "[a]", "-t", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "7M", "-bufsize", "14M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "$out\$name.mp4")
  "built $name (vo $([math]::Round($vdur,1))s, tempo $tempo)"
}
