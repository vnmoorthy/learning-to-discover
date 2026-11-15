"""Bell-pair "Hawking" toy model (independent pair creation, no unitarity constraint).

Model.  Each emission step creates a fresh Bell pair |Phi+> = (|00> + |11>)/sqrt(2):
the "outgoing" qubit joins the radiation R, the "partner" qubit stays behind (interior).
After k emissions the global state is |Phi+>^{(x) k}, a product over steps.

Exact result.  rho_R = Tr_partners |Phi+><Phi+|^{(x)k} = (I/2)^{(x)k} = I / 2^k, so
    S(R) = k log 2  exactly (and Renyi-2 = k log 2, purity = 2^-k),
monotonically increasing for all k.  If the black hole is assigned a coarse-grained
capacity of (N - k) qubits after k emissions (it loses one qubit of capacity per emission),
then S(R) = k log 2 > (N - k) log 2 = log dim(B) as soon as k > N/2: impossible for a pure
state on R (x) B with dim B = 2^(N-k), since S(R) = S(B) <= log dim B.  The toy model evades
the bound only because the partner Hilbert space (dimension 2^k) grows with every emission.
"""
from __future__ import annotations

import math

import numpy as np

LOG2 = math.log(2.0)


def hawking_entropy(k: int, bits: bool = False) -> float:
    """S(R) after k independent Bell-pair emissions: k log 2 (exact)."""
    return float(k) if bits else k * LOG2


def bh_capacity(N: int, k: int, bits: bool = False) -> float:
    """log dim of an (N-k)-qubit black hole: the maximal entropy it can hold."""
    return float(N - k) if bits else (N - k) * LOG2


def bell_pairs_state(k: int, xp=np, device=None):
    """|Phi+>^{(x)k} as a (2^k x 2^k) coefficient matrix M[r, p] over (radiation | partners).

    Radiation index r = (r_1..r_k), partner index p = (p_1..p_k); M = I / sqrt(2^k)
    because each pair contributes delta_{r_i p_i}/sqrt(2).  Built explicitly by Kronecker
    products (not by assuming the answer) so that it can be checked numerically.
    """
    if xp is np:
        pair = np.eye(2, dtype=np.complex128) / math.sqrt(2.0)
        m = np.ones((1, 1), dtype=np.complex128)
        for _ in range(k):
            m = np.kron(m, pair)
        return m
    import torch

    pair = torch.eye(2, dtype=torch.complex128, device=device) / math.sqrt(2.0)
    m = torch.ones((1, 1), dtype=torch.complex128, device=device)
    for _ in range(k):
        m = torch.kron(m, pair)
    return m


def bell_pairs_statevector(k: int) -> np.ndarray:
    """Flat state vector on 2k qubits in the interleaved order (r_1, p_1, r_2, p_2, ...)."""
    bell = np.zeros(4, dtype=np.complex128)
    bell[0] = bell[3] = 1 / math.sqrt(2.0)
    psi = np.ones(1, dtype=np.complex128)
    for _ in range(k):
        psi = np.kron(psi, bell)
    return psi
