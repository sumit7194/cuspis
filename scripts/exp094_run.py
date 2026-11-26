"""EXP-094 (P-2; registered f874dac + amendment 1 e8a1c06): n = 2 wall test, strips (2, 4), walls P = 4 -> 6. Honest exact n = 2.
Order: controls (i), (iii), (iv) -> STOP if any fails; then Q files at W2P6, W4P6 by EXP-084 phase-1 code VERBATIM (+ control (ii)); then grading.
[model: Opus 5.5]"""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE); D = os.path.join(HERE, "exp081d_results")
import exp083_honest as H
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); E86b = json.load(open(os.path.join(D, "exp086b_result.json")))
W89 = json.load(open(os.path.join(D, "exp089_wall.json"))); ends = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]; c_hi = list(ends.values())[0]
FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:70s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def logdetB_rev(geo, G):                                                    # verbatim from exp084_run.py
    Ny = geo.Ny; tot = 0.0
    for k in range(Ny):
        B = sum(G[p] * G[(k - p) % Ny] for p in reversed(range(Ny))) * (2.0 / Ny); s, ld = np.linalg.slogdet(B.T); tot += ld
    return tot
def phase1(W, P):                                                           # verbatim body of exp084_run.py phase 1 (one geometry)
    geo = H.Geom(W, P, Wbox=P, c=2); t = time.time(); rec = dict(W=W, P=P)
    ld1A = geo.logdetB(geo.Gn(1)); ld1B = logdetB_rev(geo, geo.Gn(1)); sig2 = None
    for n in (2, 3):
        sigA, itA = geo.saddle(n, tol=1e-13); sigB, itB = geo.saddle(n, tol=1e-11)
        qA = geo.logdetB(geo.Gn(n, sigA)) - n * ld1A; qB = logdetB_rev(geo, geo.Gn(n, sigB)) - n * ld1B
        qa = geo.logdetB(geo.Gn(n)) - n * ld1A                      # arm a (sigma = 0), reported only
        rec[str(n)] = dict(QA=qA, QB=qB, sigQ=abs(qA - qB), itA=itA, itB=itB, armA=qa)
        if n == 2: sig2 = np.array(sigA)
    rec["sec"] = time.time() - t; return rec, sig2
# ---------------- controls BEFORE any P = 6 number
for W in (2, 4):
    rec, s2 = phase1(W, 4); ref = json.load(open(os.path.join(D, "exp084", f"Q_W{W}P4b4.json")))
    check(f"(i) phase-1 wrapper reproduces stored Q_W{W}P4b4 QA (n = 2, 3) bitwise", rec["2"]["QA"] == ref["2"]["QA"] and rec["3"]["QA"] == ref["3"]["QA"], f"{rec['2']['QA']!r}")
    if W == 2:
        s84 = np.array(json.load(open(os.path.join(D, "exp084c", "c84_W2P4_n2.json")))["sigma"])
        check("(iv) saddle(2) sum at W2P4 == stored 084c sigma_2 sum (1e-6)", abs(s2.sum() - s84.sum()) <= 1e-6, f"{s2.sum():+.9f} vs {s84.sum():+.9f}")
def norm1(): return 1.0 / (4 * 4) / (1 / 2 - 1 / 4) / JD["1"]["kappa"]
Q4 = {W: json.load(open(os.path.join(D, "exp084", f"Q_W{W}P4b4.json")))["2"]["QA"] for W in (2, 4)}
R2_4 = -0.5 * (Q4[2] - Q4[4]) * norm1(); R84 = json.load(open(os.path.join(D, "exp084", "result.json")))["Rn"]["2"]["1"]
check("(iii) R2(P = 4) = 0.6826 (4 dp) and == 084 R2(1) within 1.5e-5", round(R2_4, 4) == 0.6826 and abs(R2_4 - R84) <= 1.5e-5, f"{R2_4:.6f} vs 084 {R84:.6f}")
sig4 = {W: np.array(json.load(open(os.path.join(D, "exp084c", f"c84_W{W}P4_n2.json")))["sigma"]) for W in (2, 4)}
cA = {(W, P): np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json")))["cA"]) for W in (2, 4) for P in (4, 6)}
def dRs(P, sg, nm):                                                         # exp086b dR verbatim (n = 2 prefactor 1)
    Ny = 4 * P; A = Ny * (np.dot(cA[(2, P)], sg[2]) - np.dot(cA[(4, P)], sg[4])) * nm; B = Ny * (c_hi * sg[2].sum() - c_hi * sg[4].sum()) * nm; return A, B
A4, B4 = dRs(4, sig4, norm1())
check("(iii) dR2^A(4), dR2^bulk(4) == exp086b_result.json bitwise", A4 == E86b["hi c(384)"]["A"]["1"] and B4 == E86b["hi c(384)"]["bulk"]["1"], f"{A4!r} / {B4!r}")
if FAIL: print(f"\nSTOP: controls failed {FAIL} -> nothing at P = 6 computed"); sys.exit(1)
# ---------------- P = 6: Q files (EXP-084 format) + sigma_2
sig6, Q6 = {}, {}
for W in (2, 4):
    fq = os.path.join(D, "exp084", f"Q_W{W}P6b6.json")
    if os.path.exists(fq): print(f"STOP: {fq} exists before this run"); sys.exit(1)
    rec, s2 = phase1(W, 6); json.dump(rec, open(fq, "w"), indent=1); json.dump(dict(W=W, P=6, sigma=list(s2)), open(os.path.join(D, f"exp094_sigma2_W{W}P6.json"), "w"))
    rel = rec["2"]["sigQ"] / abs(rec["2"]["QA"])
    check(f"(ii) two-path |QA - QB| / |QA| <= 1e-9 at W{W}P6 (n = 2)", rel <= 1e-9, f"{rel:.1e}  ({rec['sec']:.1f} s)")
    sig6[W], Q6[W] = s2, rec["2"]["QA"]
nm6 = W89["r6"]["norm"]; R2_6 = -0.5 * (Q6[2] - Q6[4]) * nm6; A6, B6 = dRs(6, sig6, nm6)
r4, r6 = R2_4 + A4, R2_6 + A6; G4, G6 = A4 - B4, A6 - B6; drop = G4 - G6; f2 = -(r6 - r4) / drop
print(f"\nP = 4: R2 {R2_4:+.5f}  dR2^A {A4:+.5f}  dR2^bulk {B4:+.5f}  rho2A {r4:+.5f}  G2b {G4:+.5f}")
print(f"P = 6: R2 {R2_6:+.5f}  dR2^A {A6:+.5f}  dR2^bulk {B6:+.5f}  rho2A {r6:+.5f}  G2b {G6:+.5f}   (norm6 {nm6:.6f})")
print(f"G2b drop {drop:+.5f} (INCONCLUSIVE if < 0.2*G2b(4) = {0.2*G4:.5f});  f2 = {f2:+.4f}")
if FAIL: lab = f"controls FAILED {FAIL}"
elif drop < 0.2 * G4: lab = "INCONCLUSIVE (G2b drop < 0.2 G2b(4))"
else: lab = f"f2 {'PASS' if -0.10 <= f2 <= 0.20 else 'FAIL'} (sealed 0.05 +- 0.15, [-0.10, 0.20]); +-2 sigma [-0.25, 0.35]: {'inside' if -0.25 <= f2 <= 0.35 else 'outside'}"
print(f"EXP-094 (P-2) READING: {lab};  descriptive rho2bulk(4) {R2_4 + B4:+.5f} -> (6) {R2_6 + B6:+.5f}")
json.dump(dict(R2=[R2_4, R2_6], dRA=[A4, A6], dRB=[B4, B6], rho2A=[r4, r6], G2b=[G4, G6], drop=drop, f2=f2, reading=lab, failed=FAIL),
          open(os.path.join(D, "exp094_result.json"), "w"), indent=1, default=float)
sys.exit(1 if FAIL else 0)
