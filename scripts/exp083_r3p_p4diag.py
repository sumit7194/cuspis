"""R3' arm (a) P = 4 grade diagnostics (after the chain; the graded numbers stay the chain's).
(a) POST HOC plant (labelled): the registered scut_low plant at W2P4 used s_cut = 1.5, but W2P4's poles all lie at s <= 1.329, so
    it could not fire. A correctly specified plant: s_cut = 1.3 (below the kept poles 1.316, 1.329); n = 1, 2. Must FAIL (a).
(b) W4P4 n = 1 floor (5.7e-7, 16x W4P2's): one variable at a time -- npt 200, Mt 320, tmax 12 (quadrature), and s_cut 3.5
    (W4P4 has poles just above the cut at s = 3.011, 3.088). W2P4 n = 1 chain setting repeated as the known-answer control. [model: Opus 5.5]"""
import json, mpmath as mp, sigma3d as S3, exp083_r3_qcont as QC
from exp083_honest import Geom
kw0 = dict(Mx=48, Mt=160, tmax=8.0)
def Q(W, n, s_cut=3.0, npt=120, **kw):
    g = Geom(W, 4); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=s_cut); k = dict(kw0); k.update(kw)
    return QC.QCont(S, npt=npt, npt0=512).Q(float(n), **k)
out = {}
hon = json.load(open("exp083_r3p/W2P4a.json"))["Q"]
for n in (1, 2):
    q = Q(2, n, s_cut=1.3); hv = 0.0 if n == 1 else float(mp.mpf(hon[str(n)])); out[f"plant13_n{n}"] = abs(q.real - hv)
    print(f"(a) W2P4 POST-HOC plant s_cut 1.3, n={n}: dev {abs(q.real - hv):.2e}", flush=True)
q = Q(2, 1); out["ctl_W2_n1"] = q.real; print(f"(b) control W2P4 n=1 chain setting: {q.real:+.6e} (chain 3.4e-09)", flush=True)
for lab, a in (("chain", {}), ("npt200", dict(npt=200)), ("Mt320", dict(Mt=320)), ("tmax12", dict(tmax=12.0)), ("scut3.5", dict(s_cut=3.5))):
    q = Q(4, 1, **a); out[f"W4n1_{lab}"] = [q.real, q.imag]; print(f"(b) W4P4 n=1 {lab:8s}: Q_cont(1) {q.real:+.6e} imag {q.imag:+.1e}", flush=True)
json.dump(out, open("exp083_r3p/p4diag.json", "w"), indent=1)
