# Rozmiso Reels v5: smooth edit.
#   - Every clip plays at real speed at its native 24 fps (no speed ramps, no frame blending, no freeze),
#     one shot per clip, joined with 0.4 s dissolves.
#   - Hinglish subtitles (the spoken lines), DM Sans, timed to the voiceover.
#   - Ending: product blended into ivory (name, price, COD) -> official Rozmiso logo animation + rozmiso.in.
# Usage: build-reels-v5.ps1 [-Only belt]
param([string]$Only = "")

$ErrorActionPreference = "Stop"
$bin  = "C:\Users\asus\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
$ff   = "$bin\ffmpeg.exe"; $fp = "$bin\ffprobe.exe"
$root = "C:\StacknStock\Research\Rozmiso\Research\ad-videos"
$logo = "C:\StacknStock\Research\Rozmiso\Research\logos\rozmiso-primary.png"
$work = "$root\work-v5"; $out = "$root\final-v5"; $sfx = "$root\work2\sfx"; $prodDir = "$root\work-final"
New-Item -ItemType Directory -Force $work, $out | Out-Null
$serif = "C\:/Windows/Fonts/georgia.ttf"
$sans  = "C\:/StacknStock/Research/Rozmiso/Research/ad-videos/fonts/DMSans.ttf"
$IVORY = "0xF5F0E7"; $FOREST = "0x173E33"; $SAGE = "0xE7ECDF"; $MUTED = "0x59685E"
$FPS = 24; $XF = 0.4
$MONT = 24.2; $ENDD = 3.8; $LOGOD = 2.8   # montage, end card, logo; two 0.4 s dissolves -> 30.0 s

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

# shots: @(clip, start, length). Lengths sum to 24.2 + 0.4 x (shots - 1).
$reels = [ordered]@{
  "1-heating-belt" = @{ cut = 27.79; vo = "1-belt.mp3"; price = "₹999"; name = "Rechargeable heat belt"; hook = "No more hot water bottle"
    shots = @(@("clips\belt-s1-bed.mp4", 0, 6.0), @("clips\belt-s2-hand.mp4", 0, 6.0), @("1-heating-belt.mp4", 0.3, 7.4), @("clips\belt-s4.mp4", 0, 6.0))
    lines = @("Hot water bottle bharna band karo.", "Ye ₹999 ka rechargeable heat belt use karo.", "Isme paani nahi hai, toh leak bhi nahi.", "USB se charge karo, kamar pe lapeto.", "Button dabao, garmi shuru.", "Saath mein halki vibration bhi.", "Kapdon ke neeche aaram se pehen sakte ho.", "Office, college, ya ghar ka kaam, chalta rahe.", "Rozmiso pe ₹999, Cash on Delivery.", "Shop Now dabao.") }
  "2-scalp-massager" = @{ cut = 27.90; vo = "2-scalp.mp3"; price = "₹999"; name = "Electric scalp massager"; hook = "Your ₹999 head massage"
    shots = @(@("clips\scalp-s1-office.mp4", 0.5, 5.0), @("clips\scalp-s5.mp4", 0.5, 5.0), @("2-scalp-massager.mp4", 1.8, 5.0), @("clips\scalp-s3.mp4", 0.3, 5.4), @("clips\scalp-s4.mp4", 0.3, 5.4))
    lines = @("Aapka ₹999 ka head massage.", "4 silicone heads ke saath.", "Haath mein pakdo, button dabao.", "Chaaron heads dheere dheere ghoomte hain.", "Soft silicone, scalp pe aaram se chalta hai.", "Heads nikal jaate hain, saaf karna easy.", "Sir ke baad gardan aur kandhe pe bhi.", "USB se charge, koi cord nahi.", "TV dekhte hue bhi use kar lo.", "Rozmiso pe ₹999, Cash on Delivery.", "Shop Now dabao.") }
  "3-tyre-booster" = @{ cut = 27.65; vo = "3-booster.mp3"; price = "₹899"; name = "Flat-tyre booster"; hook = "Flat tyre, 3 km to go"
    shots = @(@("clips\booster-s1-road.mp4", 0.3, 5.4), @("clips\booster-s2.mp4", 0.3, 5.4), @("3-tyre-booster.mp4", 0.5, 6.0), @("clips\booster-s4.mp4", 0, 3.0), @("clips\booster-s5.mp4", 0, 6.0))
    lines = @("Flat tyre, mechanic 3 km door?", "Bike phir bhi chalegi.", "Ye hai ₹899 ka flat tyre booster.", "Galvanized steel frame, chhote wheels.", "Flat tyre ke neeche fit karo.", "Size adjust ho jaata hai.", "Ab bike ko dhakka do, ghaseeto mat.", "Rim zameen se upar rehta hai.", "Bike ke saath rakh lo, kaam aayega.", "Rozmiso pe ₹899, Cash on Delivery.", "Shop Now dabao. Flat tyre ho, bike chalti rahe.") }
  "4-galaxy-projector" = @{ cut = 28.63; vo = "4-projector.mp3"; price = "₹1,299"; name = "Astronaut galaxy projector"; hook = "Skip the night lamp"
    shots = @(@("clips\projector-s1-boy.mp4", 0.5, 4.6), @("clips\projector-s2.mp4", 0.5, 5.0), @("clips\projector-s3.mp4", 0.3, 5.4), @("4-galaxy-projector.mp4", 1.0, 5.4), @("clips\projector-s4.mp4", 0.3, 5.4))
    lines = @("Night lamp mat lo.", "Ye ₹1,299 ka astronaut galaxy dikhata hai.", "Bedside table pe rakho, button dabao.", "Ceiling pe stars aur nebula aa jaate hain.", "Light dheere dheere ghoomti rehti hai.", "Remote se colours badal sakte ho.", "Bachchon ka bedtime thoda alag lagta hai.", "Christmas ya birthday gift ke liye bhi achha hai.", "Rozmiso pe ₹1,299, Cash on Delivery.", "Shop Now dabao. Night lamp nahi, ceiling pe galaxy.") }
  "5-usb-juicer" = @{ cut = 27.06; vo = "5-juicer.mp3"; price = "₹749"; name = "Portable USB juicer"; hook = "Don't skip breakfast"
    shots = @(@("clips\juicer-s1-kitchen.mp4", 0.6, 4.8), @("clips\juicer-s2-blend.mp4", 0.5, 5.0), @("5-usb-juicer.mp4", 1.0, 5.2), @("clips\juicer-s4.mp4", 0.3, 5.4), @("clips\juicer-s5.mp4", 0.3, 5.4))
    lines = @("Breakfast skip mat karo.", "Desk pe blend karo, ₹749 mein.", "Ye portable USB juicer hai.", "Fruit daalo, thoda doodh, dhakkan band.", "Button dabao, 6 blades ghoomne lagte hain.", "Smoothie ready, glass ki zaroorat nahi.", "Seedha isi bottle se piyo.", "Laptop ya power bank se charge karo.", "Office bag ya gym bag mein rakh lo.", "Rozmiso pe ₹749, Cash on Delivery.", "Shop Now dabao.") }
}

# ---- Logo card with rozmiso.in (24 fps, shared) ----
$logoCard = "$work\logo-card.mp4"
if (-not (Test-Path $logoCard)) {
  $tag = TextFile "tagline" "Thoughtful finds for a brighter everyday."
  $dom = TextFile "domain" "rozmiso.in"
  $lx = 150; $ly = 730; $markW = 189; $wordW = 591
  $vf = "[1:v]format=rgba,split[l1][l2];[l1]crop=440:480:0:0,scale=$($markW):-1[mk];" +
        "[l2]crop=1376:480:440:0,scale=$($wordW):-1[wd];" +
        "[mk]fade=t=in:st=0:d=0.4:alpha=1[mks];" +
        "[0:v][mks]overlay=x=$($lx):y=$($ly):shortest=1[b1];" +
        "[b1][wd]overlay=x=$($lx+$markW):y=$($ly):shortest=1," +
        "drawbox=x='$($lx+$markW)+$($wordW)*min(1,max(0,(t-0.35)/0.75))':y=$($ly):w=$($wordW+20):h=206:color=$($IVORY):t=fill," +
        "drawtext=fontfile='$sans':textfile='$tag':fontsize=38:fontcolor=$($MUTED):x=(w-text_w)/2:y=$($ly+245):alpha='min(1,max(0,(t-1.1)/0.5))'," +
        "drawtext=fontfile='$sans':textfile='$dom':fontsize=54:fontcolor=$($FOREST):borderw=1:bordercolor=$($FOREST):x=(w-text_w)/2:y=$($ly+330):alpha='min(1,max(0,(t-1.4)/0.5))',format=yuv420p[v]"
  Run @("-f", "lavfi", "-i", "color=c=$($IVORY):s=1080x1920:r=$($FPS):d=$LOGOD", "-loop", "1", "-framerate", "$FPS", "-t", "$LOGOD", "-i", $logo, "-filter_complex", $vf, "-map", "[v]", "-t", "$LOGOD",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "$FPS", "-fps_mode", "cfr", "-pix_fmt", "yuv420p", $logoCard)
}

$tagVox = "$root\vo3\tag-george-spoken-tight.wav"
$jingle = "$work\jingle.wav"
if (-not (Test-Path $jingle)) {
  # Rozmiso sonic logo (original): rising E5-G5-C6 on "Roz-mi-so", leading tone B5 on "dot", resolve to C6 on "in" with a G6/C7 shimmer, soft C-major pad.
  $notes = @(@(0.052, 659.25, 0.6), @(0.414, 783.99, 0.6), @(0.746, 1046.5, 0.7), @(1.171, 987.77, 0.5), @(1.45, 1046.5, 1.6), @(1.45, 1567.98, 1.2), @(1.678, 2093, 0.9))
  $jin = @(); $jf = @(); $q = 0
  foreach ($nt in $notes) {
    $jin += @("-f", "lavfi", "-i", "aevalsrc=exprs='0.55*sin(2*PI*$($nt[1])*t)*exp(-3.2*t)+0.18*sin(4*PI*$($nt[1])*t)*exp(-5*t)+0.06*sin(6*PI*$($nt[1])*t)*exp(-7*t)':s=48000:d=$($nt[2])")
    $ms = [int]($nt[0] * 1000); $jf += "[$($q):a]afade=t=in:d=0.005,adelay=$ms[n$q]"; $q++
  }
  $jin += @("-f", "lavfi", "-i", "aevalsrc=exprs='0.10*(sin(2*PI*523.25*t)+sin(2*PI*659.25*t)+sin(2*PI*783.99*t)+0.7*sin(2*PI*261.63*t))*min(1,t/0.25)*exp(-1.1*t)':s=48000:d=1.6")
  $jf += "[$($q):a]adelay=1399[n$q]"; $q++
  $mix = ($jf -join ";") + ";" + ((0..($q - 1) | ForEach-Object { "[n$_]" }) -join "") + "amix=inputs=$($q):duration=longest:normalize=0,aformat=channel_layouts=stereo,aecho=0.6:0.4:120:0.18,alimiter=limit=0.9[j]"
  Run (@($jin) + @("-filter_complex", $mix, "-map", "[j]", "-t", "3.4", "-ar", "48000", $jingle))
}

foreach ($name in $reels.Keys) {
  if ($Only -and $name -notlike "*$Only*") { continue }
  $r = $reels[$name]

  # ---- 1) Montage: real-speed shots, 0.4 s dissolves ----
  $in = @(); $fc = @(); $i = 0
  foreach ($s in $r.shots) {
    $in += @("-ss", "$($s[1])", "-t", "$($s[2])", "-i", "$root\$($s[0])")
    $fc += "[$($i):v]fps=$FPS,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p,trim=0:$($s[2]),setpts=PTS-STARTPTS[v$i]"
    $fc += "[$($i):a]aresample=48000,volume=0.10,atrim=0:$($s[2]),asetpts=PTS-STARTPTS[a$i]"
    $i++
  }
  $vlast = "v0"; $alast = "a0"; $off = 0.0
  for ($k = 1; $k -lt $i; $k++) {
    $off = [math]::Round($off + $r.shots[$k - 1][2] - $XF, 3)
    $fc += "[$vlast][v$k]xfade=transition=fade:duration=$($XF):offset=$off[vx$k]"
    $fc += "[$alast][a$k]acrossfade=d=$($XF)[ax$k]"
    $vlast = "vx$k"; $alast = "ax$k"
  }
  $fc += "[$vlast]colorbalance=rs=0.02:bs=-0.02,eq=contrast=1.03:saturation=1.06,trim=0:$MONT,setpts=PTS-STARTPTS[vm]"
  $fc += "[$alast]apad=whole_dur=$MONT,atrim=0:$MONT[am]"
  $montFile = "$work\$name-montage.mp4"
  Run (@($in) + @("-filter_complex", ($fc -join ";"), "-map", "[vm]", "-map", "[am]", "-t", "$MONT", "-r", "$FPS", "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "aac", "-b:a", "160k", $montFile))

  # ---- 2) Product end card (static, no jitter): blended product from the previous build + text ----
  $prod = "$prodDir\$name-prod.png"
  $nf = TextFile "$name-name" $r.name; $pf = TextFile "$name-price" $r.price; $cod = TextFile "$name-cod" "Cash on Delivery"; $cta = TextFile "$name-cta" "Tap Shop Now"
  $endCard = "$work\$name-end.mp4"
  $vf = "[1:v]pad=1080:1920:130:300:color=white,format=gbrp[p];[0:v]format=gbrp[bg];[bg][p]blend=all_mode=multiply,format=yuv420p," +
        "drawtext=fontfile='$serif':textfile='$nf':fontsize=56:fontcolor=$($FOREST):x=(w-text_w)/2:y=1110:alpha='min(1,max(0,(t-0.25)/0.4))'," +
        "drawtext=fontfile='$serif':textfile='$pf':fontsize=112:fontcolor=$($FOREST):x=(w-text_w)/2:y=1185:alpha='min(1,max(0,(t-0.45)/0.4))'," +
        "drawtext=fontfile='$sans':textfile='$cod':fontsize=42:fontcolor=$($FOREST):box=1:boxcolor=$($SAGE):boxborderw=18:x=(w-text_w)/2:y=1335:alpha='min(1,max(0,(t-0.7)/0.4))'," +
        "drawtext=fontfile='$sans':textfile='$cta':fontsize=38:fontcolor=$($MUTED):x=(w-text_w)/2:y=1405:alpha='min(1,max(0,(t-1.0)/0.4))'[v]"
  Run @("-f", "lavfi", "-i", "color=c=$($IVORY):s=1080x1920:r=$($FPS):d=$ENDD", "-loop", "1", "-framerate", "$FPS", "-t", "$ENDD", "-i", $prod, "-filter_complex", $vf, "-map", "[v]", "-t", "$ENDD",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "$FPS", "-fps_mode", "cfr", "-pix_fmt", "yuv420p", $endCard)

  # ---- 3) Hook card + Hinglish subtitles, timed across the voiceover by word count ----
  $voFile = "$root\vo3\$($r.vo)"
  $vdur = $r.cut
  $tempo = if ($vdur -gt 26.8) { [math]::Round($vdur / 26.8, 3) } else { 1.0 }
  $span = $vdur / $tempo; $delay = 0.25
  $draw = @("drawbox=x=0:y=1185:w=1080:h=250:color=black@0.16:t=fill:enable='lt(t,23.8)'")
  $hf = TextFile "$name-hook" $r.hook
  $draw += "drawtext=fontfile='$serif':textfile='$hf':fontsize=62:fontcolor=$($FOREST):box=1:boxcolor=$($IVORY)@0.93:boxborderw=26:x=(w-text_w)/2:y=270:alpha='if(lt(t,2.2),1,max(0,(2.6-t)/0.4))':enable='lt(t,2.6)'"
  $wc = $r.lines | ForEach-Object { ($_ -split '\s+').Count }; $tot = ($wc | Measure-Object -Sum).Sum
  $t = $delay
  for ($j = 0; $j -lt $r.lines.Count; $j++) {
    $d = $span * $wc[$j] / $tot; $a = [math]::Round($t, 2); $b = [math]::Round([math]::Min($t + $d - 0.05, 23.75), 2)
    if ($a -lt 22.9) {
      $lf = TextFile "$name-l$j" (Wrap $r.lines[$j] 26)
      $draw += "drawtext=fontfile='$sans':textfile='$lf':text_align=C:fontsize=60:fontcolor=white:borderw=1:bordercolor=white:line_spacing=8:shadowx=0:shadowy=3:shadowcolor=black@0.7:x=(w-text_w)/2:y=1235:enable='between(t,$a,$b)'"
    }
    $t += $d
  }

  # ---- 4) Assemble with dissolves; voiceover, room tone, soft accents ----
  $sfxWav = "$work\$name-sfx.wav"
  $events = @(,@(23.85, "air", 0.07))
  $si = @(); $sf = @(); $q = 0
  foreach ($e in $events) { $si += @("-i", "$sfx\$($e[1]).wav"); $ms = [int]($e[0] * 1000); $sf += "[$($q):a]volume=$($e[2]),adelay=$ms|$ms[s$q]"; $q++ }
  Run (@($si) + @("-filter_complex", (($sf -join ";") + ";" + ((0..($q - 1) | ForEach-Object { "[s$_]" }) -join "") + "amix=inputs=$($q):duration=longest:normalize=0,apad=whole_dur=30[x]"), "-map", "[x]", "-t", "30", "-ar", "48000", $sfxWav))

  $o1 = [math]::Round($MONT - $XF, 2); $o2 = [math]::Round($MONT + $ENDD - 2 * $XF, 2)
  $vchain = "[0:v]" + ($draw -join ",") + "[m];[m][1:v]xfade=transition=fade:duration=$($XF):offset=$o1[e1];[e1][2:v]xfade=transition=fade:duration=$($XF):offset=$o2,format=yuv420p[v]"
  $dms = [int]($delay * 1000)
  $achain = "[0:a]apad=whole_dur=30[amb];[3:a]atrim=0:$($r.cut),afade=t=out:st=$([math]::Round($r.cut-0.15,2)):d=0.15,atempo=$tempo,adelay=$dms|$dms,volume=1.7[vo];[5:a]adelay=27350|27350,volume=1.8[tg];[6:a]adelay=27350|27350,volume=0.55[jg];[amb][vo][4:a][tg][jg]amix=inputs=5:duration=longest:normalize=0,atrim=0:30,afade=t=out:st=29.75:d=0.25,alimiter=limit=0.95[a]"
  Run @("-i", $montFile, "-i", $endCard, "-i", $logoCard, "-i", $voFile, "-i", $sfxWav, "-i", $tagVox, "-i", $jingle, "-filter_complex", "$vchain;$achain", "-map", "[v]", "-map", "[a]", "-t", "30",
        "-r", "$FPS", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "8M", "-bufsize", "16M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "$out\$name.mp4")
  "built $name"
}
