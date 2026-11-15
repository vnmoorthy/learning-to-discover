"""Compare sf/tov.py (core) against verify/independent.py at identical central pressures.
Novelty level 1 (code verification). Writes results/verification.json."""
import json
import math
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "verify"))
import independent as I  # noqa: E402
from sf import eos as E, tov as T, units as u, models  # noqa: E402

FLAG = 5e-3
P_SURF_CORE = 1e-16   # core default surface pressure, km^-2


def configs():
    """pc at M_max taken from results/core.json (core max_mass); pc at 1.4 M_sun from core star_of_mass."""
    core_json = json.load(open(os.path.join(ROOT, "results", "core.json")))["eos"]
    sly, apr, h4 = (E.reference_eos(n) for n in ("SLy", "APR4", "H4"))
    css = models.example_css()
    lo, hi = float(u.mevfm3_to_geo(10.0)), float(u.mevfm3_to_geo(400.0))
    out = []
    for name, core_eos, ind_eos in [("SLy", sly, I.PPh("SLy")), ("APR4", apr, I.PPh("APR4")),
                                    ("H4", h4, I.PPh("H4"))]:
        s14 = T.star_of_mass(core_eos, 1.4, lo, hi)
        out.append((f"{name} @ 1.4 M_sun", core_eos, ind_eos, s14["pc"]))
        if name == "SLy":
            out.append(("SLy @ M_max", core_eos, ind_eos,
                        float(u.mevfm3_to_geo(core_json["SLy"]["pc_at_Mmax_MeV_fm3"]))))
    css_ind = I.CSSh(I.PPh("SLy"), 80.0, 250.0, 1.0)
    out.append(("SLy+CSS (p_t=80, d_eps=250 MeV/fm^3, cs2_q=1) @ pc=150 MeV/fm^3", css, css_ind,
                float(u.mevfm3_to_geo(150.0))))
    out.append(("SLy+CSS @ M_max (pc from core.json)", css, css_ind,
                float(u.mevfm3_to_geo(core_json["CSS"]["pc_at_Mmax_MeV_fm3"]))))
    return out


def main():
    t0 = time.time()
    rows = []
    for label, ce, ie, pc in configs():
        core = T.solve_star(ce, pc)
        a = I.solve(ie, pc, n_seg=400, p_surf=P_SURF_CORE)
        b = I.solve(ie, pc, n_seg=800, p_surf=P_SURF_CORE)
        z = I.solve(ie, pc, n_seg=800, p_surf=0.0)
        row = dict(config=label, pc_MeVfm3=float(u.geo_to_mevfm3(pc)),
                   core=dict(M=core["M"], R=core["R"], Lambda=core["Lambda"], k2=core["k2"],
                             r_transition=core["r_transition"]),
                   independent=dict(M=b["M"], R=b["R"], Lambda=b["Lambda"], k2=b["k2"],
                                    r_transition=b["r_transition"]),
                   independent_to_P0=dict(M=z["M"], R=z["R"], Lambda=z["Lambda"]))
        rel, conv, surf = {}, {}, {}
        for k in ("M", "R", "Lambda"):
            rel[k] = b[k] / core[k] - 1
            conv[k] = b[k] / a[k] - 1          # independent self-convergence (n=800 vs 400)
            surf[k] = z[k] / b[k] - 1          # effect of truncating at P = 1e-16 km^-2 vs P = 0
        row.update(rel_diff_ind_minus_core=rel, ind_self_convergence_800_vs_400=conv,
                   surface_truncation_effect=surf,
                   flag_gt_0p5pct=bool(max(abs(v) for v in rel.values()) > FLAG))
        rows.append(row)
        print(label, {k: f"{v:+.2e}" for k, v in rel.items()}, "surf", {k: f"{v:+.1e}" for k, v in surf.items()},
              flush=True)
    # independent check that the core M_max pc is a maximum of the independent M(pc) (+-2% in pc)
    row_max = [r for r in rows if r["config"] == "SLy @ M_max"][0]
    pcm = float(u.mevfm3_to_geo(row_max["pc_MeVfm3"]))
    Mm = [I.solve(I.PPh("SLy"), pcm * f, n_seg=800, p_surf=P_SURF_CORE)["M"] for f in (0.98, 1.0, 1.02)]
    res = dict(
        meta=dict(novelty_level=1, novelty_note="code verification (reproduction), not a discovery",
                  comparison="identical central pressure; independent solver truncated at the same surface "
                             "pressure 1e-16 km^-2 as the core (P=0 variant also reported)",
                  core="sf.tov.solve_star defaults (DOP853, rtol 1e-10, atol 1e-14, y-Riccati, r independent)",
                  independent="verify/independent.py: enthalpy formulation, s = sqrt(h_c - h), fixed-step RK4, "
                              "second-order H equation, own EOS in closed form of h, own constants",
                  flag_threshold=FLAG, units=dict(M="M_sun", R="km", pc="MeV/fm^3", Lambda="dimensionless"),
                  wall_time_s=None),
        rows=rows,
        sly_Mmax_independent_bracket=dict(pc_factors=[0.98, 1.0, 1.02], M_independent=Mm,
                                          is_local_max=bool(Mm[1] > Mm[0] and Mm[1] > Mm[2])),
        n_flagged=sum(r["flag_gt_0p5pct"] for r in rows))
    res["meta"]["wall_time_s"] = time.time() - t0
    with open(os.path.join(ROOT, "results", "verification.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print("Mmax bracket", res["sly_Mmax_independent_bracket"])
    print("wall", res["meta"]["wall_time_s"])


if __name__ == "__main__":
    main()
