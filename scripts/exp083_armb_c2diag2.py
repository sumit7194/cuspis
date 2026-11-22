"""C2 W4P4 n = 2, step 2: is the strip_sigma(None) vs production Strip3D difference at sigma = 0 (dev 2.32e-10 vs 1.04e-10)
the mirror aliasing of slices (strip_sigma reuses slice p for Ny - p; production builds every slice)? One variable: strip_sigma
WITHOUT aliasing (all Ny slices built). Prediction if aliasing: dev -> 1.04e-10 (the production value). [model: Opus 5.5]"""
import json, numpy as np, mpmath as mp, sigma3d as S3, exp083_armb as AB, exp083_r3_qcont as QC
from exp083_honest import Geom
g = Geom(4, 4); kw = dict(Mx=48, Mt=160, tmax=8.0); ha = float(mp.mpf(json.load(open("exp083_r3p/W4P4a.json"))["Q"]["2"]))
def strip_noalias(g, sigma, s_cut=3.0):
    S = S3.Strip3D.__new__(S3.Strip3D)
    S.Lx, S.Lt, S.Ny, S.cutx, S.tcut, S.s_cut, S.drop_double, S.N = g.Lx, g.Lt, g.Ny, list(g.cutx), g.tcut, s_cut, False, g.N
    idx = lambda x, t: x * g.Lt + t; sig = np.zeros(g.N) if sigma is None else np.asarray(sigma, float)
    S.sl = [AB.SliceS(g.Lx, g.Lt, 2 - 2 * np.cos(2 * np.pi * p / g.Ny), g.cutx, g.tcut, idx, sig) for p in range(g.Ny)]
    return S
Sp = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); Sa = AB.strip_sigma(g, None); Sn = strip_noalias(g, None)
for lab, S in (("production", Sp), ("strip_sigma aliased", Sa), ("strip_sigma NO alias", Sn)):
    mx = max(max((abs(a - b) for a, b in zip(sorted(S.sl[p].s), sorted(Sp.sl[p].s))), default=0.0) for p in range(g.Ny))
    print(f"{lab:22s}: max |s - s_prod| over slices {mx:.1e}", flush=True)
for lab, S in (("strip_sigma NO alias", Sn),):
    q = QC.QCont(S, npt=120, npt0=512).Q(2.0, **kw).real; print(f"arm (a) n=2 via {lab}: dev {abs(q - ha):.2e} (production 1.04e-10, aliased 2.32e-10)", flush=True)
