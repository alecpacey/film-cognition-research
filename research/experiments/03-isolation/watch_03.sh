#!/bin/zsh
# lightweight: one short python per minute, nothing resident. Harvests + pauses at 12/12 or on terminal stage.
cd "$(dirname "$0")"
while true; do
  out=$(python3 - <<'PY'
from huggingface_hub import HfApi, hf_hub_download, get_token
import json, re, urllib.request
from pathlib import Path
api=HfApi(); S="alecnpacey/tribe-probe"; RES="alecnpacey/tribe-probe-results"
try: urllib.request.urlopen(urllib.request.Request(f"https://{S.replace('/','-')}.hf.space/",headers={"Authorization":f"Bearer {get_token()}"}),timeout=15)
except Exception: pass
st=api.space_info(S).runtime.stage
ALL=set(json.load(open("names.json"))); fs=[f for f in api.list_repo_files(RES,repo_type="dataset") if f.startswith("results/") and re.sub(r"^\d{2}_","",Path(f).stem) in ALL]
done = len(fs)>=12 or st in ("PAUSED","BUILD_ERROR","RUNTIME_ERROR","CONFIG_ERROR")
if done:
    out={}
    for f in fs:
        v=json.loads(Path(hf_hub_download(RES,f,repo_type="dataset")).read_text()).get("parcels",{})
        if len(v)==180: out[re.sub(r"^\d{2}_03_","",Path(f).stem)]=v
    Path("parcel_vectors.json").write_text(json.dumps(out,indent=1))
    if st!="PAUSED": api.pause_space(S)
    print(f"DONE {st} harvested {len(out)}/12")
else: print(f"{st} {len(fs)}/12")
PY
)
  echo "[$(date +%T)] $out" >> watch.log
  [[ "$out" == DONE* ]] && break
  sleep 60
done
