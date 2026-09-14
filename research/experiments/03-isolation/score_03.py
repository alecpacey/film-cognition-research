#!/usr/bin/env python3
"""Score the 12 stage-03 clips (5 S+, 5 S-, 2 bases) on the Space via the manifest path. Pauses on every exit."""
import json, re, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download, get_token
SPACE="alecnpacey/tribe-probe"; CLIPS="alecnpacey/tribe-probe-clips"; RES="alecnpacey/tribe-probe-results"; HERE=Path(__file__).parent; api=HfApi()
FILES={f"03_{arm}_{c}":HERE/"clips"/arm/f"{c}.mp4" for arm in ("Splus","Sminus") for c in ("cut01","cut03","cut07","cut15","cut31")}
FILES.update({"03_base_face":HERE/"clips/face_close.mp4","03_base_landscape":HERE/"clips/landscape.mp4"})
def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}",flush=True)
def results(): return {re.sub(r"^\d{2}_","",Path(f).stem) for f in api.list_repo_files(RES,repo_type="dataset") if f.startswith("results/") and f.endswith(".json")}
def harvest():
    out={}
    for f in api.list_repo_files(RES,repo_type="dataset"):
        n=re.sub(r"^\d{2}_","",Path(f).stem)
        if f.startswith("results/") and n in FILES:
            v=json.loads(Path(hf_hub_download(RES,f,repo_type="dataset")).read_text()).get("parcels",{})
            if len(v)==180: out[n.replace("03_","")]=v
    (HERE/"parcel_vectors.json").write_text(json.dumps(out,indent=1)); log(f"harvested {len(out)}/12")
    api.pause_space(SPACE); log("Space paused")
try:
    assert api.space_info(SPACE).runtime.stage=="PAUSED", "Space not paused"
    v=api.get_space_variables(SPACE); assert str(getattr(v.get("AUDIO_ONLY"),"value",v.get("AUDIO_ONLY","1")))=="1", "AUDIO_ONLY not 1"
    assert not (results() & set(FILES)), "03 results already exist"
    have={Path(f).stem for f in api.list_repo_files(CLIPS,repo_type="dataset") if f.startswith("clips/")}
    for n,p in FILES.items():
        assert p.exists(), p
        if n in have: continue
        api.upload_file(path_or_fileobj=str(p),path_in_repo=f"clips/{n}.mp4",repo_id=CLIPS,repo_type="dataset",commit_message=f"03: {n}"); log(f"uploaded {n}")
    api.upload_file(path_or_fileobj=json.dumps({"clips":list(FILES)}).encode(),path_in_repo="batch.json",repo_id=CLIPS,repo_type="dataset",commit_message="03 batch")
    api.restart_space(SPACE); log("Space restarting; 12 clips ≈ 2 h")
    t0=time.time()
    while time.time()-t0<200*60:
        time.sleep(60)
        try: urllib.request.urlopen(urllib.request.Request(f"https://{SPACE.replace('/','-')}.hf.space/",headers={"Authorization":f"Bearer {get_token()}"}),timeout=15)
        except Exception: pass
        st=api.space_info(SPACE).runtime.stage; n=len(results() & set(FILES)); log(f"{st} {n}/12")
        if st in ("BUILD_ERROR","RUNTIME_ERROR","CONFIG_ERROR","PAUSED") or n==12: break
finally:
    harvest()
