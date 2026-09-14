#!/bin/zsh
# Stage 03 ladder: stage 01's build_conditions.py on the generated bases, then S+/S- arms, then cinemetrics.
set -e; cd "$(dirname "$0")"; L=build.log; : > $L
echo "[$(date +%T)] ladder" >> $L
python3 ../01-cutrate/build_conditions.py clips/face_close.mp4 clips/landscape.mp4 --outdir clips/ladder >> $L 2>&1
mkdir -p clips/Splus clips/Sminus
for f in clips/ladder/cut*.mp4; do n=$(basename $f)
  cp $f clips/Splus/$n                                   # S+: as built (face scene keeps its native dialogue)
  ffmpeg -y -loglevel error -i $f -i clips/landscape.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest clips/Sminus/$n
done
echo "[$(date +%T)] arms built: $(ls clips/Splus | wc -l | tr -d ' ') S+ / $(ls clips/Sminus | wc -l | tr -d ' ') S-" >> $L
echo "[$(date +%T)] cinemetrics" >> $L
cd ../02-index
ls ../03-isolation/clips/Splus/cut*.mp4 ../03-isolation/clips/Sminus/cut*.mp4 | xargs -P 4 -I{} sh -c 'python3 ../../cinematography/cinemetrics.py "{}" --json "{}.cinemetrics.json" >/dev/null 2>&1 && echo "[$(date +%T)] measured {}" >> ../03-isolation/build.log'
echo "[$(date +%T)] DONE" >> ../03-isolation/build.log
