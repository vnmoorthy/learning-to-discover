"""Paths, problem registry, model names and loop knobs (single place for every constant)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DB_PATH = os.environ.get("LTD_DB", os.path.join(DATA, "ltd.sqlite"))
MEMORY_MD = os.environ.get("LTD_MEMORY_MD", os.path.join(DATA, "memory.md"))
PROBLEMS_DIR = os.path.join(ROOT, "problems")
SEARCH_DIR = os.path.join(ROOT, "search")
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
TEMPLATES_PATH = os.path.join(SEARCH_DIR, "TEMPLATES.json")
SSH_CONFIG = os.path.join(SCRIPTS_DIR, "ssh_config")
SSH_HOST = "ltd"
BOX_ROOT = "~/ltd"                      # code + runs on the GPU box
WEB_DIST = os.path.join(ROOT, "web", "dist")
GALLERY_DIR = os.path.join(ROOT, "web", "public", "gallery")
SNAPSHOT_OUT = os.path.join(ROOT, "web", "public", "data")
DATA_SNAPSHOT = os.path.join(DATA, "snapshot")

PROPOSER_MODEL = os.environ.get("LTD_PROPOSER_MODEL", "gpt-6-astra")
PROPOSER_FALLBACK = "gpt-5.5"
FAST_MODEL = "gpt-5.4-mini"
EMBED_MODEL = "text-embedding-3-small"

LOOP_INTERVAL_S = int(os.environ.get("LTD_LOOP_INTERVAL", "300"))
FIRST_CYCLE_DELAY_S = int(os.environ.get("LTD_FIRST_CYCLE_DELAY", "30"))
LOOP_AUTOSTART = os.environ.get("LTD_LOOP_AUTOSTART", "1") == "1"   # 0 -> server starts with the loop paused
TELEMETRY_POLL_S = int(os.environ.get("LTD_TELEMETRY_POLL", "30"))
ARTIFACT_POLL_S = 120
HOST = "127.0.0.1"
PORT = int(os.environ.get("LTD_PORT", "8787"))

# Box capacity targets (8x A100, 124 cores; keep ~6 cores for the OS, ssh, telemetry).
GPU_COUNT = 8
# GPUs lent to other lab projects (EVENT HORIZON physics runs); never counted as free by the planner
RESERVED_GPUS = [int(x) for x in os.environ.get("LTD_RESERVED_GPUS", "0").split(",") if x.strip()]
CPU_TOTAL = 124
CPU_TARGET = 118
# Planner knobs.
STALL_MIN = 40                # minutes without improvement -> "stalled"
STALL_MIN_GPU_STOP = 25       # an adopted/running GPU strategy may be replaced only after this many stalled minutes
MAX_CPU_STOPS_PER_CYCLE = 24
MAX_GPU_STOPS_PER_CYCLE = 3
MAX_LAUNCHES_PER_CYCLE = 32
DEAD_NO_RESULT_MIN = 90       # a CPU run with no first result after this long is considered dead
DEAD_GPU_STALL_MIN = 120      # a GPU run with no improvement for this long is replaced by the planner
MAX_DEAD_KILLS_PER_CYCLE = 8
LAUNCH_SEED_BASE = 1000       # seeds for strategies the backend launches (adopted runs use small seeds)

# Problem registry. family = runs/<family>/ on the box. metric = live progress signal shown in the UI.
_REG = [
    # slug, family, metric name, lower_is_better, artifact kind, theoretical max (if any)
    ("no-three-in-line-75", "nothree", "min_violated_lines", True, "grid"),
    ("spencer-discrepancy", "spencer", "bad_vectors", True, "sign_matrix"),
    ("hadamard-det-51", "hadamard", "best_log10", False, "sign_matrix"),
    ("sidon-45-set", "sidon", "best_score", True, "integer_set"),
    ("two-deletion-code-16", "twodel", "best_size", False, "code"),
    ("snake-in-the-box-13", "snake", "best_length", False, None),
    ("ring-loading-15", "ring", "best_score", False, None),
    # added after the red-team review: records within polishing distance, plus the astrophysics domain
    ("first-autocorrelation-inequality", "autocorr1", "best_C", True, None),
    ("kakeya-needle-128", "polish_kakeya", "best_score", True, None),
    ("kissing-number-d12-842", "polish_k12", "best_penalty", True, None),
    ("kissing-number-d11-605", "polish_k11", "best_penalty", True, None),
    ("three-body-periodic-orbits", "threebody", "verified_families", False, None),
]
# Problems the lab actively attacks (others are listed but idle unless a template exists for them).
ACTIVE = ["no-three-in-line-75", "two-deletion-code-16", "first-autocorrelation-inequality", "kakeya-needle-128",
          "kissing-number-d12-842", "kissing-number-d11-605", "three-body-periodic-orbits",
          "spencer-discrepancy", "hadamard-det-51", "sidon-45-set"]


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_leaderboard(slug):
    """Leaderboard rows from problems/<slug>/best_solutions.json, best first."""
    path = os.path.join(PROBLEMS_DIR, slug, "best_solutions.json")
    try:
        rows = json.load(open(path))
    except (OSError, ValueError):
        return []
    rows = rows if isinstance(rows, list) else rows.get("solutions", [])
    meta = load_meta(slug)
    rev = meta.get("scoring", "maximize") == "maximize"
    rows = [r for r in rows if _num(r.get("score")) is not None]
    rows.sort(key=lambda r: _num(r["score"]), reverse=rev)
    return rows


def load_meta(slug):
    try:
        return json.load(open(os.path.join(PROBLEMS_DIR, slug, "meta.json")))
    except (OSError, ValueError):
        return {}


def _build():
    out = {}
    for slug, family, metric, lib, kind in _REG:
        meta = load_meta(slug)
        lb = load_leaderboard(slug)
        top = lb[0] if lb else {}
        rec = _num(top.get("score"))
        if rec is None and meta.get("record") is not None:     # non-EinsteinArena problems (e.g. three-body) carry it in meta
            rec = _num(meta.get("record"))
            top = {"agentName": meta.get("record_holder") or meta.get("holder") or "published catalogs"}
        scoring = meta.get("scoring", "maximize")
        target = {"min_violated_lines": 0.0, "bad_vectors": 0.0}.get(metric, rec)
        if metric == "best_size" and rec is not None:
            target = rec + 1
        out[slug] = {
            "slug": slug, "title": meta.get("title", slug), "scoring": scoring, "family": family,
            "record": rec, "holder": (top.get("agentName") if len(str(top.get("agentName") or "")) <= 40 else "published catalogs"), "min_improvement": float(meta.get("minImprovement") or 0),
            "metric": metric, "lower_is_better": lib, "target": target, "artifact_kind": kind,
            "active": slug in ACTIVE,
        }
    return out


PROBLEMS = _build()
FAMILY_TO_PROBLEM = {p["family"]: s for s, p in PROBLEMS.items()}
# every template's output family (runs/<family>/) maps to its problem too (twodel_lns, nothree_gpu, devin_* ...)
try:
    for _n, _t in json.load(open(TEMPLATES_PATH)).items():
        _out = (_t.get("out") or "")
        if isinstance(_t, dict) and _out.startswith("runs/") and _t.get("problem") in PROBLEMS:
            FAMILY_TO_PROBLEM.setdefault(_out[5:].split("/")[0], _t["problem"])
except (OSError, ValueError):
    pass


def beats_record(slug, score):
    """A record needs an improvement of at least minImprovement (and strictly better)."""
    p = PROBLEMS[slug]
    if score is None or p["record"] is None:
        return False
    imp = (score - p["record"]) if p["scoring"] == "maximize" else (p["record"] - score)
    return imp > 1e-12 and imp >= p["min_improvement"] - 1e-12
