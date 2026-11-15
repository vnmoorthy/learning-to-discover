"""Independent re-derivation of the upgrade's headline numbers (Tracks A-F).

Separate code path: numpy only; imports nothing from eh/ or experiments/.
Run:  /opt/anaconda3/bin/python3 verify/independent_upgrade.py
Writes results/verification_upgrade.json.  Seed 20261116 (numpy default_rng).
"""
import itertools, json, os, time
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(20261116)
out = {"seed": 20261116, "script": "verify/independent_upgrade.py", "checks": []}


def gauss_state(d):
    v = rng.normal(size=d) + 1j * rng.normal(size=d)
    return v / np.linalg.norm(v)


def haar_unitary(d):
    z = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


# ---- V1: Lubkin purity and exact third moment (Track A, eh/renyi.py) ----
t0 = time.time()
rows = []
for dA, dB, ns in [(4, 4, 20000), (8, 8, 20000), (8, 32, 10000)]:
    p2, p3 = [], []
    for _ in range(ns):
        M = gauss_state(dA * dB).reshape(dA, dB)
        s = np.linalg.svd(M, compute_uv=False) ** 2
        p2.append((s ** 2).sum()); p3.append((s ** 3).sum())
    p2, p3 = np.array(p2), np.array(p3)
    D = dA * dB
    e2 = (dA + dB) / (D + 1)
    e3 = (dA ** 2 + 3 * D + dB ** 2 + 1) / ((D + 1) * (D + 2))
    rows.append({"dA": dA, "dB": dB, "samples": ns,
                 "mc_purity": p2.mean(), "exact_purity": e2,
                 "z_purity": (p2.mean() - e2) / (p2.std(ddof=1) / np.sqrt(ns)),
                 "mc_tr_rho3": p3.mean(), "exact_tr_rho3": e3,
                 "z_tr_rho3": (p3.mean() - e3) / (p3.std(ddof=1) / np.sqrt(ns))})
# builder's stored S_2 at N=12 half cut: -log Lubkin(64,64)
fs = json.load(open(os.path.join(ROOT, "results/f_spectra.json")))
lub = fs["C_ensembles"]["N12"]["exact"]["lubkin_purity"]
mine = [(2 ** k + 2 ** (12 - k)) / (2 ** 12 + 1) for k in range(13)]
maxdiff = float(np.max(np.abs(np.array(lub) - np.array(mine))))
out["checks"].append({"id": "V1", "claim": "E Tr rho^2 = (dA+dB)/(dA dB+1) (Lubkin) and E Tr rho^3 = (dA^2+3dAdB+dB^2+1)/((D+1)(D+2)); builder's stored exact purity table at N=12",
                      "rows": rows, "max_abs_diff_stored_lubkin_N12": maxdiff,
                      "agree": bool(all(abs(r["z_purity"]) < 4 and abs(r["z_tr_rho3"]) < 4 for r in rows) and maxdiff < 1e-12),
                      "runtime_s": time.time() - t0})

# ---- V2: [[5,1,3]] perfect-code erasure (Track E, eh/qec.py) ----
t0 = time.time()
I2 = np.eye(2); X = np.array([[0, 1], [1, 0]], complex); Z = np.diag([1., -1.]).astype(complex)
P = {"I": I2, "X": X, "Z": Z}


def pauli(s):
    m = np.array([[1.]], complex)
    for c in s:
        m = np.kron(m, P[c])
    return m


gens = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
proj = np.eye(32, dtype=complex)
for g in gens:
    proj = proj @ (np.eye(32) + pauli(g)) / 2
w, v = np.linalg.eigh(proj)
code = v[:, w > 0.5]                      # 32 x 2 isometry (some logical basis)
psi = np.zeros((2, 32), complex)          # reference R (qubit) x 5 physical
psi[0] = code[:, 0] / np.sqrt(2); psi[1] = code[:, 1] / np.sqrt(2)
T = psi.reshape([2] + [2] * 5)


def S_bits(rho):
    e = np.linalg.eigvalsh(rho); e = e[e > 1e-12]
    return float(-(e * np.log2(e)).sum())


def red(keep):  # keep: list of tensor axes (0 = R, 1..5 physical)
    other = [a for a in range(6) if a not in keep]
    A = np.transpose(T, keep + other).reshape(2 ** len(keep), -1)
    return A @ A.conj().T


bad = 0; table = {}
for r in range(1, 5):
    vals = []
    for A in itertools.combinations(range(1, 6), r):
        A = list(A)
        I = S_bits(red([0])) + S_bits(red(A)) - S_bits(red([0] + A))
        vals.append(I)
        want = 2.0 if r >= 3 else 0.0
        bad += abs(I - want) > 1e-9
    table[str(r)] = [min(vals), max(vals)]
out["checks"].append({"id": "V2", "claim": "[[5,1,3]]: I(R:A) = 2 bits for |A| >= 3 and 0 for |A| <= 2 (perfect tensor), stabilizers built from scratch",
                      "I_RA_minmax_by_size": table, "violations": int(bad), "agree": bad == 0,
                      "runtime_s": time.time() - t0})

# ---- V3: Haar OTOC average -1/(d^2-1) (Track D, eh/otoc.py) ----
t0 = time.time()
N = 3; d = 2 ** N; ns = 4000
W = pauli("XII"); V = pauli("IIZ")
F = []
for _ in range(ns):
    U = haar_unitary(d)
    Wt = U.conj().T @ W @ U
    F.append(np.trace(Wt @ V @ Wt @ V).real / d)
F = np.array(F)
pred = -1 / (d ** 2 - 1)
z = (F.mean() - pred) / (F.std(ddof=1) / np.sqrt(ns))
out["checks"].append({"id": "V3", "claim": "Haar-averaged infinite-temperature OTOC of non-identity Paulis = -1/(d^2-1)",
                      "N": N, "samples": ns, "mc_mean": F.mean(), "stderr": F.std(ddof=1) / np.sqrt(ns),
                      "prediction": pred, "z": z, "agree": bool(abs(z) < 4), "runtime_s": time.time() - t0})

# ---- V4: stabilizer-state counts 6, 60, 1080 by Clifford-orbit BFS (Track B, eh/rmt.py) ----
t0 = time.time()
H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2); Sg = np.diag([1, 1j])


def canon(s):
    i = np.argmax(np.abs(s) > 1e-9)
    s = s * (abs(s[i]) / s[i])
    return tuple(np.round(s, 6).view(float))


def count(n):
    gates = []
    for q in range(n):
        for g in (H, Sg):
            m = np.array([[1.]], complex)
            for j in range(n):
                m = np.kron(m, g if j == q else I2)
            gates.append(m)
    for a in range(n):
        for b in range(n):
            if a != b:
                dim = 2 ** n; C = np.zeros((dim, dim))
                for x in range(dim):
                    bits = [(x >> (n - 1 - j)) & 1 for j in range(n)]
                    if bits[a]: bits[b] ^= 1
                    y = sum(bit << (n - 1 - j) for j, bit in enumerate(bits)); C[y, x] = 1
                gates.append(C.astype(complex))
    s0 = np.zeros(2 ** n, complex); s0[0] = 1
    seen = {canon(s0)}; frontier = [s0]
    while frontier:
        nxt = []
        for s in frontier:
            for g in gates:
                t = g @ s; k = canon(t)
                if k not in seen:
                    seen.add(k); nxt.append(t)
        frontier = nxt
    return len(seen)


counts = {n: count(n) for n in (1, 2, 3)}
formula = {n: int(2 ** n * np.prod([2 ** k + 1 for k in range(1, n + 1)])) for n in (1, 2, 3)}
out["checks"].append({"id": "V4", "claim": "Number of n-qubit stabilizer states = 2^n prod_k (2^k+1): 6, 60, 1080 for n = 1..3",
                      "bfs_counts": counts, "formula": formula, "agree": counts == formula,
                      "runtime_s": time.time() - t0})

# ---- V5: old-hole Hayden-Preskill Petz fidelity, k = 1, n_B = 3, m = 1 (Track C, eh/recovery.py) ----
t0 = time.time()
k, nB, m = 1, 3, 1
dQ = dM = 2 ** k; dB = dR = 2 ** nB; dD = 2 ** m; dBp = dM * dB // dD
Fs = []
gr = json.load(open(os.path.join(ROOT, "results/g_recovery.json")))
for _ in range(48):
    U = haar_unitary(dM * dB)
    # |Phi>_QM |Phi>_BR, U on (M B) -> (B' D); amplitudes psi[q, r, out]
    phi = np.zeros((dQ, dM, dB, dR), complex)
    for q in range(dQ):
        for b in range(dB):
            phi[q, q, b, b] = 1 / np.sqrt(dQ * dB)
    a = np.einsum("oi,qir->qro", U, phi.reshape(dQ, dM * dB, dR))
    a = a.reshape(dQ, dR, dBp, dD)                      # output = (B', D), D = last m qubits
    A = np.transpose(a, (0, 1, 3, 2)).reshape(dQ * dR * dD, dBp)   # (Q R D) x B'
    rQX = A @ A.conj().T
    rX = np.einsum("qxqy->xy", rQX.reshape(dQ, dR * dD, dQ, dR * dD))
    w, vv = np.linalg.eigh(rX); w = np.clip(w, 0, None)
    inv = vv @ np.diag(np.where(w > 1e-12, w ** -0.5, 0)) @ vv.conj().T
    Mx = rQX @ np.kron(np.eye(dQ), inv)
    Fs.append(np.trace(Mx @ Mx).real / dM)
Fs = np.array(Fs)
out["checks"].append({"id": "V5", "claim": "Old-hole Petz entanglement fidelity, Haar scrambler, k=1, n_B=3, m-k=0: builder 0.765 (24 seeds)",
                      "formula_note": "same Petz formula F=(1/d_M)Tr[(rho_QX (1 x rho_X^-1/2))^2], independent state construction, Haar sampler, partial traces and seed",
                      "mc_mean": Fs.mean(), "stderr": Fs.std(ddof=1) / np.sqrt(len(Fs)), "samples": len(Fs),
                      "builder_value": 0.765, "agree": bool(abs(Fs.mean() - 0.765) < 4 * Fs.std(ddof=1) / np.sqrt(len(Fs)) + 0.01),
                      "runtime_s": time.time() - t0})

out["agree"] = sum(c["agree"] for c in out["checks"]); out["checked"] = len(out["checks"])


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o


json.dump(clean(out), open(os.path.join(ROOT, "results/verification_upgrade.json"), "w"), indent=1)
for c in out["checks"]:
    print(c["id"], c["agree"], {k: v for k, v in c.items() if k in ("z", "mc_mean", "violations", "bfs_counts", "max_abs_diff_stored_lubkin_N12")})
print("agree", out["agree"], "/", out["checked"])
