#!/usr/bin/env python3
"""Harvest every 03b result present on the results repo, by exact name. Read-only on HF.  python3 harvest_03b.py"""
import json, re
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download
H = Path(__file__).parent; RES = "alecnpacey/tribe-probe-results"; ALL = set(json.load(open(H / "names.json")))
fs = {re.sub(r"^\d{2}_", "", Path(f).stem): f for f in HfApi().list_repo_files(RES, repo_type="dataset") if f.startswith("results/")}
pv, tl = {}, {}
for n in sorted(ALL & set(fs)):
    d = json.loads(Path(hf_hub_download(RES, fs[n], repo_type="dataset", force_download=True)).read_text())
    z = [v["z"] for v in d["parcels"].values()]; assert len(z) == 180 and all(x == x for x in z) and max(map(abs, z)) <= 8, n
    pv[n[4:]] = d["parcels"]; tl[n[4:]] = {"abs_times": d.get("abs_times"), "parcel_timeline": d.get("parcel_timeline")}
(H / "parcel_vectors.json").write_text(json.dumps(pv, indent=1)); (H / "timelines.json").write_text(json.dumps(tl))
print(f"harvested {len(pv)}/20:", sorted(pv), "| with timelines:", sum(1 for v in tl.values() if v["parcel_timeline"]))
