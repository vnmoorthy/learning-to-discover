#!/usr/bin/env python3
"""Refresh the generated result blocks in README.md and docs/RESULTS.md from the run's data files.

    python3 docs/update_results.py            # rewrite the blocks + docs/assets/reward_curve.png
    python3 docs/update_results.py --check    # exit 1 if a file would change (CI), write nothing
    python3 docs/update_results.py --no-plot  # skip the matplotlib figure

Blocks are delimited by HTML comments and replaced in place (everything else in the files is left alone):

    <!-- RESULTS:START -->  ... <!-- RESULTS:END -->     headline, problems table, lab totals
    <!-- LEARNING:START --> ... <!-- LEARNING:END -->    Tinker self-improvement numbers
    <!-- MEMORY:START -->   ... <!-- MEMORY:END -->      past.dev vs markdown vs RAG benchmark
    <!-- DETAIL:START -->   ... <!-- DETAIL:END -->      per-problem detail, predictions, sandboxes, toolsmith

Inputs (first existing file wins; nothing here talks to a network or reads .env):
    web/public/data/state.json                                   snapshot of the live run (python3 -m phoenixastar.snapshot)
    data/learning.json          | web/public/data/learning.json
    data/memory_benchmark.json  | data/snapshot/memory_benchmark.json | web/public/data/memory.json["benchmark"]
    data/toolsmith.json                                          optional
    web/public/data/decisions.json, web/public/data/sandboxes.json   optional

Every number printed comes from those files. If no record has been beaten, the block says so.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = ["README.md", os.path.join("docs", "RESULTS.md")]
BG, CYAN, AMBER, INK, MUTED, GRID = "#07080B", "#3DF5FF", "#FFB547", "#E8EDF2", "#8B96A5", "#1A2029"


# ------------------------------------------------------------------ loading
def load(*rel):
    """First readable JSON file among the given repo-relative paths -> (object, path) or (None, None)."""
    for r in rel:
        p = os.path.join(ROOT, r)
        try:
            with open(p) as f:
                return json.load(f), r
        except (OSError, ValueError):
            continue
    return None, None


def load_all():
    state, state_src = load("web/public/data/state.json")
    learning, learning_src = load("data/learning.json", "web/public/data/learning.json")
    bench, bench_src = load("data/memory_benchmark.json", "data/snapshot/memory_benchmark.json")
    if bench is None:
        mem, src = load("web/public/data/memory.json")
        if mem and mem.get("benchmark"):
            bench, bench_src = mem["benchmark"], src
    toolsmith, _ = load("data/toolsmith.json")
    decisions, _ = load("web/public/data/decisions.json")
    sandboxes, _ = load("web/public/data/sandboxes.json")
    return dict(state=state, state_src=state_src, learning=learning, learning_src=learning_src, bench=bench,
                bench_src=bench_src, toolsmith=toolsmith, decisions=decisions, sandboxes=sandboxes)


# ------------------------------------------------------------------ formatting
def num(x, digits=6):
    if x is None:
        return "n/a"
    if isinstance(x, (int, float)) and float(x).is_integer() and abs(x) < 1e15:
        return str(int(x))
    s = f"{x:.{digits}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def pct(x, d=1):
    return "n/a" if x is None else f"{100 * x:.{d}f}%"


def when(ts):
    return (ts or "unknown time").replace("T", " ").replace("Z", " UTC")


STATUS = {"record": "**RECORD**", "searching": "searching", "stalled": "stalled", "idle": "not attacked yet",
          "proved-negative": "negative result proved"}


def gap_text(p):
    ours, rec = p.get("ours"), p["record"]["score"]
    if not ours or ours.get("score") is None:
        return "no valid solution of ours yet"
    s = ours["score"]
    if rec is None:
        return "verified study (no numeric record)"
    better = (s - rec) if p["scoring"] == "maximize" else (rec - s)
    if p.get("beats_record"):
        return f"**beats the record by {num(better)}**"
    if abs(better) < 1e-12:
        return "equals the record"
    ratio = (s / rec) if p["scoring"] == "maximize" else (rec / s)
    return f"{num(-better)} short ({pct(ratio)} of the record)"


def signal_text(p):
    m = p.get("metric") or {}
    v, name, rec = m.get("value"), m.get("name"), p["record"]["score"]
    if v is None:
        return "no run"
    seeded = " (searches start from the public record; not ours)" if rec is not None and abs(v - rec) < 1e-9 and not p.get("beats_record") else ""
    if name == "min_violated_lines":
        return f"{num(v)} violated lines in the best SAT model (0 = valid)"
    if name == "bad_vectors":
        return f"{num(v)} bad sign vectors left (0 = beats the record)"
    if name == "best_log10":
        return f"best log10&#124;det&#124; {num(v, 8)}{seeded}"
    if name == "best_size":
        return f"best code size {num(v)}, need {num(m.get('target'))}{seeded}"
    return f"{name} = {num(v)}{seeded}"


# ------------------------------------------------------------------ blocks
def block_results(d):
    st = d["state"]
    if not st:
        return "_No snapshot found (`web/public/data/state.json`). Run `python3 -m phoenixastar.snapshot`, then this script._"
    snap = (st.get("snapshot") or {}).get("generated_at") or st.get("now")
    probs, tot = st["problems"], st.get("totals", {})
    won = [p for p in probs if p.get("beats_record")]
    out = [f"_Generated by `docs/update_results.py` from `{d['state_src']}`. Snapshot of the live run taken "
           f"**{when(snap)}** (cycle {st['loop']['cycle']}, proposer `{st['loop'].get('proposer_model')}`)._", ""]
    if won:
        out.append("**Records beaten (official verifier): " + "; ".join(
            f"`{p['slug']}` {num(p['ours']['score'])} vs {num(p['record']['score'])} ({p['record']['holder']})" for p in won) + ".**")
    else:
        out.append("**No record has been beaten yet.** Every row below is the distance that is left, measured by the "
                   "official verifier or by the search's own exact progress signal.")
    out += ["", "| Problem | Record (holder) | Ours, verified | Gap to the record | Live search signal | Status |",
            "|---|---|---|---|---|---|"]
    for p in probs:
        ours = p.get("ours")
        out.append(f"| `{p['slug']}` | {num(p['record']['score'])} ({p['record']['holder']}) | "
                   f"{num(ours['score']) if ours and ours.get('score') is not None else 'none'} | {gap_text(p)} | "
                   f"{signal_text(p)} | {STATUS.get(p['status'], p['status'])} |")
    c = st.get("compute", {})
    out += ["", f"Lab totals at the snapshot: **{tot.get('cycles', 0)}** cycles, **{tot.get('decisions', 0)}** logged decisions, "
                f"**{tot.get('experiments_run', 0)}** experiments, **{tot.get('sandboxes_run', 0)}** Modal sandbox programs, "
                f"**{tot.get('facts', 0)}** memory facts, **{tot.get('sources', 0)}** literature sources, "
                f"**{tot.get('records', 0)}** records. Compute in use: {sum(1 for g in c.get('gpus', []) if g.get('problem'))} of {len(c.get('gpus', []))} GPUs, "
                f"{sum((c.get('cpu_procs') or {}).values())} CPU search processes on {c.get('cpus', '?')} cores."]
    return "\n".join(out)


def block_learning(d):
    L = d["learning"]
    if not L or not L.get("steps"):
        return "_No Tinker run found (`data/learning.json`)._"
    steps = L["steps"]
    k = min(5, len(steps))
    first, last = steps[:k], steps[-k:]
    mean = lambda rows, key: sum(r[key] for r in rows) / len(rows)  # noqa: E731
    out = [f"_Generated from `{d['learning_src']}`: run `{L.get('run_id', '?')}`, base model `{L.get('base_model')}`, problem "
           f"`{L.get('problem')}`, {len(steps)} steps, {when(L.get('started_at'))} to {when(L.get('finished_at'))}, status "
           f"`{L.get('status')}`._", "",
           f"| | First {k} steps | Last {k} steps |", "|---|---|---|",
           f"| Mean reward | {mean(first, 'reward_mean'):.3f} | {mean(last, 'reward_mean'):.3f} |",
           f"| Valid constructions (official verifier) | {pct(mean(first, 'valid_rate'))} | {pct(mean(last, 'valid_rate'))} |"]
    ev = L.get("eval")
    if ev:
        out += ["", "| Evaluation (same sample budget) | Base model (gen 0) | Trained (gen N) |", "|---|---|---|"]
        tr = ev.get("train")
        if tr:
            out += [f"| Training prompts: mean reward | {num(tr['gen0']['score'], 4)} | {num(tr['genN']['score'], 4)} |",
                    f"| Training prompts: valid rate | {pct(tr['gen0']['valid_rate'])} | {pct(tr['genN']['valid_rate'])} |",
                    f"| Training prompts: best h/&#124;A&#124; | {num(tr['gen0'].get('best_ratio'), 4)} | {num(tr['genN'].get('best_ratio'), 4)} |"]
        out += [f"| Held-out prompts: mean reward | {num(ev['gen0']['score'], 4)} | {num(ev['genN']['score'], 4)} |",
                f"| Held-out prompts: valid rate | {pct(ev['gen0']['valid_rate'])} | {pct(ev['genN']['valid_rate'])} |",
                f"| Held-out prompts: best h/&#124;A&#124; | {num(ev['gen0'].get('best_ratio'), 4)} | {num(ev['genN'].get('best_ratio'), 4)} |",
                "", f"Held-out set: {ev.get('heldout', 'n/a')}. {ev.get('samples', '?')} samples per cell."]
    b = L.get("best")
    if b:
        out += ["", f"Best construction sampled during training: score {num(b.get('score'), 4)} ({b.get('found_at', '?')}); "
                    + ("**it beats the record.**" if b.get("beats_record") else
                       "it does **not** beat the record (4/7 = 0.5714, lower is better). The model learned to write "
                       "valid constructions, not record ones.")]
    return "\n".join(out)


def block_memory(d):
    B = d["bench"]
    if not B or not B.get("systems"):
        return "_No memory benchmark found (`data/memory_benchmark.json`)._"
    out = [f"_Generated from `{d['bench_src']}`: {B.get('n_questions', '?')} auto-built questions over {B.get('n_facts', '?')} "
           f"facts from the lab's own memory, run {when(B.get('time'))}; answers by "
           f"`{(B.get('models') or {}).get('answer', '?')}`, graded by `{(B.get('models') or {}).get('judge', '?')}`, "
           f"top-k = {B.get('top_k', '?')}._", "",
           "| System | Accuracy | Single-fact | Cross-fact | Mean lookup latency | Cost per question | Mean context tokens |",
           "|---|---|---|---|---|---|---|"]
    for s in B["systems"]:
        kind = s.get("accuracy_by_kind") or {}
        out.append(f"| {s['name']} | {pct(s['accuracy'])} ({s.get('correct', '?')}/{s['n']}) | {pct(kind.get('single'))} | "
                   f"{pct(kind.get('cross'))} | {s['latency_ms']:.0f} ms | ${s.get('cost_per_question_usd', s['cost_usd'] / max(1, s['n'])):.5f} | "
                   f"{num(s.get('context_tokens_mean'), 0)} |")
    best = max(B["systems"], key=lambda s: s["accuracy"])
    cheap = min(B["systems"], key=lambda s: s.get("context_tokens_mean") or 1e18)
    out += ["", f"Highest accuracy: **{best['name']}** ({pct(best['accuracy'])}). Smallest context per question: "
                f"**{cheap['name']}** ({num(cheap.get('context_tokens_mean'), 0)} tokens). "
                f"Cost note from the benchmark: {B.get('cost_note', 'n/a')}."]
    return "\n".join(out)


def block_detail(d):
    st, out = d["state"], []
    if st:
        out += ["### Per-problem detail", ""]
        for p in st["problems"]:
            md = p.get("metric_detail") or {}
            bits = [f"status `{p['status']}`", f"{p['compute']['gpus']} GPUs", f"{p['compute']['cpu_procs']} CPU processes",
                    f"{len(p.get('strategies') or [])} strategies listed"]
            if md.get("best_age_min") is not None:
                bits.append(f"best unchanged for {num(md['best_age_min'], 1)} min")
            if md.get("by_target"):
                bits.append("by target: " + ", ".join(f"{k} = {num(v)}" for k, v in md["by_target"].items()))
            if md.get("secondary"):
                bits.append("secondary: " + ", ".join(f"{k} = {num(v)}" for k, v in md["secondary"].items()))
            out.append(f"- **`{p['slug']}`** ({p['title']}): " + "; ".join(bits) + "."
                       + (f" Known negative result: {p['known_negative']}." if p.get("known_negative") else ""))
        out.append("")
    dec = d["decisions"]
    if dec:
        pr = [x for x in dec if x.get("prediction")]
        v = {}
        for x in pr:
            k = (x.get("outcome") or {}).get("verdict") or "pending"
            v[k] = v.get(k, 0) + 1
        out += ["### Predictions", "",
                f"{len(pr)} of the {len(dec)} logged decisions carry a falsifiable prediction: "
                + ", ".join(f"{v.get(k, 0)} {k}" for k in ("confirmed", "refuted", "pending", "n/a"))
                + " (`n/a` = the action was never executed, so the prediction cannot be scored).", ""]
    sb = d["sandboxes"]
    if sb and st:
        scoring = {p["slug"]: (p["scoring"], p["record"]["score"]) for p in st["problems"]}
        out += ["### Modal sandbox programs", "", "| Problem | Programs | Valid | Best verified score | Against the record |", "|---|---|---|---|---|"]
        for slug in sorted({x["problem"] for x in sb}):
            rows = [x for x in sb if x["problem"] == slug]
            sc = [x["score"] for x in rows if x.get("score") is not None and x.get("status") == "ok"]
            mode, rec = scoring.get(slug, ("maximize", None))
            best = (max(sc) if mode == "maximize" else min(sc)) if sc else None
            if best is None or rec is None:
                rel = "n/a"
            else:
                diff = (best - rec) if mode == "maximize" else (rec - best)
                rel = "**beats it**" if diff > 1e-12 else ("equals it (reproduced, not beaten)" if abs(diff) <= 1e-12 else f"{num(-diff)} short")
            out.append(f"| `{slug}` | {len(rows)} | {len(sc)} | {num(best)} | {rel} |")
        out.append("")
    ts = d["toolsmith"]
    if ts and ts.get("sessions"):
        out += ["### Toolsmith (Devin) sessions", "", "| Problem | Status | Adopted | Created |", "|---|---|---|---|"]
        for s in ts["sessions"]:
            out.append(f"| `{s.get('problem')}` | {s.get('status')} | {'yes' if s.get('adopted') else 'no'} | {when(s.get('created', '')[:19] + 'Z')} |")
        out.append("")
    return "\n".join(out).rstrip() or "_No detail data found._"


BLOCKS = {"RESULTS": block_results, "LEARNING": block_learning, "MEMORY": block_memory, "DETAIL": block_detail}


# ------------------------------------------------------------------ figure
def plot(d, path):
    L = d["learning"]
    if not L or not L.get("steps"):
        return False
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipped", os.path.relpath(path, ROOT))
        return False
    s = L["steps"]
    x = [r["step"] for r in s]
    plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
                         "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5.2), dpi=130, facecolor=BG, gridspec_kw={"wspace": 0.16})
    for ax in (a, b):
        ax.set_facecolor(BG)
        ax.grid(True, color=GRID, linewidth=1)
        ax.set_axisbelow(True)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.tick_params(length=0)
        ax.set_xlabel("training step")
        ax.set_xlim(min(x) - 0.5, max(x) + 0.5)
    a.plot(x, [r["reward_best"] for r in s], color=AMBER, linewidth=1.6, marker="o", markersize=3.5, alpha=0.9, label="best in batch")
    a.plot(x, [r["reward_mean"] for r in s], color=CYAN, linewidth=2.6, label="batch mean")
    a.fill_between(x, 0, [r["reward_mean"] for r in s], color=CYAN, alpha=0.08)
    a.set_ylim(0, None)
    a.set_title("Reward per step (official verifier)", loc="left", color=INK, fontsize=14, pad=12)
    a.legend(frameon=False, loc="lower right", labelcolor=INK)
    b.plot(x, [100 * r["valid_rate"] for r in s], color=CYAN, linewidth=2.6)
    b.fill_between(x, 0, [100 * r["valid_rate"] for r in s], color=CYAN, alpha=0.08)
    b.set_ylim(0, 105)
    b.set_title("Valid (4,5)-sets per batch, %", loc="left", color=INK, fontsize=14, pad=12)
    fig.suptitle(f"Tinker RL on {L.get('base_model')}: learning to write {L.get('problem')} constructions  "
                 f"(run {L.get('run_id', '')}, {len(s)} steps)", x=0.065, ha="left", color=MUTED, fontsize=11.5, y=0.995)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    return True


# ------------------------------------------------------------------ main
def rewrite(text, blocks):
    missing = []
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.S)
        if not pat.search(text):
            missing.append(name)
            continue
        text = pat.sub(lambda m, body=body: f"{m.group(1)}\n{body}\n{m.group(3)}", text)
    return text, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if a file would change; write nothing")
    ap.add_argument("--no-plot", action="store_true", help="do not regenerate docs/assets/reward_curve.png")
    a = ap.parse_args()
    d = load_all()
    blocks = {k: f(d) for k, f in BLOCKS.items()}
    changed = []
    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        try:
            old = open(path).read()
        except OSError:
            print("skip (missing):", rel)
            continue
        new, missing = rewrite(old, blocks)
        used = [k for k in blocks if k not in missing]
        if new != old:
            changed.append(rel)
            if not a.check:
                with open(path, "w") as f:
                    f.write(new)
        print(f"{rel}: blocks {', '.join(used) or 'none'}: {'changed' if new != old else 'up to date'}")
    if not a.check and not a.no_plot:
        out = os.path.join(ROOT, "docs", "assets", "reward_curve.png")
        if plot(d, out):
            print("wrote", os.path.relpath(out, ROOT))
    if a.check and changed:
        print("stale:", ", ".join(changed))
        sys.exit(1)


if __name__ == "__main__":
    main()
