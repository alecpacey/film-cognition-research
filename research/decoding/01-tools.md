# Decoding activation into cognitive terms

Research date: 2026-09-02. All package versions, repo states, file contents and API
signatures below were verified against PyPI, the GitHub API and raw source on that date.
Claims I could not verify are marked **[UNVERIFIED]**.

---

## Recommendation

**Build a `terms × 180` reference matrix once, in your own fsaverage5 Glasser space, then
decode every clip as a demeaned correlation against it.**

Do *not* try to push your parcel vector "up" into an MNI volume to feed a stock decoder.
That is the obvious move and it is the wrong one, for a reason I verified at source:

> `neuromaps.transforms` provides `mni152_to_fsaverage`, `mni152_to_fslr`,
> `mni152_to_civet` and `mni152_to_mni152`. It provides **no** `fsaverage_to_mni152`.
> I grepped the module: the only function name containing `to_mni` is `mni152_to_mni152`.

The validated registration-fusion bridge between MNI volume and fsaverage surface runs
**volume → surface only**. There is also no canonical volumetric Glasser atlas to paint
into: TemplateFlow has Schaefer2018, DiFuMo and Harvard-Oxford but no HCP-MMP1 (the
`atlas-HCP_dseg` file in `tpl-MNI152NLin6Asym` is the HCP subcortical segmentation, not
MMP1), and nilearn ships no Glasser fetcher at all. Every volumetric HCP-MMP1 NIfTI in
circulation is a third-party derivation of a natively-surface parcellation.

So invert the pipeline. Bring Neurosynth **down** to fsaverage5, parcellate it with *your
own* Glasser labels, and decode entirely in the space your data already lives in.

This is not a compromise. NiMARE's `CorrelationDecoder.transform` is, at source, exactly
this operation:

```python
img_vec = results.masker.transform(img)      # reduce target map to a vector
corrs   = pearson(img_vec, images)           # correlate against each term's vector
```

The masker is just "reduce a map to a vector". Substituting a *parcel-wise* reduction for
a *voxel-wise* one gives you the identical estimator with a coarser, less noisy basis.
You are reimplementing NiMARE's decoder faithfully, not approximating it.

**Five steps:**

1. `fetch_neurosynth(version="7", source="abstract", vocab="terms")` → Studyset
   (verified: 14,371 studies, 3,227 terms).
2. Fit `CorrelationDecoder` on a **curated feature subset** → `{term: MNI152 2mm map}`.
3. Project each term map MNI152 → fsaverage5 with `nilearn.surface.vol_to_surf` (BSD-3).
4. Parcellate with **your own** fsaverage5 Glasser label vector → 180 values/term. Cache.
5. Decode a clip = column-demeaned Pearson correlation of its 180-vector against the matrix.

Steps 1–4 run once (hours). Step 5 is a matrix-vector product — microseconds, so it scales
to your whole clip library.

### Three things that will silently ruin this if you skip them

**1. Your index 0 is not a brain region.** I downloaded and byte-parsed the Glasser
fsaverage `.annot` colortable. It has exactly **181 entries: `???` at index 0, then 180
named parcels** (`L_V1_ROI` … `L_p24_ROI`). Every parcel in your examples resolves —
`VMV2 → L_VMV2_ROI`, `A5 → L_A5_ROI`, `STSdp → L_STSdp_ROI`, `55b → L_55b_ROI`,
`LO2 → L_LO2_ROI`, `FEF → L_FEF_ROI`, `LIPv → L_LIPv_ROI`, `VIP → L_VIP_ROI`,
`V3B`, `V4`, `V4t`, `V7`, `IPS1`, `A4`, `PBelt`, `VMV3` — all real. So your 181 is
**one hemisphere: medial wall + 180 parcels**. Drop index 0 before correlating or you are
correlating against unassigned cortex. It also means you are decoding a single hemisphere;
if you have both, decide explicitly whether to concatenate to 360 or average to 180.

**2. Demean each parcel across terms, or every clip decodes the same.** Neurosynth term
maps are massively correlated with each other — nearly all of them light up the same
task-positive regions, because nearly all fMRI studies do. A raw Pearson correlation is
dominated by this shared mean map, and you will get near-identical rankings for the
landscape clip, the talking-heads clip and the crowd clip. Subtract the across-term mean
from each parcel column first. This is the difference between a decoder that works and a
decoder that outputs "cortex" every time. It is the parcel-space equivalent of why
Neurosynth's association test exists at all.

**3. Use the association map, not the uniformity map.** Covered below — the default is
already correct, just do not change it.

Fitting all 3,227 terms is not realistic. Start with `vocab="LDA200"` topics (200 maps,
already denoised, and topics are more interpretable than raw terms for a film context) or a
curated list of ~150–300 cognitive terms. NiMARE 0.21.0 added `_precompute_meta_estimator_maps`,
which computes study-wise MA maps once and reuses them across features — this makes a
200-feature fit dramatically cheaper than it was in older versions. Pass `n_cores=-1`.

---

## Tool comparison

| tool | what it maps | data size | licence | maintained? | API quality |
|---|---|---|---|---|---|
| **NiMARE** `0.21.0` | coordinates ↔ terms; map→ranked terms; ROI→ranked terms | code only; pulls data below | MIT | **Yes — released 2026-08-31, repo pushed 2026-09-02** | Good. Clean `fit`/`transform`. Docs thin on class lists; read source. **0.21.0 deprecates `Dataset` for `Studyset`** |
| **Neurosynth v7 data** | 14,371 studies × 3,227 terms + coords | ~10 MB features, ~3.6 MB coords, ~1.2 MB metadata | ODbL-1.0 | **Data frozen** — repo last pushed 2021-08-26. NiMARE pins a commit SHA, so fetches are stable | N/A (flat files, fetched by NiMARE) |
| **NeuroQuery** | text query → predicted brain map (encoding, not meta-analysis) | 56 MB model zip | BSD-3 | **repo ARCHIVED**; PyPI `1.1.0` (2025-08-23). **neuroquery.org is live and serving** | Simple, but archived code |
| **Neurosynth Compose** | web platform; curate + run your own meta-analyses | web | — | **Yes — `neurostore` repo pushed 2026-09-02** | Web UI + `pyNS`; not a term decoder |
| **neuromaps** `0.0.7` | volume↔surface transforms, `Parcellater` | small | **CC BY-NC-SA 4.0 — non-commercial** | Yes (pushed 2026-06-13) | Excellent. Best-in-class registration fusion |
| **nilearn** `0.14.0` | `vol_to_surf`, ships fsaverage5 in-package | small | BSD-3 | Yes (2026-07-02) | Excellent |
| **coord2region** `0.1.5` | 3D coords → atlas labels + literature + LLM summaries | small | see repo | Yes (2026-03-13) | New (arXiv 2512.18165). Anatomical labelling + retrieval, **not** a term decoder |

**Licence flag worth raising now:** neuromaps is **CC BY-NC-SA 4.0 — non-commercial**
(verified from its LICENSE file; the GitHub API reports `NOASSERTION`, and PyPI carries the
full CC text). If this film project has any commercial dimension, that is a problem. The
code below therefore uses **nilearn's `vol_to_surf` (BSD-3)** for the volume→surface step.
neuromaps' registration fusion is the better method — use it if the licence is acceptable
to you, but make that call deliberately rather than by accident.

### Neurosynth: forward vs reverse inference

Verified from `nimare/meta/cbma/mkda.py` source, `MKDAChi2`:

```python
pAgF = n_selected_active_voxels / n_selected     # P(Activation | Feature)
pFgA = pAgF * pF / pA                            # P(Feature | Activation)
...
maps = {
    "z_desc-uniformity":  pAgF_z,   # forward inference  — "uniformity test"
    "z_desc-association": pFgA_z,   # reverse inference   — "association test"
}
```

- **Uniformity test** (`z_desc-uniformity`, pAgF, forward): *given studies about this term,
  does this voxel activate consistently?* One-way chi-square. Answers "where does X activate".
  Biased toward regions that activate in almost every task — you will get insula and
  dorsal ACC for nearly everything.
- **Association test** (`z_desc-association`, pFgA, reverse): *given activation here, is
  this term more likely than base rate?* Two-way chi-square against all other studies.
  Answers "what does activation here imply" — **this is the decoding question**, and it is
  what you want.

`CorrelationDecoder`'s default is already `target_image="z_desc-association"`. Leave it.
NiMARE renamed `consistency`→`uniformity` and `specificity`→`association` in 0.2.1 to match
Neurosynth's own terminology, so older tutorials use the old names.

**The standing caveat:** reverse inference from meta-analytic co-occurrence is not
evidence that the region *performs* the function. Neurosynth's "association" is a
text-occurrence statistic over abstracts, inheriting every bias in what neuroimagers choose
to publish and how they word abstracts. Treat outputs as *"this pattern resembles studies
that talk about X"*, not *"this is X processing"*. For a film project that framing is
probably fine and arguably more honest — but do not let the phrasing drift.

### NeuroQuery vs Neurosynth — when to prefer which

NeuroQuery is an **encoding** model: it predicts a brain map from arbitrary text, including
terms too rare for a Neurosynth meta-analysis (Neurosynth needs enough studies per term;
NeuroQuery smooths across a learned semantic space). It is better when you want maps for
unusual or multi-word phrases, or a map for free text.

But you want the **inverse** direction — pattern → terms — which is Neurosynth's native
operation and NiMARE's `CorrelationDecoder`. And the `neuroquery` GitHub repo is
**archived** (as is `neuroquery_data`), though PyPI 1.1.0 was published 2025-08-23 and
neuroquery.org is live and answering queries. Use Neurosynth as primary. NeuroQuery is a
good cross-check: take your top decoded terms, generate NeuroQuery maps for them, and
confirm they resemble your input pattern.

### 2024–2026 successors

Honest answer: **there is no validated successor that replaces Neurosynth decoding.** The
field's active work is in platform and curation, not a new decoding statistic.

- **Neurosynth Compose** (`compose.neurosynth.org`, live; `neurostore` repo pushed
  2026-09-02) is the real successor *platform* — curate study sets, run meta-analyses in
  the browser, backed by NiMARE. It modernises how you *build* a meta-analysis; it does not
  give you a new pattern→terms decoder.
- **coord2region** (arXiv 2512.18165, Dec 2025; PyPI 0.1.5, Mar 2026) maps coordinates to
  atlas labels and retrieves literature with LLM summaries. Genuinely new and interesting,
  but it is anatomical labelling plus retrieval, not meta-analytic decoding. Possibly useful
  as a *narration* layer on top of your decoded terms.
- Text–brain contrastive models (e.g. NeuroConText-style work) exist but I found no
  maintained, installable package with validated decoding performance. **[UNVERIFIED]** —
  my web search budget was exhausted this session, so I could not survey the 2024–2026
  literature as broadly as I would like. Treat this bullet as incomplete rather than as a
  negative finding.

NiMARE 0.21.0 shipping two days ago, with active decoder work in it, is the strongest
signal available: the maintained path in 2026 is still NiMARE + Neurosynth v7.

---

## Getting parcel data in

This is the crux, so here it is explicitly.

**What does not work, and why:**

| route | verdict |
|---|---|
| Paint 181 values into a volumetric Glasser, feed to `CorrelationDecoder` | **Blocked.** No canonical volumetric HCP-MMP1 exists — not in TemplateFlow, not in nilearn. Third-party NIfTIs vary in provenance and quality |
| Project fsaverage5 → MNI152 with neuromaps, then decode | **Impossible.** neuromaps has no `fsaverage_to_mni152`. Registration fusion is volume→surface only (verified by grep) |
| Top-k parcels → binary ROI → `ROIAssociationDecoder` | **Blocked for the same reason.** Verified at source: `_fit` calls `kernel_transformer.transform(coords, self.masker, return_type="array")` — it needs a *volumetric* masker. Also throws away your continuous values, keeping only membership |

**What works — bring the terms to your data:**

```
Neurosynth v7 Studyset (14,371 studies, 3,227 terms)
   │  CorrelationDecoder.fit(studyset)   [curated feature subset]
   ▼
{term: MNI152 2mm association map}       decoder.results_.maps
   │  masker.inverse_transform → Nifti1Image
   ▼
{term: Nifti1Image}
   │  nilearn.surface.vol_to_surf(img, fsaverage5 pial)   [BSD-3]
   ▼
{term: fsaverage5 surface, 10242 verts/hemi}
   │  average within each Glasser parcel, using YOUR label vector
   ▼
REFERENCE MATRIX  (n_terms, 180)   ←── cache this to .npz, it is the deliverable
   │
   │  demean each parcel column across terms
   ▼
your clip's 180-vector ──► Pearson ──► ranked terms
```

**The one rule that makes it correct:** use **your own** fsaverage5 Glasser label vector on
both sides. The term-side reduction and the data-side reduction must use bit-identical
parcel definitions. If you parcellate the term maps with a freshly-downloaded annot while
your TRIBE output used a differently-resampled one, parcel *k* means different cortex on
each side and the correlation is garbage in a way that will not throw an error. You already
have this label vector — TRIBE produced 181 values with it. Reuse it. Do not re-derive it.

**If you need to reconstruct the labels:** the canonical source is Kathryn Mills,
*"HCP-MMP1.0 projected on fsaverage"*, figshare 3498446, **CC BY 4.0** — verified live via
the figshare API, providing `lh.HCP-MMP1.annot` and `rh.HCP-MMP1.annot` (1.32 MB each).
Caveat: these are **fsaverage (163,842 vertices)**, not fsaverage5 (10,242). FreeSurfer's
fsaverage meshes are nested icosahedral subdivisions, so fsaverage5 vertices are the first
10,242 of fsaverage — `labels[:10242]` downsamples correctly. This is corroborated by
nilearn's own `_resort_vertices` helper, whose docstring resorts higher-density meshes
"to have their vertices in the same order as fsaverage5". If you want belt-and-braces, use
FreeSurfer `mri_surf2surf --trgsubject fsaverage5` instead. **Best option remains: use the
labels you already have.**

---

## Worked example

Two scripts. The first is the expensive one-off build; the second is the per-clip decode.

### Part 1 — build the reference matrix (run once)

```python
"""
build_reference.py — Neurosynth term maps → (n_terms, 180) Glasser/fsaverage5 matrix.

Verified against: nimare 0.21.0, nilearn 0.14.0, nibabel 5.4.2 (PyPI, 2026-09-02).

    pip install "nimare==0.21.0" "nilearn==0.14.0" nibabel numpy
"""
import numpy as np
import nibabel as nib
from nimare.extract import fetch_neurosynth
from nimare.decode.continuous import CorrelationDecoder
from nilearn.datasets import fetch_surf_fsaverage
from nilearn.surface import vol_to_surf

# ---------------------------------------------------------------- 1. Neurosynth
# Verified signature: fetch_neurosynth(data_dir=None, version="7", overwrite=False,
#                                      return_type="studyset", target="mni152_2mm", **kwargs)
# 0.21.0 returns a Studyset by default; Decoder.fit() accepts Studyset or Dataset.
studysets = fetch_neurosynth(version="7", source="abstract", vocab="terms")
studyset = studysets[0]
print(f"{len(studyset.ids)} studies")          # 14371

# ---------------------------------------------------------------- 2. term maps
# Fitting all 3,227 terms is not tractable. Curate. Swap in your own list, or use
# vocab="LDA200" / type="weight" above for 200 pre-denoised topics instead.
TERMS = [
    "faces", "face", "speech", "auditory", "language", "voice", "semantic",
    "scene", "place", "navigation", "spatial", "landmark", "memory",
    "motion", "visual", "object", "attention", "eye movements", "saccades",
    "biological motion", "action observation", "social", "mentalizing",
    "emotion", "reward", "salience", "working memory", "executive",
]

decoder = CorrelationDecoder(
    feature_group="terms_abstract_tfidf",
    features=TERMS,
    frequency_threshold=0.001,
    target_image="z_desc-association",   # association = reverse inference. Do not change.
    n_cores=-1,                          # 0.21.0 precomputes MA maps once and reuses them
)
decoder.fit(studyset)

masker = decoder.results_.masker
term_maps = {t: masker.inverse_transform(v) for t, v in decoder.results_.maps.items()
             if v is not None}
print(f"{len(term_maps)} term maps generated")

# ---------------------------------------------------------- 3. MNI152 -> fsaverage5
# nilearn is BSD-3. neuromaps' mni152_to_fsaverage(img, '10k') is the better
# (registration-fusion) method but is CC BY-NC-SA — non-commercial.
fs5 = fetch_surf_fsaverage("fsaverage5")

def to_fs5(img):
    """Project an MNI152 volume onto both fsaverage5 hemispheres."""
    lh = vol_to_surf(img, fs5["pial_left"],  interpolation="linear")
    rh = vol_to_surf(img, fs5["pial_right"], interpolation="linear")
    return np.nan_to_num(lh), np.nan_to_num(rh)   # 10242 each

# ------------------------------------------------------------- 4. parcellate
# CRITICAL: this must be the SAME label vector TRIBE used. Load yours here.
#   labels = np.load("glasser_fs5_labels_lh.npy")   # (10242,), ints 0..180, 0 = ???
# Reconstruction fallback (figshare 3498446, CC BY 4.0), fsaverage -> fsaverage5:
#   full, ctab, names = nib.freesurfer.read_annot("lh.HCP-MMP1.annot")
#   labels = full[:10242]
labels = np.load("glasser_fs5_labels_lh.npy")

PARCEL_IDS = np.arange(1, 181)      # 1..180. Index 0 is '???' (medial wall) — EXCLUDED.

def parcellate(surf, labels):
    """Mean surface value within each of the 180 parcels."""
    return np.array([
        surf[labels == pid].mean() if np.any(labels == pid) else 0.0
        for pid in PARCEL_IDS
    ])

terms, rows = [], []
for term, img in term_maps.items():
    lh, _rh = to_fs5(img)           # left hemisphere, matching your 181-vector
    rows.append(parcellate(lh, labels))
    terms.append(term)

R = np.vstack(rows)                 # (n_terms, 180)
np.savez_compressed("neurosynth_glasser_fs5.npz", matrix=R, terms=np.array(terms))
print("reference matrix:", R.shape)
```

### Part 2 — decode a clip

```python
"""
decode.py — 181-value TRIBE parcel vector -> ranked cognitive terms.
"""
import numpy as np

d = np.load("neurosynth_glasser_fs5.npz", allow_pickle=True)
R, TERMS = d["matrix"], d["terms"]          # (n_terms, 180), (n_terms,)

# THE step that makes decoding discriminative rather than returning "cortex" every time.
# Neurosynth term maps are all mutually correlated; remove the shared mean map.
R_c = R - R.mean(axis=0, keepdims=True)


def decode(parcel_vector, top_k=10):
    """parcel_vector: length 181 from TRIBE (index 0 = '???' medial wall) or 180."""
    v = np.asarray(parcel_vector, dtype=float)
    if v.shape[0] == 181:
        v = v[1:]                            # drop '???' — verified: annot index 0
    assert v.shape[0] == 180, f"expected 180 parcels, got {v.shape[0]}"

    v = v - v.mean()
    num = R_c @ v
    den = np.linalg.norm(R_c, axis=1) * np.linalg.norm(v)
    r = np.divide(num, den, out=np.zeros_like(num), where=den > 0)

    order = np.argsort(-r)[:top_k]
    return [(str(TERMS[i]), float(r[i])) for i in order]


# --- made-up parcel vector, built from the measured top parcels of your crowd clip ---
GLASSER = {  # 1-based parcel ids; look these up once from your annot's colortable
    "LO2": 21, "V4t": 156, "V7": 16, "IPS1": 17, "FEF": 10, "LIPv": 48, "VIP": 49,
}
demo = np.random.default_rng(0).normal(0, 0.4, 181)   # background noise
demo[0] = 0.0                                          # '???' is not a region
for name, val in [("LO2", 2.43), ("V4t", 2.10), ("V7", 1.95),
                  ("IPS1", 1.80), ("FEF", 1.72), ("LIPv", 1.65), ("VIP", 1.58)]:
    demo[GLASSER[name]] = val

for term, r in decode(demo):
    print(f"{term:22s} r = {r:+.3f}")
```

**Sanity checks before you trust any output.** Decode your three measured clips and confirm
the rankings *differ* and move in the expected direction — the landscape clip (VMV2, VMV3,
V3B, V4: ventromedial visual, scene-selective cortex) should rank *scene*, *place*,
*navigation* highly; the talking-heads clip (A5, STSdp, 55b, A4, PBelt: auditory belt and
superior temporal sulcus) should rank *speech*, *auditory*, *voice*, *language*; the crowd
clip (LO2, V4t, V7, IPS1, FEF, LIPv, VIP: lateral occipital and dorsal attention) should
rank *motion*, *attention*, *biological motion*. If all three return the same terms, you
skipped the demeaning. If none of them make sense, your label vector is misaligned between
the two sides.

---

## Sources

Verified live on 2026-09-02 unless noted.

1. [NiMARE on PyPI](https://pypi.org/project/nimare/) — v0.21.0, MIT, uploaded 2026-08-31, requires-python ≥3.10.
2. [neurostuff/NiMARE](https://github.com/neurostuff/NiMARE) — 211 stars, pushed 2026-09-02, not archived, MIT.
3. [NiMARE `decode/discrete.py`](https://github.com/neurostuff/NiMARE/blob/main/nimare/decode/discrete.py) — source for `BrainMapDecoder`, `NeurosynthDecoder`, `ROIAssociationDecoder` signatures.
4. [NiMARE `decode/continuous.py`](https://github.com/neurostuff/NiMARE/blob/main/nimare/decode/continuous.py) — `CorrelationDecoder` signature, `load_imgs`, and the `transform` correlation source quoted above.
5. [NiMARE `decode/base.py`](https://github.com/neurostuff/NiMARE/blob/main/nimare/decode/base.py) — `Decoder.fit()` accepts `Studyset` **or** `Dataset`.
6. [NiMARE `meta/cbma/mkda.py`](https://github.com/neurostuff/NiMARE/blob/main/nimare/meta/cbma/mkda.py) — `pAgF`/`pFgA` definitions and the `z_desc-uniformity` / `z_desc-association` map naming (lines ~495–575).
7. [NiMARE `extract/extract.py`](https://github.com/neurostuff/NiMARE/blob/main/nimare/extract/extract.py) — `fetch_neurosynth` signature, valid `source`/`vocab`/`type` combinations, and the pinned data commit `209c33cd`.
8. [NiMARE decoding example](https://github.com/neurostuff/NiMARE/blob/main/examples/04_decoding/01_plot_discrete_decoders.py) — canonical `Studyset` → `fit` → `transform` flow.
9. [NiMARE releases](https://github.com/neurostuff/NiMARE/releases) — 0.21.0 deprecates `Dataset` for `Studyset`; discrete-decoder correction default changed `"fdr_bh"` → `"bh"`.
10. [NiMARE API docs](https://nimare.readthedocs.io/en/stable/api.html) — module-level descriptions of `decode.discrete` / `decode.continuous` / `decode.encode`.
11. [neurosynth/neurosynth-data](https://github.com/neurosynth/neurosynth-data) — ODbL-1.0, default branch `master`, last pushed 2021-08-26 (data frozen).
12. Neurosynth v7 metadata, downloaded and counted directly: **14,371 studies**; v7 term vocabulary, downloaded and counted: **3,227 terms**. LDA50/100/200/400 topic vocabularies also present for v6 and v7.
13. [neuroquery/neuroquery](https://github.com/neuroquery/neuroquery) — **archived**, BSD-3. [PyPI `neuroquery` 1.1.0](https://pypi.org/project/neuroquery/), uploaded 2025-08-23. [neuroquery.org](https://neuroquery.org) — live, HTTP 200.
14. [neuroquery/neuroquery_data](https://github.com/neuroquery/neuroquery_data) — **archived**, 56 MB model.
15. [compose.neurosynth.org](https://compose.neurosynth.org) — live. [neurostuff/neurostore](https://github.com/neurostuff/neurostore) — pushed 2026-09-02.
16. [netneurolab/neuromaps](https://github.com/netneurolab/neuromaps) — 341 stars, pushed 2026-06-13. LICENSE file is **CC BY-NC-SA 4.0**. `transforms.py` grepped: no `fsaverage_to_mni152`.
17. [neuromaps `parcellate.py`](https://github.com/netneurolab/neuromaps/blob/main/neuromaps/parcellate.py) — `Parcellater(parcellation, space, resampling_target, hemi)`.
18. [nilearn on PyPI](https://pypi.org/project/nilearn/) — 0.14.0, BSD-3, 2026-07-02. `surface.py::vol_to_surf`, `struct.py::fetch_surf_fsaverage` (default `"fsaverage5"`, shipped in-package).
19. [Mills, K. "HCP-MMP1.0 projected on fsaverage", figshare 3498446](https://figshare.com/articles/dataset/HCP-MMP1_0_projected_on_fsaverage/3498446) — CC BY 4.0, published 2016-07-25. Verified via figshare API; `lh`/`rh.HCP-MMP1.annot`, 1.32 MB each.
20. Glasser annot colortable parsed byte-wise from the file above: 163,842 vertices, **181 colortable entries — `???` at index 0 plus 180 named parcels**; all 16 of the parcel names in the brief resolved.
21. TemplateFlow repos `tpl-MNI152NLin6Asym`, `tpl-MNI152NLin2009cAsym`, `tpl-fsLR`, `tpl-fsaverage` queried via GitHub API — **no Glasser/HCP-MMP1 parcellation**. nilearn `datasets/atlas.py` grepped — no Glasser fetcher.
22. [Coord2Region, arXiv:2512.18165](https://arxiv.org/abs/2512.18165) (Dec 2025); [PyPI `coord2region` 0.1.5](https://pypi.org/project/coord2region/) (2026-03-13); [BabaSanfour/Coord2Region](https://github.com/BabaSanfour/Coord2Region).
23. Yarkoni et al. (2011), *Large-scale automated synthesis of human functional neuroimaging data*, Nat Methods — the Neurosynth method, cited in NiMARE's decoder docstrings.
24. Wager et al. (2007) — the MKDA chi-square method underlying `MKDAChi2`, cited in NiMARE source.

### Caveat on coverage

My web-search budget for this session was exhausted before I began, so this report is built
entirely from **primary sources** — package registries, the GitHub API, raw source files,
and files I downloaded and parsed myself. That makes the technical claims here unusually
well-grounded (I read the code rather than a tutorial about the code), but it means I could
not survey community discussion, blog posts, or the 2024–2026 literature broadly. The one
place this bites is the "newer successors" question: absence of evidence there is not
evidence of absence. If that section matters, it is worth a dedicated pass with search
available.
