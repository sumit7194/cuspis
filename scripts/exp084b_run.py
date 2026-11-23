"""EXP-084b (registered 48022d9 + amendment 1): does the exact-n 1/a^2 coefficient c(n) vanish as n -> 1?
Phases: 0 plants (same fit/extrapolation code) + KA (084's n = 2, 3 R_n reproduced); 1 Q_n for new n (paths A/B, like 084);
2 sigma table on disk; 3 per-n 3-parameter k-fit (full covariance), extrapolation to n = 1, reading.
Usage: exp084b_run.py N [N ...]   (new n values to compute, e.g. 4 or 4 5; n = 2, 3 are reused from EXP-084) [model: Opus 5.5]"""
import sys, os, json, time, numpy as np
import exp083_honest as H
HERE = os.path.dirname(os.path.abspath(__file__)); OUT84 = os.path.join(HERE, "exp081d_results", "exp084")
OUT = os.path.join(HERE, "exp081d_results", "exp084b"); os.makedirs(OUT, exist_ok=True)
KS = [1, 1.5, 2, 2.5]; JD = json.load(open(os.path.join(HERE, "exp081d_results.json")))
KAP = {k: JD[str(k)]["kappa"] for k in KS}; RCONT = {k: JD[str(k)]["R_T0"] for k in KS}
NEW = [int(x) for x in sys.argv[1:]]; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:58s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
norm = lambda k: 1.0 / (4 * int(4 * k)) / (1 / int(2 * k) - 1 / int(4 * k)) / KAP[k]
KSa = np.array(KS, float); X = np.column_stack([KSa ** 2, KSa, np.ones(4)])
def kfit(R, sR):
    """weighted 3-parameter fit R = c k^2 + d k + e; cov = s^2 (X^T W X)^-1, s^2 = max(1, chi2/dof); returns c, d, sc, sd, corr."""
    y = np.array([R[k] for k in KS]); s = np.maximum(np.array([sR[k] for k in KS]), 1e-15); W = np.diag(1 / s ** 2)
    A = X.T @ W @ X; p = np.linalg.solve(A, X.T @ W @ y); chi2 = float(((y - X @ p) / s) @ ((y - X @ p) / s))
    cov = max(1.0, chi2 / 1.0) * np.linalg.inv(A); sc, sd = np.sqrt(cov[0, 0]), np.sqrt(cov[1, 1])
    return float(p[0]), float(p[1]), float(sc), float(sd), float(cov[0, 1] / (sc * sd))
def extrap(ns, cs, scs):
    """amendment 1: highest order mh = min(#n-1, 2); c1 = poly value at n = 1; sigma = max(LOO spread at order mh-1, propagation at mh, 1e-12);
    drift = |c1(mh) - c1(mh-1)|. Returns dict with the label."""
    x = np.array(ns, float) - 1; y = np.array(cs); mh = min(len(x) - 1, 2)
    def c1(xx, yy, m): return float(np.polyval(np.polyfit(xx, yy, m), 0.0))
    v_hi = c1(x, y, mh); v_lo = c1(x, y, mh - 1)
    loo = [c1(np.delete(x, i), np.delete(y, i), mh - 1) for i in range(len(x))] if len(x) - 1 > mh - 1 else [v_lo]
    # propagation: c1 at order mh is linear in y; weights by unit perturbation
    w = np.array([c1(x, np.eye(len(x))[i], mh) - c1(x, np.zeros(len(x)), mh) for i in range(len(x))])
    sprop = float(np.sqrt(np.sum((w * np.array(scs)) ** 2))); spread = float(max(loo) - min(loo))
    sig = max(spread, sprop, 1e-12); drift = abs(v_hi - v_lo)
    if drift > sig: lab = "INCONCLUSIVE (order drift)"
    elif abs(v_hi) <= 2 * sig: lab = "c(1) consistent with 0"
    else: lab = "c(1) non-zero"
    return dict(c1=v_hi, c1_lower=v_lo, sigma=sig, spread=spread, sprop=sprop, drift=drift, label=lab, order=mh)
# ---------------- phase 0: plants + KA ----------------
NS_PLAN = [2, 3] + NEW; a = 0.69
for nm, fn, sc_, want in (("P-lin", lambda n: a * (n - 1), 1e-6, "c(1) consistent with 0"), ("P-quad", lambda n: a * (n - 1) ** 2, 1e-6, "NOT non-zero"),
                         ("P-const", lambda n: a, 1e-6, "c(1) non-zero")):
    r = extrap(NS_PLAN, [fn(n) for n in NS_PLAN], [sc_] * len(NS_PLAN)); check(f"plant {nm} on n={NS_PLAN}", (r["label"] != "c(1) non-zero") if want == "NOT non-zero" else (r["label"] == want), f"{r['label']} (c1 {r['c1']:+.3e}, sigma {r['sigma']:.1e}, drift {r['drift']:.1e})")
rng = np.random.default_rng(20261123); cn = [a * (n - 1) + rng.normal(0, 1e-3) for n in NS_PLAN]
r = extrap(NS_PLAN, cn, [1e-3] * len(NS_PLAN)); check("plant P-noise: sigma propagates declared 1e-3", r["sigma"] >= 1e-3, f"sigma {r['sigma']:.2e}; label reported: {r['label']}")
sR = {k: 1e-6 for k in KS}; Rp = {k: 0.69 * k * k + 0.1 for k in KS}; c, d, sc_, sd_, rho = kfit(Rp, sR)
check("plant P-cd: c k^2 + e recovers d ~ 0, c", abs(d) <= 2 * max(sd_, 1e-12) and abs(c - 0.69) <= 2 * max(sc_, 1e-12), f"c {c:.6f} d {d:+.2e} (sd {sd_:.1e}) corr(c,d) {rho:+.3f}")
res84 = json.load(open(os.path.join(OUT84, "result.json")))
def R84(n, k, key="QA"):
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); q = lambda W: json.load(open(os.path.join(OUT84, f"Q_W{W}P{P}b{P}.json")))[str(n)][key]
    return -(0.5 / (n - 1)) * (q(W1) - q(W2)) * norm(k)
dev = max(abs(R84(n, k) - res84["Rn"][str(n)][str(k) if str(k) in res84["Rn"][str(n)] else repr(float(k))]) for n in (2, 3) for k in KS)
check("KA: n = 2, 3 R_n from 084 Q files == 084 result.json", dev <= 1e-12, f"max dev {dev:.1e}")
if FAIL: print("PHASE 0 FAIL -> exit before computing"); sys.exit(1)
# ---------------- phase 1: Q_n for the new n ----------------
def logdetB_rev(geo, G):
    Ny = geo.Ny; tot = 0.0
    for k in range(Ny):
        B = sum(G[p] * G[(k - p) % Ny] for p in reversed(range(Ny))) * (2.0 / Ny); s, ld = np.linalg.slogdet(B.T); tot += ld
    return tot
for n in NEW:
    for k in KS:
        P = int(4 * k)
        for W in (int(2 * k), int(4 * k)):
            fn = os.path.join(OUT, f"Q{n}_W{W}P{P}b{P}.json")
            if os.path.exists(fn): continue
            geo = H.Geom(W, P, Wbox=P, c=2); t = time.time()
            ld1A = geo.logdetB(geo.Gn(1)); ld1B = logdetB_rev(geo, geo.Gn(1))
            sA, _ = geo.saddle(n, tol=1e-13); sB, _ = geo.saddle(n, tol=1e-11)
            qA = geo.logdetB(geo.Gn(n, sA)) - n * ld1A; qB = logdetB_rev(geo, geo.Gn(n, sB)) - n * ld1B
            json.dump(dict(W=W, P=P, n=n, QA=qA, QB=qB, sigQ=abs(qA - qB), sec=time.time() - t), open(fn, "w"), indent=1)
            print(f"Q{n} W{W}P{P}b{P}: done ({time.time()-t:.1f}s)", flush=True); del geo
# ---------------- phase 2: sigma table, phase 3: fits, extrapolation, reading ----------------
NS = [2, 3] + [n for n in NEW if all(os.path.exists(os.path.join(OUT, f"Q{n}_W{W}P{int(4*k)}b{int(4*k)}.json")) for k in KS for W in (int(2*k), int(4*k)))]
def Qv(n, W, P):
    if n in (2, 3): d = json.load(open(os.path.join(OUT84, f"Q_W{W}P{P}b{P}.json")))[str(n)]; return d["QA"], d["sigQ"]
    d = json.load(open(os.path.join(OUT, f"Q{n}_W{W}P{P}b{P}.json"))); return d["QA"], d["sigQ"]
Rn, sRn = {}, {}
for n in NS:
    Rn[n], sRn[n] = {}, {}
    for k in KS:
        W1, W2, P = int(2 * k), int(4 * k), int(4 * k); (q1, s1), (q2, s2) = Qv(n, W1, P), Qv(n, W2, P)
        Rn[n][k] = -(0.5 / (n - 1)) * (q1 - q2) * norm(k); sRn[n][k] = (0.5 / (n - 1)) * np.hypot(s1, s2) * norm(k)
json.dump({str(n): {str(k): v for k, v in sRn[n].items()} for n in NS}, open(os.path.join(OUT, "sigma_table.json"), "w"), indent=1)
print("sigma table written:", {n: max(sRn[n].values()) for n in NS}, flush=True)
if len(NS) < 3: print(f"only n = {NS}: reading needs >= 3 n (registered) -> deferred"); sys.exit(0)
fits = {n: kfit(Rn[n], sRn[n]) for n in NS}
for n in NS: print(f"n={n}: c {fits[n][0]:+.6f} +- {fits[n][2]:.1e}   d {fits[n][1]:+.6f} +- {fits[n][3]:.1e}   corr(c,d) {fits[n][4]:+.4f}", flush=True)
cc = kfit(RCONT, {k: 1e-9 for k in KS}); print(f"continued reference: c {cc[0]:+.6f}  d {cc[1]:+.6f}  corr {cc[4]:+.4f}")
ex = extrap(NS, [fits[n][0] for n in NS], [fits[n][2] for n in NS]); exd = extrap(NS, [fits[n][1] for n in NS], [fits[n][3] for n in NS])
print(f"\nEXP-084b READING (n = {NS}): {ex['label']}   c(1) = {ex['c1']:+.5f} +- {ex['sigma']:.1e} (drift {ex['drift']:.1e}, order {ex['order']})")
print(f"descriptive: d(1) = {exd['c1']:+.5f} +- {exd['sigma']:.1e} (drift {exd['drift']:.1e})  vs continued d {cc[1]:+.5f}")
json.dump(dict(NS=NS, Rn={str(n): {str(k): v for k, v in Rn[n].items()} for n in NS}, fits={str(n): fits[n] for n in NS}, cont=cc, c_extrap=ex, d_extrap=exd),
          open(os.path.join(OUT, "result.json"), "w"), indent=1, default=float)
