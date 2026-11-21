"""EXP-064 pre-check: absolute C+ at a = 1/2 from the CH05 route. At a = 1/2 the b- and c-equations (CH05 (49),(50)) coincide,
and the y -> -y reflection (which maps a -> 1-a, fixing 1/2) gives C+ = C- hence b = c = +-sqrt(h): the scale symmetry
b -> lam b, c -> c/lam is fixed. Sign chosen so that C+ < 0 (not a prediction). Absolute formula (argued; sign of the
reflection step verified by the CFT cross check): C+ = (1/(8 pi^2 a(1-a)(2a+1))) Int_0^inf s^{2a+1} b u ds.
Compared with the Born closed form -1/(8 pi^3) (T17/T20 form, Neon; my implementation of its integral reproduced it at a=0.3). [model: Opus 5.5]"""
import sys, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from mpmath import mp, besselk, mpf, pi as mpi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mp.dps = 30
a = 0.5
def data(t):
    f = lambda tt: (2 / mpi) * besselk(0, tt)          # (2/pi) sin(pi/2) K_0
    return float(f(mpf(t))), float(mp.diff(f, mpf(t)))
def run(linear, t0=18.0, t1=1e-7):
    u0, du0 = data(t0); H0 = -float(quad(lambda s: 2 * s * s * np.prod(data(s)), t0, 80)[0])
    def rhs(t, Y):
        u, v, H, I = Y
        upp = (-v / t + u) if linear else (-v / t + u / (1 + u * u) * v * v + u * (1 + u * u))
        h = H / (t * t); b = -np.sqrt(h)
        return [v, upp, 2 * t * t * u * v, -t ** (2 * a + 1) * b * u]
    tail = 0.0
    sol = solve_ivp(rhs, (t0, t1), [u0, du0, H0, tail], method="DOP853", rtol=1e-12, atol=1e-40)
    return sol.y[3, -1]
pref = 1 / (8 * np.pi ** 2 * a * (1 - a) * (2 * a + 1))
for t1 in (1e-5, 1e-7):
    Il = run(True, t1=t1); If = run(False, t1=t1)
    print(f"t1={t1:g}: C+lin(1/2) = {pref*Il:+.8f}   C+full(1/2) = {pref*If:+.8f}   ratio {If/Il:.6f}   Born closed form -1/(8 pi^3) = {-1/(8*np.pi**3):+.8f}   lin/Born {pref*Il/(-1/(8*np.pi**3)):.6f}")
