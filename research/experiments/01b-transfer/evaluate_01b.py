#!/usr/bin/env python3
"""Evaluate 01b against README.md criteria. --self-test runs it on run 00's own
vectors: must give PASS with axis r = +0.936, else the evaluator is wrong."""
import argparse, json, numpy as np
from itertools import combinations
from pathlib import Path
HERE=Path(__file__).parent; EXP=HERE.parent
PLACE=["VMV1","VMV2","VMV3","PHA1","PHA2","PHA3"]; VOICE=["A4","A5","STSdp","STSvp"]; TOPK=10; BAR=0.50
def load(p): d=json.load(open(p)); return {c:{k:(v["z"] if isinstance(v,dict) else v) for k,v in vec.items()} for c,vec in d.items()}
def axis1(parcels):
    r=json.load(open(EXP/"02-index/analysis_result.json")); sel=json.load(open(EXP/"02-index/selection.json")); dials=sel["dials"]
    B=np.array([[r["per_parcel"][p]["coef"][d] for d in dials] for p in parcels]); U,S,Vt=np.linalg.svd(B,full_matrices=False)
    a=U[:,0]; return a if Vt[0][dials.index("face_area_frac")]>0 else -a
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    src=EXP/"00-probe/parcel_vectors.json" if a.self_test else HERE/"parcel_vectors.json"
    V=load(src); parcels=sorted(V["face"]); assert set(V)=={"landscape","crowd","face"}
    vec=lambda c: np.array([V[c][p] for p in parcels]); rank=lambda c: {p:i for i,p in enumerate(sorted(parcels,key=lambda p:-V[c][p]))}
    top={c:set(sorted(parcels,key=lambda p:-V[c][p])[:TOPK]) for c in V}
    jac=[len(top[a]&top[b])/len(top[a]|top[b]) for a,b in combinations(V,2)]; c1=float(np.mean(jac))
    def chain_rank(c,chain): return np.mean([rank(c)[p] for p in chain if p in rank(c)])
    land_best=all(chain_rank("landscape",PLACE)<chain_rank(o,PLACE) for o in ("crowd","face"))
    face_best=all(chain_rank("face",VOICE)<chain_rank(o,VOICE) for o in ("landscape","crowd"))
    ax=axis1(parcels); contrast=vec("face")-vec("landscape"); c3=float(np.corrcoef(contrast,ax)[0,1])
    ref=load(EXP/"00-probe/parcel_vectors.json"); rc=np.array([ref["face"][p]-ref["landscape"][p] for p in parcels]); r_ref=float(np.corrcoef(contrast,rc)[0,1])
    ok1,ok2,ok3=c1<0.60,(land_best and face_best),c3>=BAR
    verdict="PASS" if ok1 and ok2 and ok3 else ("PARTIAL" if ok1 and ok2 else "FAIL")
    out={"source":str(src),"criterion_1_mean_jaccard":c1,"criterion_1_met":ok1,"criterion_2_landscape_place":land_best,"criterion_2_face_voice":face_best,"criterion_2_met":ok2,
         "criterion_3_axis_r":c3,"criterion_3_bar":BAR,"criterion_3_met":ok3,"reported_corr_with_run00_contrast":r_ref,
         "per_clip_corr_with_run00":{c:float(np.corrcoef(vec(c),np.array([ref[c][p] for p in parcels]))[0,1]) for c in V},"verdict":verdict}
    print(json.dumps(out,indent=1))
    if not a.self_test: (HERE/"evaluation.json").write_text(json.dumps(out,indent=1))
if __name__=="__main__": main()
