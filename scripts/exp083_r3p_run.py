"""EXP-083 R3' (registered c9a0ed0) driver, ARM (a) ONLY: route (ii) Q_cont(n) of the production Strip3D continuation vs Arb honest
integers, plus planted / known-bad variants and the route (ii) <-> route_b link. Checkpointed per (geometry, variant, n).
Discretization: inner npt 120, inner_beta0 npt0 512, Mx 48, Mt 160, tmax 8 (step-1 convergence: delta ~ 1e-10 at n >= 2, n = 1 floor
3.6e-9 from production's pole/residue precision). Usage: python exp083_r3p_run.py W P nmax variant   [model: Opus 5.5]
variants: base | scut_low (P2: 1.2, P4: 1.5) | merge_tiny (inner_beta0 merge tol 1e-15*rad) | drop_pole (smallest-s pole of slice 1 and
its mirror removed) | res_scale (that pole's residues x (1 + 1e-6)) | dd1 (confluent residues dropped) | link (FD Q'(1) vs route_b)"""
import sys, os, json, time, importlib.util, numpy as np, mpmath as mp
from exp083_honest import Geom
import exp083_r3_qcont as QC
W, P, NMAX, VAR = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "exp083_r3p"); os.makedirs(OUT, exist_ok=True)
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)
src = open(os.path.join(HERE, "sigma3d.py")).read()
if VAR == "merge_tiny":
    t = src.replace("abs(m[0] - a0) < 1e-2 * rad]", "abs(m[0] - a0) < 1e-15 * rad]"); assert t != src
    p = os.path.join(OUT, "_sigma3d_merge_tiny.py"); open(p, "w").write(t); spec = importlib.util.spec_from_file_location("s3m", p)
    S3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(S3)
else:
    import sigma3d as S3
g = Geom(W, P); s_cut = (1.2 if P == 2 else 1.5) if VAR == "scut_low" else 3.0
S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=s_cut, drop_double=(VAR == "dd1"))
if VAR in ("drop_pole", "res_scale"):
    for p in (1, g.Ny - 1):
        sl = S.sl[p]; j = int(np.argmin(sl.s))
        if VAR == "drop_pole": sl.s = [x for i, x in enumerate(sl.s) if i != j]; sl.Rp = [x for i, x in enumerate(sl.Rp) if i != j]; sl.Rm = [x for i, x in enumerate(sl.Rm) if i != j]
        else: sl.Rp[j] = sl.Rp[j] * (1 + 1e-6); sl.Rm[j] = sl.Rm[j] * (1 + 1e-6)
Qc = QC.QCont(S, npt=120, npt0=512); kw = dict(Mx=48, Mt=160, tmax=8.0)
ck = os.path.join(OUT, f"W{W}P{P}_{VAR}.json"); st = json.load(open(ck)) if os.path.exists(ck) else {}
hon = json.load(open(os.path.join(HERE, "exp083_r2" if P == 2 else "exp083_r3p", f"W{W}P{P}a.json")))["Q"]
if VAR == "link":
    h = 1e-3; qp = (Qc.Q(1 + h, **kw) - Qc.Q(1 - h, **kw)) / (2 * h)
    S0 = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); ckb = os.path.join(OUT, f"routeb_W{W}P{P}_ckpt.json"); S3.route_b(S0, ckb)
    sb = json.load(open(ckb)); x, wq = np.polynomial.legendre.leggauss(12); C = 0.0
    for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
        for xi, wi in zip(x, wq):
            si = 0.5 * (hi - lo) * (xi + 1) + lo; C += 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2 * sb[f"g|{si:.15f}"][0]
    rb = sb["t0"] + C; rel = abs(qp.real - rb) / abs(rb); st["link"] = dict(fd=qp.real, routeb=rb, rel=rel)
    log(f"LINK W{W}P{P}: route (ii) FD Q'(1) {qp.real:+.10f} vs route_b t0 + C {rb:+.10f}: rel {rel:.1e} -> {'PASS' if rel <= 1e-5 else 'FAIL'}")
else:
    for n in range(1, NMAX + 1):
        if str(n) in st: continue
        q = Qc.Q(float(n), **kw); hv = 0.0 if n == 1 else float(mp.mpf(hon[str(n)])); d = abs(q.real - hv)
        st[str(n)] = dict(qcont=q.real, imag=q.imag, honest=hv, dev=d); json.dump(st, open(ck, "w"), indent=1)
        log(f"W{W}P{P} {VAR} n={n}: Q_cont {q.real:+.12f} honest {hv:+.12f} |dev| {d:.1e}")
json.dump(st, open(ck, "w"), indent=1)
