"""Hayden-Preskill recovery in a finite-dimensional toy model (Extension 2).

Setup (Hayden & Preskill 2007, JHEP 0709:120):
  R  : reference, k qubits, maximally entangled with the diary A (k qubits)
  B  : black hole, n_B qubits
  E  : early radiation. "Old" black hole: B maximally entangled with E
       (n_B qubits). "Young" black hole: B in the pure state |0..0>, no E.
  U  : scrambling unitary on A+B (n = k + n_B qubits; A = first k qubits)
  D  : the LAST m qubits of the output (new radiation); B' = first n-m qubits.

The global pure state is stored as a tensor T[b', d, r, e] of shape
(d_B', d_D, d_R, d_E) with d_E = 1 for a young black hole.
For an old black hole  T = U / sqrt(d)  (the Choi state of U), d = 2^(k+n_B).

This is a toy model of unitary scrambling + entanglement; it contains no
gravity and says nothing by itself about semiclassical islands.
Entropies in nats; eigenvalues <= P_CLIP are dropped (0 log 0 := 0).
"""
from __future__ import annotations

import numpy as np

from .circuits import haar_unitary, brickwork_unitary, P_CLIP, LOG2  # noqa: F401

AXES = {"Bp": 0, "D": 1, "R": 2, "E": 3}


# ----------------------------------------------------------------------------
# state construction
# ----------------------------------------------------------------------------

def hp_state_old(U: np.ndarray, k: int, n_B: int, m: int) -> np.ndarray:
    """Old black hole: |Psi> = (U_AB x 1_RE) |Bell>_RA |Bell>_BE.
    Amplitude <b' d, r, e|Psi> = U[(b' d), (a=r, b=e)] / sqrt(d)."""
    n = k + n_B
    assert U.shape == (2 ** n, 2 ** n) and 0 <= m <= n
    return U.reshape(2 ** (n - m), 2 ** m, 2 ** k, 2 ** n_B) / np.sqrt(2.0 ** n)


def hp_state_young(V: np.ndarray, k: int, n_B: int, m: int) -> np.ndarray:
    """Young black hole: |Psi> = (U_AB x 1_R) |Bell>_RA |0..0>_B.
    V is the 2^n x 2^k isometry U[:, (a, b=0)] (columns a = 0..2^k-1)."""
    n = k + n_B
    assert V.shape == (2 ** n, 2 ** k)
    return V.reshape(2 ** (n - m), 2 ** m, 2 ** k, 1) / np.sqrt(2.0 ** k)


def haar_isometry(d: int, r: int, rng: np.random.Generator) -> np.ndarray:
    """First r columns of a Haar d x d unitary (QR of a d x r Ginibre matrix)."""
    z = (rng.standard_normal((d, r)) + 1j * rng.standard_normal((d, r))) / np.sqrt(2)
    q, rr = np.linalg.qr(z)
    ph = np.diagonal(rr) / np.abs(np.diagonal(rr))
    return q * ph


def young_isometry_from_unitary(U: np.ndarray, k: int, n_B: int) -> np.ndarray:
    """Columns of U with the black hole input in |0..0>."""
    n = k + n_B
    return U.reshape(2 ** n, 2 ** k, 2 ** n_B)[:, :, 0]


# ----------------------------------------------------------------------------
# entropies
# ----------------------------------------------------------------------------

def _vn(p):
    p = np.asarray(p, dtype=float)
    p = p[p > P_CLIP]
    return float(-(p * np.log(p)).sum())


def subsystem_probs(T: np.ndarray, keep: tuple[str, ...]) -> np.ndarray:
    """Spectrum of the reduced state on the named subsystems (SVD of keep|rest)."""
    ka = [AXES[x] for x in keep]
    ra = [a for a in range(4) if a not in ka]
    dk = int(np.prod([T.shape[a] for a in ka])) if ka else 1
    M = T.transpose(ka + ra).reshape(dk, -1)
    s = np.linalg.svd(M, compute_uv=False)
    return s ** 2


def S(T, keep) -> float:
    return _vn(subsystem_probs(T, tuple(keep)))


def mutual_information(T, X: tuple[str, ...], Y: tuple[str, ...]) -> float:
    return S(T, X) + S(T, Y) - S(T, tuple(X) + tuple(Y))


def reduced_density_matrix(T, keep) -> np.ndarray:
    ka = [AXES[x] for x in keep]
    ra = [a for a in range(4) if a not in ka]
    dk = int(np.prod([T.shape[a] for a in ka]))
    M = T.transpose(ka + ra).reshape(dk, -1)
    return M @ M.conj().T


# ----------------------------------------------------------------------------
# decoupling and recovery
# ----------------------------------------------------------------------------

def decoupling_metrics(T, max_dim: int = 1024) -> dict:
    """Trace distances and the Uhlmann fidelity lower bound on optimal recovery.

    T_prod = 1/2 || rho_RB' - rho_R x rho_B' ||_1
    T_mm   = 1/2 || rho_RB' - 1/(d_R d_B') ||_1
    F_uhl  = F(rho_RB', rho_R x rho_B') = (tr sqrt(sqrt(s) rho sqrt(s)))^2.
    By Uhlmann's theorem there is a decoder acting only on Bob's systems
    (E D) that produces a state with fidelity >= F_uhl with |Bell>_{R R'}
    (it is a lower bound on the optimal entanglement fidelity).
    Returns NaNs if d_R d_B' > max_dim (dense eigendecomposition too large)."""
    dBp, dD, dR, dE = T.shape
    dim = dR * dBp
    if dim > max_dim:
        return {"T_prod": float("nan"), "T_mm": float("nan"), "F_uhl": float("nan")}
    rho = reduced_density_matrix(T, ("R", "Bp"))
    rho_R = reduced_density_matrix(T, ("R",))
    rho_B = reduced_density_matrix(T, ("Bp",))
    sigma = np.kron(rho_R, rho_B)
    t_prod = 0.5 * np.abs(np.linalg.eigvalsh(rho - sigma)).sum()
    t_mm = 0.5 * np.abs(np.linalg.eigvalsh(rho - np.eye(dim) / dim)).sum()
    w, v = np.linalg.eigh(sigma)
    w = np.clip(w, 0.0, None)
    sq = (v * np.sqrt(w)) @ v.conj().T
    ev = np.linalg.eigvalsh(sq @ rho @ sq)
    f = float(np.sqrt(np.clip(ev, 0.0, None)).sum() ** 2)
    return {"T_prod": float(t_prod), "T_mm": float(t_mm), "F_uhl": min(f, 1.0)}


def yoshida_kitaev(U: np.ndarray, k: int, n_B: int, m: int) -> dict:
    """Yoshida-Kitaev probabilistic decoder (old black hole), computed from the
    explicit post-projection amplitude.

    Bob prepares |Bell>_{A'R'}, applies U* to (A', E), and projects D D' onto
    |Bell>_{DD'}. With Ut[b', d, a, b] = U reshaped:
       Phi[r, b', b'', r'] = sum_{b,d} Ut[b',d,r,b] conj(Ut[b'',d,r',b])
                             / (d_A sqrt(d_B d_D))
    P_EPR = ||Phi||^2 (success probability), F_EPR = |<Bell_RR'|Phi>|^2 / P_EPR.
    Identities (tested): P_EPR * F_EPR = 1/d_A^2 and
    P_EPR = (d_B/d_D) tr(rho_RB'^2)."""
    n = k + n_B
    dA, dB, dD, dBp = 2 ** k, 2 ** n_B, 2 ** m, 2 ** (n - m)
    Ut = U.reshape(dBp, dD, dA, dB)
    # Phi = G / (d_A sqrt(d_B d_D)) with G = M M^dag, M[(b', r), (d, b)].
    # ||G||_F^2 = ||M^dag M||_F^2, so use the smaller Gram matrix.
    M = Ut.transpose(0, 2, 1, 3).reshape(dBp * dA, dD * dB)
    G_small = M @ M.conj().T if M.shape[0] <= M.shape[1] else M.conj().T @ M
    P = float(np.real(np.vdot(G_small, G_small))) / (dA ** 2 * dB * dD)
    # <Bell_RR'|Phi>[b', b''] = sum_r Phi[r, b', b'', r] / sqrt(d_A) = (N N^dag) / (d_A^1.5 sqrt(d_B d_D))
    N = Ut.reshape(dBp, dD * dA * dB)
    proj = (N @ N.conj().T) / (dA ** 1.5 * np.sqrt(dB * dD))
    F = float(np.real(np.vdot(proj, proj))) / P
    return {"P_EPR": P, "F_EPR": F}


def yoshida_kitaev_statevector(U: np.ndarray, k: int, n_B: int, m: int) -> dict:
    """Brute-force state-vector simulation of the same decoder, for tests.
    Systems (in order): R, A, B, E, A', R'  ->  apply U on (A,B) and U* on
    (A',E), project D D' on Bell pairs, measure overlap with |Bell>_{RR'}.
    Memory ~ 2^(4k+2n_B) amplitudes; use only for small sizes."""
    n = k + n_B
    dA, dB, dD, dBp = 2 ** k, 2 ** n_B, 2 ** m, 2 ** (n - m)
    bellA = np.eye(dA) / np.sqrt(dA)
    bellB = np.eye(dB) / np.sqrt(dB)
    # psi[r, a, b, e, a', r']
    psi = np.einsum("ra,be,sp->rabesp", bellA, bellB, bellA).astype(complex)
    Ut = U.reshape(dBp, dD, dA, dB)
    # U on (a, b) -> (x, d)
    psi = np.einsum("xdab,rabesp->rxdesp", Ut, psi)
    # U* on (a'=s, e) -> (y, f), with the same (A-like, B-like) input ordering
    psi = np.einsum("yfse,rxdesp->rxdyfp", Ut.conj(), psi)
    norm = float(np.real(np.vdot(psi, psi)))
    # project D D' onto Bell
    phi = np.einsum("rxdydp->rxyp", psi) / np.sqrt(dD)
    P = float(np.real(np.vdot(phi, phi)))
    proj = np.einsum("rxyr->xy", phi) / np.sqrt(dA)
    F = float(np.real(np.vdot(proj, proj))) / P
    return {"P_EPR": P, "F_EPR": F, "norm_before_projection": norm}


# ----------------------------------------------------------------------------
# analytic (Haar-averaged) predictions
# ----------------------------------------------------------------------------

def haar_mean_purity_RBp_old(k: int, n_B: int, m: int) -> float:
    """Exact Haar average of tr(rho_RB'^2) for the old black hole, from the
    second-moment Weingarten calculus (d = d_D d_B' = d_R d_E):
      E P = [d_B' d_R + d_D d_E - (d_B' d_E + d_D d_R)/d] / (d^2 - 1)."""
    n = k + n_B
    d, dR, dE, dD, dBp = 2.0 ** n, 2.0 ** k, 2.0 ** n_B, 2.0 ** m, 2.0 ** (n - m)
    return (dBp * dR + dD * dE - (dBp * dE + dD * dR) / d) / (d * d - 1.0)


def haar_mean_purity_RBp_young(k: int, n_B: int, m: int) -> float:
    """Exact Haar average of tr(rho_RB'^2) for the young black hole (state
    V/sqrt(d_R), V the b=0 columns of a Haar U), from the second-moment
    Weingarten calculus (Monte-Carlo checked in tests). It is close to, but
    not equal to, Lubkin's (d_R d_B' + d_D)/(d_R d + 1) for a Haar-random
    state on (R B') x D, because here rho_R is exactly maximally mixed."""
    n = k + n_B
    d, dR, dD, dBp = 2.0 ** n, 2.0 ** k, 2.0 ** m, 2.0 ** (n - m)
    # output contractions: sigma=e -> d_D d_B'^2, sigma=swap -> d_D^2 d_B'
    # input contractions (R only, purity taken on R): tau=e -> d_R^2, tau=swap -> d_R
    wg_e, wg_s = 1.0 / (d * d - 1.0), -1.0 / (d * (d * d - 1.0))
    tot = (dD * dBp ** 2) * (dR ** 2) * wg_e + (dD ** 2 * dBp) * dR * wg_e \
        + (dD * dBp ** 2) * dR * wg_s + (dD ** 2 * dBp) * (dR ** 2) * wg_s
    return tot / dR ** 2


def decoupling_bound_mm(k: int, n_B: int, m: int, old: bool = True) -> float:
    """Upper bound on the Haar average of T_mm = 1/2||rho_RB' - 1/D||_1:
    E T_mm <= 1/2 sqrt(D E[P] - 1), D = d_R d_B' (Cauchy-Schwarz + Jensen).
    Old black hole, large d:  -> 1/2 * 2^(k-m), independent of n_B.
    Young black hole, large d: -> 1/2 * 2^(k + n_B/2 - m)."""
    n = k + n_B
    D = 2.0 ** k * 2.0 ** (n - m)
    P = haar_mean_purity_RBp_old(k, n_B, m) if old else haar_mean_purity_RBp_young(k, n_B, m)
    return 0.5 * float(np.sqrt(max(D * P - 1.0, 0.0)))


def yk_fidelity_prediction(k: int, n_B: int, m: int) -> float:
    """F_EPR with tr(rho_RB'^2) replaced by its exact Haar mean (an
    approximation to E[F]: it is 1/E[1/F]). Large d: 1/(1 + 4^(k-m) - 4^-m)."""
    dA, dB, dD = 2.0 ** k, 2.0 ** n_B, 2.0 ** m
    return dD / (dA ** 2 * dB * haar_mean_purity_RBp_old(k, n_B, m))


def yk_fidelity_large_d(k: int, m: int) -> float:
    return 1.0 / (1.0 + 4.0 ** (k - m) - 4.0 ** (-m))


# ----------------------------------------------------------------------------
# one-call analysis
# ----------------------------------------------------------------------------

def analyze(T, k: int, with_decoupling: bool = True, max_dim: int = 1024) -> dict:
    """All information-theoretic quantities for one HP state tensor."""
    Bob = ("E", "D")
    out = {
        "I_R_Bp": mutual_information(T, ("R",), ("Bp",)),
        "I_R_ED": mutual_information(T, ("R",), Bob),
        "S_R": S(T, ("R",)),
        "S_Bp": S(T, ("Bp",)),
        "S_RBp": S(T, ("R", "Bp")),
        "purity_RBp": float((subsystem_probs(T, ("R", "Bp")) ** 2).sum()),
    }
    if with_decoupling:
        out.update(decoupling_metrics(T, max_dim=max_dim))
    return out


# ============================================================================
# torch / GPU backend.  Everything is computed from entanglement spectra.
# ============================================================================
# Old black hole, U exactly unitary:  rho_R = 1/d_R and rho_B' = 1/d_B'
# EXACTLY (B'D is maximally mixed because U/sqrt(d) is a Choi state), so
#   rho_R x rho_B' = 1/D,  D = d_R d_B',
# and with p_i the nonzero eigenvalues of rho_RB' (rank r <= min(D, d_E d_D)):
#   T      = 1/2 ||rho_RB' - 1/D||_1 = 1/2 [ sum_i |p_i - 1/D| + (D - r)/D ]
#   F_uhl  = F(rho_RB', 1/D)         = (sum_i sqrt(p_i))^2 / D
#   I(R:B') = log D - S(RB'),   I(R:ED) = 2 k log 2 - I(R:B')
#   Yoshida-Kitaev: P_EPR = (d_B/d_D) sum p_i^2,  F_EPR = 1/(d_A^2 P_EPR)
# so no dense D x D matrix is ever needed and sizes are limited only by the
# 2^n x 2^n unitary (n = k + n_B; the global state has 2n qubits).
HP_CLIP = 1e-13


def _t_gram_spectrum(M):
    """Nonzero-side spectrum of M M^dag via the smaller Gram matrix; (r,) desc."""
    import torch
    if M.shape[0] <= M.shape[1]:
        G = M @ M.conj().T
    else:
        G = M.conj().T @ M
    from .circuits import robust_eigvalsh
    p = robust_eigvalsh(G).clamp_min(0.0)
    return torch.flip(p, dims=[0])


def _t_vn(p):
    import torch
    safe = torch.where(p > HP_CLIP, p, torch.ones_like(p))
    return float(-(torch.where(p > HP_CLIP, p, torch.zeros_like(p)) * torch.log(safe)).sum())


def _t_gram_spectrum_batch(M):
    """Batched (S, a, b) -> spectra (S, min(a, b)) descending, via the smaller Gram matrix."""
    import torch
    from .circuits import robust_eigvalsh
    if M.shape[1] <= M.shape[2]:
        G = M @ M.conj().transpose(1, 2)
    else:
        G = M.conj().transpose(1, 2) @ M
    return torch.flip(robust_eigvalsh(G).clamp_min(0.0), dims=[1])


def _t_vn_batch(p):
    import torch
    safe = torch.where(p > HP_CLIP, p, torch.ones_like(p))
    return -(torch.where(p > HP_CLIP, p, torch.zeros_like(p)) * torch.log(safe)).sum(dim=1)


OLD_FIELDS = ("trace", "S_RBp", "I_R_Bp", "I_R_ED", "purity_RBp", "T_prod", "F_uhl", "P_EPR", "F_EPR")
YOUNG_FIELDS = ("I_R_Bp", "I_R_D", "S_Bp", "S_D", "purity_RBp", "T_prod", "F_uhl", "T_mm")


def t_old_metrics_batch(U, k: int, n_B: int, m: int) -> dict:
    """Old-black-hole quantities for a batch of unitaries U: (S, 2^n, 2^n),
    from the spectrum of rho_RB' (see block comment). Returns numpy arrays (S,).
    One device->host transfer per call (cheap on a shared GPU)."""
    import torch
    from .circuits import to_np
    n = k + n_B
    S_ = U.shape[0]
    dBp, dD, dA, dB = 2 ** (n - m), 2 ** m, 2 ** k, 2 ** n_B
    M = U.reshape(S_, dBp, dD, dA, dB).permute(0, 1, 3, 2, 4).reshape(S_, dBp * dA, dD * dB) / np.sqrt(2.0 ** n)
    p = _t_gram_spectrum_batch(M)
    del M
    D = float(dBp * dA)
    r = p.shape[1]
    s_rbp = _t_vn_batch(p)
    i_rbp = np.log(D) - s_rbp
    purity = (p ** 2).sum(dim=1)
    T = 0.5 * ((p - 1.0 / D).abs().sum(dim=1) + (D - r) / D)
    F = (torch.sqrt(p).sum(dim=1) ** 2 / D).clamp_max(1.0)
    P_epr = (dB / dD) * purity
    vals = torch.stack([p.sum(dim=1), s_rbp, i_rbp, 2 * k * LOG2 - i_rbp, purity, T, F, P_epr,
                        1.0 / (dA ** 2 * P_epr)], dim=1)
    a = to_np(vals)
    return {f: a[:, i] for i, f in enumerate(OLD_FIELDS)}


def t_old_metrics(U, k: int, n_B: int, m: int) -> dict:
    """Single-unitary convenience wrapper around t_old_metrics_batch."""
    return {f: float(v[0]) for f, v in t_old_metrics_batch(U.unsqueeze(0), k, n_B, m).items()}


def t_young_metrics_batch(V, k: int, n_B: int, m: int, dense_max: int = 256) -> dict:
    """Young black hole (B starts in |0..0>, no early radiation; Bob holds only
    D). V: torch (S, 2^n, 2^k) isometries. rho_R = 1/d_R exactly; rho_B' is NOT
    maximally mixed, so the trace distance to rho_R x rho_B' needs dense
    d_R d_B' matrices and is only computed when that is <= dense_max.
    T_mm = 1/2||rho_RB' - 1/(d_R d_B')||_1 is exact from the spectrum for all
    m (and T_prod <= 2 T_mm by monotonicity + triangle inequality)."""
    import torch
    from .circuits import to_np, robust_eigvalsh
    n = k + n_B
    S_ = V.shape[0]
    dBp, dD, dR = 2 ** (n - m), 2 ** m, 2 ** k
    T3 = V.reshape(S_, dBp, dD, dR) / np.sqrt(float(dR))
    pB = _t_gram_spectrum_batch(T3.reshape(S_, dBp, dD * dR))
    pD = _t_gram_spectrum_batch(T3.permute(0, 2, 1, 3).reshape(S_, dD, dBp * dR))   # = spec(rho_RB')
    s_b, s_d = _t_vn_batch(pB), _t_vn_batch(pD)
    nan = torch.full_like(s_b, float("nan"))
    t_prod, f_uhl = nan, nan
    D = dR * dBp
    if D <= dense_max:
        tp, fu = [], []
        chunk = max(1, int(3e9 // (96 * D * D)))
        eye = torch.eye(dR, dtype=T3.dtype, device=T3.device) / dR
        for a0 in range(0, S_, chunk):
            Tc = T3[a0:a0 + chunk]
            Mx = Tc.permute(0, 3, 1, 2).reshape(-1, D, dD)             # [(r, b'), d]
            rho = Mx @ Mx.conj().transpose(1, 2)
            Mb = Tc.reshape(-1, dBp, dD * dR)
            rho_B = Mb @ Mb.conj().transpose(1, 2)
            sigma = torch.einsum("rq,sbc->srbqc", eye, rho_B).reshape(-1, D, D)
            tp.append(0.5 * robust_eigvalsh(rho - sigma).abs().sum(dim=1))
            try:
                w, v = torch.linalg.eigh(sigma)
            except Exception:
                w, v = torch.linalg.eigh(sigma.cpu()); w, v = w.to(rho.device), v.to(rho.device)
            sq = (v * torch.sqrt(w.clamp_min(0.0)).unsqueeze(1)) @ v.conj().transpose(1, 2)
            ev = robust_eigvalsh(sq @ rho @ sq).clamp_min(0.0)
            fu.append((torch.sqrt(ev).sum(dim=1) ** 2).clamp_max(1.0))
        t_prod, f_uhl = torch.cat(tp), torch.cat(fu)
    s_r = k * LOG2
    t_mm = 0.5 * ((pD - 1.0 / D).abs().sum(dim=1) + max(D - pD.shape[1], 0) / float(D))
    vals = torch.stack([s_r + s_b - s_d, s_r + s_d - s_b, s_b, s_d, (pD ** 2).sum(dim=1), t_prod, f_uhl, t_mm], dim=1)
    a = to_np(vals)
    return {f: a[:, i] for i, f in enumerate(YOUNG_FIELDS)}


def t_young_metrics(V, k: int, n_B: int, m: int, dense_max: int = 2048) -> dict:
    return {f: float(v[0]) for f, v in t_young_metrics_batch(V.unsqueeze(0), k, n_B, m, dense_max).items()}


def t_haar_isometry(d: int, r: int, seed: int, device=None):
    """First r columns of a Haar d x d unitary, on the device."""
    import torch
    from .circuits import get_device
    device = device or get_device()
    g = torch.Generator(device=device); g.manual_seed(int(seed))
    z = torch.view_as_complex(torch.randn(d, r, 2, generator=g, device=device, dtype=torch.float64))
    q, rr = torch.linalg.qr(z)
    dg = torch.diagonal(rr)
    return q * (dg / dg.abs()).unsqueeze(0)


def t_brickwork_columns(n: int, depth: int, rng, gate: str, n_cols_qubits: int, device=None, batch: int = None):
    """Columns of depth-`depth` brickwork circuits on n qubits (open chain):
    U restricted to inputs whose LAST (n - n_cols_qubits) qubits are |0>,
    shape (2^n, 2^n_cols_qubits); column index = value of the first
    n_cols_qubits input qubits.  n_cols_qubits = n gives the full unitary.
    batch=None -> one circuit, 2-D result; batch=S -> S independent circuits
    (gates drawn from rng for the whole batch per layer), shape (S, 2^n, cols)."""
    import torch
    from .circuits import get_device, t_brick_layer
    device = device or get_device()
    S_ = batch or 1
    c = 2 ** n_cols_qubits
    st = torch.zeros(S_, 2 ** n, c, dtype=torch.complex128, device=device)
    idx = torch.arange(c, device=device)
    st[:, idx * 2 ** (n - n_cols_qubits), idx] = 1.0
    for layer in range(depth):
        st = t_brick_layer(st, n, layer, rng, gate, n)
    return st if batch else st[0]
