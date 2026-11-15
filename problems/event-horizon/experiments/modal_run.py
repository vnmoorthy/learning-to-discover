"""Run the Extension 1/2 sweeps on Modal CPU containers (no GPU), then write
results JSON + figures locally. Same seeds as the local runners, so results
are identical up to BLAS round-off.

  modal run experiments/modal_run.py --which e1
  modal run experiments/modal_run.py --which e2
  modal run experiments/modal_run.py --which both [--quick]
"""
import os, sys, time
import modal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

app = modal.App("event-horizon")
image = (modal.Image.debian_slim(python_version="3.11")
         .pip_install("numpy==2.2.6", "scipy==1.15.3")
         .env({"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
         .add_local_dir(os.path.join(ROOT, "eh"), "/root/proj/eh", ignore=["__pycache__", "*.pyc"])
         .add_local_dir(HERE, "/root/proj/experiments", ignore=["__pycache__", "*.pyc"]))


@app.function(image=image, cpu=1.0, memory=2048, timeout=1800, max_containers=40)
def run_chunk(payload):
    sys.path.insert(0, "/root/proj"); sys.path.insert(0, "/root/proj/experiments")
    import importlib
    module, fname, arglist = payload
    fn = getattr(importlib.import_module(module), fname)
    return [fn(a) for a in arglist]


def _chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def _map(module, fname, jobs, chunk):
    out = []
    for part in run_chunk.map([(module, fname, ch) for ch in _chunks(jobs, chunk)]):
        out.extend(part)
    return out


def _dump(name, obj):
    """Raw per-job outputs (so figures/JSON can be rebuilt without re-running)."""
    import json
    os.makedirs(os.path.join(ROOT, "results", "raw"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "raw", name), "w") as f:
        json.dump(obj, f)


@app.local_entrypoint()
def main(which: str = "both", quick: bool = False):
    sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
    if which in ("e1", "both"):
        import e1_scrambling_cpu as e1
        t0 = time.time()
        jobs, ojobs = e1.build_jobs(quick)
        res = _map("e1_scrambling_cpu", "job", jobs, 1)
        ores = _map("e1_scrambling_cpu", "job_oneshot", ojobs, 8)
        _dump("e1_raw.json", {"res": res, "ores": ores, "quick": quick})
        e1.finalize(res, ores, quick, t0, "modal cpu (debian_slim, numpy 2.2.6)")
    if which in ("e2", "both"):
        import e2_hayden_preskill_cpu as e2
        t0 = time.time()
        configs, jobs = e2.build_jobs(quick)
        res = _map("e2_hayden_preskill_cpu", "job", jobs, 12)
        _dump("e2_raw.json", {"configs": configs, "res": res, "quick": quick})
        e2.finalize(configs, res, quick, t0, "modal cpu (debian_slim, numpy 2.2.6)")
