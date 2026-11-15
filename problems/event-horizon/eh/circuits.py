"""Scramblers for the sequential-evaporation toy model (Extension 1).

Self-contained: Haar unitaries, exact 2-qubit Clifford group (11520 elements
modulo global phase, enumerated by BFS over words in H, S, CNOT), brickwork
circuits, state-vector gate application, Schmidt spectra and entropies.

Conventions
-----------
* A state on N qubits is a complex ndarray of shape (2,)*N; qubit i = axis i.
* Entropies are in nats (natural log). Eigenvalues p <= P_CLIP are dropped
  from -sum p log p (0 log 0 := 0), so log(0) is never evaluated.
* Evaporation model: N qubits start in |0...0> (a pure "black hole"). At each
  step the scrambler acts on the remaining n_rem = N - t black-hole qubits
  (axes 0..n_rem-1), then the last remaining qubit (axis n_rem-1) is emitted
  and never touched again. Radiation after t emissions = axes N-t..N-1.
"""
from __future__ import annotations

import functools
import numpy as np

P_CLIP = 1e-15  # eigenvalues below this are treated as exactly zero
LOG2 = float(np.log(2.0))

# ----------------------------------------------------------------------------
# basic linear algebra helpers
# ----------------------------------------------------------------------------

def haar_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-distributed d x d unitary (QR of a Ginibre matrix, phases fixed)."""
    z = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    ph = np.diagonal(r) / np.abs(np.diagonal(r))
    return q * ph


def haar_state(n_qubits: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random pure state = U|0> for Haar U (normalised complex Gaussian)."""
    v = rng.standard_normal(2 ** n_qubits) + 1j * rng.standard_normal(2 ** n_qubits)
    v /= np.linalg.norm(v)
    return v.reshape((2,) * n_qubits)


def zero_state(n_qubits: int) -> np.ndarray:
    v = np.zeros(2 ** n_qubits, dtype=complex)
    v[0] = 1.0
    return v.reshape((2,) * n_qubits)


def apply_2q(state: np.ndarray, gate: np.ndarray, i: int, j: int) -> np.ndarray:
    """Apply a 4x4 gate to qubits (i, j) (i = most significant) of a state tensor.
    Extra trailing axes (e.g. a column index when building a unitary) are fine."""
    g = gate.reshape(2, 2, 2, 2)
    out = np.tensordot(g, state, axes=([2, 3], [i, j]))
    return np.moveaxis(out, [0, 1], [i, j])


def apply_1q(state: np.ndarray, gate: np.ndarray, i: int) -> np.ndarray:
    out = np.tensordot(gate, state, axes=([1], [i]))
    return np.moveaxis(out, 0, i)


def schmidt_probs(state: np.ndarray, n_left: int) -> np.ndarray:
    """Eigenvalues of the reduced density matrix for the cut (first n_left
    qubits | rest), via SVD. Returned sorted descending, normalised."""
    n = state.ndim
    m = state.reshape(2 ** n_left, 2 ** (n - n_left))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2
    return p / p.sum()


def entropy_vn(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    p = p[p > P_CLIP]
    return float(-(p * np.log(p)).sum())


def entropy_renyi2(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    return float(-np.log((p ** 2).sum()))


def page_entropy(m: int, n: int) -> float:
    """Page's exact mean entropy (nats) of the smaller subsystem of a Haar-random
    pure state in dimensions m x n (Page 1993, PRL 71:1291; proved by
    Foong-Kanno 1994, Sanchez-Ruiz 1995, Sen 1996):
        S_{m,n} = sum_{k=n+1}^{mn} 1/k - (m-1)/(2n),  m <= n."""
    if m > n:
        m, n = n, m
    ks = np.arange(n + 1, m * n + 1, dtype=float)
    return float((1.0 / ks).sum() - (m - 1) / (2.0 * n))


def page_curve(n_qubits: int) -> np.ndarray:
    """Page value of S(R) after t = 0..N emitted qubits."""
    return np.array([page_entropy(2 ** t, 2 ** (n_qubits - t)) for t in range(n_qubits + 1)])


def haar_mean_purity(m: int, n: int) -> float:
    """Exact Haar mean of tr(rho_m^2) for an m x n bipartite pure state:
    (m+n)/(mn+1) (Lubkin 1978)."""
    return (m + n) / (m * n + 1.0)


# ----------------------------------------------------------------------------
# Clifford group
# ----------------------------------------------------------------------------
H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S1 = np.array([[1, 0], [0, 1j]], dtype=complex)
I1 = np.eye(2, dtype=complex)
X1 = np.array([[0, 1], [1, 0]], dtype=complex)
Y1 = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z1 = np.array([[1, 0], [0, -1]], dtype=complex)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)

CLIFFORD_GENERATORS = {
    "H0": np.kron(H1, I1), "H1": np.kron(I1, H1),
    "S0": np.kron(S1, I1), "S1": np.kron(I1, S1),
    "CX": CNOT,
}


def _canon(u: np.ndarray) -> np.ndarray:
    """Fix the global phase of a batch (..., 4, 4): the first entry (row-major)
    with |x| > 1e-9 is made real and positive."""
    flat = u.reshape(u.shape[:-2] + (16,))
    idx = np.argmax(np.abs(flat) > 1e-9, axis=-1)
    lead = np.take_along_axis(flat, idx[..., None], axis=-1)[..., 0]
    return u * (np.abs(lead) / lead)[..., None, None]


@functools.lru_cache(maxsize=1)
def two_qubit_clifford_group() -> np.ndarray:
    """All 11520 two-qubit Clifford unitaries modulo global phase, as an array
    of shape (11520, 4, 4), enumerated by breadth-first search over words in
    {H0, H1, S0, S1, CNOT}. Deterministic ordering."""
    gens = np.array(list(CLIFFORD_GENERATORS.values()))
    ident = np.eye(4, dtype=complex)

    def keys(batch):
        r = np.round(batch, 6) + 0.0  # +0.0 turns -0.0 into 0.0
        return [row.tobytes() for row in r.reshape(len(batch), 16)]

    seen = {keys(ident[None])[0]: None}
    elems = [ident]
    frontier = ident[None]
    while len(frontier):
        cand = _canon(np.einsum("gij,fjk->fgik", gens, frontier).reshape(-1, 4, 4))
        nxt = []
        for k, v in zip(keys(cand), cand):
            if k not in seen:
                seen[k] = None
                nxt.append(v)
        elems.extend(nxt)
        frontier = np.array(nxt) if nxt else np.zeros((0, 4, 4))
    return np.array(elems)


def random_clifford_2q(rng: np.random.Generator) -> np.ndarray:
    """Uniform sample from the 2-qubit Clifford group (mod phase)."""
    g = two_qubit_clifford_group()
    return g[int(rng.integers(len(g)))]


def pauli_group_2q() -> list[np.ndarray]:
    ps = [I1, X1, Y1, Z1]
    return [np.kron(a, b) for a in ps for b in ps]


def is_pauli_up_to_sign(m: np.ndarray, tol: float = 1e-9) -> bool:
    """True iff m = +/- P for a 2-qubit Pauli string P."""
    for p in pauli_group_2q():
        c = np.trace(p.conj().T @ m) / 4.0
        if abs(abs(c) - 1.0) < tol:
            return abs(c.imag) < tol and np.allclose(m, c.real * p, atol=1e-8)
    return False


# ----------------------------------------------------------------------------
# brickwork layers
# ----------------------------------------------------------------------------

def brick_pairs(n: int, layer: int) -> list[tuple[int, int]]:
    """Nearest-neighbour pairs of an open chain of n qubits; even layers start
    at bond (0,1), odd layers at bond (1,2)."""
    return [(i, i + 1) for i in range(layer % 2, n - 1, 2)]


def apply_brick_layer(state, n_active, layer, rng, gate="haar"):
    """One brickwork layer on qubits 0..n_active-1. gate: 'haar' | 'clifford' |
    'swap' | 'cnot' | 'identity'."""
    for (i, j) in brick_pairs(n_active, layer):
        if gate == "haar":
            g = haar_unitary(4, rng)
        elif gate == "clifford":
            g = random_clifford_2q(rng)
        elif gate == "swap":
            g = SWAP
        elif gate == "cnot":
            g = CNOT
        elif gate == "identity":
            continue
        else:
            raise ValueError(gate)
        state = apply_2q(state, g, i, j)
    return state


def brickwork_unitary(n: int, depth: int, rng, gate="haar") -> np.ndarray:
    """Dense 2^n x 2^n unitary of a depth-`depth` brickwork circuit."""
    d = 2 ** n
    t = np.eye(d, dtype=complex).reshape((2,) * n + (d,))
    for layer in range(depth):
        t = apply_brick_layer(t, n, layer, rng, gate)
    return t.reshape(d, d)


# ----------------------------------------------------------------------------
# sequential evaporation
# ----------------------------------------------------------------------------
SCRAMBLERS = ("haar", "haar_shortcut", "local_haar", "clifford",
              "identity", "swap", "h_cnot")


def evaporate(n_qubits: int, scrambler: str, rng: np.random.Generator,
              depth: int = 1, return_spectra: bool = False) -> dict:
    """Run the sequential evaporation model and return S_vN(t), S_2(t) of the
    radiation for t = 0..N (nats).

    scrambler:
      'haar'          fresh Haar unitary on the remaining 2^(N-t) dims each step
                      (expensive: dense QR).
      'haar_shortcut' exact equivalent for radiation entropies: a Haar unitary
                      on |0..0> gives a Haar-random state, and later unitaries
                      on the remaining black hole cannot change the entropy of
                      already-emitted radiation, so only step 0 matters.
      'local_haar'    `depth` brickwork layers of Haar 2-qubit gates per step.
      'clifford'      `depth` brickwork layers of uniform 2-qubit Cliffords.
      'identity'      no dynamics (control).
      'swap'          `depth` brickwork layers of nearest-neighbour SWAPs
                      (control; product states stay product).
      'h_cnot'        control: at step 0 only, Hadamard on even qubits then ONE
                      CNOT layer on bonds (0,1),(2,3),.. -> static Bell dimers.
    """
    n = n_qubits
    state = zero_state(n)
    s_vn = np.zeros(n + 1)
    s_2 = np.zeros(n + 1)
    spectra = [np.array([1.0])]
    layer = 0
    for t in range(n):
        n_rem = n - t
        if scrambler == "haar":
            u = haar_unitary(2 ** n_rem, rng)
            m = state.reshape(2 ** n_rem, 2 ** t)
            state = (u @ m).reshape((2,) * n)
        elif scrambler == "haar_shortcut":
            if t == 0:
                state = haar_state(n, rng)
        elif scrambler in ("local_haar", "clifford", "swap"):
            g = {"local_haar": "haar", "clifford": "clifford", "swap": "swap"}[scrambler]
            for _ in range(depth):
                state = apply_brick_layer(state, n_rem, layer, rng, g)
                layer += 1
        elif scrambler == "h_cnot":
            if t == 0:
                for q in range(0, n, 2):
                    state = apply_1q(state, H1, q)
                state = apply_brick_layer(state, n, 0, rng, "cnot")
        elif scrambler == "identity":
            pass
        else:
            raise ValueError(scrambler)
        # emit qubit n_rem-1: radiation = last t+1 qubits
        p = schmidt_probs(state, n - (t + 1))
        s_vn[t + 1] = entropy_vn(p)
        s_2[t + 1] = entropy_renyi2(p)
        spectra.append(p)
    out = {"s_vn": s_vn, "s_2": s_2, "norm": float(np.linalg.norm(state))}
    if return_spectra:
        out["spectra"] = spectra
    return out


def one_shot_entropies(n_qubits: int, depth: int, rng, gate="haar") -> np.ndarray:
    """Apply `depth` brickwork layers to |0..0> on all N qubits (no evaporation)
    and return S_vN for every cut t = 0..N (right block of t qubits)."""
    state = zero_state(n_qubits)
    for layer in range(depth):
        state = apply_brick_layer(state, n_qubits, layer, rng, gate)
    return np.array([entropy_vn(schmidt_probs(state, n_qubits - t)) for t in range(n_qubits + 1)])


def spacing_ratio(p: np.ndarray, floor: float = 1e-12) -> float:
    """Mean adjacent-gap ratio <r> of the entanglement 'energies' xi=-log p
    (p > floor). NaN if there are fewer than 3 levels or exact degeneracies
    make every gap vanish (flat spectra, e.g. stabilizer states)."""
    p = np.asarray(p, dtype=float)
    p = p[p > floor]
    if len(p) < 3:
        return float("nan")
    xi = np.sort(-np.log(p))
    gaps = np.diff(xi)
    a, b = gaps[:-1], gaps[1:]
    mx = np.maximum(a, b)
    ok = mx > 1e-9
    if not ok.any():
        return float("nan")
    return float((np.minimum(a, b)[ok] / mx[ok]).mean())


# ============================================================================
# torch / GPU backend (complex128).  Used by experiments/e1_scrambling.py.
# ============================================================================
# Layout: a batch of B states on N qubits is a tensor of shape (B, 2^N), qubit
# 0 = most significant bit.  Small gates (4x4 Haar / Clifford) are sampled on
# the CPU with a seeded numpy Generator (device-independent reproducibility);
# large objects (Haar-random states, big Haar unitaries) are sampled on the
# device with a seeded torch.Generator.
#
# Entanglement spectra on the GPU use eigvalsh of the Gram matrix on the
# smaller side of the cut.  This squares the condition number, so eigenvalues
# are only resolved down to ~1e-15 (absolute); eigenvalues <= GRAM_CLIP are
# treated as exactly zero in entropies (error <= rank * GRAM_CLIP * |log
# GRAM_CLIP| < 2e-8 nats for rank <= 8192).
GRAM_CLIP = 1e-13


def get_device():
    import torch
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def to_t(arr, device=None):
    """numpy -> torch complex128 without the torch<->numpy bridge (the GPU
    box has a torch built against numpy 1.x next to numpy 2.x, where
    torch.from_numpy / Tensor.numpy are unavailable)."""
    import torch
    a = np.ascontiguousarray(arr, dtype=np.complex128)
    t = torch.frombuffer(bytearray(a.tobytes()), dtype=torch.complex128).reshape(a.shape)
    return t.to(device or get_device())


def to_np(t) -> np.ndarray:
    """torch (real or integer) tensor -> numpy, bridge-free."""
    return np.array(t.detach().cpu().tolist())


def t_haar_unitary(d: int, seed: int, device=None):
    """Haar d x d unitary on `device` (QR of complex Ginibre, phases of diag(R)
    fixed; Mezzadri 2007), seeded torch.Generator on that device."""
    import torch
    device = device or get_device()
    g = torch.Generator(device=device); g.manual_seed(int(seed))
    z = torch.view_as_complex(torch.randn(d, d, 2, generator=g, device=device, dtype=torch.float64))
    q, r = torch.linalg.qr(z)
    del z
    dg = torch.diagonal(r)
    return q * (dg / dg.abs()).unsqueeze(0)


def t_haar_states(batch: int, n_qubits: int, seed: int, device=None):
    """Batch of Haar-random pure states, shape (batch, 2^N)."""
    import torch
    device = device or get_device()
    g = torch.Generator(device=device); g.manual_seed(int(seed))
    v = torch.view_as_complex(torch.randn(batch, 2 ** n_qubits, 2, generator=g, device=device, dtype=torch.float64))
    return v / torch.linalg.vector_norm(v, dim=1, keepdim=True)


def t_zero_states(batch: int, n_qubits: int, device=None):
    import torch
    device = device or get_device()
    s = torch.zeros(batch, 2 ** n_qubits, dtype=torch.complex128, device=device)
    s[:, 0] = 1.0
    return s


def haar_gates_np(shape, rng: np.random.Generator) -> np.ndarray:
    """Array shape + (4, 4) of independent Haar 2-qubit gates (batched QR)."""
    z = (rng.standard_normal(tuple(shape) + (4, 4)) + 1j * rng.standard_normal(tuple(shape) + (4, 4))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    dg = np.diagonal(r, axis1=-2, axis2=-1)
    return q * (dg / np.abs(dg))[..., None, :]


def clifford_gates_np(shape, rng: np.random.Generator) -> np.ndarray:
    g = two_qubit_clifford_group()
    return g[rng.integers(len(g), size=tuple(shape))]


def t_apply_2q(state, gates, i: int):
    """Apply gates to neighbouring qubits (i, i+1).  state: (B, 2^n, ...) with
    optional trailing axes; gates: (B, 4, 4) or (4, 4) torch complex128."""
    import torch
    B = state.shape[0]
    shp = state.shape
    L = 2 ** i
    s = state.reshape(B, L, 4, -1)
    if gates.dim() == 2:
        out = torch.einsum("xy,blyr->blxr", gates, s)
    else:
        out = torch.einsum("bxy,blyr->blxr", gates, s)
    return out.reshape(shp)


def t_brick_layer(state, n_active: int, layer: int, rng, gate: str, n_total: int):
    """One brickwork layer on qubits 0..n_active-1 of states (B, 2^n_total, ...)."""
    import torch
    pairs = brick_pairs(n_active, layer)
    if not pairs or gate == "identity":
        return state
    B = state.shape[0]
    if gate == "haar":
        g = to_t(haar_gates_np((B, len(pairs)), rng), state.device)
    elif gate == "clifford":
        g = to_t(clifford_gates_np((B, len(pairs)), rng), state.device)
    elif gate == "swap":
        g = to_t(SWAP, state.device)
    elif gate == "cnot":
        g = to_t(CNOT, state.device)
    else:
        raise ValueError(gate)
    for j, (i, _) in enumerate(pairs):
        state = t_apply_2q(state, g[:, j] if g.dim() == 4 else g, i)
    return state


def robust_eigvalsh(G):
    """eigvalsh with fallbacks: the batched GPU Jacobi solver can fail to
    converge on exactly degenerate spectra (stabilizer states); retry matrix
    by matrix on the GPU (divide & conquer), then on the CPU (LAPACK)."""
    import torch
    try:
        return torch.linalg.eigvalsh(G)
    except Exception:
        pass
    if G.dim() == 2:
        return torch.linalg.eigvalsh(G.cpu()).to(G.device)
    outs = []
    for b in range(G.shape[0]):
        try:
            outs.append(torch.linalg.eigvalsh(G[b]))
        except Exception:
            outs.append(torch.linalg.eigvalsh(G[b].cpu()).to(G.device))
    return torch.stack(outs)


def t_schmidt_probs(state, n_left: int, n_total: int):
    """Spectrum of the reduced state across (first n_left qubits | rest) for a
    batch (B, 2^n_total): eigvalsh of the Gram matrix on the smaller side.
    Returns (B, 2^min(n_left, n_total-n_left)), descending, normalised, >= 0."""
    import torch
    B = state.shape[0]
    M = state.reshape(B, 2 ** n_left, 2 ** (n_total - n_left))
    if n_left <= n_total - n_left:
        G = M @ M.conj().transpose(1, 2)
    else:
        G = M.conj().transpose(1, 2) @ M
    p = robust_eigvalsh(G).clamp_min(0.0)
    del G
    p = p / p.sum(dim=1, keepdim=True)
    return torch.flip(p, dims=[1])


def t_entropies(p, clip: float = GRAM_CLIP):
    """(S_vN, S_2, S_min, rank) in nats for a batch of spectra (B, r)."""
    import torch
    safe = torch.where(p > clip, p, torch.ones_like(p))   # log(1) = 0: never log(0)
    s_vn = -(torch.where(p > clip, p, torch.zeros_like(p)) * torch.log(safe)).sum(dim=1)
    s_2 = -torch.log((p ** 2).sum(dim=1))
    s_min = -torch.log(p.max(dim=1).values)
    rank = (p > 1e-10).sum(dim=1)
    return s_vn, s_2, s_min, rank


def t_evaporate(n_qubits: int, scrambler: str, batch: int, seed_seq, depth: int = 1,
                device=None, keep_spectrum_at=None) -> dict:
    """GPU version of `evaporate` for a batch of independent runs.

    seed_seq: a numpy SeedSequence; gate randomness comes from
    default_rng(seed_seq) (drawn for the whole batch at once), device-side
    randomness (Haar states / big unitaries) from torch generators seeded with
    seed_seq.generate_state(...).  Returns numpy arrays (batch, N+1)."""
    import torch
    device = device or get_device()
    n = n_qubits
    rng = np.random.default_rng(seed_seq)
    tseeds = [int(x) for x in seed_seq.generate_state(batch * (n + 1) + 1)]
    state = t_zero_states(batch, n, device)
    out = {k: np.zeros((batch, n + 1)) for k in ("s_vn", "s_2", "s_min")}
    out["rank"] = np.ones((batch, n + 1), dtype=np.int64)
    layer = 0
    for t in range(n):
        n_rem = n - t
        if scrambler == "haar":           # explicit fresh Haar unitary on remaining BH
            M = state.reshape(batch, 2 ** n_rem, 2 ** t)
            new = torch.empty_like(M)
            for b in range(batch):
                u = t_haar_unitary(2 ** n_rem, tseeds[1 + b * (n + 1) + t], device)
                new[b] = u @ M[b]
                del u
            state = new.reshape(batch, -1)
        elif scrambler == "haar_shortcut":
            if t == 0:
                state = t_haar_states(batch, n, tseeds[0], device)
        elif scrambler in ("local_haar", "clifford", "swap"):
            g = {"local_haar": "haar", "clifford": "clifford", "swap": "swap"}[scrambler]
            for _ in range(depth):
                state = t_brick_layer(state, n_rem, layer, rng, g, n)
                layer += 1
        elif scrambler == "h_cnot":
            if t == 0:
                h2 = to_t(np.kron(H1, I1), device)
                for q in range(0, n - 1, 2):
                    state = t_apply_2q(state, h2, q)
                state = t_brick_layer(state, n, 0, rng, "cnot", n)
        elif scrambler == "identity":
            pass
        else:
            raise ValueError(scrambler)
        p = t_schmidt_probs(state, n - (t + 1), n)
        sv, s2, sm, rk = t_entropies(p)
        out["s_vn"][:, t + 1] = to_np(sv); out["s_2"][:, t + 1] = to_np(s2)
        out["s_min"][:, t + 1] = to_np(sm); out["rank"][:, t + 1] = to_np(rk)
        if keep_spectrum_at is not None and t + 1 == keep_spectrum_at:
            out["spectrum"] = to_np(p)
        del p
    out["norm"] = to_np(torch.linalg.vector_norm(state, dim=1))
    return out


def t_one_shot(n_qubits: int, gate: str, max_depth: int, batch: int, seed_seq, device=None,
               every: int = 1) -> dict:
    """Brickwork layers on all N qubits from |0..0> (no emission); half-cut
    S_vN and S_2 recorded after every `every` layers."""
    device = device or get_device()
    rng = np.random.default_rng(seed_seq)
    state = t_zero_states(batch, n_qubits, device)
    depths, svn, s2 = [], [], []
    for layer in range(max_depth):
        state = t_brick_layer(state, n_qubits, layer, rng, gate, n_qubits)
        if (layer + 1) % every == 0:
            p = t_schmidt_probs(state, n_qubits // 2, n_qubits)
            a, b, _, _ = t_entropies(p)
            depths.append(layer + 1); svn.append(to_np(a)); s2.append(to_np(b))
    return {"depths": depths, "s_vn": np.array(svn).T, "s_2": np.array(s2).T}
