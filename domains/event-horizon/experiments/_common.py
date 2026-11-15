"""Shared setup for experiment scripts: GPU 0 only, modest CPU threads, paths."""
import json
import os
import sys
import time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)

import numpy as np  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"]))
# EH_DEVICE=cpu forces the CPU backend (useful for tiny matrices, where per-call GPU overhead
# dominates, or when the GPU is busy); default: cuda if available.
DEVICE = torch.device(os.environ.get("EH_DEVICE") or ("cuda" if torch.cuda.is_available() else "cpu"))


def env_info():
    info = {
        "torch": torch.__version__,
        "numpy": np.__version__,
        "device": str(DEVICE),
        "dtype": "complex128",
        "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if DEVICE.type == "cuda":
        info["gpu"] = torch.cuda.get_device_name(0)
        info["CUDA_VISIBLE_DEVICES"] = os.environ.get("CUDA_VISIBLE_DEVICES")
    return info


def dump(name, obj):
    path = os.path.join(RESULTS, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)
    print("wrote", path, flush=True)
    return path


def sync():
    if DEVICE.type == "cuda":
        torch.cuda.synchronize()


def log(*a):
    print(time.strftime("[%H:%M:%S]"), *a, flush=True)
