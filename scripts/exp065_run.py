"""EXP-065 (pre-registered in report.md): stage C, growth of C+ on the CH07b line a = 1/2 + iy via the CH05 route.
Production: y = 0..5 step 0.25; nuisance ladder (t0, t1, rtol) in {(18,1e-7,1e-11), (14,1e-5,1e-11), (18,1e-7,1e-9)}.
Clauses: G1 rate of |C+| on [2,4] <= 2pi - 1; P planted L sin^2 rate on [3,4] within 1 of 2pi; T |C+lin| = |T23 closed form| to 1e-6;
N nuisance spread of |C+| <= 1e-5 relative. [model: Opus 5.5]"""
import sys, os, json
import numpy as np
from scipy.integrate import solve_ivp, quad
from mpmath import mp, mpc, gamma, sin, pi as mpi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp065_precheck_line import data
mp.dps = 30
def absC(y, linear, t0, t1, rtol):
    a = 0.5 + 1j * y; s2 = -y * y
    u0, du0 = data(a, t0); H0 = -float(quad(lambda s: 2 * s * s * np.prod(data(a, s)), t0, 80)[0])
    def rhs(t, Y):
        u, v, H, Ph, Ir, Ii = Y
        upp = (-v / t + u + 4 * u * s2 / (t * t)) if linear else (-v / t + u / (1 + u * u) * v * v + u * (1 + u * u) + 4 * u * s2 / (t * t * (1 + u * u)))
        h = H / (t * t); val = t ** (2 * a + 1) * np.sqrt(h) * np.exp(1j * Ph) * u
        return [v, upp, 2 * t * t * u * v, 2 * y * (u * u - h) / (t * h), -val.real, -val.imag]
    sol = solve_ivp(rhs, (t0, t1), [u0, du0, H0, 0.0, 0.0, 0.0], method="DOP853", rtol=rtol, atol=1e-40)
    return abs((sol.y[4, -1] + 1j * sol.y[5, -1]) / (8 * np.pi ** 2 * a * (1 - a) * (2 * a + 1)))
def t23(y):
    a = mpc(0.5, y); return float(abs(-(sin(mpi*a)/(4*mpi**3))*(gamma(a+0.5)/gamma(a+1))**2*gamma(3*a+0.5)*gamma(1.5-a)/gamma(2*a+2)))
if __name__ == "__main__":
    ys = np.round(np.arange(0, 5.01, 0.25), 2); lad = [(18.0, 1e-7, 1e-11), (14.0, 1e-5, 1e-11), (18.0, 1e-7, 1e-9)]
    F = {}; Lin = {}; okT = True; okN = True
    for y in ys:
        fs = [absC(y, False, *p) for p in lad]; l = absC(y, True, *lad[0]); F[y] = fs[0]; Lin[y] = l
        spread = max(abs(f / fs[0] - 1) for f in fs); okN &= spread <= 1e-5
        rt = l / t23(y) - 1; okT &= abs(rt) <= 1e-6
        print(f"y={y}: |C+| {fs[0]:.7e} (nuisance spread {spread:.1e})  |C+lin| {l:.7e}  vs T23 rel {rt:+.1e}  ratio {fs[0]/l:.4f}", flush=True)
    def rate(D, y0, y1): return np.log(D[y1] / D[y0]) / (y1 - y0)
    r = rate(F, 2.0, 4.0); rl = rate(Lin, 2.0, 4.0)
    sin2 = lambda y: abs(np.sin(np.pi * (0.5 + 1j * y))) ** 2
    rp = rate({k: F[k] * 5 * sin2(k) for k in F}, 3.0, 4.0)
    g1 = r <= 2 * np.pi - 1; p = abs(rp - 2 * np.pi) <= 1
    print(f"G1: rate of |C+| on [2,4] = {r:+.4f} (gate <= {2*np.pi-1:.4f}) [{'PASS' if g1 else 'FAIL'}];  linear-term rate {rl:+.4f}")
    print(f"P : planted rate on [3,4] = {rp:+.4f} (within 1 of 2pi) [{'PASS (fires)' if p else 'FAIL'}]")
    print(f"T : |C+lin| = |T23| to 1e-6 at all y [{'PASS' if okT else 'FAIL'}];  N: nuisance spread <= 1e-5 [{'PASS' if okN else 'FAIL'}]")
    json.dump(dict(F={str(k): v for k, v in F.items()}, Lin={str(k): v for k, v in Lin.items()}, rate=r, rate_lin=rl, planted=rp,
                   G1=bool(g1), P=bool(p), T=bool(okT), N=bool(okN)), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp065_results.json"), "w"), indent=1)
