"""Ask GPT-6 Astra (OpenAI Responses API, model gpt-6-astra) to write or fix a Blender bpy script.

Every call saves, next to the script in viz/scripts/:
  <name>.vN.prompt.md     the exact prompt sent (text; images noted by path)
  <name>.vN.py            the script Astra returned
  <name>.vN.response.md   Astra's full reply (code + notes), with model/usage
and copies the newest version to <name>.py (plus <name>.prompt.md = the newest prompt).

Usage:
  python3 viz/astra.py new <name> <brief.md>
  python3 viz/astra.py fix <name> --feedback "what is wrong" [--image render.png] [--log blender.log]
"""
import argparse, base64, glob, io, json, os, re, sys, time

VIZ = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(VIZ)
SCRIPTS = os.path.join(VIZ, "scripts")
sys.path.insert(0, ROOT)
import envload  # noqa: E402

MODEL = "gpt-6-astra"

SYSTEM = """You are GPT-6 Astra acting as a senior technical artist who writes Blender Python (bpy) scripts.
You write ONE complete, self-contained Python script that runs headless with
`Blender -b --factory-startup -P script.py -- <args>` on Blender 5.2.1 (macOS, Apple Silicon), renders with
EEVEE, and writes the output file. Rules:
- Use ONLY the Blender API as described in the API notes provided (they were verified on this exact Blender).
- Read every number from the JSON data file given by --data; never invent data. Do not hardcode data.
- Parse args after '--' with argparse. Always write to the absolute --out path.
- Build large repeated geometry as a single mesh (from_pydata) for speed. Keep total render time sane.
- Print short progress lines (build time, render time) to stdout.
- Reply with the full script in ONE ```python fenced block, then at most 6 bullet notes on design choices."""


def api_notes():
    return open(os.path.join(VIZ, "blender_api_notes.md")).read()


def next_version(name):
    vs = [int(m.group(1)) for f in glob.glob(os.path.join(SCRIPTS, name + ".v*.py"))
          if (m := re.search(r"\.v(\d+)\.py$", f))]
    return max(vs, default=0) + 1


def image_part(path, max_w=1280):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    return {"type": "input_image", "image_url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}


def call(text, images=()):
    envload.load()
    from openai import OpenAI
    client = OpenAI()
    content = [{"type": "input_text", "text": text}] + [image_part(p) for p in images]
    t = time.time()
    kw = dict(model=MODEL, instructions=SYSTEM, input=[{"role": "user", "content": content}])
    try:
        r = client.responses.create(reasoning={"effort": "medium"}, **kw)
    except Exception as e:  # model may not accept the reasoning param
        # API errors can echo a (masked) key; redact anything key-shaped before printing.
        print("retrying without reasoning param:", type(e).__name__,
              re.sub(r"(sk|tml|key)-[A-Za-z0-9_*.-]{6,}", "<redacted>", str(e))[:160])
        r = client.responses.create(**kw)
    dt = time.time() - t
    usage = getattr(r, "usage", None)
    return r.output_text, {"model": r.model, "seconds": round(dt, 1),
                           "input_tokens": getattr(usage, "input_tokens", None),
                           "output_tokens": getattr(usage, "output_tokens", None)}


def extract_code(reply):
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", reply, re.S)
    if not blocks:
        raise SystemExit("Astra reply had no code block")
    return max(blocks, key=len)


def save(name, prompt, images, reply, meta):
    os.makedirs(SCRIPTS, exist_ok=True)
    v = next_version(name)
    base = os.path.join(SCRIPTS, "%s.v%d" % (name, v))
    ptxt = "<!-- model: %s | system prompt: see viz/astra.py SYSTEM -->\n\n%s" % (MODEL, prompt)
    if images:
        ptxt += "\n\n[Attached images: %s]\n" % ", ".join(os.path.relpath(p, ROOT) for p in images)
    open(base + ".prompt.md", "w").write(ptxt)
    code = extract_code(reply)
    header = "# Written by %s (OpenAI Responses API), version %d, %s. Prompt: %s\n" % (
        meta["model"], v, time.strftime("%Y-%m-%d %H:%M"), os.path.basename(base + ".prompt.md"))
    open(base + ".py", "w").write(header + code)
    open(base + ".response.md", "w").write("<!-- %s -->\n\n%s" % (json.dumps(meta), reply))
    open(os.path.join(SCRIPTS, name + ".py"), "w").write(header + code)
    open(os.path.join(SCRIPTS, name + ".prompt.md"), "w").write(ptxt)
    print("saved %s.v%d (%s s, out tokens %s)" % (name, v, meta["seconds"], meta["output_tokens"]))
    return base + ".py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["new", "fix"])
    ap.add_argument("name")
    ap.add_argument("brief", nargs="?")
    ap.add_argument("--feedback", default="")
    ap.add_argument("--image", action="append", default=[])
    ap.add_argument("--log")
    a = ap.parse_args()
    if a.mode == "new":
        brief = open(a.brief).read()
        prompt = brief + "\n\n## Blender API notes (verified)\n\n" + api_notes()
        images = a.image
    else:
        brief_path = os.path.join(VIZ, "briefs", a.name + ".md")
        brief = open(brief_path).read()
        cur = open(os.path.join(SCRIPTS, a.name + ".py")).read()
        prompt = (brief + "\n\n## Blender API notes (verified)\n\n" + api_notes() +
                  "\n\n## Your current script (previous version)\n\n```python\n" + cur + "\n```\n")
        if a.log:
            tail = open(a.log, errors="replace").read()[-4000:]
            prompt += "\n## Blender output (tail)\n\n```\n" + tail + "\n```\n"
        if a.image:
            prompt += "\nThe attached image is the current render from this script.\n"
        prompt += ("\n## Art director feedback (fix all of this, keep what works)\n\n" + a.feedback +
                   "\n\nReturn the full corrected script.")
        images = a.image
    reply, meta = call(prompt, images)
    save(a.name, prompt, images, reply, meta)


if __name__ == "__main__":
    main()
