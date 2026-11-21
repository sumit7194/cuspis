"""EXP-068: check of Neon T27 (gap (I) of T26: kappa_max < 1 on the CH07b line; external, unverified).
(1) Step 1: -dR^T/du = (1/4)(w_R w_R^dag + v_R v_R^dag) >= 0 numerically (fixed grid; min eigenvalue of the Hermitian FD matrix).
(2) Step 3 symbol identity cosh(pi(w-y))cosh(pi(w+y)) = cosh^2(pi y) + sinh^2(pi w), and the resulting sup = 1.
(3) Step 2 corollary: kappa_max decreases in u (from the Hermitian form R^{T 1/2} R R^{T 1/2}).
(4) B(4) via the Hermitian eigenvalue route -sum log(1 - kappa_j) (avoids the non-Hermitian slogdet near kappa -> 1),
    compared with my EXP-067 value 6.78e-2 and T27's 6.871e-2. [model: Opus 5.5]"""
import numpy as np, math
from scipy.linalg import sqrtm, eigh
def Rmat(p, u, y):
    E = np.exp(-0.5 * u * np.cosh(p)); dp = p[:, None] - p[None, :]
    return (E[:, None] * E[None, :]) * np.exp(1j * y * dp) / (2 * np.cosh(0.5 * dp))
p = np.arange(-7.0, 7.0001, 0.1); h = 0.1
for y in (1.0, 3.0):
    du = 1e-5; M = -(Rmat(p, 1.0 + du, y).T - Rmat(p, 1.0 - du, y).T) / (2 * du)
    Mh = 0.5 * (M + M.conj().T)
    print(f"(1) y={y}: min eig of -dR^T/du (Hermitian part) = {np.linalg.eigvalsh(h*Mh).min():+.2e}; anti-Hermitian part {np.abs(M - M.conj().T).max():.1e}")
ws = np.linspace(-5, 5, 2001)
for y in (0.5, 2.0, 4.0):
    lhs = np.cosh(np.pi * (ws - y)) * np.cosh(np.pi * (ws + y)); rhs = np.cosh(np.pi * y) ** 2 + np.sinh(np.pi * ws) ** 2
    sym = (np.cosh(np.pi * y) / np.pi) ** 2 * np.pi ** 2 / rhs
    print(f"(2) y={y}: identity max rel err {np.max(np.abs(lhs/rhs-1)):.1e}; sup of lam^2 x symbol product = {sym.max():.15f}")
def kappas_herm(u, y, h=0.1, Pextra=1.0):
    P = math.acosh(max(2.0, 90.0 / u)) + Pextra; pp = np.arange(-P, P + 0.5 * h, h)
    R = h * Rmat(pp, u, y); RT = R.T
    ev, V = eigh(RT); ev = np.clip(ev, 0, None); S = (V * np.sqrt(ev)) @ V.conj().T   # RT^{1/2} (RT Hermitian PSD)
    Hm = S @ R @ S; Hm = 0.5 * (Hm + Hm.conj().T)
    lam2 = (np.cosh(np.pi * y) / np.pi) ** 2
    return lam2 * np.linalg.eigvalsh(Hm)
for y in (2.0,):
    print("(3) y=2: kappa_max at u = 0.1, 0.3, 1, 3:", " ".join(f"{kappas_herm(u, y).max():.10f}" for u in (0.1, 0.3, 1.0, 3.0)))
y = 4.0
for h, Pe in ((0.1, 1.0), (0.05, 1.0), (0.1, 3.0)):
    qs = np.linspace(-9.0, math.log(np.pi * y + 12), 400); us = np.exp(qs); f = []
    for u in us:
        k = kappas_herm(u, y, h, Pe); k = k[k > 0]
        f.append(-np.sum(np.log1p(-np.minimum(k, 1 - 1e-300))) * u)
    f = np.array(f); I = np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(qs))
    print(f"(4) y=4 h={h} Pextra={Pe}: B(4) Hermitian route = {I/(8*np.pi**2*(0.25+16)):.5e}  (EXP-067 slogdet 6.78e-2; T27 6.871e-2)", flush=True)
