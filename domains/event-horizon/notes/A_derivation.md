# Problem A — why a random pure state gives a Page curve

Classification: **1 (reproduction)** of Page 1993 (PRL 71, 1291; PRL 71, 3743). Finite-dimensional
quantum information only; nothing here uses or tests gravity.

## 1. Schmidt decomposition ⇒ equal spectra ⇒ S(R) = S(B)

Let |ψ⟩ ∈ H_R ⊗ H_B with dim H_R = m, dim H_B = n. Write ψ = Σ_{ab} M_{ab} |a⟩_R |b⟩_B with M an m×n complex
matrix, Tr(M M†) = 1. The singular value decomposition M = U diag(s) V† (s_i ≥ 0, i = 1..min(m,n)) gives

  |ψ⟩ = Σ_i s_i |u_i⟩_R |v_i⟩_B ,  Σ_i s_i² = 1   (Schmidt decomposition),

with {u_i} orthonormal in H_R and {v_i} orthonormal in H_B. Tracing out one side,

  ρ_R = Tr_B |ψ⟩⟨ψ| = M M† = Σ_i s_i² |u_i⟩⟨u_i| ,  ρ_B = Tr_R |ψ⟩⟨ψ| = (M† M)^T = Σ_i s_i² |v_i⟩⟨v_i| .

Both reduced states have the same non-zero eigenvalues p_i = s_i² (the larger one has |m−n| extra zeros), so every
spectral function agrees; in particular

  S(R) = S(B) = −Σ_i p_i ln p_i ,  and  S ≤ ln min(m, n).

Numerically (tests 8, 9; `experiments/a_page_curve.py`): |S(R) − S(B)| ≤ 1e-10 in all cases, typically 1e-15.

## 2. A random global state is almost maximally entangled

Take N qubits, R = k of them, B = the other N−k, so m = 2^k, n = 2^{N−k}; let |ψ⟩ be Haar-random.
Assume k ≤ N/2 (otherwise swap R ↔ B using §1).

*Purity argument (elementary).* For Haar states E[ψψ† ⊗ ψψ†] = (1 + SWAP)/(D(D+1)), D = mn, which gives
(Lubkin 1978)

  E[Tr ρ_R²] = (m + n)/(mn + 1).

By Jensen's inequality and S ≥ S₂ = −ln Tr ρ²,

  E[S(R)] ≥ −ln E[Tr ρ_R²] = ln m − ln( (1 + m/n)/(1 + 1/(mn)) ) ≥ ln m − m/n .

So E[S(R)] lies within m/n = 2^{2k−N} nats of its maximum k ln 2: exponentially close when k < N/2 and within
O(1) at k = N/2.

*Exact mean (Page's formula).* Page conjectured, and Foong–Kanno (1994), Sánchez-Ruiz (1995) and Sen (1996)
proved, for m ≤ n

  ⟨S_{m,n}⟩ = Σ_{j=n+1}^{mn} 1/j − (m−1)/(2n) = H_{mn} − H_n − (m−1)/(2n).

Using H_x = ln x + γ + 1/(2x) − 1/(12x²) + 1/(120x⁴) − … (Euler–Maclaurin):

  ⟨S_{m,n}⟩ = ln m − m/(2n) + 1/(2mn) + (1 − 1/m²)/(12n²) − (1 − 1/m⁴)/(120 n⁴) + … .

(The first two terms are Page's large-n form; the remaining terms are an elementary consequence of the exact
formula, checked symbolically with SymPy and against exact rational arithmetic in `eh/page.py::sympy_verify_asymptotic`.)

## 3. The Page curve

With m = 2^{min(k, N−k)}, n = 2^{max(k, N−k)}:

  ⟨S(R_k)⟩ = min(k, N−k) ln 2 − 2^{−|N−2k|}/2 + O(2^{−N})

* k < N/2: S(R) ≈ k ln 2 — the radiation looks thermal (maximally mixed), entropy **rises** one bit per qubit.
* k = N/2 ("Page time"): deficit is 1/2 nat − O(2^{−N}) for even N (≈ 0.72 bit); for odd N at k = (N∓1)/2 it is 1/4 nat.
* k > N/2: by §1, S(R) = S(B) ≤ (N−k) ln 2 — the entropy **falls** back to 0 at k = N because the global state is pure.

The rise-and-fall is therefore a consequence of only two ingredients: purity of the global state (S(R) = S(B), §1)
and typicality (random states nearly saturate the bound ln min(m,n), §2). Fluctuations around the mean are
exponentially small in N (seen numerically: the std over seeds shrinks with N; measure concentration).

## 4. What this does and does not say

It says: *if* evaporation is unitary and scrambling so that the radiation + hole state is typical, the
fine-grained radiation entropy follows this curve. It does not show that real black holes do this, and it
is logically separate from the semiclassical-gravity derivations of a Page curve via quantum extremal
surfaces/islands (Penington 2019; Almheiri–Engelhardt–Marolf–Maxfield 2019), which involve no random-state
assumption on a qubit Hilbert space.

## 5. Numerical result (A100, complex128)

`experiments/a_page_curve.py`: N = 8..20 plus N = 22, 24; every cut k = 0..N of each sampled state;
400 Haar states per N for N <= 14, 200 (N = 15, 16), 100 (17, 18), 50 (19, 20), 16 (N = 22), 8 (N = 24);
seed rule `torch.Generator(cuda).manual_seed(1000 + N)`. Numbers in `results/a_page_curve.json`,
figure `figures/a_page_curve.png`.

* 213 cells (N, k) with 0 < k < N: max |mean - Page| / stderr = 3.38 (at N = 24, where only 8 states were
  sampled, so the stderr itself is poorly estimated); for N <= 20 the maximum is 2.66. rms z = 1.05,
  6.6 % of cells have |z| > 2 (5 % expected for independent Gaussian z; cuts of the same state are correlated).
* max |mean - Page| = 1.6e-3 nats (N = 8) falling to 1.0e-4 nats (N = 20) and 2.6e-5 nats (N = 24).
* max |S(R) - S(B)| = 5.3e-15 nats, with S(B) from an independent eigvalsh of rho_B whenever the larger
  side has dimension <= 2048 (for larger cuts the two are equal by construction and not an independent check).
* Units: nats; divide by ln 2 for bits (both are stored in the JSON).
