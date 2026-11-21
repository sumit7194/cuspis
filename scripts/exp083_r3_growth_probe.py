"""R3 Tier-1 growth probe (no verdict): |Q_cont(n)| along n = c + i t (c = 1, 1.5, 3; t = 0..20) for
(i) the P4' 6x4 stand-in via sigma_engine route (ii) (verified known-good, EXP-079) and (ii) Strip3D W2P2 (exp083_r3_qcont).
Reports log|Q_cont|/t and smoothness under t-grid refinement (branch-jump detection). [model: Opus 5.5]"""
import time, numpy as np, sigma3d as S3, sigma_engine as E
from exp083_honest import Geom
from exp083_r3_qcont import QCont
T0 = time.time()
L = E.Lattice(6, 4, 0.5, cut_links=[(2, 1), (3, 1)])          # the EXP-079 P4' stand-in, as constructed there
g = Geom(2, 2); Qc = QCont(S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0))
for name, F in (("P4' (route ii, known-good)", lambda n: E.lattice_Qcont_route_ii(L, n)), ("Strip3D W2P2 (route ii port)", lambda n: Qc.Q(n))):
    for c in (1.0, 1.5, 3.0):
        row = []
        for t in (0.0, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20.0):
            try: q = F(complex(c, t)); row.append(f"t={t:g}: |Q| {abs(q):.3e} log|Q|/t {np.log(abs(q))/t if t else float('nan'):+.3f}")
            except Exception as e: row.append(f"t={t:g}: FAIL {type(e).__name__}")
        print(f"{name} Re n={c}: " + " | ".join(row) + f"  ({time.time()-T0:.0f}s)", flush=True)
