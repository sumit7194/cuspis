"""EXP-034 (pre-registered in report.md, commit 6785173): P3 on the lattice.  MI per unit log scale between two thin wedges
(half-opening eta) with a common apex, for the pure Gaussian state with dispersion w(k) = [4 sin^2(kx/2) + 4 sin^2(ky/2)]^(alpha/2).
alpha = 1: free massless scalar (test); 1.5: Delta = 1/4 (must plateau: the test can fail); 0.5: Delta = 3/4 (fast decay).
Checkpointed: every entropy is appended to exp034_ckpt.jsonl and reused on restart.  Run with OMP/BLAS threads = 1."""
import json, os, sys, time
import numpy as np
from scipy.linalg import cholesky, eigvalsh

D = os.path.dirname(os.path.abspath(__file__))
CK = os.path.join(D, "exp034_ckpt.jsonl")
N = 4096
ALPHAS, ETAS, THETAS, RS = (1.0, 1.5, 0.5), (0.40, 0.25, 0.15), (90, 180), (40, 56, 80)
RMAX = 2 * max(RS) + 2

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def entropy(X, P):
    L = cholesky(X, lower=True, overwrite_a=True); del X
    M = L.T @ P; del P
    M = M @ L; del L
    nu = np.sqrt(np.clip(eigvalsh(M, overwrite_a=True, check_finite=False), 0.25, None)); del M
    a, b = nu + 0.5, nu - 0.5
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(b > 1e-300, b * np.log(b), 0.0)
    return float(np.sum(a * np.log(a) - t))

def tables(alpha, n=N, mass=0.0, keep=RMAX):
    """X, P corner tables (memory-lean: one inverse FFT at a time, full arrays freed at once; fix after the first launch
    was killed by the 2 GB watchdog cap at 17 s, before any result)."""
    k = 2 * np.pi * np.arange(n) / n
    s2 = 4 * np.sin(k / 2) ** 2
    w = (s2[:, None] + s2[None, : n // 2 + 1] + mass ** 2) ** (alpha / 2)
    keep = min(keep, n)
    with np.errstate(divide="ignore"):
        f = np.where(w > 0, 1 / (2 * w), 0.0)          # k = 0 excluded when massless
    full = np.fft.irfft2(f, s=(n, n)); del f
    X = full[:keep, :keep].copy(); Xs = full.copy() if n <= 64 else None; del full
    f = w / 2; del w
    full = np.fft.irfft2(f, s=(n, n)); del f
    P = full[:keep, :keep].copy(); Ps = full.copy() if n <= 64 else None; del full
    return X, P, Xs, Ps

def submat(T, sites):
    s = sites.astype(np.int16)
    return T[np.abs(s[:, None, 0] - s[None, :, 0]), np.abs(s[:, None, 1] - s[None, :, 1])]

def tables_cached(alpha):
    """Build the N = 4096 tables in a short-lived subprocess (frees FFT memory) and keep only the small corner."""
    f = os.path.join(D, f"exp034_tables_a{alpha}.npz")
    if not os.path.exists(f):
        import subprocess
        subprocess.run([sys.executable, "-c", f"import numpy as np, exp034_wedge_mi as m; X, P, _, _ = m.tables({alpha}); "
                        f"np.savez(r'{f}', X=X, P=P)"], cwd=D, check=True)
    z = np.load(f); return z["X"], z["P"]

def wedge(eta, R, axis):  # sites with r0 <= r <= R and |polar angle - axis| <= eta; built on +x then mapped by a lattice symmetry
    r0 = 2.0 / eta
    xs, ys = np.meshgrid(np.arange(0, R + 1), np.arange(-R, R + 1), indexing="ij")
    r = np.hypot(xs, ys); ang = np.arctan2(ys, xs)
    m = (r >= r0) & (r <= R) & (np.abs(ang) <= eta + 1e-12)
    s = np.stack([xs[m], ys[m]], axis=1)
    if axis == "+x": return s
    if axis == "-x": return np.stack([-s[:, 0], s[:, 1]], axis=1)
    if axis == "+y": return np.stack([s[:, 1], s[:, 0]], axis=1)
    raise ValueError(axis)

def load_ck():
    d = {}
    if os.path.exists(CK):
        for line in open(CK):
            j = json.loads(line); d[j["key"]] = j["S"]
    return d

def main():
    log(f"EXP-034 start; threads OMP={os.environ.get('OMP_NUM_THREADS')} VECLIB={os.environ.get('VECLIB_MAXIMUM_THREADS')}")
    # ---------- Tier 1: purity on a 24x24 periodic lattice (small mass so the state is pure), each alpha ----------
    for al in ALPHAS:
        _, _, Xf, Pf = tables(al, n=24, mass=0.3, keep=24)
        xy = np.array([(i, j) for i in range(24) for j in range(24)])
        A = xy[(xy[:, 0] < 9) & (xy[:, 1] < 13)]; Ac = xy[~((xy[:, 0] < 9) & (xy[:, 1] < 13))]
        def per(sites):
            dx = (sites[:, None, 0] - sites[None, :, 0]) % 24; dy = (sites[:, None, 1] - sites[None, :, 1]) % 24
            return Xf[dx, dy], Pf[dx, dy]
        sA, sAc = entropy(*per(A)), entropy(*per(Ac))
        rel = abs(sA - sAc) / sA
        log(f"Tier-1 purity alpha={al}: S(A)={sA:.10f} S(Ac)={sAc:.10f} rel diff {rel:.2e} [{'PASS' if rel < 1e-8 else 'FAIL'}]")
        if rel >= 1e-8: log("ABORT: purity check failed"); sys.exit(2)
    ck = load_ck(); fck = open(CK, "a")
    def S(key, fn):
        if key not in ck:
            t0 = time.time(); ck[key] = fn()
            fck.write(json.dumps({"key": key, "S": ck[key]}) + "\n"); fck.flush()
            log(f"  {key}: S = {ck[key]:.10f}  ({time.time() - t0:.0f} s)")
        return ck[key]
    for al in ALPHAS:
        t0 = time.time(); X, P = tables_cached(al)
        kc = (2 * np.pi / N) / np.sqrt(np.pi)
        ir = kc ** (2 - al) / (4 * np.pi * (2 - al))
        log(f"alpha={al}: tables built ({time.time() - t0:.0f} s); X(0)={X[0,0]:.6f}; est. missing k=0 cell contribution to X: {ir:.2e} ({ir / X[0,0]:.1%})")
        for eta in ETAS:
            for R in RS:
                g1 = wedge(eta, R, "+x")
                s1 = S(f"a{al}_e{eta}_R{R}_G1", lambda: entropy(submat(X, g1), submat(P, g1)))
                for th in THETAS:
                    g2 = wedge(eta, R, "+y" if th == 90 else "-x")
                    if R == RS[0]:   # Tier-1 symmetry check: S(G2) computed separately equals S(G1)
                        s2 = S(f"a{al}_e{eta}_R{R}_G2_th{th}", lambda: entropy(submat(X, g2), submat(P, g2)))
                        log(f"Tier-1 symmetry alpha={al} eta={eta} th={th}: |S(G1)-S(G2)|/S = {abs(s1 - s2) / s1:.1e} [{'PASS' if abs(s1 - s2) / s1 < 1e-8 else 'FAIL'}]")
                    u = np.concatenate([g1, g2])
                    log(f"  alpha={al} eta={eta} R={R} th={th}: |G1|={len(g1)} |G1uG2|={len(u)}")
                    S(f"a{al}_e{eta}_R{R}_U_th{th}", lambda: entropy(submat(X, u), submat(P, u)))
        del X, P
    log("all entropies done; analysis:")
    analyse(ck)

def analyse(ck):
    lr = np.log(np.array(RS, float))
    iG = {}
    for al in ALPHAS:
        for eta in ETAS:
            for th in THETAS:
                I = np.array([2 * ck[f"a{al}_e{eta}_R{R}_G1"] - ck[f"a{al}_e{eta}_R{R}_U_th{th}"] for R in RS])
                slope = np.polyfit(lr, I, 1)[0]
                two = np.diff(I) / np.diff(lr)
                iG[(al, eta, th)] = slope
                log(f"alpha={al} eta={eta:.2f} th={th}: I(R) = {np.round(I, 6)}  slope (LSQ) = {slope:.6f}  two-point slopes = {np.round(two, 6)}")
    log("verdict quantities (frozen criteria in report.md EXP-034):")
    for al in ALPHAS:
        for th in THETAS:
            r = iG[(al, ETAS[-1], th)] / iG[(al, ETAS[0], th)]
            log(f"  r_alpha={al} (theta={th}) = i_G(0.15)/i_G(0.40) = {r:.4f}")
    for eta in (ETAS[0], ETAS[-1]):
        log(f"  scalar |i_G(90)-i_G(180)| at eta={eta}: {abs(iG[(1.0, eta, 90)] - iG[(1.0, eta, 180)]):.6f}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--analyse":
        analyse(load_ck())
    else:
        main()
