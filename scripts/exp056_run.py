"""EXP-056 run (pre-registered in report.md, 3696364): gap (c) zero counts + EXP-055 closed-form promotion. [model: Opus 5.5]"""
import sys, os, time, json, math
import numpy as np
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import exp056_sigma_kernel as K
import exp053_cone_gap as G
from mpmath import mpf

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def count(n, al, q, npts=24, kre=6.0, delta=0.05, width=1.0, planted=None):
    kth = K.threshold(n, al, q); top = kth - delta
    R, Wt = K.rho_grid_fine(min(600.0, 40.0 / delta), width=width)
    Ws, sig, _ = K.weight_scaled(n, al, q, R, Wt)            # overflow-safe form (run 3 hit NaN at q = 2, n ~ 1)
    f = lambda k: K.Bks(R, Ws, sig, k)
    c = f(planted) if planted is not None else 0.0
    rect = [0.0 + 0.0j, kre + 0.0j, kre + 1j * top, 0.0 + 1j * top]
    wnd = K.winding(lambda k: f(k) - c, rect, npts=npts)
    # diagnostics: min |B| on the contour, and B on the imaginary axis near the top
    return wnd, kth, top, abs(f(1j * top)) * np.exp(sig * 0)  # |B e^{0}| at rho-weighting; diagnostic only

def main():
    out = {}; ok1 = True
    alphas = {n: float(G.root(mpf(n))) for n in (1.05, 1.25, 2.0, 3.0)}
    log("alpha_n:", {k: round(v, 10) for k, v in alphas.items()})
    for n in (1.05, 1.25, 2.0, 3.0):
        for q in (1, 2):
            t0 = time.time(); w, kth, top, btop = count(n, alphas[n], q)
            good = abs(w) <= 0.05; ok1 &= good
            out[f"n{n}_q{q}"] = dict(winding=w, kappa0=kth, top=top)
            log(f"P1 n={n} q={q}: kappa0 = {kth:.6f}, rectangle Im<={top:.4f}: winding {w:+.4f} [{'PASS' if good else 'FAIL'}]  B(i top)={btop:.3e}  [{time.time()-t0:.0f}s]")
    log(f"P1 {'PASS' if ok1 else 'FAIL'}")
    for n in (1.05, 2.0):
        w2 = count(n, alphas[n], 1, npts=48)[0]; w3 = count(n, alphas[n], 1, width=0.5)[0]
        log(f"nuisance n={n} q=1: 48 pts/side winding {w2:+.4f}; rho-panel width 0.5 winding {w3:+.4f}")
        out[f"nuis_n{n}"] = dict(w48=w2, wfine=w3)
    wmf = count(1.05, alphas[1.05], 1, planted=2.0 + 0.5j)[0]
    log(f"must-fail (planted zero at 2+0.5i, n=1.05 q=1): winding {wmf:+.4f} [{'PASS (fires)' if abs(wmf-1)<=0.05 else 'FAIL'}]")
    out["mustfail"] = wmf
    # P2: EXP-055 closed-form promotion
    import exp055_W3 as X
    from scipy.special import gamma
    c1 = lambda a: -(math.pi / 2) * gamma(0.5 + 2 * a) * gamma(2.5 - 2 * a)
    c1bad = lambda a: -(math.pi / 2) * gamma(0.5 + a) * gamma(2.5 - a)
    res = {}
    for a in (0.006, 0.004):
        r = X.W3(a) / X.lam2(a); res[a] = r / c1(a) - 1
        log(f"P2 alpha={a}: W3/lambda^2 = {r:.8f}, closed form {c1(a):.8f}: rel {res[a]:+.2e}; wrong form {c1bad(a):.8f}: rel {r/c1bad(a)-1:+.2e}")
    p2 = all(abs(v) <= 1e-3 for v in res.values()) and abs(res[0.004]) < abs(res[0.006])
    mf2 = abs(X.W3(0.006) / X.lam2(0.006) / c1bad(0.006) - 1) > 5e-3
    log(f"P2 {'PASS' if p2 else 'FAIL'}; P2 must-fail {'PASS (fires)' if mf2 else 'FAIL'}")
    out.update(P1=bool(ok1), P2=bool(p2), P2_res={str(k): v for k, v in res.items()}, P2_mustfail=bool(mf2))
    json.dump(out, open(os.path.join(D0, "exp056_results.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
