"""EXP-090 (registered 99484ff, notes/EXP-090_registration.md): re-reads with the corrected t0 (EXP-087). [model: Opus 5.5]
Modes:  CONTROLS  zero-correction controls only (K1, K3, K4 at Delta = 0, K6): prints NO corrected value
        K25       the k <= 2.5 part: (R1), (R2) row 1, (R3), (R5), S-4, with K1-K6 and the robustness rule (only on the Bridge's word)
Fit, slope, sigma and band code are verbatim from exp085c_run.py READ. Corrections are read from the EXP-087 JSONs; model values (sigma proxy)
are parsed from notes/EXP-087_tinybox/b_art_prod.txt. No typed numeric inputs except Fable's stored R(t0+L) row (K6 target, ADDENDUM ca63760 §D)."""
import sys, os, re, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); KS = [1, 1.5, 2, 2.5]; ks = np.array(KS, float); FAIL = []
mode = sys.argv[1] if len(sys.argv) > 1 else "CONTROLS"
def check(nm, ok, det=""):
    print(f"{nm:70s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def norm(k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]
G = {(W, int(4 * k)): json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{int(4*k)}.json"))) for k in KS for W in (int(2 * k), int(4 * k))}
def Rop(key, k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return -(G[(W1, P)][key] - G[(W2, P)][key]) * norm(k)
R0 = {k: JD[str(k)]["R_T0"] for k in KS}; sR0 = {k: JD[str(k)]["sigma"] for k in KS}; comp = {k: JD[str(k)]["components"] for k in KS}
Y = {k: Rop("X_cA", k) for k in KS}; XL = {k: Rop("X_Lam", k) for k in KS}
E5 = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]
def slope_and_sigma(out, sg):                                                             # verbatim from exp085c_run / exp085_run
    y = np.array([out[k] for k in KS]); g, b0 = np.polyfit(ks, y, 1); Sxx = np.sum((ks - ks.mean()) ** 2)
    ssr = np.sum((y - (g * ks + b0)) ** 2); s_fit = np.sqrt(ssr / (len(ks) - 2) / Sxx)
    w = (ks - ks.mean()) / Sxx; s_prop = np.sqrt(np.sum((w * np.array([sg[k] for k in KS])) ** 2))
    return float(g), float(np.hypot(s_fit, s_prop))
def sband(r, s):                                                                          # SIGNED bands verbatim (085c §D)
    lo, hi = r - 2 * s, r + 2 * s
    if hi < -0.1: return "overshoot"
    if lo >= -0.1 and hi <= 0.1: return "supported"
    if lo > 0.1 and hi < 0.5: return "partial"
    if lo >= 0.5: return "refuted as sole cause"
    return "INCONCLUSIVE (straddles a band edge)"

def corrected(dW1, dW2, sdW2):
    """dW1, dW2, sdW2: dict k -> Delta on narrow / wide strip and sigma of the wide one. Returns R^c, sigma^c, t0 component^c."""
    Rc = {k: R0[k] + 0.5 * (dW2[k] - dW1[k]) * norm(k) for k in KS}
    t0c = {k: comp[k]["t0"] + 0.5 * (dW2[k] - dW1[k]) * norm(k) for k in KS}
    sc = {k: float(np.hypot(sR0[k], 0.5 * sdW2[k] * norm(k))) for k in KS}
    return Rc, sc, t0c
def series(Rc, sc, t0c, graw, tag, out):
    gA, sA = slope_and_sigma({k: Rc[k] - Y[k] for k in KS}, sc); rA, srA = gA / graw, sA / graw
    out[tag] = dict(A=dict(g=gA, s=sA, rho=rA, srho=srA, band=sband(rA, srA)))
    for nm, cc in E5.items():
        Yb = {k: -(0.5 * cc * (G[(int(2*k), int(4*k))]["Sigma3D"] - G[(int(4*k), int(4*k))]["Sigma3D"])) * norm(k) for k in KS}
        gb, sb = slope_and_sigma({k: Rc[k] - Yb[k] for k in KS}, sc); out[tag][f"bulk {nm}"] = dict(g=gb, s=sb, rho=gb / graw, srho=sb / graw, band=sband(gb / graw, sb / graw))
    gM, sM = slope_and_sigma({k: Rc[k] + Y[k] for k in KS}, sc); out[tag]["mustfail"] = dict(rho=gM / graw, band=sband(gM / graw, sM / graw))
    tL = {k: t0c[k] + XL[k] for k in KS}; out[tag]["t0+L"] = tL
    out[tag]["RA1_RA2"] = max(abs((Rc[k] - Y[k]) - (t0c[k] + comp[k]["C"] + XL[k])) / max(1.0, abs(Rc[k] - Y[k])) for k in KS)
    return out[tag]
def pairs(v): return v[2] - v[1], v[2.5] - v[1.5]
def lslopes(v): return [(v[b] - v[a]) / (b - a) for a, b in zip(KS[:-1], KS[1:])]

zero = {k: 0.0 for k in KS}; graw0 = float(np.polyfit(ks, [R0[k] for k in KS], 1)[0]); out = {}
# ---------------- K1 / K4 / K6 at Delta = 0
z = series(*corrected(zero, zero, zero), graw0, "zero", out)
ref = json.load(open(os.path.join(D, "exp085c", "result.json")))
check("K1 g_raw (Delta = 0) == 4.019821717340081 bitwise", graw0 == 4.019821717340081, repr(graw0))
check("K1 rho_A, sigma_rhoA == 085c result.json bitwise", z["A"]["rho"] == ref["rhoA"] and z["A"]["srho"] == ref["sigma_rhoA"], f"{z['A']['rho']!r} / {ref['rhoA']!r}")
check("K1 R_corr^A == 085c RA1 bitwise", all(R0[k] - Y[k] == ref["RA1"][str(k) if str(k) in ref["RA1"] else repr(float(k))] for k in KS), "")
gt, _ = slope_and_sigma(z["t0+L"], zero); p1, p2 = pairs(z["t0+L"])
check("K1 ingredient slope(t0+L) -0.808, pairs -0.475/-1.039 (5e-4)", abs(gt + 0.808) <= 5e-4 and abs(p1 + 0.475) <= 5e-4 and abs(p2 + 1.039) <= 5e-4, f"{gt:+.4f} {p1:+.4f} {p2:+.4f}")
check("K4 two-route identity (Delta = 0) 1e-10", z["RA1_RA2"] <= 1e-10, f"{z['RA1_RA2']:.1e}")
FAB = [0.7615, 0.5381, 0.2865, -0.5005]                                                   # Fable ADDENDUM §D, stored row (K6 target)
check("K6 E/X_Lam definition reproduces Fable's stored R(t0+L) row (1e-4)", all(abs(z["t0+L"][k] - f) <= 1e-4 for k, f in zip(KS, FAB)), str([round(z["t0+L"][k], 5) for k in KS]))
# ---------------- K3 placement plant (synthetic Delta = +1)
Rn, _, _ = corrected({**zero, 2: 1.0}, zero, zero); Rw, _, _ = corrected(zero, {**zero, 2: 1.0}, zero)
check("K3 plant: +1 on narrow W1 = 4 moves R(2) by -norm(2)/2; on wide W2 = 8 by +norm(2)/2 (1e-12)",
      abs(Rn[2] - R0[2] + 0.5 * norm(2)) <= 1e-12 * norm(2) and abs(Rw[2] - R0[2] - 0.5 * norm(2)) <= 1e-12 * norm(2), "")
if mode == "CONTROLS":
    print(f"\nCONTROLS only (no corrected value computed): {'PASS' if not FAIL else FAIL}"); sys.exit(1 if FAIL else 0)

# ---------------- K25: corrections from files, K2 per source
ref8 = json.load(open(os.path.join(D, "exp087_referee_W8P8.json"))); f10 = json.load(open(os.path.join(D, "exp087_t0_W10P10.json")))
art = {(int(m[0]), int(m[1])): -float(m[2]) for m in re.findall(r"W(\d+) P(\d+) Wb\d+ Ny\d+ rad 1e-05: predicted delta_t0 \(code - true\) = ([-+0-9.]+)",
       open(os.path.join(HERE, "..", "notes", "EXP-087_tinybox", "b_art_prod.txt")).read())}
check("K2 W8P8 referee OFF == stored S_W2.t0 (k = 2) 1e-10 rel", abs(ref8["off_1e-5"] - JD["2"]["S_W2"]["t0"]) <= 1e-10 * abs(JD["2"]["S_W2"]["t0"]), "")
check("K2 W10P10 OFF == stored S_W2.t0 (k = 2.5) 1e-10 rel", abs(f10["off"] - JD["2.5"]["S_W2"]["t0"]) <= 1e-10 * abs(JD["2.5"]["S_W2"]["t0"]), "")
d8, d10 = ref8["on_1e-5"] - ref8["off_1e-5"], f10["on"] - f10["off"]
s8, s10 = abs(ref8["off_1e-6"] - ref8["on_1e-5"]), abs(d10 - art[(10, 10)])
dW2 = {**zero, 2: d8, 2.5: d10}; sdW2 = {**zero, 2: s8, 2.5: s10}
print(f"\nDelta: W8P8 {d8:+.6f} (sigma {s8:.1e}, truth referee); W10P10 {d10:+.6f} (sigma {s10:.1e}, code-vs-model proxy; model {art[(10, 10)]:+.6f})")
Rc, sc, t0c = corrected(zero, dW2, sdW2); grawc = float(np.polyfit(ks, [Rc[k] for k in KS], 1)[0])
c = series(Rc, sc, t0c, grawc, "corr", out)
rob = series(*corrected(zero, dW2, {k: 0.03 * abs(dW2[k]) for k in KS}), grawc, "robust", out)
check("K4 two-route identity (corrected) 1e-10", c["RA1_RA2"] <= 1e-10, f"{c['RA1_RA2']:.1e}")
check("K5 must-fail sign lands in a band different from A's", c["mustfail"]["band"] != c["A"]["band"], f"{c['mustfail']['band']} vs {c['A']['band']}")
print(f"\n(R1) R^c(k) = {[round(Rc[k], 5) for k in KS]}  (stored {[round(R0[k], 5) for k in KS]});  g_raw^c = {grawc:+.5f} (stored {graw0:+.5f});  local slopes {[round(v, 3) for v in lslopes(Rc)]}")
gA = c["A"]; print(f"(R2) A: R_corr^A {[round(Rc[k] - Y[k], 5) for k in KS]}  g_A {gA['g']:+.4f} +- {gA['s']:.4f}  rho_s {gA['rho']:+.4f} +- {gA['srho']:.4f} -> {gA['band']}"
                   f"   [descriptive: / stored g_raw -> {gA['g']/graw0:+.4f}]   [robustness: {rob['A']['band']}]")
bands = [c[f"bulk {nm}"]["band"] for nm in E5]
for nm in E5: b = c[f"bulk {nm}"]; print(f"(R3) bulk [{nm}]: g {b['g']:+.4f} +- {b['s']:.4f}  rho_s {b['rho']:+.4f} +- {b['srho']:.4f} -> {b['band']}   [robustness: {rob[f'bulk {nm}']['band']}]")
rb = bands[0] if len(set(bands)) == 1 and not bands[0].startswith("INCONCLUSIVE") else "INCONCLUSIVE (bracket ends differ or straddle)"
if any(rob[f"bulk {nm}"]["band"] != c[f"bulk {nm}"]["band"] for nm in E5): rb = "INCONCLUSIVE (robustness)"
ra = gA["band"] if rob["A"]["band"] == gA["band"] else "INCONCLUSIVE (robustness)"
tL = c["t0+L"]; Cs = {k: comp[k]["C"] for k in KS}; thr = 0.1 * grawc
sl = {nm: (slope_and_sigma(v, zero)[0], *pairs(v), lslopes(v)) for nm, v in (("t0+L", tL), ("C", Cs), ("Y_A", Y))}
for nm, (g, a, b, l) in sl.items(): print(f"(R5) {nm:5s}: slope {g:+.4f}  pairs 1->2 {a:+.4f}, 1.5->2.5 {b:+.4f}  local {[round(x, 3) for x in l]}  values {[round(tL[k] if nm == 't0+L' else (Cs[k] if nm == 'C' else Y[k]), 4) for k in KS]}")
def clear_neg(nm): return sl[nm][1] < -thr and sl[nm][2] < -thr
def small(nm): return abs(sl[nm][1]) <= thr and abs(sl[nm][2]) <= thr
def split(nm): return np.sign(sl[nm][1]) != np.sign(sl[nm][2])
o = [x for x, ok in (("(a) t0+L", clear_neg("t0+L")), ("(b) C", clear_neg("C")), ("(c) both ~0", small("t0+L") and small("C"))) if ok]
o += [f"(d) {nm} unresolved" for nm in ("t0+L", "C") if split(nm)]
print(f"(R5) outcome map (threshold 0.1 g_raw^c = {thr:.3f}): {o if o else 'none of (a)-(d)'}")
s4 = abs(tL[2] - 0.428) <= 0.03 and abs(tL[2.5] - 0.371) <= 0.03
print(f"(R6) S-4: corrected R(t0+L)(2) {tL[2]:+.4f} vs 0.428, (2.5) {tL[2.5]:+.4f} vs 0.371 (within 0.03) -> {'PASS' if s4 else 'FAIL'}")
head = (f"EXP-090 k <= 2.5 READING: A (finite-k; 085c Y 1/a^2 row still fails; conditional on A-vs-bulk at n = 1): {ra};  bulk: {rb};  "
        f"ingredient: {o};  S-4 {'PASS' if s4 else 'FAIL'};  EXP-086 n = 2 overshoot stands (immune);  controls {'PASS' if not FAIL else FAIL}")
print("\n" + head)
json.dump(dict(mode=mode, Delta=dict(W8P8=d8, W10P10=d10), sigma=dict(W8P8=s8, W10P10=s10), Rc=Rc, graw_c=grawc, out=out, readA=ra, readBulk=rb,
               outcome=o, S4=s4, failed=FAIL, headline=head), open(os.path.join(D, "exp090_k25.json"), "w"), indent=1, default=lambda v: float(v) if np.isscalar(v) else str(v))
sys.exit(1 if FAIL else 0)
