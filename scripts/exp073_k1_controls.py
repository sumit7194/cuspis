"""EXP-073(b) controls, run ALONE before registration (no lattice-vs-CFH comparison is printed here). [model: Opus 5.5]
C1 identity: log det(I - K_free) [TGTG, untruncated supports] == four-LU connected log det, and interior-cut gauge == exterior.
C2 no twist (a = 0): K_free = 0 and D2 = 0.
C3 CFH quadrature ladder (h, P) for the top-3 eigenvalues.
C4 planted non-isospectral kernel: CFH with t -> 1.1 t; size of the shift it produces (sets the resolution the test needs).
Timing at production sizes (flat-lattice LU only)."""
import time, numpy as np, scipy.sparse.linalg as spla
from exp073_k1 import Kfree, D2_direct, cfh_eigs, top, lattice
for a in (0.3, 0.5 + 0.5j):
    for W, t in ((6, 1.0), (5, 2.0)):
        Ks, info = Kfree(W, t, a, pad_over_m=4.0, D_over_m=1e9)
        sgn_ld = np.sum(np.log(np.linalg.eigvals(np.eye(len(Ks)) - Ks)))
        d2, gauge = D2_direct(W, t, a, pad_over_m=4.0)
        wrap = lambda z: complex(z.real, (z.imag + np.pi) % (2 * np.pi) - np.pi)
        print(f"C1 a={a} W={W} t={t} N={info['N']} |P|={info['P']}: logdet(I-K)={complex(sgn_ld):+.12e}  four-LU={complex(d2):+.12e}  "
              f"diff {abs(wrap(sgn_ld - d2)):.1e}   gauge int-can {abs(wrap(gauge)):.1e}", flush=True)
Ks, _ = Kfree(6, 1.0, 0.0, pad_over_m=4.0, D_over_m=1e9); d2, _ = D2_direct(6, 1.0, 0.0, pad_over_m=4.0)
print(f"C2 a=0: max|K|={np.abs(Ks).max():.1e}  D2={abs(d2):.1e}", flush=True)
for a in (0.3, 0.5 + 0.5j):
    for t in (1.0, 2.0):
        e0 = top(cfh_eigs(t, a)); e1 = top(cfh_eigs(t, a, h=0.05)); e2 = top(cfh_eigs(t, a, h=0.05, P=np.arccosh(max(2.0, 90.0 / t)) + 2))
        ep = top(cfh_eigs(t, a, h=0.05, scale_t=1.1))
        print(f"C3 a={a} t={t}: ladder rel {np.max(np.abs(e1/e0-1)):.1e}, {np.max(np.abs(e2/e1-1)):.1e}   "
              f"C4 planted t*1.1 shifts top-3 by rel {np.round(np.abs(ep/e1-1), 3)}", flush=True)
for W, t in ((32, 1.0), (64, 2.0)):
    t0 = time.time(); g = lattice(W, t, 8.0, 0.3, 'e1'); t1 = time.time(); spla.splu(g['H'], permc_spec="COLAMD"); t2 = time.time()
    print(f"timing W={W} t={t}: N={g['H'].shape[0]} build {t1-t0:.1f}s  LU {t2-t1:.1f}s", flush=True)
