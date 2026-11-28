"""EXP-100 part B analysis (registration notes/EXP-100_registration.md 4dbbf5a + am. 1 d9edfa5 + am. 2). [model: Opus 5.5]
Modes (venv interpreter, as the routes):
  KA   MERGED STORED   split-vs-whole known answer: t0, tsad, 48 g nodes and the n1c arms BITWISE; comparator plant first
                       (one node moved by one ulp in a copy must be reported as a mismatch). rc 1 on any mismatch.
  DRY                  the READ code on stand-ins: the stored convention-A W2P4 / W4P4 checkpoints serve as BOTH B0 and B1 with
                       t0 files built from their own t0 (on == off). Delta_B must be exactly 0; all controls must PASS. No B value exists.
  READ                 the B reading. Controls first; readings only if every control PASSES.
Pair slope (registration section 1): dk(a, b; G) = -[(S_T0(a) + Delta_a/2) - (S_T0(b) + Delta_b/2)] / Ny / (1/a - 1/b),
S_T0 from exp081d_analyze.S_T (verbatim), Delta = t0_on - t0_off from exp100_t0. Delta_B = [dk(B1) - dk(B0)] / dk(B1); tau = 0.01."""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, sigma3d as S3, exp081d_analyze as A81
D = os.path.join(HERE, "exp081d_results"); KF = 0.0396481; TAU = 0.01; FAILS = []
R_STORED_K1 = 2.2552242844155943; KAPPA_A_K1 = 0.017660021859253694      # exp090_k3.json R1.Rc.T0["1"]; exp099 row A kappa12 (k = 1)
GEOS = {"B0": dict(gL=8, gR=8, hT=4, Ny=16), "B1": dict(gL=16, gR=16, hT=8, Ny=32)}
def check(n, ok, det=""):
    print(f"{n:84s} {'PASS' if ok else 'FAIL'} {det}", flush=True)
    if not ok: FAILS.append(n)
def tagged(W, g, suf="_100B"): return os.path.join(D, f"sigma_W{W}_P4_box4_c2_cp12_sc3.0_dd0_gL{g['gL']}_gR{g['gR']}_hT{g['hT']}_Ny{g['Ny']}{suf}_ckpt.json")
def t0file(W, g): return os.path.join(D, f"exp100_t0_W{W}P4_gL{g['gL']}_gR{g['gR']}_hT{g['hT']}_Ny{g['Ny']}.json")
def ka_compare(a, b):
    keys = ["t0", "tsad"] + sorted(k for k in b if k.startswith("g|"))
    bad = [k for k in keys if a.get(k) != b[k]] + ([] if a.get("n1c", {}).get("arms") == b["n1c"]["arms"] else ["n1c.arms"])
    return keys, bad
def guards(nm, st):
    sm = st.get("summary", {}); pl = st.get("planted", {}); b2 = st.get("b2b", {})
    n48 = all(f"g|{s:.15f}" in st for s, _ in A81.nodes48())
    check(f"guards {nm}: 48 nodes, t0, tsad, summary present", n48 and "t0" in st and "tsad" in st and bool(sm))
    check(f"guards {nm}: planted must-fire FIRES and matches its prediction", bool(pl.get("fires")) and bool(pl.get("match")), f"impact {pl.get('impact', float('nan')):.1e}")
    check(f"guards {nm}: B2b converged+1 (<= 1e-12 rel)", bool(b2.get("pass_")), f"rel {b2.get('rel', float('nan')):.1e}")
    check(f"guards {nm}: t0 refined vs unrefined (<= 2e-6) and residue impact (<= 1e-7)", sm.get("t0_check", 1) <= 2e-6 and bool(sm.get("residue_ok")))
    print(f"   {nm}: Woodbury must-fire {'FIRES' if sm.get('woodbury_fires') else 'does not fire'} (reported only, as in the route)")
def X_of(nm, st, t0):
    s = A81.S_T(st, None)
    check(f"S_T {nm}: not void", not s.get("void"), str(s.get("why", "")))
    check(f"KA-t0 {nm}: exp100_t0 OFF == route t0 (1e-10 rel)", abs(t0["off"] - st["t0"]) <= 1e-10 * abs(st["t0"]), f"{t0['off'] - st['t0']:+.1e}")
    dl = t0["on"] - t0["off"]; return dict(S_T0=s["S_T0"], S_T1=s["S_T1"], cum=s["cum"], Delta=dl, sDelta=0.03 * abs(dl))
def dk(X, a, b, Ny):
    f = 1.0 / Ny / (1 / a - 1 / b)
    v = {t: -((X[a][f"S_{t}"] + 0.5 * X[a]["Delta"]) - (X[b][f"S_{t}"] + 0.5 * X[b]["Delta"])) * f for t in ("T0", "T1")}
    sig = abs(v["T0"] - v["T1"]) + abs(f) * (X[a]["cum"] + X[b]["cum"] + 0.5 * X[a]["sDelta"] + 0.5 * X[b]["sDelta"])
    return v["T0"], sig
def kfree(W1, W2, g):
    Sf = {W: float(S3.FreeStrip(W + g["gL"] + g["gR"], 2 * g["hT"], g["Ny"], list(range(g["gL"], g["gL"] + W)), g["hT"] - 1).S(cpts=12).real) for W in (W1, W2)}
    return -(Sf[W1] - Sf[W2]) / g["Ny"] / (1 / W1 - 1 / W2)
def known_answer():
    """KAN: the dk code on the stored convention-A W2P4 / W4P4 checkpoints, divided by the stored kappa_A(1), must give the stored R^c_T0(1)."""
    sa = json.load(open(os.path.join(D, "sigma_W2_P4_box4_c2_cp12_sc3.0_dd0_ckpt.json"))); sb = json.load(open(os.path.join(D, "sigma_W4_P4_box4_c2_cp12_sc3.0_dd0_ckpt.json")))
    z = lambda st: dict(off=st["t0"], on=st["t0"])
    X = {2: X_of("convA W2P4", sa, z(sa)), 4: X_of("convA W4P4", sb, z(sb))}; v, _ = dk(X, 2, 4, 16); R = v / KAPPA_A_K1
    check("KAN: dk code on stored convention-A k = 1 / kappa_A(1) == stored R^c_T0(1) (1e-12 rel)", abs(R / R_STORED_K1 - 1) <= 1e-12, f"{R / R_STORED_K1 - 1:+.1e}")
    return sa, sb
def read(mode):
    sa, sb = known_answer()
    if mode == "DRY":
        CK = {(G, W): (sa if W == 2 else sb) for G in GEOS for W in (2, 4)}; T0 = {k: dict(off=v["t0"], on=v["t0"]) for k, v in CK.items()}
        NY = {"B0": 16, "B1": 16}
    else:
        CK = {(G, W): json.load(open(tagged(W, g) if G == "B1" else tagged(W, g, ""))) for G, g in GEOS.items() for W in (2, 4)}
        T0 = {(G, W): json.load(open(t0file(W, g))) for G, g in GEOS.items() for W in (2, 4)}; NY = {G: g["Ny"] for G, g in GEOS.items()}
    for (G, W), st in CK.items(): guards(f"{G} W{W}", st)
    X = {G: {W: X_of(f"{G} W{W}", CK[(G, W)], T0[(G, W)]) for W in (2, 4)} for G in GEOS}
    r = {G: dk(X[G], 2, 4, NY[G]) for G in GEOS}; d0, d1 = r["B0"][0], r["B1"][0]; DB = (d1 - d0) / d1
    sDB = abs(d0 / d1) * math.hypot(r["B0"][1] / abs(d0), r["B1"][1] / abs(d1))
    # plant: move S_T0(B1, W = 2) so that dk(B1) -> 1.02 dk(B1); Delta_B must follow the prediction
    Xp = json.loads(json.dumps(X["B1"], default=float)); Xp = {int(k): v for k, v in Xp.items()}
    Xp[2]["S_T0"] -= 0.02 * d1 * NY["B1"] * (1 / 2 - 1 / 4); d1p = dk(Xp, 2, 4, NY["B1"])[0]; pred = (1.02 * d1 - d0) / (1.02 * d1)
    check("plant: dk(B1) x 1.02 via S_T0(B1, W2) moves Delta_B to its prediction (1e-9 abs)", abs((d1p - d0) / d1p - pred) <= 1e-9, f"{(d1p - d0) / d1p - pred:+.1e}")
    if mode == "DRY":
        check("DRY: identical stand-ins for B0 and B1 give Delta_B == 0 exactly", DB == 0.0, f"{DB!r}")
        for nm, f in (("node removed", lambda c: c.pop(sorted(k for k in c if k.startswith("g|"))[0])), ("planted not firing", lambda c: c["planted"].update(fires=False)),
                      ("B2b failing", lambda c: c["b2b"].update(pass_=False)), ("residue not ok", lambda c: c["summary"].update(residue_ok=False))):
            c = json.loads(json.dumps(sa)); f(c); n0 = len(FAILS); print(f"   [guard negative '{nm}': a FAIL is expected next]"); guards(f"planted-{nm}", c)
            fired = len(FAILS) > n0; del FAILS[n0:]; check(f"DRY guard negative '{nm}': the guard FIRES", fired)
        return
    if FAILS: print(f"CONTROLS FAILED {FAILS} -> STOP, no reading printed"); sys.exit(1)
    F = json.load(open(os.path.join(D, "exp100_free.json")))["chain"]["1"]
    kl = {G: kfree(2, 4, g) for G, g in GEOS.items()}
    for G, m in (("B0", "m1"), ("B1", "m2")):
        check(f"free kappa_lat(2, 4; {G}) == part-A chain T({m[1:]}) kappa12 (bitwise)", kl[G] == F[m]["T"]["kappa12"], f"{kl[G]!r}")
    if FAILS: print(f"CONTROLS FAILED {FAILS} -> STOP, no reading printed"); sys.exit(1)
    out = dict(registration="4dbbf5a+d9edfa5+am2", dk={G: dict(value=r[G][0], sigma=r[G][1]) for G in GEOS}, Delta_B=DB, sigma_Delta_B=sDB, tau=TAU,
               branch="sigma side has an IR (Lt) bias at k = 1" if abs(DB) > TAU else "no Lt bias above tau at k = 1",
               R_D={G: r[G][0] / KF for G in GEOS}, R_bracket={G: r[G][0] / kl[G] for G in GEOS}, kappa_lat=kl,
               Delta_t0={f"{G} W{W}": X[G][W]["Delta"] for G in GEOS for W in (2, 4)},
               convA_k1=dict(dk=R_STORED_K1 * KAPPA_A_K1, R_D=R_STORED_K1 * KAPPA_A_K1 / KF, label="convention A, IR-unconverged"))
    for G in GEOS: print(f"{G}: dk(2, 4) {r[G][0]:+.9f} +- {r[G][1]:.1e}; R_D = dk/kappa_free {r[G][0] / KF:.6f}; bracket dk/kappa_lat {r[G][0] / kl[G]:.6f} (kappa_lat {kl[G]:.6f})")
    print(f"Delta_B = [dk(B1) - dk(B0)]/dk(B1) = {DB:+.6f} +- {sDB:.1e}; tau {TAU} -> {out['branch']}")
    print(f"for comparison (convention A, IR-unconverged): dk(2, 4) {out['convA_k1']['dk']:+.9f}, R_D {out['convA_k1']['R_D']:.6f}")
    json.dump(out, open(os.path.join(D, "exp100_B.json"), "w"), indent=1)
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "KA":
        a, b = json.load(open(sys.argv[2])), json.load(open(sys.argv[3]))
        c = json.loads(json.dumps(a)); k0 = sorted(k for k in c if k.startswith("g|"))[0]; c[k0] = float(np.nextafter(c[k0], np.inf))
        _, badp = ka_compare(c, b); check("KA comparator plant: one node moved by one ulp is reported", badp == [k0], f"{badp}")
        keys, bad = ka_compare(a, b)
        check(f"KA split-vs-whole: {len(keys)} keys + n1c arms BITWISE", not bad, f"mismatches {len(bad)} {bad[:5]}")
    else: read(mode)
    if FAILS: print(f"FAILED: {FAILS}"); sys.exit(1)
    print("all controls PASS")
