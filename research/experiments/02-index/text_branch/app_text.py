"""
Probe runner for the duplicated TRIBE Space.

This REPLACES the reference Space's interactive app.py. We want the reference
Space's *environment* — its tribev2 fork with relaxed torch caps, its pinned
transformers, its patches and windowing — not its UI. So we import its modules
and drive them directly.

Runs on dedicated hardware (L4), so there is no ZeroGPU decorator and no
per-call duration cap to work around.

Pass criteria are fixed in 00-probe/README.md and are evaluated here as written:
  1. separation — mean pairwise Jaccard overlap of top-10 ROI sets < 0.6
  2. direction  — judged by eye against the expected region families

What it prints is the whole result. Copy it into RESULT.md.
"""

import os
# Silence progress bars BEFORE anything imports tqdm. They were ~40% of the log,
# and HF's /logs/run only serves a bounded window from the start of the log — so
# with bars on, a 10-clip run goes unreadable after clip 4 and a stall is invisible.
os.environ.setdefault("TQDM_DISABLE", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
import json
import sys
import traceback
from itertools import combinations
from pathlib import Path

import gradio as gr
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

CLIP_DIR = Path(__file__).parent / "probe_clips"
CACHE = os.environ.get("TRIBE_CACHE", "./cache")
TOP_K = 10

# Durable results. stdout is NOT storage: HF's /logs/run serves a bounded window
# from the START of the log, so once a run passes ~1,500 lines nothing printed
# afterwards is ever readable again. Two collection runs were lost to that. Each
# clip's vector is therefore also uploaded, the moment it exists, to a SEPARATE
# private dataset repo — separate because any commit to this Space's own repo
# triggers a rebuild and would restart the run mid-batch.
RESULTS_REPO = os.environ.get("RESULTS_REPO", "alecnpacey/tribe-probe-results")
CLIPS_REPO = os.environ.get("CLIPS_REPO", "alecnpacey/tribe-probe-clips")


def _fetch_batch():
    """Pull this batch's clips from the clips dataset, as listed in its batch.json.

    Clips used to be pushed into this Space's own repo. That hit the 1 GB private
    Space storage cap on 6 Sep after ~70 clips — deleted LFS objects keep counting —
    and every push also triggered a rebuild. Now the clips live in a dataset repo,
    uploaded once, and a batch is a 200-byte manifest plus a restart.

    The manifest's order is preserved via an ordinal prefix, so sorted() below
    scores clips in the deficit-first order run_batch chose. Falls back to whatever
    is in probe_clips/ if there is no manifest, so the old path still works.
    """
    import shutil
    tok = os.environ.get("HF_TOKEN")
    try:
        from huggingface_hub import hf_hub_download
        m = hf_hub_download(CLIPS_REPO, "batch.json", repo_type="dataset", token=tok,
                            force_download=True)
        names = json.loads(Path(m).read_text())["clips"]
    except Exception as e:
        print(f"BATCH_FETCH\tno manifest ({type(e).__name__}); using local probe_clips/", flush=True)
        return
    CLIP_DIR.mkdir(exist_ok=True)
    for f in CLIP_DIR.glob("*.mp4"):
        f.unlink()
    for i, n in enumerate(names):
        src = hf_hub_download(CLIPS_REPO, f"clips/{n}.mp4", repo_type="dataset", token=tok)
        shutil.copy(src, CLIP_DIR / f"{i:02d}_{n}.mp4")
    print(f"BATCH_FETCH\t{len(names)} clips from {CLIPS_REPO}", flush=True)


UPLOAD_TIMEOUT_S = 120
UPLOAD_TRIES = 3


def _upload_result(clip, names, vals, z, shape):
    """Durable upload, bounded: a hung HTTP call must never hang the scoring thread.

    The 6 Sep 10-clip batch stopped dead after clip 6 with the web server still
    answering — consistent with an upload that never returned. So each attempt runs
    in a worker thread and is abandoned after UPLOAD_TIMEOUT_S; up to UPLOAD_TRIES
    attempts, then the failure is logged and scoring continues with the next clip.
    """
    import threading
    tok = os.environ.get("HF_TOKEN")
    if not tok:
        print(f"RESULT_UPLOAD\t{clip}\tSKIPPED\tno HF_TOKEN", flush=True); return
    payload = json.dumps({"clip": clip, "n_parcels": len(names), "timeline_shape": list(shape),
                          "parcels": {n: {"raw": float(vals[i]), "z": float(z[i])}
                                      for i, n in enumerate(names)}}).encode()
    for attempt in range(1, UPLOAD_TRIES + 1):
        outcome = {}
        def work():
            try:
                from huggingface_hub import HfApi
                HfApi().upload_file(path_or_fileobj=payload, path_in_repo=f"results/{clip}.json",
                                    repo_id=RESULTS_REPO, repo_type="dataset", token=tok,
                                    commit_message=f"result: {clip}")
                outcome["ok"] = True
            except Exception as e:
                outcome["err"] = f"{type(e).__name__}: {e}"
        th = threading.Thread(target=work, daemon=True); th.start()
        th.join(UPLOAD_TIMEOUT_S)
        if outcome.get("ok"):
            print(f"RESULT_UPLOAD\t{clip}\tOK\tresults/{clip}.json\tattempt {attempt}", flush=True); return
        why = outcome.get("err", f"timeout after {UPLOAD_TIMEOUT_S}s") if not th.is_alive() else f"timeout after {UPLOAD_TIMEOUT_S}s"
        print(f"RESULT_UPLOAD\t{clip}\tRETRY\tattempt {attempt}: {why}", flush=True)
    print(f"RESULT_UPLOAD\t{clip}\tFAILED\tafter {UPLOAD_TRIES} attempts", flush=True)

# Expected direction per clip, from README.md. Recorded here so the run itself
# carries the prediction rather than us reading it back afterwards.
EXPECTED = {
    "face": "fusiform / face-selective parcels should rank higher than in landscape",
    "crowd": "body and biological-motion parcels; many small faces",
    "landscape": "scene / place parcels (parahippocampal)",
}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else 1.0


def run_probe(mode="video", audio_only=True):
    try:
        return _run_probe(mode, audio_only)
    except Exception:
        return "PROBE FAILED\n\n" + traceback.format_exc()


def _run_probe(mode="video", audio_only=True):
    out = []

    def log(s=""):
        out.append(str(s))
        print(s, flush=True)

    try:
        from tribescore import inference, metrics
    except Exception as e:
        return f"FAILED to import tribescore: {type(e).__name__}: {e}\n\n{traceback.format_exc()}"

    _fetch_batch()
    clips = sorted(CLIP_DIR.glob("*.mp4"))
    if not clips:
        return f"No clips found in {CLIP_DIR}"
    log(f"clips: {[c.name for c in clips]}")
    log(f"mode={mode}  audio_only={audio_only}")

    log("\nloading model ...")
    model = inference.load_model(CACHE)

    # build_roi_masks returns the APP'S 5 COMPOSITE SCORES (Attention, Engagement,
    # Language, Self-relevance, Virality) — not anatomical parcels. Those composites
    # are the "engagement score" family with a published null against real audience
    # retention (r=+0.058), so they are kept only as a secondary readout. The primary
    # readout must be real HCP-MMP1 parcels from tribev2's own helpers.
    log("building composite masks (secondary readout) ...")
    masks = metrics.build_roi_masks(CACHE, mesh="fsaverage5")
    log(f"  {len(masks)} composite masks: {sorted(masks)}")

    log("\nresolving tribev2.utils parcel helpers ...")
    import inspect
    from tribev2 import utils as tu
    log("  (helper signatures suppressed — get_hcp_labels returns a dict)")

    results = {}
    for clip in clips:
        name = clip.stem
        log(f"\n--- {name} ---")
        info = {}
        # audio_only=True skips ASR + Llama-3.2-3B, which is a gated Meta repo.
        # Their own docs call this the path "to validate metrics on-Space before
        # Meta approves Llama"; the model tolerates the missing text modality via
        # modality dropout. For a content probe it also removes dialogue as a
        # confound, which we want anyway.
        # run_inference returns (preds, abs_times) -> Tuple[np.ndarray, np.ndarray].
        # Its docstring: "re-assembles a continuous 1 Hz timeline".
        timeline, abs_times = inference.run_inference(
            model, mode, str(clip), audio_only=audio_only, out_info=info)
        timeline = np.asarray(timeline, dtype="float32")
        abs_times = np.asarray(abs_times, dtype="float32")

        # This settles the disputed prediction rate. 1 Hz per the shipped config;
        # a 1.49 s TR would imply ~0.67 Hz. Record it, do not assume it.
        # Settles the disputed rate: shipped config says 1 Hz, a 1.49s TR would
        # imply ~0.67 Hz. Measured here rather than assumed.
        span = float(abs_times[-1] - abs_times[0]) if abs_times.size > 1 else 0.0
        rate = (timeline.shape[0] - 1) / span if span else float("nan")
        log(f"timeline {timeline.shape}  abs_times {abs_times.shape}  "
            f"span {span:.1f}s  -> {rate:.3f} rows/s")
        log(f"  info={info}")

        # Secondary: the 5 composites, for continuity with the app's own readout.
        comp = {}
        for roi, m in masks.items():
            m = np.asarray(m)
            sel = timeline[:, m.astype(bool)] if m.dtype == bool else timeline[:, m]
            if sel.size:
                comp[roi] = float(sel.mean())
        cz = {k: (v - np.mean(list(comp.values()))) / max(np.std(list(comp.values())), 1e-6)
              for k, v in comp.items()}
        log("  composites: " + ", ".join(f"{k} ({cz[k]:+.2f})"
            for k in sorted(cz, key=cz.get, reverse=True)))

        # PRIMARY: real HCP-MMP1 (Glasser) parcels.
        # get_hcp_labels() returns {parcel_name: np.ndarray of vertex indices},
        # so reduce directly — summarize_by_roi is unnecessary.
        vert_mean = timeline.mean(axis=0)          # (20484,)
        means = {}
        try:
            parcels = tu.get_hcp_labels()
            for pname, idx in parcels.items():
                # Index 0 of the Glasser colortable is "???" — not a brain region.
                # It was silently participating in the z-scoring on the first run.
                if str(pname).strip("? ") == "" or str(pname) == "???":
                    continue
                idx = np.asarray(idx)
                idx = idx[idx < vert_mean.size]
                if idx.size:
                    means[str(pname)] = float(vert_mean[idx].mean())
            log(f"  reduced to {len(means)} HCP parcels")
        except Exception as e:
            log(f"  parcel reduction FAILED ({type(e).__name__}: {e}) — falling back to composites")
            means = dict(comp)

        names = list(means.keys())
        vals = np.array([means[k] for k in names], dtype="float32")

        z = (vals - vals.mean()) / max(vals.std(), 1e-6)
        order = np.argsort(z)[::-1]
        top = [names[i] for i in order[:TOP_K]]
        results[name] = {
            "top": top,
            "top_z": [round(float(z[i]), 3) for i in order[:TOP_K]],
            "shape": list(timeline.shape),
            "expected": EXPECTED.get(name, ""),
        }
        log(f"top {TOP_K}: " + ", ".join(f"{n} ({z[i]:+.2f})" for n, i in zip(top, order[:TOP_K])))
        # The vector goes to the results repo as a file (proven identical to the
        # old stdout path on 6 Sep, max |delta| 5e-7). Per-parcel stdout lines are
        # dropped: 180 lines per clip filled HF's bounded log window by clip 4.
        print(f"PARCELCOUNT\t{name}\t{len(names)}", flush=True)
        _upload_result(name, names, vals, z, timeline.shape)

    # ---- criterion 1, exactly as written before the run ----
    log("\n" + "=" * 64)
    log("CRITERION 1 — separation (mean pairwise top-10 Jaccard < 0.60)")
    log("=" * 64)
    ovs = []
    for a, b in combinations(results, 2):
        j = jaccard(results[a]["top"], results[b]["top"])
        ovs.append(j)
        log(f"  {a:<12} vs {b:<12}  {j:.2f}")
    mean_ov = float(np.mean(ovs)) if ovs else 1.0
    passed = mean_ov < 0.60
    log(f"\n  mean overlap {mean_ov:.2f}  ->  {'PASS' if passed else 'FAIL'}")

    log("\nCRITERION 2 — direction: judge the region names above against")
    log("the expectations printed per clip. Do not soften them afterwards.")
    log("=" * 64)

    payload = {"results": results, "mean_top_k_overlap": mean_ov,
               "criterion_1_separation": passed}
    Path("probe_results.json").write_text(json.dumps(payload, indent=2))
    log("\nwrote probe_results.json")
    return "\n".join(out)


# --- autorun -----------------------------------------------------------------
# ~10 min/clip x 3 clips means the run outlives any client connection, so it is
# started here and its output goes to stdout, readable via the Space logs API.
import threading

def _autorun():
    print("\n" + "#" * 70, flush=True)
    print("# AUTORUN probe: mode=video audio_only=True", flush=True)
    print("#" * 70 + "\n", flush=True)
    _ao = os.environ.get("AUDIO_ONLY", "1") == "1"   # text-branch run sets AUDIO_ONLY=0
    print(f"# AUDIO_ONLY={_ao}", flush=True)
    txt = run_probe("video", _ao)
    print("\n" + "#" * 70, flush=True)
    print("# PROBE OUTPUT BEGIN", flush=True)
    print(txt, flush=True)
    print("# PROBE OUTPUT END", flush=True)
    print("#" * 70, flush=True)

if os.environ.get("AUTORUN", "1") == "1":
    threading.Thread(target=_autorun, daemon=True).start()


with gr.Blocks(title="TRIBE discrimination probe") as demo:
    gr.Markdown(
        "# 00 — Discrimination probe\n"
        "Does TRIBE separate a landscape from a crowd from a face?\n\n"
        "Pass criteria were fixed before this ran: mean pairwise top-10 Jaccard "
        "overlap below 0.60, plus correct direction on at least two clips."
    )
    # Exposed as inputs so variants can be tried without a redeploy —
    # each Space restart costs ~7 minutes of wall clock and billed GPU.
    mode_in = gr.Dropdown(["video", "audio", "text"], value="video", label="mode")
    ao_in = gr.Checkbox(value=True, label="audio_only (skips ASR + gated Llama)")
    btn = gr.Button("Run probe", variant="primary")
    box = gr.Textbox(label="output", lines=34)
    btn.click(run_probe, inputs=[mode_in, ao_in], outputs=box)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
