#!/bin/zsh
# light: one short python per minute, nothing resident. Identity test on the first REF clip; harvest + pause + restore app at the end.
cd "$(dirname "$0")"
while true; do
  out=$(python3 - <<'PY'
from huggingface_hub import HfApi, hf_hub_download, get_token
import json, re, time, urllib.request
from pathlib import Path
api=HfApi(); S="alecnpacey/tribe-probe"; RES="alecnpacey/tribe-probe-results"; BUDGET_MIN=270
ALL=json.load(open("names.json")); t0=float(open("session_start.txt").read()); el=(time.time()-t0)/60
try: urllib.request.urlopen(urllib.request.Request(f"https://{S.replace('/','-')}.hf.space/",headers={"Authorization":f"Bearer {get_token()}"}),timeout=15)
except Exception: pass
st=api.space_info(S).runtime.stage
fs={re.sub(r"^\d{2}_","",Path(f).stem):f for f in api.list_repo_files(RES,repo_type="dataset") if f.startswith("results/") and re.sub(r"^\d{2}_","",Path(f).stem) in set(ALL)}
def finish(why):
    pv,tl={}, {}
    for n,f in fs.items():
        d=json.loads(Path(hf_hub_download(RES,f,repo_type="dataset",force_download=True)).read_text())
        if len(d.get("parcels",{}))==180: pv[n[4:]]=d["parcels"]; tl[n[4:]]={"abs_times":d.get("abs_times"),"parcel_timeline":d.get("parcel_timeline")}
    Path("parcel_vectors.json").write_text(json.dumps(pv,indent=1)); Path("timelines.json").write_text(json.dumps(tl))
    if api.space_info(S).runtime.stage not in ("PAUSED",): 
        try: api.pause_space(S)
        except Exception as e: print("pause failed",e)
    api.upload_file(path_or_fileobj="app_deployed_before.py",path_in_repo="app.py",repo_id=S,repo_type="space",commit_message="03b: restore original app")
    print(f"DONE ({why}) stage {api.space_info(S).runtime.stage} harvested {len(pv)}/20 app restored")
idf=Path("identity.json")
if "03b_REF_cut01" in fs and not idf.exists():
    new=json.loads(Path(hf_hub_download(RES,fs["03b_REF_cut01"],repo_type="dataset",force_download=True)).read_text())
    old=json.load(open("../03-isolation/parcel_vectors.json"))["Sminus_cut01"]
    d=max(abs(new["parcels"][p]["raw"]-old[p]["raw"]) for p in old); tl=new.get("parcel_timeline") or {}
    dm=max(abs(sum(tl[p])/len(tl[p])-new["parcels"][p]["raw"]) for p in tl) if tl else None
    ok = d<=1e-4 and dm is not None and dm<=1e-5 and len(tl)==180
    idf.write_text(json.dumps({"max_abs_raw_delta_vs_stage03":d,"max_abs_timeline_mean_minus_raw":dm,"n_timelines":len(tl),"timeline_len":len(next(iter(tl.values()))) if tl else 0,"pass":ok}))
    if not ok: finish(f"IDENTITY FAIL raw Δ {d:.2e} tl Δ {dm}"); raise SystemExit
    print(f"IDENTITY PASS raw Δ {d:.2e}, timeline-mean Δ {dm:.2e}, {len(tl)} timelines", end=" | ")
if len(fs)>=20: finish("all 20")
elif st in ("PAUSED","BUILD_ERROR","RUNTIME_ERROR","CONFIG_ERROR") and el>4: finish(f"terminal stage {st}")
elif el>BUDGET_MIN: finish("budget minutes reached")
else: print(f"{st} {len(fs)}/20 {el:.0f} min")
PY
)
  echo "[$(date +%T)] $out" >> watch.log
  [[ "$out" == *DONE* ]] && break
  sleep 60
done
