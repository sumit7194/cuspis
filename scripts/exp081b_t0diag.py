"""EXP-081b t0 diagnosis (Ny control fired: W4P6 c=3 t0 off its x1.5 scaling by ~2.5%). Lists, for each geometry, the
closest pole pairs between DIFFERENT slices p, q (any k = p+q), flagging pairs split by s_cut (one <= s_cut < other).
Hypothesis: a near-confluent pair split by s_cut leaves an uncancelled 1/Delta residue term in inner_beta0. [model: Opus 5.5]"""
import sys, numpy as np, sigma3d as S3
def geom(W, P, c, Wbox=4):
    Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2; Ny = int(c * 2 * P)
    return S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
for W, P, c in [(4, 6, 2), (4, 6, 3), (2, 6, 2), (2, 6, 3)] + [(4, P, 2) for P in (4, 8, 10, 12)]:
    S = geom(W, P, c); Ny = S.Ny; pairs = []
    for p in range(Ny):
        for q in range(Ny):
            if np.isclose(S.sl[p].m2 if hasattr(S.sl[p], 'm2') else 2 - 2*np.cos(2*np.pi*p/Ny), 2 - 2*np.cos(2*np.pi*q/Ny)): continue
            for sa in S.sl[p].s:
                for sb in S.sl[q].s:
                    pairs.append((abs(sa - sb), p, q, sa, sb))
    pairs.sort(); split = [x for x in pairs if min(x[3], x[4]) <= 3.0 < max(x[3], x[4])]
    print(f"W{W} P{P} c{c} (Ny {Ny}): closest distinct-slice pole pairs: " + "; ".join(f"|ds| {d:.1e} (p{p} s={a:.6f}, q{q} s={b:.6f})" for d, p, q, a, b in pairs[:3:2]), flush=True)
    print(f"   closest pairs SPLIT by s_cut=3: " + ("; ".join(f"|ds| {d:.1e} (p{p} s={a:.6f}, q{q} s={b:.6f})" for d, p, q, a, b in split[:4:2]) if split else "none"), flush=True)
