"""Tests for Extensions 1 (scramblers) and 2 (Hayden-Preskill).
Run:  OMP_NUM_THREADS=2 python3 -m pytest tests/test_ext.py -q
"""
import os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from eh import circuits as c
from eh import hayden_preskill as hp

LOG2 = np.log(2.0)


# ------------------------------ Extension 1 --------------------------------
def test_clifford_group_size_and_unitarity():
    g = c.two_qubit_clifford_group()
    assert g.shape == (11520, 4, 4)
    err = np.abs(np.einsum("gij,gkj->gik", g, g.conj()) - np.eye(4)).max()
    assert err < 1e-12


def test_clifford_elements_distinct_mod_phase():
    g = c.two_qubit_clifford_group()
    # |tr(g_i^dag g_j)| = 4 iff equal up to phase; check a random subset vs all
    rng = np.random.default_rng(0)
    idx = rng.choice(len(g), 40, replace=False)
    ov = np.abs(np.einsum("aij,bij->ab", g[idx].conj(), g))
    assert ((ov > 4 - 1e-9).sum(axis=1) == 1).all()


def test_cliffords_map_paulis_to_paulis_all_elements():
    g = c.two_qubit_clifford_group()
    paulis = np.array(c.pauli_group_2q())  # 16 x 4 x 4
    # C P C^dag for all C, P ; coefficient on each Pauli Q: tr(Q^dag C P C^dag)/4
    cp = np.einsum("gij,pjk,glk->gpil", g, paulis, g.conj())
    coef = np.einsum("qli,gpil->gpq", paulis.conj(), cp) / 4.0
    mag = np.abs(coef)
    # exactly one Pauli with coefficient +/-1 (real), all others 0
    assert np.allclose(np.sort(mag, axis=-1)[..., -1], 1.0, atol=1e-9)
    assert np.allclose(np.sort(mag, axis=-1)[..., :-1], 0.0, atol=1e-9)
    lead = np.take_along_axis(coef, mag.argmax(-1)[..., None], -1)[..., 0]
    assert np.abs(lead.imag).max() < 1e-9
    # the induced map on Paulis is a permutation (injective) for every C
    assert all(len(set(row)) == 16 for row in mag.argmax(-1)[::97])


def test_is_pauli_helper_and_non_clifford_fails():
    assert c.is_pauli_up_to_sign(-np.kron(c.X1, c.Z1))
    T = np.diag([1, np.exp(1j * np.pi / 4)])
    TI = np.kron(T, c.I1)
    XI = np.kron(c.X1, c.I1)
    assert not c.is_pauli_up_to_sign(TI @ XI @ TI.conj().T)


def test_haar_unitary_is_unitary():
    rng = np.random.default_rng(1)
    u = c.haar_unitary(64, rng)
    assert np.abs(u @ u.conj().T - np.eye(64)).max() < 1e-12


@pytest.mark.parametrize("scr", ["haar", "haar_shortcut", "local_haar", "clifford",
                                 "identity", "swap", "h_cnot"])
def test_circuits_preserve_norm_and_entropy_bounds(scr):
    rng = np.random.default_rng(2)
    n = 8
    r = c.evaporate(n, scr, rng, depth=3)
    assert abs(r["norm"] - 1.0) < 1e-10
    t = np.arange(n + 1)
    cap = np.minimum(t, n - t) * LOG2
    assert (r["s_vn"] <= cap + 1e-9).all() and (r["s_vn"] >= -1e-12).all()
    assert (r["s_2"] <= r["s_vn"] + 1e-9).all()
    assert abs(r["s_vn"][0]) < 1e-12 and abs(r["s_vn"][-1]) < 1e-9


def test_brickwork_unitary_is_unitary_and_matches_state_application():
    rng = np.random.default_rng(3)
    U = c.brickwork_unitary(5, 4, rng, "haar")
    assert np.abs(U @ U.conj().T - np.eye(32)).max() < 1e-12
    rng = np.random.default_rng(3)
    st = c.zero_state(5)
    for layer in range(4):
        st = c.apply_brick_layer(st, 5, layer, rng, "haar")
    assert np.allclose(st.ravel(), U[:, 0], atol=1e-12)


def test_clifford_states_have_flat_entanglement_spectrum():
    rng = np.random.default_rng(4)
    for _ in range(5):
        r = c.evaporate(8, "clifford", rng, depth=4, return_spectra=True)
        assert np.allclose(r["s_vn"], r["s_2"], atol=1e-9)           # flat
        assert np.allclose(r["s_vn"] / LOG2, np.round(r["s_vn"] / LOG2), atol=1e-9)  # integer bits
        for p in r["spectra"]:
            nz = p[p > 1e-10]
            assert np.allclose(nz, 1.0 / len(nz), atol=1e-9)


def test_later_black_hole_unitaries_do_not_change_radiation_entropy():
    """Justifies 'haar_shortcut': a unitary on the remaining black hole leaves
    the spectrum of already-emitted radiation unchanged."""
    rng = np.random.default_rng(5)
    n, t = 8, 3
    st = c.haar_state(n, rng)
    p0 = c.schmidt_probs(st, n - t)
    u = c.haar_unitary(2 ** (n - t), rng)
    st2 = (u @ st.reshape(2 ** (n - t), 2 ** t)).reshape((2,) * n)
    assert np.allclose(p0, c.schmidt_probs(st2, n - t), atol=1e-12)


def test_page_formula_and_haar_average():
    # exact small case: m=n=2 -> S = 1/3+1/4 - 1/4 = 1/3
    assert abs(c.page_entropy(2, 2) - 1.0 / 3.0) < 1e-14
    rng = np.random.default_rng(6)
    n, t, ns = 8, 4, 400
    vals = [c.entropy_vn(c.schmidt_probs(c.haar_state(n, rng), n - t)) for _ in range(ns)]
    sem = np.std(vals) / np.sqrt(ns)
    assert abs(np.mean(vals) - c.page_entropy(16, 16)) < 5 * sem + 1e-4
    pur = [np.sum(c.schmidt_probs(c.haar_state(n, rng), n - t) ** 2) for _ in range(ns)]
    assert abs(np.mean(pur) - c.haar_mean_purity(16, 16)) < 5 * np.std(pur) / np.sqrt(ns)


def test_dimer_control_curve():
    r = c.evaporate(8, "h_cnot", np.random.default_rng(0))
    assert np.allclose(r["s_vn"] / LOG2, [0, 1, 0, 1, 0, 1, 0, 1, 0], atol=1e-9)


def test_entropy_clipping_no_nan():
    assert c.entropy_vn(np.array([1.0, 0.0, 1e-20])) == 0.0
    assert np.isnan(c.spacing_ratio(np.full(8, 1 / 8)))


# ------------------------------ Extension 2 --------------------------------
def _old(k, nB, seed):
    rng = np.random.default_rng(seed)
    return c.haar_unitary(2 ** (k + nB), rng)


@pytest.mark.parametrize("k,nB", [(1, 3), (2, 3), (1, 5)])
def test_hp_state_is_normalised_and_pure(k, nB):
    U = _old(k, nB, 10)
    for m in range(k + nB + 1):
        T = hp.hp_state_old(U, k, nB, m)
        assert abs(np.vdot(T, T).real - 1.0) < 1e-12
        # purity of the global state: complementary subsystems have equal entropy
        assert abs(hp.S(T, ("R", "Bp")) - hp.S(T, ("E", "D"))) < 1e-9
        assert abs(hp.S(T, ("R",)) - hp.S(T, ("Bp", "D", "E"))) < 1e-9
        assert abs(hp.S(T, ("R", "Bp", "D", "E"))) < 1e-9
        assert abs(hp.S(T, ("R",)) - k * LOG2) < 1e-9          # R maximally mixed
        assert abs(hp.S(T, ("E",)) - nB * LOG2) < 1e-9         # E maximally mixed


def test_hp_state_matches_explicit_construction():
    """T = U/sqrt(d) equals (U_AB x 1)|Bell>_RA|Bell>_BE built explicitly."""
    k, nB, m = 1, 2, 2
    U = _old(k, nB, 11)
    dA, dB = 2 ** k, 2 ** nB
    psi0 = np.einsum("ra,be->abre", np.eye(dA), np.eye(dB)) / np.sqrt(dA * dB)
    psi = (U @ psi0.reshape(dA * dB, dA * dB)).reshape(2 ** (k + nB - m), 2 ** m, dA, dB)
    assert np.allclose(psi, hp.hp_state_old(U, k, nB, m), atol=1e-12)


@pytest.mark.parametrize("old", [True, False])
def test_mutual_information_nonneg_symmetric_and_bounded(old):
    k, nB = 2, 4
    rng = np.random.default_rng(12)
    U = c.haar_unitary(2 ** (k + nB), rng)
    for m in range(k + nB + 1):
        T = hp.hp_state_old(U, k, nB, m) if old else \
            hp.hp_state_young(hp.young_isometry_from_unitary(U, k, nB), k, nB, m)
        pairs = [(("R",), ("Bp",)), (("R",), ("E", "D")), (("R",), ("D",)), (("Bp",), ("D",))]
        for X, Y in pairs:
            i1 = hp.mutual_information(T, X, Y)
            i2 = hp.mutual_information(T, Y, X)
            assert i1 >= -1e-9
            assert abs(i1 - i2) < 1e-9
        # pure state + R: I(R:B') + I(R:ED) = 2 S(R) = 2 k log 2
        a = hp.analyze(T, k, with_decoupling=False)
        assert abs(a["I_R_Bp"] + a["I_R_ED"] - 2 * k * LOG2) < 1e-9
        assert a["I_R_ED"] <= 2 * k * LOG2 + 1e-9


@pytest.mark.parametrize("k,nB", [(1, 4), (2, 4), (3, 3)])
def test_decoupling_limits_old(k, nB):
    U = _old(k, nB, 13)
    n = k + nB
    a0 = hp.analyze(hp.hp_state_old(U, k, nB, 0), k)
    # m = 0: Bob holds only E, which never interacted with the diary -> exactly 0
    assert abs(a0["I_R_ED"]) < 1e-9
    assert abs(a0["I_R_Bp"] - 2 * k * LOG2) < 1e-9
    assert abs(a0["F_uhl"] - 4.0 ** (-k)) < 1e-6  # sqrt of ~1e-16 eigenvalue noise
    an = hp.analyze(hp.hp_state_old(U, k, nB, n), k)
    # m = n: Bob holds everything -> I = 2 k log 2, perfect decoupling/recovery
    assert abs(an["I_R_ED"] - 2 * k * LOG2) < 1e-9
    assert an["T_prod"] < 1e-9 and abs(an["F_uhl"] - 1.0) < 1e-6


def test_decoupling_limits_young():
    k, nB = 1, 6
    rng = np.random.default_rng(14)
    V = hp.haar_isometry(2 ** (k + nB), 2 ** k, rng)
    assert np.allclose(V.conj().T @ V, np.eye(2 ** k), atol=1e-12)
    a0 = hp.analyze(hp.hp_state_young(V, k, nB, 0), k)
    an = hp.analyze(hp.hp_state_young(V, k, nB, k + nB), k)
    assert abs(a0["I_R_ED"]) < 1e-9 and abs(an["I_R_ED"] - 2 * k * LOG2) < 1e-9
    # early on (m < n_B/2) a young black hole reveals almost nothing
    a2 = hp.analyze(hp.hp_state_young(V, k, nB, 2), k)
    assert a2["I_R_ED"] < 0.2 * LOG2


def test_identity_scrambler_no_recovery_until_diary_emitted():
    """Control: U = 1. D = last m qubits = black-hole qubits; the diary (first
    k qubits) is only emitted when m > n_B."""
    k, nB = 1, 3
    U = np.eye(2 ** (k + nB), dtype=complex)
    for m in range(nB + 1):
        assert abs(hp.analyze(hp.hp_state_old(U, k, nB, m), k, False)["I_R_ED"]) < 1e-9
    a = hp.analyze(hp.hp_state_old(U, k, nB, nB + 1), k, False)
    assert abs(a["I_R_ED"] - 2 * LOG2) < 1e-9


@pytest.mark.parametrize("k,nB,m", [(1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3), (2, 2, 3), (1, 3, 2)])
def test_yoshida_kitaev_decoder(k, nB, m):
    U = _old(k, nB, 15)
    y = hp.yoshida_kitaev(U, k, nB, m)
    ysv = hp.yoshida_kitaev_statevector(U, k, nB, m)
    assert abs(ysv["norm_before_projection"] - 1.0) < 1e-10
    assert abs(y["P_EPR"] - ysv["P_EPR"]) < 1e-10
    assert abs(y["F_EPR"] - ysv["F_EPR"]) < 1e-10
    assert abs(y["P_EPR"] * y["F_EPR"] - 4.0 ** (-k)) < 1e-10
    T = hp.hp_state_old(U, k, nB, m)
    pur = hp.analyze(T, k, False)["purity_RBp"]
    assert abs(y["P_EPR"] - 2.0 ** (nB - m) * pur) < 1e-10
    assert 0 <= y["F_EPR"] <= 1 + 1e-10
    # the Uhlmann bound is a bound on the OPTIMAL decoder; YK post-selected
    # fidelity is a different quantity, both must lie in [4^-k, 1]
    assert y["F_EPR"] >= 4.0 ** (-k) - 1e-10


def test_yk_limits():
    k, nB = 2, 3
    U = _old(k, nB, 16)
    y0 = hp.yoshida_kitaev(U, k, nB, 0)
    yn = hp.yoshida_kitaev(U, k, nB, k + nB)
    assert abs(y0["P_EPR"] - 1.0) < 1e-10 and abs(y0["F_EPR"] - 4.0 ** (-k)) < 1e-10
    assert abs(yn["F_EPR"] - 1.0) < 1e-10 and abs(yn["P_EPR"] - 4.0 ** (-k)) < 1e-10


def test_haar_mean_purity_formulas():
    k, nB, ns = 1, 3, 600
    rng = np.random.default_rng(17)
    n = k + nB
    acc_o = np.zeros((ns, n + 1)); acc_y = np.zeros((ns, n + 1))
    for s in range(ns):
        U = c.haar_unitary(2 ** n, rng)
        V = hp.young_isometry_from_unitary(U, k, nB)
        for m in range(n + 1):
            acc_o[s, m] = hp.analyze(hp.hp_state_old(U, k, nB, m), k, False)["purity_RBp"]
            acc_y[s, m] = hp.analyze(hp.hp_state_young(V, k, nB, m), k, False)["purity_RBp"]
    for m in range(n + 1):
        for acc, f in ((acc_o, hp.haar_mean_purity_RBp_old), (acc_y, hp.haar_mean_purity_RBp_young)):
            sem = acc[:, m].std() / np.sqrt(ns)
            assert abs(acc[:, m].mean() - f(k, nB, m)) < 5 * sem + 1e-12
    # NOTE: the young state is NOT a Haar-random state on R x (B'D) (rho_R is
    # exactly maximally mixed), so Lubkin's formula is only the large-d limit.
    lub = (2.0 * 2.0 ** (9 - 3) + 2.0 ** 3) / (2.0 * 2.0 ** 9 + 1)
    assert abs(hp.haar_mean_purity_RBp_young(1, 8, 3) / lub - 1) < 1e-3


def test_decoupling_bound_holds_on_average():
    k, nB, ns = 1, 4, 60
    rng = np.random.default_rng(18)
    n = k + nB
    tm = np.zeros((ns, n + 1)); tp = np.zeros((ns, n + 1))
    for s in range(ns):
        U = c.haar_unitary(2 ** n, rng)
        for m in range(n + 1):
            a = hp.decoupling_metrics(hp.hp_state_old(U, k, nB, m))
            tm[s, m], tp[s, m] = a["T_mm"], a["T_prod"]
    for m in range(n + 1):
        b = hp.decoupling_bound_mm(k, nB, m)
        assert tm[:, m].mean() <= b + 1e-9
        assert tp[:, m].mean() <= 2 * b + 1e-9
    # Fuchs-van de Graaf consistency: F_uhl >= (1 - T_prod)^2
    a = hp.decoupling_metrics(hp.hp_state_old(U, k, nB, 2))
    assert a["F_uhl"] >= (1 - a["T_prod"]) ** 2 - 1e-9


# ------------------------- torch / GPU backend ------------------------------
torch = pytest.importorskip("torch")
DEV = c.get_device()


def test_gpu_gate_application_matches_numpy():
    rng = np.random.default_rng(30)
    n = 6
    st = c.haar_state(n, rng)
    g = c.haar_unitary(4, rng)
    for i in range(n - 1):
        ref = c.apply_2q(st, g, i, i + 1).ravel()
        out = c.t_apply_2q(c.to_t(st.reshape(1, -1), DEV), c.to_t(g, DEV), i)
        assert np.abs(np.array(out.cpu().tolist())[0] - ref).max() < 1e-12


def test_gpu_gram_spectrum_matches_svd():
    rng = np.random.default_rng(31)
    n = 9
    st = c.haar_state(n, rng)
    for nl in (2, 4, 5, 7):
        p = c.to_np(c.t_schmidt_probs(c.to_t(st.reshape(1, -1), DEV), nl, n))[0]
        ref = c.schmidt_probs(st, nl)
        assert np.abs(p - ref[: len(p)]).max() < 1e-12
        sv, s2, smin, rk = c.t_entropies(c.to_t(p[None], DEV).real)
        assert abs(float(sv) - c.entropy_vn(ref)) < 1e-10
        assert abs(float(s2) - c.entropy_renyi2(ref)) < 1e-10


def test_gpu_haar_unitary_and_gate_batches_are_unitary():
    u = c.t_haar_unitary(128, 7, DEV)
    eye = torch.eye(128, dtype=u.dtype, device=u.device)
    assert float((u @ u.conj().T - eye).abs().max()) < 1e-12
    for g in (c.haar_gates_np((5, 3), np.random.default_rng(1)),
              c.clifford_gates_np((5, 3), np.random.default_rng(1))):
        assert g.shape == (5, 3, 4, 4)
        assert np.abs(np.einsum("...ij,...kj->...ik", g, g.conj()) - np.eye(4)).max() < 1e-12


@pytest.mark.parametrize("scr", ["haar", "haar_shortcut", "local_haar", "clifford",
                                 "identity", "swap", "h_cnot"])
def test_gpu_evaporation_norm_bounds_and_endpoints(scr):
    n, B = 8, 6
    r = c.t_evaporate(n, scr, B, np.random.SeedSequence([99, 1]), depth=3, device=DEV)
    assert np.abs(r["norm"] - 1.0).max() < 1e-10
    t = np.arange(n + 1)
    cap = np.minimum(t, n - t) * LOG2
    assert (r["s_vn"] <= cap + 1e-8).all() and (r["s_vn"] >= -1e-10).all()
    assert (r["s_2"] <= r["s_vn"] + 1e-8).all() and (r["s_min"] <= r["s_2"] + 1e-8).all()
    assert np.abs(r["s_vn"][:, 0]).max() < 1e-12 and np.abs(r["s_vn"][:, -1]).max() < 1e-8
    if scr == "clifford":      # stabilizer states: flat spectrum, integer bits
        assert np.abs(r["s_vn"] - r["s_2"]).max() < 1e-8
        assert np.abs(r["s_vn"] / LOG2 - np.round(r["s_vn"] / LOG2)).max() < 1e-8
        assert np.abs(r["s_vn"] / LOG2 - np.log2(r["rank"])).max() < 1e-8
    if scr in ("identity", "swap"):
        assert np.abs(r["s_vn"]).max() < 1e-10
    if scr == "h_cnot":
        assert np.allclose(r["s_vn"] / LOG2, [0, 1, 0, 1, 0, 1, 0, 1, 0], atol=1e-8)


def test_gpu_explicit_sequential_haar_matches_page():
    n, B = 8, 200
    page = c.page_curve(n)
    for scr in ("haar", "haar_shortcut"):
        r = c.t_evaporate(n, scr, B, np.random.SeedSequence([99, 2]), device=DEV)
        sem = r["s_vn"].std(0, ddof=1) / np.sqrt(B)
        assert (np.abs(r["s_vn"].mean(0) - page) < 5 * sem + 1e-6).all()


def test_gpu_brickwork_columns_match_numpy_unitary():
    n = 5
    U = c.brickwork_unitary(n, 3, np.random.default_rng(40), "haar")
    # numpy version draws gates pair by pair; GPU version per layer in one call
    # -> compare structure instead: unitary + first-k-qubit column subset
    Ut = hp.t_brickwork_columns(n, 3, np.random.default_rng(40), "haar", n, DEV)
    eye = torch.eye(2 ** n, dtype=Ut.dtype, device=Ut.device)
    assert float((Ut.conj().T @ Ut - eye).abs().max()) < 1e-12
    V = hp.t_brickwork_columns(n, 3, np.random.default_rng(40), "haar", 2, DEV)
    assert float((V - Ut.reshape(32, 4, 8)[:, :, 0]).abs().max()) < 1e-12
    assert U.shape == (32, 32)


@pytest.mark.parametrize("k,nB", [(1, 3), (2, 3), (2, 4)])
def test_gpu_old_metrics_match_dense_numpy(k, nB):
    U = _old(k, nB, 50)
    Ut = c.to_t(U, DEV)
    for m in range(k + nB + 1):
        a = hp.analyze(hp.hp_state_old(U, k, nB, m), k)
        y = hp.yoshida_kitaev(U, k, nB, m)
        g = hp.t_old_metrics(Ut, k, nB, m)
        assert abs(g["trace"] - 1.0) < 1e-12                       # normalised
        assert abs(g["I_R_ED"] - a["I_R_ED"]) < 1e-8 and abs(g["I_R_Bp"] - a["I_R_Bp"]) < 1e-8
        assert g["I_R_ED"] >= -1e-8 and g["I_R_Bp"] >= -1e-8
        assert abs(g["T_prod"] - a["T_prod"]) < 1e-8 and abs(g["T_prod"] - a["T_mm"]) < 1e-8
        assert abs(g["F_uhl"] - a["F_uhl"]) < 1e-6
        assert abs(g["P_EPR"] - y["P_EPR"]) < 1e-10 and abs(g["F_EPR"] - y["F_EPR"]) < 1e-10
    g0, gn = hp.t_old_metrics(Ut, k, nB, 0), hp.t_old_metrics(Ut, k, nB, k + nB)
    assert abs(g0["I_R_ED"]) < 1e-8 and abs(gn["I_R_ED"] - 2 * k * LOG2) < 1e-8
    assert abs(g0["T_prod"] - (1 - 4.0 ** (-k))) < 1e-8 and gn["T_prod"] < 1e-8


@pytest.mark.parametrize("k,nB", [(1, 5), (2, 4)])
def test_gpu_young_metrics_match_dense_numpy(k, nB):
    rng = np.random.default_rng(51)
    V = hp.haar_isometry(2 ** (k + nB), 2 ** k, rng)
    Vt = c.to_t(V, DEV)
    for m in range(k + nB + 1):
        a = hp.analyze(hp.hp_state_young(V, k, nB, m), k)
        g = hp.t_young_metrics(Vt, k, nB, m)
        assert abs(g["I_R_D"] - a["I_R_ED"]) < 1e-8 and abs(g["I_R_Bp"] - a["I_R_Bp"]) < 1e-8
        assert abs(g["I_R_D"] + g["I_R_Bp"] - 2 * k * LOG2) < 1e-8
        assert g["I_R_D"] >= -1e-8
        assert abs(g["T_prod"] - a["T_prod"]) < 1e-8 and abs(g["F_uhl"] - a["F_uhl"]) < 1e-6
    Vg = hp.t_haar_isometry(2 ** (k + nB), 2 ** k, 3, DEV)
    eye = torch.eye(2 ** k, dtype=Vg.dtype, device=Vg.device)
    assert float((Vg.conj().T @ Vg - eye).abs().max()) < 1e-12
