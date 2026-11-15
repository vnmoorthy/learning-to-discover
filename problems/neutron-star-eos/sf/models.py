"""Illustrative (non-reference) instances of the parameterised families. Not fits to data."""
from . import eos as E
from . import units as u


def example_cs(low=None):
    """c_s^2(n) with a peak (0.7 at 3 n_sat) relaxing toward ~1/3; matched to SLy at 1.1 n_sat."""
    low = low or E.reference_eos("SLy")
    ns = u.N_SAT
    return E.SpeedOfSoundEOS(low, 1.1 * ns, [2 * ns, 3 * ns, 5 * ns, 8 * ns], [0.45, 0.70, 0.45, 0.36],
                             name="CS-peak (illustrative)")


def example_css(had=None):
    """SLy + Maxwell transition at p_t = 80 MeV/fm^3, d_eps = 250 MeV/fm^3, c_s^2(quark) = 1."""
    had = had or E.reference_eos("SLy")
    return E.CSSHybridEOS.from_mevfm3(had, 80.0, 250.0, 1.0, name="SLy+CSS (illustrative)")
