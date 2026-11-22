"""EXP-083 R3' arm (b), comparison C2 (registered 4ee07fe): route (ii) Q_cont^sad(n) on the production Strip3D carrying the
continued-gap saddle sigma_n, vs honest arm (b) in Arb.
  Q_cont^sad(n) = QCont(strip_sigma(g, sigma_n), npt 120, npt0 512).Q(n; Mx 48, Mt 160, tmax 8) + n sum_k [ld1_k(sigma_n) - ld1_k(0)]
  (QCont subtracts n * ld1 of its own strip; the constant-offset identity of route (ii) gives exactly n * ld1).
Pass per n: |dev_b(n)| <= max(3 dev_a(n), 1e-10), dev_a from the arm-(a) chain (exp083_r3p/W{W}P{P}_base.json).
Plants: sigma = 0 (arm-(a) Q_cont, from the arm-(a) chain) vs honest arm (b) must FAIL; sigma_n x (1 + 1e-6) probe at n = 2, 3.
Route-(ii) T_sad: [Q_cont^sad(1+h) - Q_cont^sad(1-h)]/2h - (arm-(a) link FD), h = 1e-3, vs C1 T_FD (<= 1e-4 rel).
Usage: python exp083_armb_c2.py W P nmax   [model: Opus 5.5]
Since slip 15 (2026-11-22): strip_sigma solves every slice (alias=False) and the tolerance goes through tools/tol_ref.ref_tol."""
import sys, os, json, time, numpy as np, mpmath as mp
from exp083_honest import Geom
import sigma3d as S3, exp083_armb as AB, exp083_r3_qcont as QC
W, P, NMAX = (int(a) for a in sys.argv[1:4]); g = Geom(W, P); T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "exp083_armb")
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)
kw = dict(Mx=48, Mt=160, tmax=8.0)
hon = json.load(open(os.path.join(HERE, "exp083_r2" if P == 2 else "exp083_r3p", f"W{W}P{P}b.json")))["Q"]
arma = json.load(open(os.path.join(HERE, "exp083_r3p", f"W{W}P{P}_base.json")))
link = json.load(open(os.path.join(HERE, "exp083_r3p", f"W{W}P{P}_link.json")))["link"]
c1 = json.load(open(os.path.join(OUT, f"c1_W{W}P{P}box4c2.json")))
ck = os.path.join(OUT, f"c2_W{W}P{P}.json"); st = json.load(open(ck)) if os.path.exists(ck) else {}
def save(): json.dump(st, open(ck, "w"), indent=1)
ld0 = QC.QCont(AB.strip_sigma(g, None), npt=120, npt0=512).ld1
from tools.tol_ref import ref_tol
S_ref = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); S_own = AB.strip_sigma(g, None)   # reference path vs own path
hon_a = json.load(open(os.path.join(HERE, "exp083_r2" if P == 2 else "exp083_r3p", f"W{W}P{P}a.json")))["Q"]
gap = AB.Gap(g, s_cut=3.0, target="direct"); G1 = g.Gn(1); J0 = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
def qsad(n, sig):
    Qc = QC.QCont(AB.strip_sigma(g, sig), npt=120, npt0=512); return Qc.Q(n, **kw) + n * (Qc.ld1 - ld0).sum()
sig, J = None, J0
for n in range(1, NMAX + 1):
    if str(n) in st: sig = np.array(st[str(n)]["sigma"]); continue
    if n == 1: s_n, F = np.zeros(g.N), 0.0
    else:
        s_n, info = gap.solve(float(n), sig0=sig, J=J); F = info["F"]; J = info["J"]
        sh, _ = g.saddle(n); dsig = float(np.abs(s_n - sh).max())
    q = qsad(float(n), s_n); hv = 0.0 if n == 1 else float(mp.mpf(hon[str(n)])); d = abs(q.real - hv)
    da = arma[str(n)]["dev"] if str(n) in arma else None; tol = None
    if da is not None:   # slip-15 guard: dev_a must be on arm (b)'s own construction path, or the larger is used (logged)
        own = lambda: abs(QC.QCont(S_own, npt=120, npt0=512).Q(float(n), **kw).real - (0.0 if n == 1 else float(mp.mpf(hon_a[str(n)]))))
        tol, tinfo = ref_tol(3, da, 1e-10, S_ref, S_own, own, log=log)
    pl = abs(arma[str(n)]["qcont"] - hv) if str(n) in arma else None
    st[str(n)] = dict(qsad=q.real, imag=q.imag, honest=hv, dev=d, dev_a=da, tol=tol, gapF=F, sigma=list(s_n),
                      sig_vs_honest=(None if n == 1 else dsig), plant_sigma0=pl,
                      verdict=(None if tol is None else ("PASS" if d <= tol else "FAIL")))
    if n in (2, 3):
        qp = qsad(float(n), s_n * (1 + 1e-6)); st[str(n)]["probe_1e-6"] = abs(qp.real - hv)
    save(); sig = s_n
    log(f"W{W}P{P} n={n}: Q_sad {q.real:+.12f} honest {hv:+.12f} |dev| {d:.1e} (tol {tol if tol is None else f'{tol:.1e}'}) "
        f"{st[str(n)]['verdict']}; plant sigma=0 dev {pl if pl is None else f'{pl:.1e}'}"
        + (f"; probe x(1+1e-6) dev {st[str(n)]['probe_1e-6']:.1e}" if n in (2, 3) else "")
        + ("" if n == 1 else f"; |sigma - honest saddle| {dsig:.1e}, gap |F| {F:.1e}"))
if "tsad_route" not in st:
    h = 1e-3; gs = AB.Gap(g, s_cut=3.0, target="self")
    sp, _ = gs.solve(1 + h, J=J0); sm, _ = gs.solve(1 - h, J=J0)
    fd = (qsad(1 + h, sp) - qsad(1 - h, sm)).real / (2 * h); T = fd - link["fd"]
    st["tsad_route"] = dict(fd_total=fd, fd_arma=link["fd"], T_route=T, T_c1=c1["T_lin"], rel=abs(T - c1["T_lin"]) / abs(c1["T_lin"]))
    save(); log(f"route-(ii) T_sad {T:+.10f} vs C1 T_FD {c1['T_lin']:+.10f}: rel {st['tsad_route']['rel']:.1e} -> "
                f"{'PASS' if st['tsad_route']['rel'] <= 1e-4 else 'FAIL'} (<= 1e-4)")
