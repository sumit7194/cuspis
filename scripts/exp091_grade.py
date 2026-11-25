"""EXP-091 (registered 33ae101 + amendment 1, notes/EXP-091_registration.md): grade Fable's S-c seals (+ S-a fail clauses), seal c615773. [model: Opus 5.5]
Controls C1-C5 first (exit 1 -> no grading). Map code verbatim from exp085c_run.py READ. Only compute: kappa(3) via exp081b_run.pair."""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp081b_run as Rn
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); FAIL = []
E5 = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]; ends = list(E5.values()); c_hi, c_lo = ends[0], ends[1]
def check(nm, ok, det=""):
    print(f"{nm:72s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def Gf(W, P): return json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json")))
def interior(g):                                                                 # verbatim from exp085c_run READ (c_A/c map)
    cA = np.array(g["cA"]); Lt = g["Lt"]; x = np.arange(len(cA)) // Lt; t = np.arange(len(cA)) % Lt; Lx = g["Lx"]
    xm = Lx // 2; inter = cA[(np.abs(x - xm) <= 1) & (np.abs(t - Lt // 2) <= 1)]; return inter.mean() / c_hi
def kappa(P, W1, W2): return Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=W1, W2=W2, Wbox=P)
def normk(P, W1, W2, kap): return 1.0 / (4 * P * (1 / W1 - 1 / W2) * kap)
def raw(g1, g2, c):                                                              # y_A, y_bulk (no norm)
    return -(g1["X_cA"] - g2["X_cA"]), -(c / 2) * (g1["Sigma3D"] - g2["Sigma3D"])
# ---- C1a / C1b on stored k <= 2.5
KS = [1, 1.5, 2, 2.5]; MAP = {4: 0.5672, 6: 0.6841, 8: 0.7509, 10: 0.7949}; BMB = [-2.49199, -2.97652, -3.45065, -3.75667]
r = {P: interior(Gf(P, P)) for P in MAP}
check("C1a interior map P = 4..10 reproduces 085c READ (1e-4)", all(abs(r[P] - v) <= 1e-4 for P, v in MAP.items()), str({P: round(v, 5) for P, v in r.items()}))
bmb = []
for k in KS:
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); yA, yb = raw(Gf(W1, P), Gf(W2, P), c_hi)
    nk = 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]; bmb.append((yA - yb) * nk)
check("C1b box-minus-bulk (hi) k <= 2.5 reproduces stored values (1e-5)", all(abs(a - b) <= 1e-5 for a, b in zip(bmb, BMB)), str([round(v, 5) for v in bmb]))
k25 = kappa(10, 5, 10)
check("C2 pair() at P = 10 (5, 10) reproduces stored kappa(2.5) (1e-12 rel)", abs(k25 - JD["2.5"]["kappa"]) <= 1e-12 * JD["2.5"]["kappa"], f"{k25!r}")
g6, g12 = Gf(6, 12), Gf(12, 12)
_, yb3 = raw(g6, g12, c_hi)
exp3 = 0.5 * 48 * 0.11411 * 0.379362; tol3 = 24 * (0.379362 * 5e-6 + 0.11411 * 5e-7)    # amendment 1: Fable's typed inputs, rounding tolerance
check("C3' y_bulk(3) (hi) == 1/2*48*0.11411*0.379362 within typed-input rounding", abs(yb3 - exp3) <= tol3, f"{yb3:.7f} vs {exp3:.7f}, |d| {abs(yb3-exp3):.2e} <= {tol3:.2e}")
check("C4 P = 12 G files: no failed entries", not g6.get("failed") and not g12.get("failed"), f"{g6.get('failed')} / {g12.get('failed')}")
r12a, r12b = interior(g12), interior(g6)
check("C5 interior ratio W12P12 == W6P12 (1e-4)", abs(r12a - r12b) <= 1e-4, "")
if FAIL: print(f"\nSTOP: controls failed {FAIL} -> no grading"); sys.exit(1)
print("\nControls PASS -> grading\n")
# ---- grading
kap3 = kappa(12, 6, 12); n3 = normk(12, 6, 12, kap3)
yA3, _ = raw(g6, g12, c_hi); gb_hi = yb3 - yA3; _, yb3lo = raw(g6, g12, c_lo); gb_lo = yb3lo - yA3
dbb_hi, dbb_lo = -gb_hi * n3, -gb_lo * n3
w6, w12 = g6["X_cA"] / (0.5 * c_hi * g6["Sigma3D"]), g12["X_cA"] / (0.5 * c_hi * g12["Sigma3D"])
inwin = 14.02 <= n3 <= 14.42; G = {}
def grade(nm, val, lo, hi, extra=""):
    ok = lo <= val <= hi; G[nm] = dict(value=val, band=[lo, hi], PASS=ok); print(f"{nm:52s} {val:+.5f}  band [{lo:+.4f}, {hi:+.4f}] -> {'PASS' if ok else 'FAIL'}  {extra}", flush=True)
print(f"kappa(3) = {kap3!r}; norm(3) = {n3:.6f} -> {'inside' if inwin else 'OUTSIDE'} Fable's [14.02, 14.42]")
for nm, v in (("W12P12", r12a), ("W6P12", r12b)): grade(f"G1 interior c_A/c (hi) P = 12 [{nm}]", v, 0.820, 0.832, f"(within +-0.003 of 0.826: {abs(v - 0.826) <= 0.003}; (1-r)P = {(1 - v) * 12:.4f})")
if inwin: grade("G2 Delta_bb(3) hi", dbb_hi, -4.05, -3.73); grade("G2' raw g_b(3) hi (secondary)", gb_hi, 0.2675, 0.2795, "(2 sigma inferred)")
else: grade("G2' raw g_b(3) hi (graded in place of G2)", gb_hi, 0.2675, 0.2795, "(2 sigma inferred)"); print(f"   Delta_bb(3) hi = {dbb_hi:+.5f} (reported; norm outside window)")
grade("G3 y_A(3)", yA3, 0.7594, 0.7714, "(2 sigma inferred)")
grade("G4 sigdot-weighted c_A/c W6P12", w6, 0.8186, 0.8226, "(2 sigma inferred)"); grade("G4 sigdot-weighted c_A/c W12P12", w12, 0.8089, 0.8129, "(2 sigma inferred)")
print(f"G5 (reported, no fail rule): Delta_bb(3) lo {dbb_lo:+.5f} vs -5.24 +- 0.11 (+-2s: {abs(dbb_lo + 5.24) <= 0.22});  raw lo {gb_lo:.5f} vs 0.3689")
step = abs(dbb_hi - BMB[3]); inc = (1 - r12a) * 12 - (1 - r[10]) * 10; prev = (1 - r[10]) * 10 - (1 - r[8]) * 8
s1, s2 = step >= 0.306, inc >= prev
print(f"S-a clause 1: |Delta_bb(3) - Delta_bb(2.5)| = {step:.4f} (fails if >= 0.306) -> {'S-a FAILS' if s1 else 'not fired'}")
print(f"S-a clause 2: (1-r)P increment P10->12 = {inc:+.4f} vs P8->10 {prev:+.4f} (fails if >=) -> {'S-a FAILS' if s2 else 'not fired'}  [operationalisation mine]")
print(f"Descriptive: Delta_bb(hi) series k = 1..3: {[round(v, 4) for v in bmb] + [round(dbb_hi, 4)]}; raw g_b(hi) k = 2.5: {-BMB[3] / normk(10, 5, 10, k25):.5f}")
json.dump(dict(kappa3=kap3, norm3=n3, interior12=[r12a, r12b], yA3=yA3, ybulk3=yb3, gb_hi=gb_hi, gb_lo=gb_lo, dbb_hi=dbb_hi, dbb_lo=dbb_lo, w6=w6, w12=w12,
               grades=G, Sa_clause1_fired=s1, Sa_clause2_fired=s2, failed=FAIL), open(os.path.join(D, "exp091_grade.json"), "w"), indent=1, default=float)
