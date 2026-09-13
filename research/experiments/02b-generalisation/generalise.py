#!/usr/bin/env python3
"""02b — does the fitted index predict out-of-medium (generated) clips? EXPLORATORY, n=3.
Predict each 01b clip's 180-parcel vector from its 14 dials via the stage-02 coefficient
matrix B, using the index's own preprocessing (centre, then divide by stage-02 within-film
SD — analyse.py D3). Compare predicted vs actual. Nulls: (a) parcel-label permutation of
the prediction; (b) all 3! dial-to-clip reassignments."""
import json, itertools, numpy as np
from pathlib import Path
E=Path(__file__).resolve().parents[1]; I=E/"02-index"; T=E/"01b-transfer"
r=json.load(open(I/"analysis_result.json")); sel=json.load(open(I/"selection.json")); dt=json.load(open(I/"dial_table.json"))
dials=sel["dials"]; parcels=sorted(r["per_parcel"]); surv=[p for p in parcels if r["per_parcel"][p]["survives"]]
B=np.array([[r["per_parcel"][p]["coef"][d] for d in dials] for p in parcels])          # 180 x 14
# stage-02 scale: within-film-centred SD over the 70 analysed segments, as analyse.py
clips70=sorted(sel["selected"]); films=np.array([dt[c]["film"] for c in clips70])
X70=np.array([[float(dt[c][d]) for d in dials] for c in clips70],float)
for f in np.unique(films): m=films==f; X70[m]-=X70[m].mean(0)
sd=X70.std(0,ddof=1); sd[sd==0]=1
raw70=np.array([[float(dt[c][d]) for d in dials] for c in clips70])
# 01b dials from cinemetrics (same mapping as measure_dials.py)
def dialvec(c):
    v=json.load(open(T/"clips"/f"{c}.cinemetrics.json")); d=v[0] if isinstance(v,list) else v
    hr=d["shot_scale"].get("hit_rate",0.0)
    return [d["cuts"]["cuts_per_min"],d["cuts"]["mean_shot_len_s"],d["camera"]["jitter"],d["camera"]["net_zoom"],d["camera"]["pan_per_frame_frac"],
            d["lighting"]["median_luma"],d["lighting"]["contrast_p5_p95"],d["lighting"]["shadow_frac"],d["colour"]["colourfulness"],d["colour"]["mean_saturation"],
            d["colour"]["warm_cool"],d["shot_scale"].get("face_area_frac") or 0.0,hr,d["dof"]["centre_surround_sharpness"]]
names=["landscape","crowd","face"]; Xg=np.array([dialvec(c) for c in names],float)
inrange={d:bool(raw70[:,i].min()<=Xg[:,i].min() and Xg[:,i].max()<=raw70[:,i].max()) for i,d in enumerate(dials)}
Xc=(Xg-Xg.mean(0))/sd
pv=json.load(open(T/"parcel_vectors.json")); Y=np.array([[pv[c][p]["z"] if isinstance(pv[c][p],dict) else pv[c][p] for p in parcels] for c in names]); Yc=Y-Y.mean(0)
P=Xc@B.T
def corr(a,b): return float(np.corrcoef(a,b)[0,1])
si=[parcels.index(p) for p in surv]
out={"EXPLORATORY":True,"n":3,"dials_within_stage02_range":inrange,
     "per_clip_profile_r":{c:corr(P[i],Yc[i]) for i,c in enumerate(names)},
     "per_clip_profile_r_survivors":{c:corr(P[i,si],Yc[i,si]) for i,c in enumerate(names)},
     "contrast_face_minus_landscape_r":corr(P[2]-P[0],Yc[2]-Yc[0]),
     "contrast_face_minus_landscape_r_survivors":corr(P[2,si]-P[0,si],Yc[2,si]-Yc[0,si])}
rng=np.random.default_rng(0)
out["null_parcel_perm_95th"]=float(np.percentile([abs(corr(rng.permutation(P[2]-P[0]),Yc[2]-Yc[0])) for _ in range(5000)],95))
reass=[]
for perm in itertools.permutations(range(3)):
    Pp=Xc[list(perm)]@B.T; reass.append((perm, np.mean([corr(Pp[i],Yc[i]) for i in range(3)])))
out["mean_profile_r_by_dial_assignment"]={"".join("LCF"[k] for k in perm):round(v,3) for perm,v in reass}
out["mean_profile_r_true_assignment_rank"]=int(sorted([v for _,v in reass],reverse=True).index(dict((p,v) for p,v in reass)[(0,1,2)])+1)
Path(__file__).with_name("result.json").write_text(json.dumps(out,indent=1)); print(json.dumps(out,indent=1))
