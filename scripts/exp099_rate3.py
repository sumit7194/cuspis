"""EXP-099 amendment 3: at hT = 4P, arm (i) Ny = 16P and arm (ii) g extended to 8P. [model: Opus 5.5]"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
def S(W, gL, gR, hT, Ny): return float(S3.FreeStrip(gL + W + gR, 2 * hT, Ny, list(range(gL, gL + W)), hT - 1).S(cpts=12).real)
def rates(v, dl):
    d = [v[j] - v[j + 1] for j in range(len(v) - 1)]
    return d, [math.log(d[j] / d[j + 1]) / dl if d[j] * d[j + 1] > 0 else float("nan") for j in range(len(d) - 1)]
def read(v, dl):
    d, r = rates(v, dl); ok = [j for j in range(len(r)) if abs(d[j + 1]) > 1e-9 * abs(v[0]) and not math.isnan(r[j])]
    last = [r[j] for j in ok[-3:]]; return r[ok[-1]], max(last) - min(last), r
g = [1 + 0.25 * j for j in range(13)]; _, r = rates([3 * math.exp(-0.5 * x) for x in g], 0.25); _, r2 = rates([math.exp(-0.5 * x) + math.exp(-0.3 * x) for x in g], 0.25)
ok1 = max(abs(x - 0.5) for x in r) <= 1e-9; ok2 = abs(r2[-1] - 0.3) < abs(r2[-1] - 0.5) and max(r2) - min(r2) > 1e-3
print(f"estimator KA {'PASS' if ok1 else 'FAIL'}; must-fire {'PASS' if ok2 else 'FAIL'}")
prev = json.load(open(os.path.join(HERE, "exp081d_results", "exp099_rate.json")))["points"]; bad = not (ok1 and ok2); out = {}
for k in (1, 2, 3):
    P = 4 * k; dl = P // 4; Lt = 8 * P; kl = 2 * math.acosh(2 - math.cos(math.pi / (Lt + 1)))
    for W in (P // 2, P):
        v1 = [S(W, P + j * dl, P + j * dl, 4 * P, 16 * P) for j in range(13)]; k1, d1, _ = read(v1, dl)
        v2 = [S(W, P + j * dl, P + j * dl, 4 * P, 4 * P) for j in range(29)]; k2, d2, r2s = read(v2, dl)
        a2 = prev[f"k{k}_hT4P_W{W}"]; same = [v2[j] - v2[j + 1] for j in range(12)] == a2["dS"]; bad |= not same
        mono = all(abs(r2s[j + 1] - kl) <= abs(r2s[j] - kl) + 1e-12 for j in range(10, len(r2s) - 1) if not math.isnan(r2s[j + 1]))
        out[f"k{k}_W{W}"] = dict(kappa_lat=kl, arm_i=dict(kappa=k1, rel=k1 / kl - 1, drift=d1), arm_ii=dict(kappa=k2, rel=k2 / kl - 1, drift=d2, rates=r2s, monotone_toward=mono), amend2_rel=a2["rel"], bitwise_first13=same)
        print(f"k={k} W={W:2d}: amend2 rel {a2['rel']:+.4f} | (i) Ny=16P rel {k1/kl-1:+.4f} drift/kl {d1/kl:.4f} | (ii) g->8P rel {k2/kl-1:+.4f} drift/kl {d2/kl:.4f} monotone {mono} | first-13 bitwise {same}", flush=True)
i_ok = all(abs(o["arm_i"]["rel"]) <= 0.02 for o in out.values()); ii_ok = all(abs(o["arm_ii"]["rel"]) <= 0.02 for o in out.values())
print(f"arm (i) Ny crossover removes it: {i_ok};  arm (ii) pre-asymptotic g removes it: {ii_ok}")
json.dump(dict(amendment=3, arm_i_removes=i_ok, arm_ii_removes=ii_ok, points=out), open(os.path.join(HERE, "exp081d_results", "exp099_rate3.json"), "w"), indent=1)
sys.exit(1 if bad else 0)
