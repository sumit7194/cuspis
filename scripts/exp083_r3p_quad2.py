"""R3' step 1b: inner discretizations (inner npt, inner_beta0 npt0) + outer (Mt, tmax) at W2P2, n = 1..6 vs Arb. [model: Opus 5.5]"""
import json, time, numpy as np, mpmath as mp, sigma3d as S3
from exp083_honest import Geom
from exp083_r3_qcont import QCont
T0 = time.time(); g = Geom(2, 2); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0)
hon = json.load(open("exp083_r2/W2P2a.json"))["Q"]
for npt, npt0, Mt, tmax in ((40, 256, 96, 6.0), (80, 256, 128, 7.0), (120, 512, 160, 8.0)):
    Qc = QCont(S, npt=npt, npt0=npt0)
    devs = [abs(Qc.Q(1.0, Mx=48, Mt=Mt, tmax=tmax))] + [abs(Qc.Q(float(n), Mx=48, Mt=Mt, tmax=tmax).real - float(mp.mpf(hon[str(n)]))) for n in range(2, 7)]
    print(f"npt {npt} npt0 {npt0} Mt {Mt} tmax {tmax}: |Q(1)| {devs[0]:.1e}; dev n=2..6: " + " ".join(f"{d:.1e}" for d in devs[1:]) + f"  ({time.time()-T0:.0f}s)", flush=True)
