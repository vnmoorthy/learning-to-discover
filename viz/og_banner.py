"""GitHub social banner (1280x640): gpt-image-2 background art composited with a real Blender render + text.

Steps
  1. gpt-image-2 (OpenAI images API, size 1536x1024) paints an abstract, text-free backdrop.
     Saved to viz/renders/og_bg_gptimage2.png with the prompt in viz/renders/og_bg_gptimage2.prompt.txt.
     Skipped if that file exists (pass --regen to repaint).
  2. The Blender lattice render (real SAT data) at 1280x640 is screen-blended over the right side.
  3. Title + tagline set with PIL (exact text, no model-drawn lettering).

Usage: python3 viz/og_banner.py --plate viz/renders/wip/lattice_banner.png [--regen]
Output: viz/renders/og-banner.png
"""
import argparse, base64, os, sys, time

VIZ = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(VIZ)
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

BG = os.path.join(VIZ, "renders", "og_bg_gptimage2.png")
OUT = os.path.join(VIZ, "renders", "og-banner.png")
W, H = 1280, 640

PROMPT = (
    "Abstract cinematic backdrop for a mathematics research lab. A dark near-black studio (#07080B) with an "
    "infinite field of tiny matte graphite pillars on a glossy black floor receding into darkness, a few "
    "pillars glowing electric cyan (#3DF5FF) and a few glowing warm amber (#FFB547), extremely fine faint red "
    "laser threads crossing between some glowing points, shallow depth of field with soft round bokeh, subtle "
    "volumetric haze, premium product-film look, minimal and clean, lots of dark negative space on the left "
    "third. Absolutely no text, no letters, no numbers, no logos, no watermark."
)


def gen_background():
    import envload
    envload.load()
    from openai import OpenAI
    client = OpenAI()
    t = time.time()
    r = client.images.generate(model="gpt-image-2", prompt=PROMPT, size="1536x1024", n=1)
    b64 = r.data[0].b64_json
    os.makedirs(os.path.dirname(BG), exist_ok=True)
    open(BG, "wb").write(base64.b64decode(b64))
    open(BG.replace(".png", ".prompt.txt"), "w").write("model: gpt-image-2, size 1536x1024\n\n" + PROMPT + "\n")
    print("gpt-image-2 background: %.1fs -> %s" % (time.time() - t, BG))


def font(names, size):
    for path, idx in names:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()


def cover(im, w, h):
    """Resize + center-crop to exactly w x h."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True, help="Blender render to composite (any size, cropped to 2:1)")
    ap.add_argument("--regen", action="store_true")
    a = ap.parse_args()
    if a.regen or not os.path.exists(BG):
        gen_background()

    bg = np.asarray(cover(Image.open(BG).convert("RGB"), W, H)).astype(np.float32) / 255.0
    plate = np.asarray(cover(Image.open(os.path.join(ROOT, a.plate) if not os.path.isabs(a.plate) else a.plate)
                             .convert("RGB"), W, H)).astype(np.float32) / 255.0

    x = np.linspace(0, 1, W)[None, :, None]
    # Blender plate fades in from 44% to 74% of the width; screen blend keeps both glows.
    m = np.clip((x - 0.44) / 0.30, 0, 1) ** 1.5
    bg = bg * 0.72
    comp = bg * (1 - m) + (1 - (1 - bg) * (1 - plate)) * m
    # Left-side darkening for text legibility.
    dark = np.clip(1 - (x - 0.0) / 0.68, 0, 1) ** 1.4 * 0.85
    comp = comp * (1 - dark) + np.array([7, 8, 11], np.float32)[None, None, :] / 255.0 * dark
    # Vignette.
    yy = np.linspace(-1, 1, H)[:, None, None]
    xx = np.linspace(-1, 1, W)[None, :, None]
    comp *= 1 - 0.35 * np.clip((xx ** 2 * 0.6 + yy ** 2) - 0.35, 0, 1)
    img = Image.fromarray((np.clip(comp, 0, 1) * 255).astype(np.uint8))

    d = ImageDraw.Draw(img)
    title_f = font([("/System/Library/Fonts/Avenir Next.ttc", 2), ("/System/Library/Fonts/HelveticaNeue.ttc", 1)], 74)
    tag_f = font([("/System/Library/Fonts/Avenir Next.ttc", 7), ("/System/Library/Fonts/HelveticaNeue.ttc", 0)], 27)
    mono_f = font([("/System/Library/Fonts/Menlo.ttc", 0)], 17)
    x0, y0 = 72, 228
    # kicker with a short cyan rule
    d.rectangle((x0, y0 - 46, x0 + 34, y0 - 44), fill=(61, 245, 255))
    d.text((x0 + 46, y0 - 56), "AUTONOMOUS RESEARCH", font=mono_f, fill=(61, 245, 255))
    # title with a soft glow
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).text((x0, y0), "Learning to Discover", font=title_f, fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    img = Image.composite(Image.new("RGB", (W, H), (61, 245, 255)), img, glow.point(lambda v: int(v * 0.22)))
    d = ImageDraw.Draw(img)
    d.text((x0, y0), "Learning to Discover", font=title_f, fill=(244, 247, 250))
    tb = d.textbbox((x0, y0), "Learning to Discover", font=title_f)
    tag1 = "An AI lab that gets better at"
    tag2 = "discovering mathematics by doing it"
    d.text((x0 + 2, tb[3] + 26), tag1, font=tag_f, fill=(178, 186, 198))
    d.text((x0 + 2, tb[3] + 26 + 38), tag2, font=tag_f, fill=(178, 186, 198))
    # amber accent dot
    ay = tb[3] + 26 + 38 + 62
    d.ellipse((x0 + 2, ay, x0 + 12, ay + 10), fill=(255, 181, 71))
    d.text((x0 + 24, ay - 5), "no-three-in-line 75  /  hadamard 51  /  spencer", font=mono_f, fill=(120, 128, 140))
    img.save(OUT)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
