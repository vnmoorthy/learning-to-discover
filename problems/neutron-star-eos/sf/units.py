"""Physical constants and unit conversions (CODATA 2018 / IAU 2015 nominal).

Internal convention: geometrized units G = c = 1, lengths in km.
  * energy density eps and pressure P : km^-2
  * mass density rho (rest mass)       : km^-2  (rho_geo = G/c^2 * rho_cgs * (1e5 cm/km)^2)
  * mass M                             : km     (M_geo = G M / c^2), reported in M_sun
  * baryon number density n            : fm^-3
  * chemical potential mu              : MeV
"""
import numpy as np

G_CGS = 6.67430e-8            # cm^3 g^-1 s^-2
C_CGS = 2.99792458e10         # cm s^-1
GM_SUN_CGS = 1.3271244e26     # cm^3 s^-2 (IAU 2015 nominal solar mass parameter)
M_SUN_G = GM_SUN_CGS / G_CGS  # g
MEV_ERG = 1.602176634e-6      # erg
FM_CM = 1.0e-13               # cm
KM_CM = 1.0e5                 # cm
M_U_G = 1.66053906660e-24     # g, atomic mass unit (baryon mass used for n = rho / m_u)
N_SAT = 0.16                  # fm^-3, nuclear saturation density (convention)

M_SUN_KM = GM_SUN_CGS / C_CGS**2 / KM_CM            # 1.4766250 km
GEO_PER_GCM3 = G_CGS / C_CGS**2 * KM_CM**2          # (g/cm^3) -> km^-2
GEO_PER_DYNCM2 = G_CGS / C_CGS**4 * KM_CM**2        # (dyn/cm^2 = erg/cm^3) -> km^-2
ERGCM3_PER_MEVFM3 = MEV_ERG / FM_CM**3              # 1.602176634e33
GEO_PER_MEVFM3 = ERGCM3_PER_MEVFM3 * GEO_PER_DYNCM2  # ~1.3234e-6 km^-2 per MeV/fm^3
# rest-mass density (km^-2) -> baryon number density (fm^-3)
FM3_PER_GEO_RHO = 1.0 / (GEO_PER_GCM3 * M_U_G) * FM_CM**3


def mevfm3_to_geo(x):
    return np.asarray(x) * GEO_PER_MEVFM3


def geo_to_mevfm3(x):
    return np.asarray(x) / GEO_PER_MEVFM3


def gcm3_to_geo(x):
    return np.asarray(x) * GEO_PER_GCM3


def geo_to_gcm3(x):
    return np.asarray(x) / GEO_PER_GCM3


def dyncm2_to_geo(x):
    return np.asarray(x) * GEO_PER_DYNCM2


def geo_to_dyncm2(x):
    return np.asarray(x) / GEO_PER_DYNCM2


def msun_to_km(m):
    return np.asarray(m) * M_SUN_KM


def km_to_msun(m):
    return np.asarray(m) / M_SUN_KM


def rho_geo_to_n_fm3(rho):
    """Rest-mass density (km^-2) -> baryon number density n = rho/m_u (fm^-3)."""
    return np.asarray(rho) * FM3_PER_GEO_RHO


def n_fm3_to_rho_geo(n):
    return np.asarray(n) / FM3_PER_GEO_RHO
