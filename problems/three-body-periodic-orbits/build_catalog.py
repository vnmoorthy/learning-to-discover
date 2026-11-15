"""Build catalog.json: known periodic orbits (zero angular momentum, isosceles collinear start) from the literature.

  python3 build_catalog.py <dir with the Li-Liao tables>
Tables are the public files of https://github.com/sjtu-liao/three-body :
  three-body-pictures.md, three-body-free-group-word.md                 (Li & Liao 2017, 695 equal-mass families)
  three-body-unequal-mass-pictures.md, ...-unequal-mass-free-group-word.md (Li, Jing & Liao 2018, 1349 families, m3 != 1)
Every entry is re-integrated with our own verifier code to compute OUR canonical syzygy word (so words are compared
in one convention) and its return error (the published initial conditions have 10 digits).
"""
import json, os, re, sys, time
import numpy as np
import verifier as V

SD2013 = [  # Suvakov & Dmitrasinovic, PRL 110, 114301 (2013), Table I (5-6 digit values as printed there)
    ("figure-eight (Moore 1993)", 0.347111, 0.532728, 6.3250, "(abAB)"),
    ("butterfly I", 0.30689, 0.12551, 6.2356, "(ab)^2(AB)^2"),
    ("butterfly II", 0.39295, 0.09758, 7.0039, "(ab)^2(AB)^2"),
    ("bumblebee", 0.18428, 0.58719, 63.5345, "(b^2(ABab)^2A^2(baBA)^2ba)(B^2(abAB)^2a^2(BAba)^2BA)"),
    ("moth I", 0.46444, 0.39606, 14.8939, "ba(BAB)ab(ABA)"),
    ("moth II", 0.43917, 0.45297, 28.6703, "(abAB)^2A(baBA)^2B"),
    ("butterfly III", 0.40592, 0.23016, 13.8658, "(ab)^2(ABA)(ba)^2(BAB)"),
    ("moth III", 0.38344, 0.37736, 25.8406, "(babABA)^2a(abaBAB)^2b"),
    ("goggles", 0.08330, 0.12789, 10.4668, "(ab)^2ABBA(ba)^2BAAB"),
    ("butterfly IV", 0.350112, 0.07934, 79.4759, "((ab)^2(AB)^2)^6A((ba)^2(BA)^2)^6B"),
    ("dragonfly", 0.08058, 0.58884, 21.2710, "(b^2(ABabAB))(a^2(BAbaBA))"),
    ("yarn", 0.55906, 0.34919, 55.5018, "(babABabaBA)^3"),
    ("yin-yang I a", 0.51394, 0.30474, 17.3284, "(ab)^2(ABA)ba(BAB)"),
    ("yin-yang I b", 0.28270, 0.32721, 10.9626, "(ab)^2(ABA)ba(BAB)"),
    ("yin-yang II a", 0.41682, 0.33033, 55.7898, "(abaBAB)^3(abaBAbab)(ABAbab)^3(AB)^2"),
    ("yin-yang II b", 0.41734, 0.31310, 54.2076, "(abaBAB)^3(abaBAbab)(ABAbab)^3(AB)^2"),
]


def rows(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for row in txt.split("<tr>")[1:]:
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, flags=re.S)
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c).replace("&nbsp;", " ")).strip() for c in cells]
        if cells: out.append(cells)
    return out


def label(c):
    m = re.search(r"\(([\d.]+)\)\s*$", c)
    m3 = float(m.group(1)) if m else 1.0
    c = re.sub(r"\(([\d.]+)\)\s*$", "", c).strip()
    return re.sub(r"\s+", " ", c), m3


def load(pic, word, tag, src):
    P = rows(pic); W = rows(word)
    words = {}
    for c in W:
        if len(c) >= 2 and re.fullmatch(r"[abAB]+", c[1].replace(" ", "")): words[c[0]] = c[1].replace(" ", "")
    ent = []
    for c in P:
        try: vx, vy, T, Ts = float(c[1]), float(c[2]), float(c[3]), float(c[4])
        except (ValueError, IndexError): continue
        name, m3 = label(c[0])
        ent.append({"name": "%s %s%s" % (tag, name, "" if m3 == 1.0 else " (m3=%g)" % m3), "vx": vx, "vy": vy, "T": T, "m3": m3,
                    "Tstar_published": Ts, "word_published": words.get(c[0]), "source": src})
    return ent


def _work(arg):
    ii, vx, vy, T, m3 = arg
    tol = float(os.environ.get("RTOL", "1e-12"))
    r = V.integrate(vx, vy, T, m3, tol, tol, events=True)
    out = []
    for q in range(len(ii)):
        seq = r["seqs"][q]
        ok = (not r["failed"][q]) and r["err"][q] < 1e-2 and len(V.reduce_cyclic(seq)) % 2 == 0
        out.append({"Tstar": float(T[q] * abs(V.energy(vx[q], vy[q], m3[q])) ** 1.5),
                    "return_error": None if not np.isfinite(r["err"][q]) else float(r["err"][q]),
                    "canon": V.canonical_word(seq) if ok else None, "free_group_word_ours": V.free_group_word(seq) if ok else None})
    return ii, out


def main():
    d = sys.argv[1]
    ent = [{"name": "SD2013 " + n, "vx": vx, "vy": vy, "T": T, "m3": 1.0, "word_published": w,
            "source": "Suvakov & Dmitrasinovic, Phys. Rev. Lett. 110, 114301 (2013), Table I; arXiv:1303.0181"} for n, vx, vy, T, w in SD2013]
    ent += load(os.path.join(d, "three-body-pictures.md"), os.path.join(d, "three-body-free-group-word.md"), "LL2017",
                "Li & Liao, Sci. China-Phys. Mech. Astron. 60, 129511 (2017); arXiv:1705.00527; data: github.com/sjtu-liao/three-body")
    ent += load(os.path.join(d, "three-body-unequal-mass-pictures.md"), os.path.join(d, "three-body-unequal-mass-free-group-word.md"), "LL2018",
                "Li, Jing & Liao, Publ. Astron. Soc. Japan 70, 64 (2018); arXiv:1709.04775; data: github.com/sjtu-liao/three-body")
    print(len(ent), "entries", flush=True)
    vx, vy, T, m3 = (np.array([e[k] for e in ent]) for k in ("vx", "vy", "T", "m3"))
    t0 = time.time()
    order = np.argsort(T); CH = 40
    chunks = [order[s:s + CH] for s in range(0, len(ent), CH)]
    from multiprocessing import Pool
    with Pool(int(os.environ.get("NPROC", "8"))) as pool:
        for k, (ii, res) in enumerate(pool.imap_unordered(_work, [(ii, vx[ii], vy[ii], T[ii], m3[ii]) for ii in chunks[::-1]])):
            for i, r in zip(ii, res): ent[i].update(r)
            print("chunk", k, "/", len(chunks), "t=%.0fs" % (time.time() - t0), flush=True)
    n_ok = sum(e["canon"] is not None for e in ent)
    cat = {"description": "Known periodic planar three-body orbits with zero angular momentum and isosceles collinear initial "
           "configuration r1=(-1,0), r2=(1,0), r3=(0,0), v1=v2=(vx,vy), v3=-2(vx,vy)/m3, G=1, m1=m2=1. 'canon' is our canonical "
           "reduced syzygy word computed by integrating the published initial condition with verifier.integrate (None when the "
           "published 10-digit initial condition does not return to within 1e-2 in float64).",
           "sources": sorted({e["source"] for e in ent}),
           "not_included": ["Hristov, Hristova, Puzynin, Puzynina, Sharipov, Tukhliev 2021-2024 (arXiv:2111.10839, 2203.02793, 2308.16159; >12,000 equal-mass orbits, db2.fmi.uni-sofia.bg/3body)",
                            "Li, Li & Liao 2021 (135,445 unequal-mass orbits, non-hierarchical-3b-supplementary_data.txt)",
                            "Dmitrasinovic, Hudomal, Shibayama, Sugita 2018 (J. Phys. A 51, 315101; ~200 orbits) and Jankovic & Dmitrasinovic 2016",
                            "Li & Liao free-fall (2019) and 3D (2025) catalogs (different initial configurations)",
                            "orbits with nonzero angular momentum (Broucke, Henon, Hadjidemetriou families)"],
           "n_entries": len(ent), "n_with_word": n_ok, "distinct_words": len({e["canon"] for e in ent if e["canon"]}),
           "entries": ent}
    json.dump(cat, open(os.path.join(V.HERE, "catalog.json"), "w"), indent=0)
    print("wrote catalog.json", len(ent), "entries,", n_ok, "with word,", cat["distinct_words"], "distinct words")


if __name__ == "__main__":
    main()
