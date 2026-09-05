# What the HCP parcels mean

Research date: 2026-09-02. Scope: the 24 HCP-MMP1 (Glasser 2016) parcels observed in our TRIBE v2 output.

**Method note / limitation.** This session's web-search budget was exhausted before research began, so nothing here comes from a search-engine sweep. Everything below was obtained by directly retrieving and parsing primary sources: the Nature supplementary PDF, the CAB-NP repository, the `hcp-utils` vertex data, the EBRAINS/siibra REST API, the GitHub repository-search API, and the NCBI E-utilities API. That makes the positive findings solid (each was downloaded and parsed here) but makes the *negative* finding in the next section — "no off-the-shelf function annotation exists" — less than exhaustive. GitHub **code** search requires auth and was not run.

## Is there a machine-readable annotation?

**No. There is no released file that maps HCP-MMP1 parcel name to cognitive function.** What exists is a set of machine-readable *network* and *naming* files that you join yourself, plus a 97-page PDF of prose that describes borders rather than functions.

Three things that are machine-readable, all verified downloaded and parsed in this session:

**1. CAB-NP — parcel to functional network. This is the real answer to "is there a table".**
Ji et al. 2019, *NeuroImage* ([PMID 30291974](https://pubmed.ncbi.nlm.nih.gov/30291974/)); repo <https://github.com/ColeLab/ColeAnticevicNetPartition>.

- File: `CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR_LabelKey.txt`
- Raw URL: `https://raw.githubusercontent.com/ColeLab/ColeAnticevicNetPartition/master/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR_LabelKey.txt`
- Format: tab-separated, 718 rows (360 cortical + 358 subcortical), header row, **CRLF line endings — strip `\r` or your parse silently fails.**
- Columns: `INDEX, KEYVALUE, LABEL, RED, GREEN, BLUE, ALPHA, HEMISPHERE, NETWORK, NETWORKKEY, NETWORKSORTEDORDER, GLASSERLABELNAME`
- Join key: `GLASSERLABELNAME`, formatted `L_V1_ROI` / `R_STSdp_ROI`.
- 12 networks: Visual1, Visual2, Somatomotor, Cingulo-Opercular, Dorsal-Attention, Language, Frontoparietal, Auditory, Default, Posterior-Multimodal, Ventral-Multimodal, Orbito-Affective.
- Also ships `.dlabel.nii`, `.mat` and a plain `cortex_subcortex_parcel_network_assignments.txt` vector.

This is the file to use. It is the only one that names a **Language** network, which matters a lot for our parcels (55b, A5, STSdp, IFJa all land there).

**2. Glasser 2016 Supplementary Neuroanatomical Results — the authoritative per-parcel document, but PDF prose.**
Direct download, verified 200/`application/pdf`/13.5 MB, no login:
`https://static-content.springer.com/esm/art%3A10.1038%2Fnature18933/MediaObjects/41586_2016_BFnature18933_MOESM330_ESM.pdf`
97 pages, extracts cleanly with `pdftotext -layout`. Contains:
- 22 numbered region sections, each with a functional preamble;
- **Supplemental Table 1** at the end: parcel index, brief name, full name, "New?" flag, section numbers, **"Other Names" (synonyms)**, and key studies.

The "Other Names" column is the single most useful thing in the document for our purpose, because it bridges Glasser's names to the functional literature: it is how you learn that PIT *is* the occipital face area, VMV2 *is* PHC1, V8 *is* VO1. The prose itself describes how each area differs from its neighbours (myelin, thickness, connectivity, task contrast), **not what the area does** — it is a border-delineation document. Do not mine it for function counts; a task contrast is mentioned there because it was diagnostic at a boundary, not because it is the area's preferred stimulus.

**3. `hcp-utils` — vertex-level maps that let you compute network overlap yourself.**
<https://github.com/rmldj/hcp-utils>, files under `hcp_utils/data/`: `mmp_1.0.npz`, `yeo7.npz`, `yeo17.npz`, `ca_network_1.1.npz`. All are `.npz` with keys `map_all` (91282 grayordinates), `labels`, `ids`, `rgba`, all on the same fs_LR 32k grayordinate space — so a per-parcel Yeo7/Yeo17 assignment is a `Counter` over `map_all`. The Yeo columns in the table below were computed this way, not copied from anywhere.

**Things that do not exist / were checked and came back empty:**

- **EBRAINS / siibra / Julich-Brain do not host HCP-MMP1.** Queried `https://siibra-api-stable.apps.hbp.eu/v3_0/parcellations`; the registry returns Julich-Brain v1.18–v3.1, DiFuMo, Desikan-Killiany, HarvardOxford, von Economo–Koskinas, MarsAtlas, and various animal atlases. Zero hits for "Glasser", "MMP", or "multi-modal parcellation". So the EBRAINS functional/receptor annotations are not reachable for these parcels without a cross-atlas mapping step.
- **No Cognitive Atlas linkage** at parcel level was found.
- **GitHub repository search** for `HCP-MMP1 functional annotation`, `glasser 360 parcel labels`, `HCP-MMP neurosynth decoding` returned nothing; `glasser parcellation` returns 3 repos, all geometry/format conversion, no annotations.
- No HuggingFace dataset found (not searchable without web search this session — treat as unchecked rather than absent).

**Practical recommendation:** there is nothing to download, so build it. `parcel-annotations.csv` sits next to this file — 24 rows, the parcels we actually observe, with Glasser index, full name, region, synonyms, CAB-NP network per hemisphere, computed Yeo7 majority with percentage, film bucket, and an evidence grade. If we later want all 360, the generator is: CAB-NP label key (join on `GLASSERLABELNAME`) + Supplemental Table 1 (OCR/parse the PDF for full names and synonyms) + a `hcp-utils` overlap computation for Yeo.

## Network assignments

Glasser's own grouping is 22 regions, defined in the Supplementary Neuroanatomical Results as "geographically contiguous areas that can be seen in their entirety from a single viewing perspective," which "often share common properties, based on architecture, task-fMRI profiles, and/or functional connectivity." Region membership below was confirmed against each section's opening paragraph, which enumerates its constituent areas — not inferred.

CAB-NP columns are read directly from the label key. Yeo7 columns are computed here as the majority label across each parcel's grayordinates, with the majority percentage, so you can see where a parcel is genuinely split.

| Parcel | Glasser region (§) | CAB-NP L | CAB-NP R | Yeo7 L (majority %) | Yeo7 R (majority %) |
|---|---|---|---|---|---|
| V4 | Early Visual Cortex (§2) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| V3B | Dorsal Stream Visual (§3) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| V7 | Dorsal Stream Visual (§3) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| V6A | Dorsal Stream Visual (§3) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| IPS1 | Dorsal Stream Visual (§3) | Visual2 | Visual2 | **Dorsal Attention 62%** (Visual 38%) | **Visual 53%** (DorsAttn 47%) |
| V8 | Ventral Stream Visual (§4) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| PIT | Ventral Stream Visual (§4) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| VMV2 | Ventral Stream Visual (§4) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| VMV3 | Ventral Stream Visual (§4) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| V3CD | MT+ Complex (§5) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| LO2 | MT+ Complex (§5) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| V4t | MT+ Complex (§5) | Visual2 | Visual2 | Visual 100% | Visual 100% |
| FEF | Premotor Cortex (§8) | Cingulo-Opercular | Cingulo-Opercular | Dorsal Attention 73% | Dorsal Attention 51% (VentAttn 30%) |
| PEF | Premotor Cortex (§8) | Dorsal-Attention | Cingulo-Opercular | Dorsal Attention 90% | Dorsal Attention 76% |
| 55b | Premotor Cortex (§8) | **Language** | **Language** | **Default 30% / Somatomotor 26%** | **VentAttn 44% / Frontoparietal 35%** |
| PBelt | Early Auditory Cortex (§10) | Auditory | Auditory | Somatomotor 100% | Somatomotor 100% |
| A4 | Auditory Association (§11) | Auditory | Auditory | Somatomotor 100% | Somatomotor 100% |
| A5 | Auditory Association (§11) | **Language** | **Language** | Somatomotor 57% (Default 42%) | Somatomotor 91% |
| STSdp | Auditory Association (§11) | **Language** | **Language** | **Default 100%** | Default 87% |
| LIPv | Superior Parietal (§16) | Visual2 | Visual2 | Dorsal Attention 100% | Dorsal Attention 94% |
| VIP | Superior Parietal (§16) | Visual2 | Visual2 | Dorsal Attention 100% | Dorsal Attention 100% |
| IP0 | Inferior Parietal (§17) | Dorsal-Attention | Dorsal-Attention | Visual 55% (DorsAttn 45%) | Dorsal Attention 51% (Visual 49%) |
| IFJa | Inferior Frontal (§21) | **Language** | **Language** | Frontoparietal 95% | Frontoparietal 89% |
| IFSp | Inferior Frontal (§21) | **Language** | Frontoparietal | Frontoparietal 88% | Frontoparietal 96% |

**Read the Yeo7 column with suspicion, and prefer CAB-NP.** Yeo's 7-network solution has no language network, so it has nowhere sensible to put our speech and voice parcels: it dumps A4 and PBelt into "Somatomotor" (they are auditory, not motor — Yeo's somatomotor network simply absorbs the perisylvian sensory strip), splits A5 between Somatomotor and Default, and fails outright on 55b, which has no majority label in either hemisphere and lands on different networks left versus right. CAB-NP, derived on the HCP-MMP1 grid itself rather than resampled onto it, assigns all four to Language and is the more trustworthy column for exactly the parcels we care most about.

Note also that CAB-NP puts LIPv and VIP in **Visual2** while Yeo7 puts them in Dorsal Attention at 94–100%. That is a genuine disagreement about where the visual-to-attention boundary falls in the intraparietal sulcus, not a bug in either. For our purposes both readings support "attention/scanning".

## Per-parcel function

Evidence grades: **Strong** = well-established function for this exact territory across many independent labs. **Moderate** = the territory is well studied but Glasser's parcel is a newly-drawn subdivision of it, so the mapping from literature to parcel is an inference. **Thin** = area newly defined in 2016 with little independent literature. **Contested** = active disagreement in the field. The "New?" flag is Glasser's own from Supplemental Table 1.

| Parcel | Plain-language function (filmmaker-usable) | Evidence | Source |
|---|---|---|---|
| **V4** | Colour and shape. Where hue, texture and contour get bound into surfaces you could point at. The biggest single lever on how a frame's palette and rendering read. | Strong | Glasser Table 1 (synonyms hOC4v, hOC4lp); large independent literature on human V4 colour/form |
| **V8** | Colour, one stage on from V4 — colour as a property of a thing, not of a patch of light. | Contested | Glasser Table 1 synonym VO1; Hadjikhani et al. 1998 proposed V8 as a colour centre, but the field largely folded this into VO1/VO2. Flagged below |
| **VMV3** | Ventral colour-and-surface map. Sits on the road between "what colour is that" and "what kind of place is this". | Moderate | Glasser Table 1 synonym VO2 (Winawer 2011); VO1/VO2 retinotopy well established, this parcel's boundaries are new |
| **VMV2** | **Place.** Part of the parahippocampal strip that answers to rooms, landscapes and built environment rather than to people. If you want a "scene" dial, this is it. | Moderate | Glasser Table 1 synonym PHC1 (Arcaro et al. 2009, *J Neurosci*, [PMID 19710316](https://pubmed.ncbi.nlm.nih.gov/19710316/); Wang et al. 2015). PHC1/PHC2 overlap the parahippocampal place area |
| **PIT** | **Face parts.** The occipital face area — eyes, mouth, the pieces of a face, before you know whose face it is. | Strong | Glasser Table 1 gives "OFA" as a synonym and cites Kanwisher & Yovel 2006 and Tsao et al. 2008 as key studies for this parcel |
| **LO2** | Object shape. Where a silhouette becomes a thing with an edge and a volume. | Strong | Glasser Table 1 synonym LO1/hOC4la, key study Larsson & Heeger 2006, *J Neurosci* ([PMID 17182764](https://pubmed.ncbi.nlm.nih.gov/17182764/)) |
| **V4t** | The motion belt wrapping the MT complex — moving contours, moving limbs. | Moderate | Glasser §5 places it inside the MT+ complex, whose motion role is very well established; the parcel itself is a subdivision |
| **V3CD** | Transitional motion-and-shape patch between early vision and the motion complex. Honestly, the least well characterised area in our set. | Thin | New in Glasser 2016; Table 1 lists three conflicting synonyms (V3A, V3B, hOC4la) — i.e. previous authors did not agree this territory was one thing |
| **V3B** | Early dorsal map: where things are and how they are moving, before you know what they are. | Strong | Glasser §3 "Dorsal Stream Visual Cortex", described as "implicated in perceiving where visual stimuli are located and in planning visually guided actions… rather than object identification" |
| **V6A** | **Wide-field flow.** Registers the whole visual field sweeping past — the bodily sense of travelling through a space. Also involved in reaching to things you can see. | Strong | Glasser §3; Pitzalis et al. 2015, *Vis Neurosci*, "The human cortical areas V6 and V6A" ([PMID 26241369](https://pubmed.ncbi.nlm.nih.gov/26241369/)) |
| **V7** | First of the parietal attention maps. A spatial index of where in the frame to look next. | Strong | Glasser Table 1 synonym IPS0 (Wang et al. 2015); retinotopic attention maps of IPS well established |
| **IPS1** | Attention map. Holds which part of the frame is currently being prioritised. | Strong | Glasser §3; standard IPS1 retinotopic attention map |
| **LIPv** | **The "what next" list for the eyes.** A ranked map of which bits of the frame are worth a look — a priority map, not a picture. | Strong | Glasser Table 1 synonym hIP3 (Scheperjans et al. 2008); macaque LIP priority-map literature is deep |
| **VIP** | **Am I moving, or is the world?** Handles looming, camera movement, and the space right around the face. Fires for things coming at you. | Moderate–Strong | Glasser §16; human VIP homology: Prog Neurobiol 2022 ([PMID 34775040](https://pubmed.ncbi.nlm.nih.gov/34775040/)); object- vs self-motion: NeuroImage 2020 ([PMID 32112961](https://pubmed.ncbi.nlm.nih.gov/32112961/)); parietal face area: Sereno, NeuroImage 2017 ([PMID 28889002](https://pubmed.ncbi.nlm.nih.gov/28889002/)) |
| **IP0** | Junction between the moving-image maps and the attention maps. Newly cut; treat as an attention parcel with a wide error bar. | Thin | New in Glasser 2016; §17 says only "Area IP0 is a new area posterior to IP1 along the lateral bank of the posterior IPS". Not mentioned at all in the Assem 2020 multiple-demand mapping |
| **FEF** | **The command to move the eyes**, and the volume knob on spatial attention. Goes up when the viewer is actively hunting the frame. | Strong | Glasser §8 identifies FEF as a "moderately myelinated eye field"; frontal eye field function is one of the best-established facts in the field |
| **PEF** | The second eye-movement field, sitting lower on the precentral gyrus. Works alongside FEF; shares its connectivity pattern. | Moderate | Glasser §8: "two moderately myelinated eye fields, the Frontal Eye Field (FEF) and the Premotor Eye Field (PEF)… The eye fields share similar patterns of functional connectivity"; Amiez & Petrides 2009 |
| **PBelt** | Third ring out from the primary hearing core. Complex sound — the timbre of a voice, the size of a room, the grain of a texture. | Strong | Glasser §10 Early Auditory Cortex; core/belt/parabelt hierarchy is standard primate auditory anatomy |
| **A4** | Second-stage hearing: past raw frequency, into sound *objects* — a voice, a door, a car. | Moderate–Strong | Glasser §11; Table 1 synonym TE3 (Morosan et al. 2005). Parcel boundaries new, territory well studied |
| **A5** | Where sound starts becoming speech-shaped. | Moderate | New in Glasser 2016. §11 defines the whole auditory association region as the cortex "activated in the LANGUAGE STORY, MATH, and STORY-MATH contrasts", strongly connected to inferior frontal areas 44/45/47l. CAB-NP assigns it to Language |
| **STSdp** | **The social channel.** Voices, moving mouths, eyes, bodies — anything carrying the signal that there is another mind present. | Moderate–Strong | New name in Glasser 2016, but posterior STS territory is heavily studied: voice-selective areas, Belin et al. 2000 *Nature* ([PMID 10659849](https://pubmed.ncbi.nlm.nih.gov/10659849/)); people-selectivity and audiovisual integration, *Cortex* 2014 ([PMID 23988132](https://pubmed.ncbi.nlm.nih.gov/23988132/)). CAB-NP: Language; Yeo7: Default 100% left |
| **55b** | **Speech planning.** A small, lightly-myelinated patch wedged between the two eye fields that lights up for narrative language; damage to it causes apraxia of speech. Individually variable — it moves between people. | Strong for the function, but see the variability flag | Glasser §8: 55b is "a lightly myelinated isthmus" separating FEF and PEF, whose connectivity "differs markedly" from theirs, and is more activated in the LANGUAGE STORY contrast than its neighbour PEF. Clinical: *Front Neurol* 2021 ([PMID 33776898](https://pubmed.ncbi.nlm.nih.gov/33776898/)); *Neurosurgery* 2020 ([PMID 32097489](https://pubmed.ncbi.nlm.nih.gov/32097489/)); *J Neurosurg Case Lessons* 2023 ([PMID 37014023](https://pubmed.ncbi.nlm.nih.gov/37014023/)) |
| **IFJa** | **Switching.** Comes up when the task changes under you — a cut to a new scene, a change of rules, a reframing of what you thought you were watching. | Moderate | New in Glasser 2016. Assem et al. 2020 *Cereb Cortex* ([PMID 32244253](https://pubmed.ncbi.nlm.nih.gov/32244253/)) place IFJa in the extended multiple-demand system: "Premotor frontal activation is strongest around IFJp, spreading toward the PEF area dorsally and inferior frontal sulcus regions (IFJa and IFSp) ventrally." IFJ-and-switching more broadly: Derrfuss et al. 2005 *HBM* ([PMID 15846824](https://pubmed.ncbi.nlm.nih.gov/15846824/)) |
| **IFSp** | **Effort.** Ramps with difficulty — a plot that needs tracking, a rule that has to be held in mind. Domain-general: it does not care whether the difficulty is visual, verbal or numerical. | Moderate | New in Glasser 2016; same Assem et al. 2020 sentence places it in the extended MD system. The MD system's domain-generality is well established, the parcel-level attribution is recent |

## Film-relevant buckets

Mapping the parcels into creative dials. A parcel can appear in more than one bucket.

**Scene / place — "what kind of world is this"**
`VMV2` (primary — this is the parahippocampal scene strip), `VMV3` (secondary).
The strongest scene dial we have. Note we do **not** have the canonical scene areas PPA/RSC/OPA in this set, so `VMV2` is carrying that whole bucket.

**Faces**
`PIT` (primary — face parts, OFA), `STSdp` (dynamic and expressive faces, not identity).
`VMV3` and `V8` sit adjacent to face-selective ventral cortex and will co-vary. We do **not** have `FFC` (the fusiform face complex), which is the parcel you would actually want for face identity — worth requesting from the model if faces matter.

**Bodies / biological motion**
`V4t`, `LO2`, `STSdp`.
Weakest bucket in the set. The dedicated body areas (`PH`, `FST`, `MT`, `MST`) are absent.

**Motion and camera — "how is the frame moving"**
`V6A` (wide-field optic flow — dollies, whip pans, travelling shots), `VIP` (self-motion vs object-motion, looming, things coming at camera), `V3CD` and `V4t` (local motion), `V3B` (spatial layout in motion).
`V6A` + `VIP` together are the closest thing we have to a "camera movement" dial, and they are conceptually distinct from local motion: they respond to the whole field moving, which is exactly what a camera move produces.

**Object and shape**
`LO2` (primary), `V4`, `V3CD`.

**Colour and surface**
`V4` (primary), `V8`, `VMV3`.

**Voices and sound texture**
`PBelt` (timbre, room, grain), `A4` (sound objects), `A5` (speech-shaped sound), `STSdp` (voice as social signal).
This is a genuinely good chain — it runs from acoustic texture to social meaning across four parcels, so you can dial "how much of the soundtrack is *someone*" separately from "how much is *something*".

**Speech and narrative language**
`55b` (speech production/planning), `A5`, `STSdp`, and `IFJa`/`IFSp` on the comprehension-effort side.
All five are CAB-NP Language network (except IFSp on the right). This is the second-strongest coherent bucket in the set after attention.

**Attention and scanning — "is the viewer hunting the frame"**
`FEF`, `PEF` (eye-movement commands), `LIPv`, `VIP`, `IPS1`, `V7`, `IP0` (priority maps).
Strongest and best-populated bucket we have — seven parcels, all well-established, spanning frontal command and parietal map. If you want one reliable dial out of this whole set, it is this one.

**Cognitive load / narrative effort**
`IFJa` (switching, discontinuity), `IFSp` (sustained difficulty).
Both are extended multiple-demand areas: they respond to *how hard the material is*, independent of what kind of material it is. Useful as a "is the audience working" readout.

**Narrative / self-referential / default-mode — ⚠️ we do not have this**
`STSdp` is the only parcel in our set with a strong default-mode signature (Yeo7 Default 100% left), and its default-mode membership reflects social cognition rather than self-referential thought. We have **no** medial prefrontal, posterior cingulate, precuneus, angular gyrus or temporal pole parcels. **There is no self-referential or narrative-integration dial available from these 24 parcels.** If that is wanted, the model needs to output `31pv`/`31pd`/`7m`/`POS2` (posterior cingulate–precuneus), `10r`/`9m`/`p32` (medial prefrontal), and `PGs`/`PGi` (angular gyrus). Worth raising before anyone designs around a "narrative" dial.

## Contested or thin — flag list

1. **Six of our 24 parcels were newly defined in 2016** and carry little independent literature: `V3CD`, `IP0`, `A5`, `STSdp`, `IFSp`, `IFJa` (Glasser "New?" = Yes), plus `VMV2`, `VMV3`, `LIPv`, `VIP`, `A4`, `PBelt` marked "Yes*" (new subdivision of a previously named region). For all of these, the function attributed above is inherited from the surrounding territory, not measured for the parcel.
2. **`V3CD` is the weakest.** Glasser's Table 1 lists V3A, V3B *and* hOC4la as prior names for the same territory — three different authors carved it three different ways. Any strong functional claim about V3CD is unsupportable.
3. **`IP0` is nearly as thin.** The Supplementary Results say essentially nothing about it beyond its position, and it does not appear in the Assem 2020 multiple-demand mapping. CAB-NP calls it Dorsal-Attention; Yeo7 splits it ~50/50 Visual vs Dorsal Attention in both hemispheres. Treat it as an attention parcel with wide uncertainty.
4. **`V8` as a distinct colour area is contested.** Hadjikhani et al. 1998 proposed it; the field's more common carving (Wandell and colleagues) treats the same cortex as VO1, which Glasser lists as its synonym. Do not build a "colour" dial on V8 alone — use V4.
5. **`V4t` / `LO2` naming collision.** Glasser's Table 1 gives "LO2" as another author's name for the parcel Glasser calls **V4t**, while Glasser separately has a parcel *named* LO2. If anyone cross-references older papers, this will bite. Always disambiguate by parcel index: V4t = 156, LO2 = 21.
6. **`55b` is real but individually variable.** Glasser explicitly notes that "the Main Text and the Supplementary Results and Discussion sections #1.3–1.4 and Supplementary Figures 7–10 describe the distinct topologies that area 55b and the eye fields have in atypical individuals." Group-average maps blur it and can place it wrongly in a given person. Its Yeo7 assignment has no majority in either hemisphere, which is a symptom of the same problem. Use it, but do not treat a single-subject 55b value as precisely localised.
7. **Do not use Yeo7 for the auditory and language parcels.** As set out above, Yeo7 has no language network and files A4, A5 and PBelt under "Somatomotor". Use CAB-NP.
8. **A methodological trap in the source document.** The Supplementary Neuroanatomical Results mentions task contrasts (FACE-AVG, PLACE-AVG, BODY-AVG, TOOL-AVG, STORY-MATH, TOM-RANDOM) constantly, and it is tempting to count them per parcel as a functional profile. Do not. Those contrasts are cited because they were *diagnostic at a boundary between two areas* — often as a deactivation, often for the neighbour. Counting them produces a confident-looking table that means nothing. If we want real per-parcel task profiles, the right source is the HCP S1200 group task-fMRI effect-size maps on BALSA, parcellated — not this PDF.
9. **Absent buckets.** No default-mode/self-referential parcels; no dedicated face-identity parcel (`FFC`); no dedicated body or motion-complex parcels (`MT`, `MST`, `FST`, `PH`); no canonical scene areas beyond `VMV2`. Several creative dials that sound obvious are simply not measurable from this parcel set.
10. **Coverage caveat on the "no annotation exists" finding.** As noted at the top, this was established by direct checks against EBRAINS/siibra, the GitHub repository-search API and the CAB-NP repo, not by a search sweep. GitHub code search and HuggingFace were not queried. The probability that a well-known resource was missed is low but not zero.

## Sources

Primary sources, all retrieved and parsed on 2026-09-02:

1. Glasser MF, Coalson TS, Robinson EC, et al. **A multi-modal parcellation of human cerebral cortex.** *Nature* 2016;536:171–178. [PMID 27437579](https://pubmed.ncbi.nlm.nih.gov/27437579/) — the parcellation itself.
2. **Supplementary Neuroanatomical Results** for the above — 97 pp PDF, direct download, no login: `https://static-content.springer.com/esm/art%3A10.1038%2Fnature18933/MediaObjects/41586_2016_BFnature18933_MOESM330_ESM.pdf`. Source for the 22 region sections and Supplemental Table 1 (parcel index, full name, "New?", synonyms, key studies).
3. Ji JL, Spronk M, Kulkarni K, Repovš G, Anticevic A, Cole MW. **Mapping the human brain's cortical-subcortical functional network organization.** *NeuroImage* 2019;185:35–57. [PMID 30291974](https://pubmed.ncbi.nlm.nih.gov/30291974/). Repo: <https://github.com/ColeLab/ColeAnticevicNetPartition> — the machine-readable network annotation.
4. `hcp-utils` — <https://github.com/rmldj/hcp-utils>, `hcp_utils/data/{mmp_1.0,yeo7,yeo17,ca_network_1.1}.npz`. Source of the vertex-level maps used to compute the Yeo7 columns here.
5. Assem M, Glasser MF, Van Essen DC, Duncan J. **A Domain-General Cognitive Core Defined in Multimodally Parcellated Human Cortex.** *Cereb Cortex* 2020;30:4361–4380. [PMID 32244253](https://pubmed.ncbi.nlm.nih.gov/32244253/) — multiple-demand system in HCP-MMP1 parcels; source for IFJa/IFSp.
6. Arcaro MJ, McMains SA, Singer BD, Kastner S. **Retinotopic organization of human ventral visual cortex.** *J Neurosci* 2009;29:10638–52. [PMID 19710316](https://pubmed.ncbi.nlm.nih.gov/19710316/) — PHC1/PHC2, i.e. VMV2.
7. Larsson J, Heeger DJ. **Two retinotopic visual areas in human lateral occipital cortex.** *J Neurosci* 2006;26:13128–42. [PMID 17182764](https://pubmed.ncbi.nlm.nih.gov/17182764/) — LO1/LO2.
8. Pitzalis S, Fattori P, Galletti C. **The human cortical areas V6 and V6A.** *Vis Neurosci* 2015;32:E007. [PMID 26241369](https://pubmed.ncbi.nlm.nih.gov/26241369/).
9. Belin P, Zatorre RJ, Lafaille P, Ahad P, Pike B. **Voice-selective areas in human auditory cortex.** *Nature* 2000;403:309–12. [PMID 10659849](https://pubmed.ncbi.nlm.nih.gov/10659849/) — the STS voice areas.
10. Deen B, Koldewyn K, Kanwisher N, Saxe R et al. **People-selectivity, audiovisual integration and heteromodality in the superior temporal sulcus.** *Cortex* 2014. [PMID 23988132](https://pubmed.ncbi.nlm.nih.gov/23988132/).
11. Sereno MI et al. **Mapping the complex topological organization of the human parietal face area.** *NeuroImage* 2017. [PMID 28889002](https://pubmed.ncbi.nlm.nih.gov/28889002/) — human VIP.
12. **The macaque ventral intraparietal area has expanded into three homologue human parietal areas.** *Prog Neurobiol* 2022. [PMID 34775040](https://pubmed.ncbi.nlm.nih.gov/34775040/).
13. **The role of the ventral intraparietal area (VIP/pVIP) in the perception of object-motion and self-motion.** *NeuroImage* 2020. [PMID 32112961](https://pubmed.ncbi.nlm.nih.gov/32112961/).
14. Derrfuss J, Brass M, Neumann J, von Cramon DY. **Involvement of the inferior frontal junction in cognitive control: meta-analyses of switching and Stroop studies.** *Hum Brain Mapp* 2005. [PMID 15846824](https://pubmed.ncbi.nlm.nih.gov/15846824/).
15. Area 55b clinical evidence: **Middle Frontal Gyrus and Area 55b: Perioperative Mapping and Language Outcomes**, *Front Neurol* 2021 ([PMID 33776898](https://pubmed.ncbi.nlm.nih.gov/33776898/)); **Pure Apraxia of Speech After Resection Based in the Posterior Middle Frontal Gyrus**, *Neurosurgery* 2020 ([PMID 32097489](https://pubmed.ncbi.nlm.nih.gov/32097489/)); **Apraxia of speech with phonological alexia and agraphia following resection of the left middle precentral gyrus**, *J Neurosurg Case Lessons* 2023 ([PMID 37014023](https://pubmed.ncbi.nlm.nih.gov/37014023/)).
16. EBRAINS siibra parcellation registry (checked, HCP-MMP1 absent): `https://siibra-api-stable.apps.hbp.eu/v3_0/parcellations`.

## Companion file

`parcel-annotations.csv` — machine-readable, 24 rows, one per observed parcel. Columns: `parcel, glasser_index, glasser_full_name, glasser_region_section, glasser_region_name, new_in_2016, glasser_synonyms, cabnp_network_L, cabnp_network_R, yeo7_majority_L, yeo7_pct_L, yeo7_majority_R, yeo7_pct_R, film_bucket, evidence`.
