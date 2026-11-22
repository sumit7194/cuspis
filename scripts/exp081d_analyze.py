"""EXP-081d analysis (registration in report.md). Committed, with its planted-value tests, BEFORE any new-k number exists. [model: Opus 5.5]

R(k) for k in {1, 1.5, 2, 2.5, 3}: pair (W1, W2) = (2k, 4k), P = 4k, box = 4k, c = 2 (Ny = 4P):
  R_T(k) = -(S_T(W1) - S_T(W2)) / Ny / (1/W1 - 1/W2) / kappa(k),  kappa(k) = the same pair formula on the free S (exp081b_run.free),
  S_T from the checkpoint with the 081b impact rule (exp081b_analyze: TOL 1e-7, rel_interp, cumulative lowering) and the R1 cap
  FIXED: s_max <= the largest C-node strictly below the first C-node (s >= 2.986) with a non-converged G (081c bug: the cap only
  fired at a checkpoint >= that node). T0 = C truncated at s_max; T1 = T0 + the 081b cubic tail fit beyond s_max.
  sigma_R(k) = |R_T0 - R_T1| + |dR/dS| (cum_W1 + cum_W2)   (numerical; the half-integer O(a) geometry is a stated limit, not in sigma).
PRIMARY (decide_r, pure function): r = [R(3) - R(1.5)] / [R(2) - R(1)], per tail.
  reading(band) only if the whole interval r +- 2 sigma_r lies in the band:
     converging r <= 0.75 (p >= 0.71)  |  log-like or slow power 0.87 <= r <= 1.15 (|p| <= 0.35)  |  power-divergent r >= 1.33 (p >= 0.70)
  (amendment 1: |p| in (0.35, 0.71) in either direction is INCONCLUSIVE by design; O(a) convergence (p = 1, r = 0.667) reads converging,
   linear growth (p = 1, r = 1.5) reads power-divergent)
  otherwise INCONCLUSIVE (naming the neighbouring readings). Also INCONCLUSIVE if |R(2) - R(1)| <= 2 sigma, if the two increments have
  opposite signs (non-monotone), if a needed k is missing/void, or if the T0 and T1 readings differ.
SECONDARY (descriptive only): r_int = [R(3) - R(2)] / [R(2) - R(1)] (log 0.585; k^-p: (2^-p - 3^-p)/(1 - 2^-p); k^p: (3^p - 2^p)/(2^p - 1));
  fits over all k: (a) Rinf + A k^-p, (b) c + B ln k, (c) c + B ln k + D/k, with residuals and leave-k=3-out predictions; per-component
  series R_t0, R_Tsad, R_C and kappa(k)."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
LO, LOGL, LOGH, HI = 0.75, 0.87, 1.15, 1.33   # amendment 1 (Bridge-named clause, before launch): was 0.60/0.80/1.25/1.60
TIER = 2.986170475685039

def band(r):
    if r <= LO: return "converging"
    if LOGL <= r <= LOGH: return "log-like or slow power (|p| <= 0.35)"
    if r >= HI: return "power-divergent"
    return None

def decide_r(R, sig, ks=(1, 1.5, 2, 3)):
    """R, sig: dict k -> value for ONE tail. Returns (reading, r, sigma_r)."""
    if any(k not in R or R[k] is None or not np.isfinite(R[k]) for k in ks): return "INCONCLUSIVE (a needed k is missing or void)", float("nan"), float("nan")
    d1, d2 = R[2] - R[1], R[3] - R[1.5]; s1 = np.hypot(sig[2], sig[1]); s2 = np.hypot(sig[3], sig[1.5])
    if abs(d1) <= 2 * s1: return "INCONCLUSIVE (R(2) - R(1) within 2 sigma of 0)", float("nan"), float("nan")
    r = d2 / d1; sr = abs(r) * np.hypot(s2 / max(abs(d2), 1e-300), s1 / abs(d1)) if d2 != 0 else s2 / abs(d1)
    if np.sign(d2) != np.sign(d1) and abs(d2) > 2 * s2: return "INCONCLUSIVE (non-monotone: increments of opposite sign)", r, sr
    lo, hi = band(r - 2 * sr), band(r + 2 * sr)
    if lo is not None and lo == hi == band(r): return lo, r, sr
    names = sorted({b for b in (band(r - 2 * sr), band(r), band(r + 2 * sr)) if b} | ({"between bands"} if band(r) is None else set()))
    return "INCONCLUSIVE (" + " / ".join(names) + ")", r, sr

def decide(tails):
    """tails: {"T0": (R, sig), "T1": (R, sig)} -> combined primary verdict."""
    res = {t: decide_r(*v) for t, v in tails.items()}
    reads = {v[0] for v in res.values()}
    if len(reads) == 1 and not next(iter(reads)).startswith("INCONCLUSIVE"): return next(iter(reads)), res
    if len(reads) > 1 and all(not x.startswith("INCONCLUSIVE") for x in reads): return "INCONCLUSIVE (T0 and T1 readings differ)", res
    return [x for x in reads if x.startswith("INCONCLUSIVE")][0] if any(x.startswith("INCONCLUSIVE") for x in reads) else "INCONCLUSIVE", res

def nodes48():
    x, w = np.polynomial.legendre.leggauss(12); out = []
    for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
        for xi, wi in zip(x, w):
            si = 0.5 * (hi - lo) * (xi + 1) + lo; out.append((si, 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2))
    return sorted(out)

def step0_cap(step0):
    """Registered Step-0 consequence (row S0): first failing checkpoint s_f. s_f <= 1.974 -> geometry void; else s_max capped at
    the last passing checkpoint below s_f. Returns (cap or None, void-node or None). step0 = dict from exp081d_step0.py, or None."""
    if not step0: return None, None
    allnodes = [n for n, _ in nodes48()]   # Step-0 keys are rounded to 3 decimals: map each to its true C-node
    nodes = sorted((min(allnodes, key=lambda n: abs(n - float(k))), v) for k, v in step0.items() if isinstance(v, dict) and "pass_" in v)
    fails = [s for s, v in nodes if not v["pass_"]]
    if not fails: return None, None
    if fails[0] <= 1.9742: return None, fails[0]
    passing = [s for s, v in nodes if v["pass_"] and s < fails[0]]
    return (max(passing) if passing else 0.0), None

def S_T(st, step0=None):
    """S_T0, S_T1, s_max, cum from an 081c/081d checkpoint dict (g floats; n1c arms; per-node stats) with the impact rule and the FIXED R1 cap."""
    import exp081b_analyze as A
    NODES = nodes48(); wt = {f"{s:.15f}": w for s, w in NODES}
    g = {f"{s:.15f}": st[f"g|{s:.15f}"] for s, _ in NODES}
    arms = {float(k): v for k, v in st["n1c"]["arms"].items()}
    checks = [(s, abs(arms[s] - g[f"{s:.15f}"]) / max(abs(g[f"{s:.15f}"]), 1e-300), abs(arms[s] - g[f"{s:.15f}"])) for s in sorted(arms)]
    smax = 0.0
    for s, rel, d in checks:
        if d * np.pi / np.cosh(np.pi * s) ** 2 <= A.TOL: smax = s
        else: break
    if checks and smax == checks[-1][0]: smax = 6.0
    ri = A.rel_interp([(s, rel) for s, rel, d in checks])
    cum = lambda sm: sum(wt[k] * ri(float(k)) * abs(v) for k, v in g.items() if float(k) <= sm)
    if cum(smax) > A.TOL:
        cand = [s for s, _, _ in checks if s < smax and cum(s) <= A.TOL]; smax = max(cand) if cand else 0.0
    unconv = sorted(s for s, _ in NODES if st.get(f"stats|{s:.15f}", {}).get("unconverged", 0) and s >= TIER)
    r1 = None
    if unconv:
        below = [s for s, _ in NODES if s < unconv[0]]; r1 = max(below); smax = min(smax, r1)
    s0cap, void = step0_cap(step0)
    if void: return dict(void=True, why=f"Step 0 failed at a node <= 1.974 ({void})")
    if s0cap is not None: smax = min(smax, s0cap)
    C0 = sum(wt[k] * v for k, v in g.items() if float(k) <= smax + 1e-12)
    fp = [(float(k), v) for k, v in g.items() if 1.0 <= float(k) <= smax + 1e-12]
    if len(fp) >= 3:
        ss = np.array([p[0] for p in fp]); gg = np.array([p[1] for p in fp])
        c = np.linalg.lstsq(np.vstack([np.ones_like(ss), ss ** 2, ss ** 3]).T, gg, rcond=None)[0]
        C1 = C0 + sum(wt[k] * (c[0] + c[1] * float(k) ** 2 + c[2] * float(k) ** 3) for k in g if float(k) > smax + 1e-12)
    else: C1 = float("nan")
    base = st["t0"] + st["tsad"]
    return dict(S_T0=0.5 * (base + C0), S_T1=0.5 * (base + C1), s_max=smax, r1_cap=r1, step0_cap=s0cap, cum=cum(smax), C0=C0, C1=C1, t0=st["t0"], tsad=st["tsad"])

def _tests():
    ok = True; cases = []
    logR = {k: 2.0 + 6.0 * np.log(k) for k in (1, 1.5, 2, 2.5, 3)}; sig = {k: 1e-5 for k in logR}
    LL = "log-like or slow power (|p| <= 0.35)"
    cases.append(("pure log -> log-like or slow power (r = 1)", decide_r(logR, sig)[0] == LL))
    cv = {k: 9.0 - 6.8 * k ** -1.5 for k in logR}; cases.append(("R_inf - A k^-1.5 -> converging (r = 0.544)", decide_r(cv, sig)[0] == "converging"))
    pw = {k: 2.255 * k ** 1.5 for k in logR}; cases.append(("A k^1.5 -> power-divergent (r = 1.84)", decide_r(pw, sig)[0] == "power-divergent"))
    mid = {1: 0.0, 2: 1.0, 1.5: 0.0, 3: 0.80}; cases.append(("r = 0.80 (gap; was 0.7 before amendment 1, now inside converging) -> INCONCLUSIVE between bands", decide_r(mid, {k: 1e-6 for k in mid})[0].startswith("INCONCLUSIVE")))
    nm = {1: 0.0, 2: 1.0, 1.5: 0.0, 3: -0.5}; cases.append(("opposite-sign increments -> INCONCLUSIVE non-monotone", "non-monotone" in decide_r(nm, {k: 1e-6 for k in nm})[0]))
    big = {k: 0.3 for k in logR}; cases.append(("sigma 0.3 at r = 1 -> INCONCLUSIVE (2 sigma leaves the band)", decide_r(logR, big)[0].startswith("INCONCLUSIVE")))
    flat = {k: 1.0 for k in logR}; cases.append(("R(2) = R(1) -> INCONCLUSIVE", decide_r(flat, sig)[0].startswith("INCONCLUSIVE")))
    miss = dict(logR); miss.pop(3); cases.append(("k = 3 missing -> INCONCLUSIVE", decide_r(miss, sig)[0].startswith("INCONCLUSIVE")))
    cases.append(("T0 log / T1 converging -> INCONCLUSIVE (tails differ)", decide({"T0": (logR, sig), "T1": (cv, sig)})[0].startswith("INCONCLUSIVE")))
    cases.append(("both tails log -> log-like or slow power", decide({"T0": (logR, sig), "T1": (logR, sig)})[0] == LL))
    c1 = {k: 9.0 - 6.8 / k for k in logR}; cases.append(("NEW: O(a) convergence p = 1 (r = 0.667) -> converging", decide_r(c1, sig)[0] == "converging"))
    g1 = {k: 2.0 * k for k in logR}; cases.append(("NEW: linear growth p = 1 (r = 1.5) -> power-divergent", decide_r(g1, sig)[0] == "power-divergent"))
    sp = {k: 3.0 * k ** 0.3 for k in logR}; cases.append(("NEW: slow power p = 0.3 (r = 1.13) -> log-like or slow power", decide_r(sp, sig)[0] == LL))
    c5 = {k: 9.0 - 6.8 * k ** -0.5 for k in logR}; cases.append(("NEW: convergence p = 0.5 (r = 0.82, in the gap) -> INCONCLUSIVE", decide_r(c5, sig)[0].startswith("INCONCLUSIVE")))
    # R1 cap known answer: the 081c W8P8 checkpoint (unconverged at 5.8562) must cap s_max below 5.8562 (081c's analysis reported 6.0)
    st = json.load(open(os.path.join(HERE, "exp081c_results", "sigma_W8_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json")))
    r = S_T(st); cases.append((f"R1 cap on 081c W8P8: s_max {r['s_max']:.4f} < 5.8562 (r1 node {r['r1_cap']})", r["s_max"] < 5.8562 and r["r1_cap"] is not None))
    st2 = dict(st); s35 = [s for s, _ in nodes48() if s > 3.5][0]; st2[f"stats|{s35:.15f}"] = {"unconverged": 1}
    r2 = S_T(st2); cases.append((f"planted unconverged at {s35:.4f}: s_max {r2['s_max']:.4f} < {s35:.4f}", r2["s_max"] < s35))
    r3 = S_T(st, {"0.937": {"pass_": True}, "1.974": {"pass_": True}, "2.986": {"pass_": True}, "3.948": {"pass_": True}, "5.052": {"pass_": False}})
    cases.append((f"NEW: Step-0 fail at 5.052 caps s_max at 3.948 (got {r3.get('s_max')})", abs(r3.get("s_max", 9) - 3.94825275150273) < 1e-6))
    r4 = S_T(st, {"0.937": {"pass_": True}, "1.974": {"pass_": False}})
    cases.append(("NEW: Step-0 fail at 1.974 -> geometry void", r4.get("void") is True))
    for name, p in cases: print(f"  planted test: {name}: {'PASS' if p else 'FAIL'}"); ok &= bool(p)
    return ok

if __name__ == "__main__" and "--test" in sys.argv:
    print("EXP-081d analysis planted-value tests:"); ok = _tests(); print("ALL PASS" if ok else "SOME FAILED"); sys.exit(0 if ok else 1)

if __name__ == "__main__":
    import exp081b_run as Rn
    assert _tests(), "planted tests failed"
    D = os.path.join(HERE, "exp081d_results"); Cc = os.path.join(HERE, "exp081c_results")
    def ckpt(W, P, B):
        tag = f"sigma_W{W}_P{P}_box{B}_c2_cp12_sc3.0_dd0_ckpt.json"
        for d in (D, Cc):
            f = os.path.join(d, tag)
            if os.path.exists(f):
                st = json.load(open(f))
                if "n1c" in st: return st, f
                if "posctl" in st: return st, f
        return None, None
    out = {}; tails = {"T0": ({}, {}), "T1": ({}, {})}
    for k in (1, 1.5, 2, 2.5, 3):
        W1, W2, P = int(2 * k), int(4 * k), int(4 * k); B = P; Ny = 4 * P
        a, fa = ckpt(W1, P, B); b, fb = ckpt(W2, P, B)
        if a is None or b is None or "n1c" not in a or "n1c" not in b: out[k] = dict(missing=True, files=[fa, fb]); continue
        s0 = lambda W_: (json.load(open(f)) if os.path.exists(f := os.path.join(D, f'step0_W{W_}P{P}b{B}.json')) else None)
        sa, sb = S_T(a, s0(W1)), S_T(b, s0(W2))
        if sa.get('void') or sb.get('void'): out[k] = dict(void=True, why=[sa.get('why'), sb.get('why')]); continue
        kap = Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=W1, W2=W2, Wbox=B)
        f = 1.0 / Ny / (1 / W1 - 1 / W2) / kap
        RT = {t: -(sa[f"S_{t}"] - sb[f"S_{t}"]) * f for t in ("T0", "T1")}
        sig = abs(RT["T0"] - RT["T1"]) + abs(f) * (sa["cum"] + sb["cum"])
        comp = {c: -(0.5 * (a[c] - b[c])) * f for c in ("t0", "tsad")}; comp["C"] = -(0.5 * (sa["C0"] - sb["C0"])) * f
        out[k] = dict(R_T0=RT["T0"], R_T1=RT["T1"], sigma=sig, kappa=kap, components=comp, S_W1=sa, S_W2=sb, files=[fa, fb])
        for t in ("T0", "T1"): tails[t][0][k] = RT[t]; tails[t][1][k] = sig
        print(f"k={k}: R_T0 {RT['T0']:+.6f}  R_T1 {RT['T1']:+.6f}  sigma {sig:.1e}  kappa {kap:.6f}  s_max {sa['s_max']:.3f}/{sb['s_max']:.3f}  components {comp}")
    verdict, per = decide(tails); out["PRIMARY"] = dict(verdict=verdict, per_tail={t: dict(reading=v[0], r=v[1], sigma_r=v[2]) for t, v in per.items()})
    print("PRIMARY:", verdict, per)
    R = tails["T0"][0]
    if all(k in R for k in (1, 2, 3)): out["r_int_DESCRIPTIVE"] = (R[3] - R[2]) / (R[2] - R[1])
    ks = np.array(sorted(R)); Rv = np.array([R[k] for k in ks]); fits = {}
    if len(ks) >= 4:
        from scipy.optimize import curve_fit
        for nm, fn, p0 in (("a_power", lambda k, Ri, A, p: Ri + A * k ** (-p), (Rv[-1], Rv[0] - Rv[-1], 1.0)), ("b_log", lambda k, c, B: c + B * np.log(k), (Rv[0], 1.0)),
                           ("c_log_1k", lambda k, c, B, Dd: c + B * np.log(k) + Dd / k, (Rv[0], 1.0, 0.0))):
            try:
                p, _ = curve_fit(fn, ks, Rv, p0=p0, maxfev=20000); resid = Rv - fn(ks, *p); m = ks < 3
                pl, _ = curve_fit(fn, ks[m], Rv[m], p0=p0, maxfev=20000) if m.sum() > len(p0) else (None, None)
                fits[nm] = dict(params=list(p), resid=list(resid), loo_k3_pred=None if pl is None else float(fn(3.0, *pl)))
            except Exception as e: fits[nm] = dict(error=str(e))
    out["fits_DESCRIPTIVE"] = fits
    json.dump(out, open(os.path.join(HERE, "exp081d_results.json"), "w"), indent=1, default=str)
