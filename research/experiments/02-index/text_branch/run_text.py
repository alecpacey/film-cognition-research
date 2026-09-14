#!/usr/bin/env python3
"""Restart the Space with AUDIO_ONLY=0, poll the text results repo (file channel + keepalive),
harvest, pause, and restore AUDIO_ONLY=1 / RESULTS_REPO on every exit path."""
import json, re, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download, get_token
api=HfApi(); SPACE="alecnpacey/tribe-probe"; RT="alecnpacey/tribe-probe-results-text"
names=json.load(open(Path(__file__).with_name("batch_names.json")))
def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}",flush=True)
def ka():
    try: urllib.request.urlopen(urllib.request.Request("https://alecnpacey-tribe-probe.hf.space/",headers={"Authorization":f"Bearer {get_token()}"}),timeout=15)
    except Exception: pass
def have():
    try: return {re.sub(r"^\d{2}_","",Path(f).stem):f for f in api.list_repo_files(RT,repo_type="dataset") if f.startswith("results/") and f.endswith(".json")}
    except Exception: return {}
def finish(why):
    log(f"finishing: {why}")
    out={}
    for n,f in have().items():
        if n in names:
            d=json.loads(Path(hf_hub_download(RT,f,repo_type="dataset")).read_text()); v=d.get("parcels",{})
            if len(v)==180: out[n]=v
    Path(__file__).with_name("parcel_vectors_text.json").write_text(json.dumps(out,indent=1)); log(f"harvested {len(out)}/{len(names)}")
    try: api.pause_space(SPACE); log("Space paused")
    except Exception as e: log(f"pause failed: {e}")
    api.add_space_variable(SPACE,"AUDIO_ONLY","1"); api.add_space_variable(SPACE,"RESULTS_REPO","alecnpacey/tribe-probe-results"); log("vars restored")
try:
    api.restart_space(SPACE); log(f"restarted; {len(names)} clips, text branch ON")
except Exception as e:
    log(f"RESTART FAILED: {type(e).__name__}: {str(e)[:200]}"); finish("restart failed"); raise SystemExit(1)
t0=time.time(); BUDGET_MIN=250   # ~$4.2 at $1/hr, under the ~$4.35 credit
while True:
    time.sleep(60); ka(); h=set(have())&set(names)
    try: st=api.space_info(SPACE).runtime.stage
    except Exception as e: st=f"?{type(e).__name__}"
    el=(time.time()-t0)/60; log(f"{st}  {len(h)}/{len(names)}  {el:.0f} min")
    if len(h)==len(names): finish("all clips reported"); break
    if st in ("BUILD_ERROR","RUNTIME_ERROR","CONFIG_ERROR","PAUSED","STOPPED"): finish(f"terminal stage {st}"); break
    if el>BUDGET_MIN: finish("budget minutes reached"); break
