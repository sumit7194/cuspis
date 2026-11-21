"""EXP-081c analysis (registered 8fcfb84 + R1 440b49f). Committed, with its planted-value tests, BEFORE the W8P8 target
is read. [model: Opus 5.5]

Verdict logic (`decide`, pure function, tested below with planted inputs):
  void / unmeasured gates -> INCONCLUSIVE with the reason;
  sigma_W = |R48(8, b8) - R24(8, b4)| enters in quadrature with the 081b route sigma (and any extra systematics), per tail;
  decided only if the 2 sigma interval of R_inf + 0.4503 excludes 0 under BOTH tails, with the same sign;
  rho = |R48(P8, b8) / R24(P4, b4) - 1| -> "resolution-stable to 10% under one doubling" (<= 0.10) or
  "not resolution-stable under one doubling" (> 0.10); Richardson 2 R48 - R24(P4) is DESCRIPTIVE.
Inputs from: exp081b_results_impact.json (081b impact rule, unchanged), 081b checkpoints (W4P8b8 under the impact rule),
exp081c_results/ (W8P8 target, W2P8b8), free-side files, Step 0 / B2a results, N4c."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
THR = 0.4503

def decide(g):
    """g: dict of gate booleans and numbers. Returns dict(verdict, reasons, per-tail numbers, labels)."""
    reasons = []
    for k, why in (("step0_ok", "Step 0 failed"), ("b2a_ok", "B2a failed"), ("b2a_mustfire", "B2a must-fire did not fire (void)"),
                   ("posctl_ok", "positive control failed"), ("planted_fires", "planted must-fire did not fire (void)"),
                   ("planted_match", "planted must-fire magnitude off by > 10% (void)"), ("b2b_ok", "B2b failed"),
                   ("t0_ok", "t0 refined vs unrefined failed"), ("residue_ok", "residue check failed"),
                   ("census_ok", "pole census flagged W8P8 or W2P8b8"), ("w8_measured", "nuisance unmeasured (W8P8 failed N1'''c)")):
        if not g[k]: reasons.append(why)
    out = dict(reasons=reasons)
    tails = {}
    for t in ("T0", "T1"):
        R48 = g["R48"][t]; sW = abs(R48 - g["R8"]) if np.isfinite(R48) else float("nan")
        extra2 = sum(e ** 2 for e in g.get("extra", []))
        sg = float(np.sqrt(g["si"] ** 2 + sW ** 2 + extra2)); stat = g["Rq"] + THR
        tails[t] = dict(R48=R48, sigma_W=sW, sigma=sg, stat=stat, decided=bool(np.isfinite(sg) and abs(stat) > 2 * sg),
                        sign=int(np.sign(stat)) if np.isfinite(sg) else 0)
    out["tails"] = tails
    if reasons: out["verdict"] = "INCONCLUSIVE (" + "; ".join(reasons) + ")"
    elif tails["T0"]["decided"] and tails["T1"]["decided"] and tails["T0"]["sign"] == tails["T1"]["sign"]:
        out["verdict"] = f"DECIDED (both tails): R_inf + 0.4503 {'> 0' if tails['T0']['sign'] > 0 else '< 0'}"
    else: out["verdict"] = "INCONCLUSIVE (2 sigma interval includes 0 under at least one tail, or tails disagree)"
    rho = abs(g["R48"]["T0"] / g["R24_P4"] - 1) if np.isfinite(g["R48"]["T0"]) else float("nan")
    out["rho"] = rho
    out["rho_label"] = ("resolution-stable to 10% under one doubling" if rho <= 0.10 else
                        "NOT resolution-stable under one doubling (refinement series to be registered separately)") if np.isfinite(rho) else "rho undefined"
    out["richardson_DESCRIPTIVE"] = 2 * g["R48"]["T0"] - g["R24_P4"]
    return out

def _planted_tests():
    base = dict(step0_ok=True, b2a_ok=True, b2a_mustfire=True, posctl_ok=True, planted_fires=True, planted_match=True, b2b_ok=True,
                t0_ok=True, residue_ok=True, census_ok=True, w8_measured=True, R48={"T0": 2.70, "T1": 2.70}, R8=2.6441,
                si=0.2919, Rq=2.4065, R24_P4=2.2552, extra=[])
    cases = []
    r = decide(base); cases.append(("small sigma_W -> decided > 0", r["verdict"].startswith("DECIDED") and "> 0" in r["verdict"]))
    r = decide(dict(base, R48={"T0": 9.0, "T1": 9.0})); cases.append(("sigma_W 6.4 -> inconclusive", r["verdict"].startswith("INCONCLUSIVE (2 sigma")))
    r = decide(dict(base, planted_fires=False)); cases.append(("planted not firing -> void", "void" in r["verdict"]))
    r = decide(dict(base, w8_measured=False)); cases.append(("W8 unmeasured -> inconclusive", "unmeasured" in r["verdict"]))
    r = decide(dict(base, R48={"T0": 2.70, "T1": float("nan")})); cases.append(("T1 undefined -> inconclusive", r["verdict"].startswith("INCONCLUSIVE")))
    r = decide(dict(base, Rq=-0.44, R48={"T0": -0.44, "T1": -0.44}, R8=-0.44, si=0.01))   # stat 0.0103 < 2 sigma 0.02 (first version used -0.40: stat 0.0503 > 0.02 is correctly decided; test-input error, kept in report); cases.append(("near threshold -> inconclusive", r["verdict"].startswith("INCONCLUSIVE")))
    r = decide(dict(base, Rq=-2.0, R8=-2.0, R48={"T0": -2.0, "T1": -2.0}, R24_P4=-2.0)); cases.append(("negative -> decided < 0", "< 0" in r["verdict"]))
    r = decide(dict(base, R48={"T0": 2.2552 * 1.2, "T1": 2.2552 * 1.2})); cases.append(("rho 0.2 -> not resolution-stable", r["rho_label"].startswith("NOT")))
    r = decide(base); cases.append(("rho 0.197 at R48 2.70 -> NOT stable", abs(r["rho"] - (2.70 / 2.2552 - 1)) < 1e-12 and r["rho_label"].startswith("NOT")))
    r = decide(dict(base, R48={"T0": 2.30, "T1": 2.30})); cases.append(("rho 0.02 -> stable", r["rho_label"].startswith("resolution-stable")))
    r = decide(dict(base, extra=[10.0])); cases.append(("extra systematic 10 -> inconclusive", r["verdict"].startswith("INCONCLUSIVE")))
    ok = all(c[1] for c in cases)
    for name, passed in cases: print(f"  planted test: {name}: {'PASS' if passed else 'FAIL'}")
    return ok

if __name__ == "__main__" and "--test" in sys.argv:
    print("EXP-081c analysis planted-value tests:"); ok = _planted_tests(); print("ALL PASS" if ok else "SOME FAILED"); sys.exit(0 if ok else 1)

if __name__ == "__main__":
    import exp081b_run as R, exp081b_analyze as A
    assert _planted_tests(), "planted tests failed"
    b = json.load(open(os.path.join(HERE, "exp081b_results_impact.json")))
    Rq, si = b["S_T0"]["route_i"]; R8 = b["S_T0"]["R"]["8"] if "8" in b["S_T0"]["R"] else b["S_T0"]["R"][8]
    R24_P4 = b["S_T0"]["R"]["4"] if "4" in b["S_T0"]["R"] else b["S_T0"]["R"][4]
    assert b["S_T0"]["premise"], "081b premise flag"
    C_OUT = os.path.join(HERE, "exp081c_results"); tagW8 = "sigma_W8_P8_box8_c2_cp12_sc3.0_dd0"
    tc = json.load(open(os.path.join(C_OUT, tagW8 + "_ckpt.json")))
    # W8P8 under N1'''c: write an 081b-format view (g as [g, None], chk = unrefined arm) and apply 081b's impact-rule machinery
    view = {"t0": tc["t0"], "tsad": tc["tsad"]}
    for k, v in tc.items():
        if k.startswith("g|"): view[k] = [v, None]
    for s, gu in tc["n1c"]["arms"].items(): view[f"chk|{float(s):.15f}"] = gu
    # non-convergence cap (R1): first node >= tier with an unconverged G caps s_max below it
    capnodes = sorted(float(k.split("|")[1]) for k, v in tc.items() if k.startswith("stats|") and k[6:7].isdigit() and v["unconverged"])
    if capnodes:   # R1 cap: force the first checkpoint at/above the first non-converged node to fail -> s_max = previous checkpoint
        cks = sorted(float(k.split("|")[1]) for k in view if k.startswith("chk|")); first = [c for c in cks if c >= capnodes[0]]
        if first: view[f"chk|{first[0]:.15f}"] = view[f"g|{first[0]:.15f}"][0] + 1e300
        print(f"non-converged G at node {capnodes[0]:.4f}: s_max capped below it (R1)")
    vfile = os.path.join(C_OUT, tagW8 + "_as081b_ckpt.json"); json.dump(view, open(vfile, "w"))
    A.OUT = C_OUT; w8 = A.S_from_ckpt(tagW8 + "_as081b", "impact"); cap = A.CUM["impact"][tagW8 + "_as081b"]; A.OUT = R.OUT
    w4 = A.S_from_ckpt("sigma_W4_P8_box8_c2_cp12_sc3.0_dd0", "impact")
    kap48 = R.pair(lambda W, P, **kw: R.free(W, P, **kw), 8, W1=4, W2=8, Wbox=8)
    Ny = 32; R48 = {}
    for t in ("T0", "T1"):
        R48[t] = (-(w4["S_" + t] - w8["S_" + t]) / Ny / (1 / 4 - 1 / 8) / kap48) if w8 else float("nan")
    st0 = json.load(open(os.path.join(HERE, "exp081c_step0_results.json")))
    b2a = json.load(open(os.path.join(HERE, "exp081c_b2a_results.json")))
    pc = [json.load(open(os.path.join(C_OUT, f"sigma_{g}_c2_cp12_sc3.0_dd0_ckpt.json")))["posctl"] for g in ("W2_P8_box4", "W4_P8_box8")]
    n4 = json.load(open(os.path.join(HERE, "exp081c_n4c_results.json")))
    cen = json.load(open(os.path.join(HERE, "exp081c_census_results.json")))
    pl = tc["planted"]; sm = tc["summary"]
    extra = [2 * abs(n4["dR"])] if abs(n4["dR"]) > 0.1 * si else []
    g = dict(step0_ok=all(v["pass_"] for k, v in st0.items() if k in ("0.937", "1.974")), b2a_ok=b2a["pass_"], b2a_mustfire=b2a["mustfire_fires"],
             posctl_ok=all(p["pass_"] for p in pc), planted_fires=pl["fires"], planted_match=pl["match"], b2b_ok=tc["b2b"]["pass_"],
             t0_ok=sm["t0_check"] <= 2e-6, residue_ok=sm["residue_rel"] <= 1e-8, census_ok=cen["ok"],
             w8_measured=bool(w8 is not None and w8["s_max"] > 0), R48=R48, R8=R8, si=si, Rq=Rq, R24_P4=R24_P4, extra=extra)
    out = decide(g)
    # decomposition (descriptive): resolution at fixed box 8, and box width at fixed resolution
    A.OUT = C_OUT; s2b8 = A.S_from_ckpt("sigma_W2_P8_box8_c2_cp12_sc3.0_dd0", "impact"); A.OUT = R.OUT
    kap24b8 = R.pair(lambda W, P, **kw: R.free(W, P, **kw), 8, W1=2, W2=4, Wbox=8)
    R24b8 = -(s2b8["S_T0"] - w4["S_T0"]) / Ny / (1 / 2 - 1 / 4) / kap24b8
    out.update(R24_b8=R24b8, resolution_part=R48["T0"] - R24b8, box_part=R24b8 - R8, kap48=kap48, kap24b8=kap24b8,
               W8_s_max=w8["s_max"] if w8 else 0.0, W8_cum=cap, n4c=n4, n4_prediction_ok=bool(abs(n4["dR"]) <= 1e-4),
               gates=g, components={"W8P8": dict(t0=tc["t0"], tsad=tc["tsad"]), "W4P8b8": "081b ckpt"})
    json.dump(out, open(os.path.join(HERE, "exp081c_results.json"), "w"), indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))
