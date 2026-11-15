"""Writes deck/storyboard.md from the same snapshot numbers as the deck (called by build_deck.py).

Do not edit storyboard.md by hand: it is regenerated on every build. Edit the wording here.
"""
from __future__ import annotations

import deckdata as dd
from deckdata import fmt, pct, short


def _words(s):
    return len(s.split())


def write(D, notes, path):
    T = D["totals"]
    recs = D["records"]
    f = D["featured"] or {}
    ev = D["eval"] or {}
    g0, gN = ev.get("gen0") or {}, ev.get("genN") or {}
    nt = (D["details"].get("no-three-in-line-75") or {}).get("artifact") or {}
    nviol = len(nt.get("violated_lines") or [])
    verified = [p for p in D["problems"] if (p.get("ours") or {}).get("verified")]
    vslug = (recs[0]["slug"] if recs else (verified[0]["slug"] if verified else "no-three-in-line-75"))
    vp = next((p for p in D["problems"] if p["slug"] == vslug), {})
    vscore = fmt((vp.get("ours") or {}).get("score"))
    vrec = fmt((vp.get("record") or {}).get("score"))
    neg = D["negatives"][0] if D["negatives"] else None
    bench = dd.bench_sentence(D)
    ref = D["referee"]
    fleet = D["modal"]
    ts = D["toolsmith"]

    if recs:
        p = recs[0]
        result_line = (f"And it worked. On {short(p['slug'])} the lab found {fmt((p.get('ours') or {}).get('score'))}. The record was {fmt(p['record']['score'])}. "
                       "The official verifier confirmed it, and the log shows every decision that led there.")
        result_short = f"new record on {short(p['slug'])}: {fmt((p.get('ours') or {}).get('score'))} vs {fmt(p['record']['score'])}"
    else:
        result_line = ("Results, honestly. No record beaten yet. "
                       + (f"Our closest search has {nt.get('count')} points on the 75 by 75 grid, with {nviol} lines still to remove. Zero settles an open case. " if nt else "")
                       + (f"We hold verified solutions on {len(verified)} problems, below the record" if verified else "We hold no verified solution above a record")
                       + (f", and one proved negative result on {short(neg['slug'])}." if neg else "."))
        result_short = "no record beaten yet" + (f"; closest: no-three-in-line, {nt.get('count')} points, {nviol} violated lines left" if nt else "")
    verify_say = (f"I click Verify now. The official verifier runs on our best solution for {short(vslug)}. It returns {vscore}. The record is {vrec}. "
                  + ("That is a new record." if vp.get("beats_record") else "Valid, and below the record. The lab says so itself."))
    learn_say = (f"And it learns. Tinker fine-tunes {D['base_model'].split('/')[-1]} with the verifier as reward. "
                 f"Valid constructions on held-out prompts went from {pct(g0.get('valid_rate'))} to {pct(gN.get('valid_rate'))} in {len(D['steps'])} steps.")
    referee_say = (f"Claude Fable, the referee, said: {D['featured_referee'].get('verdict')}." if D["featured_referee"]
                   else "A second model, Claude Fable, referees proposals before compute moves.")

    finals = [
        ("0:00-0:15", "Slide 1 (title, lattice video)",
         "This is Learning to Discover. An AI lab that gets better at discovering mathematics by doing it. What is moving behind me is our live search, not art.",
         "Deck in presenter view. App already open in a second window on Mission Control."),
        ("0:15-0:33", "Slide 2 (the problem)",
         "AI does find new math records. But it finds them with search loops nobody can audit. And the loops are static. Hour thirty searches exactly like hour one.",
         "Next slide."),
        ("0:33-0:55", "Slide 3 (the loop)",
         f"So we built a lab. Every {D['interval_min']} minutes, with no human, it reads the cluster, re-verifies every claim, shares memory, searches papers with Exa, "
         "proposes experiments with GPT-6 Astra, has Claude Fable referee them, and executes on Lambda and Modal.",
         "Next slide, then switch to the app."),
        ("0:55-1:20", "LIVE APP: Mission Control `/`",
         f"This is it, live. {len(D['gpus'])} A100s and {D['cpus']} cores, coloured by problem. I click Run cycle now. Watch the phases light up: telemetry, critic, memory, literature, propose, plan, execute. "
         "New decisions land in the feed on the right.",
         "Click **Run cycle now**. Point at the phase stepper, then the decision feed."),
        ("1:20-1:45", "LIVE APP: `/decisions`",
         f"Every decision is a card. This one, number {f.get('id', '?')}: the reason in plain English, "
         + ("the papers it found through Exa, " if f.get("sources") else "")
         + f"and a prediction with a deadline that the critic scores later. {referee_say}",
         f"Open `/decisions`. Expand decision **#{f.get('id', '?')}** (filter problem: {f.get('problem') or 'any'}). Click one Exa source link only if time allows."),
        ("1:45-2:05", f"LIVE APP: `/problems/{vslug}`", verify_say,
         f"Open `/problems/{vslug}`. Click **Verify now**. Wait for the result badge."),
        ("2:05-2:25", "LIVE APP: `/learning`", learn_say,
         "Open `/learning`. Point at the reward curve, then the gen-0 vs gen-N panel."),
        ("2:25-2:45", "Slide 6 (results)", result_line, "Back to the deck, slide 6."),
        ("2:45-3:00", "Slide 10 (close)",
         "Math is the start, because the verifier is exact. Next is physics: periodic orbits of the three-body problem. Same loop, same log. It is all public. Thank you.",
         "Jump to slide 10 (type 10, Enter). Stop talking at 2:58."),
    ]
    total_words = sum(_words(r[2]) for r in finals)

    r1 = [("0:00-0:15", 1), ("0:15-0:33", 2), ("0:33-0:58", 3), ("0:58-1:15", 4), ("1:15-1:35", 5), ("1:35-1:57", 6), ("1:57-2:17", 7), ("2:17-2:35", 8), ("2:35-2:48", 9), ("2:48-3:00", 10)]
    titles = ["Title", "The problem", "What we built", "Live compute", "A real decision", "Results", "It improves itself", "Memory and tools", "Rigour", "Close"]

    human = ("We wrote the lab, the first search scripts and the verifier harness, and we started the first searches by hand. "
             "The loop adopted those processes. After that it decides what runs, what stops and where compute goes.")
    qa = [
        ("Did you beat a record?",
         (f"Yes: {result_short}. Verified by the official verifier, and replayable from the log." if recs else
          f"Not yet, and we say so on the slide. Status as of {D['asof']}: {result_short}. "
          + (f"We also have a proved negative result on {short(neg['slug'])}. " if neg else "")
          + "Everything we do claim went through the official verifier.")),
        ("What is new compared with AlphaEvolve or Karpathy's autoresearch?",
         "Three things. One: every proposal carries a falsifiable prediction, and a critic scores it later, so the lab knows when its own reasoning was wrong. "
         "Two: two models from different labs must agree before compute moves, with a deterministic planner under both. "
         "Three: the lab improves its own parts. It fine-tunes a model on verifier reward, writes new search programs, and commissions new tools."),
        ("How do we know the results are real?",
         f"The search never grades itself. The critic runs the official EinsteinArena verifier in a separate process. It has run {fmt(D['verifier_checks'])} times in this log. "
         "You can press Verify now in the app and watch it."),
        ("How autonomous is it? What did humans do?", human + f" In this run that is {fmt(T.get('cycles'))} cycles and {fmt(T.get('decisions'))} logged decisions."),
        ("Does it really improve itself?",
         f"Two ways, both measured. The Tinker run: valid constructions on held-out prompts went from {pct(g0.get('valid_rate'))} to {pct(gN.get('valid_rate'))}, "
         f"mean reward from {fmt(g0.get('score'), 3)} to {fmt(gN.get('score'), 3)}. And the prediction scores: {D['pred_confirmed']} confirmed, {D['pred_refuted']} refuted, "
         f"{D['pred_pending']} pending. Each scored prediction becomes a lesson in memory that the next proposal reads."
         + ("" if (D["learning"].get("best") or {}).get("beats_record") else " The trained model has not beaten a record. The claim is the curve.")),
        ("Why a referee model?",
         "One model proposing and judging its own ideas is the failure we wanted to avoid. Claude Fable sees the live evidence and each proposal, and can approve, veto or amend. "
         + (f"In this log: {', '.join(f'{v} {k}' for k, v in ref.items() if k)}. " if ref else "This snapshot has no referee verdicts recorded yet, so we do not quote a number. ")
         + "If the referee fails, it abstains and the planner's hard limits still apply."),
        ("past.dev versus markdown and RAG?",
         f"We measured it on real lab facts. {bench} "
         "past.dev holds the shared lab memory that agents read from each other; the markdown file and the small RAG index exist only as baselines."),
        ("Where is Exa in the loop?",
         f"In the main loop, as the literature step. The proposer writes the queries, Exa returns sources, and decisions cite them. "
         f"{fmt(D['n_sources'])} sources stored, {fmt(D['n_cited'])} cited by decisions. Decision {f.get('id', '?')} is an example."),
        ("What does Modal do?",
         f"Two jobs. Sandboxes: {fmt(D['n_sandboxes'])} AI-written search programs ran in parallel with no network and no secrets, and {fmt(D['sb_ok'])} returned a solution the verifier accepted. "
         + (f"And an elastic CPU fleet: {fmt(fleet.get('containers') or fleet.get('launches'))} containers launched by the planner." if fleet else
            "And an elastic CPU fleet that the planner can launch when the Lambda box is full. This snapshot records no fleet container, so we quote no number.")),
        ("What about Devin?",
         ("Devin is the toolsmith. " + (f"{fmt(ts.get('requested'))} tools commissioned, {fmt(ts.get('adopted'))} adopted after passing the verifier in a Modal sandbox, {fmt(ts.get('rejected'))} rejected."
                                        if ts else "The lab commissions a new search program, tests it in a Modal sandbox against the verifier, and adopts it only if it passes. "
                                        "This snapshot has no completed toolsmith session, so we quote no number."))),
        ("What failed?",
         (f"{short(neg['slug'])}: exact search proved there is no small extension of the record set. " if neg else "")
         + f"{len([p for p in D['problems'] if p.get('status') == 'stalled'])} searches are reported as stalled. The planner rejected {D['planner_rejects']} proposals. "
         + f"The loop stopped {D['stops']} runs. All of that is in the log."),
        ("Why these problems?",
         "They are open EinsteinArena problems with exact public verifiers and live leaderboards, so a claim is either valid or it is not. "
         "No-three-in-line on the 75 grid is the last open case up to 76."),
    ]

    L = []
    A = L.append
    A("# Learning to Discover: presenter storyboard")
    A("")
    A(f"Generated by `deck/build_deck.py` from the snapshot **as of {D['asof']}** ({D['label']}). "
      "Numbers below are read from `web/public/data/*.json`. Rebuild after the snapshot is regenerated, then re-read the script once.")
    A("")
    A(f"Status line to memorise: **{result_short}**. {fmt(T.get('cycles'))} cycles, {fmt(T.get('decisions'))} decisions, "
      f"{fmt(T.get('experiments_run'))} experiments, {fmt(T.get('sandboxes_run'))} sandboxes.")
    A("")
    A("Setup before you walk up:")
    A("")
    A("- Deck open in presenter view on slide 1 (Morph and videos need PowerPoint 2019 or 365; Keynote and Google Slides fall back to a fade).")
    A("- Live app at `http://127.0.0.1:8787` in a browser window, on Mission Control `/`, loop running. Tabs pre-opened: `/decisions`, "
      f"`/problems/{vslug}`, `/learning`.")
    A("- If the box or the network is down, use the public static replay. Its buttons are disabled, so say \"this is a replay of the live run\" and skip the two clicks.")
    A("")
    A("## 1. Finals: 3 minutes, pitch plus live demo, no Q&A")
    A("")
    A(f"About {total_words} words. Speak slowly. Short sentences. If you are behind at 2:25, skip the `/learning` row.")
    A("")
    A("| Time | On screen | Say (exact words) | Do |")
    A("|---|---|---|---|")
    for t, scr, say, do in finals:
        A(f"| {t} | {scr} | {say} | {do} |")
    A("")
    A("## 2. Round 1: 5 minutes (3:00 pitch, 2:00 Q&A)")
    A("")
    A("Slides only, one idea each. The words are the speaker notes in the deck. Keep the app open on Mission Control in case a judge asks to see it.")
    A("")
    A("| Time | Slide | Say (exact words) |")
    A("|---|---|---|")
    for (t, i) in r1:
        A(f"| {t} | {i}. {titles[i - 1]} | {notes[i - 1]} |")
    A("")
    r1_words = sum(_words(n) for n in notes)
    A(f"That is about {r1_words} words. " + ("It is tight for three minutes: on slides 3, 4 and 8 say only the first two sentences." if r1_words > 430 else "It fits three minutes at a calm pace."))
    A("")
    A("### Likely questions, crisp answers")
    A("")
    for q, a in qa:
        A(f"**{q}**")
        A("")
        A(a)
        A("")
    A("## 3. Demo walkthrough: 10 minutes")
    A("")
    A("For the demo video, a sponsor judge, or anyone who wants the whole thing. Live app unless noted.")
    A("")
    walk = [
        ("0:00-1:00", "Deck slides 1 to 3", "The pitch in one minute: the tagline, the problem (opaque, static, unchecked), the loop diagram.", "Advance through slides 1 to 3."),
        ("1:00-2:30", "Mission Control `/`",
         f"The header shows the loop status and the phase stepper. The compute map shows {len(D['gpus'])} GPU tiles and {D['cpus']} CPU cells, coloured by owning problem. "
         "The cards show record against ours, a live metric and compute share. Run a cycle and narrate each phase as it lights up.",
         "Click **Run cycle now**. Hover a GPU tile. Point at totals counters."),
        ("2:30-4:00", "`/decisions`",
         f"The audit log. Filter by agent. Open decision #{f.get('id', '?')}: rationale, prediction, Exa sources, memory reads and writes, model, tokens, latency. "
         f"Then open a critic card that scores a prediction ({D['pred_confirmed']} confirmed, {D['pred_refuted']} refuted so far) and a planner reject ({D['planner_rejects']} so far).",
         f"Filter agent = proposer, expand **#{f.get('id', '?')}**, open one source link. Filter agent = critic, expand a `score_prediction`. Filter agent = planner, expand a `reject`."),
        ("4:00-5:30", "`/problems/no-three-in-line-75`",
         (f"The flagship problem. The canvas shows {nt.get('count')} points and {nviol} violated lines in red. The record is 148; 149 is new; 150 settles the last open case up to 76. " if nt else "The flagship problem. ")
         + "Show the metric history, the running strategies table and the launch form generated from the strategy schema.",
         "Scroll: description, leaderboard, chart, grid, strategies. Do not stop a running strategy."),
        ("5:30-6:15", f"`/problems/{vslug}`", verify_say, "Click **Verify now**."),
        ("6:15-7:30", "`/learning`",
         learn_say + f" Then the sandboxes table: {fmt(D['n_sandboxes'])} programs written by the proposer, run on Modal with no network and no secrets, each scored by the verifier. Open one to show the code.",
         "Point at reward curve and valid-rate curve. Open one sandbox row in the code viewer. Optional: **Run N sandboxes** with N = 2."),
        ("7:30-8:30", "`/memory`",
         f"The agent graph: an edge means one agent read a fact another agent wrote. {fmt(D['n_facts'])} facts, {fmt(D['cross_reads'])} cross-agent reads. Then the benchmark. {bench}",
         "Hover an edge. Scroll to the benchmark chart. Do not press Run benchmark on stage (it takes over a minute)."),
        ("8:30-9:00", "`/literature` and `/gallery`",
         f"Exa sources grouped by problem, with the decisions that cite them: {fmt(D['n_sources'])} sources, {fmt(D['n_cited'])} cited. "
         "The gallery: Blender renders of real artifacts; the scripts were written by GPT-6 Astra.",
         "Open one cited source. Play the lattice orbit video."),
        ("9:00-10:00", "Deck slides 6, 9, 10", result_line + " Then rigour: what was verified, what was predicted, what failed. Then what is next, and the repo link.", "Slides 6, 9, 10."),
    ]
    A("| Time | Screen | Say | Click |")
    A("|---|---|---|---|")
    for t, scr, say, do in walk:
        A(f"| {t} | {scr} | {say} | {do} |")
    A("")
    A("## Things not to say")
    A("")
    if not recs:
        A("- Do not say \"we beat\" or \"new record\". As of this snapshot `totals.records` is " + fmt(T.get("records") or 0) + ".")
        A("- The Hadamard and two-deletion live signals equal the record because those searches start from the record solution. That is not our result.")
    if not ref:
        A("- Do not quote a referee approval or veto count: this snapshot has none recorded.")
    if not fleet:
        A("- Do not quote a Modal fleet size: this snapshot records sandboxes only.")
    if not ts:
        A("- Do not quote a number of Devin tools adopted: this snapshot records none.")
    S = D["bench_systems"]
    if S and "past.dev" in S and max(S.values(), key=lambda s: s.get("accuracy") or 0) is not S["past.dev"]:
        A("- Do not say past.dev beat markdown or RAG on accuracy. Say what was measured (see the Q&A answer); the README must explain it for the past.dev challenge.")
    A("- If a rebuild changes any of the above, this list changes with it.")
    A("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))
