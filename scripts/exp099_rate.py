"""EXP-099 amendment 2: x-edge decay rate vs the t-slab (registered before running). [model: Opus 5.5]"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
def S(W, gL, gR, hT, Ny): return float(S3.FreeStrip(gL + W + gR, 2 * hT, Ny, list(range(gL, gL + W)), hT - 1).S(cpts=12).real)
def rates(vals, delta):
    d = [vals[j] - vals[j + 1] for j in range(len(vals) - 1)]
    return d, [math.log(d[j] / d[j + 1]) / delta if d[j] * d[j + 1] > 0 else float("nan") for j in range(len(d) - 1)]
FAILS = []
def check(n, ok, det=""):
    print(f"{n:76s} {'PASS' if ok else 'FAIL'} {det}", flush=True)
    if not ok: FAILS.append(n)
g = [1 + 0.25 * j for j in range(13)]
_, r = rates([3.0 * math.exp(-0.5 * x) for x in g], 0.25)
check("estimator KA: pure exp, kappa* = 0.5 recovered to 1e-9", max(abs(x - 0.5) for x in r) <= 1e-9, f"{max(abs(x - 0.5) for x in r):.1e}")
_, r2 = rates([math.exp(-0.5 * x) + math.exp(-0.3 * x) for x in g], 0.25)
check("estimator must-fire: two exps -> last rate nearer 0.3, sequence not constant", abs(r2[-1] - 0.3) < abs(r2[-1] - 0.5) and max(r2) - min(r2) > 1e-3, f"last {r2[-1]:.4f} spread {max(r2)-min(r2):.3f}")
for k in (1, 2, 3):
    P = 4 * k; st = json.load(open(os.path.join(HERE, "exp081b_results", f"free_W{P}_P{P}_box{P}_c2.json")))["S"]
    check(f"KA-A k={k}: (W=P, g=P, hT=P) == stored convention A", S(P, P, P, P, 4 * P) == st)
if FAILS: print("CONTROLS FAILED -> STOP"); sys.exit(1)
out = {}; verdict_pts = []
for k in (1, 2, 3):
    P = 4 * k; dl = P // 4; gs = [P + j * dl for j in range(13)]
    for m in (1, 2, 4):
        Lt = 2 * m * P; kl = 2 * math.acosh(2 - math.cos(math.pi / (Lt + 1)))
        for W in (P // 2, P):
            vals = [S(W, x, x, m * P, 4 * P) for x in gs]; d, r = rates(vals, dl)
            ok = [j for j in range(len(r)) if abs(d[j + 1]) > 1e-9 * abs(vals[0]) and not math.isnan(r[j])]
            if len(ok) < 3: km, dr = float("nan"), float("nan")
            else: km = r[ok[-1]]; last = [r[j] for j in ok[-3:]]; dr = max(last) - min(last)
            out[f"k{k}_hT{m}P_W{W}"] = dict(P=P, hT=m * P, W=W, Lt=Lt, kappa_lat=kl, kappa_meas=km, drift=dr, rel=km / kl - 1, rates=r, dS=d, usable=ok)
            verdict_pts.append((km / kl - 1, dr / kl))
            print(f"k={k} hT={m}P W={W:2d}: kappa_meas {km:.5f} (P*k {km*P:.4f})  kappa_lat {kl:.5f}  rel {km/kl-1:+.4f}  drift/kl {dr/kl:.4f}  usable j {len(ok)}", flush=True)
sup = all(abs(a) <= 0.02 and b <= 0.02 for a, b in verdict_pts)
rej = any(abs(a) > 0.05 and b <= 0.02 for a, b in verdict_pts)
V = "SUPPORTED" if sup else ("REJECTED" if rej else "UNSETTLED"); print(f"\nVERDICT (registered): {V}")
for k in (1, 2, 3):
    for W in (2 * k, 4 * k):
        a, b, c = (out[f"k{k}_hT{m}P_W{W}"]["kappa_meas"] for m in (1, 2, 4))
        print(f"   1/Lt test k={k} W={W}: kappa(P)/kappa(2P) {a/b:.4f}  kappa(2P)/kappa(4P) {b/c:.4f}")
json.dump(dict(amendment=2, verdict=V, points=out), open(os.path.join(HERE, "exp081d_results", "exp099_rate.json"), "w"), indent=1)
