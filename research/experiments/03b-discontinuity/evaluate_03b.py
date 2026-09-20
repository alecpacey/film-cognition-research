#!/usr/bin/env python3
"""
Evaluate 03b against README.md, as fixed in commit 221faad. Written before any 03b result existed.

Primary: frontal ratio rho_F = mean slope of IFJa/IFJp/IFSp/8C on ln(constructed cuts) / REF's +0.251,
one-sided level-permutation p over 120 orderings. REPRODUCES: rho_F >= 0.50 and p <= 0.05.
ABSENT: rho_F <= 0.25. else PARTIAL. Same-scene = B and C jointly. Verdict table per README.
    ../02-index/.venv-analysis/bin/python evaluate_03b.py [--selftest]  ->  evaluation.json
"""
import json, sys, itertools, numpy as np
from pathlib import Path
H = Path(__file__).parent; REF = json.loads((H / "reference_mode.json").read_text())
parcels, m = REF["parcels"], np.array(REF["reference_slopes_Sminus"]); LV = ["cut01", "cut03", "cut07", "cut15", "cut31"]; x = np.log([1, 3, 7, 15, 31])
ci, ai = [parcels.index(p) for p in REF["cluster"]], [parcels.index(p) for p in REF["auditory"]]
F0, A0 = float(m[ci].mean()), float(m[ai].mean())
def slope(Z, xx): xc = xx - xx.mean(); return (xc @ (Z - Z.mean(0))) / (xc @ xc)
def ladder(pv, prefix):
    Z = np.array([[pv[f"{prefix}{c}"][p]["z"] for p in parcels] for c in LV])
    f = lambda xx: (lambda b: (b[ci].mean(), b[ai].mean(), (b @ m) / (m @ m), np.corrcoef(b, m)[0, 1]))(slope(Z, xx))
    o = f(x); null = np.array([f(x[list(p)]) for p in itertools.permutations(range(5))])
    ev = np.linalg.eigvalsh(np.cov((Z - Z.mean(0)).T)); ev = ev[ev > 1e-9]; b = slope(Z, x)
    rF, pF = o[0] / F0, float((null[:, 0] >= o[0] - 1e-12).mean())
    cls = "REPRODUCES" if (rF >= 0.50 and pF <= 0.05) else ("ABSENT" if rF <= 0.25 else "PARTIAL")
    return {"frontal_slope": float(o[0]), "rho_F": float(rF), "p_F": pF, "class": cls,
            "per_parcel_frontal_slopes": {p: float(b[parcels.index(p)]) for p in REF["cluster"]},
            "auditory_slope": float(o[1]), "rho_A": float(o[1] / A0), "p_A": float((null[:, 1] <= o[1] + 1e-12).mean()),
            "gain": float(o[2]), "p_gain": float((null[:, 2] >= o[2] - 1e-12).mean()), "r_with_ref_mode": float(o[3]),
            "participation_ratio_across_levels": float(ev.sum() ** 2 / (ev ** 2).sum()),
            "whole_vector_r_cut01_vs_cut31": float(np.corrcoef(Z[0], Z[-1])[0, 1])}
def verdict(B, C, D):
    ss = "REPRODUCES" if B == C == "REPRODUCES" else ("ABSENT" if B == C == "ABSENT" else "PARTIAL")
    if D is None: return ss, {"REPRODUCES": "DISCONTINUITY (D dropped)", "ABSENT": "NOT-DISCONTINUITY (D dropped)"}.get(ss, "GRADED (D dropped)")
    if ss == "REPRODUCES": return ss, ("EITHER" if D == "REPRODUCES" else "DISCONTINUITY")
    if ss == "ABSENT" and D == "REPRODUCES": return ss, "SWITCH"
    if ss == "ABSENT" and D == "ABSENT": return ss, "CONJUNCTION"
    return ss, "GRADED"
if "--selftest" in sys.argv:
    pv3 = json.loads((H.parent / "03-isolation" / "parcel_vectors.json").read_text()); cal = REF["calibration"]
    a, b = ladder(pv3, "Sminus_"), ladder(pv3, "Splus_")
    assert abs(a["rho_F"] - 1) < 1e-9 and abs(a["gain"] - 1) < 1e-9 and abs(b["gain"] - cal["stage03_Splus_on_Sminus"]["gain"]) < 1e-9 and abs(b["frontal_slope"] - cal["stage03_Splus_on_Sminus"]["cluster_slope"]) < 1e-9
    assert verdict("REPRODUCES", "REPRODUCES", "ABSENT")[1] == "DISCONTINUITY" and verdict("ABSENT", "ABSENT", "REPRODUCES")[1] == "SWITCH" and verdict("ABSENT", "ABSENT", "ABSENT")[1] == "CONJUNCTION" and verdict("REPRODUCES", "PARTIAL", "ABSENT")[1] == "GRADED" and verdict("REPRODUCES", "REPRODUCES", "REPRODUCES")[1] == "EITHER"
    print(f"selftest PASS: S- on itself rho_F {a['rho_F']:.3f} ({a['class']}, p {a['p_F']:.3f}); S+ rho_F {b['rho_F']:.3f} ({b['class']}, p {b['p_F']:.3f}), gain {b['gain']:.3f}"); sys.exit(0)
pv = json.loads((H / "parcel_vectors.json").read_text()); out = {}
for lad in ("REF", "B", "C", "D"):
    if all(f"{lad}_{c}" in pv for c in LV): out[lad] = ladder(pv, f"{lad}_")
ss, v = verdict(out["B"]["class"], out["C"]["class"], out["D"]["class"] if "D" in out else None)
out["same_scene_class"], out["verdict"] = ss, v; out["identity"] = json.loads((H / "identity.json").read_text()) if (H / "identity.json").exists() else None
(H / "evaluation.json").write_text(json.dumps(out, indent=1))
for lad in ("REF", "B", "C", "D"):
    if lad in out: o = out[lad]; print(f"{lad:3} rho_F {o['rho_F']:+.2f} (p {o['p_F']:.3f}) {o['class']:10} | rho_A {o['rho_A']:+.2f} (p {o['p_A']:.3f}) | gain {o['gain']:+.2f} (p {o['p_gain']:.3f}) r {o['r_with_ref_mode']:+.2f} | PR {o['participation_ratio_across_levels']:.2f} | frontal " + " ".join(f"{k} {s:+.2f}" for k, s in o["per_parcel_frontal_slopes"].items()))
print(f"\nsame-scene: {ss}   VERDICT: {v}")
