"""EXP-090 k = 3 part (registration notes/EXP-090_registration.md §3-§6 and amendment 1, 65e0b6a "frozen after the 11-28 exposure of S").
[model: Opus 5.5]
Modes:  DRY   code-path test on a PLANTED k = 3 (never opens the W6P12 / W12P12 checkpoints, their G files, or the A6 W12 result):
              exercises every reading, gate and control with synthetic inputs; prints only planted-input readings.
        K3    the real k = 3 readings (ONLY on the Bridge's go, after the EXP-096 amendment-6 READING): (R1) R^c(3), (R2) row 2,
              (R4) 081e PRIMARY (a) as registered and (b) corrected, (R5) pair 2 -> 3 (descriptive), (R6) S-1/S-2/S-3 and sub-seals.
Order inside K3: K1-K6 (exp090_reread.py CONTROLS, must exit 0) -> gates 1-3 and 4' -> K-k3 controls (KA-R at k = 2 bitwise through THIS
code path, kappa(3) bitwise vs EXP-091, K2 at W12P12, placement plant at k = 3) -> amendment-6 dependency (s_KA) -> readings.
Code reused VERBATIM: exp081d_analyze.S_T / decide / decide_r (imported); slope_and_sigma and sband from exp085c_run READ (as in
exp090_reread.py; slope_and_sigma takes the k list as an argument, otherwise unchanged); the 081d R(k) block (exp081d_analyze __main__).
Choices the registration does NOT fix are labelled DESCRIPTIVE in the output (amendment 1, item 7); they are listed in IMPLEMENTATION_NOTES."""
import sys, os, re, json, time, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp081d_analyze as A81
mode = sys.argv[1] if len(sys.argv) > 1 else "DRY"
assert mode in ("DRY", "K3"), "mode must be DRY or K3"
FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:78s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
IMPLEMENTATION_NOTES = [
    "N1 (R2) row 2: rho_s uses g_raw^c as DEFINED in §2 (slope over k in {1, 1.5, 2, 2.5}), PRIMARY (Bridge ruling 2026-11-28: the frozen definition); the k <= 3 denominator is printed beside it, DESCRIPTIVE.",
    "N2 (R6) S-1 / S-2: the header gives a 68% band and an outer band without naming which is the PASS band (S-3 names it). Both are "
    "printed; the S-1 / S-2 main-seal grades are DESCRIPTIVE (Bridge ruling 2026-11-28: not fixed before the exposure, so not fixable now).",
    "N3 (R4) robustness / secondary-sigma rows use the same decide() on the same tails; only sigma changes.",
]
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); K25 = [1, 1.5, 2, 2.5]; KS3 = [1, 1.5, 2, 2.5, 3]

# ---------------- verbatim helpers (exp085c_run READ via exp090_reread.py; k list as argument)
def slope_and_sigma(out, sg, KS):
    ks = np.array(KS, float)
    y = np.array([out[k] for k in KS]); g, b0 = np.polyfit(ks, y, 1); Sxx = np.sum((ks - ks.mean()) ** 2)
    ssr = np.sum((y - (g * ks + b0)) ** 2); s_fit = np.sqrt(ssr / (len(ks) - 2) / Sxx)
    w = (ks - ks.mean()) / Sxx; s_prop = np.sqrt(np.sum((w * np.array([sg[k] for k in KS])) ** 2))
    return float(g), float(np.hypot(s_fit, s_prop))
def sband(r, s):
    lo, hi = r - 2 * s, r + 2 * s
    if hi < -0.1: return "overshoot"
    if lo >= -0.1 and hi <= 0.1: return "supported"
    if lo > 0.1 and hi < 0.5: return "partial"
    if lo >= 0.5: return "refuted as sole cause"
    return "INCONCLUSIVE (straddles a band edge)"

# ---------------- K1-K6 first (the committed controls; exit 0 required)
r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "exp090_reread.py"), "CONTROLS"], capture_output=True, text=True, cwd=HERE)
check("K1-K6: exp090_reread.py CONTROLS exits 0", r.returncode == 0, f"rc {r.returncode}")
if FAIL: print(r.stdout[-2000:]); sys.exit(1)

# ---------------- the 081d R(k) block (verbatim from exp081d_analyze __main__), with an explicit file map
import exp081b_run as Rn
def kappa(P, W1, W2): return Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=W1, W2=W2, Wbox=P)
def Rk(k, fa, fb, kap=None):
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); B = P; Ny = 4 * P
    a, b = json.load(open(fa)), json.load(open(fb))
    s0 = lambda W_: (json.load(open(f)) if os.path.exists(f := os.path.join(D, f'step0_W{W_}P{P}b{B}.json')) else None)
    sa, sb = A81.S_T(a, s0(W1)), A81.S_T(b, s0(W2))
    if sa.get('void') or sb.get('void'): return dict(void=True, why=[sa.get('why'), sb.get('why')])
    kap = kappa(P, W1, W2) if kap is None else kap
    f = 1.0 / Ny / (1 / W1 - 1 / W2) / kap
    RT = {t: -(sa[f"S_{t}"] - sb[f"S_{t}"]) * f for t in ("T0", "T1")}
    sig = abs(RT["T0"] - RT["T1"]) + abs(f) * (sa["cum"] + sb["cum"])
    comp = {c: -(0.5 * (a[c] - b[c])) * f for c in ("t0", "tsad")}; comp["C"] = -(0.5 * (sa["C0"] - sb["C0"])) * f
    return dict(R_T0=RT["T0"], R_T1=RT["T1"], sigma=sig, kappa=kap, components=comp, S_W1=sa, S_W2=sb, t0_W1=a["t0"], t0_W2=b["t0"])
def ck(W, P):
    tag = f"sigma_W{W}_P{P}_box{P}_c2_cp12_sc3.0_dd0_ckpt.json"
    for d in (D, os.path.join(HERE, "exp081c_results")):
        f = os.path.join(d, tag)
        if os.path.exists(f) and "n1c" in json.load(open(f)): return f
    return None
# KA-R: k = 2 through THIS code path must equal the stored 081d R(2) bitwise (both tails and sigma)
t = time.time(); r2 = Rk(2, ck(4, 8), ck(8, 8))
check("KA-R k = 2 through this code path == exp081d_results.json (R_T0, R_T1, sigma, kappa bitwise)",
      all(r2[x] == JD["2"][x] for x in ("R_T0", "R_T1", "sigma", "kappa")), f"({time.time()-t:.0f} s) R_T0 {r2['R_T0']!r} vs {JD['2']['R_T0']!r}")
kap3 = kappa(12, 6, 12); K91 = json.load(open(os.path.join(D, "exp091_grade.json")))
check("kappa(3) via exp081b_run.pair == EXP-091 stored kappa3 (bitwise)", kap3 == K91["kappa3"], f"{kap3!r}")
def norm(k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / (kap3 if k == 3 else JD[str(k)]["kappa"])
check("norm(3) == EXP-091 norm3 (1e-12 rel)", abs(norm(3) - K91["norm3"]) <= 1e-12 * K91["norm3"], f"{norm(3):.10f}")

# ---------------- corrections (from files; §2) and sigma rows (§2 + amendment 1 items 2-3)
ref8 = json.load(open(os.path.join(D, "exp087_referee_W8P8.json"))); f10 = json.load(open(os.path.join(D, "exp087_t0_W10P10.json")))
f12 = json.load(open(os.path.join(D, "exp087_t0_W12P12.json")))
art = {(int(m[0]), int(m[1])): -float(m[2]) for m in re.findall(r"W(\d+) P(\d+) Wb\d+ Ny\d+ rad 1e-05: predicted delta_t0 \(code - true\) = ([-+0-9.]+)",
       open(os.path.join(HERE, "..", "notes", "EXP-087_tinybox", "b_art_prod.txt")).read())}
d8, d10, d12 = ref8["on_1e-5"] - ref8["off_1e-5"], f10["on"] - f10["off"], f12["on"] - f12["off"]
s8, s10, s12 = abs(ref8["off_1e-6"] - ref8["on_1e-5"]), abs(d10 - art[(10, 10)]), abs(d12 - art[(12, 12)])
G96 = json.load(open(os.path.join(D, "exp096", "grade_W12P12.json"))); D96 = abs(G96["D"])
S_KA0 = 7.84e-7

# ---------------- k = 3 inputs: REAL (K3) or PLANTED (DRY)
F6 = os.path.join(D, "sigma_W6_P12_box12_c2_cp12_sc3.0_dd0_081e_ckpt.json"); F12 = os.path.join(D, "sigma_W12_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json")
def G(W, P): return json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json")))
def Rop(key, k, G1, G2): return -(G1[key] - G2[key]) * norm(k)
def k3_gates():
    rk3 = open(os.path.join(D, "run_k3.txt")).read(); r6 = open(os.path.join(D, "run_w6p12.txt")).read()
    check("gate 1: W12 route rc 0 with the stale-file guard PASS (run_k3.txt)", "e_route_W12_r2 rc 0" in rk3 and "stale-file guard PASS" in rk3, "")
    c1 = open(os.path.join(D, "e_c1_W12.out")).read()
    check("gate 2: C1 W12 rc 0 and its C1 row PASS", "e_c1_W12 rc 0" in rk3 and re.search(r"C1 W12P12box12c2: .*-> PASS", c1) is not None, "")
    check("gate 3: exp087_t0_W12P12.json exists, K2 OFF == W12 route t0 (1e-10 rel)",
          abs(f12["off"] - json.load(open(F12))["t0"]) <= 1e-10 * abs(f12["off"]), "")
    i = r6.rfind("e_route_W6_081e_r1 rc 0")
    check("gate 4': W6P12 rerun rc 0, stale-file guard PASS after it, run_w6p12.done", i >= 0 and "stale-file guard PASS" in r6[i:]
          and os.path.exists(os.path.join(D, "run_w6p12.done")), "")
if mode == "K3":
    k3_gates()
    if FAIL: print(f"\nSTOP: gate(s) failed -> k = 3 readings VOID: {FAIL}"); sys.exit(1)
    R3 = Rk(3, F6, F12, kap3)
    if R3.get("void"): print(f"k = 3 VOID: {R3['why']}"); sys.exit(1)
    G6, G12 = G(6, 12), G(12, 12)
    A6 = os.path.join(D, "exp096", "W12P12Wb12Ny48_r2_onoff.json")
    if os.path.exists(A6):
        a6 = json.load(open(A6))["reading"]; s_KA = 0.0 if a6.startswith("R-a") else S_KA0
        s_lab = f"amendment-6 READING: {a6} -> s_KA {'dropped (R-a)' if s_KA == 0 else 'kept'}"
    elif time.time() >= time.mktime(time.strptime("2026-11-28 18:00", "%Y-%m-%d %H:%M")):
        s_KA, s_lab = S_KA0, "amendment-6 READING not landed by 2026-11-28 18:00 -> s_KA INCLUDED (amendment 1 item 5)"
    else:
        print("STOP: the amendment-6 READING has not landed and it is before 18:00 (amendment 1 item 5): no k = 3 reading"); sys.exit(1)
else:   # DRY: planted k = 3 built from the k = 2.5 values (no k = 3 file opened)
    R3 = dict(R_T0=JD["2.5"]["R_T0"] + 2.0, R_T1=JD["2.5"]["R_T1"] + 2.0, sigma=JD["2.5"]["sigma"], kappa=kap3,
              components={c: v + 1.0 for c, v in JD["2.5"]["components"].items()}, t0_W1=-100.0, t0_W2=-480.0)
    G6 = dict(X_cA=0.0, X_Lam=51.0); G12 = dict(X_cA=-0.5, X_Lam=241.0)
    s_KA, s_lab = S_KA0, "DRY: s_KA kept (planted)"
print(f"\n{s_lab}")

# ---------------- K-k3 controls

# ---------------- series (k <= 2.5 from JD, k = 3 from R3), corrected per §2, sigma rows per amendment 1
R = {t: {**{k: JD[str(k)][f"R_{t}"] for k in K25}, 3: R3[f"R_{t}"]} for t in ("T0", "T1")}
sR = {**{k: JD[str(k)]["sigma"] for k in K25}, 3: R3["sigma"]}
comp = {**{k: JD[str(k)]["components"] for k in K25}, 3: R3["components"]}
dW2 = {1: 0.0, 1.5: 0.0, 2: d8, 2.5: d10, 3: d12}; dW1 = {k: 0.0 for k in KS3}
def sigrows(sd12, extra):
    sd = {1: 0.0, 1.5: 0.0, 2: s8, 2.5: s10, 3: sd12}
    out = {k: float(np.hypot(sR[k], 0.5 * sd[k] * norm(k))) for k in KS3}
    out[3] = float(np.hypot(out[3], 0.5 * extra * norm(3))); return out
SIG = {"primary": sigrows(s12, s_KA), "robust": {k: float(np.hypot(sR[k], 0.5 * 0.03 * abs(dW2[k]) * norm(k))) for k in KS3},
       "secondary": sigrows(float(np.hypot(D96, s_KA)), 0.0)}
SIG["robust"][3] = float(np.hypot(SIG["robust"][3], 0.5 * s_KA * norm(3)))
def corr(Rt, w2, w1): return {k: Rt[k] + 0.5 * (w2[k] - w1[k]) * norm(k) for k in KS3}       # §2 R^c (the one function every reading uses)
zero3 = {k: 0.0 for k in KS3}; pw = corr(R["T0"], {**zero3, 3: 1.0}, zero3); pn = corr(R["T0"], zero3, {**zero3, 3: 1.0})
check("K3' placement plant at k = 3 through corr(): +1 on WIDE W2 = 12 moves R(3) by +norm(3)/2, on NARROW W1 = 6 by -norm(3)/2 (1e-12)",
      abs(pw[3] - R["T0"][3] - 0.5 * norm(3)) <= 1e-12 * norm(3) and abs(pn[3] - R["T0"][3] + 0.5 * norm(3)) <= 1e-12 * norm(3)
      and all(pw[k] == R["T0"][k] for k in K25), "")
Rc = {t: corr(R[t], dW2, dW1) for t in R}
t0c = {k: comp[k]["t0"] + 0.5 * (dW2[k] - dW1[k]) * norm(k) for k in KS3}
Y = {**{k: Rop("X_cA", k, G(int(2 * k), int(4 * k)), G(int(4 * k), int(4 * k))) for k in K25}, 3: Rop("X_cA", 3, G6, G12)}
XL = {**{k: Rop("X_Lam", k, G(int(2 * k), int(4 * k)), G(int(4 * k), int(4 * k))) for k in K25}, 3: Rop("X_Lam", 3, G6, G12)}
grawc = float(np.polyfit(np.array(K25, float), [Rc["T0"][k] for k in K25], 1)[0])
k25 = json.load(open(os.path.join(D, "exp090_k25.json")))
check("consistency: g_raw^c recomputed == exp090_k25.json graw_c (bitwise)", grawc == k25["graw_c"], f"{grawc!r}")
if FAIL: print(f"\nSTOP: control(s) failed before any reading: {FAIL} -> no k = 3 reading"); sys.exit(1)
out = dict(mode=mode, notes=IMPLEMENTATION_NOTES, s_KA=s_KA, s_label=s_lab, Delta=dict(W12P12=d12), sigma_Delta=dict(W12P12_primary=s12, W12P12_secondary=float(np.hypot(D96, s_KA))))

# (R1) descriptive
ls = [(Rc["T0"][b] - Rc["T0"][a]) / (b - a) for a, b in zip(KS3[:-1], KS3[1:])]
print(f"\n(R1) R^c_T0(k) {[round(Rc['T0'][k], 5) for k in KS3]}  R^c_T1(3) {Rc['T1'][3]:+.5f}  sigma^c(3) {SIG['primary'][3]:.2e}  local slopes {[round(x, 3) for x in ls]}  [descriptive]")
out["R1"] = dict(Rc=Rc, sigma=SIG, local=ls)
# (R2) row 2
row = {}
for nm, sg in SIG.items():
    gA, sA = slope_and_sigma({k: Rc["T0"][k] - Y[k] for k in KS3}, sg, KS3); row[nm] = (gA, sA, gA / grawc, sA / grawc, sband(gA / grawc, sA / grawc))
b = row["primary"][4]
if row["robust"][4] != b: b = "INCONCLUSIVE (robustness)"
dep = " [sigma_Delta-choice dependent]" if row["secondary"][4] != row["primary"][4] else ""
r1band = k25["readA"]; krange = "" if r1band == b else f" [k-range dependent: row 1 {r1band}]"
graw3 = float(np.polyfit(np.array(KS3, float), [Rc["T0"][k] for k in KS3], 1)[0])
print(f"(R2) row 2 (k = 1..3): g_A {row['primary'][0]:+.4f} +- {row['primary'][1]:.4f}  rho_s {row['primary'][2]:+.4f} +- {row['primary'][3]:.4f} -> {b}{dep}{krange}"
      f"   [secondary-sigma: {row['secondary'][4]}; robustness: {row['robust'][4]}; descriptive N1: / g_raw over k<=3 {graw3:+.4f} -> rho {row['primary'][0]/graw3:+.4f}]")
out["R2"] = dict(rows={k: list(v) for k, v in row.items()}, reading=b + dep + krange, graw3_descriptive=graw3)
# (R4) 081e PRIMARY
ra, pa = A81.decide({t: ({k: R[t][k] for k in (1, 1.5, 2, 3)}, {k: sR[k] for k in (1, 1.5, 2, 3)}) for t in R})
rb = {nm: A81.decide({t: ({k: Rc[t][k] for k in (1, 1.5, 2, 3)}, {k: sg[k] for k in (1, 1.5, 2, 3)}) for t in Rc}) for nm, sg in SIG.items()}
r4 = rb["primary"][0]
if rb["robust"][0] != r4: r4 = "INCONCLUSIVE (robustness)"
dep4 = " [sigma_Delta-choice dependent]" if rb["secondary"][0] != rb["primary"][0] else ""
print(f"(R4)(a) 081e as registered (carries the EXP-087 defect at W8P8 and W12P12): {ra}  {[(t, round(v[1], 4), round(v[2], 4)) for t, v in pa.items()]}")
print(f"(R4)(b) EXP-090 corrected (the physics reading): {r4}{dep4}  {[(t, round(v[1], 4), round(v[2], 4)) for t, v in rb['primary'][1].items()]}"
      f"   [secondary-sigma: {rb['secondary'][0]}; robustness: {rb['robust'][0]}]")
out["R4"] = dict(a=ra, a_tails={t: list(v) for t, v in pa.items()}, b=r4 + dep4, b_rows={nm: [v[0], {t: list(x) for t, x in v[1].items()}] for nm, v in rb.items()})
# (R5) pair 2 -> 3, descriptive
tL = {k: t0c[k] + XL[k] for k in KS3}; Cs = {k: comp[k]["C"] for k in KS3}
p23 = {nm: v[3] - v[2] for nm, v in (("t0+L", tL), ("C", Cs), ("Y_A", Y))}
print(f"(R5) pair 2 -> 3 [descriptive]: {{{', '.join(f'{k}: {v:+.4f}' for k, v in p23.items())}}}")
out["R5"] = p23
# (R6) seals
E6 = 0.5 * R3["t0_W1"] + G6["X_Lam"]; E12 = 0.5 * R3["t0_W2"] + G12["X_Lam"]; E12c = 0.5 * (R3["t0_W2"] + d12) + G12["X_Lam"]
Rcur, Rcor = -(E6 - E12) * norm(3), -(E6 - E12c) * norm(3)
inb = lambda v, lo, hi: lo <= v <= hi
S1 = dict(R=Rcur, in68=inb(Rcur, -2.0, -1.1), inouter=inb(Rcur, -2.5, -0.7), E6=E6, E6_pass=abs(E6 - 1.892) <= 0.008, E12=E12, E12_pass=abs(E12 - 1.78) <= 0.03)
S2 = dict(R=Rcur, in68=inb(Rcur, -0.30, 0.15), inouter=inb(Rcur, -0.60, 0.40), E6_pass=abs(E6 - 1.895) <= 0.006, E12_pass=abs(E12 - 1.890) <= 0.02,
          XL12=G12["X_Lam"], XL12_pass=abs(G12["X_Lam"] - 244.958) <= 0.02)
S3 = dict(R=Rcor, pass_=inb(Rcor, 0.25, 0.42), fable_fail_rule_fires=not inb(Rcor, 0.15, 0.50), dt0_pass=abs(d12 - 0.0575) <= 0.03)
print(f"(R6) S-1 (current code): R(t0+L)(3) {Rcur:+.4f}; in 68% [-2.0,-1.1] {S1['in68']}, in outer [-2.5,-0.7] {S1['inouter']} [main grade DESCRIPTIVE, N2]; "
      f"E(W6P12) {E6:.4f} vs 1.892+-0.008 {'PASS' if S1['E6_pass'] else 'FAIL'}; E(W12P12) {E12:.4f} vs 1.78+-0.03 {'PASS' if S1['E12_pass'] else 'FAIL'}")
print(f"(R6) S-2 (current code): in 68% [-0.30,+0.15] {S2['in68']}, in outer [-0.60,+0.40] {S2['inouter']} [main grade DESCRIPTIVE, N2]; "
      f"E(W6P12) vs 1.895+-0.006 {'PASS' if S2['E6_pass'] else 'FAIL'}; E(W12P12) vs 1.890+-0.02 {'PASS' if S2['E12_pass'] else 'FAIL'}; "
      f"X_Lam(W12P12) {G12['X_Lam']:.4f} vs 244.958+-0.02 {'PASS' if S2['XL12_pass'] else 'FAIL'}")
print(f"(R6) S-3 (corrected t0): R(t0+L)(3) {Rcor:+.4f} in [0.25, 0.42] -> {'PASS' if S3['pass_'] else 'FAIL'}; Fable's fail rule (outside [0.15, 0.50]) "
      f"{'FIRES' if S3['fable_fail_rule_fires'] else 'does not fire'}; sub-seal dt0 {d12:+.6f} vs 0.0575+-0.03 {'PASS' if S3['dt0_pass'] else 'FAIL'}")
out["R6"] = dict(S1=S1, S2=S2, S3=S3)
head = (f"EXP-090 k = 3 READING ({mode}{'; PLANTED INPUTS, NOT A RESULT' if mode == 'DRY' else ''}): (R4)(b) {r4}{dep4}; (R2) row 2 {b}{dep}{krange}; "
        f"S-3 {'PASS' if S3['pass_'] else 'FAIL'}; {s_lab}; fix carried, partially verified (EXP-096); A-vs-bulk open; EXP-086 tension stands; "
        f"exposure of S(W6P12) recorded (65e0b6a); S-1/S-2 PASS band not fixed before exposure; graded descriptive (Bridge ruling 2026-11-28); "
        f"controls {'PASS' if not FAIL else FAIL}")
print("\n" + head); out["headline"] = head; out["failed"] = FAIL
json.dump(out, open(os.path.join(D, f"exp090_k3{'_DRY' if mode == 'DRY' else ''}.json"), "w"), indent=1, default=lambda v: float(v) if np.isscalar(v) else str(v))
sys.exit(1 if FAIL else 0)
