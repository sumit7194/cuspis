"""R3' step 1: route (ii) port quadrature convergence at W2P2 vs Arb honest (n = 1..6): Mx (beta nodes) x Mt (tail nodes) x tmax.
Goal delta <= 1e-11. [model: Opus 5.5]"""
import json, time, numpy as np, mpmath as mp, sigma3d as S3
from exp083_honest import Geom
from exp083_r3_qcont import QCont
T0 = time.time(); g = Geom(2, 2); Qc = QCont(S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0))
hon = json.load(open("exp083_r2/W2P2a.json"))["Q"]
for Mx, Mt, tmax in ((24, 48, 4.0), (48, 48, 4.0), (64, 64, 5.0), (96, 96, 6.0)):
    devs = [abs(Qc.Q(1.0, Mx=Mx, Mt=Mt, tmax=tmax))] + [abs(Qc.Q(float(n), Mx=Mx, Mt=Mt, tmax=tmax).real - float(mp.mpf(hon[str(n)]))) for n in range(2, 7)]
    print(f"Mx {Mx} Mt {Mt} tmax {tmax}: |Q(1)| {devs[0]:.1e}; |Q_cont - honest| n=2..6: " + " ".join(f"{d:.1e}" for d in devs[1:]) + f"  ({time.time()-T0:.0f}s)", flush=True)
