"""EXP-039 (pre-registered in report.md): cancellation-free wedge MI for Delta = 0.9 (alpha = 0.2), closing the EXP-038
Part C void.  Same state, same circle discretisation, same s-quadrature as EXP-035/038; the only change is that the three
entropies in I_s = 2 S(G1) - S(G1 u G2) are evaluated in 35-digit arithmetic (mpmath: Cholesky, L^T P L, symmetric
eigenproblem) from the double-precision X, P blocks.  Rationale: the inputs carry the cross-correlation to ~1e-10 relative;
the precision was lost only in the subtraction of O(1-10) entropies to leave I ~ 1e-11."""
import json, os, sys, time
import numpy as np, mpmath as mp
from numpy.polynomial.legendre import leggauss
import exp035_cylinder_mi as e35

D0 = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D0, "exp039_results.json")
PLAN = ((1e-3, (32, 64)), (1e-4, (32, 64)), (1e-5, (16, 32)))

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def S_mp(X, P, dps=35):
    with mp.workdps(dps):
        L = mp.cholesky(mp.matrix(X.tolist())); M = L.T * mp.matrix(P.tolist()) * L
        s = mp.mpf(0); q = mp.mpf(1) / 4; h = mp.mpf(1) / 2
        for v in mp.eigsy(M, eigvals_only=True):
            nu = mp.sqrt(v if v > q else q); a, b = nu + h, nu - h
            s += a * mp.log(a) - (b * mp.log(b) if b > 0 else 0)
        return s

def blk(row, idx, M):
    d = np.abs(idx[:, None] - idx[None, :]); d = np.minimum(d, M - d); return row[d]

def mi_mp(al, s, n_p, M, dps=35):
    x, p = e35.rows(al, s, M); a = np.arange(n_p)
    s1 = S_mp(blk(x, a, M), blk(p, a, M), dps); out = []
    for sep in (M // 4, M // 2):
        u = np.concatenate([a, a + sep]); out.append(2 * s1 - S_mp(blk(x, u, M), blk(p, u, M), dps))
    return [float(v) for v in out]

def iG_mp(al, eta, n_p, nodes, dps=35):
    M, ee = e35.geometry(eta, n_p)
    t, w = leggauss(nodes); t = 0.5 * (t + 1); w = 0.5 * w; s = t / (1 - t); jac = 1 / (1 - t) ** 2
    acc = np.zeros(2)
    for si, wi, ji in zip(s, w, jac):
        acc += wi * ji * np.array(mi_mp(al, si, n_p, M, dps))
    return acc / np.pi, M

def validate():
    # V1: per-s agreement with double precision where double is reliable (I_s >= 1e-6)
    for al, eta in ((0.2, 0.1), (0.8, 0.001)):
        M, _ = e35.geometry(eta, 32)
        for s in (0.0, 0.8, 2.5):
            x, p = e35.rows(al, s, M); d = e35.mi_both(x, p, 32, M); m = mi_mp(al, s, 32, M)
            for th, a, b in zip((90, 180), d, m):
                if a >= 1e-6:
                    r = abs(a / b - 1)
                    log(f"V1 alpha={al} eta={eta} s={s} th={th}: double {a:.12e} mp {b:.12e} rel {r:.1e} [{'PASS' if r < 1e-6 else 'FAIL'}]")
                    if r >= 1e-6: sys.exit(2)
    # V2: precision gate at the smallest eta: dps 35 vs 50
    M, _ = e35.geometry(1e-5, 32)
    for s in (0.0, 1.0, 4.0):
        a, b = mi_mp(0.2, s, 32, M, 35), mi_mp(0.2, s, 32, M, 50)
        r = max(abs(a[i] / b[i] - 1) for i in range(2))
        log(f"V2 alpha=0.2 eta=1e-5 s={s}: dps35 {a}  dps50 {b}  max rel {r:.1e} [{'PASS' if r < 1e-8 else 'FAIL'}]")
        if r >= 1e-8: sys.exit(3)
    # V3: reproduce an EXP-038 double-precision i_G where double was reliable (Delta = 0.6, eta = 1e-4, n_p = 32)
    ref = json.load(open(os.path.join(D0, "exp038_partC.json")))["a0.8_e0.0001_np32"]
    v, _ = iG_mp(0.8, 1e-4, 32, 96)
    r = max(abs(v[0] / ref["i90"] - 1), abs(v[1] / ref["i180"] - 1))
    log(f"V3 Delta=0.6 eta=1e-4 n_p=32: mp {v}  EXP-038 double {[ref['i90'], ref['i180']]}  max rel {r:.1e} [{'PASS' if r < 1e-6 else 'FAIL'}]")
    if r >= 1e-6: sys.exit(4)

def main():
    log("EXP-039 start"); validate()
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    jobs = [(eta, n_p, 96) for eta, nps in PLAN for n_p in nps] + [(1e-3, 64, 48)]
    for eta, n_p, q in jobs:
        k = f"e{eta}_np{n_p}_q{q}"
        if k in res: continue
        t0 = time.time(); v, M = iG_mp(0.2, eta, n_p, q)
        res[k] = {"i90": v[0], "i180": v[1], "M": M}; json.dump(res, open(OUT, "w"), indent=0)
        log(f"  {k}: M={M} i_G={v} ({time.time() - t0:.0f} s)")
    analyse(res)

def analyse(res):
    p_pred, tol = 1.6, 0.10
    for th in ("i90", "i180"):
        q = abs(res["e0.001_np64_q48"][th] / res["e0.001_np64_q96"][th] - 1)
        dr = [abs(res[f"e{e}_np{a}_q96"][th] / res[f"e{e}_np{b}_q96"][th] - 1) for e, (a, b) in PLAN]
        g = lambda e: res[f"e{e}_np{dict(PLAN)[e][1]}_q96"][th]
        p1 = np.log(g(1e-3) / g(1e-4)) / np.log(10); p2 = np.log(g(1e-4) / g(1e-5)) / np.log(10)
        ok = q < 1e-3 and max(dr) < 0.02
        log(f"Delta=0.9 {th}: gates quad {q:.1e}, n_p drift {[f'{x:.1e}' for x in dr]} [{'PASS' if ok else 'FAIL'}];  "
            f"i_G = {g(1e-3):.6e}, {g(1e-4):.6e}, {g(1e-5):.6e}")
        log(f"    p(1e-3->1e-4) = {p1:.4f};  p(1e-4->1e-5) = {p2:.4f};  predicted 1.6  |p2-1.6| = {abs(p2 - p_pred):.4f} <= {tol}: "
            f"[{'PASS' if ok and abs(p2 - p_pred) <= tol else ('FAIL' if ok else 'VOID (gates)')}]")

if __name__ == "__main__":
    analyse(json.load(open(OUT))) if sys.argv[1:] == ["--analyse"] else main()
