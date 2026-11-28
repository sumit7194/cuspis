"""EXP-098 stage 0: third strip width W3 = 3P/4 at k = 1 (P = 4) and k = 2 (P = 8). Registration notes/EXP-098_registration.md (243b079).
[model: Opus 5.5]
Modes:  DRY  synthetic W3 (sigma AND free) on an exact s = s_inf + A/W line through the stored W1/W2 values: D must be 0 and R_q must equal
             R(W1,W2) (to 1e-12 rel); a planted 1/W^2 term must give the analytic D. No route output at a new width is opened.
        S0   the real stage-0 readings: needs the _098 checkpoints (W3P4, W6P8) and exp087_t0_W3P4.json / exp087_t0_W6P8.json.
Order (S0): KA-A (bitwise R(1), R(2) and Rc(1), Rc(2)) -> inputs -> plants P1 (1/W^2: D fires, R_q holds) and P2 (W3 wiring) -> readings.
Reused verbatim: exp081d_analyze.S_T; exp081b_run.free / pair; the Rk and corr() expressions of exp090_k3.py (same float order)."""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp081d_analyze as A81, exp081b_run as Rn
mode = sys.argv[1] if len(sys.argv) > 1 else "DRY"; assert mode in ("DRY", "S0")
FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:84s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); K25 = json.load(open(os.path.join(D, "exp090_k25.json")))
ref8 = json.load(open(os.path.join(D, "exp087_referee_W8P8.json")))
d8, s8 = ref8["on_1e-5"] - ref8["off_1e-5"], abs(ref8["off_1e-6"] - ref8["on_1e-5"])
def ck(W, P, suffix=""):                                     # exp090_k3.ck, plus the _098 suffix for the new widths
    tag = f"sigma_W{W}_P{P}_box{P}_c2_cp12_sc3.0_dd0{suffix}_ckpt.json"
    for d in (D, os.path.join(HERE, "exp081c_results")):
        f = os.path.join(d, tag)
        if os.path.exists(f) and "n1c" in json.load(open(f)): return f
    return None
def kappa(P, W1, W2): return Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=W1, W2=W2, Wbox=P)   # exp090_k3.kappa verbatim
def Rk(k, fa, fb, kap=None):                                 # exp090_k3.Rk verbatim (step0 is None at P <= 8)
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); B = P; Ny = 4 * P
    a, b = json.load(open(fa)), json.load(open(fb))
    s0 = lambda W_: (json.load(open(f)) if os.path.exists(f := os.path.join(D, f'step0_W{W_}P{P}b{B}.json')) else None)
    sa, sb = A81.S_T(a, s0(W1)), A81.S_T(b, s0(W2))
    if sa.get('void') or sb.get('void'): return dict(void=True, why=[sa.get('why'), sb.get('why')])
    kap = kappa(P, W1, W2) if kap is None else kap
    f = 1.0 / Ny / (1 / W1 - 1 / W2) / kap
    RT = {t: -(sa[f"S_{t}"] - sb[f"S_{t}"]) * f for t in ("T0", "T1")}
    sig = abs(RT["T0"] - RT["T1"]) + abs(f) * (sa["cum"] + sb["cum"])
    return dict(R_T0=RT["T0"], R_T1=RT["T1"], sigma=sig, kappa=kap)

# ---------------- the pair / drift / three-width functions (registration §2)
def pairR(P, a, b, X, F):
    """X[W] = dict(S_T0, S_T1, cum, Delta, sDelta); F[W] = free S. Corrected pair value in corr() float order."""
    Ny = 4 * P; kap = -(F[a] - F[b]) / Ny / (1 / a - 1 / b)        # exp081b_run.pair expression
    f = 1.0 / Ny / (1 / a - 1 / b) / kap
    R = {t: -(X[a][f"S_{t}"] - X[b][f"S_{t}"]) * f for t in ("T0", "T1")}
    Rc = {t: R[t] + 0.5 * (X[b]["Delta"] - X[a]["Delta"]) * (1.0 / (4 * P) / (1 / a - 1 / b) / kap) for t in R}
    sig = abs(Rc["T0"] - Rc["T1"]) + abs(f) * (X[a]["cum"] + X[b]["cum"] + 0.5 * X[a]["sDelta"] + 0.5 * X[b]["sDelta"])
    return dict(T0=Rc["T0"], T1=Rc["T1"], sigma=sig, kappa=kap, f=f, raw_T0=R["T0"])
def quadA(Ws, ys):
    M = np.array([[1.0, 1.0 / W, 1.0 / W ** 2] for W in Ws]); return float(np.linalg.solve(M, np.array(ys, float))[1])
def Rq(P, Ws, X, F, t):
    Ny = 4 * P
    As = quadA(Ws, [(X[W][f"S_{t}"] + 0.5 * X[W]["Delta"]) / Ny for W in Ws]); Af = quadA(Ws, [F[W] / Ny for W in Ws])
    return As / Af
def readings(k, X, F):
    P = 4 * k; W1, W3, W2 = P // 2, 3 * P // 4, P; Ws = (W1, W3, W2)
    p12, p13, p32 = pairR(P, W1, W2, X, F), pairR(P, W1, W3, X, F), pairR(P, W3, W2, X, F)
    Dt = {t: p13[t] - p32[t] for t in ("T0", "T1")}; sD = p13["sigma"] + p32["sigma"]
    rq = {t: Rq(P, Ws, X, F, t) for t in ("T0", "T1")}
    sq = abs(rq["T0"] - rq["T1"])
    for W in Ws:                                                       # finite-difference propagation of cum + sDelta/2
        h = 1e-6 * max(abs(X[W]["S_T0"]), 1.0); Xp = {w: dict(v) for w, v in X.items()}; Xm = {w: dict(v) for w, v in X.items()}
        Xp[W]["S_T0"] += h; Xm[W]["S_T0"] -= h
        sq += abs((Rq(P, Ws, Xp, F, "T0") - Rq(P, Ws, Xm, F, "T0")) / (2 * h)) * (X[W]["cum"] + 0.5 * X[W]["sDelta"])
    Rc = p12["T0"]
    seen = abs(Dt["T0"]) > 2 * sD and np.sign(Dt["T0"]) == np.sign(Dt["T1"])
    return dict(k=k, P=P, widths=Ws, R12=p12, R13=p13, R32=p32, D_T0=Dt["T0"], D_T1=Dt["T1"], sigma_D=sD, d=Dt["T0"] / Rc,
                sigma_d=sD / abs(Rc), drift_seen=bool(seen), Rq_T0=rq["T0"], Rq_T1=rq["T1"], sigma_q=sq, q=(rq["T0"] - Rc) / Rc, sigma_qrel=sq / abs(Rc))

# ---------------- inputs
def Xstored(k):
    P = 4 * k; W1, W2 = P // 2, P; out = {}
    for W in (W1, W2):
        st = A81.S_T(json.load(open(ck(W, P))), None)
        dl, sdl = (d8, s8) if (W, P) == (8, 8) else (0.0, 0.0)      # dW2(1) = 0, dW2(2) = d8, dW1 = 0 (exp090_k3.py)
        out[W] = dict(S_T0=st["S_T0"], S_T1=st["S_T1"], cum=st["cum"], Delta=dl, sDelta=sdl)
    return out
def Fstored(k): P = 4 * k; return {W: Rn.free(W, P, Wbox=P) for W in (P // 2, P)}

# ---------------- KA-A: the W1/W2 path reproduces stored R(1), R(2) and Rc(1), Rc(2) bitwise
for k in (1, 2):
    P = 4 * k; r = Rk(k, ck(P // 2, P), ck(P, P))
    check(f"KA-A k = {k}: Rk (verbatim) == exp081d_results.json (R_T0, R_T1, sigma, kappa bitwise)",
          all(r[x] == JD[str(k)][x] for x in ("R_T0", "R_T1", "sigma", "kappa")), f"R_T0 {r['R_T0']!r}")
    X, F = Xstored(k), Fstored(k); p = pairR(P, P // 2, P, X, F)
    check(f"KA-A k = {k}: pairR raw == Rk R_T0 and kappa (bitwise)", p["raw_T0"] == r["R_T0"] and p["kappa"] == r["kappa"], "")
    check(f"KA-A k = {k}: pairR corrected == exp090_k25.json Rc (bitwise)", p["T0"] == K25["Rc"][str(k)], f"{p['T0']!r} vs {K25['Rc'][str(k)]!r}")
if FAIL: print(f"\nSTOP: KA-A failed: {FAIL}"); sys.exit(1)

# ---------------- W3 inputs: DRY synthetic (exact 1/W line) or S0 real
def synth(k):
    P = 4 * k; W1, W3, W2 = P // 2, 3 * P // 4, P; X, F = Xstored(k), Fstored(k)
    lin = lambda y1, y2: y1 + (y2 - y1) * (1 / W3 - 1 / W1) / (1 / W2 - 1 / W1)     # exact s = s_inf + A/W through W1, W2
    X[W3] = {t: lin(X[W1][t] + (0.5 * X[W1]["Delta"] if t.startswith("S_") else 0), X[W2][t] + (0.5 * X[W2]["Delta"] if t.startswith("S_") else 0))
             for t in ("S_T0", "S_T1")}
    X[W3].update(cum=0.5 * (X[W1]["cum"] + X[W2]["cum"]), Delta=0.0, sDelta=0.0)
    for W in (W1, W2):                                                 # fold Delta into S so the line is exact in corrected S
        X[W] = dict(X[W], S_T0=X[W]["S_T0"] + 0.5 * X[W]["Delta"], S_T1=X[W]["S_T1"] + 0.5 * X[W]["Delta"], Delta=0.0)
    F[W3] = lin(F[W1], F[W2]); return X, F
def real(k):
    P = 4 * k; W3 = 3 * P // 4; X, F = Xstored(k), Fstored(k)
    f3 = ck(W3, P, "_098"); assert f3, f"missing _098 checkpoint W{W3}P{P}"
    st = A81.S_T(json.load(open(f3)), None); assert not st.get("void"), st
    e = json.load(open(os.path.join(D, f"exp087_t0_W{W3}P{P}.json")))
    check(f"KA-t0 W{W3}P{P}: exp087 OFF == route t0 (1e-10 rel)", abs(e["off"] - st["t0"]) <= 1e-10 * abs(st["t0"]), f"{e['off'] - st['t0']:+.1e}")
    dl = e["on"] - e["off"]; X[W3] = dict(S_T0=st["S_T0"], S_T1=st["S_T1"], cum=st["cum"], Delta=dl, sDelta=0.03 * abs(dl))
    F[W3] = Rn.free(W3, P, Wbox=P); return X, F
INP = {k: (synth(k) if mode == "DRY" else real(k)) for k in (1, 2)}

# ---------------- controls on the inputs
for k, (X, F) in INP.items():
    P = 4 * k; W1, W3, W2 = P // 2, 3 * P // 4, P; r0 = readings(k, X, F); Rc = r0["R12"]["T0"]
    if mode == "DRY":
        check(f"DRY k = {k}: exact 1/W line -> D_T0 == 0 (<= 1e-12 rel)", abs(r0["D_T0"]) <= 1e-12 * abs(Rc), f"{r0['D_T0']:+.2e}")
        check(f"DRY k = {k}: exact 1/W line -> R_q == R(W1,W2) (<= 1e-12 rel)", abs(r0["Rq_T0"] - Rc) <= 1e-12 * abs(Rc), f"{r0['Rq_T0'] - Rc:+.2e}")
    # P1: add Ny*B/W^2 to S at all three widths (S = Ny s); predicted D shift = -B[(1/W1+1/W3)/k13 - (1/W3+1/W2)/k32]
    k13, k32 = r0["R13"]["kappa"], r0["R32"]["kappa"]; unit = -((1 / W1 + 1 / W3) / k13 - (1 / W3 + 1 / W2) / k32)
    target = 10 * max(r0["sigma_D"], 1e-9 * abs(Rc)); B = target / unit; Ny = 4 * P
    Xp = {W: dict(v, S_T0=v["S_T0"] + Ny * B / W ** 2, S_T1=v["S_T1"] + Ny * B / W ** 2) for W, v in X.items()}; r1 = readings(k, Xp, F)
    mv = r1["D_T0"] - r0["D_T0"]
    check(f"P1 k = {k}: 1/W^2 plant moves D_T0 by the predicted {target:.3e} (1%) -> FIRES", abs(mv - target) <= 0.01 * abs(target), f"moved {mv:.3e}")
    check(f"P1 k = {k}: ... and R_q holds (<= 1e-9 rel)", abs(r1["Rq_T0"] - r0["Rq_T0"]) <= 1e-9 * abs(r0["Rq_T0"]), f"{r1['Rq_T0'] - r0['Rq_T0']:+.1e}")
    # P2: add eps to S(W3) only; predicted D shift = eps (f13 + f32)   [sign: see the registration amendment, 2026-11-28]
    f13, f32 = r0["R13"]["f"], r0["R32"]["f"]; eps = target / (f13 + f32)
    Xq = {W: dict(v) for W, v in X.items()}; Xq[W3]["S_T0"] += eps; mv2 = readings(k, Xq, F)["D_T0"] - r0["D_T0"]
    check(f"P2 k = {k}: eps on S(W3) moves D_T0 by eps (f13 + f32) = {target:.3e} (1%) -> FIRES", abs(mv2 - target) <= 0.01 * abs(target), f"moved {mv2:.3e}")
if FAIL: print(f"\nSTOP: control(s) failed: {FAIL} -> no reading"); sys.exit(1)

# ---------------- readings (registration §3; DESCRIPTIVE)
out = dict(mode=mode, registration="243b079", readings={})
for k, (X, F) in INP.items():
    r = readings(k, X, F); out["readings"][str(k)] = r
    print(f"\n{'(DRY, SYNTHETIC W3 - NOT A RESULT) ' if mode == 'DRY' else ''}k = {k} (W = {r['widths']}): R(W1,W3) {r['R13']['T0']:+.6f}  R(W3,W2) {r['R32']['T0']:+.6f}  R(W1,W2) {r['R12']['T0']:+.6f}")
    print(f"  D_T0 {r['D_T0']:+.3e}  D_T1 {r['D_T1']:+.3e}  sigma_D {r['sigma_D']:.2e}  d = {r['d']:+.4%} +- {r['sigma_d']:.4%}  drift seen: {r['drift_seen']}")
    print(f"  R_q T0 {r['Rq_T0']:+.6f}  T1 {r['Rq_T1']:+.6f}  sigma_q {r['sigma_q']:.2e}  q = {r['q']:+.4%} +- {r['sigma_qrel']:.4%}"
          + (f"   Delta(W3) {X[r['widths'][1]]['Delta']:+.3e}" if mode == "S0" else ""))
json.dump(out, open(os.path.join(D, f"exp098_stage0{'_DRY' if mode == 'DRY' else ''}.json"), "w"), indent=1, default=float)
print(f"\nEXP-098 stage 0 ({mode}{'; SYNTHETIC W3, NOT A RESULT' if mode == 'DRY' else ''}): controls PASS; readings DESCRIPTIVE (basis of the k = 3 seal)")
