"""EXP-081b unregistered diagnostic (the Bridge, a2b838b): pole census for every production geometry. Per unique slice
(p <= Ny/2), sign-change scan on a 1/2000 grid over [0, s_cut] of F(s) = det((I + M C(z)) D), D = diag(1, z, 1, z, ...)
(= z^W det(I + M C), all entries O(1), so float64 is well-conditioned), brackets refined by brentq; compared with
production's pole list s <= s_cut (count, positions within 1e-6). Near-touch minima of |F| (no sign change at 1/2000) are rescanned locally at step 1e-7
(+-1e-3); a touch left unresolved is reported. First pass (no refinement) kept as exp081b_census_output_pass1.txt: it missed close
pairs (spacing 5e-5..2.5e-4) in the W8P8 geometry. A missed pole BELOW s_cut flags
that geometry's R. Control: the W4P4 geometry with the cut raised to 4.0 must report the known miss at s = 3.9476.
[model: Opus 5.5]"""
import os, sys, json, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3

def F_slice(sl):
    W = sl.W; M = sl.M
    def F(s):
        z = np.exp(-2 * np.pi * s); CD = np.zeros((2 * W, 2 * W)); D = np.ones(2 * W)
        for j in range(W): CD[2 * j + 1, 2 * j] = -(z - 1); CD[2 * j, 2 * j + 1] = -(1 - z); D[2 * j + 1] = z
        return np.linalg.det(np.diag(D) + M @ CD)
    return F

def census(S, s_cut):
    out = []
    for p in range(S.Ny // 2 + 1):
        sl = S.sl[p]; F = F_slice(sl); g = np.arange(int(round(s_cut * 2000)) + 1) / 2000; v = np.array([F(x) for x in g])
        own = [brentq(F, g[i], g[i + 1], xtol=1e-15) for i in range(len(g) - 1) if v[i] * v[i + 1] < 0]
        sc = np.abs(v).max(); a = np.abs(v)
        touch = [g[i] for i in range(1, len(g) - 1) if a[i] < a[i - 1] and a[i] < a[i + 1] and v[i - 1] * v[i + 1] > 0 and v[i] * v[i - 1] > 0 and a[i] < 1e-6 * sc]
        for t in touch:                                                   # refinement: local scan, step 1e-7, around each near-touch
            gl = np.linspace(max(t - 1e-3, 0), min(t + 1e-3, s_cut), 20001); vl = np.array([F(x) for x in gl])
            own += [brentq(F, gl[i], gl[i + 1], xtol=1e-15) for i in range(len(gl) - 1) if vl[i] * vl[i + 1] < 0]
        own = sorted(set(round(x, 12) for x in own)); res_touch = []
        for t in touch:                                                   # a touch is resolved if refinement found roots near it
            if not any(abs(x - t) <= 1e-3 for x in own): res_touch.append(t)
        touch = res_touch
        prod = sorted(x for x in sl.s if x <= s_cut)
        match = len(prod) == len(own) and all(abs(x - y) <= 1e-6 for x, y in zip(prod, own))
        out.append(dict(p=p, prod=prod, own=own, match=bool(match), touch=touch))
    return out

def geom(W, P, Wbox=4, c=2):
    Lx, Lt, Ny = 2 * P + Wbox, 2 * P, int(c * 2 * P); x0 = P + (Wbox - W) // 2
    return S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)

if __name__ == "__main__":
    res = {}
    S = geom(4, 4); ctl = census(S, 4.0); fired = not all(r["match"] for r in ctl)
    print(f"control (W4P4, cut raised to 4.0): {'FIRES' if fired else 'DOES NOT FIRE (control failed)'}: "
          f"{[(r['p'], [round(x, 4) for x in r['prod']], [round(x, 4) for x in r['own']]) for r in ctl if not r['match']]}", flush=True)
    res["control_fires"] = bool(fired); del S
    geoms = [(W, P, 4, 2) for P in (4, 6, 8, 10, 12) for W in (2, 4)] + [(W, 6, 4, 3) for W in (2, 4)] + [(4, 8, 8, 2), (8, 8, 8, 2)]
    for W, P, Wbox, c in geoms:
        S = geom(W, P, Wbox, c); r = census(S, 3.0); ok = all(x["match"] and not x["touch"] for x in r)
        tag = f"W{W}_P{P}_box{Wbox}_c{c}"; res[tag] = dict(ok=bool(ok), slices=r)
        bad = [(x["p"], [round(y, 6) for y in x["prod"]], [round(y, 6) for y in x["own"]], x["touch"]) for x in r if not (x["match"] and not x["touch"])]
        print(f"{tag}: {'all slices MATCH' if ok else 'MISMATCH ' + str(bad)}  (poles <= 3 per slice: {[len(x['own']) for x in r]})", flush=True)
        del S
    json.dump(res, open(os.path.join(HERE, "exp081b_census_results.json"), "w"), indent=1, default=float)
