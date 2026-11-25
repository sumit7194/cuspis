"""EXP-092 (registered a48bde4): c_A on the n = 1 box by a THIRD implementation (dense G_p inverses; streams over distinct |q|; no 085c code,
no sine modes, no Strip3D). [model: Opus 5.5]
c_A(z) = -4 term1(z) + 2 (B_0 Lambda)(z);  term1 = (1/Ny) sum_k diag(G_k M_k G_k);  M_k = (1/Ny) sum_q A_q o G_(k-q);  A_q = B_q^-1;
B_q = (2/Ny) sum_p G_p o G_(q-p);  Lambda = rowsum((1/Ny) sum_k A_k o G_k).  Box: Lx = 3P, Lt = 2P (Dirichlet), Ny = 4P sectors; site = x*Lt + t.
Usage:  KA            controls (KA-all P = 4, 6; KA-centre P = 8, 10, 12; must-fail plant) -> exit 1 on any FAIL
        P <P>         centre c_A at P (4 centre sites) -> exp081d_results/exp092_cA_P<P>.json"""
import sys, os, json, time, resource, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "exp081d_results")
def box(P):
    Lx, Lt, Ny = 3 * P, 2 * P, 4 * P; N = Lx * Lt; A = np.zeros((N, N))
    for x in range(Lx):
        for t in range(Lt):
            i = x * Lt + t
            if x + 1 < Lx: A[i, i + Lt] = A[i + Lt, i] = 1.0
            if t + 1 < Lt: A[i, i + 1] = A[i + 1, i] = 1.0
    return Lx, Lt, Ny, N, A
def cA_sites(P, Z, two=2.0):
    Lx, Lt, Ny, N, A = box(P); half = Ny // 2
    G = [np.linalg.inv(np.diag(np.full(N, 4.0 + 2.0 - 2.0 * np.cos(2 * np.pi * p / Ny))) - A) for p in range(half + 1)]
    ix = lambda k: min(k % Ny, Ny - k % Ny)
    Z = list(Z); term1 = np.zeros(len(Z)); Lam = np.zeros(N); B0Z = None
    for q in range(half + 1):
        m = 1 if q in (0, half) else 2
        B = np.zeros((N, N))
        for p in range(Ny): B += G[ix(p)] * G[ix(q - p)]
        B *= 2.0 / Ny
        if q == 0: B0Z = B[Z, :].copy()
        Aq = np.linalg.inv(B); del B
        Lam += m * (Aq * G[ix(q)]).sum(axis=1) / Ny
        for k in range(Ny):
            X = Aq * G[ix(k - q)]; GkZ = G[ix(k)][Z, :]
            term1 += m * np.sum((GkZ @ X) * GkZ, axis=1) / Ny ** 2
        del Aq
    return -4.0 * term1 + two * (B0Z @ Lam)
def centre(P): Lx, Lt = 3 * P, 2 * P; return [x * Lt + t for x in (Lx // 2 - 1, Lx // 2) for t in (Lt // 2 - 1, Lt // 2)]
def peak_GB(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes
FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:62s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
mode = sys.argv[1]
if mode == "KA":
    for P in (4, 6):
        ref = np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{P}P{P}.json")))["cA"]).real; t = time.time()
        v = cA_sites(P, range(len(ref))); dev = np.abs(v - ref).max() / np.abs(ref).max()
        check(f"KA-all P = {P} ({len(ref)} sites) vs stored office c_A (1e-10 rel)", dev <= 1e-10, f"max rel {dev:.1e} ({time.time()-t:.1f} s)")
    for P in (8, 10, 12):
        ref = np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{P}P{P}.json")))["cA"]).real; Zc = centre(P); t = time.time()
        v = cA_sites(P, Zc); dev = np.abs(v - ref[Zc]).max() / np.abs(ref[Zc]).max()
        check(f"KA-centre P = {P} vs stored office c_A (1e-10 rel)", dev <= 1e-10, f"max rel {dev:.1e}; centre {v.mean():+.10f} ({time.time()-t:.1f} s, peak {peak_GB():.2f} GB)")
    ref = np.array(json.load(open(os.path.join(D, "exp085c", "G_W4P4.json")))["cA"]).real
    v = cA_sites(4, range(len(ref)), two=1.0); dev = np.abs(v - ref).max() / np.abs(ref).max()
    check("must-fail plant (factor 2 -> 1 on B0 Lambda) at P = 4 FAILS the KA", dev > 1e-10, f"max rel {dev:.1e}")
    print(f"\nKA {'PASS' if not FAIL else FAIL}"); sys.exit(1 if FAIL else 0)
P = int(sys.argv[2]); Zc = centre(P); t = time.time(); v = cA_sites(P, Zc); sec = time.time() - t
sym = np.abs(v - v.mean()).max() / abs(v.mean())
print(f"P = {P}: centre c_A sites {[f'{x:+.12f}' for x in v]}  symmetry {sym:.1e} {'PASS' if sym <= 1e-12 else 'FAIL'}  ({sec:.0f} s, peak {peak_GB():.2f} GB)", flush=True)
print(f"P = {P}: centre c_A (mean of 4) = {v.mean():+.12f}")
json.dump(dict(P=P, sites=Zc, cA=[float(x) for x in v], centre=float(v.mean()), sym=float(sym), sec=sec, peak_GB=peak_GB()), open(os.path.join(D, f"exp092_cA_P{P}.json"), "w"), indent=1)
sys.exit(0 if sym <= 1e-12 else 1)
