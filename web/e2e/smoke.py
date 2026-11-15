"""Headless smoke test of the web UI (Python Playwright, Chromium).

Visits every page at desktop and phone width and fails on: uncaught page errors, console errors, failed /api or
data requests, horizontal page scroll, or a page that never renders its heading.

    python3 web/e2e/smoke.py --url http://127.0.0.1:8787              # live backend: READ-ONLY, clicks nothing that mutates
    python3 web/e2e/smoke.py --url http://localhost:5173 --mutate     # fixtures / replay backends only: also clicks buttons
    python3 web/e2e/smoke.py --url http://localhost:4173/learning-to-discover/ --static

Never pass --mutate against the real ltd.server: it would pause the loop, launch/stop strategies on the GPU box, etc.
"""
import argparse
import json
import re
import sys
import time

from playwright.sync_api import sync_playwright

SLUGS = ["no-three-in-line-75", "spencer-discrepancy", "hadamard-det-51", "sidon-45-set", "two-deletion-code-16",
         "snake-in-the-box-13", "ring-loading-15"]
PAGES = [("/", "An AI lab that gets better at"), ("/decisions", "Decision audit log"), ("/memory", "Multi-agent memory"),
         ("/literature", "Literature"), ("/learning", "Self-improvement"), ("/gallery", "Gallery")] + \
        [(f"/problems/{s}", "Leaderboard") for s in SLUGS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--static", action="store_true", help="hash routes (static replay build)")
    ap.add_argument("--mutate", action="store_true", help="click mutating buttons (fixtures / replay only)")
    ap.add_argument("--widths", default="1440,390")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    route = (lambda p: f"{base}/#{p}") if a.static else (lambda p: f"{base}{p}")
    problems = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for w in [int(x) for x in a.widths.split(",")]:
            ctx = browser.new_context(viewport={"width": w, "height": 900 if w > 600 else 820})
            page = ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("console", lambda m: m.type == "error" and errs.append(f"console: {m.text[:300]}"))

            def on_resp(r):
                u = r.url
                if r.status >= 400 and ("/api/" in u or "/data/" in u or "/gallery/" in u or "/assets/" in u):
                    errs.append(f"HTTP {r.status} {u}")
            page.on("response", on_resp)

            for path, heading in PAGES:
                errs.clear()
                t0 = time.time()
                page.goto(route(path), wait_until="domcontentloaded")
                ok = True
                try:
                    page.locator("main").get_by_text(heading, exact=False).first.wait_for(timeout=15000)
                except Exception:  # noqa: BLE001
                    ok = False
                page.wait_for_timeout(1500)
                sw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                body = page.inner_text("main") if page.locator("main").count() else ""
                issues = list(errs)
                if not ok:
                    issues.append(f"heading {heading!r} never appeared")
                if sw[0] > sw[1] + 1:
                    issues.append(f"horizontal scroll: scrollWidth {sw[0]} > {sw[1]}")
                for bad in ("undefined", "NaN", "[object Object]"):
                    if re.search(rf"(^|[\s(:=]){re.escape(bad)}($|[\s),.])", body):
                        issues.append(f"page text contains {bad!r}")
                status = "OK " if not issues else "BAD"
                print(f"{status} w={w} {path} ({time.time() - t0:.1f}s)" + ("" if not issues else "\n    " + "\n    ".join(issues[:8])))
                if issues:
                    problems.append((w, path, issues))

            if a.mutate and w > 600:
                problems += mutate_checks(page, route, errs)
            ctx.close()
        browser.close()
    print(json.dumps({"failures": len(problems)}))
    sys.exit(1 if problems else 0)


def mutate_checks(page, route, errs):
    """Clicks every mutating control once and checks it gives visible feedback (fixtures / replay backends only)."""
    out = []

    def check(name, fn):
        errs.clear()
        try:
            res = fn()
            bad = [e for e in errs if not e.startswith("HTTP")]
            print(f"{'OK ' if not bad else 'BAD'} action {name}: {res}" + ("" if not bad else "\n    " + "\n    ".join(bad)))
            if bad:
                out.append(("action", name, bad))
        except Exception as e:  # noqa: BLE001
            print(f"BAD action {name}: {type(e).__name__}: {str(e)[:300]}")
            out.append(("action", name, [str(e)]))

    def toast_text():
        page.wait_for_timeout(300)
        return page.locator("[aria-live=polite]").inner_text(timeout=3000).replace("\n", " | ")[:220]

    def verify(slug):
        page.goto(route(f"/problems/{slug}"))
        page.get_by_role("button", name="Verify now").click()
        box = page.get_by_test_id("verify-result")
        box.wait_for(timeout=30000)
        return box.inner_text().replace("\n", " ")[:200] + " || toast: " + toast_text()

    def launch():
        page.goto(route("/problems/two-deletion-code-16"))
        page.get_by_role("button", name="Launch strategy").click()
        page.wait_for_timeout(2500)
        return toast_text()

    def loop():
        page.goto(route("/"))
        btn = page.get_by_role("button", name=re.compile(r"^(Pause|Resume)$"))
        btn.first.wait_for(timeout=10000)
        label = btn.first.inner_text()
        btn.first.click()
        page.wait_for_timeout(1200)
        return f"clicked {label}: {toast_text()}"

    def bench():
        page.goto(route("/memory"))
        page.get_by_role("button", name="Run benchmark").click()
        page.wait_for_timeout(1500)
        return toast_text()

    def sandboxes():
        page.goto(route("/learning"))
        page.get_by_role("button", name=re.compile(r"Run \d+ sandboxes")).click()
        page.wait_for_timeout(1500)
        return toast_text()

    def code_viewer():
        page.goto(route("/learning"))
        page.get_by_text("view", exact=True).first.click()
        page.get_by_text("Program written by the proposer", exact=False).wait_for(timeout=5000)
        page.keyboard.press("Escape")
        return "code viewer opened and closed"

    def training():
        page.goto(route("/learning"))
        b = page.get_by_role("button", name="Start training")
        b.wait_for(timeout=10000)
        if b.is_disabled():
            return "Start training disabled (a run is in progress)"
        b.click()
        page.wait_for_timeout(1500)
        return toast_text()

    for slug in ("spencer-discrepancy", "hadamard-det-51", "ring-loading-15"):
        check(f"verify {slug}", lambda s=slug: verify(s))
    check("launch strategy", launch)
    check("pause/resume", loop)
    check("memory benchmark", bench)
    check("run sandboxes", sandboxes)
    check("sandbox code viewer", code_viewer)
    check("start training", training)
    return out


if __name__ == "__main__":
    main()
