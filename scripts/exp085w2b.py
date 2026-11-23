"""EXP-085w2b (registration notes/EXP-085w2_registration.md): route (ii) Q_cont^sad at W4P4 (Wbox 4) n = 2 with s_cut = SC in Gap AND every
strip_sigma call (084c's default 3 is the one variable). Usage: exp085w2b.py SC   (SC = 3: KA, must reproduce exp084c/c84_W4P4_n2.json bitwise;
SC = 6: the test). 084c one-geometry code otherwise verbatim. [model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exp083_honest as H, exp083_armb as AB, exp083_r3_qcont as QC
SC = float(sys.argv[1]); W, P, n = 4, 4, 2; KW = dict(Mx=48, Mt=160, tmax=8.0); T0 = time.time(); FAIL = []
OUT = os.path.join(HERE, "exp081d_results", "exp085w"); os.makedirs(OUT, exist_ok=True)
ref = json.load(open(os.path.join(HERE, "exp081d_results", "exp084c", "c84_W4P4_n2.json")))
def check(nm, ok, det=""):
    print(f"{nm:60s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
g = H.Geom(W, P, Wbox=P, c=2); gap = AB.Gap(g, s_cut=SC, target="direct"); G1 = g.Gn(1); J = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
Q0 = QC.QCont(AB.strip_sigma(g, None, s_cut=SC), npt=120, npt0=512); ld0 = Q0.ld1
def qsad(nn, s):
    Qc = QC.QCont(AB.strip_sigma(g, s, s_cut=SC), npt=120, npt0=512); return (Qc.Q(nn, **KW) + nn * (Qc.ld1 - ld0).sum()).real
s_n, info = gap.solve(float(n), sig0=None, J=J); q = qsad(float(n), s_n); hb, ha = ref["honest"], ref["honest_a"]
qa = Q0.Q(float(n), **KW).real; dev_a = abs(qa - ha); tol = max(3 * dev_a, 1e-10); dev = abs(q - hb)
print(f"s_cut {SC}: qsad {q!r}  dev {dev:.4e}  dev_a {dev_a:.4e}  tol {tol:.3e}  gap |F| {info['F']:.1e}  ({time.time()-T0:.0f}s)", flush=True)
rec = dict(SC=SC, qsad=q, dev=dev, dev_signed=q - hb, dev_a=dev_a, tol=tol, gapF=info["F"])
if SC == 3.0:
    check("KA: s_cut 3 reproduces stored 084c W4P4 n=2 qsad bitwise", q == ref["qsad"], f"{q!r} vs {ref['qsad']!r}")
    check("KA: dev_a reproduces stored bitwise", dev_a == ref["dev_a"], f"{dev_a!r} vs {ref['dev_a']!r}")
else:
    qp = qsad(float(n), s_n * (1 + 1e-6)); rec["probe"] = abs(qp - hb)
    check("must-fire: probe sigma(1+1e-6) exceeds tol", rec["probe"] > tol, f"{rec['probe']:.3e} vs {tol:.2e}")
    check("PREDICTION 1: dev <= 3.1e-10 (084c's s_cut-3 tol)", dev <= 3.0756197588743817e-10, f"{dev:.4e}  (s_cut 3: {ref['dev']:.4e})")
    check("PREDICTION 2: dev <= max(3 dev_a', 1e-10) at s_cut 6", dev <= tol, f"{dev:.4e} vs {tol:.3e}")
rec["failed"] = FAIL; rec["sec"] = time.time() - T0
json.dump(rec, open(os.path.join(OUT, f"route2_W4P4_n2_scut{SC:g}.json"), "w"), indent=1)
sys.exit(1 if FAIL else 0)
