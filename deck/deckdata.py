"""Loads the static snapshot (web/public/data/*.json) and derives every number the deck and storyboard show.

Nothing here is hard-coded: if the snapshot is regenerated, re-running build_deck.py picks up the new numbers.
Fields that newer snapshots may add (referee verdicts, Modal fleet, Devin toolsmith) are detected defensively and
reported as None / 0 when the snapshot does not contain them, so the slides say "not in this snapshot" instead of
inventing a value.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from collections import Counter
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "web", "public", "data")
GALLERY = os.path.join(ROOT, "web", "public", "gallery")
REPO_URL = "https://github.com/vnmoorthy/learning-to-discover"

SHORT = {
    "no-three-in-line-75": "No-three-in-line 75×75",
    "spencer-discrepancy": "Spencer discrepancy",
    "hadamard-det-51": "Hadamard max-det, order 51",
    "sidon-45-set": "Sidon (4,5)-sets",
    "two-deletion-code-16": "Two-deletion code, n=16",
    "snake-in-the-box-13": "Snake-in-the-box Q13",
    "ring-loading-15": "Ring loading, 15 pairs",
}
TINY = {
    "no-three-in-line-75": "no-three",
    "spencer-discrepancy": "spencer",
    "hadamard-det-51": "hadamard",
    "sidon-45-set": "sidon",
    "two-deletion-code-16": "two-del",
    "snake-in-the-box-13": "snake",
    "ring-loading-15": "ring",
}
METRIC_LABEL = {
    "min_violated_lines": "collinear lines left",
    "bad_vectors": "bad sign vectors left",
    "best_log10": "live log10|det|",
    "best_size": "live code size",
    "best_score": "live score",
    "best_length": "live snake length",
}


def _load(name, default=None):
    p = os.path.join(DATA, name)
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return default


def fmt(v, digits=7):
    """Compact number: integers stay integers, floats keep `digits` significant digits."""
    if v is None:
        return "–"
    try:
        f = float(v)
    except Exception:  # noqa: BLE001
        return str(v)
    if abs(f - round(f)) < 1e-12 and abs(f) < 1e15:
        return f"{int(round(f)):,}"
    return f"{f:.{digits}g}"


def pct(v, nd=0):
    return "–" if v is None else f"{100 * float(v):.{nd}f}%"


def short(slug):
    return SHORT.get(slug, slug or "lab-wide")


def clip(text, n):
    """Cut at a sentence or word boundary, never mid-word."""
    text = " ".join((text or "").split())
    if len(text) <= n:
        return text
    cut = text[:n]
    dot = max(cut.rfind(". "), cut.rfind("; "))
    if dot > n * 0.55:
        return cut[:dot + 1] + " …"
    return cut[:cut.rfind(" ")] + " …"


def _pt(iso):
    try:
        t = dt.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=dt.timezone.utc)
        return t.astimezone(ZoneInfo("America/Los_Angeles"))
    except Exception:  # noqa: BLE001
        return None


def pt_label(iso, with_date=True):
    t = _pt(iso)
    if not t:
        return str(iso or "unknown time")
    h = t.strftime("%I:%M %p").lstrip("0")
    return (t.strftime("%b %d, ") + h + " PT") if with_date else (h + " PT")


def _referee_index(decisions):
    """Verdicts logged as separate decisions with agent == 'referee'."""
    idx = {}
    for d in decisions:
        if (d.get("agent") or "").lower() != "referee":
            continue
        p = d.get("params") or {}
        o = d.get("outcome") or {}
        verdict = p.get("verdict") or (d.get("action") if d.get("action") in ("approve", "veto", "amend", "abstain", "approved", "vetoed", "amended") else None) or o.get("verdict")
        rec = {"verdict": verdict, "reason": p.get("reason") or d.get("rationale") or "", "model": d.get("model") or p.get("model"), "id": d.get("id")}
        for key in ("proposer_decision", "decision_id", "decision", "target"):
            if isinstance(p.get(key), int):
                idx[p[key]] = rec
        for key in ("proposer_decisions", "decision_ids"):
            for i in p.get(key) or []:
                idx[i] = rec
    return idx


def referee_of(d, idx):
    for holder in (d, d.get("params") or {}, d.get("outcome") or {}):
        r = holder.get("referee") if isinstance(holder, dict) else None
        if isinstance(r, dict) and r.get("verdict"):
            return {"verdict": r.get("verdict"), "reason": r.get("reason") or "", "model": r.get("model"), "id": d.get("id")}
    return idx.get(d.get("id"))


def _norm_verdict(v):
    v = (v or "").lower()
    if v.startswith("approv"):
        return "approve"
    if v.startswith("veto"):
        return "veto"
    if v.startswith("amend"):
        return "amend"
    if v.startswith("abstain"):
        return "abstain"
    return v or None


def _modal_fleet(state, decisions):
    comp = state.get("compute") or {}
    raw = None
    for k, v in comp.items():
        if "modal" in k.lower() or "fleet" in k.lower():
            raw = v
            break
    if raw is None:
        raw = state.get("modal") or state.get("fleet")
    n = None
    if isinstance(raw, list):
        n = len(raw)
    elif isinstance(raw, dict):
        for k in ("containers", "running", "active", "procs", "workers", "count"):
            v = raw.get(k)
            if isinstance(v, (int, float)):
                n = int(v)
                break
            if isinstance(v, list):
                n = len(v)
                break
    elif isinstance(raw, (int, float)):
        n = int(raw)
    strat = 0
    for p in state.get("problems") or []:
        for s in p.get("strategies") or []:
            if str(s.get("where") or s.get("resource") or "").lower() == "modal" or str(s.get("id", "")).startswith("modal"):
                strat += 1
    launches = sum(1 for d in decisions
                   if d.get("action") == "launch" and d.get("agent") in ("executor", "planner")
                   and "modal" in json.dumps(d.get("params") or {}).lower())
    if n is None and strat:
        n = strat
    if n is None and not launches:
        return None
    return {"containers": n, "strategies": strat, "launches": launches}


def _toolsmith(state, decisions):
    rows = [d for d in decisions if (d.get("agent") or "").lower() in ("toolsmith", "devin")
            or "toolsmith" in (d.get("action") or "").lower() or "devin" in (d.get("action") or "").lower()]
    sess = state.get("toolsmith") if isinstance(state.get("toolsmith"), (list, dict)) else None
    if isinstance(sess, dict):
        sess = sess.get("sessions")
    if not rows and not sess:
        return None
    blob = json.dumps(rows).lower()
    out = {"events": len(rows), "requested": 0, "adopted": 0, "rejected": 0, "last": None}
    if sess:
        out["requested"] = len(sess)
        out["adopted"] = sum(1 for s in sess if s.get("status") == "adopted" or s.get("adopted"))
        out["rejected"] = sum(1 for s in sess if s.get("status") == "rejected")
    else:
        for d in rows:
            a = (d.get("action") or "").lower()
            st = str((d.get("params") or {}).get("status") or "").lower()
            if "request" in a or "commission" in a:
                out["requested"] += 1
            if "adopt" in a or st == "adopted":
                out["adopted"] += 1
            if "reject" in a or st == "rejected":
                out["rejected"] += 1
        if not out["requested"]:
            out["requested"] = max(1, out["adopted"] + out["rejected"]) if ("devin" in blob or rows) else 0
    if rows:
        d = rows[0]
        out["last"] = {"id": d.get("id"), "problem": d.get("problem"), "text": d.get("rationale") or ""}
    return out


def _featured(decisions, ref_idx, lit_followups):
    best, best_score = None, -1
    n = len(decisions)
    for i, d in enumerate(decisions):                      # newest first
        if d.get("agent") != "proposer" or len(d.get("rationale") or "") < 60:
            continue
        verdict = ((d.get("outcome") or {}).get("verdict") or "")
        s = (4 if d.get("sources") else 0) + (3 if referee_of(d, ref_idx) else 0) + (2 if d.get("prediction") else 0) \
            + (1 if verdict in ("confirmed", "refuted") else 0) + (0.5 if d.get("id") in lit_followups else 0) + 0.4 * (n - i) / n
        if s > best_score:
            best, best_score = d, s
    return best


def load():
    state = _load("state.json", {}) or {}
    decisions = _load("decisions.json", []) or []
    memory = _load("memory.json", {}) or {}
    learning = _load("learning.json", {}) or {}
    sandboxes = _load("sandboxes.json", []) or []
    literature = _load("literature.json", []) or []
    try:
        gallery = json.load(open(os.path.join(GALLERY, "gallery.json")))
    except Exception:  # noqa: BLE001
        gallery = _load("gallery.json", []) or []
    details = {}
    pdir = os.path.join(DATA, "problems")
    if os.path.isdir(pdir):
        for fn in os.listdir(pdir):
            if fn.endswith(".json"):
                details[fn[:-5]] = _load(os.path.join("problems", fn), {})

    D = {"state": state, "decisions": decisions, "memory": memory, "learning": learning, "sandboxes": sandboxes,
         "literature": literature, "gallery": gallery, "details": details}

    snap = (state.get("snapshot") or {}).get("generated_at") or state.get("now")
    D["snap_iso"] = snap
    D["asof"] = pt_label(snap)
    D["asof_short"] = pt_label(snap, with_date=False)
    D["label"] = (state.get("snapshot") or {}).get("label") or "snapshot"
    D["totals"] = state.get("totals") or {}
    D["loop"] = state.get("loop") or {}
    D["interval_min"] = max(1, round((D["loop"].get("interval_s") or 300) / 60))
    D["proposer_model"] = D["loop"].get("proposer_model") or "gpt-6-astra"

    # ---- compute
    comp = state.get("compute") or {}
    gpus = comp.get("gpus") or []
    D["gpus"] = gpus
    D["gpu_busy"] = sum(1 for g in gpus if (g.get("util") or 0) >= 50)
    D["cpus"] = comp.get("cpus") or 0
    D["load1"] = comp.get("load1")
    D["cpu_procs"] = comp.get("cpu_procs") or {}
    D["cpu_total"] = sum(D["cpu_procs"].values())
    D["modal"] = _modal_fleet(state, decisions)

    # ---- problems
    probs = state.get("problems") or []
    D["problems"] = probs
    D["records"] = [p for p in probs if p.get("beats_record")]
    D["active"] = [p for p in probs if (p.get("compute") or {}).get("cpu_procs") or (p.get("compute") or {}).get("gpus")]
    D["negatives"] = [p for p in probs if p.get("status") == "proved-negative" or p.get("known_negative")]
    D["strategies_running"] = sum(len(p.get("strategies") or []) for p in probs)

    # ---- decisions / rigour
    ref_idx = _referee_index(decisions)
    D["ref_idx"] = ref_idx
    by_agent = Counter(d.get("agent") for d in decisions)
    D["by_agent"] = by_agent
    D["n_decisions"] = D["totals"].get("decisions") or len(decisions)
    D["verifier_checks"] = sum(1 for d in decisions if d.get("agent") == "critic" and (d.get("action") or "").startswith(("verif", "record")))
    scored = [d for d in decisions if d.get("action") == "score_prediction"]
    if scored:
        D["pred_confirmed"] = sum(1 for d in scored if (d.get("outcome") or {}).get("verdict") == "confirmed")
        D["pred_refuted"] = sum(1 for d in scored if (d.get("outcome") or {}).get("verdict") == "refuted")
    else:
        withp = [d for d in decisions if d.get("prediction")]
        D["pred_confirmed"] = sum(1 for d in withp if (d.get("outcome") or {}).get("verdict") == "confirmed")
        D["pred_refuted"] = sum(1 for d in withp if (d.get("outcome") or {}).get("verdict") == "refuted")
    D["pred_made"] = sum(1 for d in decisions if d.get("prediction"))
    D["pred_pending"] = sum(1 for d in decisions if d.get("prediction") and (d.get("outcome") or {}).get("verdict") == "pending")
    D["planner_rejects"] = sum(1 for d in decisions if d.get("agent") == "planner" and d.get("action") == "reject")
    D["stops"] = sum(1 for d in decisions if d.get("agent") == "executor" and d.get("action") == "stop")
    D["errors"] = sum(1 for d in decisions if d.get("action") == "error")
    verdicts = Counter()
    for d in decisions:
        if d.get("agent") == "proposer":
            r = referee_of(d, ref_idx)
            if r:
                verdicts[_norm_verdict(r.get("verdict"))] += 1
    if not verdicts:
        for r in {id(v): v for v in ref_idx.values()}.values():
            verdicts[_norm_verdict(r.get("verdict"))] += 1
    D["referee"] = dict(verdicts) if verdicts else None
    D["toolsmith"] = _toolsmith(state, decisions)

    lit_follow = {}
    for d in decisions:
        if d.get("agent") == "literature":
            pid = (d.get("params") or {}).get("proposer_decision")
            if pid is not None:
                lit_follow[pid] = d
    feat = _featured(decisions, ref_idx, lit_follow)
    D["featured"] = feat
    D["featured_referee"] = referee_of(feat, ref_idx) if feat else None
    D["featured_lit"] = lit_follow.get(feat.get("id")) if feat else None
    # a real prediction to show next to the card: the featured one, else the newest scored one, else the newest
    pred = None
    if feat and feat.get("prediction"):
        pred = {"d": feat, "score": None}
    else:
        by_id = {d.get("id"): d for d in decisions}
        for sc in scored:
            src = by_id.get((sc.get("params") or {}).get("decision_id"))
            if src and src.get("prediction"):
                pred = {"d": src, "score": sc}
                break
        if not pred:
            for d in decisions:
                if d.get("prediction") and d.get("agent") == "proposer":
                    pred = {"d": d, "score": None}
                    break
    D["pred_card"] = pred
    # a planner follow-up on the featured decision (deterministic layer), if any
    D["featured_planner"] = next((d for d in decisions if feat and d.get("agent") in ("planner", "executor")
                                  and (d.get("params") or {}).get("proposer_decision") == feat.get("id")), None)

    # ---- literature
    D["n_sources"] = D["totals"].get("sources") or len(literature)
    D["n_cited"] = sum(1 for x in literature if x.get("cited_by"))
    D["exa_searches"] = by_agent.get("literature", 0)

    # ---- memory
    facts = memory.get("facts") or []
    links = memory.get("links") or []
    D["n_facts"] = D["totals"].get("facts") or len(facts)
    D["n_agents"] = len(memory.get("agents") or [])
    D["cross_reads"] = sum(1 for link in links if link.get("from_agent") != link.get("to_agent"))
    bench = memory.get("benchmark") or None
    D["bench"] = bench
    D["bench_systems"] = {s.get("name"): s for s in (bench or {}).get("systems") or []}

    # ---- learning
    steps = learning.get("steps") or []
    D["steps"] = steps
    ev = learning.get("eval") or {}
    D["eval"] = ev
    D["base_model"] = learning.get("base_model") or "Qwen/Qwen3-8B"
    D["learn_problem"] = learning.get("problem")
    if steps:
        k = max(1, min(3, len(steps) // 4 or 1))
        D["reward_first"] = sum(s.get("reward_mean") or 0 for s in steps[:k]) / k
        D["reward_last"] = sum(s.get("reward_mean") or 0 for s in steps[-k:]) / k
        D["valid_first"] = sum(s.get("valid_rate") or 0 for s in steps[:k]) / k
        D["valid_last"] = sum(s.get("valid_rate") or 0 for s in steps[-k:]) / k
    D["learn_minutes"] = None
    a, b = _pt(learning.get("started_at")), _pt(learning.get("finished_at"))
    if a and b:
        D["learn_minutes"] = round((b - a).total_seconds() / 60, 1)

    # ---- sandboxes
    D["n_sandboxes"] = D["totals"].get("sandboxes_run") or len(sandboxes)
    D["sb_ok"] = sum(1 for s in sandboxes if s.get("status") == "ok")
    D["sb_problems"] = sorted({s.get("problem") for s in sandboxes if s.get("problem")})
    D["sb_matched_record"] = 0
    D["sb_beat"] = sum(1 for s in sandboxes if s.get("beats_record"))
    rec = {p["slug"]: p for p in probs}
    for s in sandboxes:
        p = rec.get(s.get("problem"))
        if p and s.get("score") is not None and abs(float(s["score"]) - float(p["record"]["score"])) < 1e-9:
            D["sb_matched_record"] += 1
    return D


def bench_sentence(D):
    """One honest sentence about the memory benchmark, whatever it says."""
    S = D["bench_systems"]
    if not S or "past.dev" not in S:
        return "The memory benchmark has not run in this snapshot."
    pd = S["past.dev"]
    best = max(S.values(), key=lambda s: s.get("accuracy") or 0)
    n = (D["bench"] or {}).get("n_questions") or pd.get("n")
    nf = (D["bench"] or {}).get("n_facts")
    cpq = {k: (v.get("cost_per_question_usd") or ((v.get("cost_usd") or 0) / max(1, v.get("n") or 1))) for k, v in S.items()}
    cheapest = min(cpq, key=cpq.get)
    if best is pd or abs((best.get("accuracy") or 0) - (pd.get("accuracy") or 0)) < 1e-9:
        head = f"past.dev is the most accurate memory on {n} questions ({pct(pd.get('accuracy'))})"
    else:
        head = (f"On {n} questions over {nf} real lab facts, {best['name']} is the most accurate ({pct(best.get('accuracy'))}); "
                f"past.dev scores {pct(pd.get('accuracy'))}")
    tail = f"; {cheapest} is cheapest per question" + (" and we report that as measured." if best is not pd else ".")
    return head + tail


if __name__ == "__main__":
    d = load()
    print(json.dumps({k: d[k] for k in ("asof", "totals", "gpu_busy", "cpu_total", "modal", "referee", "toolsmith", "verifier_checks",
                                        "pred_confirmed", "pred_refuted", "pred_made", "planner_rejects", "cross_reads", "n_cited")}, indent=1, default=str))
    print("featured:", d["featured"] and d["featured"]["id"], "| pred card:", d["pred_card"] and d["pred_card"]["d"]["id"])
    print(bench_sentence(d))
