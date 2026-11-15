"""Adversarial tests added in review (offline, no paid calls; never touch the live data files or ledger).

Run:  cd ROOT && python3 -m pytest -q -p no:cacheprovider phoenixastar/tests_labs
"""
import json
import os
import sys
import threading
import time

import pytest

os.environ["PHOENIX_LABS_LEDGER"] = "0"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from phoenixastar import learning, memory_bench, sandboxes  # noqa: E402

LIVE_FILES = [os.path.join(ROOT, "data", f) for f in ("learning.json", "sandboxes.jsonl", "memory_benchmark.json")]


@pytest.fixture(autouse=True)
def _live_files_untouched():
    """Every test here must leave the real data files byte-for-byte alone."""
    before = {p: (os.path.getmtime(p), os.path.getsize(p)) for p in LIVE_FILES if os.path.exists(p)}
    yield
    after = {p: (os.path.getmtime(p), os.path.getsize(p)) for p in LIVE_FILES if os.path.exists(p)}
    assert before == after, "a test modified a live data file"


@pytest.fixture
def temp_ledger(tmp_path, monkeypatch):
    """A throwaway SQLite ledger, so decision logging can be exercised without the live DB."""
    from phoenixastar import config, ledger
    monkeypatch.setenv("PHOENIX_LABS_LEDGER", "1")
    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "ledger.sqlite"))
    monkeypatch.setattr(ledger, "_conn", None)
    yield ledger
    if ledger._conn is not None:
        ledger._conn.close()
    ledger._conn = None


# ------------------------------------------------------------------------------------------ sandboxes
def test_append_ids_unique_under_concurrency(tmp_path, monkeypatch):
    monkeypatch.setattr(sandboxes, "RUNS_PATH", str(tmp_path / "sb.jsonl"))
    out = []

    def w(i):
        out.append(sandboxes._append({"id": None, "problem": "sidon-45-set", "i": i})["id"])

    ts = [threading.Thread(target=w, args=(i,)) for i in range(40)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert sorted(out) == list(range(1, 41))
    assert sorted(r["id"] for r in sandboxes.list_runs(1000)) == list(range(1, 41))


def test_annotate_keeps_other_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(sandboxes, "RUNS_PATH", str(tmp_path / "sb.jsonl"))
    for _ in range(3):
        sandboxes._append({"id": None, "problem": "sidon-45-set", "decision_id": None})
    assert sandboxes.annotate(2, decision_id=77)
    assert not sandboxes.annotate(99, decision_id=1)
    runs = {r["id"]: r for r in sandboxes.list_runs()}
    assert set(runs) == {1, 2, 3} and runs[2]["decision_id"] == 77 and runs[1]["decision_id"] is None


def test_scrub_removes_keys_and_home():
    home = os.path.expanduser("~")
    s = sandboxes._scrub(f"Error code: 401 - Incorrect API key provided: sk-proj-abc123XYZ***wxyz at {home}/x.py "
                         "Authorization: Bearer abc.def-ghi")
    assert "sk-proj" not in s and "abc.def-ghi" not in s and home not in s and "[redacted]" in s


def _wait_idle():
    for _ in range(200):
        if not sandboxes.active_batches():
            return
        time.sleep(0.02)


def test_batch_ids_unique_when_started_back_to_back(monkeypatch):
    _wait_idle()
    ids = [sandboxes._register("sidon-45-set", 1) for _ in range(sandboxes.MAX_ACTIVE_BATCHES)]
    try:
        assert len(set(ids)) == len(ids) == len(sandboxes.active_batches())
    finally:
        with sandboxes._active_lock:
            for b in ids:
                sandboxes._active.pop(b, None)


def test_batch_limit_and_release(monkeypatch):
    _wait_idle()
    gate = threading.Event()
    monkeypatch.setattr(sandboxes, "run_batch", lambda p, n, c="", **kw: gate.wait(5) and [])
    for _ in range(sandboxes.MAX_ACTIVE_BATCHES):
        sandboxes.start_batch_async("sidon-45-set", 2)
    with pytest.raises(RuntimeError):
        sandboxes.start_batch_async("sidon-45-set", 2)
    assert len(sandboxes.active_batches()) == sandboxes.MAX_ACTIVE_BATCHES
    gate.set()
    for _ in range(100):
        if not sandboxes.active_batches():
            break
        time.sleep(0.05)
    assert sandboxes.active_batches() == []


def test_setup_failure_is_recorded_not_lost(tmp_path, monkeypatch):
    monkeypatch.setattr(sandboxes, "RUNS_PATH", str(tmp_path / "sb.jsonl"))

    def boom():
        raise RuntimeError("Incorrect API key provided: sk-proj-SECRETSECRET")

    monkeypatch.setattr(sandboxes, "_openai", boom)
    _wait_idle()
    res = sandboxes.run_batch("sidon-45-set", 3)
    assert [r["status"] for r in res] == ["error"] * 3
    assert all("SECRETSECRET" not in r["error"] for r in res)
    assert len(sandboxes.list_runs()) == 3 and sandboxes.active_batches() == []


def test_one_logs_decision_with_id(tmp_path, monkeypatch, temp_ledger):
    monkeypatch.setattr(sandboxes, "RUNS_PATH", str(tmp_path / "sb.jsonl"))
    info = sandboxes.problem_info("sidon-45-set")
    rec_sol = info["record"]["solution"]
    monkeypatch.setattr(sandboxes, "write_program",
                        lambda *a, **k: {"idea": "print the record", "code": "print(1)", "model": "m", "tokens": 5})
    monkeypatch.setattr(sandboxes, "run_in_sandbox", lambda code: {
        "rc": 0, "stdout": "progress\n" + json.dumps(rec_sol) + "\n", "stderr": "", "seconds": 1.0, "killed": False})
    r = sandboxes._one(None, info, {"name": "a", "idea": "b"}, 0, 1, "", "sb-test")
    assert r["status"] == "ok" and r["same_as_record"] is True and isinstance(r["decision_id"], int)
    d = temp_ledger.get_decision(r["decision_id"])
    assert d["agent"] == "sandbox" and d["action"] == "sandbox_run" and d["params"]["run_id"] == r["id"]
    assert d["outcome"]["observed"] == r["score"] and "record solution itself" in d["rationale"]
    stored = sandboxes.list_runs()[0]
    assert stored["decision_id"] == r["decision_id"]


def test_backfill_sets_decision_ids(tmp_path, monkeypatch, temp_ledger):
    p = tmp_path / "sb.jsonl"
    rec_sol = sandboxes.problem_info("sidon-45-set")["record"]["solution"]
    p.write_text("\n".join(json.dumps({"id": i, "problem": "sidon-45-set", "time": "2026-11-15T14:30:00Z",
                                       "status": "ok", "score": 4 / 7, "solution": rec_sol, "decision_id": None})
                           for i in (1, 2)) + "\n")
    monkeypatch.setattr(sandboxes, "RUNS_PATH", str(p))
    assert sandboxes.backfill_decisions() == 2
    runs = sandboxes.list_runs()
    assert all(isinstance(r["decision_id"], int) and r["same_as_record"] for r in runs)
    assert temp_ledger.get_decision(runs[0]["decision_id"])["time"] == "2026-11-15T14:30:00Z"
    assert sandboxes.backfill_decisions() == 0  # idempotent


def test_live_runs_file_contract():
    """The real data/sandboxes.jsonl rows have the API fields with the right types."""
    for r in sandboxes.list_runs(1000):
        assert isinstance(r["id"], int) and r["problem"] in sandboxes.SUPPORTED
        assert r["status"] in ("ok", "invalid", "timeout", "error")
        assert r["score"] is None or isinstance(r["score"], float)
        assert isinstance(r["seconds"], (int, float)) and isinstance(r["code"], str) and isinstance(r["time"], str)
        assert r["decision_id"] is None or isinstance(r["decision_id"], int)
        if r["status"] == "ok":
            assert sandboxes.verify(r["problem"], r["solution"])["score"] == r["score"]


# ------------------------------------------------------------------------------------------ learning
@pytest.fixture
def temp_learning(tmp_path, monkeypatch):
    path = tmp_path / "learning.json"
    monkeypatch.setattr(learning, "DATA_PATH", str(path))
    saved = learning._state
    yield path
    if learning._thread is not None:
        learning._thread.join(5)
    learning._state = saved


def test_persist_is_thread_safe(temp_learning):
    learning._state = learning._empty_state()
    errs = []

    def w():
        try:
            for _ in range(20):
                learning._persist()
        except Exception as e:  # noqa: BLE001
            errs.append(e)

    ts = [threading.Thread(target=w) for _ in range(8)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert not errs and json.load(open(temp_learning))["status"] == "idle"
    assert not [f for f in os.listdir(temp_learning.parent) if f.endswith(".tmp")]


def test_stale_running_file_is_not_running(temp_learning):
    temp_learning.write_text(json.dumps({"status": "running", "pid": os.getppid(), "steps": []}))
    assert learning._foreign_running()
    old = time.time() - learning.STALE_S - 5
    os.utime(temp_learning, (old, old))   # pid alive (our parent) but the file stopped being written
    assert not learning._foreign_running()
    with learning._lock:
        learning._load()
    assert learning._state["status"] == "error"


def test_failed_run_keeps_previous_run(temp_learning, monkeypatch):
    done = dict(learning._empty_state(), status="done", run_id="old", steps=[
        {"step": 1, "reward_mean": 0.1, "reward_best": 0.2, "valid_rate": 0.0, "time": "t"},
        {"step": 2, "reward_mean": 0.3, "reward_best": 0.4, "valid_rate": 0.5, "time": "t"}])
    temp_learning.write_text(json.dumps(done))

    def fail(steps, run_id):
        raise RuntimeError("tinker down, key tml-abcdefghijklmnop")

    monkeypatch.setattr(learning, "_train", fail)
    assert learning.start(3) is True
    learning._thread.join(5)
    st = learning.status()
    assert st["status"] == "done" and st["run_id"] == "old" and len(st["steps"]) == 2
    assert st["last_attempt"]["status"] == "error" and "tml-abc" not in st["last_attempt"]["error"]
    assert json.load(open(temp_learning))["run_id"] == "old"


def test_start_rejects_junk_and_double_start(temp_learning, monkeypatch):
    with pytest.raises(ValueError):
        learning.start("abc")
    gate = threading.Event()
    monkeypatch.setattr(learning, "_train", lambda steps, run_id: gate.wait(5))
    assert learning.start(2) is True
    st = learning.status()
    assert st["status"] == "running" and st["planned_steps"] == 2
    results = []
    ts = [threading.Thread(target=lambda: results.append(learning.start(2))) for _ in range(5)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert results == [False] * 5
    gate.set()


def test_live_learning_file_contract():
    st = json.load(open(os.path.join(ROOT, "data", "learning.json")))
    assert st["status"] in ("idle", "running", "done", "error")
    for row in st["steps"]:
        for k in ("reward_mean", "reward_best", "valid_rate"):
            assert isinstance(row[k], (int, float))
        assert isinstance(row["step"], int) and isinstance(row["time"], str)
    if st.get("eval"):
        for g in ("gen0", "genN"):
            assert isinstance(st["eval"][g]["score"], (int, float)) and isinstance(st["eval"][g]["valid_rate"], (int, float))
        assert isinstance(st["eval"]["heldout"], str)
    if st.get("best"):
        assert sandboxes.verify("sidon-45-set", st["best"]["solution"])["score"] == st["best"]["score"]


# ------------------------------------------------------------------------------------------ memory bench
def test_norm_caps_and_dedupes():
    facts = [{"id": "dup", "text": f"fact {i}", "time": f"2026-11-15T{i // 60:02d}:{i % 60:02d}:00Z"}
             for i in range(memory_bench.MAX_INDEX_FACTS + 40)]
    out = memory_bench._norm_facts(facts)
    assert len(out) == memory_bench.MAX_INDEX_FACTS and len({f["id"] for f in out}) == len(out)
    assert out[-1]["text"] == facts[-1]["text"]  # the most recent facts are kept
    q = memory_bench._question_facts(out)
    assert len(q) == memory_bench.MAX_QUESTION_FACTS and q[0] is out[0]


def test_start_async_rejects_too_few_facts():
    with pytest.raises(ValueError):
        memory_bench.start_async([{"text": "a"}, {"text": ""}])
    assert not memory_bench.running()


class _FakeSys:
    def __init__(self, name, facts, *a, **k):
        self.name, self.facts, self.cost_usd, self.setup, self.identity = name, facts, 0.0, {}, "phoenixastar-bench-test"

    def lookup(self, q):
        return "\n".join(f["text"] for f in self.facts)

    def ingest(self):
        return True

    def finish(self):
        pass


def _offline_bench(monkeypatch, tmp_path, questions, fail_every=0):
    monkeypatch.setattr(memory_bench, "OUT_PATH", str(tmp_path / "bench.json"))
    monkeypatch.setattr(memory_bench, "_client", lambda: None)
    monkeypatch.setattr(memory_bench, "PastDev", lambda facts: _FakeSys("past.dev", facts))
    monkeypatch.setattr(memory_bench, "Rag", lambda client, facts: _FakeSys("rag", facts))
    monkeypatch.setattr(memory_bench, "build_qa", lambda client, facts: (questions, {"input": 1, "output": 1}))
    import itertools
    counter = itertools.count(1)

    def answer(client, q, ctx):
        k = next(counter)
        if fail_every and k % fail_every == 0:
            raise TimeoutError("Request timed out (sk-proj-SECRET123456)")
        return "42", {"input": 100, "output": 5, "cached": 0}

    monkeypatch.setattr(memory_bench, "answer", answer)
    monkeypatch.setattr(memory_bench, "judge", lambda c, q, f, a: {"correct": a == "42", "reason": "ok",
                                                                   "usage": {"input": 1, "output": 1}})
    facts = [{"id": f"f{i}", "text": f"value is 42 ({i})", "time": f"2026-11-15T0{i}:00:00Z"} for i in range(5)]
    return memory_bench.run(facts, label="offline test")


def test_bench_survives_failed_calls(monkeypatch, tmp_path):
    qs = [{"question": f"q{i}", "answer": "42", "fact_ids": [f"f{i}"], "kind": "single"} for i in range(5)]
    b = _offline_bench(monkeypatch, tmp_path, qs, fail_every=4)
    assert {s["name"] for s in b["systems"]} == {"past.dev", "markdown", "rag"}
    assert sum(s["call_errors"] for s in b["systems"]) == 3       # 15 answer calls, every 4th fails
    assert all(0 < s["accuracy"] <= 1 and s["n"] == 5 for s in b["systems"])
    assert "SECRET123456" not in json.dumps(b)
    assert json.load(open(tmp_path / "bench.json"))["n_questions"] == 5


def test_bench_without_questions_keeps_previous(monkeypatch, tmp_path):
    (tmp_path / "bench.json").write_text(json.dumps({"systems": [], "time": "previous"}))
    with pytest.raises(RuntimeError):
        _offline_bench(monkeypatch, tmp_path, [])
    assert json.load(open(tmp_path / "bench.json"))["time"] == "previous"


def test_latest_reports_running_and_error(monkeypatch, tmp_path):
    p = tmp_path / "bench.json"
    p.write_text(json.dumps({"systems": [], "time": "t"}))
    monkeypatch.setattr(memory_bench, "OUT_PATH", str(p))
    monkeypatch.setattr(memory_bench, "run", lambda facts, label=None: (_ for _ in ()).throw(RuntimeError("boom")))
    assert memory_bench.start_async([{"text": "a"}, {"text": "b"}, {"text": "c"}]) is True
    for _ in range(100):
        if not memory_bench.running():
            break
        time.sleep(0.02)
    b = memory_bench.latest()
    assert b["running"] is False and "boom" in b["last_error"] and b["time"] == "t"
    memory_bench._run_info.clear()


def test_live_benchmark_file_contract():
    b = memory_bench.latest()
    if b is None:
        pytest.skip("no benchmark yet")
    assert isinstance(b["time"], str)
    for s in b["systems"]:
        assert s["name"] in ("past.dev", "markdown", "rag")
        for k in ("accuracy", "latency_ms", "cost_usd"):
            assert isinstance(s[k], (int, float))
        assert isinstance(s["n"], int) and s["n"] == b["n_questions"]
