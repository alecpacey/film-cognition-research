#!/usr/bin/env python3
"""03b: score ONE ladder (<= 8 clips; auto_batch.py's SAFE_BATCH) under the guarded app. Resume by omission.
    python3 score_batch.py D"""
import json, re, sys, time
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download
H = Path(__file__).parent; api = HfApi(); lad = sys.argv[1]; assert lad in ("C", "D")
SPACE, CLIPS, RES = "alecnpacey/tribe-probe", "alecnpacey/tribe-probe-clips", "alecnpacey/tribe-probe-results"
def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)
st = api.space_info(SPACE).runtime.stage; assert st == "PAUSED", f"Space is {st}"
v = api.get_space_variables(SPACE); val = lambda k: str(getattr(v.get(k), "value", v.get(k)))
assert val("AUDIO_ONLY") == "1" and val("RESULTS_REPO") == RES
done = {re.sub(r"^\d{2}_", "", Path(f).stem) for f in api.list_repo_files(RES, repo_type="dataset") if f.startswith("results/")}
todo = [f"03b_{lad}_{c}" for c in ("cut01", "cut03", "cut07", "cut15", "cut31") if f"03b_{lad}_{c}" not in done]
assert 0 < len(todo) <= 8, f"todo={todo}"
have = {Path(f).stem for f in api.list_repo_files(CLIPS, repo_type="dataset") if f.startswith("clips/")}; assert set(todo) <= have, "clips missing from clips repo"
api.upload_file(path_or_fileobj=json.dumps({"clips": todo}).encode(), path_in_repo="batch.json", repo_id=CLIPS, repo_type="dataset", commit_message=f"03b batch {lad}")
assert json.loads(Path(hf_hub_download(CLIPS, "batch.json", repo_type="dataset", force_download=True)).read_text())["clips"] == todo
api.set_space_sleep_time(SPACE, 1800); log("Space sleep timeout -> 1800 s for this session")
api.upload_file(path_or_fileobj=str(H / "app_timelines_guarded.py"), path_in_repo="app.py", repo_id=SPACE, repo_type="space", commit_message="03b: guarded app (self-pause on completion, 80 min watchdog)")
(H / "batch_names.json").write_text(json.dumps(todo)); (H / "session_start.txt").write_text(str(time.time()))
if api.space_info(SPACE).runtime.stage == "PAUSED": api.restart_space(SPACE)
log(f"launched {lad}: {todo}; server-side cap 80 min")
