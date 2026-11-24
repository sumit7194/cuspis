"""EXP-086 (registration notes/EXP-086_registration.md): T54 counterterm at INTEGER n = 2, stored data only. [model: Opus 5.5]
dR_n(k) = (n/(2(n-1))) Ny c [Sum sigma_n(W1) - Sum sigma_n(W2)] norm(k);  eta = (d(2) + g_ct)/|g_ct|, signed bands, both c ends."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "exp081d_results")
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); KS = [1, 1.5, 2]; KS4 = [1, 1.5, 2, 2.5]; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:60s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def norm(k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]
def dR(n, k, c, S1, S2): return (n / (2.0 * (n - 1))) * (4 * int(4 * k)) * c * (S1 - S2) * norm(k)
miss = [f for k in KS for W in (int(2 * k), int(4 * k)) for f in [os.path.join(D, "exp084c", f"c84_W{W}P{int(4*k)}_n2.json")] if not os.path.exists(f)]
if miss: print("missing sigma_2 files -> not run:", miss); sys.exit(2)
# ---- controls on code paths (before any reading) ----
k = 2; exp = (4 * 8) * 1.0 / (4 * 8) / (1 / 4 - 1 / 8) / JD["2"]["kappa"]                      # Ny * norm(2), independent
check("planted normalisation (dSig2=1, c=1, k=2, n=2)", abs(dR(2, 2, 1.0, 1.0, 0.0) - exp) <= 1e-12 * abs(exp), f"{dR(2,2,1.0,1.0,0.0)!r} vs {exp!r}")
Cg = {(W, int(4 * k)): json.load(open(os.path.join(D, "exp085", f"C_W{W}P{int(4*k)}.json"))) for k in KS for W in (int(2 * k), int(4 * k))}
eps = 1e-6; cc = -0.11410550636913405
for k in KS:
    a, b = Cg[(int(2 * k), int(4 * k))], Cg[(int(4 * k), int(4 * k))]; Ny = 4 * int(4 * k)
    lim = dR(1 + eps, k, cc, eps * a["Sigma3D"] / Ny, eps * b["Sigma3D"] / Ny); ref = 0.5 * cc * (a["Sigma3D"] - b["Sigma3D"]) * norm(k)
    check(f"n -> 1 reduction k={k}: formula == 085 corr", abs(lim - ref) <= 1e-5 * abs(ref), f"{lim!r} vs {ref!r}")
R84 = json.load(open(os.path.join(D, "exp084", "result.json")))["Rn"]["2"]; F84b = json.load(open(os.path.join(D, "exp084b", "result.json")))["fits"]["2"]
R2 = {k: R84[str(k)] for k in KS}; c2, d2, sc2, sd2, rho = F84b
check("KA inputs: R2 and 084b fits read from stored files", all(isinstance(R2[k], float) for k in KS) and len(F84b) == 5, f"d(2) {d2!r}, c(2) {c2!r}, corr {rho:+.4f}")
# d(2) systematic: 2-parameter c k^2 + d k (no constant) on the same 4 k (honest R2 at 4 k from 084)
R2all = np.array([R84[str(k)] for k in KS4]); ks4 = np.array(KS4, float)
p2 = np.linalg.lstsq(np.column_stack([ks4 ** 2, ks4]), R2all, rcond=None)[0]; sd_sys = abs(d2 - p2[1])
print(f"d(2) = {d2:+.5f} (084b 3-param, stat {sd2:.1e}); 2-param (no const) d = {p2[1]:+.5f}  -> sigma_d,sys {sd_sys:.4f}", flush=True)
# ---- reading ----
ends = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]
S2 = {}
for k in KS:
    for W in (int(2 * k), int(4 * k)): S2[(W, int(4 * k))] = float(np.sum(json.load(open(os.path.join(D, "exp084c", f"c84_W{W}P{int(4*k)}_n2.json")))["sigma"]))
ksa = np.array(KS, float)
def band(e, s):
    lo, hi = e - 2 * s, e + 2 * s
    if lo >= -0.1 and hi <= 0.1: return "cancels at n = 2"
    if hi < -0.1: return "overshoot at n = 2"
    if lo > 0.1: return "under at n = 2"
    return "INCONCLUSIVE (straddles a band edge)"
def reading(c, sgn=1.0, scale=1.0):
    ct = {k: sgn * scale * dR(2, k, c, S2[(int(2 * k), int(4 * k))], S2[(int(4 * k), int(4 * k))]) for k in KS}
    y = np.array([ct[k] for k in KS]); g, b0 = np.polyfit(ksa, y, 1); Sxx = np.sum((ksa - ksa.mean()) ** 2)
    sg = float(np.sqrt(np.sum((y - (g * ksa + b0)) ** 2) / (len(ksa) - 2) / Sxx)); dc = d2 + g
    if g == 0: return ct, g, sg, dc, None, None, "n/a (zero counterterm)"
    eta = dc / abs(g); se = np.sqrt(sd2 ** 2 + sd_sys ** 2 + sg ** 2) / abs(g); return ct, float(g), sg, dc, eta, se, band(eta, se)
res = {}
for tag, c in ends.items():
    ct, g, sg, dc, eta, se, b = reading(c); res[tag] = dict(ct=ct, g=g, sg=sg, dcorr=dc, eta=eta, se=se, band=b)
    print(f"[{tag}] dR2 {[round(ct[k], 5) for k in KS]}  g_ct {g:+.4f} +- {sg:.4f}  d_corr {dc:+.4f}  eta {eta:+.4f} +- {se:.4f} -> {b}", flush=True)
    _, _, _, dz, _, _, _ = reading(c, scale=0.0); check(f"[{tag}] zero control: d_corr == d(2) bitwise", dz == d2, f"{dz!r} vs {d2!r}")
    _, _, _, _, em, sm, bm = reading(c, sgn=-1.0); check(f"[{tag}] must-fail sign: band differs from registered", bm != b, f"{bm} (eta {em:+.3f}) vs {b}")
print("--- DESCRIPTIVE (pre-read note): parity-matched k = 1 -> 2 slopes ---", flush=True)
print(f"   honest R2: {R2[2] - R2[1]:+.5f}", flush=True)
for tag, r in res.items(): print(f"   counterterm dR2 [{tag}]: {r['ct'][2] - r['ct'][1]:+.5f}   (R2 + dR2: {(R2[2] + r['ct'][2]) - (R2[1] + r['ct'][1]):+.5f})", flush=True)
bands = {r["band"] for r in res.values()}
lab = (list(bands)[0] if len(bands) == 1 else "INCONCLUSIVE (bracket ends differ)") if not FAIL else "INCONCLUSIVE (control failed)"
print(f"\nEXP-086 READING: {lab}   (honest R2 linear coeff d(2) {d2:+.4f}; k^2 coeff c(2) {c2:+.4f} set aside, as registered; 3 k, 1 dof; controls {'PASS' if not FAIL else FAIL})")
json.dump(dict(reading=lab, res=res, d2=d2, c2=c2, sd_sys=sd_sys, S2={f"W{W}P{P}": v for (W, P), v in S2.items()}, failed=FAIL),
          open(os.path.join(D, "exp086_result.json"), "w"), indent=1, default=float)
sys.exit(1 if FAIL else 0)
