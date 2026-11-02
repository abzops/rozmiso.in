# Rozmiso Reels v2: fast-cut clickbait edit (10 shots x 3 s), hook headline on frame 0,
# timed word captions, SFX accents (whoosh / pop / riser / hit), price slam at 24 s.
# Two hook versions (A, B) per product. Usage: powershell -File build-reels-v2.ps1 [-Only belt]
param([string]$Only = "")

$ErrorActionPreference = "Stop"
$ff   = "C:\Users\asus\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
$root = "C:\StacknStock\Research\Rozmiso\Research\ad-videos"
$work = "$root\work2"; $out = "$root\final"
New-Item -ItemType Directory -Force $work, $out | Out-Null
$font = "C\:/Windows/Fonts/arialbd.ttf"

function Run($argList) {
  & $ff -hide_banner -loglevel error -y @argList
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed: $($argList -join ' ')" }
}
function Esc($p) { $p -replace '\\', '/' -replace ':', '\:' }
function TextFile($name, $text) {
  $p = "$work\$name.txt"
  [IO.File]::WriteAllText($p, $text, (New-Object Text.UTF8Encoding $false))
  return (Esc $p)
}
function Wrap($s, $max) {
  if ($s.Length -le $max) { return $s }
  $mid = [int]($s.Length / 2); $best = -1
  for ($d = 0; $d -lt $mid; $d++) {
    if ($mid + $d -lt $s.Length -and $s[$mid + $d] -eq ' ') { $best = $mid + $d; break }
    if ($mid - $d -gt 0 -and $s[$mid - $d] -eq ' ') { $best = $mid - $d; break }
  }
  if ($best -lt 0) { return $s }
  return $s.Substring(0, $best) + "`n" + $s.Substring($best + 1)
}

# ---- Sound effects, made once with FFmpeg (no music) ----
$sfx = "$work\sfx"; New-Item -ItemType Directory -Force $sfx | Out-Null
if (-not (Test-Path "$sfx\hit.wav")) {
  Run @("-f","lavfi","-i","anoisesrc=d=0.45:c=pink:a=0.8","-af","highpass=f=350,lowpass=f=5000,afade=t=in:d=0.28:curve=qsin,afade=t=out:st=0.28:d=0.17,aformat=sample_rates=48000:channel_layouts=stereo","$sfx\air.wav")
  Run @("-f","lavfi","-i","sine=f=820:d=0.08","-af","afade=t=out:d=0.08:curve=exp,aformat=sample_rates=48000:channel_layouts=stereo","$sfx\pop.wav")
  Run @("-f","lavfi","-i","anoisesrc=d=0.85:c=pink:a=0.8","-af","highpass=f=250,afade=t=in:d=0.82:curve=exp,afade=t=out:st=0.82:d=0.03,aformat=sample_rates=48000:channel_layouts=stereo","$sfx\riser.wav")
  Run @("-f","lavfi","-i","sine=f=58:d=0.6","-af","afade=t=out:d=0.6:curve=exp,lowpass=f=2500,aformat=sample_rates=48000:channel_layouts=stereo","$sfx\hit.wav")
}

# Shots: @(file, start) for clips, @("photo:<file>") for animated product photos. 10 shots x 3 s.
$reels = [ordered]@{
  "1-heating-belt" = @{ vo="1-belt.mp3"; delay=0.2; tempo=1.035; price="₹999"; mrp=""; cta="Neeche link pe order karo"
    hookA="Hot water bottle ka`nzamana gaya!"; hookB="Ladkiyon ka naya`nfavourite gadget"
    shots=@(@("clips\belt-s1-bed.mp4",0),@("clips\belt-s1-bed.mp4",3),@("clips\belt-s2-hand.mp4",0),@("clips\belt-s2-hand.mp4",3),
            @("1-heating-belt.mp4",1),@("1-heating-belt.mp4",4),@("clips\belt-s4.mp4",0),@("clips\belt-s4.mp4",3),@("photo:belt-5.jpg"),@("photo:belt-11.jpg"))
    caps=@("Har mahine wahi garam paani ki bottle","wahi leak, wahi geeli bedsheet","Phir maine ye try kiya","Rechargeable heating belt","Bas button dabao","kuch hi seconds mein garmi","aur saath mein halka massage","Pehen ke aaram se baitho","ya kurta ke neeche, office college","Na paani, na jhanjhat","Sirf ₹999, Cash on Delivery","Neeche link pe click karo!") }
  "2-scalp-massager" = @{ vo="2-scalp.mp3"; delay=0.2; tempo=1.01; price="₹999"; mrp=""; cta="Neeche link pe order karo"
    hookA="10 minute mein salon`njaisa head massage?"; hookB="Papa ne wapas`nhi nahi diya!"
    shots=@(@("clips\scalp-s1-office.mp4",0),@("clips\scalp-s1-office.mp4",3),@("clips\scalp-s5.mp4",0),@("2-scalp-massager.mp4",2),
            @("clips\scalp-s3.mp4",0),@("clips\scalp-s3.mp4",3),@("clips\scalp-s4.mp4",0),@("clips\scalp-s4.mp4",3),@("clips\scalp-s5.mp4",3),@("photo:scalp-7.jpg"))
    caps=@("Poora din screen, traffic, tension","aur shaam tak sir bhaari","Ye dekho...","Electric scalp massager","4 soft silicone heads","jo dheere dheere ghoomte hain","Bas 10 minute","jaise salon wala head massage","Papa ne wapas hi nahi diya!","Cordless, USB charging","Sirf ₹999, Cash on Delivery","Link pe click karo!") }
  "3-tyre-booster" = @{ vo="3-booster.mp3"; delay=1.2; tempo=1.0; price="₹899"; mrp="MRP ₹1,999"; cta="Neeche link pe order karo"
    hookA="Puncture hua?`nYe jugaad jaan lo"; hookB="Har bike wale ke paas`nye hona chahiye"
    shots=@(@("clips\booster-s1-road.mp4",0),@("clips\booster-s1-road.mp4",3),@("clips\booster-s2.mp4",0),@("clips\booster-s2.mp4",3),
            @("3-tyre-booster.mp4",0),@("3-tyre-booster.mp4",3),@("clips\booster-s4.mp4",0),@("clips\booster-s5.mp4",0),@("clips\booster-s5.mp4",3),@("photo:booster-5.jpg"))
    caps=@("Bhai, raste mein puncture!","Mechanic 3 km door","Dhoop mein bike ghaseetna?","Kisi ko pasand nahi","Isliye ab main ye rakhta hoon","Flat tyre booster","Flat tyre ke neeche lagao","Bike ek haath se chalegi","Rim safe, tyre safe","Steel body, mazboot wheels","Sirf ₹899, Cash on Delivery","Link pe order karo!") }
  "4-galaxy-projector" = @{ vo="4-projector.mp3"; delay=0.2; tempo=1.015; price="₹1,299"; mrp="MRP ₹2,999"; cta="18 Dec se pehle order karo"
    hookA="Bachche ne kaha`nspace jaana hai..."; hookB="Pura kamra galaxy`nban gaya!"
    shots=@(@("clips\projector-s1-boy.mp4",0),@("clips\projector-s1-boy.mp4",3),@("clips\projector-s2.mp4",0),@("clips\projector-s2.mp4",3),
            @("clips\projector-s3.mp4",0),@("clips\projector-s3.mp4",3),@("4-galaxy-projector.mp4",2),@("clips\projector-s4.mp4",0),@("clips\projector-s4.mp4",3),@("4-galaxy-projector.mp4",5))
    caps=@("Bete ne kaha...","Papa, mujhe space jaana hai!","Toh main space hi ghar le aaya","Astronaut galaxy projector","Bas ek button...","aur poora kamra galaxy!","Stars, nebula, sab ghoomte hue","Remote se colours badlo","Bedtime ban jaaye mazedaar","Is Christmas ka best gift","Sirf ₹1,299, Cash on Delivery","18 December se pehle order karo!") }
  "5-usb-juicer" = @{ vo="5-juicer.mp3"; delay=0.8; tempo=1.0; price="₹749"; mrp="MRP ₹826"; cta="Neeche link pe order karo"
    hookA="Breakfast skip`nkarte ho?"; hookB="Office mein fresh`nsmoothie? Ye dekho"
    shots=@(@("clips\juicer-s1-kitchen.mp4",0),@("clips\juicer-s1-kitchen.mp4",3),@("clips\juicer-s2-blend.mp4",0),@("clips\juicer-s2-blend.mp4",3),
            @("5-usb-juicer.mp4",1),@("5-usb-juicer.mp4",4),@("clips\juicer-s4.mp4",0),@("clips\juicer-s4.mp4",3),@("clips\juicer-s5.mp4",0),@("clips\juicer-s5.mp4",3))
    caps=@("Subah ki bhaagdaud mein breakfast?","Skip! Par ab nahi.","Portable USB juicer","Fruit daalo, thoda doodh","Button dabao...","aur fresh smoothie ready","Glass ki zaroorat nahi","Seedha isi bottle se piyo","Office bag, gym bag mein rakho","Laptop se hi charge karo","Sirf ₹749, Cash on Delivery","Link pe click karo!") }
}

$voDur = @{ "1-belt.mp3"=30.96; "2-scalp.mp3"=30.16; "3-booster.mp3"=25.68; "4-projector.mp3"=30.4; "5-juicer.mp3"=26.8 }

foreach ($name in $reels.Keys) {
  if ($Only -and $name -notlike "*$Only*") { continue }
  $r = $reels[$name]; $segs = @()

  # 1) Ten 3-second shots, each with a slow push-in.
  for ($i = 0; $i -lt 10; $i++) {
    $s = $r.shots[$i]; $seg = "$work\$name-$i.mp4"
    if ($s[0] -like "photo:*") {
      $src = "$root\photos\$($s[0].Substring(6))"
      $vf = "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.12,fps=30,loop=90:1:0,trim=0:3,setpts=N/30/TB[bg];" +
            "[b]scale=1000:-2,zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1000x1000:fps=30[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-60:shortest=1,setsar=1[v]"
      Run @("-loop","1","-t","3","-i",$src,"-f","lavfi","-t","3","-i","anullsrc=r=48000:cl=stereo","-filter_complex",$vf,"-map","[v]","-map","1:a","-t","3",
            "-c:v","libx264","-preset","veryfast","-crf","18","-r","30","-c:a","aac","-b:a","160k",$seg)
    } else {
      Run @("-ss",$s[1],"-t","3","-i","$root\$($s[0])",
            "-vf","fps=30,scale=1080:1920:flags=lanczos,zoompan=z='1+0.0009*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1",
            "-af","volume=0.12,aresample=48000","-ac","2","-t","3","-c:v","libx264","-preset","veryfast","-crf","18","-c:a","aac","-b:a","160k",$seg)
    }
    $segs += $seg
  }
  $list = "$work\$name-list.txt"
  ($segs | ForEach-Object { "file '$($_ -replace '\\','/')'" }) | Set-Content -Encoding ascii $list
  $joined = "$work\$name-joined.mp4"
  Run @("-f","concat","-safe","0","-i",$list,"-c:v","libx264","-preset","veryfast","-crf","18","-c:a","aac","-b:a","160k",$joined)

  # 2) Caption timing: spread the chunks over the voiceover by text length.
  $start = $r.delay; $len = $voDur[$r.vo] / $r.tempo
  $tot = ($r.caps | ForEach-Object { $_.Length + 6 } | Measure-Object -Sum).Sum
  $t = $start; $capDraw = @(); $events = @(); $k = 0
  foreach ($c in $r.caps) {
    $d = $len * ($c.Length + 6) / $tot; $a = [math]::Round($t, 2); $b = [math]::Round($t + $d - 0.04, 2)
    $col = if ($k % 2 -eq 0) { "white" } else { "0xFFD21F" }
    $tf = TextFile "$name-c$k" (Wrap $c 20)
    if ($k -lt 10) { $capDraw += "drawtext=fontfile='$font':textfile='$tf':text_align=C:fontsize=76:fontcolor=$($col):line_spacing=10:borderw=7:bordercolor=black:shadowx=0:shadowy=6:shadowcolor=black@0.5:x=(w-text_w)/2:y=1230:alpha='min(1,(t-$a)/0.08)':enable='between(t,$a,$b)'" ; $events += ,@($a, "pop", 0.05) }
    $t += $d; $k++
  }
  for ($c = 1; $c -lt 10; $c++) { $events += ,@(($c * 3 - 0.18), "air", 0.10) }
  $events += ,@(23.15, "riser", 0.10); $events += ,@(24.0, "hit", 0.55); $events += ,@(0.02, "hit", 0.40)

  # 3) Price slam (24 s on), MRP strike, CTA.
  $pf = TextFile "$name-price" $r.price; $cf = TextFile "$name-cod" "CASH ON DELIVERY"; $ctf = TextFile "$name-cta" $r.cta
  $price = @(
    "drawtext=fontfile='$font':textfile='$pf':fontsize=170:fontcolor=0xFFD21F:borderw=10:bordercolor=black:x=(w-text_w)/2:y=640:alpha='min(1,(t-24)/0.1)':enable='gte(t,24)'",
    "drawtext=fontfile='$font':textfile='$cf':fontsize=58:fontcolor=0x151A2D:box=1:boxcolor=0xFFD21F:boxborderw=22:x=(w-text_w)/2:y=860:alpha='min(1,(t-24.3)/0.1)':enable='gte(t,24.3)'",
    "drawtext=fontfile='$font':textfile='$ctf':fontsize=50:fontcolor=white:borderw=5:bordercolor=black:x=(w-text_w)/2:y=1000:enable='gte(t,25.2)*lt(mod(t*2,2),1.6)'"
  )
  if ($r.mrp) {
    $mf = TextFile "$name-mrp" $r.mrp
    $price += "drawtext=fontfile='$font':textfile='$mf':fontsize=52:fontcolor=white:borderw=5:bordercolor=black:x=(w-text_w)/2:y=570:enable='gte(t,24)'"
    $price += "drawbox=x=iw/2-170:y=598:w=340:h=7:color=0xFF3B3B:t=fill:enable='gte(t,24.15)'"
  }

  # SFX bed for this reel.
  $sfxIn = @(); $sfxF = @(); $j = 0
  foreach ($e in $events) {
    $sfxIn += @("-i", "$sfx\$($e[1]).wav"); $ms = [int]($e[0] * 1000)
    $sfxF += "[$($j):a]volume=$($e[2]),adelay=$ms|$ms[s$j]"; $j++
  }
  $sfxMix = ($sfxF -join ";") + ";" + ((0..($j - 1) | ForEach-Object { "[s$_]" }) -join "") + "amix=inputs=$($j):duration=longest:normalize=0,apad=whole_dur=30[sfxbed]"
  $sfxWav = "$work\$name-sfx.wav"
  Run (@($sfxIn) + @("-filter_complex", $sfxMix, "-map", "[sfxbed]", "-t", "30", "-ar", "48000", $sfxWav))

  # 4) Two hook versions.
  foreach ($v in @("A", "B")) {
    $hook = if ($v -eq "A") { $r.hookA } else { $r.hookB }
    $hf = TextFile "$name-hook$v" $hook
    $hookDraw = "drawtext=fontfile='$font':textfile='$hf':text_align=C:fontsize=80:fontcolor=0x151A2D:line_spacing=12:box=1:boxcolor=0xFFD21F:boxborderw=26:x=(w-text_w)/2:y=230:enable='lt(t,2.9)'"
    $look = "eq=contrast=1.05:saturation=1.10,vignette=PI/5,noise=alls=3:allf=t,format=yuv420p"
    $vchain = "[0:v]$look,$hookDraw," + (($capDraw + $price) -join ",") + "[v]"
    $dms = [int]($r.delay * 1000)
    $achain = "[1:a]atempo=$($r.tempo),adelay=$dms|$dms,volume=1.7[vo];[0:a][vo][2:a]amix=inputs=3:duration=first:normalize=0,afade=t=out:st=29.5:d=0.5,alimiter=limit=0.95[a]"
    Run @("-i",$joined,"-i","$root\vo\$($r.vo)","-i",$sfxWav,"-filter_complex","$vchain;$achain","-map","[v]","-map","[a]","-t","30",
          "-c:v","libx264","-preset","medium","-crf","21","-maxrate","7M","-bufsize","14M","-profile:v","high","-pix_fmt","yuv420p","-movflags","+faststart",
          "-c:a","aac","-b:a","192k","-ar","48000","$out\$name-hook$v.mp4")
  }
  "built $name"
}
