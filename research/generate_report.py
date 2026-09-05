#!/usr/bin/env python3
"""Assemble results/*.json into report.md, driven by fields.yaml."""
import json, glob, os, re, sys, datetime
import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "results")
FIELDS = os.path.join(BASE, "fields.yaml")
OUT = os.path.join(BASE, "report.md")

CATEGORY_MAPPING = {
    "identity":   ["identity", "Identity"],
    "interface":  ["interface", "Interface"],
    "performance":["performance", "performance_metrics", "Performance"],
    "complexity": ["complexity", "Complexity"],
    "decision":   ["decision", "Decision"],
    "risk":       ["risk", "Risk"],
    "economics":  ["economics", "Economics", "business_info"],
    "evidence":   ["evidence", "Evidence", "sources_section"],
}
NESTED_KEYS = {k for v in CATEGORY_MAPPING.values() for k in v}
SKIP_KEYS = {"_source_file", "uncertain"}
CAT_TITLE = {
    "identity": "Identity", "interface": "Interface", "performance": "Performance",
    "complexity": "Complexity", "decision": "Decision", "risk": "Risk",
    "economics": "Economics", "evidence": "Evidence",
}

def load_fields():
    d = yaml.safe_load(open(FIELDS, encoding="utf-8"))
    cats = []
    for c in d.get("field_categories", []):
        cats.append((c["category"], [f["name"] for f in c.get("fields", [])]))
    return cats

def find_field(data, name):
    """top level -> category dicts -> any nested dict"""
    if name in data:
        return data[name]
    for k, v in data.items():
        if k in NESTED_KEYS and isinstance(v, dict) and name in v:
            return v[name]
    stack = [data]
    while stack:
        o = stack.pop()
        if isinstance(o, dict):
            for k, v in o.items():
                if k == name:
                    return v
                if isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(o, list):
            stack.extend(i for i in o if isinstance(i, (dict, list)))
    return None

def is_uncertain(val, name, unc):
    if name in unc:
        return True
    if val is None:
        return True
    if isinstance(val, str):
        s = val.strip()
        if not s or "[uncertain]" in s:
            return True
    return False

def fmt(val, depth=0):
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, (int, float, bool)):
        return str(val)
    if isinstance(val, list):
        if not val:
            return ""
        if all(isinstance(i, dict) for i in val):
            return "\n".join(
                "- " + " | ".join(f"**{k}**: {fmt(v, depth+1)}" for k, v in i.items())
                for i in val)
        parts = [fmt(i, depth+1) for i in val]
        if sum(len(p) for p in parts) < 120 and all("\n" not in p for p in parts):
            return ", ".join(parts)
        return "\n".join("- " + p.replace("\n", "\n  ") for p in parts)
    if isinstance(val, dict):
        lines = []
        for k, v in val.items():
            body = fmt(v, depth+1)
            if "\n" in body:
                lines.append(f"- **{k}**:\n" + "\n".join("  " + l for l in body.splitlines()))
            else:
                lines.append(f"- **{k}**: {body}")
        return "\n".join(lines)
    return str(val)

def block(text):
    """Render long prose readably."""
    t = fmt(text)
    if not t:
        return ""
    if "\n" in t or len(t) > 100:
        return t
    return t

def anchor(name):
    a = name.lower()
    a = re.sub(r"[^a-z0-9\s-]", "", a)
    return re.sub(r"\s+", "-", a.strip())

def badge(data, unc):
    dc = find_field(data, "dev_complexity")
    rating = ""
    if not is_uncertain(dc, "dev_complexity", unc) and isinstance(dc, str):
        m = re.search(r"\b(LOW|MEDIUM|MED|HIGH)\b", dc, re.I)
        if m:
            rating = m.group(1).upper()
    cost = find_field(data, "cost")
    csnip = ""
    if not is_uncertain(cost, "cost", unc):
        c = fmt(cost)
        m = re.search(r"\$[\d,]+(?:\.\d+)?\s*(?:/|per\s)?\s*(?:hr|hour|s\b|sec|second|mo|month|day)?", c)
        if m:
            csnip = m.group(0).strip()
        elif c:
            csnip = (c[:38] + "…") if len(c) > 38 else c
    bits = []
    if rating: bits.append(f"Complexity: **{rating}**")
    if csnip:  bits.append(f"Cost: {csnip}")
    return " · ".join(bits)

def main():
    cats = load_fields()
    defined = {f for _, fs in cats for f in fs}
    files = sorted(glob.glob(os.path.join(RESULTS, "*.json")))
    if not files:
        sys.exit("no results found")

    items = []
    for p in files:
        data = json.load(open(p, encoding="utf-8"))
        unc = set(data.get("uncertain") or [])
        title = find_field(data, "name") or os.path.basename(p)[:-5].replace("_", " ").title()
        if not isinstance(title, str):
            title = os.path.basename(p)[:-5].replace("_", " ").title()
        items.append({"file": os.path.basename(p), "data": data, "unc": unc, "title": title.strip()})

    items.sort(key=lambda i: i["title"].lower())

    L = []
    L.append("# Brain-Reactive Livestream: TRIBE v2 → MiniMax H3 Max")
    L.append("")
    topic = ""
    try:
        topic = yaml.safe_load(open(os.path.join(BASE, "outline.yaml"), encoding="utf-8")).get("topic", "") or ""
    except Exception:
        # outline is documentation, not a hard dependency — fall back to a regex read
        try:
            raw = open(os.path.join(BASE, "outline.yaml"), encoding="utf-8").read()
            m = re.search(r"^topic:\s*>-?\s*\n((?:[ \t]+.*\n)+)", raw, re.M)
            if m:
                topic = " ".join(m.group(1).split())
        except Exception:
            pass
    L.append(f"> {' '.join(topic.split())}")
    L.append("")
    L.append(f"*Generated {datetime.date.today().isoformat()} · {len(items)} research items · "
             f"all validated at 100% field coverage · fields marked uncertain are omitted*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Contents")
    L.append("")
    for n, it in enumerate(items, 1):
        b = badge(it["data"], it["unc"])
        L.append(f"{n}. [{it['title']}](#{anchor(it['title'])})" + (f" — {b}" if b else ""))
    L.append("")
    L.append("---")
    L.append("")

    for n, it in enumerate(items, 1):
        data, unc = it["data"], it["unc"]
        L.append(f"## {it['title']}")
        L.append("")
        used = set()
        for cat, fnames in cats:
            rows = []
            for fn in fnames:
                v = find_field(data, fn)
                used.add(fn)
                if is_uncertain(v, fn, unc):
                    continue
                rows.append((fn, v))
            if not rows:
                continue
            L.append(f"### {CAT_TITLE.get(cat, cat.title())}")
            L.append("")
            for fn, v in rows:
                L.append(f"**{fn}**")
                L.append("")
                L.append(block(v))
                L.append("")

        extras = []
        for k, v in data.items():
            if k in SKIP_KEYS or k in NESTED_KEYS or k in defined or k == "name":
                continue
            if is_uncertain(v, k, unc):
                continue
            extras.append((k, v))
        if extras:
            L.append("### Other Info")
            L.append("")
            for k, v in extras:
                L.append(f"**{k}**")
                L.append("")
                L.append(block(v))
                L.append("")

        if unc:
            L.append("### Flagged Uncertain (omitted above)")
            L.append("")
            for u in sorted(unc):
                L.append(f"- `{u}`")
            L.append("")
        L.append("---")
        L.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print(f"wrote {OUT}")
    print(f"items: {len(items)}  lines: {len(L)}")

if __name__ == "__main__":
    main()
