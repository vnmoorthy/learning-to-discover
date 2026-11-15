"""Track E: black holes as quantum error-correcting codes (finite-dimensional toy models).

One logical qubit, maximally entangled with a reference R, is encoded into n physical qubits by
  (a) the [[5,1,3]] perfect code (Laflamme-Miquel-Paz-Zurek 1996; Bennett-DiVincenzo-Smolin-Wootters 1996),
  (b) random stabilizer codes  (encoder = random Clifford circuit on |l>|0...0>),
  (c) Haar-random isometries   (V = first two columns of a Haar unitary).
A subset E of the physical qubits is erased; we ask whether the logical qubit can be recovered from
the complement A.  Exact quantities (nats unless *_bits):
  I(R:A) = S(R) + S(A) - S(RA)   (= 2 log 2 iff perfectly recoverable from A; I(R:A)+I(R:E) = 2 log 2)
  I_c(R>A) = S(A) - S(RA)        (coherent information, = log 2 iff recoverable)
  F_Petz  = entanglement fidelity of the Petz (transpose-channel) recovery from A.  Closed form derived
            here for erasure with maximally mixed input:  F_Petz = Tr_E[(Tr_R sqrt(rho_RE))^2] / d_R
            (checked against the explicit Kraus construction in tests).  Barnum-Knill (2002):
            F_Petz <= F_opt <= sqrt(F_Petz), so this brackets the optimal recovery fidelity.
IMPORTANT: this is a finite-dimensional, model-specific statement about codes.  It illustrates the
entanglement-wedge / QEC language (Almheiri-Dong-Harlow 2015) but does NOT derive holography or say
anything about real black holes beyond the toy.
"""
from __future__ import annotations

import itertools
from functools import reduce

import numpy as np

LOG2 = np.log(2.0)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}

FIVE_QUBIT_GENERATORS = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
FIVE_QUBIT_LOGICAL_X = "XXXXX"
FIVE_QUBIT_LOGICAL_Z = "ZZZZZ"


# --------------------------------------------------------------------------- Pauli utilities
def pauli_string(s: str) -> np.ndarray:
    """Dense 2^n x 2^n matrix of a Pauli string; qubit 0 is the most significant (leftmost) factor."""
    return reduce(np.kron, [PAULI[ch] for ch in s])


def code_projector(generators) -> np.ndarray:
    """P = prod_i (1 + g_i)/2 for commuting, independent Pauli generators."""
    mats = [pauli_string(g) for g in generators]
    d = mats[0].shape[0]
    P = np.eye(d, dtype=complex)
    for g in mats:
        P = P @ (np.eye(d) + g) / 2.0
    return P


def five_qubit_code():
    """Returns (P, V) with V: C^2 -> C^32 the encoding isometry (columns |0_L>, |1_L>)."""
    P = code_projector(FIVE_QUBIT_GENERATORS)
    e0 = np.zeros(32, dtype=complex); e0[0] = 1.0
    v0 = P @ e0
    v0 /= np.linalg.norm(v0)
    v1 = pauli_string(FIVE_QUBIT_LOGICAL_X) @ v0
    return P, np.stack([v0, v1], axis=1)


def knill_laflamme_deviation(V: np.ndarray, erased: tuple[int, ...], n: int) -> float:
    """max over Paulis Ea,Eb supported on `erased` of the KL violation
    || <i|Ea^dag Eb|j> - c_ab delta_ij ||, c_ab = <0|Ea^dag Eb|0>.  0 <=> erasure of `erased` correctable."""
    worst = 0.0
    labels = ["".join(p) for p in itertools.product("IXYZ", repeat=len(erased))]
    ops = []
    for lab in labels:
        s = ["I"] * n
        for q, ch in zip(erased, lab):
            s[q] = ch
        ops.append(pauli_string("".join(s)) @ V)
    for a in ops:
        for b in ops:
            M = a.conj().T @ b  # 2x2 in code basis
            c = M[0, 0]
            dev = np.abs(M - c * np.eye(2)).max()
            worst = max(worst, float(dev))
    return worst


# --------------------------------------------------------------------------- encoders
def haar_isometry(n: int, rng: np.random.Generator) -> np.ndarray:
    d = 2 ** n
    Gm = rng.standard_normal((d, 2)) + 1j * rng.standard_normal((d, 2))
    Q, R = np.linalg.qr(Gm)
    return Q * (np.diag(R) / np.abs(np.diag(R)))


def _apply_2q_tensor(psi: np.ndarray, gate: np.ndarray, i: int, j: int) -> np.ndarray:
    """psi has shape (2,)*m; apply a 4x4 gate to axes i,j (i is the more significant)."""
    g = gate.reshape(2, 2, 2, 2)
    out = np.tensordot(g, psi, axes=([2, 3], [i, j]))
    return np.moveaxis(out, [0, 1], [i, j])


def random_clifford_isometry(n: int, rng: np.random.Generator, n_gates: int | None = None,
                             cliffords: np.ndarray | None = None) -> np.ndarray:
    """Encoding isometry of a random [[n,1]] stabilizer code: V|l> = C |l 0...0>, with C a random
    Clifford circuit of `n_gates` (default 10 n) uniformly random 2-qubit Cliffords on uniformly random
    qubit pairs (all-to-all).  Any Clifford encoder gives an exact stabilizer code; the circuit only
    approximates the uniform distribution over Clifford encoders."""
    if cliffords is None:
        from eh.circuits import two_qubit_clifford_group
        cliffords = two_qubit_clifford_group()
    if n_gates is None:
        n_gates = 10 * n
    cols = []
    gates = [(cliffords[int(rng.integers(len(cliffords)))], *rng.choice(n, 2, replace=False))
             for _ in range(n_gates)]
    for l in range(2):
        psi = np.zeros((2,) * n, dtype=complex)
        psi[(l,) + (0,) * (n - 1)] = 1.0
        for g, i, j in gates:
            psi = _apply_2q_tensor(psi, g, int(i), int(j))
        cols.append(psi.reshape(-1))
    return np.stack(cols, axis=1)


def code_projector_from_isometry(V: np.ndarray) -> np.ndarray:
    return V @ V.conj().T


# --------------------------------------------------------------------------- erasure diagnostics
def reference_state(V: np.ndarray) -> np.ndarray:
    """|Psi>_{RQ} = (1/sqrt2) sum_l |l>_R V|l>, returned with shape (2,)*(n+1), axis 0 = R."""
    n = int(round(np.log2(V.shape[0])))
    psi = V.T / np.sqrt(2.0)  # (2, 2^n): psi[l, q] = V[q, l]/sqrt2
    return psi.reshape((2,) * (n + 1))


def _bipartition(psi: np.ndarray, left_axes) -> np.ndarray:
    m = psi.ndim
    right = [a for a in range(m) if a not in left_axes]
    M = np.transpose(psi, list(left_axes) + right).reshape(2 ** len(left_axes), -1)
    return M


def _vn_from_sv(s: np.ndarray) -> float:
    p = s ** 2
    p = p[p > 1e-15]
    return float(-(p * np.log(p)).sum())


def erasure_diagnostics(V: np.ndarray, erased, with_petz: bool = True) -> dict:
    """Exact diagnostics for erasing physical qubits `erased` (indices 0..n-1)."""
    n = int(round(np.log2(V.shape[0])))
    psi = reference_state(V)
    E = [1 + q for q in erased]
    A = [1 + q for q in range(n) if q not in set(erased)]
    # S(A)
    S_A = _vn_from_sv(np.linalg.svd(_bipartition(psi, A), compute_uv=False)) if A else 0.0
    S_E = _vn_from_sv(np.linalg.svd(_bipartition(psi, E), compute_uv=False)) if E else 0.0
    S_R = LOG2
    I_RA = S_R + S_A - S_E          # S(RA) = S(E) for the pure state
    I_RE = S_R + S_E - S_A
    out = {"S_A": S_A, "S_E": S_E, "I_RA": I_RA, "I_RE": I_RE, "Ic_R_to_A": S_A - S_E,
           "I_RA_bits": I_RA / LOG2}
    if with_petz:
        out["F_petz"] = petz_fidelity(psi, E)
    return out


def petz_fidelity(psi: np.ndarray, E_axes) -> float:
    """F_Petz = Tr_E[(Tr_R sqrt(rho_RE))^2] / d_R  (d_R = 2), via the Schmidt decomposition across
    (R E | A).  sqrt(rho_RE) = U diag(s) U^dag with psi_{(RE),(A)} = U S W^dag."""
    RE = [0] + list(E_axes)
    M = _bipartition(psi, RE)  # (2 d_E, d_A)
    d_E = M.shape[0] // 2
    U, s, _ = np.linalg.svd(M, full_matrices=False)
    keep = s > 1e-12
    U, s = U[:, keep], s[keep]
    U = U.reshape(2, d_E, -1)
    Xm = sum((U[r] * s) @ U[r].conj().T for r in range(2))  # Tr_R sqrt(rho_RE), d_E x d_E
    return float(np.real(np.vdot(Xm, Xm)) / 2.0)


def petz_fidelity_kraus(V: np.ndarray, erased) -> float:
    """Reference implementation (slow): explicit Petz map R = pi^{1/2} N^dag(N(pi)^{-1/2} . N(pi)^{-1/2}) pi^{1/2}
    for N(rho) = Tr_E[V rho V^dag], entanglement fidelity sum_{jk} |Tr(R_j K_k pi)|^2."""
    n = int(round(np.log2(V.shape[0])))
    A = [q for q in range(n) if q not in set(erased)]
    T = V.reshape((2,) * n + (2,))
    T = np.transpose(T, list(erased) + A + [n]).reshape(2 ** len(erased), 2 ** len(A), 2)
    K = [T[k] for k in range(T.shape[0])]  # K_k: C^2 -> C^{d_A}
    rhoA = sum(k @ k.conj().T for k in K) / 2.0
    w, Uw = np.linalg.eigh(rhoA)
    inv_sqrt = np.where(w > 1e-12, 1.0 / np.sqrt(np.clip(w, 1e-300, None)), 0.0)
    Yh = (Uw * inv_sqrt) @ Uw.conj().T
    pi_half = np.eye(2) / np.sqrt(2.0)
    R = [pi_half @ k.conj().T @ Yh for k in K]
    pi = np.eye(2) / 2.0
    return float(sum(abs(np.trace(r @ k @ pi)) ** 2 for r in R for k in K))


def code_distance_from_erasures(results_by_subset: dict, n: int, tol: float = 1e-8) -> int:
    """Smallest |E| with an uncorrectable erasure (I(R:E) > tol).  results_by_subset: {E_tuple: I_RE}."""
    for e in range(n + 1):
        for E, val in results_by_subset.items():
            if len(E) == e and val > tol:
                return e
    return n + 1


def page_approx_I_RA(n: int, a: int) -> float:
    """Page-formula approximation (NOT exact here; rho_R is fixed to I/2) for Haar isometries:
    I(R:A) ~ log2 + S_Page(d_A, 2 d_E) - S_Page(d_E, 2 d_A), d_A = 2^a, d_E = 2^(n-a)."""
    from eh.page import page_entropy
    e = n - a
    sA = page_entropy(2 ** a, 2 ** (e + 1)) if a > 0 else 0.0
    sE = page_entropy(2 ** e, 2 ** (a + 1)) if e > 0 else 0.0
    return LOG2 + sA - sE
