"""Entropies from eigenvalue / Schmidt spectra (numpy arrays or torch tensors).

Conventions
-----------
* Natural-log units (nats) unless ``bits=True``.
* Eigenvalues p <= CLIP (default 1e-15) contribute exactly 0 to -sum p log p; this is the
  documented clipping threshold, so log(0) is never evaluated.  Small negative eigenvalues
  produced by round-off are treated the same way (clipped to zero contribution).
* Functions act on the LAST axis, so batches of spectra are supported.
"""
from __future__ import annotations

import math

import numpy as np

try:  # optional
    import torch
except Exception:  # pragma: no cover
    torch = None

CLIP = 1e-15
LOG2 = math.log(2.0)


def _is_torch(x):
    return torch is not None and isinstance(x, torch.Tensor)


def von_neumann(p, clip: float = CLIP, bits: bool = False):
    """S = -sum_i p_i log p_i over the last axis; entries <= clip contribute 0."""
    if _is_torch(p):
        q = torch.where(p > clip, p, torch.ones_like(p))
        s = -(q * torch.log(q)).sum(dim=-1)
    else:
        p = np.asarray(p, dtype=float)
        q = np.where(p > clip, p, 1.0)
        s = -(q * np.log(q)).sum(axis=-1)
    return s / LOG2 if bits else s


def purity(p):
    """Tr rho^2 = sum_i p_i^2 over the last axis."""
    if _is_torch(p):
        return (p * p).sum(dim=-1)
    p = np.asarray(p, dtype=float)
    return (p * p).sum(axis=-1)


def renyi2(p, bits: bool = False):
    """S_2 = -log Tr rho^2."""
    pu = purity(p)
    s = -torch.log(pu) if _is_torch(pu) else -np.log(pu)
    return s / LOG2 if bits else s


def schmidt_to_probs(s):
    """Schmidt coefficients (singular values) -> normalised probabilities p_i = s_i^2 / sum s^2."""
    p = s * s
    if _is_torch(p):
        return p / p.sum(dim=-1, keepdim=True)
    return p / p.sum(axis=-1, keepdims=True)


def entropy_from_schmidt(s, clip: float = CLIP, bits: bool = False):
    return von_neumann(schmidt_to_probs(s), clip=clip, bits=bits)


def entropy_of_density(rho, clip: float = CLIP, bits: bool = False):
    """von Neumann entropy of a Hermitian density matrix via eigvalsh."""
    if _is_torch(rho):
        ev = torch.linalg.eigvalsh(rho)
    else:
        ev = np.linalg.eigvalsh(np.asarray(rho))
    return von_neumann(ev, clip=clip, bits=bits)
