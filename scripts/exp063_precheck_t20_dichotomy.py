"""EXP-063 pre-check 1: reproduce Neon T20's outer-vector dichotomy with Cuspis's own EXP-060 kernel code (independent
implementation of the same kernel). F(v) = v^T (1 - lam^2 R^T R)^{-1} R^T v at u = 1 on a = 1/2 + iy, with
R(p,p') = e^{-(u/2)cosh p} e^{(a-1/2)(p-p')}/(2cosh((p-p')/2)) e^{-(u/2)cosh p'} (T20, = EXP-044's R~ with theta = 2a-1, t = u),
v0 = e^{-(u/2)cosh p}, v_a = e^{a p} v0, v_osc = e^{iyp} v0. Unconjugated bilinear forms (T20). [model: Opus 5.5]"""
import numpy as np, math
def mats(u, a, h=0.1):
    P = math.acosh(max(2.0, 90.0 / u)); p = np.arange(-P, P + 0.5 * h, h)
    E = np.exp(-0.5 * u * np.cosh(p)); dp = p[:, None] - p[None, :]
    R = np.exp((a - 0.5) * dp) * (E[:, None] * E[None, :]) / (2 * np.cosh(0.5 * dp))
    return p, h, R, E
for y in (0.0, 1.0, 2.0, 3.0, 3.5):
    a = 0.5 + 1j * y; lam2 = (np.sin(np.pi * a) / np.pi) ** 2
    p, h, R, E = mats(1.0, a); RT = R.T
    M = np.eye(len(p)) - lam2 * h * h * (RT @ R)
    row = []
    for name, v in (("v0", E), ("v_a", np.exp(a * p) * E), ("v_osc", np.exp(1j * y * p) * E)):
        x = np.linalg.solve(M, h * (RT @ v)); F = h * (v @ x)
        row.append(f"{name} {abs(F):.3e}")
    kmax = np.max(np.linalg.eigvals(lam2 * h * h * (R @ RT)).real)
    print(f"y={y}: 1-kappa_max {1-kmax:.2e}  |F|: " + "  ".join(row), flush=True)
