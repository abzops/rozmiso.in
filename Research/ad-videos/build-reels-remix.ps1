# Rozmiso Reels, "Boss montage" remix (reference: Reel Maker\_refs\De9IAUTh25l-boss-montage\style.md).
# Kept from the reference: a cut every 1.25 s, speed ramps (fast into the cut, slow after it), horizontal whip
# blur on every third cut, warm punchy grade, freeze on the last frame.
# Changed: our own Flow clips and DeoDap photos, the brand-voice voiceovers (vo3), brand hook and price cards.
# Usage: build-reels-remix.ps1 [-Only belt]
param([string]$Only = "")

$ErrorActionPreference = "Stop"
$bin  = "C:\Users\asus\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
$ff   = "$bin\ffmpeg.exe"; $fp = "$bin\ffprobe.exe"
$root = "C:\StacknStock\Research\Rozmiso\Research\ad-videos"
$work = "$root\work-remix"; $out = "$root\final-remix"; $sfx = "$root\work2\sfx"
New-Item -ItemType Directory -Force $work, $out | Out-Null
$serif = "C\:/Windows/Fonts/georgia.ttf"
$sans  = "C\:/StacknStock/Research/Rozmiso/Research/ad-videos/fonts/DMSans.ttf"
$IVORY = "0xF5F0E7"; $FOREST = "0x173E33"; $SAGE = "0xE7ECDF"
$SHOT = 1.25

function Run($argList) {
  & $ff -hide_banner -loglevel error -y @argList
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed: $($argList -join ' ')" }
}
function TextFile($name, $text) {
  $p = "$work\$name.txt"
  [IO.File]::WriteAllText($p, $text, (New-Object Text.UTF8Encoding $false))
  return ($p -replace '\\', '/' -replace ':', '\:')
}

# Sources per product, in story order: @(file, number of 1.25 s shots). Clips are cut into 1.5 s source
# windows starting at "from"; photos become fast push-ins. 23 shots + a 1.25 s freeze = 30 s.
$reels = [ordered]@{
  "1-heating-belt" = @{ vo = "1-belt.mp3"; price = "₹999"; hook = "No more hot water bottle"
    src = @(@("clips\belt-s1-bed.mp4", 4, 0), @("clips\belt-s2-hand.mp4", 4, 0), @("1-heating-belt.mp4", 5, 0), @("clips\belt-s4.mp4", 4, 0), @("photo:belt-5.jpg", 2), @("photo:belt-11.jpg", 4))
    cards = @(@(5.0, "Rechargeable heat belt"), @(10.0, "No water. No leak."), @(15.0, "Gentle heat and vibration"), @(20.0, "Wear it under your kurta")) }
  "2-scalp-massager" = @{ vo = "2-scalp.mp3"; price = "₹999"; hook = "Your ₹999 head massage"
    src = @(@("clips\scalp-s1-office.mp4", 4, 0), @("clips\scalp-s5.mp4", 4, 0), @("2-scalp-massager.mp4", 4, 1.5), @("clips\scalp-s3.mp4", 4, 0), @("clips\scalp-s4.mp4", 4, 0), @("photo:scalp-7.jpg", 3))
    cards = @(@(5.0, "4 soft silicone heads"), @(10.0, "Detachable, easy to clean"), @(15.0, "Scalp, neck and shoulders"), @(20.0, "USB rechargeable")) }
  "3-tyre-booster" = @{ vo = "3-booster.mp3"; price = "₹899"; hook = "Flat tyre, 3 km to go"
    src = @(@("clips\booster-s1-road.mp4", 4, 0), @("clips\booster-s2.mp4", 4, 0), @("3-tyre-booster.mp4", 5, 0), @("clips\booster-s4.mp4", 2, 0), @("clips\booster-s5.mp4", 4, 0), @("photo:booster-5.jpg", 4))
    cards = @(@(5.0, "Flat-tyre booster"), @(10.0, "Galvanized steel frame"), @(15.0, "Adjustable fit"), @(20.0, "Push, don't drag")) }
  "4-galaxy-projector" = @{ vo = "4-projector.mp3"; price = "₹1,299"; hook = "Skip the night lamp"
    src = @(@("clips\projector-s1-boy.mp4", 4, 0), @("clips\projector-s2.mp4", 4, 0), @("clips\projector-s3.mp4", 4, 0), @("4-galaxy-projector.mp4", 5, 0), @("clips\projector-s4.mp4", 4, 0), @("photo:projector-4.jpg", 2))
    cards = @(@(5.0, "Astronaut galaxy projector"), @(10.0, "Stars and nebula overhead"), @(15.0, "Remote control"), @(20.0, "A gift for Christmas")) }
  "5-usb-juicer" = @{ vo = "5-juicer.mp3"; price = "₹749"; hook = "Don't skip breakfast"
    src = @(@("clips\juicer-s1-kitchen.mp4", 4, 0), @("clips\juicer-s2-blend.mp4", 4, 0), @("5-usb-juicer.mp4", 5, 0), @("clips\juicer-s4.mp4", 4, 0), @("clips\juicer-s5.mp4", 4, 0), @("photo:juicer-8.jpg", 2))
    cards = @(@(5.0, "Blend it at your desk"), @(10.0, "6 blades, one button"), @(15.0, "Drink from the bottle"), @(20.0, "Charges over USB")) }
}

foreach ($name in $reels.Keys) {
  if ($Only -and $name -notlike "*$Only*") { continue }
  $r = $reels[$name]; $segs = @(); $n = 0

  foreach ($s in $r.src) {
    for ($k = 0; $k -lt $s[1]; $k++) {
      $seg = "$work\$name-$('{0:D2}' -f $n).mp4"
      $whipOut = ($n % 3 -eq 2); $whipIn = ($n % 3 -eq 0 -and $n -gt 0)
      $blur = @()
      if ($whipIn)  { $blur += "dblur=angle=0:radius=60:enable='lt(t,0.10)'" }
      if ($whipOut) { $blur += "dblur=angle=0:radius=60:enable='gt(t,1.13)'" }
      $blurChain = if ($blur) { "," + ($blur -join ",") } else { "" }
      if ($s[0] -like "photo:*") {
        $src = "$root\photos\$($s[0].Substring(6))"
        $z0 = 1.0 + 0.06 * $k
        $vf = "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.10,fps=30,loop=38:1:0,trim=0:$SHOT,setpts=N/30/TB[bg];" +
              "[b]scale=1000:-2,zoompan=z='$z0+0.004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=38:s=1000x1000:fps=30[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-60:shortest=1,setsar=1$blurChain[v]"
        Run @("-loop", "1", "-t", "$SHOT", "-i", $src, "-f", "lavfi", "-t", "$SHOT", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", $vf, "-map", "[v]", "-map", "1:a", "-t", "$SHOT",
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", "30", "-c:a", "aac", "-b:a", "160k", $seg)
      } else {
        $ss = $s[2] + 1.5 * $k
        # Speed ramp: 0.4 s at 2x, 0.5 s at 0.67x (frame-blended slow-mo), 0.6 s at 2x  ->  1.25 s out.
        $vf = "[0:v]fps=24,scale=1080:1920:flags=lanczos,setsar=1,split=3[a][b][c];" +
              "[a]trim=0:0.4,setpts=(PTS-STARTPTS)/2,fps=30[a1];" +
              "[b]trim=0.4:0.9,setpts=(PTS-STARTPTS)*1.5,minterpolate=fps=30:mi_mode=blend[b1];" +
              "[c]trim=0.9:1.5,setpts=(PTS-STARTPTS)/2,fps=30[c1];" +
              "[a1][b1][c1]concat=n=3:v=1:a=0,trim=0:$SHOT,setpts=PTS-STARTPTS$blurChain[v];" +
              "[0:a]atrim=0:$SHOT,asetpts=PTS-STARTPTS,volume=0.10,aresample=48000[au]"
        Run @("-ss", "$ss", "-t", "1.5", "-i", "$root\$($s[0])", "-filter_complex", $vf, "-map", "[v]", "-map", "[au]", "-t", "$SHOT", "-ac", "2",
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", "30", "-c:a", "aac", "-b:a", "160k", $seg)
      }
      $segs += $seg; $n++
    }
  }

  # Join the 23 shots and hold the last frame (freeze, like the reference ending).
  $list = "$work\$name-list.txt"
  ($segs | ForEach-Object { "file '$($_ -replace '\\','/')'" }) | Set-Content -Encoding ascii $list
  $joined = "$work\$name-joined.mp4"
  Run @("-f", "concat", "-safe", "0", "-i", $list, "-vf", "tpad=stop_mode=clone:stop_duration=1.3", "-af", "apad=pad_dur=1.3",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-c:a", "aac", "-b:a", "160k", $joined)

  # Brand overlays: hook card on frame 0, short feature cards, price card from 24 s.
  $draw = @(); $events = @()
  $hf = TextFile "$name-hook" $r.hook
  $draw += "drawtext=fontfile='$serif':textfile='$hf':fontsize=70:fontcolor=$($FOREST):box=1:boxcolor=$($IVORY)@0.96:boxborderw=30:x=(w-text_w)/2:y=290:enable='lt(t,2.5)'"
  foreach ($c in $r.cards) {
    $a = $c[0]; $b = $a + 3.6; $cf = TextFile "$name-card$a" $c[1]
    $draw += "drawtext=fontfile='$sans':textfile='$cf':fontsize=56:fontcolor=$($FOREST):box=1:boxcolor=$($IVORY)@0.94:boxborderw=24:x=(w-text_w)/2:y=300:alpha='min(1,(t-$a)/0.15)':enable='between(t,$a,$b)'"
  }
  $pf = TextFile "$name-price" $r.price; $cod = TextFile "$name-cod" "Cash on Delivery"; $nx = TextFile "$name-next" "Tap Shop Now"; $sh = TextFile "$name-shop" "Shop on Rozmiso"
  $draw += "drawbox=x=110:y=600:w=860:h=560:color=$($IVORY)@0.97:t=fill:enable='gte(t,24)'"
  $draw += "drawtext=fontfile='$sans':textfile='$sh':fontsize=40:fontcolor=0x59685E:x=(w-text_w)/2:y=650:enable='gte(t,24)'"
  $draw += "drawtext=fontfile='$serif':textfile='$pf':fontsize=150:fontcolor=$($FOREST):x=(w-text_w)/2:y=720:alpha='min(1,(t-24.1)/0.25)':enable='gte(t,24.1)'"
  $draw += "drawbox=x=200:y=930:w=680:h=96:color=$($SAGE):t=fill:enable='gte(t,24.3)'"
  $draw += "drawtext=fontfile='$sans':textfile='$cod':fontsize=50:fontcolor=$($FOREST):x=(w-text_w)/2:y=953:enable='gte(t,24.3)'"
  $draw += "drawtext=fontfile='$sans':textfile='$nx':fontsize=46:fontcolor=$($FOREST):x=(w-text_w)/2:y=1070:alpha='min(1,(t-25)/0.3)':enable='gte(t,25)'"

  # Accents where the reference puts them: air on the whip cuts, one hit on the price.
  for ($i = 3; $i -lt 23; $i += 3) { $events += ,@(($i * $SHOT - 0.15), "air", 0.07) }
  $events += ,@(24.0, "hit", 0.30)
  $in = @(); $fl = @(); $j = 0
  foreach ($e in $events) { $in += @("-i", "$sfx\$($e[1]).wav"); $ms = [int]($e[0] * 1000); $fl += "[$($j):a]volume=$($e[2]),adelay=$ms|$ms[s$j]"; $j++ }
  $sfxWav = "$work\$name-sfx.wav"
  Run (@($in) + @("-filter_complex", (($fl -join ";") + ";" + ((0..($j - 1) | ForEach-Object { "[s$_]" }) -join "") + "amix=inputs=$($j):duration=longest:normalize=0,apad=whole_dur=30[x]"), "-map", "[x]", "-t", "30", "-ar", "48000", $sfxWav))

  $voFile = "$root\vo3\$($r.vo)"
  $vdur = [double](& $fp -v error -show_entries format=duration -of csv=p=0 $voFile)
  $tempo = if ($vdur -gt 29.4) { [math]::Round($vdur / 29.4, 3) } else { 1.0 }
  # Warm, punchy grade from the reference (R > G > B, saturation pushed).
  $look = "colorbalance=rs=0.05:gs=0.01:bs=-0.05:rm=0.03:bm=-0.03,eq=contrast=1.07:saturation=1.22,noise=alls=2:allf=t,format=yuv420p"
  $vchain = "[0:v]$look," + ($draw -join ",") + "[v]"
  $achain = "[1:a]atempo=$tempo,adelay=250|250,volume=1.7[vo];[0:a]volume=0.8[amb];[amb][vo][2:a]amix=inputs=3:duration=longest:normalize=0,atrim=0:30,afade=t=out:st=29.4:d=0.6,alimiter=limit=0.95[a]"
  Run @("-i", $joined, "-i", $voFile, "-i", $sfxWav, "-filter_complex", "$vchain;$achain", "-map", "[v]", "-map", "[a]", "-t", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "7M", "-bufsize", "14M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "$out\$name.mp4")
  "built $name ($n shots)"
}
