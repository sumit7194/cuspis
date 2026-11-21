"""EXP-065 pre-check (stage C, CH05 route): |C+| on the CH07b line a = 1/2 + iy, linear and full.
On the line 1-a = conj(a); (ln b)'(a) + (ln b)'(conj a) = (ln h)' exactly (from CH05 (50),(51)), and C-symmetry gives
b(a) b(1-a) = h, so |b| = sqrt(h), b = sqrt(h) e^{i Phi}, Phi' = 2y(u^2 - h)/(t h); a constant phase drops out of |C+|.
|C+| = |pref Int_0^inf s^{2a+1} b u ds|, pref = 1/(8 pi^2 a(1-a)(2a+1)) (same convention factor as at a = 1/2, y-independent).
Rates: local d ln|C+|/dy. Planted control: x L sin^2(pi a) (L = 5) must add 2 pi to the rate. [model: Opus 5.5]"""
import sys, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from mpmath import mp, besselk, mpf, mpc, sin, pi as mpi
mp.dps = 30
def data(a, t):
    a = mpc(a); f = lambda tt: (2 / mpi) * sin(a * mpi) * besselk(1 - 2 * a, tt)
    return float(mp.re(f(mpf(t)))), float(mp.re(mp.diff(f, mpf(t))))
def absC(y, linear, t0=18.0, t1=1e-7):
    a = 0.5 + 1j * y; s2 = -y * y
    u0, du0 = data(a, t0); H0 = -float(quad(lambda s: 2 * s * s * np.prod(data(a, s)), t0, 80)[0])
    def rhs(t, Y):
        u, v, H, Ph, Ir, Ii = Y
        upp = (-v / t + u + 4 * u * s2 / (t * t)) if linear else (-v / t + u / (1 + u * u) * v * v + u * (1 + u * u) + 4 * u * s2 / (t * t * (1 + u * u)))
        h = H / (t * t); dPh = 2 * y * (u * u - h) / (t * h)
        val = t ** (2 * a + 1) * np.sqrt(h) * np.exp(1j * Ph) * u
        return [v, upp, 2 * t * t * u * v, dPh, -val.real, -val.imag]
    sol = solve_ivp(rhs, (t0, t1), [u0, du0, H0, 0.0, 0.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-40)
    I = sol.y[4, -1] + 1j * sol.y[5, -1]
    pref = 1 / (8 * np.pi ** 2 * a * (1 - a) * (2 * a + 1))
    return abs(pref * I), sol.status
if __name__ == "__main__":
    ys = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    L = []; F = []
    for y in ys:
        l, s1 = absC(y, True); f, s2 = absC(y, False); L.append(l); F.append(f)
        planted = f * 5 * abs(np.sin(np.pi * (0.5 + 1j * y))) ** 2
        print(f"y={y}: |C+lin| {l:.6e}  |C+| {f:.6e}  |ratio| {f/l:.4f}  planted |C+|*5|sin^2| {planted:.4e}  (status {s1},{s2})", flush=True)
    L = np.array(L); F = np.array(F); ys = np.array(ys)
    for i in range(1, len(ys)):
        dy = ys[i] - ys[i - 1]
        print(f"  y {ys[i-1]}->{ys[i]}: rate lin {np.log(L[i]/L[i-1])/dy:+.3f}  full {np.log(F[i]/F[i-1])/dy:+.3f}  "
              f"planted {np.log(F[i]/F[i-1])/dy + np.log(abs(np.sin(np.pi*(0.5+1j*ys[i])))**2/abs(np.sin(np.pi*(0.5+1j*ys[i-1])))**2)/dy:+.3f}")
