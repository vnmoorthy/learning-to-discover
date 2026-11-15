"""Referee: a second frontier model (Claude Fable 5.2, via the local Claude Code CLI) reviews the proposer's
decisions before the planner executes them. Two different labs' models must agree before compute moves.

review(state_summary, decisions) -> list of {"index", "verdict": approve|veto|amend, "reason", "amended_params"?}
On any failure (CLI missing, timeout, bad JSON) the referee abstains ("abstain"), and the planner's own hard
limits still apply, so the loop never blocks on it.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time

MODEL = os.environ.get("LTD_REFEREE_MODEL", "claude-fable-5-2")
TIMEOUT_S = int(os.environ.get("LTD_REFEREE_TIMEOUT", "150"))

PROMPT = """You are the REFEREE of an autonomous mathematics research lab. A different model (the proposer) has
proposed actions for this cycle. Your job: protect the lab's compute and its scientific integrity.
Approve an action only if it is (1) consistent with the live evidence below, (2) likely to move a problem toward
beating its record or to produce a falsifiable, informative result, and (3) not wasteful (e.g. relaunching a
symmetry class already proved UNSAT, stopping the only run that is still improving, duplicating an identical run).
You may AMEND params of a launch if a clear improvement exists (only params already present).

LIVE STATE (compact):
{state}

PROPOSED ACTIONS (indexed):
{decisions}

Answer with ONLY a JSON object, no prose, exactly:
{{"verdicts": [{{"index": <int>, "verdict": "approve"|"veto"|"amend", "reason": "<one or two sentences citing the evidence>", "amended_params": {{...}} }}]}}
Include every index exactly once. amended_params only when verdict is amend."""


def available() -> bool:
    return shutil.which("claude") is not None


def review(state_summary: dict, decisions: list[dict]) -> dict:
    t0 = time.time()
    if not decisions:
        return {"verdicts": [], "model": MODEL, "latency_ms": 0, "status": "empty"}
    if not available():
        return {"verdicts": [{"index": i, "verdict": "abstain", "reason": "referee CLI not available"} for i in range(len(decisions))],
                "model": MODEL, "latency_ms": 0, "status": "unavailable"}
    prompt = PROMPT.format(state=json.dumps(state_summary, default=str)[:12000],
                           decisions=json.dumps([{"index": i, **{k: d.get(k) for k in ("problem", "action", "template", "params", "strategy_id", "rationale", "prediction", "n")}}
                                                 for i, d in enumerate(decisions)], default=str)[:12000])
    try:
        with tempfile.TemporaryDirectory() as tmp:     # empty cwd: no project files or instructions leak in
            r = subprocess.run(["claude", "-p", "--model", MODEL, "--output-format", "text", prompt],
                               capture_output=True, text=True, timeout=TIMEOUT_S, cwd=tmp)
        txt = r.stdout.strip()
        m = re.search(r"\{.*\}", txt, re.S)
        data = json.loads(m.group(0)) if m else {}
        verdicts = data.get("verdicts") or []
        seen = {v.get("index") for v in verdicts if isinstance(v, dict)}
        for i in range(len(decisions)):
            if i not in seen:
                verdicts.append({"index": i, "verdict": "abstain", "reason": "referee gave no verdict"})
        for v in verdicts:
            if v.get("verdict") not in ("approve", "veto", "amend", "abstain"):
                v["verdict"] = "abstain"
        return {"verdicts": sorted(verdicts, key=lambda v: v.get("index", 0)), "model": MODEL,
                "latency_ms": int((time.time() - t0) * 1000), "status": "ok" if m else "unparsed"}
    except subprocess.TimeoutExpired:
        return {"verdicts": [{"index": i, "verdict": "abstain", "reason": "referee timed out"} for i in range(len(decisions))],
                "model": MODEL, "latency_ms": int((time.time() - t0) * 1000), "status": "timeout"}
    except Exception as e:  # noqa: BLE001
        return {"verdicts": [{"index": i, "verdict": "abstain", "reason": f"referee error: {type(e).__name__}"} for i in range(len(decisions))],
                "model": MODEL, "latency_ms": int((time.time() - t0) * 1000), "status": "error"}


if __name__ == "__main__":
    demo = review({"no-three-in-line-75": {"record": 148, "rot180-150": {"runs": 26, "unsat": 0, "best_violated": 107}},
                   "spencer-discrepancy": {"record": 1.6977, "n20_D8_best_bad": 2592, "minutes_without_improvement": 70}},
                  [{"problem": "spencer-discrepancy", "action": "launch", "template": "spencer_gpu", "params": {"n": 20, "D": 8, "seed": 9},
                    "rationale": "more seeds"},
                   {"problem": "no-three-in-line-75", "action": "launch", "template": "nothree_sat", "params": {"sym": "rot180-150", "seed": 77},
                    "rationale": "best class, add seeds"}])
    print(json.dumps(demo, indent=1))
