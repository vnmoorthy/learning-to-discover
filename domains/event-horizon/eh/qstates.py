"""Haar-random states / unitaries, partial traces and Schmidt spectra.

numpy backend (always available) and an optional torch backend (complex128, CUDA if present).

Haar unitaries: QR decomposition of a complex Ginibre matrix followed by the phase fix
Q -> Q diag(R_ii/|R_ii|)  (F. Mezzadri, "How to generate random matrices from the classical
compact groups", Notices of the AMS 54 (2007) 592).  Without the phase fix the output of a
LAPACK QR is NOT Haar distributed.

Qubit / subsystem ordering: a state on subsystems with dimensions dims = (d_0, ..., d_{n-1})
is stored as a flat vector in C order, i.e. psi.reshape(dims)[i_0, ..., i_{n-1}].
"""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np

try:  # optional
    import torch
except Exception:  # pragma: no cover
    torch = None


# ----------------------------------------------------------------------------- numpy backend
def haar_state(d: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random pure state in C^d (normalised complex Gaussian vector)."""
    z = rng.standard_normal(d) + 1j * rng.standard_normal(d)
    return z / np.linalg.norm(z)


def haar_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random d x d unitary (Ginibre + QR + Mezzadri phase fix)."""
    g = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / math.sqrt(2.0)
    q, r = np.linalg.qr(g)
    diag = np.diagonal(r)
    return q * (diag / np.abs(diag))


def _split(dims: Sequence[int], keep: Sequence[int]):
    dims = tuple(int(x) for x in dims)
    keep = tuple(int(k) for k in keep)
    rest = tuple(i for i in range(len(dims)) if i not in keep)
    dk = int(np.prod([dims[i] for i in keep])) if keep else 1
    dr = int(np.prod([dims[i] for i in rest])) if rest else 1
    return dims, keep, rest, dk, dr


def state_matrix(psi, dims: Sequence[int], keep: Sequence[int]):
    """Reshape |psi> into the (d_keep x d_rest) coefficient matrix M of the bipartition keep|rest.

    Works for numpy arrays and torch tensors.  rho_keep = M M^dagger, rho_rest = (M^dagger M)^T.
    """
    dims, keep, rest, dk, dr = _split(dims, keep)
    t = psi.reshape(dims)
    perm = keep + rest
    if torch is not None and isinstance(t, torch.Tensor):
        t = t.permute(perm)
    else:
        t = np.transpose(t, perm)
    return t.reshape(dk, dr)


def reduced_density_matrix(psi, dims: Sequence[int], keep: Sequence[int]):
    """rho_keep = Tr_rest |psi><psi| for an arbitrary set of kept subsystems."""
    m = state_matrix(psi, dims, keep)
    return m @ m.conj().T


def partial_trace(rho, dims: Sequence[int], keep: Sequence[int]):
    """Partial trace of a density MATRIX over all subsystems not in ``keep`` (reshape + einsum)."""
    dims, keep, rest, dk, dr = _split(dims, keep)
    n = len(dims)
    t = rho.reshape(dims + dims)
    perm = keep + rest + tuple(n + i for i in keep) + tuple(n + i for i in rest)
    if torch is not None and isinstance(t, torch.Tensor):
        t = t.permute(perm).reshape(dk, dr, dk, dr)
        return torch.einsum("atbt->ab", t)
    t = np.transpose(t, perm).reshape(dk, dr, dk, dr)
    return np.einsum("atbt->ab", t)


def schmidt_coefficients(psi, dims: Sequence[int], keep: Sequence[int]):
    """Schmidt coefficients (singular values, descending) of |psi> across keep|rest via SVD."""
    m = state_matrix(psi, dims, keep)
    if torch is not None and isinstance(m, torch.Tensor):
        return torch.linalg.svdvals(m)
    return np.linalg.svd(m, compute_uv=False)


# ----------------------------------------------------------------------------- torch backend
def torch_device(prefer_cuda: bool = True):
    if torch is None:
        raise RuntimeError("torch is not installed")
    return torch.device("cuda" if (prefer_cuda and torch.cuda.is_available()) else "cpu")


def torch_generator(seed: int, device=None):
    device = torch_device() if device is None else device
    g = torch.Generator(device=device)
    g.manual_seed(int(seed))
    return g


def ginibre_t(shape, gen, device=None):
    """Complex Ginibre tensor, entries CN(0,1) (real and imaginary parts N(0,1/2)), complex128."""
    device = gen.device if device is None else device
    return torch.randn(shape, generator=gen, device=device, dtype=torch.complex128)


def haar_states_t(batch: int, d: int, gen, device=None):
    """(batch, d) Haar-random pure states."""
    z = ginibre_t((batch, d), gen, device)
    return z / torch.linalg.vector_norm(z, dim=-1, keepdim=True)


def haar_isometry_t(d: int, r: int, gen, device=None):
    """Haar (invariant) random isometry C^r -> C^d, d >= r: first r columns of a Haar unitary.

    Reduced QR of a d x r Ginibre matrix + Mezzadri phase fix."""
    g = ginibre_t((d, r), gen, device)
    q, rr = torch.linalg.qr(g, mode="reduced")
    del g
    diag = torch.diagonal(rr)
    return q * (diag / diag.abs())


def haar_unitary_t(d: int, gen, device=None):
    """Haar-random d x d unitary on the torch device."""
    return haar_isometry_t(d, d, gen, device)


def schmidt_probs_t(m, method: str = "gram"):
    """Normalised Schmidt probabilities (ascending) of coefficient matrices m[..., a, b].

    method="gram": eigvalsh of the Gram matrix on the SMALLER side (m m^dag or m^dag m).
        Absolute eigenvalue error ~ 1e-16 * p_max; entropy error is negligible because
        eigenvalues <= 1e-15 are clipped anyway.  Much faster than an SVD on the GPU.
    method="svd":  squared singular values (torch.linalg.svdvals); used in tests as reference.
    """
    a, b = m.shape[-2], m.shape[-1]
    if method == "svd":
        s = torch.linalg.svdvals(m)
        p = torch.flip(s * s, dims=(-1,))
    else:
        if a <= b:
            g = m @ m.conj().transpose(-1, -2)
        else:
            g = m.conj().transpose(-1, -2) @ m
        p = torch.linalg.eigvalsh(g).clamp_min(0.0)
    return p / p.sum(dim=-1, keepdim=True)
