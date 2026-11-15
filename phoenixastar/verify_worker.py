"""Subprocess entry: run the OFFICIAL verifier problems/<slug>/verifier.py on a solution read from stdin.

python3 -m phoenixastar.verify_worker <slug>  < solution.json   ->  {"ok": bool, "score": float|null, "error": str|null, "seconds": float}
"""
import importlib.util
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    slug = sys.argv[1]
    if "/" in slug or ".." in slug:
        raise SystemExit("bad slug")
    path = os.path.join(ROOT, "problems", slug, "verifier.py")
    spec = importlib.util.spec_from_file_location(f"verifier_{slug.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sol = json.load(sys.stdin)
    t0 = time.time()
    try:
        score = float(mod.evaluate(sol))
        res = {"ok": True, "score": score, "error": None}
    except Exception as e:  # noqa: BLE001 - verifier raises on any invalid solution
        res = {"ok": False, "score": None, "error": f"{type(e).__name__}: {e}"[:500]}
    res["seconds"] = round(time.time() - t0, 3)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
