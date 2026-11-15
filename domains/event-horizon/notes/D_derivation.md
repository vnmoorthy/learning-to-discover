# Problem D — Bell-pair "Hawking" toy model

Classification: **1 (reproduction)** of the textbook qubit caricature of Hawking's argument
(information-losing pair production). Not a calculation in semiclassical gravity.

## Model
A hole formed from matter in a pure state |χ⟩_M. Emission j creates a fresh Bell pair
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2 on (r_j, p_j): r_j flies out (radiation), p_j is the interior partner.
After k emissions

  |Ψ_k⟩ = |χ⟩_M ⊗ |Φ⁺⟩_{r_1 p_1} ⊗ … ⊗ |Φ⁺⟩_{r_k p_k}.

## S(R) = k ln 2 exactly
Tr_{p_j} |Φ⁺⟩⟨Φ⁺| = I/2. The global state is a tensor product, so the partial trace factorises:

  ρ_R = Tr_{M, p_1..p_k} |Ψ_k⟩⟨Ψ_k| = (I/2)^{⊗k} = I/2^k .

Spectrum: 2^k eigenvalues all equal to 2^{-k}. Hence S(R) = ln 2^k = k ln 2 (k bits), purity 2^{-k},
all Rényi entropies equal k ln 2; S is strictly monotone in k and never turns over. Numerically
(`experiments/d_hawking_pairs.py`, explicit state vectors up to 16 qubits) |S − k ln 2| is at round-off level,
I(r_i : r_j) = 0, I(r_j : p_j) = 2 bits.

## The conflict after the Page time
If the hole's coarse-grained (Bekenstein–Hawking-like) entropy in the toy model is the log of the dimension
of what remains, S_BH(k) = (N − k) ln 2, then a hole whose fine-grained entropy is bounded by S_BH must satisfy
S(R) = S(interior) ≤ (N − k) ln 2 for a pure total state. The pair model gives

  S(R) − S_BH = (2k − N) ln 2 > 0  for k > N/2 ,

i.e. it violates the bound for every k after the Page time k = N/2, by up to N ln 2 at the end, where a
"hole" of zero remaining qubits would have to purify N bits of radiation (or the final state is mixed:
pure → mixed, information loss). The unitary model of Problem C instead has S(R) ≤ min(k, N−k) ln 2 and returns to 0.

## Exactly which assumptions produce the difference
* **A1 – independent pairs.** Each emission is created in a product state with the matter and all earlier
  pairs; the emission process never acts on the hole's existing degrees of freedom. (In C the emitted qubit
  is one of the hole's own qubits after a unitary on the whole remaining hole.)
* **A2 – no correlations among radiation quanta.** ρ_R is exactly a product (I/2)^{⊗k}; I(r_i : r_j) = 0.
  In C the late radiation is strongly correlated with the early radiation — that is how S(R) decreases.
* **A3 – partners stay behind the horizon.** The purification of R is the set {p_j}, which is never emitted;
  the interior Hilbert space effectively *grows* by one qubit per emission (dimension 2^{N+k}).
* **A4 – yet the hole is assumed to shrink.** Only when A1–A3 are combined with a shrinking entropy budget
  (N − k) ln 2 for the hole is there a contradiction. Without A4 (a remnant with unbounded interior
  capacity) the model is consistent but the hole never loses its entropy.

In the unitary model the total dimension is fixed at 2^N and the emitted qubits are taken *out of* the hole
(negating A1, A3), so correlations between radiation quanta are forced (negating A2).
The toy comparison identifies which assumptions conflict; it does not decide which one nature gives up,
and it is separate from the semiclassical island computations (Penington 2019; Almheiri et al. 2019).
