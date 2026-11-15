"""Strategy templates (from search/TEMPLATES.json, re-read when it changes): validation, command lines, cmdline parsing.

Launch command lines are built ONLY here. Every value is checked against the template's param spec
(type, range, enum), so nothing the LLM writes reaches a shell unvalidated.
"""
import json
import math
import os
import re
import shlex
import threading

from . import config

_cache = {"mtime": None, "data": {}}
_lock = threading.Lock()


def templates():
    """Current template registry (re-read whenever TEMPLATES.json changes on disk)."""
    with _lock:
        try:
            mt = os.path.getmtime(config.TEMPLATES_PATH)
        except OSError:
            return _cache["data"]
        if mt != _cache["mtime"]:
            try:
                data = json.load(open(config.TEMPLATES_PATH))
                _cache["data"] = {k: v for k, v in data.items() if isinstance(v, dict) and v.get("script")}
                _cache["mtime"] = mt
            except ValueError:
                pass  # half-written file: keep the previous registry
        return _cache["data"]


def get(name):
    t = templates().get(name)
    if not t:
        raise ValueError(f"unknown template {name!r}; known: {sorted(templates())}")
    return t


def for_problem(slug):
    return {k: v for k, v in templates().items() if v.get("problem") == slug}


def family_dirs():
    """runs/<family> directories the telemetry should parse (built-ins + any template's out dir)."""
    dirs = {"spencer", "hadamard", "nothree"}
    for t in templates().values():
        out = t.get("out") or ""
        if out.startswith("runs/"):
            dirs.add(out[len("runs/"):].strip("/").split("/")[0])
    return sorted(d for d in dirs if d)


def public_params(t):
    """Param spec in the API shape {p: {type, min?, max?, values?, default}}."""
    out = {}
    for p, s in (t.get("params") or {}).items():
        d = {"type": s.get("type", "int"), "default": s.get("default")}
        for k in ("min", "max", "values"):
            if k in s:
                d[k] = s[k]
        out[p] = d
    return out


def validate(name, params):
    """Return a complete, type-checked param dict (defaults filled) or raise ValueError."""
    t = get(name)
    spec = t.get("params") or {}
    params = dict(params or {})
    # accept underscores for hyphenated names
    for k in list(params):
        if k not in spec and k.replace("_", "-") in spec:
            params[k.replace("_", "-")] = params.pop(k)
    unknown = [k for k in params if k not in spec]
    if unknown:
        raise ValueError(f"{name}: unknown params {unknown}; allowed {sorted(spec)}")
    out = {}
    for p, s in spec.items():
        v = params.get(p, s.get("default"))
        typ = s.get("type", "int")
        if v is None:
            if s.get("required"):
                raise ValueError(f"{name}: param {p} is required")
            continue
        if typ == "int":
            if isinstance(v, bool) or not isinstance(v, (int, float, str)):
                raise ValueError(f"{name}.{p}: expected int")
            try:
                fv = float(v)
            except (ValueError, OverflowError):
                raise ValueError(f"{name}.{p}: expected int, got {str(v)[:40]!r}")
            if not math.isfinite(fv) or fv != int(fv):
                raise ValueError(f"{name}.{p}: expected int, got {v!r}")
            v = int(fv)
        elif typ == "float":
            if isinstance(v, bool):
                raise ValueError(f"{name}.{p}: expected float, got {v!r}")
            try:
                v = float(v)
            except (TypeError, ValueError, OverflowError):
                raise ValueError(f"{name}.{p}: expected float, got {str(v)[:40]!r}")
            if not math.isfinite(v):      # nan passes every min/max comparison
                raise ValueError(f"{name}.{p}: expected a finite float, got {v!r}")
        elif typ == "enum":
            if v not in s.get("values", []):
                raise ValueError(f"{name}.{p}: {v!r} not in {s.get('values')}")
        elif typ == "bool":
            if not isinstance(v, bool):
                raise ValueError(f"{name}.{p}: expected bool")
        else:
            raise ValueError(f"{name}.{p}: unsupported type {typ}")
        if typ in ("int", "float"):
            if "min" in s and v < s["min"]:
                raise ValueError(f"{name}.{p}: {v} < min {s['min']}")
            if "max" in s and v > s["max"]:
                raise ValueError(f"{name}.{p}: {v} > max {s['max']}")
        out[p] = v
    return out


def _fmt(pattern, sid, params):
    vals = {"id": sid, **{k: v for k, v in params.items()}}
    return re.sub(r"\{([\w-]+)\}", lambda m: str(vals.get(m.group(1), m.group(0))), pattern)


def log_path(name, sid, params):
    t = get(name)
    fam = (t.get("out") or "runs/misc").rstrip("/")
    pat = t.get("log") or f"{fam}/{{id}}.log"
    return _fmt(pat, sid, params)


def argv(name, params):
    """Script argv (relative to ~/ltd) for validated params."""
    t = get(name)
    spec = t.get("params") or {}
    args = ["python3", "-B", t["script"]]
    for p, v in params.items():
        s = spec.get(p, {})
        flag = s.get("flag") or ("--" + p)
        if s.get("type") == "bool":
            if v:
                args.append(flag)
            continue
        args += [flag, str(v)]
    args += [str(a) for a in t.get("fixed_args", [])]
    out_flag = t.get("out_flag", "--out")
    if out_flag and t.get("out"):
        args += [out_flag, t["out"]]
    return args


def command(name, params, sid, gpu=None):
    """Full remote shell command that launches the strategy detached, writes its pid file and echoes the pid."""
    t = get(name)
    params = validate(name, params)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", sid):
        raise ValueError(f"bad strategy id {sid!r}")
    log = log_path(name, sid, params)
    out = t.get("out") or "runs/misc"
    env = f"PHOENIX_STRATEGY_ID={shlex.quote(sid)}"
    # Per-template environment. Default for GPU (torch) templates: ignore ~/.local site-packages, because numpy 2.x
    # installed there breaks the system torch build ("Numpy is not available"); system numpy 1.x works with it.
    tenv = t.get("env")
    if tenv is None and t.get("resource") == "gpu":
        tenv = {"PYTHONNOUSERSITE": "1"}
    for k, v in (tenv or {}).items():
        if re.fullmatch(r"[A-Z_][A-Z0-9_]{0,40}", str(k)) and re.fullmatch(r"[\w.,:/=+-]{0,200}", str(v)):
            env += f" {k}={shlex.quote(str(v))}"
    if t.get("resource") == "gpu":
        if gpu is None:
            raise ValueError("gpu template needs a gpu index")
        env += f" CUDA_VISIBLE_DEVICES={int(gpu)}"
    a = " ".join(shlex.quote(x) for x in argv(name, params))
    pidf = f"runs/strategies/{sid}.pid"
    return (f"cd {config.BOX_ROOT} && mkdir -p runs/strategies {shlex.quote(out)} {shlex.quote(os.path.dirname(log) or '.')} && "
            f"( {env} nohup setsid {a} > {shlex.quote(log)} 2>&1 < /dev/null & echo $! > {shlex.quote(pidf)} ) && "
            f"echo LAUNCHED {sid} $(cat {shlex.quote(pidf)})"), log, params


def match_script(cmdline_tokens):
    """(template_name, index_of_script_token) for a process argv, or (None, None)."""
    for name, t in templates().items():
        script = t["script"]
        for i, tok in enumerate(cmdline_tokens):
            if tok == script or tok.endswith("/" + script) or (os.path.basename(tok) == os.path.basename(script)
                                                                 and tok.endswith(".py")):
                return name, i
    return None, None


def parse_cmdline(tokens):
    """Parse an adopted process' argv into (template, params, extra). params get template defaults filled in."""
    if isinstance(tokens, str):
        tokens = tokens.split()
    if not tokens or not os.path.basename(tokens[0]).startswith("python"):
        return None, {}, {}
    name, i = match_script(tokens)
    if name is None:
        return None, {}, {}
    spec = get(name).get("params") or {}
    flag_to_p = {(s.get("flag") or "--" + p): p for p, s in spec.items()}
    raw, extra, k = {}, {}, i + 1
    while k < len(tokens):
        tok = tokens[k]
        if tok.startswith("--"):
            key, val = tok, None
            if "=" in tok:
                key, val = tok.split("=", 1)
            elif k + 1 < len(tokens) and not tokens[k + 1].startswith("--"):
                val = tokens[k + 1]; k += 1
            p = flag_to_p.get(key)
            if p:
                raw[p] = val if val is not None else True
            else:
                extra[key.lstrip("-")] = val if val is not None else True
        k += 1
    params = {}
    for p, s in spec.items():
        v = raw.get(p, s.get("default"))
        try:
            if s.get("type") == "int" and v is not None:
                v = int(float(v))
            elif s.get("type") == "float" and v is not None:
                v = float(v)
            elif s.get("type") == "bool":
                v = bool(v)
        except (TypeError, ValueError):
            pass
        if v is not None:
            params[p] = v
    return name, params, extra
