"""End-to-end CLI tests for twodel_ils / sidon_sa / snake_beam (reviewer additions to test_strategies.py).

Runs each script as the backend does (same flags, LTD_STRATEGY_ID=test-*) in a throwaway working directory, then
checks: no crash on edge-case params the template accepts, the best_<id>.json and FOUND_*.json shapes, every saved
solution against the OFFICIAL verifier, and that scripts/telemetry.py's log parser reads the expected metric.

  python3 search/test_strategies_cli.py [twodel] [sidon] [snake]
"""
import glob, importlib.util, json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


TEL = _load(os.path.join(ROOT, "scripts", "telemetry.py"), "ltd_telemetry_for_tests")
VER = {s: _load(os.path.join(ROOT, "problems", s, "verifier.py"), "v_" + s.replace("-", "_"))
       for s in ("two-deletion-code-16", "sidon-45-set", "snake-in-the-box-13")}


def run(cwd, sid, script, args, timeout=900, pre=None):
    """Run one search like the launcher does; returns (returncode, log text)."""
    env = dict(os.environ, LTD_STRATEGY_ID=sid)
    cmd = [sys.executable, "-B"] + ([pre] if pre else [os.path.join(HERE, script)]) + args
    t = time.time()
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    out = p.stdout + p.stderr
    print(f"    {sid}: rc={p.returncode} {time.time()-t:.0f}s  last: {out.strip().splitlines()[-1][:110] if out.strip() else ''}")
    return p.returncode, out


def metric(cwd, fam, sid, out):
    """What scripts/telemetry.py would report for this run's log."""
    log = os.path.join(cwd, "runs", fam, sid + ".log")
    open(log, "w").write(out)
    return (TEL.parse_log(log, fam).get("values") or {}).get("best")


def check_found(cwd, fam, slug, sid, key):
    fs = glob.glob(os.path.join(cwd, "runs", fam, f"FOUND_{sid}_*.json"))
    assert fs, f"no FOUND file for {sid}"
    for f in fs:
        d = json.load(open(f))
        assert set(d) >= {"solution", "score"} and list(d["solution"]) == [key], (f, list(d))
        assert VER[slug].evaluate(d["solution"]) == d["score"], f
    return fs


def best_file(cwd, fam, sid, slug):
    d = json.load(open(os.path.join(cwd, "runs", fam, f"best_{sid}.json")))
    sol = d.get("solution", d)       # exactly how ltd/critic.py reads a candidate file
    return d, VER[slug].evaluate(sol)


def test_twodel(cwd):
    slug = "two-deletion-code-16"
    # default template argv (from_record) for a short budget: must keep 226 and must NOT claim a record
    rc, out = run(cwd, "test-cli-td1", "twodel_ils.py", ["--seed", "0", "--mode", "from_record", "--group", "full",
                  "--algo", "ils", "--perturb", "1", "--pmulti", "0.15", "--accept", "arw", "--restart", "50000",
                  "--rank", "0", "--tenure", "15", "--seconds", "20", "--out", "runs/twodel"])
    assert rc == 0, out
    d, sc = best_file(cwd, "twodel", "test-cli-td1", slug)
    assert sc == d["count"] == 226 and not glob.glob(os.path.join(cwd, "runs/twodel/FOUND_test-cli-td1_*"))
    assert metric(cwd, "twodel", "test-cli-td1", out) == 226
    # FOUND path (forced with a low --target): file shape + official verifier
    rc, out = run(cwd, "test-cli-td2", "twodel_ils.py", ["--seed", "1", "--mode", "symmetric", "--group", "rev",
                  "--target", "100", "--seconds", "20", "--out", "runs/twodel"])
    assert rc == 0, out
    check_found(cwd, "twodel", slug, "test-cli-td2", "words")
    d, sc = best_file(cwd, "twodel", "test-cli-td2", slug)
    assert sc == d["count"] and metric(cwd, "twodel", "test-cli-td2", out) == d["count"]
    # tabu + symmetric
    rc, out = run(cwd, "test-cli-td3", "twodel_ils.py", ["--seed", "2", "--mode", "symmetric", "--algo", "tabu",
                  "--seconds", "20", "--out", "runs/twodel"])
    assert rc == 0, out
    d, sc = best_file(cwd, "twodel", "test-cli-td3", slug)
    assert sc == d["count"]
    print("twodel CLI OK")


def test_sidon(cwd):
    slug = "sidon-45-set"
    base = ["--T0", "0.3", "--T1", "0.01", "--cycle", "20000", "--pstruct", "0.55", "--plocal", "0.2",
            "--phub", "0.2", "--pw", "0.8", "--seconds", "8", "--out", "runs/sidon"]
    cases = [("test-cli-sd1", ["--seed", "0", "--n", "15", "--target", "0", "--M", "2000", "--init", "matang"]),
             ("test-cli-sd2", ["--seed", "0", "--n", "18", "--target", "0", "--M", "200", "--init", "random"]),
             ("test-cli-sd3", ["--seed", "0", "--n", "12", "--target", "12", "--M", "200", "--init", "matang"])]
    for sid, a in cases:
        rc, out = run(cwd, sid, "sidon_sa.py", a + base)
        assert rc == 0, out
        d, sc = best_file(cwd, "sidon", sid, slug)
        assert abs(sc - d["score"]) < 1e-12 and d["h"] == round(sc * d["n"]), (d["h"], sc)
        assert d["target_h"] == (4 * d["n"] - 1) // 7, d["target_h"]     # target clamped to t/n < 4/7
        assert abs(metric(cwd, "sidon", sid, out) - round(sc, 6)) < 1e-9
    # FOUND path: pretend the record is 0.99 so the first improvement is "a record"
    wrap = os.path.join(cwd, "sidon_found_wrapper.py")
    open(wrap, "w").write("import sys\nsys.path.insert(0, %r)\nimport sidon_sa as S\nS.RECORD = 0.99\n"
                          "sys.argv = ['sidon_sa.py'] + sys.argv[1:]\nS.main()\n" % HERE)
    rc, out = run(cwd, "test-cli-sdF", None, ["--seed", "2", "--n", "16", "--init", "random", "--seconds", "30",
                                                "--out", "runs/sidon"], pre=wrap)
    assert rc == 0, out
    fs = check_found(cwd, "sidon", slug, "test-cli-sdF", "elements")
    sc = json.load(open(fs[0]))["score"]
    assert abs(metric(cwd, "sidon", "test-cli-sdF", out) - round(sc, 6)) < 1e-9, "final log line lost best="
    print("sidon CLI OK")


def test_snake(cwd):
    slug = "snake-in-the-box-13"
    rc, out = run(cwd, "test-cli-sn1", "snake_beam.py", ["--seed", "1", "--rank", "0", "--wmin", "100", "--wmax",
                  "50", "--budget", "20000", "--psideways", "0.5", "--pend", "0.05", "--seconds", "8",
                  "--out", "runs/snake"])
    assert rc == 0 and "normalised to [50,100]" in out, out
    d, sc = best_file(cwd, "snake", "test-cli-sn1", slug)
    assert sc == d["length"] >= 2950 and metric(cwd, "snake", "test-cli-sn1", out) == d["length"]
    rc, out = run(cwd, "test-cli-snF", "snake_beam.py", ["--seed", "2", "--rank", "3", "--target", "100",
                  "--wmin", "2", "--wmax", "2", "--pend", "1", "--seconds", "8", "--out", "runs/snake"])
    assert rc == 0, out
    check_found(cwd, "snake", slug, "test-cli-snF", "actions")
    print("snake CLI OK")


if __name__ == "__main__":
    which = sys.argv[1:] or ["twodel", "sidon", "snake"]
    cwd = tempfile.mkdtemp(prefix="ltd_cli_test_")
    for f in ("twodel", "sidon", "snake"):
        os.makedirs(os.path.join(cwd, "runs", f), exist_ok=True)
    for w in which:
        t = time.time()
        globals()["test_" + w](cwd)
        print(f"  ({time.time()-t:.0f}s)")
    print("outputs in", cwd)
