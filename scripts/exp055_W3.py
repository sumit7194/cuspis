"""EXP-055 (pre-registered in report.md, 49460d1): D = 3 two-edge free-scalar moment W3(alpha) = Int_0^inf w_S(t, alpha) dt
at real twist alpha, from the EXP-044 Fredholm form; log-t Gauss-Legendre.   [model: Opus 5.5]"""
import sys, math, time, json, os, warnings
import numpy as np
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import exp044_det as E

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
nwarn = {"n": 0, "where": []}

def w(t, a, h=0.1):
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        v = E.w_scalar(t, a, h=h)[0].real
    if ws:
        nwarn["n"] += len(ws)
        if len(nwarn["where"]) < 5: nwarn["where"].append((t, a, str(ws[0].message)[:40]))
    if not math.isfinite(v): raise RuntimeError(f"non-finite w at t={t}, a={a}")
    return v

def W3(a, N=120, tmin=1e-14, tmax=20.0, h=0.1):
    x, wt = np.polynomial.legendre.leggauss(N)
    u0, u1 = math.log(tmin), math.log(tmax)
    u = 0.5 * (u1 - u0) * x + 0.5 * (u1 + u0); wu = 0.5 * (u1 - u0) * wt
    return float(sum(wi * math.exp(ui) * w(math.exp(ui), a, h) for ui, wi in zip(u, wu)))

def lam2(a): return math.sin(math.pi * a) ** 2 / math.pi ** 2
def slope(a1, v1, a2, v2): return math.log(abs(v2 / v1)) / math.log(a2 / a1)

def run():
    out = {}; al = [0.0125, 0.025, 0.05, 0.1]
    Wv = []
    for a in al:
        t0 = time.time(); Wv.append(W3(a)); log(f"W3({a}) = {Wv[-1]:.8e}  W3/lambda^2 = {Wv[-1]/lam2(a):.6f}  [{time.time()-t0:.0f} s]")
    sl = [slope(al[i], Wv[i], al[i + 1], Wv[i + 1]) for i in range(3)]
    p1 = all(1.85 <= s <= 2.15 for s in sl[:2])
    r = [W / lam2(a) for W, a in zip(Wv, al)]; p2 = abs(r[0] / r[1] - 1) < 0.03
    log(f"P1 slopes {['%.4f'%s for s in sl]} [{'PASS' if p1 else 'FAIL'}];  P2 ratio W3/lambda^2: {r[0]:.6f} vs {r[1]:.6f} (rel {r[0]/r[1]-1:+.4f}) [{'PASS' if p2 else 'FAIL'}]")
    w1, w2 = w(1e-12, 0.1), w(1e-12, 0.2); smf = slope(0.1, w1, 0.2, w2)
    log(f"must-fail t=1e-12: w(0.1) {w1:.5e}, w(0.2) {w2:.5e}, slope {smf:.3f} [{'PASS (fires, <= 1.3)' if smf <= 1.3 else 'FAIL'}]")
    sweeps = {}
    for lab, kw in (("N240", dict(N=240)), ("tmin1e-18", dict(tmin=1e-18)), ("h0.05", dict(h=0.05))):
        for a in (0.0125, 0.05):
            v = W3(a, **kw); base = Wv[al.index(a)]; sweeps[f"{lab}_{a}"] = v
            log(f"  sweep {lab} a={a}: W3 {v:.8e}  rel drift {v/base-1:+.2e}")
    log(f"slogdet warnings: {nwarn['n']}; first: {nwarn['where']}")
    out.update(alpha=al, W3=Wv, slopes=sl, ratio=r, P1=p1, P2=p2, mustfail_slope=smf, sweeps=sweeps, warnings=nwarn)
    json.dump(out, open(os.path.join(D0, "exp055_results.json"), "w"), indent=1)

if __name__ == "__main__":
    run()
