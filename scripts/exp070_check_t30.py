"""EXP-070: check of Neon T30 (gap II; external, unverified) and of T26's Step-5 Parseval bound it rests on.
(a) |K_{iw}(u)| <= e * e^{-pi|w|/2} * K0(2u/(pi(1+|w|))) on a grid (mpmath, imaginary order).
(b) Parseval: Tr B_u = (2cosh^2(pi y)/pi^2) Int dw K_{iw}(u)^2 (w-2y)/sinh(pi(w-2y)) vs the direct matrix trace lam^2 h^2 Tr(R^T R).
(c) Bound shape: Tr B_u / [(1+|y|)^2 (1 + ln+(1/u) + ln(1+|y|))^2] bounded over u in [1e-4, 10], y in [0, 6] (report the max = C1 estimate).
(d) T30 margin m(u,y) = 1/(30000 L^2 e^{2pi|y|} cosh^2(pi y)), L = arccosh((2pi|y|+10)/u), below 1 - kappa_max where double precision
    resolves it (1 - kappa >= 1e-9). [model: Opus 5.5]"""
import numpy as np, math
from mpmath import mp, besselk, mpf, mpc, quad, sinh, cosh, pi, e as E_, inf
mp.dps = 30
worst = 0
for u in (1e-3, 1e-2, 0.1, 1.0, 5.0):
    for w in (0.0, 0.5, 1, 2, 5, 10, 20, 40):
        lhs = abs(besselk(mpc(0, w), u)); rhs = E_ * mp.exp(-pi * w / 2) * besselk(0, 2 * u / (pi * (1 + w)))
        worst = max(worst, float(lhs / rhs))
print(f"(a) max |K_iw(u)| / bound over the grid = {worst:.4f}  [{'holds' if worst <= 1 else 'VIOLATED'}]", flush=True)
def trB_parseval(u, y):
    f = lambda w: besselk(mpc(0, w), u).real ** 2 * ((w - 2 * y) / sinh(pi * (w - 2 * y)) if abs(w - 2 * y) > 1e-12 else 1 / pi)
    return float(2 * cosh(pi * y) ** 2 / pi ** 2 * quad(f, [-inf, 2 * y - 5, 2 * y, 2 * y + 5, inf]))
def trB_direct(u, y, h=0.05):
    P = math.acosh(max(2.0, 90.0 / u)) + 2.0; p = np.arange(-P, P + 0.5 * h, h)
    E = np.exp(-0.5 * u * np.cosh(p)); dp = p[:, None] - p[None, :]
    R = (E[:, None] * E[None, :]) * np.exp(1j * y * dp) / (2 * np.cosh(0.5 * dp)); lam2 = (np.cosh(np.pi * y) / np.pi) ** 2
    return float((lam2 * h * h * np.trace(R.T @ R)).real)
for u, y in ((1.0, 0.0), (1.0, 2.0), (0.1, 1.0), (3.0, 3.0)):
    a, b = trB_parseval(u, y), trB_direct(u, y)
    print(f"(b) u={u} y={y}: Parseval {a:.10e}  direct {b:.10e}  rel {a/b-1:+.1e}", flush=True)
mx = 0; arg = None
for y in (0, 1, 2, 3, 4, 6):
    for u in (1e-4, 1e-3, 1e-2, 0.1, 0.5, 1, 3, 10):
        t = trB_parseval(u, y); norm = (1 + y) ** 2 * (1 + max(0, math.log(1 / u)) + math.log(1 + y)) ** 2
        if t / norm > mx: mx, arg = t / norm, (u, y)
print(f"(c) max Tr B_u / [(1+|y|)^2 (1 + ln+(1/u) + ln(1+|y|))^2] = {mx:.4f} at (u, y) = {arg}  (bounded => C1 ~ this)", flush=True)
def kmax(u, y, h=0.1):
    P = math.acosh(max(2.0, 90.0 / u)) + 1.0; p = np.arange(-P, P + 0.5 * h, h)
    E = np.exp(-0.5 * u * np.cosh(p)); dp = p[:, None] - p[None, :]
    R = (E[:, None] * E[None, :]) * np.exp(1j * y * dp) / (2 * np.cosh(0.5 * dp)); lam2 = (np.cosh(np.pi * y) / np.pi) ** 2
    return np.max(np.linalg.eigvals(lam2 * h * h * (R.T @ R)).real)
for u, y in ((1.0, 1.0), (1.0, 2.0), (3.0, 2.0), (3.0, 3.0), (0.3, 1.0)):
    g = 1 - kmax(u, y); L = math.acosh((2 * math.pi * y + 10) / u)
    m = 1 / (30000 * L ** 2 * math.exp(2 * math.pi * y) * math.cosh(math.pi * y) ** 2)
    print(f"(d) u={u} y={y}: 1-kappa_max = {g:.3e}  T30 margin m = {m:.3e}  [{'m <= gap' if m <= g else 'VIOLATED'}]", flush=True)
