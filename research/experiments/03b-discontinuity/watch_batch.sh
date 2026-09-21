#!/bin/zsh
# one short python per minute. Pauses on: batch complete, stall (no new result in 25 min), 85 min, terminal stage. Never restores/pauses late: every exit path pauses.
cd "$(dirname "$0")"
while true; do
  out=$(python3 - <<'PY'
from huggingface_hub import HfApi, get_token
import json, re, time, urllib.request
from pathlib import Path
api=HfApi(); S="alecnpacey/tribe-probe"; RES="alecnpacey/tribe-probe-results"
ALL=json.load(open("batch_names.json")); t0=float(open("session_start.txt").read()); now=time.time(); el=(now-t0)/60
try: urllib.request.urlopen(urllib.request.Request(f"https://{S.replace('/','-')}.hf.space/",headers={"Authorization":f"Bearer {get_token()}"}),timeout=15)
except Exception: pass
st=api.space_info(S).runtime.stage
n=len({re.sub(r"^\d{2}_","",Path(f).stem) for f in api.list_repo_files(RES,repo_type="dataset") if f.startswith("results/")} & set(ALL))
pf=Path("progress.json"); pr=json.loads(pf.read_text()) if pf.exists() else {"n":-1,"t":t0}
if pr.get("t0")!=t0: pr={"n":-1,"t":t0,"t0":t0}
if n!=pr["n"]: pr.update(n=n,t=now); pf.write_text(json.dumps(pr))
stall=(now-pr["t"])/60
def stop(why):
    s2=api.space_info(S).runtime.stage
    if s2!="PAUSED":
        try: api.pause_space(S)
        except Exception as e: print("pause failed",e)
    print(f"DONE ({why}) was {s2} now {api.space_info(S).runtime.stage} {n}/{len(ALL)} {el:.0f} min")
if st=="PAUSED" and el>3: stop("Space paused itself" if n>=len(ALL) else "Space paused early")
elif n>=len(ALL): stop("all scored; self-pause had not fired yet")
elif st in ("BUILD_ERROR","RUNTIME_ERROR","CONFIG_ERROR"): stop(f"terminal {st}")
elif stall>(35 if n<=0 else 25): stop(f"STALL {stall:.0f} min without a new result")
elif el>85: stop("85 min cap")
else: print(f"{st} {n}/{len(ALL)} {el:.0f} min (last progress {stall:.0f} min ago)")
PY
)
  echo "[$(date +%T)] $out" >> watch_batch.log
  [[ "$out" == *DONE* ]] && break
  sleep 60
done
