"""EXP-071 pre-check: (1) C_line sign/normalisation against the exact n->1 limit for g = cos(beta(a - 1/2)) (EXP-044 C0: the scalar
form -1/2 Int (pi/cosh^2) cosh(beta s) = lim (1/(2(1-n))) sum_{k=1}^{n-1} g(k/n)), so C[g] = d/dn sum |_1 = +Int (pi/cosh^2) g(1/2+is)?
(2) kappa_free from C_line applied to Fredholm w_S, with the real-scalar factor 1/2: c_S(t) = -(1/2) C[w_S(t, .)] ... vs EXP-044 c_vn,
then kappa = pref(3) * Int c dt (EXP-040 Impl-1 prefactor, via exp044 moment); ladder in ns, smax, t-grid. [model: Opus 5.5]"""
import sys, os, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp071_sc import C_line
import exp044_det as X
for b in (1.0, 3.0):
    g = lambda a: np.cos(b * (a - 0.5))
    exact = -b / (4 * math.sin(b / 2))                 # = lim (1/(2(1-n))) sum_{k=1}^{n-1} g(k/n)   (EXP-044 C0, verified)
    # => d/dn sum_{k=1}^{n-1} g(k/n) at n=1 = -2 * exact  (sum vanishes at n=1)
    cl = C_line(lambda a: complex(g(a)).real)
    print(f"(1) beta={b}: C_line[g] = {cl:.12f}   d/dn sum|_1 = -2*exact = {-2*exact:.12f}   rel {cl/(-2*exact)-1:+.1e}", flush=True)
# (2) c_S via my C_line vs EXP-044 c_vn
for t in (0.3, 1.0, 3.0):
    mine = -0.5 * C_line(lambda a: complex(X.w_scalar(t, a)[0]).real)
    ref = X.c_vn("S", t)
    print(f"(2) t={t}: -1/2 C_line[w_S] = {mine:.10f}   EXP-044 c_vn = {ref:.10f}   rel {mine/ref-1:+.1e}", flush=True)
