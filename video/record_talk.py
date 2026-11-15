"""Record the screen footage for the presenter demo video, one clip per talk-track section (docs/TALK_TRACK.md).

Durations come from the presenter's own take (video/me/sections.json, written by compose_talk.py align), so every clip
is exactly as long as the presenter speaks over it. Read-only navigation against the live lab: no mutating clicks.
Runs headed Chrome by default so the WebGL black hole renders on the GPU.

  python3 video/record_talk.py            # all sections
  python3 video/record_talk.py s4 s5      # some sections
"""
import asyncio, base64, json, os, re, shutil, subprocess, sys, time
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("APP_URL", "http://127.0.0.1:8787")
W, H = 1920, 1080
SECS = {s["id"]: s for s in json.load(open(f"{HERE}/me/sections.json"))["sections"]}
OUT = f"{HERE}/clips_talk"
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
        self.page, self.cdp, self.name, self.dur = page, cdp, name, dur
        self.frames, self.mx, self.my, self.t0 = [], 960, 540, None

    async def start(self):
        d = f"{HERE}/frames_talk/{self.name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d); self.dir = d

        async def ack(sid):
            try: await self.cdp.send("Page.screencastFrameAck", {"sessionId": sid})
            except Exception: pass

        def on(ev):
            p = f"{d}/{len(self.frames):05d}.jpg"; open(p, "wb").write(base64.b64decode(ev["data"]))
            self.frames.append((time.time(), p)); asyncio.ensure_future(ack(ev["sessionId"]))
        self.cdp.on("Page.screencastFrame", on)
        await self.cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "maxWidth": W, "maxHeight": H, "everyNthFrame": 1})
        await self.page.mouse.move(self.mx, self.my); await asyncio.sleep(0.3); self.t0 = time.time()

    def now(self): return time.time() - self.t0

    async def until(self, frac):
        """wait until a fraction of this clip's duration has elapsed"""
        d = min(frac * self.dur, self.dur + 0.3) - self.now()
        if d > 0: await asyncio.sleep(d)

    async def glide(self, x, y, ms=900, down=False):
        x0, y0 = self.mx, self.my; st = time.time()
        if down: await self.page.mouse.down()
        while True:
            k = min(1.0, (time.time() - st) * 1000 / ms); e = k * k * (3 - 2 * k)
            await self.page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e)
            if k >= 1: break
            await asyncio.sleep(0.012)
        if down: await self.page.mouse.up()
        self.mx, self.my = x, y

    async def scroll(self, y, ms=1400): await self.page.evaluate("([y,ms]) => window.__scrollTo(y,ms)", [y, ms])

    async def page_y(self, pat, nth=0):
        loc = self.page.get_by_text(re.compile(pat, re.I)).nth(nth)
        b = await loc.bounding_box(); return b["y"] + await self.page.evaluate("window.scrollY")

    async def to(self, pat, dx=0.5, dy=0.5, ms=900, nth=0):
        try: b = await self.page.get_by_text(re.compile(pat, re.I)).nth(nth).bounding_box()
        except Exception: b = None
        if b: await self.glide(b["x"] + b["width"] * dx, b["y"] + b["height"] * dy, ms)

    async def biggest_canvas(self):
        return await self.page.evaluate("""() => { let best=null, a=0; for (const e of document.querySelectorAll('canvas')) {
          const r=e.getBoundingClientRect(); if (r.width*r.height>a && r.width>300 && r.bottom>0 && r.top<innerHeight) { a=r.width*r.height; best=[r.x,r.y,r.width,r.height]; } } return best; }""")

    async def finish(self):
        await self.until(1.0); await asyncio.sleep(0.3); await self.cdp.send("Page.stopScreencast"); await asyncio.sleep(0.2)
        fr = self.frames; pre = [f for f in fr if f[0] <= self.t0]; post = [f for f in fr if f[0] > self.t0]
        seq = ([(self.t0, pre[-1][1])] if pre else []) + post; end = self.t0 + self.dur + 0.3
        with open(f"{self.dir}/list.txt", "w") as f:
            for i, (t, p) in enumerate(seq):
                nt = seq[i + 1][0] if i + 1 < len(seq) else end
                if nt - t > 0: f.write(f"file '{p}'\nduration {nt - t:.4f}\n")
            f.write(f"file '{seq[-1][1]}'\n")
        os.makedirs(OUT, exist_ok=True)
        out = f"{OUT}/{self.name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{self.dir}/list.txt",
                        "-vf", f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p", "-t", f"{self.dur:.2f}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16", out], check=True)
        print(self.name, "frames", len(seq), "dur", round(self.dur, 2), "->", out, flush=True)


# ---------------------------------------------------------------- shots (prep is unrecorded, then start())
async def s1(s):   # hook: Mission Control hero
    await s.start(); await s.to(r"^cycles$", 0.5, 1.6, 1400); await s.until(0.5); await s.to(r"^decisions$", 0.5, 1.6, 1000, nth=-1)


async def s2(s):   # the loop + compute map
    await s.start()
    await s.scroll(240, 1400); await s.until(0.12)
    for i in range(8):
        await s.to("css=[data-phase]", 0.5, 0.55, 500, nth=i) if False else None
        try:
            b = await s.page.locator("[data-phase]").nth(i).bounding_box()
            if b: await s.glide(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2, 550)
        except Exception: pass
        await s.until(0.12 + 0.05 * (i + 1))
    y = await s.page_y(r"^compute map$"); await s.scroll(y - 110, 1500); await s.until(0.62)
    await s.to(r"^GPU 2$", 1.5, 2.0, 900); await s.until(0.72); await s.to(r"^cpu cores$", 3.0, 3.5, 1000); await s.until(0.84)
    await s.to(r"^modal fleet", 1.2, 2.6, 1000)


async def s3(s):   # refuted prediction, then the no-three problem page
    el = s.page.locator("#decision-191")
    try:
        await el.wait_for(timeout=15000); await asyncio.sleep(1.5)
        btn = el.locator("button").first
        if await btn.get_attribute("aria-expanded") != "true": await btn.evaluate("b => b.click()"); await asyncio.sleep(0.6)
        y = (await el.bounding_box())["y"] + await s.page.evaluate("window.scrollY"); await s.page.evaluate(f"window.scrollTo(0,{max(0, y - 260)})")
    except Exception: pass
    await asyncio.sleep(0.8); await s.start()
    for pat, t in ((r"^predicted$", 0.25), (r"^observed", 0.5)):
        try:
            b = await el.get_by_text(re.compile(pat, re.I)).first.bounding_box()
            if b: await s.glide(b["x"] + b["width"] * 1.4, b["y"] + b["height"] * 2.2, 1000)
        except Exception: pass
        await s.until(t)
    await s.page.goto(BASE + "/problems/no-three-in-line-75", wait_until="domcontentloaded"); await asyncio.sleep(2.0)
    await s.page.evaluate(CURSOR_JS); await s.to(r"^record$", 0.5, 2.2, 900)


async def s4(s):   # Event Horizon: play with the live black hole, then the study
    y = await s.page_y(r"^EVENT HORIZON · black hole information$"); await s.page.evaluate(f"window.scrollTo(0,{y - 70})"); await asyncio.sleep(3.0)
    await s.start()
    c = await s.biggest_canvas(); x, y0, w, h = c; cx, cy = x + w / 2, y0 + h / 2
    await s.glide(cx + w * 0.18, cy - h * 0.05, 700); await s.glide(cx - w * 0.10, cy + h * 0.28, 2200, down=True)   # orbit above the disk
    await s.until(0.22)
    await s.glide(cx, cy, 500); await s.page.mouse.down(); await s.page.mouse.up()            # activate scroll-zoom (also pauses spin)
    for _ in range(14): await s.page.mouse.wheel(0, -120); await asyncio.sleep(0.09)
    await s.until(0.42)
    await s.glide(cx + w * 0.1, cy, 500); await s.glide(cx - w * 0.15, cy - h * 0.30, 2000, down=True)   # orbit to below the disk
    await s.until(0.55)
    try:
        lens = s.page.get_by_role("button", name=re.compile("^Lensing$"))
        b = await lens.bounding_box(); await s.glide(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2, 700); await lens.click()
        await s.until(0.68); await lens.click()
    except Exception: pass
    await s.until(0.78)
    for _ in range(10): await s.page.mouse.wheel(0, 120); await asyncio.sleep(0.08)
    await s.page.goto(BASE + "/problems/event-horizon", wait_until="domcontentloaded"); await asyncio.sleep(2.5); await s.page.evaluate(CURSOR_JS)
    try:
        y = await s.page_y(r"^Research cycles$|^Figures$"); await s.scroll(y - 120, 1600)
    except Exception: await s.scroll(1400, 1600)


async def s5(s):   # STARFORGE
    await asyncio.sleep(1.0); await s.start(); await s.to(r"STARFORGE", 0.3, 0.5, 1000); await s.until(0.2)
    try:
        y = await s.page_y(r"mass.radius|Mass-radius|M-R", 0); await s.scroll(y - 160, 1800)
    except Exception: await s.scroll(900, 1800)
    await s.until(0.6)
    try:
        y = await s.page_y(r"causal|reject|twin", 0); await s.scroll(y - 160, 1600)
    except Exception: await s.scroll(1800, 1600)


async def s6(s):   # three-body on Physics: drag the orbits
    y = await s.page_y(r"^Three-body periodic orbits"); await s.page.evaluate(f"window.scrollTo(0,{y - 70})"); await asyncio.sleep(2.5)
    await s.start()
    c = await s.biggest_canvas(); x, y0, w, h = c
    await s.glide(x + w * 0.6, y0 + h * 0.5, 700); await s.glide(x + w * 0.35, y0 + h * 0.62, 2400, down=True); await s.until(0.6)
    await s.to(r"^vx$", 0.5, 3.0, 1200)


async def s7(s):   # self-improvement + memory benchmark
    await s.start(); await s.to(r"^reward per step$", 1.0, 8.0, 1000); await s.until(0.3); await s.to(r"^valid-construction rate$", 2.5, 3.0, 1200)
    await s.until(0.55); await s.page.goto(BASE + "/memory", wait_until="domcontentloaded"); await asyncio.sleep(2.0); await s.page.evaluate(CURSOR_JS)
    try:
        y = await s.page_y(r"^memory benchmark$"); await s.scroll(y - 120, 1400); await s.to(r"^accuracy$", 1.2, 5.0, 900)
    except Exception: pass


async def s8(s):   # close: Mission Control top
    await s.start(); await s.until(0.4); await s.to(r"Phoenixastar", 0.5, 0.5, 1200)


SHOTS = [("s1", "/", s1), ("s2", "/", s2), ("s3", "/decisions?problem=no-three-in-line-75&focus=191", s3), ("s4", "/physics", s4),
         ("s5", "/problems/neutron-star-eos", s5), ("s6", "/physics", s6), ("s7", "/learning", s7), ("s8", "/", s8)]


async def main():
    want = sys.argv[1:]
    async with async_playwright() as p:
        br = await p.chromium.launch(headless=bool(os.environ.get("HEADLESS")), args=["--force-device-scale-factor=1", "--hide-scrollbars", "--window-size=1920,1080"])
        ctx = await br.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, url, fn in SHOTS:
            if want and name not in want: continue
            if name not in SECS: continue
            dur = SECS[name]["dur"]
            for attempt in range(2):
                page = await ctx.new_page()
                try:
                    await page.goto(BASE + url, wait_until="domcontentloaded", timeout=30000); await asyncio.sleep(3.0)
                    await page.evaluate(CURSOR_JS); cdp = await ctx.new_cdp_session(page); s = Shot(page, cdp, name, dur)
                    page.set_default_timeout(6000)
                    try: await asyncio.wait_for(fn(s), timeout=dur + 60)
                    except Exception as e:
                        print("shot actions incomplete", name, type(e).__name__, str(e)[:160], flush=True)
                        if s.t0 is None: await s.start()
                    await s.finish(); await page.close(); break
                except Exception as e:
                    print("SHOT FAILED", name, attempt, type(e).__name__, str(e)[:240], flush=True)
                    try: await page.close()
                    except Exception: pass
        await br.close()

asyncio.run(main())
