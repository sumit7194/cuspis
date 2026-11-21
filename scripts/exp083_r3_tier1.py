"""R3 Tier-1: Strip3D route (ii) Q_cont(n) at W2P2 (real n): vs Arb honest Q(n) at n = 2, 3, 4 (arm a), and FD Q'(1) vs route_b
t0 + C (exp083_r2 production checkpoint). No verdict. [model: Opus 5.5]"""
import json, time, numpy as np, mpmath as mp
import sigma3d as S3
from exp083_honest import Geom
from exp083_r3_qcont import QCont
T0 = time.time()
g = Geom(2, 2); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); Qc = QCont(S)
hon = json.load(open("exp083_r2/W2P2a.json"))["Q"]
for n in (2, 3, 4):
    q = Qc.Q(float(n)); print(f"n={n}: Q_cont {q.real:+.12f}{q.imag:+.1e}j | honest {float(mp.mpf(hon[str(n)])):+.12f} | diff {abs(q.real - float(mp.mpf(hon[str(n)]))):.1e}  ({time.time()-T0:.0f}s)", flush=True)
for tmax, Mt in ((4.0, 48), (6.0, 96)):
    for h in (1e-3,):
        qp = (Qc.Q(1 + h, Mt=Mt, tmax=tmax) - Qc.Q(1 - h, Mt=Mt, tmax=tmax)) / (2 * h)
        st = json.load(open("exp083_r2/prod_W2P2_sc3.0_dd0_ckpt.json"))
        x, w = np.polynomial.legendre.leggauss(12); C = 0.0
        for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
            for xi, wi in zip(x, w):
                si = 0.5 * (hi - lo) * (xi + 1) + lo; C += 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2 * st[f"g|{si:.15f}"][0]
        print(f"FD Q'(1) (h={h}, tmax {tmax}, Mt {Mt}) = {qp.real:+.10f} | route_b t0 + C = {st['t0'] + C:+.10f} | diff {abs(qp.real - st['t0'] - C):.1e}  ({time.time()-T0:.0f}s)", flush=True)
