"""Explicit Hayden-Preskill recovery: Petz (transpose-channel) decoder, decoupling
and noise (Track C).  NEW module; it reuses eh.hayden_preskill for Haar formulas.

Subsystems (this module's naming; eh.hayden_preskill calls Q "R" and R "E"):
  Q  : reference, k qubits, maximally entangled with the message M
  M  : message ("diary"), k qubits = the FIRST k qubits of the scrambler input
  B  : black hole, n_B qubits (the last n_B input qubits)
  R  : early radiation. Old hole: R holds the purification of B (|Bell>_BR,
       n_B qubits). Young hole: B starts in |0..0> and R is trivial.
  U  : unitary on M+B, n = k + n_B qubits, U[out, in] (qubit 0 most significant)
  D  : new radiation = the LAST m output qubits;  B' = the first n - m outputs.
Bob holds X = (D, R).  The message channel is N: M -> D R,
  N(x) = Tr_B'[(U x 1_R)(x_M (x) |Bell><Bell|_BR)(U x 1_R)^dag].

Decoder: the Petz recovery map (transpose channel, Barnum-Knill 2002, J. Math.
Phys. 43, 2097) with reference state sigma_M = 1/d_M,
  P(Y) = sigma^1/2 N^dag(N(sigma)^-1/2 Y N(sigma)^-1/2) sigma^1/2,
with N(sigma)^-1/2 the inverse on its support. Its entanglement fidelity is
  F_Petz = <Phi_QM|(id x P o N)(Phi_QM)|Phi_QM>
         = (1/d_M) Tr[(rho_QX Omega)^2],  Omega = 1_Q x rho_X^{-1/2},
and, if the global state is pure with complement C (here C = B'),
         = (1/d_M) || Tr_Q sqrt(rho_QC) ||_F^2          (derived in g_recovery
notes; cross-checked against an explicit Kraus construction in the tests).
Barnum-Knill: F_Petz >= F_opt^2, so F_Petz <= F_opt <= sqrt(F_Petz), where F_opt
is the optimal entanglement fidelity of any decoder acting on X.
Uhlmann: F_opt >= F(rho_QB', tau_Q x rho_B') (a decoder exists achieving it).

Everything is exact dense linear algebra on small Hilbert spaces: a finite
circuit / random-matrix toy model. It contains no gravity.
"""
from __future__ import annotations

import numpy as np

from .circuits import haar_unitary, brickwork_unitary  # noqa: F401
from . import hayden_preskill as hp

EIG_CUT = 1e-12  # relative eigenvalue cutoff for pseudo-inverses


# ----------------------------------------------------------------------------
# states
# ----------------------------------------------------------------------------

def hp_tensor(U: np.ndarray, k: int, n_B: int, m: int, old: bool = True) -> np.ndarray:
    """Global pure state as a tensor Psi[q, b', d, r] (shape d_Q, d_B', d_D, d_R).
    Old:   Psi = <b' d| U |a=q, b=r> / sqrt(d_M d_B)
    Young: Psi = <b' d| U |a=q, b=0> / sqrt(d_M),  d_R = 1."""
    n = k + n_B
    dM, dB, dD, dBp = 2 ** k, 2 ** n_B, 2 ** m, 2 ** (n - m)
    assert U.shape == (2 ** n, 2 ** n) and 0 <= m <= n
    Ut = U.reshape(dBp, dD, dM, dB)
    if old:
        return Ut.transpose(2, 0, 1, 3) / np.sqrt(float(dM * dB))
    return Ut[..., 0].transpose(2, 0, 1)[..., None] / np.sqrt(float(dM))


def rho_QBp(Psi: np.ndarray) -> np.ndarray:
    dQ, dBp, dD, dR = Psi.shape
    A = Psi.reshape(dQ * dBp, dD * dR)
    return A @ A.conj().T


def rho_QX(Psi: np.ndarray) -> np.ndarray:
    """Reduced state on Q and Bob's X = (D, R), ordering (q, d, r)."""
    dQ, dBp, dD, dR = Psi.shape
    A = Psi.transpose(1, 0, 2, 3).reshape(dBp, dQ * dD * dR)
    return A.T @ A.conj()


# ----------------------------------------------------------------------------
# channels
# ----------------------------------------------------------------------------

def depolarize_qubits(rho: np.ndarray, n_qubits: int, which, p: float) -> np.ndarray:
    """Apply the single-qubit depolarizing channel x -> (1-p) x + p Tr(x) 1/2
    to each qubit in `which` of an n_qubits-qubit density matrix (qubit 0 most
    significant). p = 0 is the identity, p = 1 fully depolarizes."""
    if p == 0 or len(which) == 0:
        return rho
    t = rho.reshape((2,) * (2 * n_qubits))
    for i in which:
        tr = np.trace(t, axis1=i, axis2=n_qubits + i)  # removes axes i, n+i
        rep = np.expand_dims(np.expand_dims(tr, i), n_qubits + i)
        rep = np.broadcast_to(rep, t.shape) * np.eye(2).reshape(
            [2 if a in (i, n_qubits + i) else 1 for a in range(2 * n_qubits)]) / 2.0
        t = (1.0 - p) * t + p * rep
    return t.reshape(rho.shape)


def depolarizing_kraus(p: float) -> list[np.ndarray]:
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.diag([1.0 + 0j, -1.0])
    return [np.sqrt(1 - 3 * p / 4) * I] + [np.sqrt(p / 4) * P for P in (X, Y, Z)]


def hp_channel_kraus(U: np.ndarray, k: int, n_B: int, m: int, old: bool = True) -> np.ndarray:
    """Kraus operators of N: M -> X=(D,R), indexed by the B' basis.
    K[b'][(d, r), a] = sqrt(d_M) Psi[a, b', d, r]."""
    Psi = hp_tensor(U, k, n_B, m, old)
    dQ, dBp, dD, dR = Psi.shape
    return np.sqrt(dQ) * Psi.transpose(1, 2, 3, 0).reshape(dBp, dD * dR, dQ)


def apply_kraus(K: np.ndarray, x: np.ndarray) -> np.ndarray:
    return np.einsum("kia,ab,kjb->ij", K, x, K.conj())


def is_trace_preserving(K: np.ndarray, tol: float = 1e-10) -> bool:
    S = np.einsum("kia,kib->ab", K.conj(), K)
    return bool(np.allclose(S, np.eye(S.shape[0]), atol=tol))


def _inv_sqrt_psd(rho: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh(rho)
    cut = EIG_CUT * max(float(w.max()), 1e-300)
    s = np.where(w > cut, 1.0 / np.sqrt(np.where(w > cut, w, 1.0)), 0.0)
    return (v * s) @ v.conj().T


def _sqrt_psd(rho: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh(rho)
    return (v * np.sqrt(np.clip(w, 0.0, None))) @ v.conj().T


def petz_kraus(K: np.ndarray) -> np.ndarray:
    """Kraus operators of the Petz map (sigma = 1/d_M) for channel Kraus K,
    R_j = d_M^-1/2 K_j^dag N(sigma)^-1/2 (support-restricted)."""
    dM = K.shape[2]
    out = apply_kraus(K, np.eye(dM) / dM)
    Om = _inv_sqrt_psd(out)
    return np.einsum("kia,ij->kaj", K.conj(), Om) / np.sqrt(dM)


def entanglement_fidelity_kraus(A: np.ndarray) -> float:
    """F_e(1/d, channel with Kraus A) = sum_j |Tr A_j|^2 / d^2."""
    d = A.shape[1]
    return float(np.sum(np.abs(np.einsum("jaa->j", A)) ** 2) / d ** 2)


def petz_fidelity_explicit(K: np.ndarray) -> float:
    """Brute force: compose Petz Kraus with channel Kraus, then F_e."""
    R = petz_kraus(K)
    A = np.einsum("iax,jxb->ijab", R, K).reshape(-1, K.shape[2], K.shape[2])
    return entanglement_fidelity_kraus(A)


# ----------------------------------------------------------------------------
# fidelities
# ----------------------------------------------------------------------------

def petz_fidelity_pure(Psi: np.ndarray) -> float:
    """F_Petz = (1/d_M) || Tr_Q sqrt(rho_QB') ||_F^2 (global state pure)."""
    dQ, dBp = Psi.shape[:2]
    sq = _sqrt_psd(rho_QBp(Psi)).reshape(dQ, dBp, dQ, dBp)
    g = np.einsum("qiqj->ij", sq)
    return float(np.real(np.vdot(g, g)) / dQ)


def petz_fidelity_mixed(rhoQX: np.ndarray, dQ: int) -> float:
    """F_Petz = (1/d_Q) Tr[(rho_QX (1 x rho_X^-1/2))^2] for any Choi state."""
    dX = rhoQX.shape[0] // dQ
    t = rhoQX.reshape(dQ, dX, dQ, dX)
    rX = np.einsum("qiqj->ij", t)
    Om = _inv_sqrt_psd(rX)
    A = (rhoQX.reshape(dQ * dX * dQ, dX) @ Om).reshape(dQ * dX, dQ * dX)
    return float(np.real(np.sum(A * A.T)) / dQ)


def uhlmann_fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    s = _sqrt_psd(sigma)
    ev = np.linalg.eigvalsh(s @ rho @ s)
    return float(min(np.sqrt(np.clip(ev, 0.0, None)).sum() ** 2, 1.0))


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    return float(0.5 * np.abs(np.linalg.eigvalsh(rho - sigma)).sum())


def decoupling(Psi: np.ndarray) -> dict:
    """Decoupling of the reference Q from the remaining hole B'."""
    dQ, dBp = Psi.shape[:2]
    rho = rho_QBp(Psi)
    t = rho.reshape(dQ, dBp, dQ, dBp)
    rQ = np.einsum("aibi->ab", t)
    rB = np.einsum("aiaj->ij", t)
    prod = np.kron(rQ, rB)
    D = dQ * dBp
    return {
        "T_prod": trace_distance(rho, prod),
        "T_mm": trace_distance(rho, np.eye(D) / D),
        "F_uhl": uhlmann_fidelity(rho, np.kron(np.eye(dQ) / dQ, rB)),
        "purity_QBp": float(np.real(np.trace(rho @ rho))),
    }


def recovery_metrics(U, k, n_B, m, old=True, with_yk=True) -> dict:
    """Noiseless metrics for one unitary."""
    Psi = hp_tensor(U, k, n_B, m, old)
    out = {"F_petz": petz_fidelity_pure(Psi)}
    out.update(decoupling(Psi))
    if old and with_yk:
        out.update(hp.yoshida_kitaev(U, k, n_B, m))
    return out


def noisy_petz_fidelity(U, k, n_B, m, p, old=True, noise_on="D") -> float:
    """Petz fidelity when every qubit of the radiation is depolarized with
    strength p before decoding. noise_on: 'D' (new radiation only) or 'DR'
    (new and early radiation)."""
    Psi = hp_tensor(U, k, n_B, m, old)
    dR = Psi.shape[3]
    nR = int(round(np.log2(dR)))
    rho = rho_QX(Psi)
    nq = k + m + nR
    which = list(range(k, k + m))
    if noise_on == "DR":
        which += list(range(k + m, nq))
    rho = depolarize_qubits(rho, nq, which, p)
    return petz_fidelity_mixed(rho, 2 ** k)


def haar_bounds(k, n_B, m, old=True) -> dict:
    """Haar-average decoupling bound (exact second moment, eh.hayden_preskill)
    and its large-d limit."""
    out = {"T_mm_bound": hp.decoupling_bound_mm(k, n_B, m, old=old)}
    out["T_mm_bound_large_d"] = 0.5 * 2.0 ** (k - m) if old else 0.5 * 2.0 ** (k + n_B / 2 - m)
    if old:
        out["F_yk_pred"] = hp.yk_fidelity_prediction(k, n_B, m)
    return out
