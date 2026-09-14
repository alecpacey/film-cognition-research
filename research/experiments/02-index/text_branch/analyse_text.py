#!/usr/bin/env python3
"""Exploratory: cut-rate -> parcel r with text branch OFF (registered vectors) vs ON, same segments."""
import json, numpy as np
from pathlib import Path
H=Path(__file__).parent; I=H.parent
on=json.load(open(H/"parcel_vectors_text.json")); off_all=json.load(open(I/"parcel_vectors.json")); dt=json.load(open(I/"dial_table.json"))
names=[n for n in json.load(open(H/"batch_names.json")) if n in on]; assert names, "no text-on vectors"
parcels=sorted(off_all[names[0]]); films=np.array([dt[n]["film"] for n in names])
def cw(M):
    M=M.astype(float).copy()
    for f in np.unique(films): m=films==f; M[m]-=M[m].mean(0)
    return M
z=lambda src,n,p: src[n][p]["z"] if isinstance(src[n][p],dict) else src[n][p]
Yoff=cw(np.array([[z(off_all,n,p) for p in parcels] for n in names])); Yon=cw(np.array([[z(on,n,p) for p in parcels] for n in names]))
x=cw(np.array([[float(dt[n]["cuts_per_min"])] for n in names]))[:,0]
def r(a,b): return float(np.corrcoef(a,b)[0,1]) if a.std()>0 and b.std()>0 else float("nan")
tab={p:{"r_off":r(x,Yoff[:,parcels.index(p)]),"r_on":r(x,Yon[:,parcels.index(p)])} for p in ["A4","A5","MBelt","A1","IFJa","IFJp","IFSp","8C"]}
seg_corr={n:r(np.array([z(off_all,n,p) for p in parcels]),np.array([z(on,n,p) for p in parcels])) for n in names}
allr_off=np.array([r(x,Yoff[:,j]) for j in range(180)]); allr_on=np.array([r(x,Yon[:,j]) for j in range(180)])
out={"EXPLORATORY":True,"n":len(names),"segments":names,"cut_rate_r":tab,"per_segment_off_on_vector_r":seg_corr,
     "corr_of_cutrate_maps_off_vs_on":r(allr_off,allr_on),"top_on":[parcels[j] for j in np.argsort(allr_on)[:5]]+["|"]+[parcels[j] for j in np.argsort(-allr_on)[:5]]}
Path(H/"result.json").write_text(json.dumps(out,indent=1)); print(json.dumps(out,indent=1))
