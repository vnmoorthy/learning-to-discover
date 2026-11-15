"""Multimessenger EOS inference runner (emcee). One process per (model, prior) chain or evidence job.

Usage: .venv/bin/python run_inference.py mcmc PP A <deadline_epoch>
       .venv/bin/python run_inference.py evidence CS A <deadline_epoch>
Models (G = c = 1, km; see sf/units.py):
  PP : Read et al. 2009 piecewise polytrope, theta = (log10 p1 [dyn/cm^2] at rho1 = 10^14.7 g/cm^3, G1, G2, G3),
       SLy crust. Bounds: log10 p1 in [33.9, 35.0], G_i in [1.4, 5.0].
       Prior A: uniform in theta.  Prior B: uniform in log10 p1 and in ln(G_i - 1) (favours softer pieces).
  CS : sound-speed model, SLy below n_match = 1.1 n_sat, c_s^2 piecewise linear in n with nodes at
       n = 2, 3, 5, 8 n_sat (constant beyond 8 n_sat up to n = 2 fm^-3). theta = c_s^2 at the 4 nodes.
       Prior A: uniform in [0.01, 1].  Prior B: log-uniform in [0.01, 1] (favours soft matter).
Both priors are truncated by: valid EOS construction, causality c_s^2 <= 1 up to the centre of the
maximum-mass star, and a TOV maximum found below pc = 3000 MeV/fm^3.
Results (chains + blobs) are cached in results/chain_<model>_<prior>.npz and results/evidence_<model>.npz.
"""
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.modules.setdefault("h5py", None)  # anaconda's h5py is ABI-broken vs numpy 2.5; emcee's HDF backend is optional
import numpy as np
import emcee

from sf import eos as E, units as u, fasttov as F, likelihood as LK

HERE = os.path.dirname(os.path.abspath(__file__))
OBS = LK.load_observations()
M_GRID = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2])
NBLOB = 3 + len(M_GRID)
SLY = E.reference_eos("SLy")
NS = u.N_SAT

BOUNDS = {"PP": np.array([[33.9, 35.0], [1.4, 5.0], [1.4, 5.0], [1.4, 5.0]]),
          "CS": np.array([[0.01, 1.0]] * 4)}
INIT = {"PP": (np.array([34.384, 3.005, 2.988, 2.851]), np.array([0.03, 0.15, 0.15, 0.15])),
        "CS": (np.array([0.45, 0.70, 0.45, 0.36]), np.array([0.05, 0.05, 0.05, 0.05]))}
LABELS = {"PP": ["log10 p1 [dyn/cm^2]", "Gamma1", "Gamma2", "Gamma3"],
          "CS": ["c_s^2(2 n_sat)", "c_s^2(3 n_sat)", "c_s^2(5 n_sat)", "c_s^2(8 n_sat)"]}


def build(model, th):
    if model == "PP":
        return E.read_pp(*th)
    return E.SpeedOfSoundEOS(SLY, 1.1 * NS, [2 * NS, 3 * NS, 5 * NS, 8 * NS], list(th), num=4001)


def log_prior(model, prior, th):
    b = BOUNDS[model]
    if np.any(th < b[:, 0]) or np.any(th > b[:, 1]):
        return -np.inf
    if prior == "A":
        return 0.0
    if model == "PP":
        return float(-np.sum(np.log(th[1:] - 1.0)))
    return float(-np.sum(np.log(th)))


def evaluate(model, th):
    """Returns (logL, blob) or (-inf, nan blob) if outside the truncated prior support."""
    blob = np.full(NBLOB, np.nan)
    try:
        eos = build(model, th)
        c = F.mr_curve(eos, num=18, nstep=160)
    except Exception:
        return -np.inf, blob
    if c["edge"] or c["cs2_max_to_center"] > 1.0 or not np.isfinite(c["M_max"]):
        return -np.inf, blob
    ll, _ = LK.total_log_likelihood(c, OBS)
    blob[0], blob[1], blob[2] = c["M_max"], LK.radius_at(c, 1.4), LK.lambda_at(c, 1.4)
    blob[3:] = [LK.radius_at(c, m) for m in M_GRID]
    return ll, blob


def log_prob(th, model, prior):
    lp = log_prior(model, prior, th)
    if not np.isfinite(lp):
        return -np.inf, np.full(NBLOB, np.nan)
    ll, blob = evaluate(model, th)
    return (lp + ll if np.isfinite(ll) else -np.inf), blob


def run_mcmc(model, prior, deadline, nwalk=10, seed=1):
    rng = np.random.default_rng(seed + (0 if model == "PP" else 10) + (0 if prior == "A" else 100))
    mu, sd = INIT[model]
    b = BOUNDS[model]
    p0 = []
    while len(p0) < nwalk:
        th = np.clip(mu + sd * rng.standard_normal(4), b[:, 0] + 1e-6, b[:, 1] - 1e-6)
        if np.isfinite(log_prob(th, model, prior)[0]):
            p0.append(th)
    s = emcee.EnsembleSampler(nwalk, 4, log_prob, args=(model, prior))
    out = os.path.join(HERE, "results", f"chain_{model}_{prior}.npz")
    t0 = time.time()
    for i, _ in enumerate(s.sample(np.array(p0), iterations=100000)):
        if time.time() > deadline:
            break
        if i % 5 == 0:
            np.savez(out, chain=s.get_chain(), lnp=s.get_log_prob(), blobs=s.get_blobs(),
                     acc=s.acceptance_fraction, wall=time.time() - t0)
    np.savez(out, chain=s.get_chain(), lnp=s.get_log_prob(), blobs=s.get_blobs(),
             acc=s.acceptance_fraction, wall=time.time() - t0)


def run_evidence(model, deadline, seed=7):
    """Prior Monte Carlo (prior A): Z = E_prior[L] over draws inside the truncated support.
    Unbiased for the truncated-prior evidence; its error is estimated by bootstrap."""
    rng = np.random.default_rng(seed + (0 if model == "PP" else 1))
    b = BOUNDS[model]
    lls, nsupport, ndraw = [], 0, 0
    out = os.path.join(HERE, "results", f"evidence_{model}.npz")
    while time.time() < deadline:
        th = b[:, 0] + (b[:, 1] - b[:, 0]) * rng.random(4)
        ndraw += 1
        ll, _ = evaluate(model, th)
        if ll == -np.inf and not np.isfinite(_[0]):
            continue  # outside truncated support
        nsupport += 1
        lls.append(ll)
        if nsupport % 10 == 0:
            np.savez(out, lls=np.array(lls), nsupport=nsupport, ndraw=ndraw)
    np.savez(out, lls=np.array(lls), nsupport=nsupport, ndraw=ndraw)


if __name__ == "__main__":
    mode, model = sys.argv[1], sys.argv[2]
    if mode == "mcmc":
        run_mcmc(model, sys.argv[3], float(sys.argv[4]))
    else:
        run_evidence(model, float(sys.argv[3]))
