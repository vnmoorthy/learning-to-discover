"""The autonomous cycle:
telemetry -> critic(found + predictions) -> memory (problem agents write + read) -> literature (Exa, if stalled)
-> proposer (LLM) -> planner (validate, provable kills, refill idle capacity) -> execute (box / sandboxes) -> ledger.

Runs in a background thread inside the server. Pause / resume / run-now. A failing cycle never kills the thread:
the error is logged as a decision (agent "system", action "error").
"""
import concurrent.futures as cf
import json
import os
import threading
import time
import traceback

from . import config, critic, events, ledger, literature, memory, monitor, planner, proposer

PHASES = ["idle", "telemetry", "critic", "memory", "literature", "propose", "referee", "plan", "execute"]
TEST_MODE = os.environ.get("PHOENIX_TEST_MODE", "0") == "1"   # launches get test- ids; stops of non-test runs are dry-run


class Loop:
    def __init__(self):
        self.status = "running" if config.LOOP_AUTOSTART else "paused"
        self.cycle = ledger.max_cycle()
        self.phase = "idle"
        self.interval_s = config.LOOP_INTERVAL_S
        self.started_at = ledger.now()
        self.next_cycle_at = time.time() + config.FIRST_CYCLE_DELAY_S
        self._wake = threading.Event()
        self._force = False
        self._busy = threading.Lock()
        self._thread = None
        self.last = None
        self.locked_out = None      # reason string when another server instance owns the loop for this DB

    # ---------------- control
    def view(self):
        v = {"status": self.status, "cycle": self.cycle, "phase": self.phase,
             "next_cycle_at": ledger.iso(self.next_cycle_at) if (self.status == "running" and self.next_cycle_at) else None,
             "interval_s": self.interval_s, "proposer_model": config.PROPOSER_MODEL, "started_at": self.started_at,
             "test_mode": TEST_MODE}
        if self.locked_out:
            v["locked_out"] = self.locked_out
        return v

    def lock_out(self, why):
        """This process may serve the API but must never run cycles (another instance owns the loop)."""
        self.locked_out = why
        self.status = "paused"

    def start(self):
        try:
            from . import fleet
            n = fleet.bootstrap()
            if n:
                did = ledger.add_decision(self.cycle, "executor", "adopt", None, {"where": "modal", "count": n},
                                          f"Adopted {n} Modal fleet containers launched before the loop managed the fleet "
                                          f"(two-deletion, Sidon, snake and no-three-in-line CPU searches).")
                events.publish("decision", ledger.get_decision(did))
        except Exception as e:  # noqa: BLE001
            events.log(f"modal fleet bootstrap failed: {e}", "warn")
        if self._thread is None:
            self._thread = threading.Thread(target=self._run, name="phoenixastar-loop", daemon=True)
            self._thread.start()

    def pause(self):
        self.status = "paused"
        events.publish("phase", {"phase": self.phase, "cycle": self.cycle, "status": self.status})

    def resume(self):
        if self.locked_out:
            events.log(f"resume ignored: {self.locked_out}", "warn")
            return
        self.status = "running"
        self.next_cycle_at = time.time() + 5
        self._wake.set()
        events.publish("phase", {"phase": self.phase, "cycle": self.cycle, "status": self.status})

    def run_now(self):
        if self.locked_out:
            events.log(f"run-now ignored: {self.locked_out}", "warn")
            return
        self._force = True
        self._wake.set()

    def _run(self):
        while True:
            try:
                wait = max(0.0, self.next_cycle_at - time.time()) if self.status == "running" else 3600
                self._wake.wait(timeout=min(wait, 30))
                self._wake.clear()
                if self._force or (self.status == "running" and time.time() >= self.next_cycle_at):
                    self._force = False
                    self.run_cycle()
                    self.next_cycle_at = time.time() + self.interval_s
            except Exception as e:  # noqa: BLE001 - the loop thread must never die (e.g. a locked DB outside _cycle)
                events.log(f"loop thread error: {type(e).__name__}: {e}", "error")
                self.next_cycle_at = time.time() + 60
                time.sleep(5)

    def _phase(self, ph):
        self.phase = ph
        events.publish("phase", {"phase": ph, "cycle": self.cycle})

    # ---------------- one cycle
    def run_cycle(self):
        if self.locked_out or not self._busy.acquire(blocking=False):
            return None
        try:
            self.cycle = max(self.cycle, ledger.max_cycle()) + 1
            c = self.cycle
            t0 = time.time()
            try:
                self.last = self._cycle(c)
            except Exception as e:  # noqa: BLE001
                tb = traceback.format_exc()
                did = ledger.add_decision(c, "system", "error", None, {"traceback": tb[-2000:]},
                                          f"Cycle {c} failed in phase {self.phase}: {type(e).__name__}: {e}")
                events.publish("decision", ledger.get_decision(did))
                events.log(f"cycle {c} failed: {e}", "error")
                self.last = {"error": str(e)}
            ledger.kv_set("last_cycle", {"cycle": c, "seconds": round(time.time() - t0, 1), "time": ledger.now()})
            return self.last
        finally:
            self._phase("idle")
            self._busy.release()

    def _cycle(self, c):
        res = {"cycle": c}
        # 1. telemetry ---------------------------------------------------------
        self._phase("telemetry")
        snap = monitor.poll(c, artifacts=True)
        if snap is None:
            did = ledger.add_decision(c, "system", "error", None, {"box": "offline"},
                                      f"Cycle {c}: telemetry unavailable ({monitor.current().get('error')}); no actions taken.")
            events.publish("decision", ledger.get_decision(did))
            return {"cycle": c, "error": "telemetry unavailable"}
        # 2. critic ------------------------------------------------------------
        self._phase("critic")
        res["verified"] = critic.process_queue(c, budget_s=180)
        res["predictions"] = critic.score_predictions(c, monitor.current()["metrics"])
        threading.Thread(target=self._toolsmith_tick, args=(c,), daemon=True).start()
        an = planner.analyze()
        # 3. memory: every problem agent writes what it sees, then reads what the others wrote ---------------
        self._phase("memory")
        facts, writes = self._memory(c, an)
        # 4. literature (Exa) for stalled problems ------------------------------
        self._phase("literature")
        cards = self._literature(c, an)
        # 5. propose -----------------------------------------------------------
        self._phase("propose")
        state = proposer.build_state(an, facts, cards, c)
        try:
            decs, meta = proposer.propose(state)
        except Exception as e:  # noqa: BLE001 - the deterministic planner still runs (kills, refill)
            did = ledger.add_decision(c, "system", "error", None, {"phase": "propose"},
                                      f"Proposer failed ({type(e).__name__}: {str(e)[:300]}); continuing with the "
                                      f"deterministic planner only (provable kills + refill).")
            events.publish("decision", ledger.get_decision(did))
            decs, meta = [], {"model": None, "tokens": None, "latency_ms": None, "summary": "", "error": str(e)}
        pids = {}
        share = int((meta["tokens"] or 0) / max(1, len(decs))) if meta.get("tokens") else None
        reads_by = {}
        for d in decs:
            params = {k: d.get(k) for k in ("template", "params", "count", "strategy_ids", "stop_filter", "queries", "n")
                      if d.get(k) not in (None, [], {})}
            if d.get("prediction"):
                # the metric's value now: the critic scores the prediction against it (no change predicted = trivial)
                base = critic.observe(str(d["prediction"].get("metric", "")), monitor.current()["metrics"], d["problem"])
                if isinstance(base, (int, float)):
                    params["baseline"] = base
            did = ledger.add_decision(c, "proposer", d["action"], d["problem"], params, d.get("rationale", ""),
                                      d.get("prediction"), sources=d.get("cite"), memory_reads=d.get("memory_used"),
                                      model=meta["model"], tokens=share, latency_ms=meta["latency_ms"])
            pids[id(d)] = did
            if d.get("memory_used"):
                memory.mark_read(d["memory_used"], "proposer", "past.dev", did)
                reads_by.setdefault(d["problem"], []).extend(d["memory_used"])
            events.publish("decision", ledger.get_decision(did))
        if meta.get("error"):
            events.log(f"proposer fell back: {meta['error']}", "warn")
        res["proposer"] = {"model": meta["model"], "tokens": meta["tokens"], "latency_ms": meta["latency_ms"],
                           "summary": meta["summary"], "n": len(decs)}
        # 5b. referee: a second frontier model (Claude Fable 5.2) must agree before compute moves ----------
        if decs:
            self._phase("referee")
            decs, res["referee"] = self._referee(c, decs, pids, state)
        # 6. plan ---------------------------------------------------------------
        self._phase("plan")
        actions, rejections = planner.plan(decs, an, c, test=TEST_MODE)
        for rj in rejections:
            did = ledger.add_decision(c, "planner", "reject", rj["decision"]["problem"],
                                      {"proposer_decision": pids.get(id(rj["decision"])), "action": rj["decision"]["action"]},
                                      f"Planner rejected (part of) proposer decision #{pids.get(id(rj['decision']))}: {rj['reason']}")
            events.publish("decision", ledger.get_decision(did))
        if TEST_MODE:
            actions = self._dry_run_stops(actions, c, pids)
        # 7. execute ------------------------------------------------------------
        self._phase("execute")
        results = planner.execute(actions, c, pids)
        # a prediction attached to an action that never ran cannot be scored
        done = {r["src"] for r in results if r.get("src") and r.get("ok")}
        rej = {pids.get(id(rj["decision"])): rj["reason"] for rj in rejections}
        for d in decs:
            did = pids.get(id(d))
            if d.get("prediction") and did not in done:
                why = rej.get(did) or ("dry run (test mode)" if TEST_MODE and d["action"] == "stop" else "not executed")
                ledger.update_decision(did, outcome={"observed": None, "verdict": "n/a", "note": f"not executed: {why}"[:300]})
        res["actions"] = [{"kind": a["kind"], "agent": a["agent"], "problem": a["problem"],
                           "n": len(a.get("items") or a.get("recs") or [])} for a in actions]
        res["results"] = [{k: r.get(k) for k in ("kind", "ok", "ids", "errors", "decision_id")} for r in results]
        # memory write: each problem agent records what was decided for it (and what the planner did with it)
        rej_by = {}
        for rj in rejections:
            rej_by.setdefault(rj["decision"]["problem"], []).append(rj["reason"][:160])
        by_prob = {}
        for d in decs:
            by_prob.setdefault(d["problem"], []).append(d)
        for slug, ds in by_prob.items():
            parts = []
            for d in ds:
                what = d["action"] + (f" {d.get('template')}" if d.get("template") else "")
                if d.get("count"):
                    what += f" x{d['count']}"
                if d.get("stop_filter"):
                    what += f" {json.dumps(d['stop_filter'], sort_keys=True)}"
                if d.get("params") and d["action"] == "launch":
                    what += f" {json.dumps(d['params'], sort_keys=True)[:120]}"
                pr = d.get("prediction")
                parts.append(f"#{pids.get(id(d))} {what}: {d.get('rationale', '')[:200]}"
                             + (f" [predicts {pr['metric']} -> {pr['expected']} in {pr['horizon_min']} min]" if pr else ""))
            txt = f"[cycle {c}] Decisions: " + " | ".join(parts)
            if rej_by.get(slug):
                txt += " | Planner: " + "; ".join(rej_by[slug])
            writes.append(memory.write(f"agent:{slug}", slug, txt[:1500], ["decision"]))
        # memory write: the proposer's plan for the next agents to read
        if decs:
            txt = f"Cycle {c} plan ({meta['model']}): {meta['summary'][:400]}"
            fid = memory.write("proposer", None, txt, ["plan"])
            writes.append(fid)
        # refresh telemetry so the UI shows the new allocation right away
        if any(r["kind"] in ("launch", "stop") and r["ok"] for r in results):
            time.sleep(2)
            monitor.poll(c)
        return res

    def _referee(self, c, decs, pids, state):
        from . import referee
        summ = {p["slug"]: {k: p.get(k) for k in ("record", "metric", "status", "best_age_min", "rate_1h", "procs", "gpus",
                                                   "sat_classes", "modal_runs_total", "our_best_verified")}
                for p in state["problems"]}
        summ["_budget"] = state.get("budget")
        rv = referee.review(summ, decs)
        kept, judged, vetoed, amended = [], set(), 0, 0
        for v in rv["verdicts"]:
            i = v.get("index")
            if not isinstance(i, int) or not 0 <= i < len(decs):
                continue
            judged.add(i)
            d = decs[i]
            src = pids.get(id(d))
            verdict = v.get("verdict", "abstain")
            params = {"proposer_decision": src, "status": rv["status"]}
            if verdict == "amend" and isinstance(v.get("amended_params"), dict):
                params["amended_params"] = v["amended_params"]
            did = ledger.add_decision(c, "referee", verdict, d["problem"], params,
                                      f"{rv['model']} on proposer decision #{src} ({d['action']}): {v.get('reason', '')}"[:1200],
                                      model=rv["model"], latency_ms=rv["latency_ms"])
            events.publish("decision", ledger.get_decision(did))
            if verdict == "veto":
                vetoed += 1
                if d.get("prediction"):
                    ledger.update_decision(src, outcome={"observed": None, "verdict": "n/a",
                                                         "note": f"vetoed by the referee (#{did})"[:300]})
                continue
            if verdict == "amend" and isinstance(v.get("amended_params"), dict) and isinstance(d.get("params"), dict):
                d["params"] = {**d["params"], **v["amended_params"]}
                amended += 1
            kept.append(d)
        kept += [d for i, d in enumerate(decs) if i not in judged]
        return kept, {"status": rv["status"], "model": rv["model"], "latency_ms": rv["latency_ms"], "vetoed": vetoed,
                      "amended": amended, "approved": len(kept) - amended}

    def _toolsmith_tick(self, c):
        """Advance Devin sessions; log adoptions/rejections as toolsmith decisions (runs off the cycle thread)."""
        try:
            from . import toolsmith
            before = {r["session_id"]: r.get("status") for r in toolsmith.sessions()}
            after = toolsmith.poll()
            for r in after:
                if before.get(r["session_id"]) == r.get("status") or r.get("status") not in ("adopted", "rejected", "testing", "expired"):
                    continue
                sm = r.get("smoke") or {}
                txt = {"adopted": f"Devin's strategy {r.get('filename')} passed the Modal sandbox smoke test (official verifier score "
                                   f"{sm.get('score')}) and is now template {r.get('template')}; the planner may launch it.",
                       "rejected": f"Devin's strategy {r.get('filename')} failed the Modal sandbox smoke test: {sm.get('error')}",
                       "testing": f"Devin delivered {r.get('filename')}; testing it in a Modal sandbox against the official verifier.",
                       "expired": "The Devin session expired without delivering code."}[r["status"]]
                did = ledger.add_decision(c, "toolsmith", r["status"], r.get("problem"),
                                          {"devin_session": r.get("url"), "file": r.get("filename"), "smoke": sm,
                                           "template": r.get("template")}, txt[:1200])
                events.publish("decision", ledger.get_decision(did))
        except Exception as e:  # noqa: BLE001
            events.log(f"toolsmith poll failed: {e}", "warn")

    def _dry_run_stops(self, actions, c, pids):
        """Test mode: only test- strategies are really stopped; the rest is logged as a dry run."""
        out = []
        for a in actions:
            if a["kind"] != "stop":
                out.append(a); continue
            real = [p for p in a["recs"] if str(p["id"]).startswith("test-")]
            dry = [p for p in a["recs"] if not str(p["id"]).startswith("test-")]
            if dry:
                src = pids.get(id(a.get("decision"))) if a.get("decision") is not None else None
                did = ledger.add_decision(c, "planner" if a["agent"] == "planner" else "executor", "stop", a["problem"],
                                          {"strategy_ids": [p["id"] for p in dry], "dry_run": True, "proposer_decision": src},
                                          f"[test mode: dry run, nothing killed] would stop {len(dry)} runs "
                                          f"({', '.join(p['id'] for p in dry[:5])}{'...' if len(dry) > 5 else ''}): {a['rationale'][:300]}")
                events.publish("decision", ledger.get_decision(did))
            if real:
                out.append(dict(a, recs=real))
        return out

    def _observation(self, slug, a, an):
        P = config.PROBLEMS[slug]
        age = f"{round(a['best_age_min'])} min" if a["best_age_min"] is not None else "n/a"
        if slug == "no-three-in-line-75":
            cls = sorted(an["classes"].values(), key=lambda x: (x["best_violated"] is None, x["best_violated"] or 0))
            parts = [f"{x['sym']} best {x['best_violated']} ({x['procs']} runs{', UNSAT' if x['unsat'] else ''})" for x in cls]
            ex = a.get("extra") or {}
            gpu = (f" GPU min-conflicts runs: best {ex.get('nothree_gpu.best_triples'):g} collinear triples, "
                   f"{ex.get('nothree_gpu.best_after_deletion'):g} after deleting the best point (0 = valid 149)."
                   if ex.get("nothree_gpu.best_triples") is not None and ex.get("nothree_gpu.best_after_deletion") is not None else "")
            return (f"{a['procs']} runs; best SAT model has {a['value']} violated lines (target 0), best unchanged for {age}. "
                    f"Classes: {'; '.join(parts)}.{gpu}")
        if slug == "spencer-discrepancy":
            sub = ", ".join(f"{k}: {v:g} bad vectors" for k, v in sorted(a["sub"].items()))
            return (f"{a['procs']} GPU tabu runs; {sub or 'no data'}; best unchanged for {age} (0 bad = beats record "
                    f"{P['record']:.6f}).")
        if slug == "hadamard-det-51":
            v = a["value"]
            rel = "equals" if v is not None and abs(v - P["record"]) < 1e-9 else ("exceeds" if v and v > P["record"] else "is below")
            return (f"{a['procs']} GPU runs; best log10|det| {v} {rel} the record {P['record']} (unchanged for {age}).")
        if a["procs"] == 0:
            return f"No runs. Status {a['status']}." + (f" Known: {planner.KNOWN_NEGATIVE[slug]}." if slug in planner.KNOWN_NEGATIVE else "")
        return f"{a['procs']} runs; {a['metric']}={a['value']}; best unchanged for {age}; status {a['status']}."

    def _memory(self, c, an):
        writes, facts = [], {}
        last = ledger.kv_get("last_observation", {}) or {}
        todo = [s for s, a in an["problems"].items() if config.PROBLEMS[s]["active"]]
        for slug in todo:
            a = an["problems"][slug]
            txt = self._observation(slug, a, an)
            key = f"{a['value']}|{a['procs']}|{a['status']}|{len(a['sub'])}"
            if last.get(slug, {}).get("key") != key or c - last.get(slug, {}).get("cycle", 0) >= 3:
                fid = memory.write(f"agent:{slug}", slug, f"[cycle {c}] {txt}", ["observation"])
                writes.append(fid)
                last[slug] = {"key": key, "cycle": c}
        ledger.kv_set("last_observation", last)

        def rd(slug):
            a = an["problems"][slug]
            q = f"{config.PROBLEMS[slug]['title']}: what worked, what failed, stalls, lessons. Now {a['status']}, {a['metric']}={a['value']}"
            return slug, memory.recall(f"agent:{slug}", q, k=5, problem=slug)
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            for slug, fs in ex.map(rd, todo):
                facts[slug] = fs
        n = sum(len(v) for v in facts.values())
        did = ledger.add_decision(c, "memory", "recall", None,
                                  {"agents": [f"agent:{s}" for s in todo], "facts_read": n, "facts_written": len(writes)},
                                  f"Problem agents wrote {len(writes)} observations and read {n} facts from the shared "
                                  f"past.dev space (identity {memory.IDENTITY}) before proposing.",
                                  memory_reads=sorted({f['id'] for v in facts.values() for f in v})[:60], memory_writes=writes)
        events.publish("decision", ledger.get_decision(did))
        return facts, writes

    def _literature(self, c, an):
        cards = {}
        last = ledger.kv_get("last_research", {}) or {}
        for slug, a in an["problems"].items():
            if not config.PROBLEMS[slug]["active"]:
                continue
            due = a["status"] in ("stalled",) and time.time() - last.get(slug, 0) > 3600
            due = due or (not literature.cards_for(slug, 1) and time.time() - last.get(slug, 0) > 3600)
            if due:
                situation = self._observation(slug, a, an)
                qs, model = literature.suggest_queries(slug, situation)
                ids = []
                for qtext in qs:
                    try:
                        cs, cached, lat = literature.search(slug, qtext)
                        ids += [x["id"] for x in cs]
                    except Exception as e:  # noqa: BLE001
                        events.log(f"exa search failed for {slug}: {e}", "warn")
                last[slug] = time.time()
                did = ledger.add_decision(c, "literature", "search", slug, {"queries": qs, "query_model": model},
                                          f"{slug} is {a['status']} (best unchanged {a['best_age_min'] and round(a['best_age_min'])} min): "
                                          f"searched Exa with {len(qs)} queries, {len(set(ids))} sources.",
                                          sources=sorted(set(ids)), model=model, link_sources=False)
                events.publish("decision", ledger.get_decision(did))
            cards[slug] = literature.cards_for(slug, 6)
        ledger.kv_set("last_research", last)
        return cards


LOOP = None


def get():
    global LOOP
    if LOOP is None:
        LOOP = Loop()
    return LOOP
