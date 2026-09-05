# Experiments

Where the tests are run and where the results are kept. One directory per
experiment, numbered in the order they gate each other — each one is allowed to
kill the ones after it.

```
experiments/
  LOG.md              running log, newest first. Every run gets a line.
  00-probe/           does TRIBE discriminate content at all?
    README.md         hypothesis, method, pass criteria — written BEFORE running
    probe.py          the script
    clips/            input videos (gitignored — source your own)
    out/              raw predictions (gitignored — large)
    RESULT.md         what happened (committed)
```

## The rule

**Pass criteria are written before the run, not after.** Every experiment's
README states what result would falsify it. This matters more than usual here:
TRIBE returns plausible-looking numbers for inputs it cannot handle, so
"the output looked reasonable" is not evidence of anything.

## What gets committed

| Committed | Not committed |
|---|---|
| scripts, READMEs, RESULT.md, derived summaries (JSON/CSV under ~1 MB) | input video, raw `(T, 20484)` prediction arrays, model weights, fMRI volumes |

Raw predictions for one 30 s clip are ~2.5 MB of float32 and there will be
thousands. Keep them local, commit the reductions.

## Where these run

TRIBE needs ~13 GB VRAM (not the 28–32 GB widely quoted — the extractors are
freed after each is cached) and CUDA. This machine is an Apple M4 with MPS and
no CUDA, so the options are, cheapest first:

1. **The existing public Space** — `techfreakworm/tribev2-brain-timeline` is a
   working deployment on ZeroGPU. Free, zero setup. Try this before paying for anything.
2. **Duplicate that Space** to a dedicated L40S, ~$1.80/hr. The install traps are
   already solved inside it.
3. **RunPod A6000 48 GB**, ~$0.33/hr community pricing. Cheapest per hour, most setup.
4. **Local MPS** — a stretch. Needs a Python 3.11/3.12 venv (`numpy==2.2.6` has no
   3.14 wheels) and V-JEPA-2 on MPS is untested. Worth one attempt because it is free.

## Install, wherever it runs

```sh
# upstream main does not import — exca is left unpinned and a removed API breaks it
pip install "git+https://github.com/facebookresearch/tribev2@refs/pull/67/head"
export HF_HUB_DOWNLOAD_TIMEOUT=300 HF_HUB_HTTP_TIMEOUT=300
```

Video-only inference skips the Llama-3.2-3B branch entirely, which also skips
the gated Meta licence and the `HF_TOKEN` requirement. Use it unless you
specifically need the text branch.
