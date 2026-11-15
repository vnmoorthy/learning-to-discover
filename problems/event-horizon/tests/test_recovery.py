"""Tests for eh/recovery.py (Petz decoder, decoupling, noise) and eh/otoc.py.
Run:  python -m pytest -q tests/test_recovery.py      (fixed seeds below)
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eh import recovery as rc  # noqa: E402
from eh import otoc as ot  # noqa: E402
from eh import hayden_preskill as hp  # noqa: E402
from eh.circuits import haar_unitary, brickwork_unitary  # noqa: E402

SEED = 20261115 + 777


def rng(o=0):
    return np.random.default_rng(SEED + o)


def rand_density(d, r):
    g = rng(r).standard_normal((d, d + r)) + 1j * rng(r + 50).standard_normal((d, d + r))
    x = g @ g.conj().T
    return x / np.trace(x).real


# ---------------------------------------------------------------- channels
@pytest.mark.parametrize("old", [True, False])
@pytest.mark.parametrize("m", [0, 1, 2, 3])
def test_hp_channel_trace_preserving(old, m):
    U = haar_unitary(8, rng(1))
    K = rc.hp_channel_kraus(U, 1, 2, m, old)
    assert rc.is_trace_preserving(K)


def test_depolarizing_kraus_tp_and_matches_superop():
    p = 0.37
    K = np.array(rc.depolarizing_kraus(p))
    assert rc.is_trace_preserving(K)
    rho = rand_density(2, 3)
    a = rc.apply_kraus(K, rho)
    b = rc.depolarize_qubits(rho, 1, [0], p)
    assert np.allclose(a, b, atol=1e-13)
    rho3 = rand_density(8, 4)
    out = rc.depolarize_qubits(rho3, 3, [0, 2], p)
    assert abs(np.trace(out) - 1) < 1e-13
    assert np.allclose(out, out.conj().T)
    assert np.linalg.eigvalsh(out).min() > -1e-13


@pytest.mark.parametrize("old", [True, False])
@pytest.mark.parametrize("m", [1, 2, 3])
def test_petz_composite_is_trace_preserving(old, m):
    U = haar_unitary(16, rng(2))
    K = rc.hp_channel_kraus(U, 1, 3, m, old)
    R = rc.petz_kraus(K)
    A = np.einsum("iax,jxb->ijab", R, K).reshape(-1, 2, 2)
    assert rc.is_trace_preserving(A, tol=1e-9)


# ---------------------------------------------------------------- Petz fidelity
@pytest.mark.parametrize("old", [True, False])
@pytest.mark.parametrize("k,nB", [(1, 3), (2, 2)])
def test_petz_three_formulas_agree(old, k, nB):
    n = k + nB
    U = haar_unitary(2 ** n, rng(3 + k))
    for m in range(n + 1):
        Psi = rc.hp_tensor(U, k, nB, m, old)
        a = rc.petz_fidelity_pure(Psi)
        b = rc.petz_fidelity_mixed(rc.rho_QX(Psi), 2 ** k)
        c = rc.petz_fidelity_explicit(rc.hp_channel_kraus(U, k, nB, m, old))
        assert abs(a - b) < 1e-10 and abs(a - c) < 1e-10


@pytest.mark.parametrize("old", [True, False])
def test_petz_endpoints(old):
    k, nB = 1, 3
    U = haar_unitary(16, rng(5))
    assert abs(rc.petz_fidelity_pure(rc.hp_tensor(U, k, nB, 0, old)) - 0.25) < 1e-12
    assert abs(rc.petz_fidelity_pure(rc.hp_tensor(U, k, nB, 4, old)) - 1.0) < 1e-12


def test_fidelity_bounds_and_fuchs_van_de_graaf():
    for r in range(6):
        a, b = rand_density(6, r), rand_density(6, r + 10)
        F = rc.uhlmann_fidelity(a, b)
        T = rc.trace_distance(a, b)
        assert 0.0 <= F <= 1.0 and 0.0 <= T <= 1.0
        assert 1 - np.sqrt(F) <= T + 1e-12
        assert T <= np.sqrt(1 - F) + 1e-12
    assert abs(rc.uhlmann_fidelity(a, a) - 1) < 1e-9


@pytest.mark.parametrize("old", [True, False])
def test_recovery_fidelity_bounds_and_barnum_knill(old):
    k, nB = 1, 4
    U = haar_unitary(32, rng(6))
    for m in range(6):
        r = rc.recovery_metrics(U, k, nB, m, old=old, with_yk=False)
        assert 0.25 - 1e-12 <= r["F_petz"] <= 1 + 1e-12          # 1/d_M^2 <= F <= 1
        assert 0.0 <= r["F_uhl"] <= 1.0
        assert r["F_petz"] >= r["F_uhl"] ** 2 - 1e-10           # F_Petz >= F_opt^2 >= F_uhl^2
        assert np.sqrt(r["F_uhl"]) >= 1 - r["T_prod"] - 1e-10   # Fuchs-van de Graaf
        assert r["T_prod"] <= 2 * r["T_mm"] + 1e-12


def test_noise_limits():
    k, nB = 1, 3
    U = haar_unitary(16, rng(7))
    for m in (1, 2, 3):
        pure = rc.petz_fidelity_pure(rc.hp_tensor(U, k, nB, m, True))
        assert abs(rc.noisy_petz_fidelity(U, k, nB, m, 0.0, True) - pure) < 1e-10
        # fully depolarized D: Bob keeps only R, which is decoupled from Q -> 1/d_M^2
        assert abs(rc.noisy_petz_fidelity(U, k, nB, m, 1.0, True) - 0.25) < 1e-10


def test_light_cone_no_recovery():
    """Brickwork depth t < n - m: the message (qubit 0) cannot reach D."""
    k, nB = 1, 5
    n = k + nB
    for m in (1, 2, 3):
        for t in range(0, n - m):
            U = brickwork_unitary(n, t, rng(8 + t), gate="haar") if t else np.eye(2 ** n, dtype=complex)
            F = rc.petz_fidelity_pure(rc.hp_tensor(U, k, nB, m, True))
            assert abs(F - 0.25) < 1e-10


def test_haar_purity_matches_formula_mc():
    k, nB, m = 1, 3, 2
    vals = [rc.decoupling(rc.hp_tensor(haar_unitary(16, rng(100 + s)), k, nB, m, True))["purity_QBp"]
            for s in range(300)]
    mu, se = np.mean(vals), np.std(vals) / np.sqrt(len(vals))
    assert abs(mu - hp.haar_mean_purity_RBp_old(k, nB, m)) < 4 * se + 1e-12


# ---------------------------------------------------------------- OTOCs
def test_otoc_identity_is_one():
    U = haar_unitary(16, rng(9))
    I = np.eye(16, dtype=complex)
    Z0 = ot.pauli_string(4, {0: "Z"})
    assert abs(ot.otoc(U, I, Z0) - 1) < 1e-12
    assert abs(ot.otoc(U, Z0, I) - 1) < 1e-12
    assert abs(ot.otoc(I, I, I) - 1) < 1e-12


def test_otoc_t0_commutation():
    I = np.eye(8, dtype=complex)
    assert abs(ot.otoc(I, ot.pauli_string(3, {0: "X"}), ot.pauli_string(3, {0: "Z"})) + 1) < 1e-12
    assert abs(ot.otoc(I, ot.pauli_string(3, {0: "X"}), ot.pauli_string(3, {1: "Z"})) - 1) < 1e-12


def test_otoc_haar_average():
    n = 3
    W, V = ot.pauli_string(n, {2: "Z"}), ot.pauli_string(n, {0: "X"})
    vals = [ot.otoc(haar_unitary(2 ** n, rng(200 + s)), W, V) for s in range(400)]
    mu, se = np.mean(vals), np.std(vals) / np.sqrt(len(vals))
    assert abs(mu - ot.haar_otoc(n)) < 4 * se


def test_clifford_otoc_is_plus_minus_one():
    W, V = ot.pauli_string(4, {3: "Z"}), ot.pauli_string(4, {0: "X"})
    for s in range(5):
        U = brickwork_unitary(4, 6, rng(300 + s), gate="clifford")
        assert abs(abs(ot.otoc(U, W, V)) - 1) < 1e-10


def test_otoc_vs_depth_matches_dense():
    pairs = [({3: "Z"}, {0: "X"})]
    a = ot.otoc_vs_depth(4, 5, rng(400), "haar", pairs)
    U = brickwork_unitary(4, 5, rng(400), gate="haar")
    assert abs(a[5, 0] - ot.otoc(U, ot.pauli_string(4, {3: "Z"}), ot.pauli_string(4, {0: "X"}))) < 1e-12
    assert abs(a[0, 0] - 1) < 1e-12


@pytest.mark.parametrize("gate", ["haar_global", "haar", "clifford"])
def test_yoshida_kitaev_otoc_identity(gate):
    """P_EPR (eh.hayden_preskill) == OTOC averaged over all Paulis on M and D."""
    k, nB = 1, 3
    n = k + nB
    U = haar_unitary(16, rng(500)) if gate == "haar_global" else brickwork_unitary(n, 4, rng(501), gate=gate)
    for m in (1, 2):
        P = hp.yoshida_kitaev(U, k, nB, m)["P_EPR"]
        O = ot.pauli_averaged_otoc(U, n, list(range(k)), list(range(n - m, n)))
        assert abs(P - O) < 1e-12


def test_otoc_fast_matches_dense():
    U = haar_unitary(16, rng(600))
    for w in ({3: "Z"}, {2: "Y"}, {1: "X", 3: "Y"}):
        vs = [{0: "X"}, {0: "Y"}, {0: "Z"}, {0: "Y", 1: "Y"}]
        fast = ot.otoc_fast(U, 4, w, vs)
        for v, f in zip(vs, fast):
            assert abs(f - ot.otoc(U, ot.pauli_string(4, w), ot.pauli_string(4, v))) < 1e-12


def test_clifford_petz_fidelity_is_discrete():
    """Stabilizer states: F_Petz takes values in {1/4, 1/2, 1} for k = 1."""
    for s in range(6):
        U = brickwork_unitary(4, 12, rng(700 + s), gate="clifford")
        for m in range(5):
            F = rc.petz_fidelity_pure(rc.hp_tensor(U, 1, 3, m, True))
            assert min(abs(F - x) for x in (0.25, 0.5, 1.0)) < 1e-9
