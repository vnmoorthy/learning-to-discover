"""Infinite-temperature out-of-time-order correlators for brickwork circuits
(Track D).  NEW module.

Convention (stated once, used everywhere):
    F(t) = 2^-N Tr[ W(t) V W(t)^dag V^dag ],   W(t) = U_t^dag W U_t,
with U_t the depth-t circuit, W and V Pauli strings (Hermitian, so this is
2^-N Tr[W(t) V W(t) V]). This is the infinite-temperature (beta = 0)
normalized OTOC; at beta = 0 there is no thermal-regularisation ambiguity
(rho^1/4 insertions all equal 2^-N/4 x identity). F(0) = +1 if W, V commute
and -1 if they anticommute; F = 1 whenever W or V is the identity.
Haar (and any unitary 2-design, e.g. the Clifford group) average for
non-identity Paulis:  E[F] = -1/(d^2 - 1),  d = 2^N.
Yoshida-Kitaev (arXiv:1710.03363) identity tested in tests/test_recovery.py:
    P_EPR = average over ALL Paulis O_M on M and O_D on D of F(O_D, O_M),
where O_D sits at the output (D, last m qubits) and O_M at the input message.
"""
from __future__ import annotations

import itertools

import numpy as np

from .circuits import apply_brick_layer

I2 = np.eye(2, dtype=complex)
PAULI = {
    "I": I2,
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]]),
    "Z": np.diag([1.0 + 0j, -1.0]),
}


def pauli_string(n: int, ops: dict) -> np.ndarray:
    """Dense 2^n x 2^n Pauli string; ops = {qubit: 'X'|'Y'|'Z'|'I'}, qubit 0
    most significant (same convention as eh.circuits)."""
    out = np.array([[1.0 + 0j]])
    for q in range(n):
        out = np.kron(out, PAULI[ops.get(q, "I")])
    return out


def otoc(U: np.ndarray, W: np.ndarray, V: np.ndarray) -> float:
    """F = 2^-N Tr[W(t) V W(t)^dag V^dag] with W(t) = U^dag W U."""
    d = U.shape[0]
    Wt = U.conj().T @ (W @ U)
    val = np.trace(Wt @ V @ Wt.conj().T @ V.conj().T) / d
    return float(np.real(val))


def haar_otoc(n: int) -> float:
    d = 2.0 ** n
    return -1.0 / (d * d - 1.0)


def pauli_averaged_otoc(U: np.ndarray, n: int, in_qubits, out_qubits, include_identity=True) -> float:
    """Average of F over Pauli strings O_out on out_qubits (applied at the output,
    Heisenberg-evolved) and O_in on in_qubits (at the input). include_identity:
    average over the full Pauli groups (Yoshida-Kitaev normalisation)."""
    labels = "IXYZ" if include_identity else "XYZ"

    def strings(qs):
        for combo in itertools.product(labels, repeat=len(qs)):
            if not include_identity or True:
                yield pauli_string(n, dict(zip(qs, combo)))

    Vs = list(strings(list(in_qubits)))
    tot, cnt = 0.0, 0
    for W in strings(list(out_qubits)):
        Wt = U.conj().T @ (W @ U)
        for V in Vs:
            tot += float(np.real(np.trace(Wt @ V @ Wt.conj().T @ V.conj().T))) / U.shape[0]
            cnt += 1
    return tot / cnt


def otoc_vs_depth(n: int, max_depth: int, rng, gate: str, pairs) -> np.ndarray:
    """OTOCs F_t for t = 0..max_depth of ONE brickwork circuit (same random
    draws as eh.circuits.brickwork_unitary with the same rng).
    pairs: list of (W_ops, V_ops) dicts. Returns array (max_depth+1, len(pairs))."""
    d = 2 ** n
    t = np.eye(d, dtype=complex).reshape((2,) * n + (d,))
    mats = [(pauli_string(n, w), pauli_string(n, v)) for w, v in pairs]
    out = np.zeros((max_depth + 1, len(pairs)))
    for layer in range(max_depth + 1):
        if layer > 0:
            t = apply_brick_layer(t, n, layer - 1, rng, gate)
        U = t.reshape(d, d)
        for j, (W, V) in enumerate(mats):
            out[layer, j] = otoc(U, W, V)
    return out
