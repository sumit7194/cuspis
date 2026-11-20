"""EXP-051 (pre-registered in report.md, e6e9360): 2D Euclidean lattice twisted-propagator solver vs EXP-044's Fredholm
w_S(b, t). Real scalar (= 1/2 complex), monodromy phi+ = lam phi- across an interval cut of r links, lam = -e^{2 pi b}
(CH07b's bosonic Z[-lam]); the complex-field operator with unitary twist has A[a,b] = -lam, A[b,a] = -conj(lam) = -1/lam,
continued analytically to real lam. log Z = -1/2 log|det A_lam| + (r-free const); w = r d/dr log Z at fixed m = t/r.
[model: Opus 5.5]   Usage: python exp051_twisted_lattice.py tier1 | run"""
import sys, math, time, json, os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu

D0 = os.path.dirname(os.path.abspath(__file__))

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def logdet_twisted(m, r, lam, box):
    Ly = Lx = box; n = Lx * Ly
    idx = lambda i, j: i * Lx + j
    i0 = Ly // 2 - 1; j0 = (Lx - r) // 2
    rows, cols, vals = [], [], []
    diag = np.full(n, 4.0 + m * m)
    I, J = np.meshgrid(np.arange(Ly), np.arange(Lx), indexing="ij"); I = I.ravel(); J = J.ravel(); S = I * Lx + J
    # horizontal links (j, j+1): never cut
    msk = J < Lx - 1
    rows += [S[msk], S[msk] + 1]; cols += [S[msk] + 1, S[msk]]; vals += [-np.ones(msk.sum()), -np.ones(msk.sum())]
    # vertical links (i, i+1): cut between rows i0 and i0+1 for j in [j0, j0+r)
    msk = I < Ly - 1
    a_up = S[msk] + Lx; b_dn = S[msk]                                  # site above (row i+1) and below (row i)
    cut = (I[msk] == i0) & (J[msk] >= j0) & (J[msk] < j0 + r)
    w_ab = np.where(cut, lam, 1.0); w_ba = np.where(cut, 1.0 / lam, 1.0)
    rows += [a_up, b_dn]; cols += [b_dn, a_up]; vals += [-w_ab, -w_ba]
    A = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)) + sp.diags(diag)
    lu = splu(A.tocsc())
    d = lu.U.diagonal()
    return float(np.sum(np.log(np.abs(d)))), int(np.sum(d < 0) % 2)

def w_lat(t, r, b, sign=-1.0):
    m = t / r; lam = sign * math.exp(2 * math.pi * b)
    box = int(max(6 * r, math.ceil(12 / m))); box += box % 2
    lp, sp_ = logdet_twisted(m, r + 1, lam, box); lm, sm = logdet_twisted(m, r - 1, lam, box)
    return r * (-0.5) * (lp - lm) / 2.0, box, (sp_, sm)

def w_rich(t, r1, b, sign=-1.0):
    a, box1, s1 = w_lat(t, r1, b, sign); c, box2, s2 = w_lat(t, 2 * r1, b, sign)
    rich = (4 * c - a) / 3
    return rich, a, c, 3 * abs(rich - c) + 1e-4, (box1, box2, s1, s2)

def w_det_pred(t, b):
    sys.path.insert(0, D0)
    import exp044_det as E
    return +0.5 * E.w_scalar(t, 0.5 + 1j * b)[0].real   # amended after Tier 1 (report.md EXP-051): real field = 1/2 complex, Z_lat = CH05 Z_a

def tier1():
    log("EXP-051 Tier 1: one point, small r")
    t, r, b = 1.0, 8, 0.5
    t0 = time.time(); rich, a, c, tol, info = w_rich(t, r, b); el = time.time() - t0
    p = w_det_pred(t, b)
    log(f"  t={t} b={b} r={r},{2*r}: w_lat {a:.6f}, {c:.6f} -> Richardson {rich:.6f} (tol {tol:.1e}); prediction -1/2 w_det = {p:.6f}; "
        f"diff {rich-p:+.2e}; boxes {info[0]},{info[1]}; det-sign parities {info[2]},{info[3]}  [{el:.1f} s]")

def run():
    out = {}; ok = True
    for t, r in ((1.0, 16), (3.0, 16)):
        for b in (0.0, 0.5, 1.0):
            t0 = time.time(); rich, a, c, tol, info = w_rich(t, r, b); p = w_det_pred(t, b)
            good = abs(rich - p) <= tol; ok &= good
            out[f"t{t}_b{b}"] = dict(rich=rich, r=a, r2=c, tol=tol, pred=p)
            log(f"  t={t} b={b}: lattice r={r}: {a:.6f}  2r: {c:.6f}  Richardson {rich:.6f} | prediction {p:.6f} | diff {rich-p:+.2e} tol {tol:.1e} "
                f"[{'PASS' if good else 'FAIL'}]  boxes {info[0]},{info[1]} ({time.time()-t0:.0f} s)")
    log(f"PREDICTION {'PASS' if ok else 'FAIL'}")
    t, b, r = 1.0, 0.5, 16
    rich, a, c, tol, info = w_rich(t, r, b, sign=+1.0); p = w_det_pred(t, b)
    fires = abs(rich - p) > 10 * out[f"t{t}_b{b}"]["tol"]
    log(f"must-fail (lam = +e^(2 pi b), fermionic sign) t={t} b={b}: lattice {rich:.6f} vs bosonic prediction {p:.6f}: miss {abs(rich-p):.2e} "
        f"[{'PASS (control fires)' if fires else 'FAIL (control does not fire)'}]")
    out["mustfail"] = dict(rich=rich, pred=p, fires=bool(fires))
    json.dump(out, open(os.path.join(D0, "exp051_results.json"), "w"), indent=1)

if __name__ == "__main__":
    {"tier1": tier1, "run": run}[sys.argv[1]]()
