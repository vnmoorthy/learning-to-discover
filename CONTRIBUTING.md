# Contributing

Thanks for looking. This started as a hackathon entry, so the bar is simple: keep it honest, keep it verifiable,
keep it working.

## Ground rules

1. **Nothing counts until the official verifier says so.** A result is a score returned by
   `problems/<slug>/verifier.py`. Do not modify the verifiers; they are the EinsteinArena originals.
2. **No invented numbers.** Results in `README.md` and `docs/RESULTS.md` live inside generated blocks. Change the
   data, then run `python3 docs/update_results.py`. Do not edit the blocks by hand.
3. **Label what is not live.** Snapshots, fixtures and illustrations must say what they are, in the UI and in docs.
4. **No secrets, anywhere.** Keys stay in `.env` (git-ignored) and are loaded with `envload.load()`. Never print,
   log or commit one, and never send one to the GPU box, a Modal container or a sandbox.
5. **No LLM output in a shell.** Launch command lines are built only in `ltd/strategies.py` from validated
   template parameters.
6. **Be careful with other people's compute.** Never stop a process you did not start. Test launches carry an id
   that starts with `test-`. Use `LTD_TEST_MODE=1` while developing.

## Good first contributions

### Add a search strategy

1. Write a CLI script in `search/` that follows the conventions in [`SPEC.md`](SPEC.md) section 2: `--seed`,
   `--out`, one parseable progress line per step, and `FOUND_*.json` containing `{"solution": ...}` only after an
   exact check.
2. Declare it in `search/TEMPLATES.json` with typed, ranged parameters and its resource (`gpu` or `cpu`).
3. Add a test in `search/test_strategies.py` showing that your objective agrees with the official verifier on
   the public best solutions and on random inputs.

### Add a problem

1. Create `problems/<slug>/` with `verifier.py` (`evaluate(solution: dict) -> float`, raising on invalid input),
   `meta.json`, `description.md` and `best_solutions.json`.
2. Register it in `ltd/config.py` (`_REG`, and `ACTIVE` if the loop should attack it) with its live metric.
3. Teach `scripts/telemetry.py` to parse the strategy's log line.

Any domain works if it has an exact verifier. See the roadmap in the README.

## Before you open a pull request

```bash
python3 search/test_strategies.py
python3 search/test_strategies_cli.py
python3 -m pytest -q ltd/tests_labs                 # offline tests: sandboxes, learning, memory benchmark
python3 -m ltd.smoke                                # against a running server; read-only
cd web && npm run typecheck && npm run build
python3 e2e/smoke.py --url http://127.0.0.1:8787    # from web/; never pass --mutate against a real server
python3 docs/update_results.py --check
```

Keep the API contract in `SPEC.md` section 4 and the types in `web/src/types.ts` in step: the frontend and the
backend must match exactly.

## Style

- Python: standard library first, small modules, a docstring at the top of every file that says what it does and
  how to run it.
- Docs: short sentences, tables over prose, no claims without a file to back them.
- Commits: one change per commit, written in the imperative.

## Reporting a problem with a result

If you believe a reported score is wrong, open an issue with the solution JSON and the output of
`python3 -m ltd.verify_worker <slug> < solution.json`. That is the fastest way to settle it.

## License

By contributing you agree that your contribution is licensed under the [MIT License](LICENSE).
