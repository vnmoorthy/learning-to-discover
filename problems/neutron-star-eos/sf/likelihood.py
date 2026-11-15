"""Multimessenger likelihoods for EOS inference. Inputs come from data/observations.json (provenance there).

Units: masses in M_sun, radii in km, Lambda dimensionless.

1. Radio mass measurement (PSR J0348+0432, Antoniadis et al. 2013): the pulsar exists, so the EOS must support
   its mass. With a Gaussian mass measurement N(mu, sigma) and a step-function "exists if M <= M_max",
       L = P(M_true <= M_max) = Phi((M_max - mu) / sigma).
2. NICER (J0030+0451, J0740+6620): APPROXIMATION - each published posterior is replaced by a product of two
   independent split-normal densities in M and R (median as location, 16%/84% offsets as the two widths), i.e.
   the M-R correlation ("banana") of the real posterior is ignored, and the analyses' own priors are treated as
   flat. The two analyses of the SAME data (Riley et al., Miller et al.) are NOT multiplied (that would double
   count the same photons); we use an equal-weight mixture 0.5 p_Riley + 0.5 p_Miller, which represents
   systematic (pipeline) uncertainty as model averaging. The EOS predicts R(M) on the stable branch; with a
   population prior on the star's mass uniform on [M_LO, M_max],
       L = int_{M_LO}^{M_max} p(M, R(M)) dM / (M_max - M_LO).
   The J0740 NICER posteriors already used the radio-timing mass (Fonseca et al. 2021) as an informative prior,
   so the Fonseca mass is NOT multiplied in again (no double counting); it enters through the NICER term.
3. GW170817 (LIGO/Virgo 2018, PRL 121 161101): Lambda_1.4 = 190 (+390, -120), 90% credible, common-EOS analysis.
   APPROXIMATION: split-normal in ln Lambda_1.4 with sigma_minus = ln(190/70)/1.645 and
   sigma_plus = ln(580/190)/1.645 (90% bounds mapped to +-1.645 sigma). The published posterior includes the
   LVC prior; treating it as a likelihood is an approximation.
"""
import json
import math
import os

import numpy as np
from scipy.special import ndtr

M_LO = 1.0
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_observations(path=None):
    with open(path or os.path.join(HERE, "data", "observations.json")) as f:
        return json.load(f)


def split_normal_logpdf(x, mu, s_minus, s_plus):
    x = np.asarray(x, float)
    s = np.where(x < mu, s_minus, s_plus)
    return math.log(2.0 / (math.sqrt(2 * math.pi) * (s_minus + s_plus))) - 0.5 * ((x - mu) / s) ** 2


def log_mass_likelihood(M_max, mu, sigma):
    return float(np.log(max(ndtr((M_max - mu) / sigma), 1e-300)))


def nicer_mixture_pdf(M, R, analyses):
    """analyses: list of dicts with M, M_minus, M_plus, R, R_minus, R_plus; equal-weight mixture."""
    tot = 0.0
    for a in analyses:
        tot = tot + np.exp(split_normal_logpdf(M, a["M"], a["M_minus"], a["M_plus"])
                           + split_normal_logpdf(R, a["R"], a["R_minus"], a["R_plus"]))
    return tot / len(analyses)


def log_nicer_likelihood(curve, analyses, ngrid=300):
    Ms, Rs = curve["M"], curve["R"]
    M_max = curve["M_max"]
    lo = max(M_LO, float(Ms[0]))
    if M_max <= lo:
        return -np.inf
    mg = np.linspace(lo, min(M_max, float(Ms[-1])), ngrid)
    rg = np.interp(mg, Ms, Rs)
    val = np.trapezoid(nicer_mixture_pdf(mg, rg, analyses), mg) / (M_max - M_LO)
    return float(np.log(max(val, 1e-300)))


def lambda_at(curve, M_target):
    if curve["M_max"] < M_target or curve["M"][0] > M_target:
        return np.nan
    return float(np.exp(np.interp(M_target, curve["M"], np.log(curve["Lambda"]))))


def radius_at(curve, M_target):
    if curve["M_max"] < M_target or curve["M"][0] > M_target:
        return np.nan
    return float(np.interp(M_target, curve["M"], curve["R"]))


def log_gw_likelihood(Lam14, med=190.0, lo90=70.0, hi90=580.0):
    if not np.isfinite(Lam14) or Lam14 <= 0:
        return -np.inf
    sm, sp = math.log(med / lo90) / 1.645, math.log(hi90 / med) / 1.645
    return float(split_normal_logpdf(math.log(Lam14), math.log(med), sm, sp))


def total_log_likelihood(curve, obs):
    """Returns (logL, parts dict)."""
    parts = {}
    j0348 = obs["constraints"]["J0348_mass"]
    parts["J0348_mass"] = log_mass_likelihood(curve["M_max"], j0348["value"], j0348["sigma"])
    for key in ("J0030_nicer", "J0740_nicer"):
        parts[key] = log_nicer_likelihood(curve, obs["constraints"][key]["analyses"])
    parts["GW170817_Lambda14"] = log_gw_likelihood(lambda_at(curve, 1.4))
    return float(sum(parts.values())), parts
