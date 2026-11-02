# Builds the 5 Rozmiso 30-second Reels from Flow clips, DeoDap photos and ElevenLabs voiceovers.
# Usage: powershell -ExecutionPolicy Bypass -File build-reels.ps1 [-Only belt]
param([string]$Only = "")

$ErrorActionPreference = "Stop"
$ff   = "C:\Users\asus\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
$root = "C:\StacknStock\Research\Rozmiso\Research\ad-videos"
$img  = "C:\StacknStock\Research\Rozmiso\Research\ad-videos\photos"
$work = "$root\work"
$out  = "$root\final"
New-Item -ItemType Directory -Force $work, $out | Out-Null
$font = "C\:/Windows/Fonts/arialbd.ttf"

# Each shot: type clip (file, start) or photo (file, mode card|full, optional crop filter), plus its caption.
$reels = [ordered]@{
  "1-heating-belt" = @{ vo = "1-belt.mp3"; voDelay = 0.2; tempo = 1.035; price = "₹999"; mrp = ""; extra = "Order now - link below"
    shots = @(
      @{ t = "clip";  f = "clips\belt-s1-bed.mp4";   ss = 0;   cap = "Har mahine wahi leak wali`nhot water bottle?" },
      @{ t = "clip";  f = "clips\belt-s2-hand.mp4";  ss = 0;   cap = "Ye try karo:`nrechargeable heating belt" },
      @{ t = "clip";  f = "1-heating-belt.mp4";      ss = 1.5; cap = "Button dabao -`ngarmi + halka massage" },
      @{ t = "photo"; f = "belt-5.jpg";  mode = "card"; cap = "Kurta ke neeche pehno,`nkaam karte raho" },
      @{ t = "photo"; f = "belt-11.jpg"; mode = "card"; cap = "Na paani. Na leak." }
    ) }
  "2-scalp-massager" = @{ vo = "2-scalp.mp3"; voDelay = 0.2; tempo = 1.01; price = "₹999"; mrp = ""; extra = "Order now - link below"
    shots = @(
      @{ t = "clip";  f = "clips\scalp-s1-office.mp4"; ss = 0;   cap = "Shaam tak sir bhaari?" },
      @{ t = "photo"; f = "scalp-9.jpg"; mode = "card"; cap = "Electric scalp massager" },
      @{ t = "clip";  f = "2-scalp-massager.mp4";      ss = 1.8; cap = "4 soft silicone heads" },
      @{ t = "photo"; f = "scalp-2.jpg"; mode = "card"; crop = "crop=iw:ih*0.66:0:0"; cap = "10 minute =`nsalon wala head massage" },
      @{ t = "photo"; f = "scalp-7.jpg"; mode = "card"; cap = "Cordless. USB charging." }
    ) }
  "3-tyre-booster" = @{ vo = "3-booster.mp3"; voDelay = 1.5; tempo = 1.0; price = "₹899"; mrp = "MRP ₹1,999"; extra = "Order now - link below"
    shots = @(
      @{ t = "clip";  f = "clips\booster-s1-road.mp4"; ss = 0;   cap = "Puncture +`nmechanic 3 km door?" },
      @{ t = "photo"; f = "booster-7.jpg"; mode = "card"; cap = "Flat tyre booster" },
      @{ t = "clip";  f = "3-tyre-booster.mp4";        ss = 1.0; cap = "Flat tyre ke neeche lagao,`nbike aaram se chalao" },
      @{ t = "photo"; f = "booster-2.jpg"; mode = "card"; cap = "Rim safe. Tyre safe.`nSteel body." },
      @{ t = "photo"; f = "booster-5.jpg"; mode = "card"; cap = "Har bike mein rakho" }
    ) }
  "4-galaxy-projector" = @{ vo = "4-projector.mp3"; voDelay = 0.2; tempo = 1.015; price = "₹1,299"; mrp = "MRP ₹2,999"; extra = "Order before 18 Dec"
    shots = @(
      @{ t = "clip";  f = "clips\projector-s1-boy.mp4"; ss = 0;  cap = "Papa, mujhe space`njaana hai!" },
      @{ t = "photo"; f = "projector-2.jpg"; mode = "card"; cap = "Astronaut galaxy projector" },
      @{ t = "clip";  f = "4-galaxy-projector.mp4";     ss = 0;  cap = "Ek button -`nkamra galaxy ban jaata hai" },
      @{ t = "photo"; f = "projector-4.jpg"; mode = "card"; cap = "Remote se colours badlo" },
      @{ t = "clip";  f = "4-galaxy-projector.mp4";     ss = 2;  cap = "Is Christmas ka`nsabse pyaara gift" }
    ) }
  "5-usb-juicer" = @{ vo = "5-juicer.mp3"; voDelay = 1.0; tempo = 1.0; price = "₹749"; mrp = "MRP ₹826"; extra = "Order now - link below"
    shots = @(
      @{ t = "clip";  f = "clips\juicer-s1-kitchen.mp4"; ss = 0;   cap = "Subah ki bhaagdaud mein`nbreakfast skip?" },
      @{ t = "clip";  f = "clips\juicer-s2-blend.mp4";   ss = 0;   cap = "Fruit + doodh + button" },
      @{ t = "clip";  f = "5-usb-juicer.mp4";            ss = 1.5; cap = "Fresh smoothie,`nseedha bottle se" },
      @{ t = "photo"; f = "juicer-2.jpg"; mode = "full";  cap = "Office bag, gym bag -`nlaptop se charge" },
      @{ t = "photo"; f = "juicer-8.jpg"; mode = "card";  cap = "Portable USB juicer" }
    ) }
}

function Run($argList) {
  & $ff -hide_banner -loglevel error -y @argList
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed: $($argList -join ' ')" }
}
function TextFile($name, $text) {
  $p = "$work\$name.txt"
  [IO.File]::WriteAllText($p, ($text -replace '`n', "`n"), (New-Object Text.UTF8Encoding $false))
  return ($p -replace '\\', '/' -replace ':', '\:')
}

$look = "eq=contrast=1.03:saturation=1.06,noise=alls=6:allf=t,format=yuv420p"

foreach ($name in $reels.Keys) {
  if ($Only -and $name -notlike "*$Only*") { continue }
  $r = $reels[$name]; $segs = @(); $i = 0
  foreach ($s in $r.shots) {
    $i++; $seg = "$work\$name-s$i.mp4"
    if ($s.t -eq "clip") {
      Run @("-ss", $s.ss, "-t", "6", "-i", "$root\$($s.f)",
            "-vf", "scale=1080:1920:flags=lanczos,fps=30,setsar=1",
            "-af", "volume=0.18,aresample=48000", "-ac", "2",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "160k", $seg)
    } else {
      $src = "$img\$($s.f)"
      $pre = if ($s.crop) { "$($s.crop)," } else { "" }
      if ($s.mode -eq "full") {
        $vf = "[0:v]${pre}scale=-2:2112,crop=1188:2112,zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=1080x1920:fps=30,setsar=1[v]"
      } else {
        $vf = "[0:v]${pre}split[a][b];" +
              "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.10[bg];" +
              "[b]scale=1040:-2,zoompan=z='1+0.0005*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=1040x1040:fps=30[fg];" +
              "[bg]fps=30,loop=180:1:0,trim=0:6,setpts=N/30/TB[bgl];[bgl][fg]overlay=(W-w)/2:(H-h)/2+150:shortest=1,setsar=1[v]"
      }
      Run @("-loop", "1", "-t", "6", "-i", $src, "-f", "lavfi", "-t", "6", "-i", "anullsrc=r=48000:cl=stereo",
            "-filter_complex", $vf, "-map", "[v]", "-map", "1:a", "-t", "6",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30", "-c:a", "aac", "-b:a", "160k", $seg)
    }
    $segs += $seg
  }

  # Join the 5 shots.
  $list = "$work\$name-list.txt"
  ($segs | ForEach-Object { "file '$($_ -replace '\\','/')'" }) | Set-Content -Encoding ascii $list
  $joined = "$work\$name-joined.mp4"
  Run @("-f", "concat", "-safe", "0", "-i", $list, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "160k", $joined)

  # Captions per shot, price card on the last shot.
  $draw = @()
  for ($k = 0; $k -lt 5; $k++) {
    $tf = TextFile "$name-cap$k" $r.shots[$k].cap
    $a = $k * 6 + 0.15; $b = ($k + 1) * 6 - 0.1
    $draw += "drawtext=fontfile='$font':textfile='$tf':fontsize=62:fontcolor=white:line_spacing=14:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=h*0.20:enable='between(t,$a,$b)'"
  }
  $pf = TextFile "$name-price" "$($r.price)  |  Cash on Delivery"
  $ef = TextFile "$name-extra" $r.extra
  $draw += "drawbox=x=90:y=ih*0.56:w=iw-180:h=150:color=0xFFCC1F@0.96:t=fill:enable='between(t,24.4,30)'"
  $draw += "drawtext=fontfile='$font':textfile='$pf':fontsize=66:fontcolor=0x151A2D:x=(w-text_w)/2:y=h*0.56+42:enable='between(t,24.4,30)'"
  $draw += "drawtext=fontfile='$font':textfile='$ef':fontsize=46:fontcolor=white:borderw=4:bordercolor=black@0.8:x=(w-text_w)/2:y=h*0.56+180:enable='between(t,24.8,30)'"
  if ($r.mrp) {
    $mf = TextFile "$name-mrp" $r.mrp
    $draw += "drawtext=fontfile='$font':textfile='$mf':fontsize=40:fontcolor=white:borderw=3:bordercolor=black@0.8:x=(w-text_w)/2:y=h*0.56-60:enable='between(t,24.4,30)'"
    $draw += "drawbox=x=(iw/2)-150:y=ih*0.56-40:w=300:h=5:color=white@0.95:t=fill:enable='between(t,24.4,30)'"
  }
  $vchain = "[0:v]$look," + ($draw -join ",") + "[v]"
  $delayMs = [int]($r.voDelay * 1000)
  $achain = "[1:a]atempo=$($r.tempo),adelay=${delayMs}|${delayMs},volume=1.6[vo];[0:a][vo]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,afade=t=out:st=29.4:d=0.6,alimiter=limit=0.95[a]"

  Run @("-i", $joined, "-i", "$root\vo\$($r.vo)", "-filter_complex", "$vchain;$achain",
        "-map", "[v]", "-map", "[a]", "-t", "30",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "$out\$name-reel.mp4")
  "built $name"
}
