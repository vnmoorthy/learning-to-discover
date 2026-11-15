"""STARFORGE physics core: units, EOS models, TOV + tidal deformability.

Conventions: geometrized units G = c = 1 with lengths in km. Pressure P and
energy density eps are in km^-2, masses in km internally (reported in M_sun),
baryon number density n in fm^-3. See sf/units.py for conversion constants.
"""
from . import units, eos, tov  # noqa: F401
