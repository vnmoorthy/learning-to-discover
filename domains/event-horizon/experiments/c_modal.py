"""OPTIONAL: compute the N=11/12 main runs of Problem C on Modal CPU containers
(same seeds, same code as the local path) and write the same cache files that
experiments/c_evaporation.py reads.  Usage:
    modal run experiments/c_modal.py --n 12 --seeds 20
No GPUs; a few CPU-minutes in total."""
import os, pickle
import modal

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
image = (modal.Image.debian_slim(python_version="3.12").pip_install("numpy==2.2.6", "scipy==1.15.3")
         .add_local_dir(os.path.join(ROOT, "eh"), "/root/eh", ignore=["__pycache__", "plotstyle.py", "plotting.py", "circuits.py", "hayden_preskill.py"]))
app = modal.App("event-horizon")


@app.function(image=image, cpu=2.0, memory=4096, timeout=3600, max_containers=20)
def traj(args):
    import os, sys, time
    os.environ.setdefault("OMP_NUM_THREADS", "2")
    sys.path.insert(0, "/root")
    import numpy as np
    from eh import evaporation as ev
    N, i, base = args
    rng = np.random.default_rng(np.random.SeedSequence([base, 0, N, i]))
    t0 = time.process_time()
    out = ev.run_trajectory(N, rng, init="zero")
    return i, out, time.process_time() - t0


@app.local_entrypoint()
def main(n: int = 12, seeds: int = 20, base: int = 20261115):
    res = sorted(traj.map([(n, i, base) for i in range(seeds)]), key=lambda r: r[0])
    trajs = [r[1] for r in res]
    cpu = sum(r[2] for r in res)
    d = os.path.join(ROOT, "results", "c_cache")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"N{n}_seeds{seeds}.pkl")
    path = path.replace(".pkl", "_modal.pkl")
    pickle.dump((trajs, cpu), open(path, "wb"))
    print("wrote", path, "cpu s/traj", cpu / seeds)
