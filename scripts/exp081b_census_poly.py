"""EXP-081b pole census, grid-free (unregistered diagnostic): F(z) = det((I + M C(z)) D), D = diag(1, z, ...), has every column
linear in z, so it is a polynomial of degree <= 2W. Coefficients from 120-digit samples (pass 2; pass 1 at 50 digits lost a real root to the precision floor) on the unit circle (exact DFT), all roots by
mp.polyroots, keep real roots with s = -ln z/(2 pi) in (0, s_cut]; compare with production (count, positions <= 1e-6).
Control: W4P4 at s_cut = 4 must report production's known miss (s = 3.9476). [model: Opus 5.5]"""
import os, sys, json, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
mp.mp.dps = 120                                                            # pass 2: 50 digits sat at the floor (coefficients span 1e-51..1); pass 1 kept

def roots_s(sl, s_cut):
    W = sl.W; M = mp.matrix(sl.M.tolist()); n = 2 * W + 1        # float64 M is the production object under census
    def F(z):
        A = mp.eye(2 * W)
        for j in range(W): A[2 * j + 1, 2 * j + 1] = z
        CD = mp.zeros(2 * W, 2 * W)
        for j in range(W): CD[2 * j + 1, 2 * j] = -(z - 1); CD[2 * j, 2 * j + 1] = -(1 - z)
        return mp.det(A + M * CD)
    w = [mp.exp(2j * mp.pi * k / n) for k in range(n)]; v = [F(x) for x in w]
    c = [sum(v[k] * w[k] ** (-m) for k in range(n)) / n for m in range(n)]   # c[m] = coefficient of z^m
    while abs(c[-1]) < mp.mpf(10) ** -110 * max(abs(x) for x in c): c.pop()
    rts = mp.polyroots(c[::-1], maxsteps=400, extraprec=200)
    zmin = mp.exp(-2 * mp.pi * s_cut)
    return sorted(float(-mp.log(mp.re(r)) / (2 * mp.pi)) for r in rts if abs(mp.im(r)) < mp.mpf(10) ** -40 * abs(r) and zmin <= mp.re(r) < 1), len(c) - 1

def geom(W, P, Wbox=4, c=2):
    Lx, Lt, Ny = 2 * P + Wbox, 2 * P, int(c * 2 * P); x0 = P + (Wbox - W) // 2
    return S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)

def census(S, s_cut):
    out = []
    for p in range(S.Ny // 2 + 1):
        own, deg = roots_s(S.sl[p], s_cut); prod = sorted(x for x in S.sl[p].s if x <= s_cut)
        out.append(dict(p=p, prod=prod, own=own, deg=deg, match=bool(len(prod) == len(own) and all(abs(a - b) <= 1e-6 for a, b in zip(prod, own)))))
    return out

if __name__ == "__main__":
    res = {}; S = geom(4, 4); ctl = census(S, 4.0); fired = not all(r["match"] for r in ctl)
    print(f"control (W4P4, s_cut 4): {'FIRES' if fired else 'DOES NOT FIRE (control failed)'}: {[(r['p'], [round(x, 4) for x in r['prod']], [round(x, 4) for x in r['own']]) for r in ctl if not r['match']]}", flush=True)
    res["control_fires"] = bool(fired)
    geoms = [(W, P, 4, 2) for P in (4, 6, 8, 10, 12) for W in (2, 4)] + [(W, 6, 4, 3) for W in (2, 4)] + [(4, 8, 8, 2), (8, 8, 8, 2)]
    for W, P, Wbox, c in geoms:
        S = geom(W, P, Wbox, c); r = census(S, 3.0); ok = all(x["match"] for x in r); tag = f"W{W}_P{P}_box{Wbox}_c{c}"
        mx = max((abs(a - b) for x in r if x["match"] for a, b in zip(x["prod"], x["own"])), default=0.0)
        res[tag] = dict(ok=bool(ok), maxdiff=mx, slices=r)
        print(f"{tag}: {'all slices MATCH' if ok else 'MISMATCH ' + str([(x['p'], x['prod'], x['own']) for x in r if not x['match']])}  max |ds| {mx:.1e}  degree {sorted(set(x['deg'] for x in r))}", flush=True)
    json.dump(res, open(os.path.join(HERE, "exp081b_census_poly_results.json"), "w"), indent=1, default=float)
