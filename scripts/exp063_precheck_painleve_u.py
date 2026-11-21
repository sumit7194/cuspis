"""EXP-063 pre-check 2: CH05 Painleve-type ODE (52) for u(t), integrated inward from the Bessel boundary data (79),
u ~ (2/pi) sin(a pi) K_{1-2a}(t); w(t) = -Int_t^inf y u^2 dy (CH05 (81)). Two-implementation control: w from u vs
EXP-044's Fredholm w_S(t, a) = -t d/dt log det(1 - lam^2 R R^T). On a = 1/2 + iy the ODE and data are real
((a-1/2)^2 = -y^2, sin(pi a) = cosh(pi y), K_{2iy}(t) real). [model: Opus 5.5]"""
import sys, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from mpmath import mp, besselk, mpf, mpc, cosh, pi as mpi, sin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp044_det import w_scalar
mp.dps = 30

def bc(a, t):
    a = mpc(a); nu = 1 - 2 * a
    f = lambda tt: (2 / mpi) * sin(a * mpi) * besselk(nu, tt)
    v = f(mpf(t)); d = mp.diff(f, mpf(t))
    return float(mp.re(v)), float(mp.re(d)), abs(complex(mp.im(v))) + abs(complex(mp.im(d)))

def solve_u(a, t0=14.0, t1=0.02):
    s = ((complex(a) - 0.5) ** 2).real           # real on Re a = 1/2 and for real a
    u0, du0, imag = bc(a, t0)
    def rhs(t, Y):
        u, v, W = Y
        upp = -v / t + u / (1 + u * u) * v * v + u * (1 + u * u) + 4 * u * s / (t * t * (1 + u * u))
        return [v, upp, t * u * u]                 # W' = t u^2  =>  w(t) = -Int_t^inf y u^2 = W(t) - W(inf) with W(t0) = tail
    tail0 = float(quad(lambda y: y * bc(a, y)[0] ** 2, t0, 60)[0])
    sol = solve_ivp(rhs, (t0, t1), [u0, du0, -tail0], method="DOP853", rtol=1e-12, atol=1e-30, dense_output=True)
    return sol, imag

if __name__ == "__main__":
    for a in (0.3, 0.5 + 0.5j, 0.5 + 1.0j, 0.5 + 2.0j):
        sol, imag = solve_u(a)
        print(f"a={a}: imag part of boundary data {imag:.1e}", flush=True)
        for t in (3.0, 1.0, 0.3, 0.1):
            w_ode = sol.sol(t)[2]                   # W(t) = -Int_t^inf y u^2 (W(t0) = -tail, W' = t u^2)
            w_det = w_scalar(t, a)[0]
            print(f"   t={t}: w (Painleve u) {w_ode:+.10f}   w_S (Fredholm, EXP-044) {complex(w_det).real:+.10f}   diff {w_ode-complex(w_det).real:+.1e}", flush=True)
