"""Renyi entropies, trace moments and exact Haar moments (Upgrade track A).

Model class: finite-dimensional quantum information only (density matrices / Schmidt spectra).
Nothing here is a statement about gravity.

Definitions (natural logs, nats)
--------------------------------
    S_n(rho) = log Tr(rho^n) / (1 - n)            n > 0, n != 1
    S_1      = -Tr rho log rho                     (limit n -> 1, von Neumann)
    S_0      = log rank(rho)                       (Hartley; rank counts p > clip)
    S_inf    = -log lambda_max                     (min-entropy)
Monotonicity: S_n is non-increasing in n (S_0 >= S_1/2 >= S_1 >= S_2 >= S_3 >= S_inf), and
S_inf >= S_2 / 2 (since Tr rho^2 <= lambda_max).  All S_n coincide iff the nonzero spectrum is flat.
Capacity of entanglement C = Var_p(-log p) = sum p log^2 p - S_1^2 (= 0 iff flat spectrum).

Exact Haar trace moments
------------------------
For |psi> Haar on C^m (x) C^n, rho = Tr_B |psi><psi| = W / Tr W with W = G G^dag, G an m x n
complex Ginibre matrix; Tr W is independent of rho, E(Tr W)^k = mn(mn+1)...(mn+k-1), and the
complex-Wishart moments are  E Tr W^k = sum_{sigma in S_k} m^{#(sigma)} n^{#(sigma^-1 gamma)}.
Hence
    E Tr rho^2 = (m + n) / (mn + 1)                                          (Lubkin 1978)
    E Tr rho^3 = (m^2 + 3mn + n^2 + 1) / ((mn+1)(mn+2))
    E Tr rho^4 = (m^3 + 6m^2 n + 6mn^2 + n^3 + 5m + 5n) / ((mn+1)(mn+2)(mn+3))
The k-th moment is a degree-(k,k) polynomial in (psi, psi*), so ANY ensemble that is a state
k-design (e.g. Clifford orbits of |0>, which form a 3-design) reproduces the first k of these.
"""
from __future__ import annotations

import math
from itertools import permutations

import numpy as np

CLIP = 1e-15
NS_DEFAULT = (0.5, 1.0, 2.0, 3.0, math.inf)


def _probs(p, clip=CLIP):
    p = np.asarray(p, dtype=float)
    return np.where(p > clip, p, 0.0)


def trace_moment(p, k: float, clip: float = CLIP):
    """Tr rho^k = sum_i p_i^k over the last axis (entries <= clip dropped)."""
    q = _probs(p, clip)
    if k == 0:
        return (q > 0).sum(axis=-1)
    return (q ** k).sum(axis=-1)


def renyi(p, n: float, clip: float = CLIP):
    """Renyi-n entropy of a spectrum p (last axis); n in [0, inf]."""
    q = _probs(p, clip)
    if n == 0:
        return np.log((q > 0).sum(axis=-1).astype(float))
    if n == 1:
        safe = np.where(q > 0, q, 1.0)
        return -(safe * np.log(safe)).sum(axis=-1)
    if math.isinf(n):
        return -np.log(q.max(axis=-1))
    return np.log((q ** n).sum(axis=-1)) / (1.0 - n)


def renyi_profile(p, ns=NS_DEFAULT, clip: float = CLIP) -> dict:
    """{n: S_n} for several n."""
    return {n: renyi(p, n, clip) for n in ns}


def capacity(p, clip: float = CLIP):
    """Capacity of entanglement C = sum p log^2 p - (sum p log p)^2 (variance of -log p)."""
    q = _probs(p, clip)
    safe = np.where(q > 0, q, 1.0)
    lg = np.log(safe)
    s1 = -(q * lg).sum(axis=-1)
    return (q * lg * lg).sum(axis=-1) - s1 * s1


def spectrum_of(rho):
    """Eigenvalues (ascending) of a Hermitian density matrix."""
    return np.linalg.eigvalsh(np.asarray(rho))


def renyi_of_density(rho, n: float, clip: float = CLIP):
    return renyi(np.clip(spectrum_of(rho), 0.0, None), n, clip)


# ----------------------------------------------------------------------------- exact Haar moments
def _cycles(perm) -> int:
    seen, c = [False] * len(perm), 0
    for i in range(len(perm)):
        if not seen[i]:
            c += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return c


def wishart_moment(k: int, m: int, n: int) -> int:
    """E Tr (G G^dag)^k for an m x n complex Ginibre G (entries CN(0,1)), by the permutation sum
    over S_k (exact integer; k <= 7 is cheap)."""
    gamma = tuple((i + 1) % k for i in range(k))
    tot = 0
    for s in permutations(range(k)):
        inv = [0] * k
        for i, si in enumerate(s):
            inv[si] = i
        comp = tuple(inv[gamma[i]] for i in range(k))
        tot += m ** _cycles(s) * n ** _cycles(comp)
    return tot


def haar_trace_moment(k: int, m: int, n: int) -> float:
    """Exact Haar average E Tr rho_A^k for a random pure state on C^m (x) C^n (any k >= 1)."""
    d = m * n
    rising = 1
    for j in range(k):
        rising *= d + j
    return wishart_moment(k, m, n) / rising


def lubkin_purity(m: int, n: int) -> float:
    """E Tr rho_A^2 = (m + n) / (mn + 1)  (Lubkin, J. Math. Phys. 19, 1028 (1978))."""
    return (m + n) / (m * n + 1.0)


def haar_moment3_closed(m: int, n: int) -> float:
    return (m * m + 3 * m * n + n * n + 1) / ((m * n + 1.0) * (m * n + 2.0))


def haar_moment4_closed(m: int, n: int) -> float:
    return (m**3 + 6 * m * m * n + 6 * m * n * n + n**3 + 5 * m + 5 * n) / (
        (m * n + 1.0) * (m * n + 2.0) * (m * n + 3.0))


def annealed_renyi(k: int, m: int, n: int) -> float:
    """-log E Tr rho^k / (k-1): the 'annealed' Renyi-k entropy of the Haar ensemble (exact).
    By Jensen (-log is convex), E S_k >= annealed value for k > 1."""
    return math.log(haar_trace_moment(k, m, n)) / (1.0 - k)
