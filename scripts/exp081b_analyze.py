"""EXP-081b analysis from checkpoints under BOTH reliability rules (registered report.md b61f7a0, a206381, 019439c):
 orig   = N1'' (relative 1e-8 on g at checkpoints) / N2 (relative 1e-8, referee),
 impact = N1''' (per checkpoint |dg| pi/cosh^2(pi s) <= 1e-7) + CUMULATIVE (sum over C-nodes <= s_max of estimated |dg| x
          quadrature weight x pi/cosh^2 <= 1e-7; |dg| from log-linear interpolation of checkpoint relative errors x |g|) / N2'.
Tails T0/T1, extrapolation, routes, nuisances and sign rule are executed from exp081b_run.py unchanged. [model: Opus 5.5]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exp081b_run as R
OUT = R.OUT; TOL = 1e-7; CUM = {}

def rel_interp(checks):
    """log-linear interpolation of checkpoint relative errors; constant below the first, extrapolated above the last."""
    cs = np.array([c[0] for c in checks]); lr = np.log(np.maximum([c[1] for c in checks], 1e-16))
    def f(s):
        if s <= cs[0]: return float(np.exp(lr[0]))
        if s >= cs[-1]: return float(np.exp(lr[-1] + (lr[-1] - lr[-2]) / (cs[-1] - cs[-2]) * (s - cs[-1])))
        return float(np.exp(np.interp(s, cs, lr)))
    return f

def S_from_ckpt(tag, rule):
    st = json.load(open(os.path.join(OUT, tag + "_ckpt.json")))
    nodes = sorted((float(k.split("|")[1]), v[0]) for k, v in st.items() if k.startswith("g|"))
    x, w = np.polynomial.legendre.leggauss(12); wt = {}
    for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
        for xi, wi in zip(x, w):
            si = 0.5 * (hi - lo) * (xi + 1) + lo; wt[f"{si:.15f}"] = 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2
    gmap = {f"{s:.15f}": g for s, g in nodes}
    checks = []
    for k, gd in sorted(((k, v) for k, v in st.items() if k.startswith("chk|")), key=lambda kv: float(kv[0].split("|")[1])):
        s = float(k.split("|")[1]); g = gmap[f"{s:.15f}"]; checks.append((s, abs(gd - g) / max(abs(g), 1e-300), abs(gd - g)))
    smax = 0.0
    for s, rel, d in checks:
        ok = (rel <= 1e-8) if rule == "orig" else (d * np.pi / np.cosh(np.pi * s) ** 2 <= TOL)
        if ok: smax = s
        else: break
    if checks and smax == checks[-1][0]: smax = 6.0
    ri = rel_interp([(s, rel) for s, rel, d in checks])
    cum = lambda sm: sum(wt[k] * ri(float(k)) * abs(g) for k, g in gmap.items() if float(k) <= sm)
    c_at = cum(smax); flag = False
    if rule == "impact" and c_at > TOL:                                    # registered 019439c: lower s_max, flag
        flag = True; cand = [s for s, _, _ in checks if s < smax and cum(s) <= TOL]; smax = max(cand) if cand else 0.0
    C0 = sum(wt[k] * g for k, g in gmap.items() if float(k) <= smax)
    fp = [(float(k), g) for k, g in gmap.items() if 1.0 <= float(k) <= smax]
    if len(fp) >= 3:
        ss = np.array([p[0] for p in fp]); gg = np.array([p[1] for p in fp])
        c = np.linalg.lstsq(np.vstack([np.ones_like(ss), ss ** 2, ss ** 3]).T, gg, rcond=None)[0]
        C1 = C0 + sum(wt[k] * (c[0] + c[1] * float(k) ** 2 + c[2] * float(k) ** 3) for k in gmap if float(k) > smax)
    else: C1 = float("nan")
    base = st["t0"] + st.get("tsad", 0.0)
    CUM.setdefault(rule, {})[tag] = dict(s_max=smax, cum_at_node_smax=c_at, cum_final=cum(smax), lowered=flag)
    return {"S_T0": 0.5 * (base + C0), "S_T1": 0.5 * (base + C1), "s_max": smax}

def referee(rule):
    fn = os.path.join(HERE, "exp081b_referee_results.json")
    if not os.path.exists(fn): return "referee not available"
    ref = json.load(open(fn)); res = {float(k): v for k, v in ref["res"].items()}
    if rule == "orig":
        return f"N2 (orig): {'PASS' if ref['pass_'] else 'FAIL'} (applied at s <= production s_max {ref['s_max']:.2f}); {json.dumps(ref['res'])}"
    import sigma3d as S3                                                    # N2': impact = rel x |logdet| x pi/cosh^2
    W, P, Wbox, Ny = 4, 4, 4, 8; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); out, ok = [], True
    for s, v in sorted(res.items()):
        ld = abs(S3.logdet(S.inner(1.0, 0.5 + 1j * s, npt=24)[0]).real); I = v["logdet"] * ld * np.pi / np.cosh(np.pi * s) ** 2
        ok &= I <= TOL; out.append(f"s={s}: rel {v['logdet']:.1e} |logdet| {ld:.3g} impact {I:.1e}")
    return f"N2' (impact): {'PASS' if ok else 'FAIL -> VOID'}; " + "; ".join(out) + f"  [descriptive: {json.dumps(ref['res'])}]"

if __name__ == "__main__":
    for rule in ("orig", "impact"):
        def sig(W, P, Wbox=4, c=2, cpts=12, s_cut=3.0, dd=0):
            return S_from_ckpt(f"sigma_W{W}_P{P}_box{Wbox}_c{c}_cp{cpts}_sc{s_cut}_dd{int(dd)}", rule)
        R.sigma = sig
        print(f"\n===== rule {rule} =====", flush=True)
        exec(open(os.path.join(HERE, "exp081b_run.py")).read().split('if __name__ == "__main__":')[1].replace("\n    ", "\n").replace('"exp081b_results.json"', f'"exp081b_results_{rule}.json"'),
             dict(R.__dict__, sigma=sig))
        print(f"--- reliability per geometry (rule {rule}): s_max, cumulative impact (estimate) ---")
        for tag, v in sorted(CUM[rule].items()):
            print(f"  {tag}: s_max {v['s_max']:.2f}  cum {v['cum_final']:.1e}" + (f"  [LOWERED: cum at per-node s_max {v['cum_at_node_smax']:.1e}]" if v["lowered"] else ""))
        print(referee(rule), flush=True)
