"""Offline tests for the sponsor-lab modules (no paid API calls).

Run:  cd ROOT && python3 -m pytest -q ltd/tests_labs
Live smoke (one tiny Modal sandbox, ~15 s):  LTD_LIVE=1 python3 -m pytest -q ltd/tests_labs -k live
"""
import json
import os
import sys

import pytest

os.environ["LTD_LABS_LEDGER"] = "0"   # offline tests never write decisions into the live ledger
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ltd import learning, memory_bench, sandboxes  # noqa: E402

MA_TANG = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


# ------------------------------------------------------------------------------------------ sandboxes
def test_problem_info_all_supported():
    for slug in sandboxes.SUPPORTED:
        info = sandboxes.problem_info(slug)
        assert info["record"] and "evaluate" in info["verifier_src"]
    with pytest.raises(ValueError):
        sandboxes.problem_info("hadamard-det-51")


def test_verify_official_subprocess():
    ok = sandboxes.verify("sidon-45-set", {"elements": MA_TANG})
    assert ok["ok"] and abs(ok["score"] - 4 / 7) < 1e-12
    bad = sandboxes.verify("sidon-45-set", {"elements": list(range(14))})
    assert not bad["ok"] and "(4,5)" in bad["error"]
    ring = sandboxes.problem_info("ring-loading-15")["record"]["solution"]
    r = sandboxes.verify("ring-loading-15", ring)
    assert r["ok"] and abs(r["score"] - 1.125) < 1e-12


def test_beats_record_direction():
    sid = sandboxes.problem_info("sidon-45-set")
    assert sandboxes.beats_record(sid, 0.55) and not sandboxes.beats_record(sid, 4 / 7)
    sp = sandboxes.problem_info("spencer-discrepancy")
    assert sandboxes.beats_record(sp, 1.8) and not sandboxes.beats_record(sp, 1.6977)


def test_parse_last_line():
    out = 'progress 1\n{"elements": [1, 2]}\n'
    assert sandboxes._parse_solution(out, True)[0] == {"elements": [1, 2]}
    assert sandboxes._parse_solution('{"elements": [1]}\nTraceback', True)[0] is None
    assert sandboxes._parse_solution('{"elements": [1]}\nkilled', False)[0] == {"elements": [1]}


def test_same_as_record():
    rec = {"elements": MA_TANG}
    assert sandboxes._same({"elements": list(reversed(MA_TANG))}, rec)
    assert not sandboxes._same({"elements": MA_TANG[:-1]}, rec)


def test_list_runs_newest_first(tmp_path, monkeypatch):
    p = tmp_path / "sb.jsonl"
    p.write_text("\n".join(json.dumps({"id": i, "problem": "sidon-45-set"}) for i in (1, 3, 2)) + "\n")
    monkeypatch.setattr(sandboxes, "RUNS_PATH", str(p))
    assert [r["id"] for r in sandboxes.list_runs(2)] == [3, 2]


@pytest.mark.skipif(os.environ.get("LTD_LIVE") != "1", reason="set LTD_LIVE=1 for the Modal smoke test")
def test_live_modal_sandbox():
    run = sandboxes.run_in_sandbox('import json, numpy, numba; print(json.dumps({"elements": %s}))' % MA_TANG)
    assert run["rc"] == 0
    sol, _ = sandboxes._parse_solution(run["stdout"], True)
    assert sandboxes.verify("sidon-45-set", sol)["ok"]
    # network must be blocked inside the sandbox
    net = sandboxes.run_in_sandbox("import urllib.request as u; u.urlopen('https://example.com', timeout=5)")
    assert net["rc"] != 0


# ------------------------------------------------------------------------------------------ learning
def test_reward_shapes():
    rec = learning.reward("```json\n%s\n```" % MA_TANG, 14)
    assert rec["valid"] and abs(rec["ratio"] - 4 / 7) < 1e-12 and rec["reward"] > 1.5
    sidon = learning.reward(json.dumps([2 ** i for i in range(12)]), 12)
    assert sidon["valid"] and sidon["ratio"] == 1.0 and abs(sidon["reward"] - 0.5) < 1e-9
    squares = learning.reward(json.dumps([i * i for i in range(14)]), 14)
    assert not squares["valid"] and 0 < squares["reward"] < 0.3
    assert learning.reward("no list here")["reward"] == 0.0
    assert learning.reward("[1, 2, 3]")["reward"] == 0.0          # too small (< 12)
    assert learning.reward(json.dumps([1] * 13))["reward"] == 0.0  # duplicates
    # beating the record is worth much more than matching it
    assert rec["reward"] < 0.5 + 0.5 + 4 * 0.25 + 0.3 + 2.0


def test_count_3aps():
    assert learning.count_3aps([0, 1, 2, 4]) == 2
    assert learning.count_3aps([2 ** i for i in range(10)]) == 0


def test_status_shape():
    st = learning.status()
    for k in ("status", "base_model", "problem", "steps", "eval", "best"):
        assert k in st
    assert st["status"] in ("idle", "running", "done", "error")
    for row in st["steps"]:
        assert {"step", "reward_mean", "reward_best", "valid_rate", "time"} <= set(row)


# ------------------------------------------------------------------------------------------ memory bench
def test_norm_and_markdown():
    facts = memory_bench._norm_facts([{"text": "b", "time": "2026-11-15T02:00:00Z"},
                                      {"text": "a", "time": "2026-11-15T01:00:00Z", "id": "x/y"}, {"text": ""}])
    assert [f["text"] for f in facts] == ["a", "b"] and facts[0]["id"] == "x_y"
    md = memory_bench.Markdown(facts)
    assert "a" in md.lookup("anything") and md.lookup("q") == md.doc


def test_cost():
    assert abs(memory_bench._cost("gpt-5.4-mini", 1_000_000, 1_000_000) - 5.25) < 1e-9
    assert memory_bench._cost("unknown-model", 10, 10) == 0.0


def test_latest_shape():
    b = memory_bench.latest()
    if b is None:
        pytest.skip("no benchmark has been run yet")
    names = {s["name"] for s in b["systems"]}
    assert names == {"past.dev", "markdown", "rag"}
    for s in b["systems"]:
        assert {"name", "accuracy", "latency_ms", "cost_usd", "n"} <= set(s)
    assert isinstance(b["time"], str)


# ------------------------------------------------------------------------------------------ async wrappers
def test_async_wrappers_call_back(monkeypatch):
    import threading
    ev, got = threading.Event(), {}
    monkeypatch.setattr(sandboxes, "run_batch", lambda p, n, c="", **kw: [{"id": 1, "problem": p, "n": n}])
    sandboxes.start_batch_async("sidon-45-set", 3, callback=lambda r: (got.update(sb=r), ev.set()))
    assert ev.wait(5) and got["sb"][0]["n"] == 3
    with pytest.raises(ValueError):
        sandboxes.start_batch_async("not-a-problem", 1)

    ev.clear()
    gate = threading.Event()

    def fake_run(facts, label=None):
        gate.wait(5)
        return {"systems": [], "time": "t", "n": len(facts)}

    monkeypatch.setattr(memory_bench, "run", fake_run)
    three = [{"text": "a"}, {"text": "b"}, {"text": "c"}]
    assert memory_bench.start_async(three, callback=lambda r: (got.update(mb=r), ev.set())) is True
    assert memory_bench.running()
    assert memory_bench.start_async(three) is False  # ignored while one is running
    gate.set()
    assert ev.wait(5) and got["mb"]["n"] == 3
    for _ in range(50):
        if not memory_bench.running():
            break
        import time
        time.sleep(0.05)
    assert not memory_bench.running()


def test_learning_start_refuses_when_running(monkeypatch):
    import threading
    gate = threading.Event()
    monkeypatch.setattr(learning, "_runner", lambda steps, run_id: gate.wait(5))
    monkeypatch.setattr(learning, "_persist", lambda: None)
    monkeypatch.setattr(learning, "_foreign_running", lambda: False)
    assert learning.start(2) is True
    assert learning.start(2) is False
    assert learning.status()["status"] == "running"
    gate.set()
    learning._thread.join(5)
    learning._load()  # restore the persisted run in memory
