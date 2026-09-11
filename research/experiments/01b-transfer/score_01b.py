#!/usr/bin/env python3
"""Score the three 01b clips on the Space. Mirrors run_batch.py's manifest path
(clips repo + batch.json) and auto_batch.py's file-channel completion + keepalive.
    python3 score_01b.py            # upload, restart, poll, harvest, pause
    python3 score_01b.py --harvest  # just collect + pause
"""
import argparse, json, re, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download, get_token
SPACE="alecnpacey/tribe-probe"; CLIPS_REPO="alecnpacey/tribe-probe-clips"; RESULTS_REPO="alecnpacey/tribe-probe-results"
NAMES=["01b_landscape","01b_crowd","01b_face"]; HERE=Path(__file__).parent; api=HfApi()
def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}",flush=True)
def keepalive():
    try: urllib.request.urlopen(urllib.request.Request(f"https://{SPACE.replace('/','-')}.hf.space/",headers={"Authorization":f"Bearer {get_token()}"}),timeout=15)
    except Exception: pass
def results():
    return {re.sub(r"^\d{2}_","",Path(f).stem):f for f in api.list_repo_files(RESULTS_REPO,repo_type="dataset") if f.startswith("results/") and f.endswith(".json")}
def harvest():
    out={}
    for n,f in results().items():
        if n in NAMES:
            d=json.loads(Path(hf_hub_download(RESULTS_REPO,f,repo_type="dataset")).read_text()); v=d.get("parcels",{})
            assert len(v)==180, f"{n}: {len(v)} parcels"; out[n.replace("01b_","")]=v
    (HERE/"parcel_vectors.json").write_text(json.dumps(out,indent=1)); log(f"harvested {len(out)}/3 -> parcel_vectors.json")
    api.pause_space(SPACE); log("Space paused"); return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--harvest",action="store_true"); a=ap.parse_args()
    if a.harvest: harvest(); return
    pre=set(results()); assert not (pre & set(NAMES)), f"01b results already exist: {pre & set(NAMES)} — refusing to rescore"
    have={Path(f).stem for f in api.list_repo_files(CLIPS_REPO,repo_type="dataset") if f.startswith("clips/")}
    for n in NAMES:
        f=HERE/"clips"/f"{n.replace('01b_','')}.mp4"; assert f.exists(), f"missing {f}"
        if n in have: log(f"clips/{n}.mp4 already in {CLIPS_REPO} — not re-uploading"); continue
        api.upload_file(path_or_fileobj=str(f),path_in_repo=f"clips/{n}.mp4",repo_id=CLIPS_REPO,repo_type="dataset",commit_message=f"01b: {n}")
        log(f"uploaded clips/{n}.mp4 ({f.stat().st_size//1024} kB)")
    api.upload_file(path_or_fileobj=json.dumps({"clips":NAMES}).encode(),path_in_repo="batch.json",repo_id=CLIPS_REPO,repo_type="dataset",commit_message="01b batch")
    api.restart_space(SPACE); log("Space restarting; polling results repo (~35 min for 3 clips)")
    t0=time.time()
    while time.time()-t0<70*60:
        time.sleep(60); keepalive(); have=set(results()) & set(NAMES)
        st=api.space_info(SPACE).runtime.stage; log(f"{st}  {len(have)}/3 result files")
        if st in ("BUILD_ERROR","RUNTIME_ERROR","CONFIG_ERROR"): log("TERMINAL STAGE"); break
        if len(have)==3: break
    harvest()
if __name__=="__main__": main()
