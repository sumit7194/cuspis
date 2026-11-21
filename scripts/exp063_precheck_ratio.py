"""EXP-063 pre-check 3: resummation ratio for C+ from the CH05 system (no outer vector).
dc/dL = -m^2 b u/(8 pi a(1-a)) (argued), b = beta m^{2a-1} bhat(t); C+ = (beta/(8 pi^2 a(1-a))) Int_0^inf s^{2a+1}/(2a+1) bhat u ds.
Ratio full/linear: rho = Int s^{2a+1} bhat u / Int s^{2a+1} bhat_lin u_lin (beta cancels).
u: ODE (52) [full] or u_lin = (2/pi) sin(pi a) K_{1-2a}(t) [linear]; H = t^2 h: H' = 2 t^2 u u' (H(inf)=0);
(ln b)' = [-(1-2a) u^2 + t u u' - 2 a h]/(t h) (CH05 (50)); bhat = b e^{t} t^{3/2} -> 1 as t -> inf (both). [model: Opus 5.5]"""
import sys, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from mpmath import mp, besselk, mpf, mpc, sin, pi as mpi
mp.dps = 30

def Kdata(a, t):
    a = mpc(a); f = lambda tt: (2 / mpi) * sin(a * mpi) * besselk(1 - 2 * a, tt)
    return float(mp.re(f(mpf(t)))), float(mp.re(mp.diff(f, mpf(t))))

def run(a, linear, t0=16.0, t1=1e-3):
    a = complex(a); s2 = ((a - 0.5) ** 2).real
    u0, du0 = Kdata(a, t0)
    H0 = -float(quad(lambda s: 2 * s * s * np.prod(Kdata(a, s)), t0, 70)[0])    # H(t0) = -Int_t0^inf 2 s^2 u u'
    def rhs(t, Y):
        u, v, H, lbr, lbi, Ir, Ii = Y
        if linear:
            upp = -v / t + u + 4 * u * s2 / (t * t)
        else:
            upp = -v / t + u / (1 + u * u) * v * v + u * (1 + u * u) + 4 * u * s2 / (t * t * (1 + u * u))
        h = H / (t * t)
        dlb = (-(1 - 2 * a) * u * u + t * u * v - 2 * a * h) / (t * h) + 1 + 1.5 / t      # d/dt ln(bhat)
        bh = np.exp(lbr + 1j * lbi)
        integrand = t ** (2 * a + 1) * bh * np.exp(-t) * t ** (-1.5) * u                 # s^{2a+1} b u  with b = bhat e^{-t} t^{-3/2}
        return [v, upp, 2 * t * t * u * v, dlb.real, dlb.imag, -integrand.real, -integrand.imag]
    # tail of Int_t0^inf s^{2a+1} b u ~ small (e^{-2 t0}); start at 0
    sol = solve_ivp(rhs, (t0, t1), [u0, du0, H0, 0.0, 0.0, 0.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-40, dense_output=True)
    return sol

if __name__ == "__main__":
    for a in [0.3] + [0.5 + 1j * y for y in (0.5, 1.0, 2.0, 3.0, 4.0)]:
        out = []
        for lin in (True, False):
            sol = run(a, lin); Y = sol.y[:, -1]
            out.append((Y[5] + 1j * Y[6], sol.status, sol.t[-1]))
        rho = out[1][0] / out[0][0]
        print(f"a={a}: I_lin {out[0][0]:.6e}  I_full {out[1][0]:.6e}  ratio {rho:.6f} |ratio| {abs(rho):.4e}  "
              f"(status {out[0][1]},{out[1][1]}; t_end {out[1][2]:.1e})", flush=True)
