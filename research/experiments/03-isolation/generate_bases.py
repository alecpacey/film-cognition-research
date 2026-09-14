#!/usr/bin/env python3
"""Stage 03 base scenes on minimax/h3-max/text-to-video. DRY RUN BY DEFAULT.
`--go --price-per-s 0.02 --cap USD` submits with a hard cap. Live schema is fetched and
asserted before any payload is built. Modelled on 01b-transfer/generate_01b.py."""
import argparse, json, os, subprocess, urllib.request
from pathlib import Path
HERE=Path(__file__).parent; ENV=HERE.parent/"01b-transfer"/".env"; ENDPOINT="minimax/h3-max/text-to-video"
SEG_S, N_SEG, RES, ASPECT = 15, 4, "768P", "16:9"
SEEDS={"face":20260920,"landscape":20260930}
STYLE=("Photographic, live-action look, 35 mm film grain. ONE SINGLE CONTINUOUS TAKE with NO cuts, NO edits, "
       "NO scene changes, NO camera switches: the same shot held unbroken for the whole duration. No text, no captions.")
PROMPTS={
 "face": "Two people in conversation at a kitchen table, medium close-up on both, warm interior light, locked-off camera on a tripod, "
         "natural back-and-forth dialogue in the audio, expressive faces, eye contact. "+STYLE,
 "landscape": "A wide river valley at late afternoon — hills, trees, water, moving cloud shadow — the camera drifting very slowly and "
              "continuously, no people, no animals. Audio: wind and distant water only, no voices, no music. "+STYLE,
}
def key():
    kv=dict(l.split("=",1) for l in ENV.read_text().splitlines() if "=" in l and not l.startswith("#"))
    k=kv.get("FAL_KEY","").strip(); assert k, "FAL_KEY missing"; os.environ["FAL_KEY"]=k; return k
def schema(k):
    url=f"https://fal.ai/api/openapi/queue/openapi.json?endpoint_id={ENDPOINT}"
    s=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"Authorization":f"Key {k}"}),timeout=30))
    inp=[v for n,v in s["components"]["schemas"].items() if n.endswith("Input")][0]; props=inp["properties"]
    print("INPUT SCHEMA (live):"); [print(f"  {f:24} req={f in inp.get('required',[])} enum={v.get('enum')} min={v.get('minimum')} max={v.get('maximum')}") for f,v in props.items()]
    assert props["duration"]["minimum"]<=SEG_S<=props["duration"]["maximum"]; assert RES in props["resolution"]["enum"]; assert "prompt_expansion_mode" in props
def payload(clip,seg,image_url=None,prompt=None):
    d={"prompt":prompt or PROMPTS[clip],"prompt_expansion_mode":"balanced","duration":SEG_S,"resolution":RES,"seed":SEEDS[clip]+seg,"enable_safety_checker":True}
    if image_url: d["image_url"]=image_url
    else: d["aspect_ratio"]=ASPECT
    return d
def last_frame(mp4):
    out=mp4.with_suffix(".last.jpg"); subprocess.run(["ffmpeg","-y","-loglevel","error","-sseof","-1","-i",str(mp4),"-update","1","-frames:v","1","-q:v","2",str(out)],check=True); return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--go",action="store_true"); ap.add_argument("--cap",type=float,default=0.0)
    ap.add_argument("--price-per-s",type=float,default=0.0); ap.add_argument("--only",choices=list(PROMPTS)); ap.add_argument("--tag",default="")
    ap.add_argument("--first-frame",help="local image to seed segment 1 (regeneration)"); ap.add_argument("--prompt",help="override the clip prompt (regeneration at different framing)"); ap.add_argument("--seed-offset",type=int,default=0); a=ap.parse_args()
    k=key(); schema(k); clips=[a.only] if a.only else list(PROMPTS)
    est=len(clips)*N_SEG*SEG_S*a.price_per_s; print(f"\nESTIMATE: {len(clips)} clip(s) × {N_SEG}×{SEG_S}s × ${a.price_per_s}/s = ${est:.2f} (cap ${a.cap})")
    for c in clips: print(f"\n[{c}] seed {SEEDS[c]+a.seed_offset}\n"+json.dumps(payload(c,a.seed_offset,prompt=(a.prompt+" "+STYLE) if a.prompt else None),indent=1)[:700])
    if not a.go: print("\nDRY RUN — nothing submitted."); return
    assert a.price_per_s>0 and a.cap>0 and est<=a.cap, f"estimate ${est:.2f} vs cap ${a.cap}"
    import fal_client
    out=HERE/"clips"; out.mkdir(exist_ok=True); recp=HERE/"generation_record.json"; rec=json.loads(recp.read_text()) if recp.exists() else {}
    for c in clips:
        name=c+a.tag; parts=[]; img=fal_client.upload_file(a.first_frame) if a.first_frame else None
        for seg in range(N_SEG):
            s=seg+a.seed_offset; ep=ENDPOINT if img is None else "minimax/h3-max/image-to-video"
            f=out/f"{name}_{seg+1}.mp4"; pl=payload(c,s,img,prompt=(a.prompt+" "+STYLE) if a.prompt else None)
            if f.exists() and f.stat().st_size>0: print(f"↺ {name} seg {seg+1} exists — resuming",flush=True); rec.setdefault(name,[]).append({"seg":seg+1,"resumed":True})
            else:
                print(f"→ {name} seg {seg+1}/{N_SEG} via {ep} seed {pl['seed']}",flush=True)
                r=fal_client.subscribe(ep,arguments=pl,with_logs=False); url=r["video"]["url"]; urllib.request.urlretrieve(url,f)
                rec.setdefault(name,[]).append({"seg":seg+1,"endpoint":ep,"seed":pl["seed"],"url":url,"expanded_prompt":r.get("expanded_prompt"),"timings":r.get("timings")})
            parts.append(f); img=fal_client.upload_file(str(last_frame(f)))
        lst=out/f"{name}_parts.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
        subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(out/f"{name}.mp4")],check=True)
        recp.write_text(json.dumps(rec,indent=1)); print(f"✓ {name}.mp4",flush=True)
if __name__=="__main__": main()
