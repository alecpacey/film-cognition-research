# OSF Preprints — submission sheet (preprint v1)

Everything to paste, in roughly the order OSF asks for it. OSF's form labels change from time
to time; match by meaning if a label differs. **Submitting on the general OSF Preprints server
publishes immediately and mints a DOI; a preprint can later be versioned or withdrawn, but not
deleted.**

## Before you start — three checks

1. **Lift the OSF embargo on `osf.io/dg7fe`.** The paper says the registration is released with
   it, and the preregistration link below is useless to readers while it is embargoed.
2. **Open the PDF once and read the first page and the last two.**
   `research/preprint/Pacey-2026-technique-response-index-v1.pdf` — 36 pages, A4.
3. **Confirm the two marked statements below** (funding; the film's producer). They are facts only
   you know; do not paste them unchecked.

## Server

**OSF Preprints** (general). An alternative with the same form is **PsyArXiv**, which is moderated
and read by the cognitive-science audience; OSF Preprints was the plan.

## File

`research/preprint/Pacey-2026-technique-response-index-v1.pdf`

## Title

A technique→response index for cinematography, measured through a brain encoding model

## Abstract

Paste the five paragraphs under "Abstract" in `research/PAPER.md` (397 words), as plain text.
If the form strips the arrow in the title or the Greek letters, they are not in the abstract.

## Authors

- **Alec Pacey** — Independent researcher — alecpacey12@gmail.com — ORCID: link it from your OSF
  profile (or send me the iD and I will add it to the PDF).

## Licence

**CC BY 4.0** (Creative Commons Attribution 4.0 International) — the same licence as the text
and data in the repository.

## Subjects (OSF uses the bepress taxonomy)

- Life Sciences › Neuroscience and Neurobiology › Cognitive Neuroscience
- Social and Behavioral Sciences › Psychology › Cognitive Psychology
- Arts and Humanities › Film and Media Studies

## Tags / keywords

cinematography · film editing · cut rate · brain encoding model · TRIBE · fMRI · naturalistic
neuroimaging · pre-registration · model-based sensor · Algonauts 2025

## Original publication date / DOI of a published article

None — not published elsewhere.

## Author assertions

**Conflict of interest — Yes, declared:**

> The author is making a short film, *The Simulated Viewer*, whose premise — a machine
> optimising a simulated cortex drifts towards faces — is a hypothesis this research tests, not
> a result it relies on (§1.3). **[CONFIRM: is the film produced by mutuals inc.? If so add: "The
> film is produced by the author's company, mutuals inc."]** The author has no financial interest
> in TRIBE, Meta, fal, MiniMax or Hugging Face. **[CONFIRM: funding — if true, add: "The work
> received no external funding; compute (≈ $40–43, §4.9) was paid by the author."]**

**Public data — Available:**

- Link: `https://github.com/alecpacey/film-cognition-research`
- Description:

> The repository holds the sensor's outputs for every scored clip (180-parcel vectors per stage;
> 1 Hz timelines for stage 03b), the dial table for all 244 segments, content descriptors and
> transcripts, every summary output the paper's claims trace to, and all analysis code, with
> full history. Code MIT; text and data CC BY 4.0 (the parcel vectors are TRIBE's predictions and
> may also be subject to TRIBE's licence). The source films are public-domain prints identified
> by Internet Archive identifier; segment files and generated clips are not redistributed.

**Preregistration — Available, type: Analysis Plan:**

- Link: `https://osf.io/dg7fe`
- Description:

> Stage 02's analysis plan was registered on OSF on 8 September 2026, after data collection and
> before the analysis was run, with the frozen dataset attached (SHA-256 93807b80…3a3189); it was
> amended through OSF's update process on 20 September 2026 to correct a false statement about
> an interim check. The other stages' criteria were fixed in the repository before each run; the
> commits are listed in the paper's availability statement. Stages 00 and 01 predate the
> repository. Exploratory analyses are labelled as such throughout.

## Supplemental materials

Link the GitHub repository (above). If OSF asks for an OSF project instead, the registration's
parent project is the natural one.

## After it is posted

Send me the preprint's DOI. I will add it to the paper's front matter and README, tag the
repository commit the PDF was built from as `preprint-v1`, and record it in `LOG.md`.
