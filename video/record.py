"""Records each screen shot of the demo from the live app with a CDP screencast (read-only navigation; no mutating clicks).
usage: python3 record.py [shot_name ...]"""
import asyncio, base64, json, os, re, shutil, subprocess, sys, time, urllib.request
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = "http://127.0.0.1:8787"
SEC = {x["id"]: x for x in json.load(open(f"{HERE}/sections.json"))["sections"]}
W, H = 1920, 1080
CURSOR_JS = """() => { if (window.__cur) return; const c = document.createElement('div'); window.__cur = c;
 c.style.cssText = 'position:fixed;left:-50px;top:-50px;width:26px;height:26px;z-index:2147483647;pointer-events:none;transition:none';
 c.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2 L4 20 L9 15.5 L12.2 22.5 L15 21.2 L11.8 14.3 L18.5 14.3 Z" fill="white" stroke="black" stroke-width="1.4" stroke-linejoin="round"/></svg>';
 document.documentElement.appendChild(c);
 document.addEventListener('mousemove', e => { c.style.left = (e.clientX - 4) + 'px'; c.style.top = (e.clientY - 2) + 'px'; }, true);
 window.__scrollTo = (y, ms) => new Promise(res => { const y0 = window.scrollY, t0 = performance.now();
   const step = now => { let k = Math.min(1, (now - t0) / ms); k = k < .5 ? 4*k*k*k : 1 - Math.pow(-2*k + 2, 3) / 2; window.scrollTo(0, y0 + (y - y0) * k); if (now - t0 < ms) requestAnimationFrame(step); else res(); };
   requestAnimationFrame(step); }); }"""

class Shot:
    def __init__(self, page, cdp, name, dur):
        self.page, self.cdp, self.name, self.dur = page, cdp, name, dur; self.frames = []; self.mx, self.my = 960, 540; self.t0 = None
    async def start(self):
        d = f"{HERE}/frames/{self.name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d); self.dir = d
        async def ack(sid): 
            try: await self.cdp.send("Page.screencastFrameAck", {"sessionId": sid})
            except Exception: pass
        def on(ev):
            p = f"{d}/{len(self.frames):05d}.jpg"; open(p, "wb").write(base64.b64decode(ev["data"]))
            self.frames.append((time.time(), p)); asyncio.ensure_future(ack(ev["sessionId"]))
        self.cdp.on("Page.screencastFrame", on)
        await self.cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 93, "maxWidth": W, "maxHeight": H, "everyNthFrame": 1})
        await self.page.mouse.move(self.mx, self.my); await asyncio.sleep(0.4); self.t0 = time.time()
    def now(self): return time.time() - self.t0
    async def until(self, t):
        d = t - self.now()
        if d > 0: await asyncio.sleep(d)
    async def glide(self, x, y, ms=900):
        x0, y0 = self.mx, self.my; st = time.time()
        while True:
            k = min(1.0, (time.time() - st) * 1000 / ms); e = k * k * (3 - 2 * k)
            await self.page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e)
            if k >= 1: break
            await asyncio.sleep(0.012)
        self.mx, self.my = x, y
    async def scroll(self, y, ms=1400): await self.page.evaluate("([y,ms]) => window.__scrollTo(y,ms)", [y, ms])
    async def box(self, pat, nth=0):
        loc = self.page.get_by_text(re.compile(pat, re.I)).nth(nth) if isinstance(pat, str) and not pat.startswith("css=") else self.page.locator(pat[4:]).nth(nth)
        return await loc.bounding_box()
    async def page_y(self, pat, nth=0):
        b = await self.box(pat, nth); return b["y"] + await self.page.evaluate("window.scrollY")
    async def to(self, pat, dx=0.5, dy=0.5, ms=900, nth=0):
        b = await self.box(pat, nth)
        if b: await self.glide(b["x"] + b["width"] * dx, b["y"] + b["height"] * dy, ms)
    async def finish(self):
        await self.until(self.dur + 0.4); await self.cdp.send("Page.stopScreencast"); await asyncio.sleep(0.2)
        fr = [(t, p) for t, p in self.frames]; pre = [f for f in fr if f[0] <= self.t0]; post = [f for f in fr if f[0] > self.t0]
        seq = ([(self.t0, pre[-1][1])] if pre else []) + post; end = self.t0 + self.dur + 0.3
        with open(f"{self.dir}/list.txt", "w") as f:
            for i, (t, p) in enumerate(seq):
                nt = seq[i + 1][0] if i + 1 < len(seq) else end
                if nt - t > 0: f.write(f"file '{p}'\nduration {nt - t:.4f}\n")
            f.write(f"file '{seq[-1][1]}'\n")
        out = f"{HERE}/clips/{self.name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{self.dir}/list.txt", "-vf", f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p",
                        "-t", f"{self.dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "15", out], check=True)
        print(self.name, "frames", len(seq), "fps", round(len(post) / max(0.1, self.frames[-1][0] - self.t0), 1), "dur", self.dur, "->", out, flush=True)

def state():
    try: return json.load(urllib.request.urlopen(BASE + "/api/state", timeout=10))
    except Exception as e: print("state err", e, flush=True); return {"loop": {"phase": "?"}}

# ---- shots: each gets a loaded page; prep (unrecorded) then start() then timed actions ----
async def s2_loop(s):
    await s.start(); ph = "css=[data-phase]"
    await s.to(r"^cycles$", 0.5, 1.6, 1200); await s.until(2.2); await s.to(r"^decisions$", 0.5, 1.6, 900, nth=-1) if False else None
    await s.until(3.2); await s.scroll(250, 1500)
    seq = [(0, 5.4), (1, 6.6), (2, 7.8), (3, 9.0), (4, 10.6), (5, 12.6), (6, 14.6), (7, 15.3)]
    for i, t in seq:
        await s.until(t - 0.7); await s.to(ph, 0.5, 0.55, 650, nth=i)
    await s.until(16.4); await s.to(r"^next cycle in|in progress", 0.3, 0.5, 900)
async def s3_compute(s):
    y = await s.page_y(r"^compute map$"); await s.page.evaluate(f"window.scrollTo(0,{y - 250})"); await asyncio.sleep(0.8)
    await s.start(); await s.scroll(y - 120, 1300)
    await s.to(r"^GPU 2$", 1.5, 2.0, 900); await s.until(3.0); await s.to(r"^GPU 6$", 1.5, 2.0, 1000); await s.until(4.6)
    await s.to(r"^cpu cores$", 3.0, 3.5, 1000); await s.until(6.2); await s.to(r"^cpu cores$", 6.0, 5.0, 900)
    await s.until(7.6); await s.to(r"^modal fleet", 1.2, 2.6, 1000); await s.until(9.2); await s.to(r"containers$", -1.5, 2.6, 1200)
async def s4_problem(s):
    await s.start(); await s.to(r"^record$", 0.5, 2.2, 1000); await s.until(3.2)
    y = await s.page_y(r"^current construction$"); await s.scroll(y - 95, 1500)
    b = await s.page.evaluate("""() => { let best=null, a=0; for (const e of document.querySelectorAll('canvas,svg')) { const r=e.getBoundingClientRect(); if (r.width*r.height>a && r.width>300) { a=r.width*r.height; best=[r.x,r.y,r.width,r.height]; } } return best; }""")
    print("canvas", b); x, y0, w, h = b
    pts = [(0.30, 0.30, 5.6), (0.42, 0.44, 7.4), (0.60, 0.52, 9.4), (0.70, 0.72, 11.4), (0.50, 0.50, 13.6)]
    for fx, fy, t in pts:
        await s.glide(x + w * fx, y0 + h * fy, 1300); await s.until(t)
def dec_shot(did, cues):
    async def f(s):
        el = s.page.locator(f"#decision-{did}"); await el.wait_for(timeout=20000); await asyncio.sleep(2.5)
        btn = el.locator("button").first
        if await btn.get_attribute("aria-expanded") != "true": await btn.evaluate("b => b.click()"); await asyncio.sleep(0.8)
        y = (await el.bounding_box())["y"] + await s.page.evaluate("window.scrollY"); await s.page.evaluate(f"window.scrollTo(0,{max(0, y - 300)})"); await asyncio.sleep(1.0)
        await s.start()
        for pat, dx, dy, t in cues:
            b = await el.get_by_text(re.compile(pat, re.I)).first.bounding_box()
            if b: await s.glide(b["x"] + b["width"] * dx, b["y"] + b["height"] * dy, 1000)
            await s.until(t)
    return f
async def s6_memory(s):
    await asyncio.sleep(2.5); await s.start()
    await s.to(r"^proposer$", 0.5, -0.6, 1200); await s.until(2.6); await s.to(r"^critic$", 0.5, -0.8, 1100); await s.until(4.3)
    y = await s.page_y(r"^memory benchmark$"); await s.scroll(min(y - 120, 10000), 1400)
    await s.to(r"^accuracy$", 1.2, 5.0, 900); await s.until(8.0); await s.to(r"^accuracy$", 3.2, 4.0, 900); await s.until(9.4); await s.to(r"^accuracy$", 5.0, 4.0, 900)
async def s7_learning(s):
    await s.start(); await s.to(r"^reward per step$", 1.0, 8.0, 1000); await s.until(2.4); await s.to(r"^reward per step$", 4.5, 3.5, 2200)
    await s.until(5.4); await s.to(r"^valid-construction rate$", 2.5, 3.0, 1200); await s.until(7.2)
    await s.scroll(230, 1200); await s.to(r"^valid rate$", 6.0, 4.6, 1000, nth=-1); await s.until(11.2)
    y = await s.page_y(r"^modal agent sandboxes$"); await s.scroll(y - 110, 1500); await s.to(r"^\d+ runs$", 1.5, 0.5, 1000); await s.until(14.5); await s.to(r"^status$", 0.5, 5.0, 1200)
async def s8_gallery(s):
    await asyncio.sleep(1.5); await s.start(); await s.to(r"^Hadamard City$", 0.5, -8.0, 1200); await s.until(2.2)
    y = await s.page_y(r"^Three-body: the figure-eight"); await s.scroll(y - 620, 2000); await s.to(r"^Three-body: the figure-eight", 0.5, -8.0, 1000); await s.until(7.0)
    await s.scroll(y - 620 + 520, 1800); await s.to(r"^Three-body: candidate orbit", 0.5, -8.0, 1000)

d5 = SEC["s5_decisions"]["vdur"]; a5, b5 = round(d5 * 0.39, 2), round(d5 * 0.20, 2)
SHOTS = [
 ("s2_loop", "/", SEC["s2_loop"]["vdur"], s2_loop),
 ("s3_compute", "/", SEC["s3_compute"]["vdur"], s3_compute),
 ("s4_problem", "/problems/no-three-in-line-75", SEC["s4_problem"]["vdur"], s4_problem),
 ("s5a_dec211", "/decisions?agent=proposer&focus=211", a5, dec_shot(211, [(r"gpt-6-astra|^research$", 0.5, 0.5, 1.6), (r"^sources", 0.5, 0.5, 3.6), (r"No-three-in-line, n = 75", 0.5, 0.6, 99)])),
 ("s5b_dec219", "/decisions?agent=referee&focus=219", b5, dec_shot(219, [(r"^approve$", 0.5, 0.6, 1.5), (r"claude-fable-5-2 on proposer", 0.4, 0.6, 99)])),
 ("s5c_dec191", "/decisions?problem=no-three-in-line-75&focus=191", round(d5 - a5 - b5, 2), dec_shot(191, [(r"^launch$", 0.5, 0.6, 1.2), (r"^predicted$", 1.5, 2.2, 4.4), (r"^observed", 1.2, 2.4, 99)])),
 ("s6_memory", "/memory", SEC["s6_memory"]["vdur"], s6_memory),
 ("s7_learning", "/learning", SEC["s7_learning"]["vdur"], s7_learning),
 ("s8_gallery", "/gallery", SEC["s8_gallery"]["vdur"], s8_gallery),
]
async def main():
    want = sys.argv[1:]
    async with async_playwright() as p:
        br = await p.chromium.launch(headless=not os.environ.get("HEADED"), args=["--force-device-scale-factor=1", "--hide-scrollbars"] + os.environ.get("CHROME_ARGS", "").split())
        ctx = await br.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, url, dur, fn in SHOTS:
            if want and name not in want: continue
            if name == "s2_loop":   # try to catch the loop mid-cycle so the phase stepper is lit
                for _ in range(45):
                    if state()["loop"]["phase"] in ("telemetry", "critic", "memory", "literature", "propose"): break
                    time.sleep(2)
                print("loop phase at record:", state()["loop"]["phase"], flush=True)
            for attempt in range(3):
                page = await ctx.new_page()
                try:
                    await page.goto(BASE + url, wait_until="domcontentloaded", timeout=30000)
                    try: await page.wait_for_load_state("networkidle", timeout=8000)
                    except Exception: pass
                    await asyncio.sleep(3.0); await page.evaluate(CURSOR_JS)
                    cdp = await ctx.new_cdp_session(page); s = Shot(page, cdp, name, dur)
                    await asyncio.wait_for(fn(s), timeout=dur + 90); await s.finish(); await page.close(); break
                except Exception as e:
                    print("SHOT FAILED", name, attempt, type(e).__name__, str(e)[:300], flush=True)
                    try: await page.close()
                    except Exception: pass
        await br.close()
asyncio.run(main())
