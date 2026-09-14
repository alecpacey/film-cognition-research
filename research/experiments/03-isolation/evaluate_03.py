#!/usr/bin/env python3
"""Evaluate stage 03 against README.md. Per arm: Pearson r of each parcel's z vs log(measured cut count) over 5 levels."""
import json, numpy as np
from pathlib import Path
H=Path(__file__).parent; pv=json.load(open(H/"parcel_vectors.json")); parcels=sorted(next(iter(pv.values())))
cuts={"cut01":1,"cut03":3,"cut07":7,"cut15":15,"cut31":31}; CL=["IFJa","IFJp","IFSp","8C"]; AUD=["A4","A5","MBelt","A1"]
z=lambda c,p: pv[c][p]["z"] if isinstance(pv[c][p],dict) else pv[c][p]
out={}
for arm in ("Splus","Sminus"):
    lv=[f"{arm}_{c}" for c in cuts]; x=np.log([cuts[c] for c in cuts])
    r={p:float(np.corrcoef(x,[z(c,p) for c in lv])[0,1]) for p in parcels}
    v0=np.array([z(lv[0],p) for p in parcels]); v4=np.array([z(lv[-1],p) for p in parcels])
    out[arm]={"n_parcels_abs_r_gt_0.9":sum(abs(v)>0.9 for v in r.values()),"cluster":{p:r[p] for p in CL},"auditory":{p:r[p] for p in AUD},
              "cluster_hits_r_gt_0.9_positive":sum(r[p]>0.9 for p in CL),"cut01_vs_cut31_whole_vector_r":float(np.corrcoef(v0,v4)[0,1]),
              "top6":sorted(r.items(),key=lambda kv:-abs(kv[1]))[:6]}
h3a=out["Splus"]["cluster_hits_r_gt_0.9_positive"]>=2; h3b=out["Sminus"]["cluster_hits_r_gt_0.9_positive"]>=2
aud_tracks=any(abs(out[a]["auditory"][p])>0.9 for a in out for p in AUD)
verdict="PASS" if h3a and h3b else "PARTIAL-A" if h3a else ("PARTIAL-B" if aud_tracks else "FAIL")
out["H3a"]=h3a; out["H3b"]=h3b; out["verdict"]=verdict
(H/"evaluation.json").write_text(json.dumps(out,indent=1))
for arm in ("Splus","Sminus"):
    o=out[arm]; print(f"{arm}: |r|>0.9 parcels {o['n_parcels_abs_r_gt_0.9']}/180 (chance~7) | cluster hits {o['cluster_hits_r_gt_0.9_positive']}/4 | cut01~cut31 r {o['cut01_vs_cut31_whole_vector_r']:+.3f}")
    print("   cluster:", {p:round(v,3) for p,v in o["cluster"].items()}); print("   auditory:", {p:round(v,3) for p,v in o["auditory"].items()})
    print("   top:", [(p,round(v,3)) for p,v in o["top6"]])
print(f"\nH3a {h3a}  H3b {h3b}  VERDICT: {verdict}")
