"""EXP-084 (registered, notes/EXP-084_registration.md). Phases in registered order:
0 plants on the reading function (exit 1 if any label is wrong) and the KA known answer; 1 Q values (paths A and B) per geometry;
2 the sigma table, written BEFORE any R or ratio; 3 R_n(k), the ratios and the reading.
Usage: exp084_run.py [kmax]   (kmax limits the geometries; the reading runs only when all four k are present) [model: Opus 5.5]"""
import sys, json, os, time, numpy as np
from scipy.optimize import brentq
import exp083_honest as H
OUT = "exp081d_results/exp084"; os.makedirs(OUT, exist_ok=True)
KS = [1, 1.5, 2, 2.5]; KAP = {1: 0.017660, 1.5: 0.018206, 2: 0.017743, 2.5: 0.017468}
RCONT = {1: 2.255224, 1.5: 4.233446, 2: 6.441981, 2.5: 8.218749}; GCONT = 4.02
rsh = lambda p: np.log(2.5 / 1.5) / np.log(2) if abs(p) < 1e-12 else (2.5**p - 1.5**p) / (2**p - 1)
EDGES = dict(conv=rsh(-0.71), logl=rsh(-0.35), logh=rsh(0.35), pow=rsh(0.70))
def band(r):
    if r <= EDGES["conv"]: return "converging"
    if EDGES["logl"] <= r <= EDGES["logh"]: return "log-like"
    if r >= EDGES["pow"]: return "power-divergent"
    return None
def ratio(R, sR):
    d1, d2 = R[2] - R[1], R[2.5] - R[1.5]; r = d2 / d1
    sr = abs(r) * np.hypot(np.hypot(sR[2.5], sR[1.5]) / abs(d2), np.hypot(sR[2], sR[1]) / abs(d1)); return r, sr
def read1(R, sR):
    r, sr = ratio(R, sR); lo, mid, hi = band(r - 2 * sr), band(r), band(r + 2 * sr)
    return (mid if lo == mid == hi and mid else "INCONCLUSIVE"), r, sr
def slope(R): k = np.array(KS); v = np.array([R[x] for x in KS]); return np.polyfit(k, v, 1)[0]
def reading(R2, s2, R3, s3):
    (b2, r2, sr2), (b3, r3, sr3) = read1(R2, s2), read1(R3, s3); thr = max(0.15, 3 * np.hypot(sr2, sr3)); g2, g3 = slope(R2), slope(R3)
    if b2 in ("converging", "log-like") and b3 in ("converging", "log-like"): lab = "(i) continuation"
    elif b2 == b3 == "power-divergent":
        if abs(r2 - r3) >= thr: lab = "(ii-b) n-dependent"
        elif g2 >= 0.5 * GCONT and g3 >= 0.5 * GCONT: lab = "(ii-a) sigma-sector, n-independent"
        else: lab = "mixed (both loci contribute)"
    else: lab = "INCONCLUSIVE"
    return lab, dict(b2=b2, r2=r2, sr2=sr2, b3=b3, r3=r3, sr3=sr3, thr=thr, g2=g2, g3=g3)
# ---------------- phase 0: plants and known answer ----------------
z = {k: 1e-9 for k in KS}; f = lambda fn: {k: 1.0 + fn(k) for k in KS}
plants = [("const + 4k", f(lambda k: 4 * k), f(lambda k: 4 * k), "(ii-a) sigma-sector, n-independent"),
          ("const + 0.5 ln k", f(lambda k: 0.5 * np.log(k)), f(lambda k: 0.5 * np.log(k)), "(i) continuation"),
          ("const + 1/k", f(lambda k: 1 / k), f(lambda k: 1 / k), "(i) continuation"),
          ("4k vs 4k^1.5", f(lambda k: 4 * k), f(lambda k: 4 * k**1.5), "(ii-b) n-dependent"),
          ("0.5k", f(lambda k: 0.5 * k), f(lambda k: 0.5 * k), "mixed (both loci contribute)"),
          ("k^0.5 (gap)", f(lambda k: k**0.5), f(lambda k: k**0.5), "INCONCLUSIVE")]
bad = 0
for nm, a, b, want in plants:
    got = reading(a, z, b, z)[0]; ok = got == want; bad += not ok
    print(f"plant {nm:16s} -> {got:40s} expected {want:40s} {'PASS' if ok else 'FAIL'}", flush=True)
from mpmath import mpf
ref = json.load(open("exp083_r2/W2P2b.json"))["Q"]; g = H.Geom(2, 2, Wbox=4, c=2)
for n in (2, 3):
    d = abs(g.Q(n, saddle=True) - float(mpf(ref[str(n)]))); bad += not d < 1e-11
    print(f"KA W2P2 arm b n={n}: |float64 - Arb| {d:.1e} {'PASS' if d < 1e-11 else 'FAIL'}", flush=True)
if bad: print("PHASE 0 FAIL -> exit before reading data"); sys.exit(1)
# ---------------- phase 1: Q values, paths A and B ----------------
def logdetB_rev(geo, G):
    Ny = geo.Ny; tot = 0.0
    for k in range(Ny):
        B = sum(G[p] * G[(k - p) % Ny] for p in reversed(range(Ny))) * (2.0 / Ny); s, ld = np.linalg.slogdet(B.T); tot += ld
    return tot
kmax = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5
for k in [x for x in KS if x <= kmax]:
    P = int(4 * k)
    for W in (int(2 * k), int(4 * k)):
        fn = f"{OUT}/Q_W{W}P{P}b{P}.json"
        if os.path.exists(fn): continue
        geo = H.Geom(W, P, Wbox=P, c=2); t = time.time(); rec = dict(W=W, P=P)
        ld1A = geo.logdetB(geo.Gn(1)); ld1B = logdetB_rev(geo, geo.Gn(1))
        for n in (2, 3):
            sigA, itA = geo.saddle(n, tol=1e-13); sigB, itB = geo.saddle(n, tol=1e-11)
            qA = geo.logdetB(geo.Gn(n, sigA)) - n * ld1A; qB = logdetB_rev(geo, geo.Gn(n, sigB)) - n * ld1B
            qa = geo.logdetB(geo.Gn(n)) - n * ld1A                      # arm a (sigma = 0), reported only
            rec[str(n)] = dict(QA=qA, QB=qB, sigQ=abs(qA - qB), itA=itA, itB=itB, armA=qa)
        rec["sec"] = time.time() - t; json.dump(rec, open(fn, "w"), indent=1)
        print(f"Q W{W}P{P}b{P}: done ({rec['sec']:.1f}s)", flush=True)      # values not printed here
# ---------------- phase 2: sigma table (before any ratio) ----------------
have = {k: all(os.path.exists(f"{OUT}/Q_W{W}P{int(4*k)}b{int(4*k)}.json") for W in (int(2*k), int(4*k))) for k in KS}
if not all(have.values()): print(f"geometries present: {have}; reading deferred until all four k exist"); sys.exit(0)
Q = {k: {W: json.load(open(f"{OUT}/Q_W{W}P{int(4*k)}b{int(4*k)}.json")) for W in (int(2*k), int(4*k))} for k in KS}
norm = lambda k: 1.0 / (4 * int(4 * k)) / (1 / int(2 * k) - 1 / int(4 * k)) / KAP[k]
sig = {n: {k: 0.5 / (n - 1) * np.hypot(Q[k][int(2*k)][str(n)]["sigQ"], Q[k][int(4*k)][str(n)]["sigQ"]) * norm(k) for k in KS} for n in (2, 3)}
json.dump(sig, open(f"{OUT}/sigma_table.json", "w"), indent=1); print("sigma table (R units):", {n: {k: f"{v:.1e}" for k, v in sig[n].items()} for n in sig}, flush=True)
# ---------------- phase 3: R_n, ratios, reading ----------------
Rn = {n: {k: -(0.5 / (n - 1)) * (Q[k][int(2*k)][str(n)]["QA"] - Q[k][int(4*k)][str(n)]["QA"]) * norm(k) for k in KS} for n in (2, 3)}
Ra = {n: {k: -(0.5 / (n - 1)) * (Q[k][int(2*k)][str(n)]["armA"] - Q[k][int(4*k)][str(n)]["armA"]) * norm(k) for k in KS} for n in (2, 3)}
lab, det = reading(Rn[2], sig[2], Rn[3], sig[3]); rc, _ = ratio(RCONT, {k: 0.0 for k in KS})
for n in (2, 3): print(f"R_{n}(k) arm b: {[round(Rn[n][k], 6) for k in KS]}   arm a (reported only): {[round(Ra[n][k], 6) for k in KS]}")
print(f"continued reference: R {[RCONT[k] for k in KS]}, r {rc:.4f}, band {band(rc)}, slope {slope(RCONT):.3f}")
print(f"READING: {lab}   details {det}")
json.dump(dict(Rn=Rn, Ra=Ra, sigma=sig, reading=lab, details=det, ref=dict(r=rc, band=band(rc))), open(f"{OUT}/result.json", "w"), indent=1, default=str)
