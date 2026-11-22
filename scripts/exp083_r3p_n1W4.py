"""R3' P = 2 grade: is W4P2's n = 1 value (3.5e-8, 10x the W2P2 floor) quadrature-independent like W2's? One variable at a time:
npt 120 -> 200; Mt 160 -> 320; tmax 8 -> 12. W2P2 n = 1 repeated as the known-answer control (3.557659e-9). [model: Opus 5.5]"""
import numpy as np, sigma3d as S3, exp083_r3_qcont as QC
from exp083_honest import Geom
for W in (2, 4):
    g = Geom(W, 2); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0)
    for lab, npt, kw in (("chain", 120, dict(Mx=48, Mt=160, tmax=8.0)), ("npt200", 200, dict(Mx=48, Mt=160, tmax=8.0)),
                         ("Mt320", 120, dict(Mx=48, Mt=320, tmax=8.0)), ("tmax12", 120, dict(Mx=48, Mt=160, tmax=12.0))):
        if W == 2 and lab != "chain": continue
        q = QC.QCont(S, npt=npt, npt0=512).Q(1.0, **kw); print(f"W{W}P2 n=1 {lab:7s}: Q_cont(1) {q.real:+.6e} imag {q.imag:+.1e}", flush=True)
