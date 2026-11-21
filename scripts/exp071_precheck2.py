"""EXP-071 pre-check 2: (a) kappa_free/C_T from -1/2 C_line[w_S] on a log-t grid with EXP-044's tails and EXP-040 prefactor
(exp044_det.ratio('S', 3, U, C)); ladder in grid size nt and C_line (ns, smax). (b) BIE coincident trace at one complex point:
w_S^BIE(t, a) = 2 m^2 Int d^2x [G_a(x,x) - G_0(x,x)] (CH05 eq. (7) with w = t d/dt log Z, m = 1, t = w_len) vs Fredholm w_S. [model: Opus 5.5]"""
import sys, os, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp071_sc import C_line
import exp044_det as X
t0 = time.time()
for nt, ns, smax in ((60, 60, 6.0), (120, 60, 6.0), (120, 90, 7.0)):
    U = np.linspace(math.log(1e-3), math.log(6.0), nt)
    C = np.array([-0.5 * C_line(lambda a: complex(X.w_scalar(math.exp(u), a)[0]).real, smax=smax, ns=ns) for u in U])
    r = X.ratio("S", 3.0, U, C)
    print(f"(a) nt={nt} ns={ns} smax={smax}: kappa/C_T = {r:.6f}  kappa = {r*3/(32*math.pi**2):.7f}   [{time.time()-t0:.0f}s]", flush=True)
