"""EXP-083 R3' arm (a) P = 2 grade, cause diagnostic (not a retune; the graded numbers stay the chain's): ONE variable changed --
tail range tmax = 48/n (= 8 at n = 6, the step-1 converged setting) instead of fixed 8; Mt 160, Mx 48, npt 120, npt0 512 unchanged.
Hypothesis: the fixed Gauss t-grid under-resolves the kernel 1/(e^{2 pi n t} + 1) (scale 1/(2 pi n)) at large n -> the growing
deviation; and gk at large n*t overflows -> W4P2 NaN from n = 38. Prediction: dev(n) back to <~ 1e-9 and no NaN.
Also records which piece is NaN at the fixed grid (W4P2 n = 38). Usage: python exp083_r3p_taildiag.py   [model: Opus 5.5]"""
import json, time, numpy as np, mpmath as mp
from exp083_honest import Geom
import sigma3d as S3, exp083_r3_qcont as QC
T0 = time.time(); out = {}
for W, ns in ((2, (12, 24, 30, 54, 72)), (4, (24, 38, 72))):
    g = Geom(W, 2); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); Qc = QC.QCont(S, npt=120, npt0=512)
    hon = json.load(open(f"exp083_r2/W{W}P2a.json"))["Q"]; base = json.load(open(f"exp083_r3p/W{W}P2_base.json"))
    for n in ns:
        q = Qc.Q(float(n), Mx=48, Mt=160, tmax=48.0 / n); hv = float(mp.mpf(hon[str(n)])); d = abs(q.real - hv)
        out[f"W{W}n{n}"] = dict(q=q.real, imag=q.imag, dev=d, dev_chain=base[str(n)]["dev"])
        print(f"[{time.time()-T0:5.0f}s] W{W}P2 n={n}: tmax 48/n dev {d:.2e} (chain, tmax 8: {base[str(n)]['dev']:.2e}); imag {q.imag:.1e}", flush=True)
# where the NaN comes from at the fixed grid (W4P2 n = 38): scan gk along eps + i t
g = Geom(4, 2); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); Qc = QC.QCont(S, npt=120, npt0=512); n = 38.0
for t in (0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
    v = Qc.gk(n, 1 / (2 * n) + 1j * t); print(f"   W4 n=38 gk(eps + i {t}): finite {bool(np.all(np.isfinite(v)))}, |sum| {abs(v.sum()):.3e}", flush=True)
    out[f"nan_scan_t{t}"] = bool(np.all(np.isfinite(v)))
json.dump(out, open("exp083_r3p/taildiag_P2.json", "w"), indent=1)
