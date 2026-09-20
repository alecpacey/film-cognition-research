# Amendment to OSF registration `osf.io/dg7fe` — ready to paste

Redrafted 20 September 2026 (the first draft, on the Desktop, no longer exists). File through
the registration's **Update** process; the original stays visible as version 1. Nothing below
changes a threshold, criterion, sample size or model specification.

## Field: "Justification for update" (paste as is)

This update corrects a false statement about protocol compliance. It changes no hypothesis,
criterion, threshold, sample size, or analysis specification.

The registration states in item_11 and item_15 that the pre-registered futility check
(`futility_check.py`) "has never been executed", and in item_11 that "no dial→parcel
relationship has been computed, inspected, or estimated, by any means, at any point". Both
statements are incorrect. The futility check was executed once, on 6 September 2026, at 30 of
70 segments, and returned CONTINUE.

The check is the pre-specified stopping rule described in item_15, so running it was permitted
by the protocol. By construction it prints a single binary verdict. Only that verdict was
recorded; no dial, parcel, coefficient or effect size was produced or inspected, and
collection proceeded exactly as it would have otherwise. The registered confirmatory test was
run once, on the complete frozen dataset, after registration.

How the error arose: before filing, the claim was checked by searching the repository and its
logs for the script's output banner and verdict strings, which returned nothing. The script
was untracked in version control and had been run interactively, printing to a terminal.
Absence of a record was read as absence of execution. The accurate statement at the time would
have been "no record of execution exists on disk".

The error was identified after registration and before any publication, and is disclosed in
the study's result document and working paper.

## item_11 · Explanation of existing data — replace the two bullets

Replace:

> - No dial→parcel relationship has been computed, inspected, or estimated, by any
>   means, at any point.
> - **No elastic net has been fitted to the response data. No permutation null has
>   been run.** The pre-registered futility script `futility_check.py` exists in the
>   repository but **has never been executed** — see item_15.

with:

> - The only dial→parcel computation performed before registration was the pre-registered
>   futility check (item_15), executed once on 6 September 2026 at 30 of 70 segments. It fits
>   the elastic net and a permutation null internally and prints a single binary verdict,
>   which was CONTINUE. No dial, parcel, coefficient or effect size was output or inspected.
> - Apart from that check, no elastic net has been fitted to the response data and no
>   permutation null has been run. **[Corrected by update: the original text stated the
>   futility script had never been executed. That was false.]**

## item_15 · Stopping rule — replace the first sentence of the paragraph

Replace:

> **The futility check was never executed, and the study did not rely on it.** The
> script implementing it (`futility_check.py`) was written and is in the repository,
> but its banner appears in no log and no verdict string exists anywhere on disk.
> Collection ran to completion without it.

with:

> **The futility check was executed once, on 6 September 2026 at 30 of 70 segments, and
> returned CONTINUE.** Its banner appears in no log and no verdict string exists on disk
> because the script was untracked and was run interactively, printing to a terminal; the
> original text of this item inferred from that absence that it had never run, which was
> false. Only the binary verdict was recorded. Collection then ran to completion.
> **[Corrected by update.]**

Leave the rest of item_15 (the description of `gate_and_continue.sh`) unchanged; it is accurate.

## After filing

Record the date here and in `../../CONSOLIDATION.md` (step 1d), and align PAPER § 4.8 / § 7,
which currently say the registration "was amended publicly".

---

## Exact edits against the text as posted on OSF (supplied by the author, 20 Sep 2026)

Field **"Explanation of foreknowledge and managing unintended influences"** — three changes;
every other paragraph is left byte-for-byte as posted.

**1 · Lead-in and list of WHAT WAS OBSERVED.** Change the lead-in sentence and add item (g):

> WHAT WAS OBSERVED. Pipeline-health quantities, each declared in advance in the project's stage README before collection began, and one further item, (g), added by this update:
> … (a) to (f) unchanged …
>  (g) [ADDED BY UPDATE] the single binary verdict of the pre-registered futility check (see Stopping rule), executed once on 6 September 2026 at 30 of 70 segments. The verdict was CONTINUE. The original text of this registration omitted this item and stated the check had never been executed; that was false.

**2 · WHAT WAS NOT OBSERVED** — replace the paragraph.

**3 · Action 2** — replace the sentence claiming the script HAS NEVER BEEN EXECUTED.

Full replacement text for 2 and 3 is in the conversation record of 20 Sep and in the OSF
revision itself once approved.

---

## Review-page check, 20 Sep 2026 — further locations found before submission

Reading the full review page showed the false claim, or a claim it makes false, in more fields
than the local notes recorded, plus one unrelated false statement:

- **Starting and stopping rules** — the first paste did not take; review page still showed the original.
- **Research Design → Additional blinding → item 5** ("THE FUTILITY SCRIPT WAS NEVER RUN").
- **Analysis Plan → Inference criteria** ("No interim version of it has been run").
- **Analysis Plan → Other planned analysis → item 1** (lists interim looks, omits the futility look).
- **Research Design → Study design** and **Variables → Measured variables → COVARIATES**: both say
  scene-boundary counts per segment are kept in the dial table. They never were (found 15 Sep;
  PAPER § 4.3 corrected). Not in the registered model, so no analysis is affected.

The justification was rewritten to use OSF's field names and to cover both corrections. The
OSF revision, once approved, is the authoritative text.
