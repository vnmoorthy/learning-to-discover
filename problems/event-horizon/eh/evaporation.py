"""Sequential unitary evaporation toy model (Problem C).  numpy only.

State: matrix M of shape (2^k, 2^(N-k)); rows = radiation R (k emitted qubits, in emission
order), columns = remaining black hole B.
Step k -> k+1:
  1. apply a scrambling unitary U to B only:   M <- M U^T
  2. move the first qubit of B to R:           reshape (2^k,2,2^(N-k-1)) -> (2^(k+1), 2^(N-k-1))

This module only depends on eh.entropy (von_neumann, purity) and eh.qstates.haar_unitary.
"""
from __future__ import annotations
import time
import numpy as np
from . import qstates as qs
from .entropy import von_neumann, purity


def ginibre(rng, rows, cols=None):
    """Complex Ginibre matrix, entries CN(0,1)."""
    cols = rows if cols is None else cols
    return (rng.standard_normal((rows, cols)) + 1j * rng.standard_normal((rows, cols))) / np.sqrt(2.0)


def haar_apply(rng, x):
    """Return U @ x for a Haar-random unitary U (dim = x.shape[0]) WITHOUT forming U:
    Householder QR of a Ginibre matrix (LAPACK zgeqrf), then U x = Q (Lambda x) with
    Lambda = diag(R_ii/|R_ii|) (Mezzadri 2007 phase fix), Q applied through zunmqr.
    Consumes the same random numbers and yields the same U as
    eh.qstates.haar_unitary(dim, rng) (tested in tests/test_evaporation.py), ~3-4x faster."""
    from scipy.linalg import lapack, qr
    x = np.asarray(x, dtype=complex)
    vec = x.ndim == 1
    if vec:
        x = x[:, None]
    z = ginibre(rng, x.shape[0])
    (a, tau), r = qr(z, mode="raw", check_finite=False, overwrite_a=True)
    d = np.diagonal(r)
    c = np.asfortranarray((d / np.abs(d))[:, None] * x)
    _, work, info = lapack.zunmqr("L", "N", a, tau, c, -1)
    out, work, info = lapack.zunmqr("L", "N", a, tau, c, int(work[0].real), overwrite_c=1)
    if info != 0:
        raise RuntimeError("zunmqr failed")
    return out[:, 0] if vec else out


def _scramble_haar(M, rng):
    # M U^T = (U M^T)^T, U Haar on the 2^(N-k)-dim black hole factor
    return haar_apply(rng, M.T).T


def _scramble_brickwork(M, rng, nb, offset):
    """CONTROL (not Haar on the whole hole): one layer of independent Haar 2-qubit gates on
    neighbouring pairs (offset, offset+1), (offset+2, offset+3), ... of the remaining hole."""
    k_dim = M.shape[0]
    t = M.reshape((k_dim,) + (2,) * nb)
    for a in range(offset, nb - 1, 2):
        g = qs.haar_unitary(4, rng).reshape(2, 2, 2, 2)
        t = np.moveaxis(np.tensordot(t, g, axes=([1 + a, 2 + a], [2, 3])), [-2, -1], [1 + a, 2 + a])
    return t.reshape(k_dim, 2 ** nb)


def run_trajectory(N, rng, init="zero", scrambler="haar", check_B=True, keep_spectra=True):
    """One evaporation history.  Returns dict of per-step lists (k = 0..N).
    S_R from eigvalsh(M M^dag); S_B independently from eigvalsh(M^T M^*)."""
    if init == "zero":
        psi = np.zeros(2 ** N, dtype=complex)
        psi[0] = 1.0
    elif init == "random":
        psi = qs.haar_state(2 ** N, rng)
    else:
        raise ValueError(init)
    M = psi.reshape(1, 2 ** N)
    out = {"k": list(range(N + 1)), "dim_R": [1], "dim_B": [2 ** N], "S_R": [0.0], "S_B": [0.0],
           "purity_R": [1.0], "spectra": [[1.0]], "step_seconds": [0.0], "norm": [1.0]}
    for k in range(N):
        t0 = time.perf_counter()
        nb = N - k
        if scrambler == "haar":
            M = _scramble_haar(M, rng)
        elif scrambler == "brickwork":
            M = _scramble_brickwork(M, rng, nb, k % 2)
        else:
            raise ValueError(scrambler)
        M = np.ascontiguousarray(M).reshape(2 ** (k + 1), 2 ** (nb - 1))
        dR, dB = M.shape
        pR = np.linalg.eigvalsh(M @ M.conj().T)[::-1]
        out["S_R"].append(float(von_neumann(pR)))
        out["purity_R"].append(float(purity(pR)))
        out["S_B"].append(float(von_neumann(np.linalg.eigvalsh(M.T @ M.conj()))) if check_B else float("nan"))
        out["norm"].append(float(pR.sum()))
        out["dim_R"].append(dR)
        out["dim_B"].append(dB)
        out["spectra"].append(pR[: min(dR, dB)].tolist() if keep_spectra else None)
        out["step_seconds"].append(time.perf_counter() - t0)
    return out


def nested_cut_spectra(psi, N):
    """Spectra of rho_{first k qubits}, k = 0..N, of ONE state (reference ensemble for C)."""
    return [np.linalg.svd(psi.reshape(2 ** k, 2 ** (N - k)), compute_uv=False) ** 2 for k in range(N + 1)]
