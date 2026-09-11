#!/bin/zsh
# 01b target-audio tracks. Free/local route: macOS say + ffmpeg. Reproducible; re-run to regenerate.
set -e; cd "$(dirname "$0")"; W=audio/work; mkdir -p $W
VA=Daniel; VB=Flo; RATE=165
norm() { ffmpeg -y -loglevel error -i "$1" -af "apad,atrim=0:60,loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -ac 2 -c:a aac -b:a 192k -t 60 "$2"; }

# ---- face: two-voice dialogue from CLIPS.md ----
python3 - <<'PY' > $W/lines.tsv
import re
t=open("CLIPS.md").read()
blk=t.split("### Face-clip dialogue")[1].split("Content is deliberately")[0]
for l in blk.splitlines():
    m=re.match(r"> \*\*([AB]):\*\* (.*)",l.strip())
    if m: print(m.group(1)+"\t"+re.sub(r"\*\(.*?\)\*","",m.group(2)).strip())
PY
rm -f $W/face_parts.txt; i=0
while IFS=$'\t' read -r who line; do
  v=$VA; [ "$who" = "B" ] && v=$VB
  say -v "$v" -r $RATE -o $W/l$i.aiff "$line"
  ffmpeg -y -loglevel error -i $W/l$i.aiff -af "apad=pad_dur=0.55" $W/l$i.wav
  echo "file 'l$i.wav'" >> $W/face_parts.txt; i=$((i+1))
done < $W/lines.tsv
ffmpeg -y -loglevel error -f concat -safe 0 -i $W/face_parts.txt -c copy $W/face_raw.wav
norm $W/face_raw.wav audio/face.m4a

# ---- landscape: wind (brown noise, lowpass, slow tremolo) + river (pink band) ----
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=c=brown:r=48000:a=0.6:d=60" -f lavfi -i "anoisesrc=c=pink:r=48000:a=0.25:d=60"   -filter_complex "[0:a]lowpass=f=400,tremolo=f=0.1:d=0.6[wind];[1:a]bandpass=f=1600:w=1200,volume=0.5[river];[wind][river]amix=inputs=2:normalize=0[out]"   -map "[out]" $W/land_raw.wav
norm $W/land_raw.wav audio/landscape.m4a

# ---- crowd: 8 overlapping low-content voices (walla) + 2 distant chimes ----
sents=("the platform for the later service is on the other side" "we could wait here or go down and see" "they said twenty minutes but that was a while ago" "no I think it was the one before that" "did you get the tickets or should I" "it is the same every time we come through here" "let us just find somewhere to sit for a bit" "I will call them once we are on the train")
vs=($(say -v '?' | awk '/en_(GB|US|AU|IE)/{print $1}' | grep -vE 'Bad|Bahh|Bells|Boing|Bubbles|Cellos|Wobble|Whisper|Trinoids|Zarvox|Jester|Organ|Superstar|Good' | head -8))
rm -f $W/walla_in.txt; j=0
for s in "${sents[@]}"; do v=${vs[$((j % ${#vs[@]} + 1))]}; say -v "$v" -r $((150+j*7)) -o $W/w$j.aiff "$s. $s. $s. $s. $s. $s."; j=$((j+1)); done
ffmpeg -y -loglevel error $(for k in $(seq 0 7); do printf -- "-i $W/w%d.aiff " $k; done) -f lavfi -i "sine=f=880:d=0.25" -f lavfi -i "sine=f=1108:d=0.35"   -filter_complex "$(for k in $(seq 0 7); do printf "[%d:a]adelay=%d|%d,aloop=loop=-1:size=2e9,atrim=0:60,volume=0.10,lowpass=f=3500[v%d];" $k $((k*1700)) $((k*1700)) $k; done)[8:a]adelay=20000|20000,volume=0.25[c1];[9:a]adelay=20300|20300,volume=0.25[c2];[8:a]adelay=45000|45000,volume=0.25[c3];[9:a]adelay=45300|45300,volume=0.25[c4];[v0][v1][v2][v3][v4][v5][v6][v7][c1][c2][c3][c4]amix=inputs=12:normalize=0,aecho=0.7:0.6:60:0.3[out]"   -map "[out]" -t 60 $W/crowd_raw.wav
norm $W/crowd_raw.wav audio/crowd.m4a
for f in landscape crowd face; do printf "%-10s %s s  %s\n" $f "$(ffprobe -v error -show_entries format=duration -of csv=p=0 audio/$f.m4a)" "$(ffprobe -v error -select_streams a -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 audio/$f.m4a)"; done
