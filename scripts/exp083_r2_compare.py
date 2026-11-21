"""EXP-083 R2 (+A1): referee Q'(1) from the Arb honest data (fixed own-pole bases at 120 digits; M1-M4; hold-outs; data ranges),
completeness spread, and comparison with production route_b at P = 2 (fresh runs), with must-fires (dd=1, saddle-off) and the
s_cut diagnostics. Usage: python exp083_r2_compare.py P nlo nhi   [model: Opus 5.5]"""
import sys, os, json, numpy as np, mpmath as mp
from flint import acb_mat, acb, arb, ctx
import sigma3d as S3
from exp083_honest import Geom
from exp083_arb import ArbGeom
ctx.prec = 400; mp.mp.dps = 300   # fits at 300 digits (registered 130; mpmath QR absolute-eps test failed at 130, run1/run2 kept)
P, NLO, NHI = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); OUT = "exp083_r2"

def own_poles_hp(g):
    """float own poles (full-operator scan) refined by secant in Arb on F(s) = z^W det H(is) / det H0."""
    ag = ArbGeom(g); res = {}
    for p in range(g.Ny // 2 + 1):
        base = [[acb(0)] * g.N for _ in range(g.N)]; m2 = ag.m2(p)
        for i in range(g.N): base[i][i] = acb(4) + m2
        for i, j in ag.nz: base[i][j] = acb(-1)
        d0 = acb_mat(base).det()
        def F(s):
            z = (-2 * arb.pi() * s).exp(); rows = [r[:] for r in base]
            for (l, u) in g.links: rows[u][l] = acb(-z); rows[l][u] = acb(-1 / z)
            return (acb_mat(rows).det() * z ** len(g.links) / d0).real
        out = []
        for s0 in g.own_poles(p):
            a, b = arb(s0), arb(s0 + 1e-9); fa, fb = F(a), F(b)
            for _ in range(80):
                if float(abs((fb - fa).mid())) == 0: break
                c = b - fb * (b - a) / (fb - fa); a, fa, b, fb = b, fb, c, F(c)
                if float(abs((b - a).mid())) < 1e-110: break
            out.append(mp.mpf(b.mid().str(120, radius=False)))
        res[p] = out
    return res

def fit(ns, Qs, hold, singles, n2=(), prods=()):
    rows, y = [], []
    for n, q in zip(ns, Qs):
        if n in hold: continue
        r = [mp.mpf(n), mp.mpf(1)]
        for b in singles: r += [b ** n, n * b ** n]
        for b in n2: r += [n ** 2 * b ** n]
        for b in prods: r += [b ** n, n * b ** n]
        rows.append(r); y.append(q)
    A = mp.matrix(rows)
    sc = [mp.sqrt(mp.fsum(A[i, j] ** 2 for i in range(A.rows))) for j in range(A.cols)]   # column scaling: mpmath's Householder
    for j in range(A.cols):                                                                # tests an ABSOLUTE squared column norm
        for i in range(A.rows): A[i, j] /= sc[j]                                           # vs eps; scaling is exact algebra
    c, _ = mp.qr_solve(A, mp.matrix(y)); c = [c[j] / sc[j] for j in range(A.cols)]
    def ev(n):
        r = [mp.mpf(n), mp.mpf(1)] + sum(([b ** n, n * b ** n] for b in singles), []) + [n ** 2 * b ** n for b in n2] + sum(([b ** n, n * b ** n] for b in prods), [])
        return sum(ci * ri for ci, ri in zip(c, r))
    dv = [mp.mpf(1), mp.mpf(0)] + sum(([b * mp.log(b), b * (1 + mp.log(b))] for b in singles), []) + [b * (2 + mp.log(b)) for b in n2] + sum(([b * mp.log(b), b * (1 + mp.log(b))] for b in prods), [])
    qp = sum(ci * di for ci, di in zip(c, dv)); res = max([abs(ev(n) - q) / abs(q) for n, q in zip(ns, Qs) if n in hold] + [mp.mpf(0)])
    return qp, res

def referee(W, arm, poles, Ny):
    d = json.load(open(f"{OUT}/W{W}P{P}{arm}.json")); Qd = {1: mp.mpf(0), **{int(k): mp.mpf(v) for k, v in d["Q"].items()}}
    mult = {}
    for p in range(Ny):
        for s in poles[p if p <= Ny // 2 else Ny - p]: k = mp.nstr(s, 30); mult[k] = mult.get(k, 0) + 1
    out = {}
    for floor in (mp.mpf("1e-4"), mp.mpf("1e-6")):
        singles = sorted({mp.nstr(mp.exp(-2 * mp.pi * s), 60): mp.exp(-2 * mp.pi * s) for k in poles for s in poles[k]}.values(), reverse=True)
        singles = [b for b in singles if b > floor]
        n2 = [mp.exp(-2 * mp.pi * mp.mpf(k)) for k, m in mult.items() if m > 2 and mp.exp(-2 * mp.pi * mp.mpf(k)) > floor]
        top = singles[:6]; prods = sorted({mp.nstr(a * b, 60): a * b for i, a in enumerate(top) for b in top[i:] if a * b > floor}.values(), reverse=True)
        models = {"M1": dict(singles=singles), "M2": dict(singles=singles, n2=n2), "M3": dict(singles=singles, prods=prods), "M4": dict(singles=singles, n2=n2, prods=prods)}
        for nmax in (NLO, NHI):
            ns = list(range(1, nmax + 1)); Qs = [Qd[n] for n in ns]
            for name, kw in models.items():
                for hn, hold in (("last", {nmax}), ("interior", {6, 7})):
                    cols = 2 + 2 * len(kw["singles"]) + len(kw.get("n2", ())) + 2 * len(kw.get("prods", ()))
                    if cols > nmax - len(hold): out[f"{name} f{mp.nstr(floor,1)} n<={nmax} {hn}"] = None; continue
                    try: out[f"{name} f{mp.nstr(floor,1)} n<={nmax} {hn}"] = fit(ns, Qs, hold, **kw)
                    except ValueError as e:                               # exactly singular design (coinciding bases): excluded, logged
                        out[f"{name} f{mp.nstr(floor,1)} n<={nmax} {hn}"] = None; print(f"     {name} n<={nmax} {hn}: SINGULAR design ({cols} cols) -> excluded", flush=True)
    adequate = {k: v for k, v in out.items() if v is not None and v[1] <= mp.mpf("1e-40")}
    vals = [v[0] for v in adequate.values()]
    spread = (max(vals) - min(vals)) if vals else mp.inf
    return out, adequate, (mp.fsum(vals) / len(vals) if vals else mp.nan), spread

def production(W, s_cut=3.0, dd=False, tag=""):
    g = Geom(W, P); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=s_cut, drop_double=dd)
    ck = f"{OUT}/prod_W{W}P{P}_sc{s_cut}_dd{int(dd)}{tag}_ckpt.json"; r = S3.route_b(S, ck)
    st = json.load(open(ck)); x, w = np.polynomial.legendre.leggauss(12); C = 0.0
    for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
        for xi, wi in zip(x, w):
            si = 0.5 * (hi - lo) * (xi + 1) + lo; C += 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2 * st[f"g|{si:.15f}"][0]
    return dict(t0=st["t0"], tsad=st["tsad"], C=C, checks=r["checks"], s_max=r["s_max"])

if __name__ == "__main__":
    res = {}
    for W in (2, 4):
        g = Geom(W, P); poles = own_poles_hp(g)
        for arm in ("a", "b"):
            out, adeq, mean, spread = referee(W, arm, poles, g.Ny)
            print(f"W{W}P{P} arm ({arm}): {len(adeq)} adequate of {sum(v is not None for v in out.values())} fitted; referee Q'(1) = {mp.nstr(mean, 15)}, spread {mp.nstr(spread, 3)}", flush=True)
            for k, v in out.items():
                if v is not None: print(f"     {k:28s}: {mp.nstr(v[0], 15)}  held-out {mp.nstr(v[1], 2)}", flush=True)
            res[f"W{W}{arm}"] = dict(mean=mean, spread=spread)
        prod = {k: production(W, **kw) for k, kw in (("base", {}), ("dd1", dict(dd=True)), ("scinf", dict(s_cut=np.inf)), ("sc1.5", dict(s_cut=1.5)))}
        res[f"W{W}prod"] = prod
        for k, v in prod.items(): print(f"   production {k:6s}: t0 {v['t0']:+.12f} tsad {v['tsad']:+.12f} C {v['C']:+.12f} | t0+C {v['t0']+v['C']:+.12f} | t0+tsad+C {v['t0']+v['tsad']+v['C']:+.12f}  checks {[(round(a,2), f'{b:.0e}') for a, b in v['checks']]}", flush=True)
    print("\n=== VERDICT (registered R2+A1+A2: adequate = held-out <= 1e-40; |cont - referee| <= 3 x spread; spread <= 1e-6 required, > 1e-3 STOP) ===", flush=True)
    verdict = {}
    for W in (2, 4):
        pb = res[f"W{W}prod"]
        for arm, key in (("a", lambda v: v["t0"] + v["C"]), ("b", lambda v: v["t0"] + v["tsad"] + v["C"])):
            ref, sp = res[f"W{W}{arm}"]["mean"], res[f"W{W}{arm}"]["spread"]; tol = 3 * sp
            for var in ("base", "scinf", "dd1", "sc1.5"):
                d = abs(mp.mpf(key(pb[var])) - ref)
                print(f"  W{W}P{P} arm ({arm}) vs {var:5s}: cont {key(pb[var]):+.12f} ref {mp.nstr(ref, 15)} |diff| {mp.nstr(d, 3)} tol {mp.nstr(tol, 3)} -> {'AGREE' if d <= tol else 'DISAGREE'}", flush=True)
                verdict[f"W{W}{arm}{var}"] = (float(d), float(tol))
            if arm == "b":
                d = abs(mp.mpf(pb["base"]["t0"] + pb["base"]["C"]) - ref)
                print(f"  W{W}P{P} saddle-off (t0+C) vs referee (b): |diff| {mp.nstr(d, 3)} -> {'FIRES' if d > tol else 'DOES NOT FIRE'}", flush=True)
                verdict[f"W{W}saddleoff"] = (float(d), float(tol))
    json.dump({k: [str(x) for x in v] if isinstance(v, tuple) else str(v) for k, v in verdict.items()}, open(f"{OUT}/verdict_P{P}.json", "w"), indent=1)
