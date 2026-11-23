"""EXP-085 amendment 4 (registered): extrapolate c(n) = c_inf + A/n + B/n^2 on n in {64, 96, 128, 192, 256}; the SAME on the Watson sum
G0(n) = <G(k)>_{k != 0} (known answer W_sc/6, computed with mpmath at run time); held-out n = 384 for both. Writes A4.json
(c := c_inf, sigma_c := sigma_inf, converged := all checks pass) for exp085_run.py phases B-E. [model: Opus 5.5]"""
import os, sys, json, time, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "exp081d_results", "exp085"); os.makedirs(OUT, exist_ok=True)
WIN = [64, 96, 128, 192, 256]; HOLD = 384; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:58s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def Gk(n):
    k = 2 * np.pi * np.arange(n) / n; E = sum(np.meshgrid(*(2 - 2 * np.cos(k),) * 3, indexing="ij"))
    G = np.zeros_like(E); m = E > 1e-14; G[m] = 1.0 / E[m]; return G
def avgconv(A, B): return np.real(np.fft.fftn(np.fft.ifftn(A) * np.fft.ifftn(B)))
def c_of_n(n):                                          # amendment-3 path: q = 0 included
    G = Gk(n); Bq = 2 * avgconv(G, G); S2 = avgconv(G * G, G); return float(-4 * np.mean((1.0 / Bq) * (S2 - G * np.mean(G * G))))
def g0_of_n(n): return float(np.mean(Gk(n)))           # <G(k)>, k != 0 term is 0 (excluded), same Gk
def fit3(ns, ys):
    X = np.column_stack([np.ones(len(ns)), 1.0 / np.array(ns), 1.0 / np.array(ns) ** 2]); p, *_ = np.linalg.lstsq(X, ys, rcond=None)
    r = ys - X @ p; dof = len(ns) - 3; s2 = float(r @ r / dof) if dof > 0 else 0.0; cov = s2 * np.linalg.inv(X.T @ X); return p, cov
def fit2(ns, ys):
    X = np.column_stack([np.ones(len(ns)), 1.0 / np.array(ns)]); p, *_ = np.linalg.lstsq(X, ys, rcond=None); return p
def extrap(vals):
    ns = np.array(WIN, float); ys = np.array([vals[n] for n in WIN]); p, cov = fit3(ns, ys)
    loo = [fit3(np.delete(ns, i), np.delete(ys, i))[0] for i in range(len(ns))]
    p2 = fit2(ns[-3:], ys[-3:])
    pred = lambda q, x: q[0] + q[1] / x + (q[2] / x ** 2 if len(q) > 2 else 0.0)
    s_inf = max(max(q[0] for q in loo) - min(q[0] for q in loo), abs(p[0] - p2[0]), float(np.sqrt(cov[0, 0])))
    v = np.array([1, 1 / HOLD, 1 / HOLD ** 2]); s_cov = float(np.sqrt(v @ cov @ v))
    preds = [pred(q, HOLD) for q in loo]
    s_pred = max(max(preds) - min(preds), abs(pred(p, HOLD) - pred(p2, HOLD)), s_cov)
    return dict(inf=float(p[0]), sigma_inf=s_inf, pred384=float(pred(p, HOLD)), sigma_pred=s_pred, A=float(p[1]), B=float(p[2]), inf_2param=float(p2[0]))
mp.mp.dps = 30
W_sc = mp.sqrt(6) / (32 * mp.pi ** 3) * mp.gamma(mp.mpf(1) / 24) * mp.gamma(mp.mpf(5) / 24) * mp.gamma(mp.mpf(7) / 24) * mp.gamma(mp.mpf(11) / 24)
G0_true = float(W_sc / 6); print(f"Watson exact (mpmath): W_sc = {mp.nstr(W_sc, 20)},  G0 = W_sc/6 = {G0_true!r}", flush=True)
cvals, gvals = {}, {}
for n in WIN + [HOLD]:
    t = time.time(); cvals[n] = c_of_n(n); gvals[n] = g0_of_n(n)
    print(f"   n={n}: c {cvals[n]:+.12f}   G0 {gvals[n]:.12f}   ({time.time()-t:.1f}s)", flush=True)
ew, ec = extrap(gvals), extrap(cvals)
check("Watson KA: |G0_inf - W/6| <= sigma_W", abs(ew["inf"] - G0_true) <= ew["sigma_inf"], f"G0_inf {ew['inf']:.10f} true {G0_true:.10f} diff {abs(ew['inf']-G0_true):.2e} sigma {ew['sigma_inf']:.2e}")
check("Watson KA: sigma_W < 1% of W/6", ew["sigma_inf"] < 0.01 * G0_true, f"sigma/true {ew['sigma_inf']/G0_true:.2e}")
check("Watson held-out n=384", abs(ew["pred384"] - gvals[HOLD]) <= ew["sigma_pred"], f"pred {ew['pred384']:.10f} computed {gvals[HOLD]:.10f} diff {abs(ew['pred384']-gvals[HOLD]):.2e} sigma_pred {ew['sigma_pred']:.2e}")
check("c held-out n=384", abs(ec["pred384"] - cvals[HOLD]) <= ec["sigma_pred"], f"pred {ec['pred384']:+.10f} computed {cvals[HOLD]:+.10f} diff {abs(ec['pred384']-cvals[HOLD]):.2e} sigma_pred {ec['sigma_pred']:.2e}")
ok = not FAIL
print(f"\nAMENDMENT 4: {'ALL PASS -> c := c_inf = %+.8f +- %.2e' % (ec['inf'], ec['sigma_inf']) if ok else 'FAIL -> 085 stays INCONCLUSIVE; c_inf not pursued'}")
json.dump(dict(c=ec["inf"], sigma_c=ec["sigma_inf"], converged=ok, amendment=4, c_extrap=ec, watson=ew, cvals=cvals, gvals=gvals, G0_true=G0_true, failed=FAIL),
          open(os.path.join(OUT, "A4.json"), "w"), indent=1)
sys.exit(0 if ok else 1)
