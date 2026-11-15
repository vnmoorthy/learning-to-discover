"""Core correctness tests.  Run:  .venv/bin/python -m pytest -q tests/test_core.py

All random tests use fixed seeds (recorded below) so that the run is reproducible.
"""
import itertools
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eh import entropy as E  # noqa: E402
from eh import page as P  # noqa: E402
from eh import pairs  # noqa: E402
from eh import qstates as Q  # noqa: E402

try:
    import torch

    HAS_CUDA = torch.cuda.is_available()
except Exception:  # pragma: no cover
    torch = None
    HAS_CUDA = False

SEED = 20261115
TOL = 1e-12


def rng(offset=0):
    return np.random.default_rng(SEED + offset)


def partial_trace_loop(rho, dims, keep):
    """Explicit (slow) index-loop partial trace, written independently of eh.qstates."""
    n = len(dims)
    rest = [i for i in range(n) if i not in keep]
    dk = int(np.prod([dims[i] for i in keep])) if keep else 1
    out = np.zeros((dk, dk), dtype=complex)
    strides = [int(np.prod(dims[i + 1:])) for i in range(n)]

    def flat(idx):
        return sum(i * s for i, s in zip(idx, strides))

    keep_ranges = [range(dims[i]) for i in keep]
    rest_ranges = [range(dims[i]) for i in rest]
    for a, ka in enumerate(itertools.product(*keep_ranges)):
        for b, kb in enumerate(itertools.product(*keep_ranges)):
            acc = 0.0
            for r in itertools.product(*rest_ranges):
                ia = [0] * n
                ib = [0] * n
                for pos, i in enumerate(keep):
                    ia[i] = ka[pos]
                    ib[i] = kb[pos]
                for pos, i in enumerate(rest):
                    ia[i] = r[pos]
                    ib[i] = r[pos]
                acc += rho[flat(ia), flat(ib)]
            out[a, b] = acc
    return out


CASES = [((2, 3), (0,)), ((2, 3), (1,)), ((2, 2, 2), (0, 2)), ((3, 2, 4), (1,)), ((2, 3, 2, 2), (3, 0)),
         ((4, 5), (0,)), ((2, 2, 2, 2, 2), (1, 3, 4))]


@pytest.mark.parametrize("dims,keep", CASES)
def test_density_matrix_properties(dims, keep):
    d = int(np.prod(dims))
    psi = Q.haar_state(d, rng(1))
    rho = Q.reduced_density_matrix(psi, dims, keep)
    dk = rho.shape[0]
    assert np.abs(rho - rho.conj().T).max() < TOL  # Hermitian
    ev = np.linalg.eigvalsh(rho)
    assert ev.min() >= -1e-12  # positive semidefinite
    assert abs(np.trace(rho).real - 1) < TOL and abs(np.trace(rho).imag) < TOL  # unit trace
    assert abs(ev.sum() - 1) < TOL  # eigenvalue normalisation
    s = E.von_neumann(ev)
    assert s >= 0 and s <= math.log(dk) + 1e-12
    pu = E.purity(ev)
    assert 1.0 / dk - 1e-12 <= pu <= 1 + 1e-12
    assert abs(pu - np.trace(rho @ rho).real) < TOL
    assert E.renyi2(ev) <= s + 1e-12  # S_2 <= S_1


@pytest.mark.parametrize("dims,keep", CASES)
def test_partial_trace_vs_explicit_loop(dims, keep):
    d = int(np.prod(dims))
    r = rng(2)
    # generic mixed state
    a = r.standard_normal((d, d)) + 1j * r.standard_normal((d, d))
    rho = a @ a.conj().T
    rho /= np.trace(rho)
    fast = Q.partial_trace(rho, dims, keep)
    slow = partial_trace_loop(rho, list(dims), list(keep))
    assert np.abs(fast - slow).max() < TOL
    # pure state: matrix route == state route
    psi = Q.haar_state(d, r)
    assert np.abs(Q.partial_trace(np.outer(psi, psi.conj()), dims, keep) - Q.reduced_density_matrix(psi, dims, keep)).max() < TOL


def test_partial_trace_product_states():
    r = rng(3)
    dims = (3, 2, 4)
    vs = [Q.haar_state(d, r) for d in dims]
    psi = np.kron(np.kron(vs[0], vs[1]), vs[2])
    for keep in [(0,), (1,), (2,), (0, 1), (1, 2), (0, 2), (2, 0)]:
        rho = Q.reduced_density_matrix(psi, dims, keep)
        expect = np.ones((1, 1), dtype=complex)
        for i in keep:
            expect = np.kron(expect, np.outer(vs[i], vs[i].conj()))
        assert np.abs(rho - expect).max() < TOL
        assert abs(E.entropy_of_density(rho)) < 1e-10  # product state: zero entanglement
        assert abs(E.purity(np.linalg.eigvalsh(rho)) - 1) < 1e-10
    # mixed product state rho_A (x) rho_B
    a = r.standard_normal((3, 3)) + 1j * r.standard_normal((3, 3)); ra = a @ a.conj().T; ra /= np.trace(ra)
    b = r.standard_normal((4, 4)) + 1j * r.standard_normal((4, 4)); rb = b @ b.conj().T; rb /= np.trace(rb)
    rho = np.kron(ra, rb)
    assert np.abs(Q.partial_trace(rho, (3, 4), (0,)) - ra).max() < TOL
    assert np.abs(Q.partial_trace(rho, (3, 4), (1,)) - rb).max() < TOL


@pytest.mark.parametrize("dA,dB", [(2, 2), (2, 7), (3, 5), (4, 4), (5, 3), (8, 16), (16, 8), (6, 35), (32, 32), (7, 64)])
def test_schmidt_equals_both_reduced_spectra_and_SR_eq_SB(dA, dB):
    for trial in range(5):
        psi = Q.haar_state(dA * dB, rng(100 + trial))
        s = Q.schmidt_coefficients(psi, (dA, dB), (0,))
        assert abs((s**2).sum() - 1) < TOL
        p = np.sort(s**2)[::-1]
        ra = Q.reduced_density_matrix(psi, (dA, dB), (0,))
        rb = Q.reduced_density_matrix(psi, (dA, dB), (1,))
        ea = np.sort(np.linalg.eigvalsh(ra))[::-1]
        eb = np.sort(np.linalg.eigvalsh(rb))[::-1]
        k = min(dA, dB)
        assert np.abs(ea[:k] - p).max() < 1e-12 and np.abs(eb[:k] - p).max() < 1e-12
        assert np.abs(ea[k:]).max(initial=0) < 1e-12 and np.abs(eb[k:]).max(initial=0) < 1e-12
        sa, sb, ss = E.von_neumann(ea), E.von_neumann(eb), E.entropy_from_schmidt(s)
        assert abs(sa - sb) < 1e-11 and abs(sa - ss) < 1e-11  # S(R) = S(B)
        assert abs(E.purity(ea) - E.purity(eb)) < 1e-12


def test_SR_eq_SB_multi_qubit_bipartitions():
    N = 8
    psi = Q.haar_state(2**N, rng(7))
    dims = (2,) * N
    for keep in [(0,), (0, 1, 2), (1, 3, 5, 7), (6, 2), (0, 1, 2, 3, 4, 5, 6)]:
        rest = tuple(i for i in range(N) if i not in keep)
        sa = E.entropy_of_density(Q.reduced_density_matrix(psi, dims, keep))
        sb = E.entropy_of_density(Q.reduced_density_matrix(psi, dims, rest))
        assert abs(sa - sb) < 1e-11


def test_haar_unitary_is_unitary_and_phase_fixed():
    r = rng(8)
    for d in (2, 5, 16, 64):
        u = Q.haar_unitary(d, r)
        assert np.abs(u.conj().T @ u - np.eye(d)).max() < 1e-12
    # Haar test (first moment of |U_00|^2 = 1/d, eigenphase density flat): mean of tr U ~ 0, E|tr U|^2 = 1
    tr = np.array([np.trace(Q.haar_unitary(6, r)) for _ in range(4000)])
    assert abs(np.mean(np.abs(tr) ** 2) - 1.0) < 4 * np.std(np.abs(tr) ** 2) / math.sqrt(len(tr))
    assert abs(tr.mean()) < 4 / math.sqrt(len(tr))


def test_unitary_preserves_global_entropy_and_spectrum():
    r = rng(9)
    d = 24
    a = r.standard_normal((d, d)) + 1j * r.standard_normal((d, d))
    rho = a @ a.conj().T
    rho /= np.trace(rho)
    u = Q.haar_unitary(d, r)
    rho2 = u @ rho @ u.conj().T
    e1, e2 = np.linalg.eigvalsh(rho), np.linalg.eigvalsh(rho2)
    assert np.abs(e1 - e2).max() < 1e-12
    assert abs(E.von_neumann(e1) - E.von_neumann(e2)) < 1e-11
    assert abs(E.purity(e1) - E.purity(e2)) < 1e-12
    # pure state stays pure (S = 0), norm preserved
    psi = Q.haar_state(d, r)
    phi = u @ psi
    assert abs(np.linalg.norm(phi) - 1) < TOL
    assert abs(E.entropy_of_density(np.outer(phi, phi.conj()))) < 1e-10
    # local unitary on B leaves the Schmidt spectrum across R|B invariant
    dR, dB = 4, 6
    ub = Q.haar_unitary(dB, r)
    m = psi.reshape(dR, dB)
    m2 = m @ ub.T
    s1 = np.linalg.svd(m, compute_uv=False)
    s2 = np.linalg.svd(m2, compute_uv=False)
    assert np.abs(s1 - s2).max() < 1e-12


def test_entropy_clipping_no_log_zero():
    p = np.array([0.5, 0.5, 0.0, -1e-17, 1e-300])
    with np.errstate(all="raise"):
        s = E.von_neumann(p)
    assert abs(s - math.log(2)) < 1e-15
    assert abs(E.von_neumann(p, bits=True) - 1) < 1e-15
    assert E.von_neumann(np.array([1.0, 0, 0])) == 0.0
    assert abs(E.von_neumann(np.full(8, 1 / 8)) - 3 * math.log(2)) < 1e-14


def test_page_formula_exact_values():
    from fractions import Fraction

    assert P.page_entropy_fraction(1, 5) == 0
    assert P.page_entropy_fraction(2, 2) == Fraction(1, 3)  # known: two qubits, <S> = 1/3
    assert P.page_entropy_fraction(2, 3) == Fraction(1, 4) + Fraction(1, 5) + Fraction(1, 6) - Fraction(1, 6)
    for m, n in [(2, 2), (3, 7), (4, 4), (8, 32), (16, 16), (5, 100)]:
        exact = P.page_entropy_fraction(m, n)
        assert exact == P.harmonic_fraction(m * n) - P.harmonic_fraction(n) - Fraction(m - 1, 2 * n)
        assert abs(float(exact) - P.page_entropy(m, n)) < 1e-13
        assert P.page_entropy(m, n) == P.page_entropy(n, m)
        assert abs(P.page_entropy(m, n, bits=True) * math.log(2) - P.page_entropy(m, n)) < 1e-13
        assert 0 < P.page_entropy(m, n) < math.log(m)
    # digamma branch agrees with direct summation
    from scipy.special import digamma

    m, n = 64, 4096
    assert abs(P.page_entropy(m, n) - (digamma(m * n + 1) - digamma(n + 1) - (m - 1) / (2 * n))) < 1e-11
    assert abs(P.page_entropy(4096, 4096) - (math.log(4096) - 0.5)) < 1e-6  # large-m=n limit ln m - 1/2


def test_page_asymptotics_sympy():
    out = P.sympy_verify_asymptotic()
    assert out["symbolic_ok"]
    # numerical error ordering: each added order improves the approximation
    for m, n in [(4, 64), (16, 256), (32, 32)]:
        ex = P.page_entropy(m, n)
        errs = [abs(P.page_asymptotic(m, n, o) - ex) for o in (0, 1, 2)]
        assert errs[0] > errs[1] > errs[2]


def _mc_entropies(m, n, samples, generator):
    """Entropies of the m-dim subsystem for Haar states on C^m (x) C^n (numpy batched-SVD route)."""
    out = np.empty(samples)
    chunk = max(1, 2**18 // (m * n))
    for i in range(0, samples, chunk):
        c = min(chunk, samples - i)
        z = generator.standard_normal((c, m * n)) + 1j * generator.standard_normal((c, m * n))
        z /= np.linalg.norm(z, axis=1, keepdims=True)  # Haar states
        out[i:i + c] = E.entropy_from_schmidt(np.linalg.svd(z.reshape(c, m, n), compute_uv=False))
    return out


@pytest.mark.parametrize("m,n,samples", [(2, 2, 20000), (2, 5, 20000), (3, 3, 20000), (4, 16, 8000), (8, 8, 8000),
                                         (5, 40, 4000), (16, 16, 3000), (16, 64, 1500)])
def test_page_formula_vs_monte_carlo_numpy(m, n, samples):
    s = _mc_entropies(m, n, samples, rng(1000 + 17 * m + n))
    se = s.std(ddof=1) / math.sqrt(samples)
    z = (s.mean() - P.page_entropy(m, n)) / se
    assert abs(z) < 4, (m, n, s.mean(), P.page_entropy(m, n), se, z)


def test_monte_carlo_convergence_inverse_sqrt():
    """RMS error of the sample mean over independent replicas scales like samples^(-1/2)."""
    m, n = 4, 8
    exact = P.page_entropy(m, n)
    g = rng(2000)
    sizes = [50, 200, 800, 3200]
    reps = 40
    rms = []
    for sz in sizes:
        errs = [(_mc_entropies(m, n, sz, g).mean() - exact) for _ in range(reps)]
        rms.append(math.sqrt(np.mean(np.square(errs))))
    slope = np.polyfit(np.log(sizes), np.log(rms), 1)[0]
    assert -0.65 < slope < -0.35, (slope, rms)
    # and the predicted stderr sigma/sqrt(samples) matches the observed RMS error within 35%
    sigma = _mc_entropies(m, n, 20000, g).std(ddof=1)
    for sz, r in zip(sizes, rms):
        assert 0.65 < r / (sigma / math.sqrt(sz)) < 1.35


def test_bell_pairs_exact_entropy():
    for k in range(0, 7):
        m = pairs.bell_pairs_state(k)
        p = np.linalg.svd(m, compute_uv=False) ** 2
        assert abs(E.von_neumann(p) - k * math.log(2)) < 1e-12
        assert abs(E.purity(p) - 2.0**-k) < 1e-14
        # interleaved state vector, tracing out the partner qubits explicitly
        psi = pairs.bell_pairs_statevector(k)
        if k:
            rho = Q.reduced_density_matrix(psi, (2,) * (2 * k), tuple(range(0, 2 * k, 2)))
            assert np.abs(rho - np.eye(2**k) / 2**k).max() < 1e-14
    assert pairs.hawking_entropy(5, bits=True) == 5


# ----------------------------------------------------------------------------- torch / GPU
needs_torch = pytest.mark.skipif(torch is None, reason="torch not installed")


@needs_torch
def test_torch_backend_matches_numpy():
    dev = Q.torch_device()
    gen = Q.torch_generator(SEED, dev)
    psi = Q.haar_states_t(3, 2**10, gen)
    assert torch.allclose(torch.linalg.vector_norm(psi, dim=-1), torch.ones(3, dtype=torch.float64, device=dev), atol=1e-13)
    for k in (1, 3, 5, 8):
        m = psi.reshape(3, 2**k, 2 ** (10 - k))
        pg = Q.schmidt_probs_t(m, "gram")
        ps = Q.schmidt_probs_t(m, "svd")
        assert (pg - ps).abs().max().item() < 1e-13
        s_t = E.von_neumann(pg).cpu().numpy()
        for b in range(3):
            v = psi[b].cpu().numpy()
            s_np = E.entropy_from_schmidt(Q.schmidt_coefficients(v, (2**k, 2 ** (10 - k)), (0,)))
            assert abs(s_t[b] - s_np) < 1e-11
            # S(R) = S(B) via the two Gram matrices
            rb = Q.reduced_density_matrix(psi[b], (2**k, 2 ** (10 - k)), (1,))
            assert abs(E.entropy_of_density(rb).item() - s_np) < 1e-10
    # torch partial trace == numpy partial trace on a mixed state
    a = Q.ginibre_t((12, 12), gen)
    rho = a @ a.conj().T
    rho = rho / torch.trace(rho).real
    pt = Q.partial_trace(rho, (2, 3, 2), (2, 0)).cpu().numpy()
    assert np.abs(pt - Q.partial_trace(rho.cpu().numpy(), (2, 3, 2), (2, 0))).max() < 1e-13


@needs_torch
def test_torch_haar_unitary_and_isometry():
    dev = Q.torch_device()
    gen = Q.torch_generator(SEED + 1, dev)
    u = Q.haar_unitary_t(128, gen)
    eye = torch.eye(128, dtype=torch.complex128, device=dev)
    assert (u.conj().T @ u - eye).abs().max().item() < 1e-12
    w = Q.haar_isometry_t(256, 16, gen)
    assert (w.conj().T @ w - eye[:16, :16]).abs().max().item() < 1e-12
    # spectrum of a mixed state preserved under conjugation
    a = Q.ginibre_t((128, 128), gen)
    rho = a @ a.conj().T
    rho = rho / torch.trace(rho).real
    e1 = torch.linalg.eigvalsh(rho)
    e2 = torch.linalg.eigvalsh(u @ rho @ u.conj().T)
    assert (e1 - e2).abs().max().item() < 1e-12
    # Haar check: E|tr U|^2 = 1 for d >= 2
    tr = torch.stack([torch.trace(Q.haar_unitary_t(8, gen)) for _ in range(3000)]).abs() ** 2
    assert abs(tr.mean().item() - 1.0) < 4 * tr.std().item() / math.sqrt(3000)


@needs_torch
@pytest.mark.parametrize("m,n,samples", [(2, 2, 200000), (4, 4, 100000), (8, 64, 20000), (32, 32, 8000), (64, 256, 2000),
                                         (256, 256, 400)])
def test_page_formula_vs_monte_carlo_torch(m, n, samples):
    dev = Q.torch_device()
    gen = Q.torch_generator(SEED + 31 * m + n, dev)
    chunks = []
    chunk = max(1, min(samples, 2**22 // (m * n)))
    done = 0
    while done < samples:
        c = min(chunk, samples - done)
        g = Q.ginibre_t((c, m, n), gen)  # unnormalised Haar state; schmidt_probs_t normalises
        chunks.append(E.von_neumann(Q.schmidt_probs_t(g)).cpu().numpy())
        done += c
    s = np.concatenate(chunks)
    se = s.std(ddof=1) / math.sqrt(samples)
    z = (s.mean() - P.page_entropy(m, n)) / se
    assert abs(z) < 4, (m, n, s.mean(), P.page_entropy(m, n), se, z)
