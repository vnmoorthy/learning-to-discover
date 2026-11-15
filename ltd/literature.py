"""Exa in the main loop: search + highlights for a problem, cached by query, stored as literature cards."""
import json
import os
import time

from . import config, ledger

EXA_URL = "https://api.exa.ai/search"
CACHE_S = 6 * 3600


def _key():
    import sys
    if config.ROOT not in sys.path:
        sys.path.insert(0, config.ROOT)
    import envload
    envload.load()
    return os.environ.get("EXA_API_KEY", "")


def card(r):
    return {"id": r["id"], "title": r["title"], "url": r["url"], "published": r["published"],
            "highlight": (r["highlight"] or "")[:400]}


def search(problem, query, n=5):
    """Run (or reuse) an Exa search. Returns (cards, cached: bool, latency_ms)."""
    import httpx
    query = query.strip()[:300]
    hit = ledger.q("SELECT * FROM lit_queries WHERE query=?", (query,))
    if hit and time.time() - (ledger.parse_iso(hit[0]["time"]) or 0) < CACHE_S:
        ids = ledger.uj(hit[0]["ids"], []) or []
        rows = ledger.q(f"SELECT * FROM literature WHERE id IN ({','.join('?' * len(ids))})", ids) if ids else []
        return [card(r) for r in rows], True, 0
    t0 = time.time()
    resp = httpx.post(EXA_URL, headers={"x-api-key": _key()}, timeout=40,
                      json={"query": query, "numResults": int(n), "type": "auto",
                            "contents": {"highlights": {"numSentences": 3, "highlightsPerUrl": 2}}})
    resp.raise_for_status()
    lat = int((time.time() - t0) * 1000)
    ids = []
    for res in resp.json().get("results", []):
        url = res.get("url") or res.get("id")
        if not url:
            continue
        hl = " ... ".join(h.strip() for h in (res.get("highlights") or []) if h)[:1200]
        ex = ledger.q("SELECT id FROM literature WHERE problem=? AND url=?", (problem, url))
        if ex:
            lid = ex[0]["id"]
            if hl:
                ledger.x("UPDATE literature SET highlight=? WHERE id=?", (hl, lid))
        else:
            lid = ledger.x("INSERT INTO literature(problem,query,title,url,published,highlight,time,cited_by) VALUES(?,?,?,?,?,?,?,?)",
                           (problem, query, (res.get("title") or url)[:300], url, (res.get("publishedDate") or None),
                            hl, ledger.now(), "[]"))
        ids.append(lid)
    ledger.x("INSERT INTO lit_queries(query,problem,time,ids) VALUES(?,?,?,?) ON CONFLICT(query) DO UPDATE SET "
             "time=excluded.time, ids=excluded.ids, problem=excluded.problem", (query, problem, ledger.now(), json.dumps(ids)))
    rows = ledger.q(f"SELECT * FROM literature WHERE id IN ({','.join('?' * len(ids))})", ids) if ids else []
    return [card(r) for r in rows], False, lat


def cards_for(problem, limit=6):
    """Most recent cards for a problem (what the proposer sees)."""
    rows = ledger.q("SELECT * FROM literature WHERE problem=? ORDER BY id DESC LIMIT ?", (problem, limit))
    return [card(r) for r in rows]


def suggest_queries(problem, situation, n=2):
    """FAST_MODEL writes search queries for a stalled problem (fallback: a fixed query from the title)."""
    P = config.PROBLEMS[problem]
    try:
        import sys
        if config.ROOT not in sys.path:
            sys.path.insert(0, config.ROOT)
        import envload
        envload.load()
        from openai import OpenAI
        schema = {"type": "object", "properties": {"queries": {"type": "array", "items": {"type": "string"}}},
                  "required": ["queries"], "additionalProperties": False}
        r = OpenAI().responses.create(
            model=config.FAST_MODEL,
            input=(f"You help a math research lab. Problem: {P['title']} (record {P['record']} by {P['holder']}, "
                   f"{P['scoring']}). Current situation: {situation}\nWrite {n} web search queries (papers, constructions, "
                   f"bounds, search techniques) most likely to unblock progress. Short, specific."),
            text={"format": {"type": "json_schema", "name": "queries", "schema": schema, "strict": True}})
        qs = json.loads(r.output_text)["queries"][:n]
        if qs:
            return qs, config.FAST_MODEL
    except Exception:  # noqa: BLE001
        pass
    return [f"{P['title']} best known construction search method"], None
