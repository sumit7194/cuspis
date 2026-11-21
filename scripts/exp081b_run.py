"""EXP-081b driver (registered in report.md 0ab92d4 + N1'' 7c61bb9): strip-pair lean P1.
Each sigma geometry runs in a FRESH worker process under its own watchdog (cap 2.2 GB; raised to 3.2 GB after the P12 kill, see report); results in exp081b_results/;
resume = skip finished. Free side in-process (cheap). Analysis per registration for tails T0 and T1. [model: Opus 5.5]"""
import os, sys, json, subprocess, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
OUT = os.path.join(HERE, "exp081b_results"); os.makedirs(OUT, exist_ok=True)
PY = os.path.join(HERE, "..", ".venv", "bin", "python"); KF = 0.0396481
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)

def sigma(W, P, Wbox=4, c=2, cpts=12, s_cut=3.0, dd=0):
    tag = f"sigma_W{W}_P{P}_box{Wbox}_c{c}_cp{cpts}_sc{s_cut}_dd{int(dd)}"; f = os.path.join(OUT, tag + ".json")
    if not os.path.exists(f):
        cmd = [PY, os.path.join(HERE, "tools", "watchdog.py"), "--log", os.path.join(OUT, tag + ".wd.log"), "--cap-gb", "3.2",
               "--min-disk-gb", "5", "--stop-on-pressure-warn", "--stdout", os.path.join(OUT, tag + ".out"), "--",
               PY, "-u", "-W", "ignore", os.path.join(HERE, "exp081b_worker.py"), str(W), str(P), str(Wbox), str(c), str(cpts), str(s_cut), str(int(dd))]
        env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
        t0 = time.time(); r = subprocess.run(["nice", "-n", "12"] + cmd, env=env)
        if not os.path.exists(f): raise RuntimeError(f"worker failed: {tag} (exit {r.returncode}); see {tag}.wd.log")
        d = json.load(open(f)); log(f"{tag}: S_T0 {d['S_T0']:.10f} S_T1 {d['S_T1']:.10f} s_max {d['s_max']:.2f} checks {[(round(a, 2), f'{b:.0e}') for a, b in d['checks']]}  [{time.time()-t0:.0f}s]")
    return json.load(open(f))

def free(W, P, Wbox=4, c=2):
    f = os.path.join(OUT, f"free_W{W}_P{P}_box{Wbox}_c{c}.json")
    if not os.path.exists(f):
        Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
        json.dump(dict(S=float(S3.FreeStrip(Lx, Lt, int(c * 2 * P), list(range(x0, x0 + W)), P - 1).S(cpts=12).real)), open(f, "w"))
    return json.load(open(f))["S"]

def pair(fn, P, W1=2, W2=4, Wbox=4, key=None, **kw):
    Ny = int(kw.get("c", 2) * 2 * P)
    a, b = fn(W1, P, Wbox=Wbox, **kw), fn(W2, P, Wbox=Wbox, **kw)
    if key: a, b = a[key], b[key]
    return -(a - b) / Ny / (1 / W1 - 1 / W2)

def fit(xs, ys, form):
    x = np.asarray(xs, float); X = np.vstack([np.ones_like(x), 1 / x, 1 / x ** 2 if form == "A" else np.log(x) / x]).T
    c = np.linalg.lstsq(X, np.asarray(ys, float), rcond=None)[0]
    return c[0], (lambda P: c[0] + c[1] / P + (c[2] / P ** 2 if form == "A" else c[2] * np.log(P) / P))

def extrap(d, label):
    Ps = sorted(d); tr = [P for P in Ps if P <= 10]; out = {}
    for form in ("A", "B"):
        xi_tr, pr = fit(tr, [d[P] for P in tr], form); xi_all, _ = fit(Ps, [d[P] for P in Ps], form)
        out[form] = dict(train=xi_tr, all=xi_all, ho=abs(pr(12) - d[12]))
    s_ho = 6 * max(out["A"]["ho"], out["B"]["ho"]); s_sp = abs(out["A"]["all"] - out["B"]["all"]) / 2
    c = 0.5 * (out["A"]["all"] + out["B"]["all"]); s = float(np.hypot(s_ho, s_sp))
    log(f"{label}: A train {out['A']['train']:.6f} all {out['A']['all']:.6f} ho {out['A']['ho']:.1e} | B train {out['B']['train']:.6f} all {out['B']['all']:.6f} ho {out['B']['ho']:.1e} -> {c:.6f} +- {s:.6f}")
    return c, s, out

if __name__ == "__main__":
    Ps = (4, 6, 8, 10, 12); res = {}
    kap = {P: pair(lambda W, P, **kw: free(W, P, **kw), P) for P in Ps}
    log("free kappa_lat:", {P: round(v, 6) for P, v in kap.items()})
    kc, ks, ko = extrap(kap, "free (planted control K)")
    K_pass = all(abs(ko[f]["train"] - KF) <= 2 * ks for f in ("A", "B")) and all(ko[f]["ho"] <= ks for f in ("A", "B"))
    log(f"K: {kc:.6f} +- {ks:.6f} vs {KF} [{'PASS' if K_pass else 'FAIL'}]"); res["K"] = dict(central=kc, sigma=ks, pass_=bool(K_pass))
    for P in Ps:
        for W in (2, 4): sigma(W, P)
    # nuisances
    for W in (2, 4): sigma(W, 6, c=3); sigma(W, 6, cpts=16); sigma(W, 6, s_cut=2.5); sigma(W, 4, dd=1); sigma(W * 2, 8, Wbox=8)
    out = {}
    for tail in ("S_T0", "S_T1"):
        dk = {P: pair(sigma, P, key=tail) for P in Ps}; R = {P: dk[P] / kap[P] for P in Ps}
        log(f"[{tail}] delta_kappa_lat {{P: value}} = {{{', '.join(f'{P}: {v:.6f}' for P, v in dk.items())}}}; R = {{{', '.join(f'{P}: {v:.4f}' for P, v in R.items())}}}")
        Ri, si, _ = extrap(R, f"[{tail}] route (i) R")
        dki, sdk, _ = extrap(dk, f"[{tail}] route (ii) delta_kappa_lat"); Rii, sii = dki / KF, sdk / KF
        ny = abs(pair(sigma, 6, key=tail, c=3) / dk[6] - 1); sq = abs(pair(sigma, 6, key=tail, cpts=16) / dk[6] - 1)
        sc = abs(pair(sigma, 6, key=tail, s_cut=2.5) / dk[6] - 1)
        kap48 = pair(lambda W, P, **kw: free(W, P, **kw), 8, W1=4, W2=8, Wbox=8)
        R48 = pair(sigma, 8, W1=4, W2=8, Wbox=8, key=tail) / kap48; sigW = abs(R48 - R[8])
        extra = 0.0
        if ny > 0.01: extra = np.hypot(extra, ny * abs(Ri))
        if sq > 1e-3: extra = np.hypot(extra, sq * abs(Ri))
        premise = abs(Ri - Rii) <= np.hypot(si, sii)
        if premise: Rq, sg = Ri, float(np.sqrt(si ** 2 + sigW ** 2 + extra ** 2))
        else:
            lo, hi = min(Ri - si, Rii - sii), max(Ri + si, Rii + sii); Rq, sg = 0.5 * (lo + hi), float(np.sqrt(((hi - lo) / 2) ** 2 + sigW ** 2 + extra ** 2))
        dd_shift = abs(pair(sigma, 4, key=tail, dd=1) / kap[4] - R[4])
        log(f"[{tail}] Ny {ny:.1e} [{'PASS' if ny <= 0.01 else 'FAIL->sys'}]; s-quad {sq:.1e} [{'PASS' if sq <= 1e-3 else 'FAIL->sys'}]; "
            f"s_cut 2.5 vs 3: {sc:.1e} [{'PASS' if sc <= 1e-6 else 'FAIL'}]; sigma_W (4,8) pair: R48 {R48:.4f} vs R(8) {R[8]:.4f} -> {sigW:.4f}")
        log(f"[{tail}] routes: (i) {Ri:.4f} +- {si:.4f}, (ii) {Rii:.4f} +- {sii:.4f}, premise {'OK' if premise else 'FAILS (union)'}; "
            f"R_inf = {Rq:.4f} +- {sg:.4f}; R_inf + 0.4503 = {Rq + 0.4503:.4f} (2 sigma {2*sg:.4f}); must-fire shift {dd_shift:.4f} [{'FIRES' if dd_shift > sg else 'does not fire'}]")
        out[tail] = dict(dk=dk, R=R, route_i=[Ri, si], route_ii=[Rii, sii], premise=bool(premise), R_inf=[Rq, sg], stat=Rq + 0.4503,
                         decided=bool(abs(Rq + 0.4503) > 2 * sg), sign=(int(np.sign(Rq + 0.4503)) if np.isfinite(Rq) else 0), ny=ny, squad=sq, scut=sc, sigW=sigW, mustfire=dd_shift)
    both = K_pass and out["S_T0"]["decided"] and out["S_T1"]["decided"] and out["S_T0"]["sign"] == out["S_T1"]["sign"]
    verdict = ("INCONCLUSIVE (planted control K failed)" if not K_pass else
               (f"DECIDED (both tails agree): delta(kappa/C_T) {'> 0' if out['S_T0']['sign'] > 0 else '< 0'} (pending the N2 referee)" if both else "INCONCLUSIVE"))
    log("VERDICT:", verdict); res.update(out); res["verdict"] = verdict
    json.dump(res, open(os.path.join(HERE, "exp081b_results.json"), "w"), indent=1, default=str)
