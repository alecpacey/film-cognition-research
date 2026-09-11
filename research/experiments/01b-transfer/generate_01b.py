#!/usr/bin/env python3
"""01b generation against minimax/h3-max/text-to-video. DRY RUN BY DEFAULT: prints
the exact payloads and submits nothing. `--go --cap USD` submits with a hard spend cap.
Introspection first: the live OpenAPI is fetched and the input schema printed and
asserted before any payload is built (standing rule: introspect before writing)."""
import argparse, json, os, re, sys, time, hashlib, subprocess, urllib.request
from pathlib import Path
HERE=Path(__file__).parent; ENDPOINT="minimax/h3-max/text-to-video"
SEG_S, N_SEG, RES, ASPECT = 15, 4, "768P", "16:9"
SEEDS={"landscape":20260911,"crowd":20260912,"face":20260913}
STYLE="Photographic, live-action look, natural light, 35 mm film grain. No text, no captions."
def key():
    kv=dict(l.split("=",1) for l in (HERE/".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
    k=kv.get("FAL_KEY","").strip(); assert k, "FAL_KEY missing in .env"; os.environ["FAL_KEY"]=k; return k
def prompts():
    t=(HERE/"README.md").read_text()
    rows=re.findall(r"\| \*\*(landscape|crowd|face)\*\* \| \*(.*?)\* \|", t, re.S)
    P={k:" ".join(v.split()) for k,v in rows}; assert set(P)=={"landscape","crowd","face"}, P.keys()
    c=(HERE/"CLIPS.md").read_text(); blk=c.split("### Face-clip dialogue")[1].split("Content is deliberately")[0]
    lines=[re.sub(r"\*\(.*?\)\*","",m.group(2)).strip() for m in re.finditer(r"> \*\*([AB]):\*\* (.*)",blk)]
    P["_face_lines"]=lines  # split across segments in payload(); ~5 lines per 15 s
    P["landscape"]+=" Audio: wind through trees, a distant river, no voices, no music."
    P["crowd"]+=" Audio: the indistinct murmur of many people, footsteps, a distant announcement chime; no intelligible words, no music."
    return P
def schema(k):
    url=f"https://fal.ai/api/openapi/queue/openapi.json?endpoint_id={ENDPOINT}"
    s=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"Authorization":f"Key {k}"}),timeout=30))
    inp=[v for n,v in s["components"]["schemas"].items() if n.endswith("Input")][0]
    props=inp["properties"]; print("INPUT SCHEMA (live):")
    for f,v in props.items(): print(f"  {f:24} req={f in inp.get('required',[])} {v.get('type','')} enum={v.get('enum')} min={v.get('minimum')} max={v.get('maximum')} default={v.get('default')}")
    assert props["duration"]["minimum"]<=SEG_S<=props["duration"]["maximum"], "duration out of range"
    assert RES in props["resolution"]["enum"], f"resolution {RES} not offered"
    assert "prompt_expansion_mode" in props, "schema drift: prompt_expansion_mode gone"
    return props
def payload(clip,text,seg,image_url=None,lines=None):
    if clip=="face" and lines:
        per=-(-len(lines)//N_SEG); chunk=lines[seg*per:(seg+1)*per]
        text+=" Two voices, alternating, one lower and one higher register, conversational pace. In this shot they say, in order: "+" / ".join(f'"{l}"' for l in chunk)
    d={"prompt":text,"prompt_expansion_mode":"balanced","duration":SEG_S,"resolution":RES,"seed":SEEDS[clip]+seg,"enable_safety_checker":True}
    if image_url: d["image_url"]=image_url
    else: d["aspect_ratio"]=ASPECT
    return d
def last_frame(mp4):
    out=mp4.with_suffix(".last.jpg"); subprocess.run(["ffmpeg","-y","-loglevel","error","-sseof","-0.05","-i",str(mp4),"-frames:v","1","-q:v","2",str(out)],check=True); return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--go",action="store_true"); ap.add_argument("--cap",type=float,default=0.0); ap.add_argument("--only",choices=["landscape","crowd","face"]); ap.add_argument("--price-per-s",type=float,default=0.0,help="USD per second at 768P, user-verified"); a=ap.parse_args()
    k=key(); props=schema(k); P=prompts(); FL=P.pop("_face_lines")
    est=3*N_SEG*SEG_S*a.price_per_s; print(f"\nESTIMATE: 3 clips × {N_SEG}×{SEG_S}s = {3*N_SEG*SEG_S}s × ${a.price_per_s}/s = ${est:.2f}  (cap ${a.cap})")
    print("\nPAYLOADS (segment 1 of each clip; segments 2-4 add image_url = previous last frame, seed+1..3):")
    for clip,text in P.items():
        if a.only and clip!=a.only: continue
        for seg in range(N_SEG if clip=="face" else 1):
            print(f"\n[{clip}] seg {seg+1}  seed {SEEDS[clip]+seg}\n"+json.dumps(payload(clip,text,seg,lines=FL),indent=1)[:900])
    if not a.go: print("\nDRY RUN — nothing submitted. Re-run with --go --cap <USD> to generate."); return
    assert a.price_per_s>0 and a.cap>0, "set --price-per-s and --cap"; assert est<=a.cap, f"estimate ${est:.2f} exceeds cap ${a.cap}"
    import fal_client
    out=HERE/"clips"; out.mkdir(exist_ok=True); rec={}
    for clip,text in P.items():
        if a.only and clip!=a.only: continue
        parts=[]; img=None
        for seg in range(N_SEG):
            ep=ENDPOINT if img is None else "minimax/h3-max/image-to-video"
            pl=payload(clip,text,seg,img,lines=FL); print(f"→ {clip} seg {seg+1}/{N_SEG} via {ep} seed {pl['seed']}",flush=True)
            r=fal_client.subscribe(ep,arguments=pl,with_logs=False)
            url=r["video"]["url"]; f=out/f"{clip}_{seg+1}.mp4"; urllib.request.urlretrieve(url,f)
            parts.append(f); rec.setdefault(clip,[]).append({"seg":seg+1,"endpoint":ep,"seed":pl["seed"],"url":url,"expanded_prompt":r.get("expanded_prompt"),"timings":r.get("timings")})
            img=fal_client.upload_file(str(last_frame(f)))
        lst=out/f"{clip}_parts.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
        subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(out/f"{clip}.mp4")],check=True)
        (HERE/"generation_record.json").write_text(json.dumps(rec,indent=1)); print(f"✓ {clip}.mp4")
if __name__=="__main__": main()
