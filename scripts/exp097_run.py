"""EXP-097 (registration notes/EXP-096_097_registration.md): the EXP-094 n = 2 wall test one wall further, strips (2, 4), P = 8.
DESCRIPTIVE (no sealed band): f2(6 -> 8) and the span f2(4 -> 8), each with its own INCONCLUSIVE rule (drop < 0.2 x G2b at the start).
Code: EXP-094's phase 1 and dRs VERBATIM (imported from exp094_run's definitions by copy, below). [model: Opus 5.5]
Controls BEFORE any P = 8 value of W2P8 (stop if any fails):
  (i)   phase1(W, 4) and phase1(W, 6) reproduce the stored Q_W{W}P4b4 / Q_W{W}P6b6 QA (n = 2, 3): rel <= TOL;
        saddle(2) sum at W{W}P6 reproduces exp094_sigma2_W{W}P6 (rel <= TOL);
  (ii)  phase1(4, 8) reproduces the stored Q_W4P8b8 QA (n = 2, 3) (EXP-084, never used at n = 2 in a wall test): rel <= TOL;
  (iii) the P = 4 and P = 6 rows (R2, dRA, dRB, rho2A, G2b) reproduce exp094_result.json: rel <= TOL;
  (iv)  two-path |QA - QB| / |QA| <= 1e-9 at W2P8 and W4P8 (n = 2) (EXP-084's own gate);
  (v)   stale-file guard: exp097/Q_W2P8b8.json and exp097/Q_W4P8b8.json absent before the run;
  (vi)  must-fail plant: dRA(8) recomputed with sigma2(W2P8) x 1.01 must move by > 1e-3 relative.
TOL = 1e-10 relative (cross-platform: the M1 Air vs the M4 Mac agreed to 5.7e-11 on the EXP-093 identity); bitwise is reported."""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE); D = os.path.join(HERE, "exp081d_results")
import exp083_honest as H
TOL = 1e-10
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); R94 = json.load(open(os.path.join(D, "exp094_result.json")))
W89 = json.load(open(os.path.join(D, "exp089_wall.json"))); P93 = json.load(open(os.path.join(D, "exp093_p1.json")))
ends = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]; c_hi = list(ends.values())[0]
OUT = os.path.join(D, "exp097"); os.makedirs(OUT, exist_ok=True); FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:74s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def rel(x, y): return abs(x - y) / max(abs(y), 1e-300)
def logdetB_rev(geo, G):                                                    # verbatim from exp084_run.py (via exp094_run.py)
    Ny = geo.Ny; tot = 0.0
    for k in range(Ny):
        B = sum(G[p] * G[(k - p) % Ny] for p in reversed(range(Ny))) * (2.0 / Ny); s, ld = np.linalg.slogdet(B.T); tot += ld
    return tot
def phase1(W, P):                                                           # verbatim from exp094_run.py
    geo = H.Geom(W, P, Wbox=P, c=2); t = time.time(); rec = dict(W=W, P=P)
    ld1A = geo.logdetB(geo.Gn(1)); ld1B = logdetB_rev(geo, geo.Gn(1)); sig2 = None
    for n in (2, 3):
        sigA, itA = geo.saddle(n, tol=1e-13); sigB, itB = geo.saddle(n, tol=1e-11)
        qA = geo.logdetB(geo.Gn(n, sigA)) - n * ld1A; qB = logdetB_rev(geo, geo.Gn(n, sigB)) - n * ld1B
        qa = geo.logdetB(geo.Gn(n)) - n * ld1A
        rec[str(n)] = dict(QA=qA, QB=qB, sigQ=abs(qA - qB), itA=itA, itB=itB, armA=qa)
        if n == 2: sig2 = np.array(sigA)
    rec["sec"] = time.time() - t; return rec, sig2
cA = {(W, P): np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json")))["cA"]) for W in (2, 4) for P in (4, 6, 8)}
for P in (8,):
    for W in (2, 4): check(f"G_W{W}P{P}: failed empty", not json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json"))).get("failed"))
def dRs(P, sg, nm):                                                         # exp086b dR verbatim (n = 2 prefactor 1), as in exp094_run.py
    Ny = 4 * P; A = Ny * (np.dot(cA[(2, P)], sg[2]) - np.dot(cA[(4, P)], sg[4])) * nm; B = Ny * (c_hi * sg[2].sum() - c_hi * sg[4].sum()) * nm; return A, B
# ---------------- (v) stale guard, (i) P = 4 / 6 KAs, (ii) W4P8 KA, (iii) rows
for W in (2, 4): check(f"(v) exp097/Q_W{W}P8b8.json absent before the run", not os.path.exists(os.path.join(OUT, f"Q_W{W}P8b8.json")))
if FAIL: print("STOP: stale files"); sys.exit(1)
Q, SIG = {}, {}
for P in (4, 6):
    for W in (2, 4):
        rec, s2 = phase1(W, P); ref = json.load(open(os.path.join(D, "exp084", f"Q_W{W}P{P}b{P}.json")))
        for n in ("2", "3"):
            check(f"(i) phase1 W{W}P{P} QA n={n} vs stored", rel(rec[n]["QA"], ref[n]["QA"]) <= TOL, f"rel {rel(rec[n]['QA'], ref[n]['QA']):.1e} bitwise {rec[n]['QA'] == ref[n]['QA']}")
        Q[(W, P)], SIG[(W, P)] = rec["2"]["QA"], s2
        if P == 6:
            sref = np.array(json.load(open(os.path.join(D, f"exp094_sigma2_W{W}P6.json")))["sigma"])
            check(f"(i) saddle(2) W{W}P6 vs exp094_sigma2 (max rel)", float(np.max(np.abs(s2 - sref)) / np.max(np.abs(sref))) <= TOL, f"{np.max(np.abs(s2 - sref)):.1e}")
sig4 = {W: np.array(json.load(open(os.path.join(D, "exp084c", f"c84_W{W}P4_n2.json")))["sigma"]) for W in (2, 4)}   # as EXP-094 (its P = 4 sigma)
nm = {4: 1.0 / (4 * 4) / (1 / 2 - 1 / 4) / JD["1"]["kappa"], 6: W89["r6"]["norm"], 8: P93["r8"]["norm"]}
Q4 = {W: json.load(open(os.path.join(D, "exp084", f"Q_W{W}P4b4.json")))["2"]["QA"] for W in (2, 4)}                # stored, as EXP-094
row = {}
for P, sg, QQ in ((4, sig4, Q4), (6, {W: SIG[(W, 6)] for W in (2, 4)}, {W: Q[(W, 6)] for W in (2, 4)})):
    R2 = -0.5 * (QQ[2] - QQ[4]) * nm[P]; A, B = dRs(P, sg, nm[P]); row[P] = dict(R2=R2, dRA=A, dRB=B, rho2A=R2 + A, G2b=A - B)
for i, P in enumerate((4, 6)):
    for key in ("R2", "dRA", "dRB", "rho2A", "G2b"):
        check(f"(iii) P={P} {key} vs exp094_result.json", rel(row[P][key], R94[key][i]) <= TOL, f"rel {rel(row[P][key], R94[key][i]):.1e}")
recs = {}
rec4, s48 = phase1(4, 8); ref = json.load(open(os.path.join(D, "exp084", "Q_W4P8b8.json")))
for n in ("2", "3"):
    check(f"(ii) phase1 W4P8 QA n={n} vs stored Q_W4P8b8 (EXP-084)", rel(rec4[n]["QA"], ref[n]["QA"]) <= TOL, f"rel {rel(rec4[n]['QA'], ref[n]['QA']):.1e} bitwise {rec4[n]['QA'] == ref[n]['QA']}")
if FAIL: print(f"\nSTOP: controls failed {FAIL} -> W2P8 not computed"); sys.exit(1)
# ---------------- P = 8: W2P8 (fresh) + W4P8
rec2, s28 = phase1(2, 8); recs = {2: rec2, 4: rec4}; sig8 = {2: s28, 4: s48}
for W in (2, 4):
    json.dump(recs[W], open(os.path.join(OUT, f"Q_W{W}P8b8.json"), "w"), indent=1)
    json.dump(dict(W=W, P=8, sigma=list(sig8[W])), open(os.path.join(OUT, f"sigma2_W{W}P8.json"), "w"))
    r_ = recs[W]["2"]["sigQ"] / abs(recs[W]["2"]["QA"])
    check(f"(iv) two-path |QA - QB| / |QA| <= 1e-9 at W{W}P8 (n = 2)", r_ <= 1e-9, f"{r_:.1e} ({recs[W]['sec']:.1f} s)")
R2 = -0.5 * (rec2["2"]["QA"] - rec4["2"]["QA"]) * nm[8]; A8, B8 = dRs(8, sig8, nm[8]); row[8] = dict(R2=R2, dRA=A8, dRB=B8, rho2A=R2 + A8, G2b=A8 - B8)
Ap, _ = dRs(8, {2: s28 * 1.01, 4: s48}, nm[8]); check("(vi) plant: dRA(8) moves > 1e-3 rel when sigma2(W2P8) x 1.01", rel(Ap, A8) > 1e-3, f"rel {rel(Ap, A8):.1e}")
def fstep(a_, b_):
    drop = row[a_]["G2b"] - row[b_]["G2b"]; f = -(row[b_]["rho2A"] - row[a_]["rho2A"]) / drop; inc = drop < 0.2 * row[a_]["G2b"]
    return dict(drop=drop, thr=0.2 * row[a_]["G2b"], f=f, inconclusive=inc)
s68, s48s = fstep(6, 8), fstep(4, 8)
n1 = {P: (W89[f"r{P}"] if P in (4, 6) else P93["r8"]) for P in (4, 6, 8)}
f1_48 = -(n1[8]["rhoA"] - n1[4]["rhoA"]) / (n1[4]["Gb"] - n1[8]["Gb"])
for P in (4, 6, 8): print(f"P = {P}: R2 {row[P]['R2']:+.6f}  dR2^A {row[P]['dRA']:+.6f}  dR2^bulk {row[P]['dRB']:+.6f}  rho2A {row[P]['rho2A']:+.6f}  G2b {row[P]['G2b']:+.6f}")
for nmx, s in (("6 -> 8", s68), ("4 -> 8", s48s)):
    print(f"f2({nmx}) = {s['f']:+.4f}; G2b drop {s['drop']:+.6f} vs 0.2 G2b(start) {s['thr']:.6f} -> {'INCONCLUSIVE' if s['inconclusive'] else 'conclusive'}")
print(f"DESCRIPTIVE, n = 1 beside it: f(4->6) {W89['f']:+.4f}, f(6->8) {P93['f']:+.4f}, f(4->8) {f1_48:+.4f};  n = 2 f2(4->6) {R94['f2']:+.4f} (INCONCLUSIVE)")
if FAIL: print(f"controls FAILED after P = 8: {FAIL}")
json.dump(dict(rows=row, step68=s68, span48=s48s, n1_f46=W89["f"], n1_f68=P93["f"], n1_f48=f1_48, failed=FAIL, sec={W: recs[W]["sec"] for W in (2, 4)}),
          open(os.path.join(D, "exp097_result.json"), "w"), indent=1, default=float)
sys.exit(1 if FAIL else 0)
