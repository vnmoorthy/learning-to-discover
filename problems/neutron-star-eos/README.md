# STARFORGE: reproduce

All commands run from this directory. Use Python 3 with numpy, scipy, matplotlib and emcee; see `requirements.txt`.

```bash
/opt/anaconda3/bin/python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q tests                # 21 tests, ~12 s
.venv/bin/python sweep_reference.py                # reference EOS M-R, figures/*_reference.png, results/core.json
.venv/bin/python verify/run_verification.py        # independent solver -> results/verification.json (~30 s)
.venv/bin/python studies/sound_speed.py && .venv/bin/python studies/plot_sound_speed.py   # cs2 requirement (~7 min)
.venv/bin/python phase_sweep.py && .venv/bin/python twins.py      # 220-EOS transition grid + twins (~7 min, 6 procs)
.venv/bin/python run_inference.py && .venv/bin/python analyze_inference.py   # MCMC (unconverged in our run)
```

## Layout

- `sf/` is the validated core:
  - `units.py`: unit conversions
  - `eos.py`: piecewise polytrope, sound-speed and CSS hybrid EOSs
  - `tov.py`: TOV, Love number and jump condition
  - fast solvers: `fasttov.py`, `fastcss.py`
  - `likelihood.py`: observation likelihoods
- `verify/independent.py` is a second TOV and Love-number implementation that does not import `sf.tov` or `sf.eos`.
- `data/observations.json` holds the observational constraints with their provenance.
- `results/` holds cached JSON:
  - `dashboard.json` and `research_log.json`: the judge-facing summary
  - `verification.json`: the independent-solver comparison
- `figures/` holds the PNG figures (dark theme, every axis labelled with units).
- `paper/starforge.md` is the full write-up.

## Units

Internally G = c = 1 with lengths in km. 1 MeV/fm^3 = 1.32383e-6 km^-2 and M_sun = 1.4766250 km.
