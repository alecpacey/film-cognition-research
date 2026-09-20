#!/usr/bin/env python3
"""03b session 1: stage 20 clips (REF first, so the identity test lands early), deploy the timeline-saving
app, restart the Space, exit. Not resident. watch_03b.sh does the rest.   python3 score_03b.py"""
import json, time
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd
H = Path(__file__).parent; api = HfApi()
SPACE, CLIPS, RES = "alecnpacey/tribe-probe", "alecnpacey/tribe-probe-clips", "alecnpacey/tribe-probe-results"
SRC = {"REF": H.parent / "03-isolation" / "clips" / "Sminus", "B": H / "clips" / "B", "C": H / "clips" / "C", "D": H / "clips" / "D"}
LV = ["cut01", "cut03", "cut07", "cut15", "cut31"]
FILES = {f"03b_{lad}_{c}": SRC[lad] / f"{c}.mp4" for lad in ("REF", "B", "C", "D") for c in LV}
def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)
import re
st = api.space_info(SPACE).runtime.stage; assert st == "PAUSED", f"Space is {st}, not PAUSED"
v = api.get_space_variables(SPACE); val = lambda k: str(getattr(v.get(k), "value", v.get(k)))
assert val("AUDIO_ONLY") == "1", "AUDIO_ONLY is not 1"; assert val("RESULTS_REPO") == RES, f"RESULTS_REPO is {val('RESULTS_REPO')}"
existing = {re.sub(r"^\d{2}_", "", Path(f).stem) for f in api.list_repo_files(RES, repo_type="dataset") if f.startswith("results/")}
assert not (existing & set(FILES)), f"03b results already exist: {sorted(existing & set(FILES))}"
for n, p in FILES.items(): assert p.exists(), p
have = {Path(f).stem for f in api.list_repo_files(CLIPS, repo_type="dataset") if f.startswith("clips/")}
for n, p in FILES.items():
    if n in have: continue
    api.upload_file(path_or_fileobj=str(p), path_in_repo=f"clips/{n}.mp4", repo_id=CLIPS, repo_type="dataset", commit_message=f"03b: {n}"); log(f"uploaded {n}")
api.upload_file(path_or_fileobj=json.dumps({"clips": list(FILES)}).encode(), path_in_repo="batch.json", repo_id=CLIPS, repo_type="dataset", commit_message="03b batch")
staged = json.loads(Path(__import__("huggingface_hub").hf_hub_download(CLIPS, "batch.json", repo_type="dataset", force_download=True)).read_text())["clips"]
assert staged == list(FILES), "batch.json did not verify"
api.upload_file(path_or_fileobj=str(H / "app_timelines.py"), path_in_repo="app.py", repo_id=SPACE, repo_type="space", commit_message="03b: save per-parcel 1 Hz timelines (adds fields only)")
log("patched app deployed"); (H / "names.json").write_text(json.dumps(list(FILES))); (H / "session_start.txt").write_text(str(time.time()))
st = api.space_info(SPACE).runtime.stage
if st == "PAUSED": api.restart_space(SPACE); log("Space restart requested")
else: log(f"Space already {st} after app upload")
log("20 clips staged; expect ≈ 3.5 h. Run watch_03b.sh.")
