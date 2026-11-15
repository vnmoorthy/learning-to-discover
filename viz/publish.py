"""Copy final renders to web/public/gallery/ and write web/public/gallery/gallery.json (same shape as /api/gallery).

Usage: python3 viz/publish.py

- Only files that exist are published; a missing render is skipped with a warning (never a placeholder).
- Captions are computed from viz/data/*.json. A render made from different data than the caption (checked with
  the <render>.stamp.json that viz/render.py writes) is refused, so a caption can never describe other pixels.
- Big PNGs are published as visually lossless JPEG (q90, 4:4:4, about 10x smaller) and gallery.json points at
  the JPEG; the PNG is published too, so older links to /gallery/<name>.png keep working.
- MP4s are remuxed with +faststart (no re-encode) so playback starts before the whole file has downloaded.
- Previously published files are never deleted.
"""
import datetime, hashlib, json, os, shutil, subprocess, sys

VIZ = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(VIZ)
RENDERS = os.path.join(VIZ, "renders")
DATA = os.path.join(VIZ, "data")
GALLERY = os.path.join(ROOT, "web", "public", "gallery")
JPEG_FOR = {"hero.png", "hadamard_city.png", "snake.png", "og_bg_gptimage2.png"}
KEYS = ("title", "src", "kind", "made_with", "caption")


def sha1(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()


def when(utc):
    """'06:32 PT, Nov 15' from an ISO UTC string (falls back to UTC if no tz database)."""
    t = datetime.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        t = t.astimezone(ZoneInfo("America/Los_Angeles"))
        return t.strftime("%H:%M PT, %b ") + str(t.day)
    except Exception:  # noqa: BLE001
        return t.strftime("%H:%M UTC, %b ") + str(t.day)


def items():
    lat = json.load(open(os.path.join(DATA, "lattice.json")))
    had = json.load(open(os.path.join(DATA, "hadamard.json")))
    snk = json.load(open(os.path.join(DATA, "snake.json")))
    blender = "Blender 5.2 EEVEE (script by GPT-6 Astra)"
    lat_src = "SAT model %s, seed %d, round %d" % (lat["sym"], lat["seed"], lat["round"])
    if lat.get("snapshot_utc"):
        lat_src += ", taken %s" % when(lat["snapshot_utc"])
    if lat["violated"]:
        lat_title = "The Lattice: %d points, %d lines to go" % (lat["count"], lat["violated"])
        lat_state = "red threads join chosen points that are still collinear (%d violated lines)" % lat["violated"]
    else:
        lat_title = "The Lattice: %d points, no three in a line" % lat["count"]
        lat_state = "no line holds three of them"
    plus = sum(v == 1 for row in had["matrix"] for v in row)
    cells = had["n"] * had["n"]
    return [
        {"file": "hero.png", "data": "lattice.json", "kind": "image", "title": lat_title, "made_with": blender,
         "caption": "Snapshot of our live no-three-in-line search on the 75x75 grid (%s). The %d chosen points "
                    "glow as pillars; %s. Amber pillars sit on 4 or more violated lines: the solver's hot spots. "
                    "Record to beat: %d (%s)." % (lat_src, lat["count"], lat_state, lat["record_count"],
                                                  lat["record_holder"])},
        {"file": "lattice_orbit.mp4", "data": "lattice.json", "kind": "video", "title": "Lattice orbit",
         "made_with": blender + ", FFMPEG H.264",
         "caption": "8-second seamless camera orbit around the same live SAT snapshot (%s): %d points, %d violated "
                    "lines. The model is 180-degree symmetric, so the view repeats every half turn."
                    % (lat_src, lat["count"], lat["violated"]) if lat["sym"].startswith("rot180") else
                    "8-second seamless camera orbit around the same live SAT snapshot (%s): %d points, %d violated "
                    "lines." % (lat_src, lat["count"], lat["violated"])},
        {"file": "hadamard_city.png", "data": "hadamard.json", "kind": "image", "title": "Hadamard City",
         "made_with": blender,
         "caption": "The record %dx%d +-1 matrix (log10|det| = %.4f, %s) extruded as a city: the %d +1 entries are "
                    "cyan-roofed towers, the %d -1 entries low amber plinths (mostly hidden between towers at this "
                    "angle); tower height follows the mean sign of each 5x5 neighbourhood."
                    % (had["n"], had["n"], had["log10_det"], had["holder"], plus, cells - plus)},
        {"file": "snake.png", "data": "snake.json", "kind": "image", "title": "Snake in the 13-cube",
         "made_with": blender,
         "caption": "The record %d-edge snake-in-the-box (%s), verified and linearly projected from 13 dimensions to "
                    "3: rarely flipped coordinates become long bridges, frequent ones local wiggles. Colour runs amber "
                    "(start) to cyan (end); faint dust marks all 8192 cube vertices." % (snk["edges"], snk["holder"])},
        {"file": "snake_turntable.mp4", "data": "snake.json", "kind": "video", "title": "Snake turntable",
         "made_with": blender + ", FFMPEG H.264",
         "caption": "The same %d-edge snake rotating once about its vertical axis." % snk["edges"]},
        {"file": "og-banner.png", "data": "lattice.json", "stamp_of": "wip/lattice_banner.png", "kind": "image",
         "title": "Social banner",
         "made_with": "gpt-image-2 backdrop + Blender 5.2 render (script by GPT-6 Astra) + PIL type",
         "caption": "1280x640 GitHub social preview. The backdrop is AI-generated art (illustrative, not data); the "
                    "lattice on the right is the Blender render of our real SAT snapshot."},
        {"file": "og_bg_gptimage2.png", "kind": "image", "title": "gpt-image-2 backdrop",
         "made_with": "gpt-image-2 (OpenAI images API)",
         "caption": "Illustrative backdrop painted by gpt-image-2 for the banner (art direction only; not real data)."},
    ]


def check_stamp(it):
    """None if fine, else the reason this render must not be published with this caption."""
    if "data" not in it:
        return None
    stamp = os.path.join(RENDERS, it.get("stamp_of", it["file"])) + ".stamp.json"
    if not os.path.exists(stamp):
        print("  note: %s has no render stamp (rendered before stamps existed); not checked" % it["file"])
        return None
    st = json.load(open(stamp))
    if st["data_sha1"] != sha1(os.path.join(DATA, it["data"])):
        return ("%s was rendered from a different viz/data/%s than the caption uses (rendered %s). "
                "Re-render it: bash viz/build_all.sh" % (it["file"], it["data"], st.get("rendered_utc")))
    return None


def to_jpeg(src, dst):
    from PIL import Image
    Image.open(src).convert("RGB").save(dst + ".tmp", "JPEG", quality=90, subsampling=0, optimize=True,
                                        progressive=True)
    os.replace(dst + ".tmp", dst)


def faststart(src, dst):
    """Lossless remux with the moov atom first; plain copy if ffmpeg is missing or fails."""
    ff = shutil.which("ffmpeg")
    if ff:
        tmp = dst + ".tmp.mp4"
        p = subprocess.run([ff, "-v", "error", "-y", "-i", src, "-c", "copy", "-movflags", "+faststart", tmp],
                           capture_output=True, text=True)
        if p.returncode == 0 and os.path.getsize(tmp) > 0:
            os.replace(tmp, dst)
            return "faststart"
        if os.path.exists(tmp):
            os.remove(tmp)
        print("  warning: ffmpeg remux failed (%s); copying as is" % p.stderr.strip()[-200:])
    shutil.copy2(src, dst)
    return "copied"


def main():
    its = [it for it in items() if os.path.exists(os.path.join(RENDERS, it["file"]))]
    for it in items():
        if it not in its:
            print("skip (not rendered):", it["file"])
    bad = [r for r in map(check_stamp, its) if r]
    if bad:
        print("REFUSING to publish (nothing was changed):\n  " + "\n  ".join(bad))
        sys.exit(1)
    os.makedirs(GALLERY, exist_ok=True)
    out = []
    for it in its:
        src = os.path.join(RENDERS, it["file"])
        dst = os.path.join(GALLERY, it["file"])
        how = faststart(src, dst) if it["file"].endswith(".mp4") else (shutil.copy2(src, dst) and "copied")
        pub = it["file"]
        if it["file"] in JPEG_FOR:
            pub = it["file"].rsplit(".", 1)[0] + ".jpg"
            to_jpeg(src, os.path.join(GALLERY, pub))
            how += " + %s (%d KB)" % (pub, os.path.getsize(os.path.join(GALLERY, pub)) // 1024)
        out.append({"title": it["title"], "src": "/gallery/" + pub, "kind": it["kind"],
                    "made_with": it["made_with"], "caption": it["caption"]})
        print("published %s (%d KB, %s)" % (it["file"], os.path.getsize(src) // 1024, how))
    # Contract check (SPEC section 4, GET /api/gallery) before anything reads it.
    for o in out:
        assert tuple(o) == KEYS and all(isinstance(o[k], str) and o[k] for k in KEYS), o
        assert o["kind"] in ("image", "video") and o["src"].startswith("/gallery/"), o
        assert os.path.isfile(os.path.join(GALLERY, o["src"][len("/gallery/"):])), o["src"]
    tmp = os.path.join(GALLERY, "gallery.json.tmp")
    json.dump(out, open(tmp, "w"), indent=2)
    os.replace(tmp, os.path.join(GALLERY, "gallery.json"))
    print("wrote", os.path.join(GALLERY, "gallery.json"), len(out), "items")


if __name__ == "__main__":
    main()
