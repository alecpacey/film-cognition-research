# Authoring tooling

Third-party Agent Skills used to draft, audit and validate `research/PAPER.md`.
They are **not** part of the research record and are not vendored into this repo;
they are recorded here so the authoring environment is reproducible, per the TOP
framework's expectation that software and versions be stated.

Installed under `.claude/skills/` (gitignored). Both sources are MIT-licensed.

| skill | source repo | pinned commit |
|---|---|---|
| research-paper-writing | https://github.com/Master-cai/Research-Paper-Writing-Skills | `77e7c2c1ba06f7d71844873147665437a03aac1b` |
| scientific-writing | https://github.com/k-dense-ai/scientific-agent-skills | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |
| peer-review | same | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |
| scientific-critical-thinking | same | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |
| statistical-power | same | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |
| statistical-analysis | same | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |
| citation-management | same | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |
| venue-templates | same | `1e5eeffbdad3749125afe7ab48a39694e27f181c` |

Fetched 5 September 2026. Upstream commit dates: k-dense `2026-09-02T09:25:16-07:00`, Master-cai `2026-06-23T10:28:54+08:00`.
K-Dense plugin version 2.66.0 (163 skills upstream; the seven above were selected,
the rest are bioinformatics and cheminformatics and are not relevant here).

Scanned before installation: no `eval`, `exec`, `os.system`, shell injection or
credential access. One `subprocess` call, in `venue-templates/scripts/validate_format.py`,
invoking poppler on a local PDF without `shell=True`. Outbound hosts are academic
only — OpenAlex, Crossref, DataCite, NCBI/PubMed, arXiv — plus venue sites.
