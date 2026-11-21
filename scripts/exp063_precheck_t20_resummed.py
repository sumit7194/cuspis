"""EXP-063 pre-check 4: T20's resummed C+ formula in Cuspis's own code at real alpha (outer vectors v0, v_alpha),
C+ = -(lam/(4 pi^2 Gamma(1+a)^2)) Int dq e^q (e^q/2)^{2a} v^T (1 - lam^2 R^T R)^{-1} R^T v,  u = e^q.
Gate: Born (v0, no resolvent) must reproduce T20/T17's closed form C+^Born(0.3) = -0.0064736 (Neon, unverified) to 1e-4.
Compare resummed values with the CH05 ratio route: 1.162062 x Born. [model: Opus 5.5]"""
import numpy as np, math
from scipy.special import gamma
def F(u, a, vec, resum, h=0.1):
    P = math.acosh(max(2.0, 90.0 / u)); p = np.arange(-P, P + 0.5 * h, h)
    E = np.exp(-0.5 * u * np.cosh(p)); dp = p[:, None] - p[None, :]
    R = np.exp((a - 0.5) * dp) * (E[:, None] * E[None, :]) / (2 * np.cosh(0.5 * dp))
    v = E if vec == "v0" else np.exp(a * p) * E
    lam2 = (np.sin(np.pi * a) / np.pi) ** 2
    y = h * (R.T @ v)
    if resum: y = np.linalg.solve(np.eye(len(p)) - lam2 * h * h * (R.T @ R), y)
    return h * (v @ y)
def Cplus(a, vec, resum):
    lam = np.sin(np.pi * a) / np.pi
    qs = np.linspace(-9, 3.5, 251); dq = qs[1] - qs[0]
    f = np.array([np.exp(q) * (np.exp(q) / 2) ** (2 * a) * F(np.exp(q), a, vec, resum) for q in qs])
    integ = dq * (f.sum() - 0.5 * (f[0] + f[-1]))
    return -lam / (4 * np.pi ** 2 * gamma(1 + a) ** 2) * integ
a = 0.3
born = Cplus(a, "v0", False)
print(f"Born (v0, no resolvent) at a=0.3: {born:.7f}   T17/T20 closed form -0.0064736   rel {born/-0.0064736-1:+.1e}")
for vec in ("v0", "v_a"):
    r = Cplus(a, vec, True)
    print(f"resummed with {vec}: {r:.7f}   ratio to Born {r/born:.6f}")
print(f"CH05 ratio route: ratio 1.162062 -> C+ = {1.162062*born:.7f}")
