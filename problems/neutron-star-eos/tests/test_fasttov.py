"""Fast vectorised TOV (sf/fasttov.py) against the validated adaptive solver sf.tov.solve_star."""
import numpy as np
import pytest

from sf import eos as E, tov as T, units as u, fasttov as F


@pytest.mark.parametrize("name", ["SLy", "MPA1"])
@pytest.mark.parametrize("pc_mev", [60.0, 300.0])
def test_fasttov_matches_core(name, pc_mev):
    e = E.reference_eos(name)
    pc = u.mevfm3_to_geo(pc_mev)
    ref = T.solve_star(e, pc, rtol=1e-9, atol=1e-13)
    tab = F.EOSTable(e, p_hi=pc * 1.1)
    s = F.solve_many(tab, np.array([pc]), nstep=200)
    assert abs(s["M"][0] / ref["M"] - 1) < 2e-3
    assert abs(s["R"][0] - ref["R"]) < 0.02          # km
    assert abs(s["Lambda"][0] / ref["Lambda"] - 1) < 2e-2
