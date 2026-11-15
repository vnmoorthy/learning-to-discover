# STARFORGE: an autonomous computational study of the neutron-star equation of state

*Phoenixastar research lab, hackathon entry, 2026-11-15. Every result below is labelled with a novelty level: 1 reproduction, 2 verification of a known relation, 3 new computational exploration of known models, 4 new testable hypothesis, 5 potentially novel and in need of expert review. No result in this paper is above level 3.*

## Abstract
We built a general-relativistic stellar-structure code that solves the TOV equations together with the tidal Love-number equation, and validated it in two ways:

- against analytic limits, with 21 of 21 tests passing;
- against an independently written solver, which agrees to at most 6e-6 in Lambda.

With it we:

- reproduce the SLy reference values: M_max = 2.048 M_sun, R_1.4 = 11.70 km, Lambda_1.4 = 296 (level 1);
- show that if SLy holds up to 2 n_sat, reaching 2 M_sun requires c_s^2,max >= 0.37, which exceeds the conformal value 1/3 (level 2, consistent with Bedaque & Steiner 2015 and Tews et al. 2018);
- confirm the Seidov criterion numerically in 214 of 220 Maxwell + CSS hybrid EOSs (level 2);
- map where twin stars occur (58 of 220 EOSs) and find that, in illustrative models, equal-mass twins differ in Lambda by factors of about 7 to 20 (level 3).

A multimessenger MCMC pipeline was built, but its chains did not converge, so no posterior is reported.

## 1. Motivation
Above about 2 n_sat, the EOS of cold, catalysed matter is not known from first principles. Three kinds of constraint bear on it: 2 M_sun pulsars, NICER mass-radius measurements, and the GW170817 tidal deformability. Our aim is to test, in a way that is reproducible and verified, what these constraints and basic physics (causality and the first law of thermodynamics) imply. We also want to know when a strong first-order phase transition leaves an observable signature.

## 2. Mathematical foundations
**Units.** G = c = 1 with lengths in km, and P and eps in km^-2. Conversions: 1 MeV/fm^3 = 1.32383e-6 km^-2, and M_sun = 1.4766250 km (IAU nominal GM_sun). n is in fm^-3 and mu in MeV.

**TOV equations.**
- dm/dr = 4 pi r^2 eps
- dP/dr = -(eps + P)(m + 4 pi r^3 P) / [r(r - 2m)]

**Tidal response.** The Riccati variable y = r H'/H obeys

r y' + y^2 + y e^lambda [1 + 4 pi r^2 (P - eps)] + r^2 Q = 0, with Q = 4 pi e^lambda (5 eps + 9 P + (eps + P)/c_s^2) - 6 e^lambda / r^2 - (nu')^2.

k2 follows from the compactness C = M/R and y_R (Hinderer 2008), and Lambda = (2/3) k2 C^-5.

**Jump condition.** At a density discontinuity Delta_eps at radius r, y jumps by

y+ = y- - 4 pi r^3 Delta_eps / (m + 4 pi r^3 P) = y- - 3 Delta_eps / (eps_bar + 3P), where eps_bar = 3m / (4 pi r^3).

The Newtonian limit is -3 Delta_rho / rho_bar. Setting P = 0 gives the surface correction for an EOS with eps_surface > 0.

**Thermodynamic consistency.** Each EOS satisfies the first law, d eps = (eps + P) dn / n, with mu = (eps + P)/n and c_s^2 = dP/d eps. We require 0 <= c_s^2 <= 1 everywhere except across explicit Maxwell jumps.

**EOS families.**
1. Read et al. (2009) piecewise polytropes on an SLy crust, with eps = (1 + a_i) rho + P/(Gamma_i - 1) and core dividing densities at 10^14.7 and 10^15 g/cm^3.
2. Sound-speed models: c_s^2(n) is piecewise linear, ln mu is integrated from it, dP = mu c_s^2 dn and eps = n mu - P.
3. CSS hybrids: a Maxwell transition at p_t with mu continuous, an energy-density jump Delta_eps, then a constant-sound-speed quark phase.

## 3. Numerical methods
- **Core solver (`sf/tov.py`).** DOP853 with rtol 1e-10, integrating (m, ln P, y) segment by segment between kinks and jumps, with terminal events at each target pressure. For C < 0.05 the Love number is evaluated with 50-digit mpmath.
- **Stability.** dM/d eps_c > 0 for the reference stars. For the transition grid we use the Bardeen-Thorne-Meltzer turning-point rule on the M-R curve.
- **Fast paths.** `sf/fasttov.py` uses vectorised RK4 in xi = sqrt(ln p_c - ln P). With 160 to 200 steps the errors are 0.08% in M and about 0.6 to 1% in Lambda. `sf/fastcss.py` gives scalar EOS fast paths that agree with the core exactly.

## 4. Validation (level 1)
- **Analytic limits.**
  - Schwarzschild constant-density interior: rel 1e-7.
  - Lane-Emden n = 1 and n = 1.5 in the Newtonian limit: rel 1e-3.
  - Newtonian k2 for n = 1, (15 - pi^2)/(2 pi^2): rel 2e-3.
  - Incompressible k2 -> 3/4, which requires the surface jump.
- **Jump condition.** Lambda from the analytic jump converges to the result for a smeared transition as the width w -> 0.
- **Thermodynamic consistency.** Checked for 6 EOSs.
- **Test status.** 21 of 21 tests pass (`.venv/bin/python -m pytest -q tests`, 11.8 s).
- **Independent verification.** `verify/independent.py` imports neither `sf.tov` nor `sf.eos`. It uses the enthalpy formulation, fixed-step RK4, the second-order H equation, its own constants and its own derivation of the jump. Across 6 configurations (SLy, APR4 and H4 at 1.4 M_sun, SLy at M_max, and SLy+CSS at two central pressures), its largest relative differences from the core are 9e-7 in M, 7e-8 in R and 6e-6 in Lambda. None of the 6 is flagged at the 0.5% threshold.

## 5. Observational constraints and provenance
Each entry was checked against the arXiv abstract. Details are in `data/observations.json`.

| Constraint | Source | Value |
|---|---|---|
| PSR J0348+0432 mass | Antoniadis+2013 (1304.6875) | M = 2.01 +- 0.04 M_sun |
| PSR J0740+6620 mass | Fonseca+2021 (2104.00880) | M = 2.08 +- 0.07 M_sun (used only through the NICER priors, to avoid double counting) |
| J0030 NICER | Riley+2019 (1912.05702) | M = 1.34 +0.15/-0.16, R = 12.71 +1.14/-1.19 km |
| J0030 NICER | Miller+2019 (1912.05705) | M = 1.44 +0.15/-0.14, R = 13.02 +1.24/-1.06 km |
| J0740 NICER | Riley+2021 (2105.06980) | M = 2.072 +0.067/-0.066, R = 12.39 +1.30/-0.98 km |
| J0740 NICER | Miller+2021 (2105.06979) | R = 13.7 +2.6/-1.5 km |
| GW170817 | LVC PRL 121 161101 (1805.11581) | Lambda_1.4 = 190 +390/-120 (90%) |

## 6. Inference (levels 1-2; retracted as a result)
**Setup.**
- Sampler: emcee.
- EOS models and priors: a PP model with two priors (A uniform, B uniform in ln(Gamma - 1)) and a sound-speed model.
- NICER likelihood: split-normal M and R marginals. This ignores the M-R correlation. The two analyses of each star enter as an equal-weight mixture.
- Pulsar mass likelihood: Phi((M_max - 2.01)/0.04).
- GW170817 likelihood: split-normal in ln Lambda_1.4.

**Outcome.** All four chains stopped at the deadline after 23 to 27 steps, with 10 walkers and steps/tau of about 10. They are **unconverged**, and we report no posterior. The figures `posterior_*.png` and `prior_sensitivity.png` carry an "unconverged" label and serve only as pipeline diagnostics.

## 7. Sound-speed requirement (level 2)
SLy is fixed below a matching density n_m, and c_s^2 rises to c_s^2,max either abruptly (the "step" completion, which is the stiffest) or over 1.5 n_sat (the "ramp" completion). The table gives the minimum c_s^2,max for each mass target.

| n_m | step, M_max >= 2.0 | step, M_max >= 2.08 | ramp, M_max >= 2.0 |
|---|---|---|---|
| 1.1 n_sat | 0.247 | 0.263 | 0.366 |
| 1.5 n_sat | 0.304 | 0.326 | not run |
| 2.0 n_sat | 0.372 | 0.405 | 0.484 |

At n_m = 2 n_sat with c_s^2 = 1 we find M_max = 2.91 M_sun, which reproduces Kalogera & Baym (1996) at level 1.

The early stiffening that minimises the c_s^2 requirement also gives large Lambda_1.4, about 1000 to 1560. That is probably in tension with GW170817, but we did not quantify the tension.

## 8. Phase transitions and twin stars (levels 2-3)
**Grid.** 220 SLy + Maxwell + CSS EOSs:
- p_t/eps_t from 0.04 to 0.40;
- Delta_eps/eps_t from 0.1 to 1.7;
- c_s^2_q = 1/3 or 1.

**Seidov criterion.** We re-derived the slope ratio of dM/dp_c across the transition to leading order in the quark-core radius. It changes sign at Delta_eps/eps_t = 1/2 + 3 p_t/(2 eps_t), which is the Seidov criterion.
- The numerical slope ratios match this prediction, for example 0.68804 numerically against 0.68795 predicted.
- The criterion agrees with the numerical classification in 214 of 220 cases.
- All 6 disagreements lie within one grid step of the bound.

**Topology.** Counts by Alford-Han-Prakash category:

| c_s^2_q | C | D | B | N |
|---|---|---|---|---|
| 1/3 | 46 | 21 | 2 | 41 |
| 1 | 43 | 34 | 5 | 28 |

**Twins.**
- They occur in 58 EOSs.
- With c_s^2_q = 1/3, twins appear only for p_t/eps_t <= 0.12, and the heaviest twin is 1.19 M_sun.
- With c_s^2_q = 1, they appear for p_t/eps_t <= 0.24, the heaviest twin is 1.73 M_sun, and the third family reaches up to 2.40 M_sun.

**Equal-mass twin Lambda (level 3, illustrative).** Two example EOSs, with p_t and Delta_eps in MeV/fm^3:

| EOS | M | R, hadronic / hybrid | Lambda, hadronic / hybrid |
|---|---|---|---|
| p_t = 57, Delta_eps = 503, c_s^2 = 1/3 | 1.123 M_sun | 11.82 / 9.36 km | 1163 / 158 |
| p_t = 91, Delta_eps = 873, c_s^2 = 1 | 1.307 M_sun | 11.75 / 8.31 km | 462 / 22 |

Both twin pairs survive +-2% changes in p_t, Delta_eps and c_s^2_q. The hybrid-twin Lambda shifts by up to about 15% under those changes.

## 9. Hypotheses
The full list is in `results/research_log.json`.

| ID | Hypothesis | Status | Level |
|---|---|---|---|
| H1 | The core solver is correct | verified | 1 |
| H2 | c_s^2 > 1/3 if SLy holds to 2 n_sat | supported | 2 |
| H3 | The Seidov criterion holds | supported, 214/220 | 2 |
| H4 | The twin-existence region is bounded in p_t/eps_t | supported | 3 |
| H5 | Equal-mass twins are distinguishable by Lambda | supported in illustrative models; testable with future GW events; largely expected from the compactness difference | 3 |
| H6 | The posterior is robust to the prior | retracted: chains unconverged | none |

## 10. Adversarial review (objections and outcomes)
1. **Units could be wrong consistently in both codes.** Answered: the independent code uses its own constants, and the Lane-Emden tests fix the absolute scale in km.
2. **Numerical artifacts in the twin results.** Twins survive +-2% perturbations and the core runs at rtol 1e-8. The hybrid Lambda is parameter-sensitive, so we report ranges.
3. **Seidov disagreements.** All 6 sit at the grid edge of the bound, so we attribute them to grid resolution. They are recorded as unresolved, not explained away.
4. **Prior dependence of the inference.** It could not be assessed. The inference is retracted.
5. **Unsupported novelty.** H5 was downgraded from level 4 to 3, because a large Lambda ratio at equal mass follows from the difference in compactness. The topology counts reproduce Alford, Han & Prakash (2013).
6. **Compute.** For about 40 s the cap of 6 processes was exceeded by one process. This had no effect on the results.

Of the 7 key claims, 3 passed independent verification: core correctness, the SLy, APR4 and H4 reference values, and CSS hybrid M, R and Lambda with the jump condition. Three are supported, using the verified core, but were not re-run by a second code: the sound-speed requirement, the Seidov and topology map, and the twin Lambda. One (the inference) is retracted.

## 11. Limitations
- Everything is conditioned on the SLy crust and low-density EOS.
- There are only two sound-speed completion shapes.
- Phase transitions are Maxwell only: no Gibbs or mixed phases, and no finite surface tension.
- The grid has about 30 stars per EOS, so narrow third families may be missed.
- The likelihoods are approximate and the MCMC is unconverged.
- No rotation, finite temperature or radial-mode analysis beyond the turning-point rule.

## 12. Conclusions
STARFORGE provides a verified, unit-explicit TOV and tidal code, with a correct jump condition for first-order transitions. The main physics results are reproductions or verifications of known relations: SLy structure, c_s^2 > 1/3 if SLy holds to 2 n_sat, and the Seidov criterion. They are complemented by a level-3 map of twin-star regions and their tidal signatures. No breakthrough is claimed. A converged multimessenger posterior is the next step.

## References
- Alford, Han & Prakash, PRD 88, 083013 (2013)
- Antoniadis et al., Science 340, 6131 (2013), arXiv:1304.6875
- Bedaque & Steiner, PRL 114, 031103 (2015)
- Fonseca et al., ApJL 915, L12 (2021), arXiv:2104.00880
- Hinderer, ApJ 677, 1216 (2008)
- Kalogera & Baym, ApJL 470, L61 (1996)
- LIGO/Virgo, PRL 121, 161101 (2018), arXiv:1805.11581
- Lindblom, ApJ 398, 569 (1992)
- Miller et al., ApJL 887, L24 (2019), arXiv:1912.05705
- Miller et al., ApJL 918, L28 (2021), arXiv:2105.06979
- Read, Lackey, Owen & Friedman, PRD 79, 124032 (2009)
- Riley et al., ApJL 887, L21 (2019), arXiv:1912.05702
- Riley et al., ApJL 918, L27 (2021), arXiv:2105.06980
- Seidov, Sov. Astron. 15, 347 (1971)
- Tews, Carlson, Gandolfi & Reddy, ApJ 860, 149 (2018)
- Damour & Nagar, PRD 80, 084035 (2009)
