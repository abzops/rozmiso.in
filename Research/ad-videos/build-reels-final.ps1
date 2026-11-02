# Rozmiso Reels, final: "Boss montage" pacing (speed ramps, whip cuts) + Hindi subtitles + clean brand ending.
#   0.0-24.2  montage of real video shots only (18 shots), subtle warm grade, hook card, Hindi subtitles
#  24.2-27.2  product end card: product photo blended into ivory (multiply + feathered edges), name, price, COD
#  27.6-30.0  Rozmiso logo motion: official logo (store theme SVG), R mark scales in, wordmark wipes in, brand line
# Usage: build-reels-final.ps1 [-Only belt]
param([string]$Only = "")

$ErrorActionPreference = "Stop"
$bin  = "C:\Users\asus\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
$ff   = "$bin\ffmpeg.exe"; $fp = "$bin\ffprobe.exe"
$root = "C:\StacknStock\Research\Rozmiso\Research\ad-videos"
$logo = "C:\StacknStock\Research\Rozmiso\Research\logos\rozmiso-primary.png"
$work = "$root\work-final"; $out = "$root\final-v4"; $sfx = "$root\work2\sfx"
New-Item -ItemType Directory -Force $work, $out | Out-Null
$serif = "C\:/Windows/Fonts/georgia.ttf"
$sans  = "C\:/StacknStock/Research/Rozmiso/Research/ad-videos/fonts/DMSans.ttf"
$hindi = "C\:/Windows/Fonts/Nirmala.ttc"
$IVORY = "0xF5F0E7"; $FOREST = "0x173E33"; $SAGE = "0xE7ECDF"; $MUTED = "0x59685E"
$N = 18; $L = 1.3334; $W = 1.6          # shots, output length per shot, source window per shot
$MONT = 24.2; $ENDD = 3.8; $LOGOD = 2.8  # section lengths; two 0.4 s cross-fades -> 30.0 s

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

# src: @(file, shots, from, maxSeconds). Hindi lines are exactly what the voiceover says.
$reels = [ordered]@{
  "1-heating-belt" = @{ vo = "1-belt.mp3"; price = "₹999"; name = "Rechargeable heat belt"; photo = "belt-5.jpg"; hook = "No more hot water bottle"
    src = @(@("clips\belt-s1-bed.mp4", 4, 0, 6), @("clips\belt-s2-hand.mp4", 4, 0, 6), @("1-heating-belt.mp4", 6, 0, 8), @("clips\belt-s4.mp4", 4, 0, 6))
    hi  = @("हॉट वॉटर बॉटल भरना बंद करो।", "ये ₹999 का रिचार्जेबल हीट बेल्ट यूज़ करो।", "इसमें पानी नहीं है, तो लीक भी नहीं।", "USB से चार्ज करो, कमर पे लपेटो।", "बटन दबाओ, गर्मी शुरू।", "साथ में हल्की वाइब्रेशन भी।", "कपड़ों के नीचे आराम से पहन सकते हो।", "ऑफिस, कॉलेज, या घर का काम... चलता रहे।", "Rozmiso पे ₹999, कैश ऑन डिलीवरी।", "Shop Now दबाओ। हॉट वॉटर बॉटल को छुट्टी दो।") }
  "2-scalp-massager" = @{ vo = "2-scalp.mp3"; price = "₹999"; name = "Electric scalp massager"; photo = "scalp-5.jpg"; hook = "Your ₹999 head massage"
    src = @(@("clips\scalp-s1-office.mp4", 4, 0, 6), @("clips\scalp-s5.mp4", 4, 0, 6), @("2-scalp-massager.mp4", 3, 1.6, 8), @("clips\scalp-s3.mp4", 4, 0, 6), @("clips\scalp-s4.mp4", 3, 0, 6))
    hi  = @("आपका ₹999 का हेड मसाज।", "चार सिलिकॉन हेड्स के साथ।", "हाथ में पकड़ो, बटन दबाओ।", "चारों हेड्स धीरे-धीरे घूमते हैं।", "सॉफ्ट सिलिकॉन, स्कैल्प पे आराम से चलता है।", "हेड्स निकल जाते हैं, साफ़ करना आसान।", "सिर के बाद गर्दन और कंधे पे भी।", "USB से चार्ज, कोई कॉर्ड नहीं।", "TV देखते हुए भी यूज़ कर लो।", "Rozmiso पे ₹999, कैश ऑन डिलीवरी।", "Shop Now दबाओ। घर पे हेड मसाज, एक बटन से।") }
  "3-tyre-booster" = @{ vo = "3-booster.mp3"; price = "₹899"; name = "Flat-tyre booster"; photo = "booster-5.jpg"; hook = "Flat tyre, 3 km to go"
    src = @(@("clips\booster-s1-road.mp4", 4, 0, 6), @("clips\booster-s2.mp4", 4, 0, 6), @("3-tyre-booster.mp4", 5, 0, 8), @("clips\booster-s4.mp4", 1, 0, 3), @("clips\booster-s5.mp4", 4, 0, 6))
    hi  = @("फ्लैट टायर, मैकेनिक तीन किलोमीटर दूर?", "बाइक फिर भी चलेगी।", "ये है ₹899 का फ्लैट टायर बूस्टर।", "गैल्वनाइज़्ड स्टील फ्रेम, छोटे व्हील्स।", "फ्लैट टायर के नीचे फिट करो।", "साइज़ एडजस्ट हो जाता है।", "अब बाइक को धक्का दो, घसीटो मत।", "रिम ज़मीन से ऊपर रहता है।", "बाइक के साथ रख लो, काम आएगा।", "Rozmiso पे ₹899, कैश ऑन डिलीवरी।", "Shop Now दबाओ। फ्लैट टायर हो, बाइक चलती रहे।") }
  "4-galaxy-projector" = @{ vo = "4-projector.mp3"; price = "₹1,299"; name = "Astronaut galaxy projector"; photo = "projector-4.jpg"; hook = "Skip the night lamp"
    src = @(@("clips\projector-s1-boy.mp4", 3, 0, 6), @("clips\projector-s2.mp4", 4, 0, 6), @("clips\projector-s3.mp4", 4, 0, 6), @("4-galaxy-projector.mp4", 4, 0, 8), @("clips\projector-s4.mp4", 3, 0, 6))
    hi  = @("नाइट लैंप मत लो।", "ये ₹1,299 का एस्ट्रोनॉट, गैलेक्सी दिखाता है।", "बेडसाइड टेबल पे रखो, बटन दबाओ।", "सीलिंग पे स्टार्स और नेबुला आ जाते हैं।", "लाइट धीरे-धीरे घूमती रहती है।", "रिमोट से कलर्स बदल सकते हो।", "बच्चों का बेडटाइम थोड़ा अलग लगता है।", "क्रिसमस या बर्थडे गिफ्ट के लिए भी अच्छा है।", "Rozmiso पे ₹1,299, कैश ऑन डिलीवरी।", "Shop Now दबाओ। नाइट लैंप नहीं, सीलिंग पे गैलेक्सी।") }
  "5-usb-juicer" = @{ vo = "5-juicer.mp3"; price = "₹749"; name = "Portable USB juicer"; photo = "juicer-4.jpg"; hook = "Don't skip breakfast"
    src = @(@("clips\juicer-s1-kitchen.mp4", 3, 0, 6), @("clips\juicer-s2-blend.mp4", 4, 0, 6), @("5-usb-juicer.mp4", 4, 0, 8), @("clips\juicer-s4.mp4", 4, 0, 6), @("clips\juicer-s5.mp4", 3, 0, 6))
    hi  = @("ब्रेकफास्ट स्किप मत करो।", "डेस्क पे ब्लेंड करो, ₹749 में।", "ये पोर्टेबल USB जूसर है।", "फ्रूट डालो, थोड़ा दूध, ढक्कन बंद।", "बटन दबाओ, छह ब्लेड्स घूमने लगते हैं।", "स्मूदी रेडी, ग्लास की ज़रूरत नहीं।", "सीधा इसी बोतल से पियो।", "लैपटॉप या पावर बैंक से चार्ज करो।", "ऑफिस बैग या जिम बैग में रख लो।", "Rozmiso पे ₹749, कैश ऑन डिलीवरी।", "Shop Now दबाओ। कल से ब्रेकफास्ट डेस्क पे।") }
}

# ---- Logo motion card (same for every product) ----
$logoCard = "$work\logo-card.mp4"
if (-not (Test-Path $logoCard)) {
  $tag = TextFile "tagline" "Thoughtful finds for a brighter everyday."
  # Logo PNG is 1816x480; the R mark sits in x 0-440, the wordmark in x 440-1816. Scaled to 780 px wide.
  $lx = 150; $ly = 760; $markW = 189; $wordW = 591
  $vf = "[1:v]format=rgba,split[l1][l2];[l1]crop=440:480:0:0,scale=$($markW):-1[mk];" +
        "[l2]crop=1376:480:440:0,scale=$($wordW):-1[wd];" +
        "[mk]scale=w='$($markW)*(0.82+0.18*min(1,t/0.5))':h=-1:eval=frame,fade=t=in:st=0:d=0.35:alpha=1[mks];" +
        "[0:v][mks]overlay=x='$lx+$($markW)/2-w/2':y='$ly+103-h/2':shortest=1[b1];" +
        "[b1][wd]overlay=x=$($lx+$markW):y=$($ly):shortest=1," +
        "drawbox=x='$($lx+$markW)+$($wordW)*min(1,max(0,(t-0.45)/0.7))':y=$($ly):w=$($wordW+20):h=206:color=$($IVORY):t=fill," +
        "drawtext=fontfile='$sans':textfile='$tag':fontsize=38:fontcolor=$($MUTED):x=(w-text_w)/2:y=$($ly+250):alpha='min(1,max(0,(t-1.3)/0.5))',tpad=stop_mode=clone:stop_duration=0.3,fps=30,trim=0:$LOGOD,format=yuv420p[v]"
  Run @("-f", "lavfi", "-i", "color=c=$($IVORY):s=1080x1920:r=30:d=$LOGOD", "-loop", "1", "-t", "$LOGOD", "-i", $logo, "-filter_complex", $vf, "-map", "[v]", "-t", "$LOGOD",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "30", "-pix_fmt", "yuv420p", $logoCard)
}

foreach ($name in $reels.Keys) {
  if ($Only -and $name -notlike "*$Only*") { continue }
  $r = $reels[$name]; $segs = @(); $n = 0

  # ---- 1) Montage: 18 ramped shots of real video ----
  foreach ($s in $r.src) {
    $avail = [math]::Min($s[3], [double](& $fp -v error -show_entries format=duration -of csv=p=0 "$root\$($s[0])")) - $s[2]
    $step = if ($s[1] -gt 1) { ($avail - $W) / ($s[1] - 1) } else { 0 }
    for ($k = 0; $k -lt $s[1]; $k++) {
      $ss = [math]::Round($s[2] + $k * $step, 3)
      $seg = "$work\$name-$('{0:D2}' -f $n).mp4"
      $blur = @()
      if ($n % 3 -eq 0 -and $n -gt 0) { $blur += "dblur=angle=0:radius=50:enable='lt(t,0.09)'" }
      if ($n % 3 -eq 2) { $blur += "dblur=angle=0:radius=50:enable='gt(t,$([math]::Round($L - 0.1, 3)))'" }
      $bc = if ($blur) { "," + ($blur -join ",") } else { "" }
      $a = [math]::Round(0.27 * $W, 3); $b = [math]::Round(0.6 * $W, 3)
      $vf = "[0:v]fps=24,scale=1080:1920:flags=lanczos,setsar=1,split=3[x][y][z];" +
            "[x]trim=0:$a,setpts=(PTS-STARTPTS)/2,fps=30[x1];" +
            "[y]trim=$($a):$b,setpts=(PTS-STARTPTS)*1.5,minterpolate=fps=30:mi_mode=blend[y1];" +
            "[z]trim=$($b):$W,setpts=(PTS-STARTPTS)/2,fps=30[z1];" +
            "[x1][y1][z1]concat=n=3:v=1:a=0,fps=30,trim=0:$L,setpts=PTS-STARTPTS$bc[v];" +
            "[0:a]atrim=0:$L,asetpts=PTS-STARTPTS,volume=0.08,aresample=48000[au]"
      Run @("-ss", "$ss", "-t", "$W", "-i", "$root\$($s[0])", "-filter_complex", $vf, "-map", "[v]", "-map", "[au]", "-t", "$L", "-ac", "2",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", "30", "-fps_mode", "cfr", "-c:a", "aac", "-b:a", "160k", $seg)
      $segs += $seg; $n++
    }
  }
  if ($n -ne $N) { throw "$name has $n shots, expected $N" }
  $list = "$work\$name-list.txt"
  ($segs | ForEach-Object { "file '$($_ -replace '\\','/')'" }) | Set-Content -Encoding ascii $list
  $montFile = "$work\$name-montage.mp4"
  # Subtle warm grade (toned down from the reference so it stays clean), tiny tail hold for the cross-fade.
  Run @("-f", "concat", "-safe", "0", "-i", $list,
        "-vf", "fps=30,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,eq=contrast=1.04:saturation=1.10,tpad=stop_mode=clone:stop_duration=0.3,trim=0:$MONT,setpts=PTS-STARTPTS,format=yuv420p",
        "-af", "apad=whole_dur=$MONT,atrim=0:$MONT", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "aac", "-b:a", "160k", $montFile)

  # ---- 2) Product end card: photo melted into ivory ----
  $prod = "$work\$name-prod.png"
  $lv = if ($name -like "*projector*") { ",colorlevels=rimax=0.91:gimax=0.91:bimax=0.91" } else { "" }; $pc = if ($name -like "*projector*") { "crop=720:720:530:375," } else { "" }; $fe = if ($name -like "*projector*") { 120 } else { 70 }
  Run @("-i", "$root\photos\$($r.photo)", "-vf",
        "$($pc)scale=820:820$lv,format=rgb24,geq=r='r(X,Y)*M+255*(1-M)':g='g(X,Y)*M+255*(1-M)':b='b(X,Y)*M+255*(1-M)'".Replace("M", "clip(min(min(X,W-X),min(Y,H-Y))/$fe,0,1)"),
        "-frames:v", "1", $prod)
  $nf = TextFile "$name-name" $r.name; $pf = TextFile "$name-price" $r.price; $cod = TextFile "$name-cod" "Cash on Delivery"; $cta = TextFile "$name-cta" "Tap Shop Now"
  $endCard = "$work\$name-end.mp4"
  $vf = "[1:v]scale=w='820*(1+0.035*t/$ENDD)':h=-1:eval=frame,pad=1080:1920:(ow-iw)/2:'300-(ih-820)/2':color=white:eval=frame,format=gbrp[p];" +
        "[0:v]format=gbrp[bg];[bg][p]blend=all_mode=multiply,format=yuv420p," +
        "drawtext=fontfile='$serif':textfile='$nf':fontsize=56:fontcolor=$($FOREST):x=(w-text_w)/2:y=1110:alpha='min(1,max(0,(t-0.25)/0.4))'," +
        "drawtext=fontfile='$serif':textfile='$pf':fontsize=112:fontcolor=$($FOREST):x=(w-text_w)/2:y=1185:alpha='min(1,max(0,(t-0.45)/0.4))'," +
        "drawtext=fontfile='$sans':textfile='$cod':fontsize=42:fontcolor=$($FOREST):box=1:boxcolor=$($SAGE):boxborderw=18:x=(w-text_w)/2:y=1335:alpha='min(1,max(0,(t-0.7)/0.4))'," +
        "drawtext=fontfile='$sans':textfile='$cta':fontsize=38:fontcolor=$($MUTED):x=(w-text_w)/2:y=1405:alpha='min(1,max(0,(t-1.0)/0.4))'[v]"
  Run @("-f", "lavfi", "-i", "color=c=$($IVORY):s=1080x1920:r=30:d=$ENDD", "-loop", "1", "-t", "$ENDD", "-i", $prod, "-filter_complex", $vf, "-map", "[v]", "-t", "$ENDD",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "30", "-pix_fmt", "yuv420p", $endCard)

  # ---- 3) Hook card + Hindi subtitles over the montage, timed to the voiceover by word count ----
  $voFile = "$root\vo3\$($r.vo)"
  $vdur = [double](& $fp -v error -show_entries format=duration -of csv=p=0 $voFile)
  $tempo = if ($vdur -gt 29.4) { [math]::Round($vdur / 29.4, 3) } else { 1.0 }
  $span = $vdur / $tempo; $delay = 0.25
  $draw = @()
  $hf = TextFile "$name-hook" $r.hook
  $draw += "drawtext=fontfile='$serif':textfile='$hf':fontsize=62:fontcolor=$($FOREST):box=1:boxcolor=$($IVORY)@0.93:boxborderw=26:x=(w-text_w)/2:y=270:alpha='if(lt(t,2.2),1,max(0,(2.6-t)/0.4))':enable='lt(t,2.6)'"
  $wc = $r.hi | ForEach-Object { ($_ -split '\s+').Count }; $tot = ($wc | Measure-Object -Sum).Sum
  $t = $delay
  for ($i = 0; $i -lt $r.hi.Count; $i++) {
    $d = $span * $wc[$i] / $tot; $a = [math]::Round($t, 2); $b = [math]::Round([math]::Min($t + $d - 0.05, 23.75), 2)
    if ($a -lt 22.9) {
      $lf = TextFile "$name-hi$i" (Wrap $r.hi[$i] 24)
      $draw += "drawtext=fontfile='$hindi':textfile='$lf':text_shaping=1:text_align=C:fontsize=60:fontcolor=white:borderw=2:bordercolor=white:line_spacing=10:shadowx=0:shadowy=3:shadowcolor=black@0.7:x=(w-text_w)/2:y=1230:enable='between(t,$a,$b)'"
    }
    $t += $d
  }
  # soft dark band behind the subtitles so they read on bright shots
  $band = "drawbox=x=0:y=1180:w=1080:h=260:color=black@0.18:t=fill:enable='lt(t,23.8)'"

  # ---- 4) Assemble: montage -> end card -> logo card, with 0.4 s cross-fades; then text and audio ----
  $sfxWav = "$work\$name-sfx.wav"
  $events = @(); for ($i = 3; $i -lt $N; $i += 3) { $events += ,@(($i * $L - 0.12), "air", 0.06) }
  $events += ,@(23.9, "air", 0.08); $events += ,@(27.3, "air", 0.07); $events += ,@(27.75, "hit", 0.18)
  $in = @(); $fl = @(); $j = 0
  foreach ($e in $events) { $in += @("-i", "$sfx\$($e[1]).wav"); $ms = [int]($e[0] * 1000); $fl += "[$($j):a]volume=$($e[2]),adelay=$ms|$ms[s$j]"; $j++ }
  Run (@($in) + @("-filter_complex", (($fl -join ";") + ";" + ((0..($j - 1) | ForEach-Object { "[s$_]" }) -join "") + "amix=inputs=$($j):duration=longest:normalize=0,apad=whole_dur=30[x]"), "-map", "[x]", "-t", "30", "-ar", "48000", $sfxWav))

  $o1 = [math]::Round($MONT - 0.4, 2); $o2 = [math]::Round($MONT + $ENDD - 0.8, 2)
  $vchain = "[0:v]$band," + ($draw -join ",") + "[m];[m][1:v]xfade=transition=fade:duration=0.4:offset=$o1[e1];[e1][2:v]xfade=transition=fade:duration=0.4:offset=$o2,fps=30,format=yuv420p[v]"
  $dms = [int]($delay * 1000)
  $achain = "[0:a]apad=whole_dur=30[amb];[3:a]atempo=$tempo,adelay=$dms|$dms,volume=1.7[vo];[amb][vo][4:a]amix=inputs=3:duration=longest:normalize=0,atrim=0:30,afade=t=out:st=29.4:d=0.6,alimiter=limit=0.95[a]"
  Run @("-i", $montFile, "-i", $endCard, "-i", $logoCard, "-i", $voFile, "-i", $sfxWav, "-filter_complex", "$vchain;$achain", "-map", "[v]", "-map", "[a]", "-t", "30",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "8M", "-bufsize", "16M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "$out\$name.mp4")
  "built $name"
}
