"""EXP-044 (pre-registered in report.md, d669fbd): lattice-free von Neumann c-functions from the Fredholm determinant
det(1 - lam^2 R R^T) (CFH05 (58)-(60)) and the n -> 1 continuation (CH07b (42); scalar weight derived in the
registration). Nystrom/trapezoid quadrature in p = ln u (Born10). [model: Opus 5.5]
Usage: python exp044_det.py tier1 | gates | run"""
import sys, math, time, json, os
import numpy as np
from scipy.integrate import quad
from scipy.special import k1

D0 = os.path.dirname(os.path.abspath(__file__))

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

# ---------------- determinant ----------------
def w_det(t, theta, lam2, sign, h=0.1, P=None):
    """w = sign * t d/dt log det(1 - lam2 * R R^T); returns (w, det, roundoff_floor, m)."""
    if P is None:
        P = math.acosh(max(2.0, 90.0 / t))
    p = np.arange(-P, P + 0.5 * h, h)
    ch = np.cosh(p); E = np.exp(-0.5 * t * ch)
    dp = p[:, None] - p[None, :]
    R = np.exp(0.5 * theta * dp) * (E[:, None] * E[None, :]) / (2.0 * np.cosh(0.5 * dp))
    dR = -0.5 * (ch[:, None] + ch[None, :]) * R
    RT = R.T
    A = h * h * (R @ RT)
    dA = h * h * (dR @ RT + R @ dR.T)
    M = np.eye(len(p)) - lam2 * A
    sgn, ld = np.linalg.slogdet(M)
    dlog = -lam2 * np.trace(np.linalg.solve(M, dA))
    detv = sgn * np.exp(ld)
    floor = math.sqrt(len(p)) * np.linalg.norm(lam2 * A) * 2.0 ** -53 / max(abs(detv), 1e-300)
    return sign * t * dlog, detv, floor, len(p)

def w_dirac(t, a, **kw):          # a may be complex; theta = 2a, lam^2 = -sin^2(pi a)/pi^2
    return w_det(t, 2 * a, -np.sin(np.pi * a) ** 2 / np.pi ** 2, +1, **kw)

def w_scalar(t, a, **kw):         # theta = 2a - 1, lam^2 = sin^2(pi a)/pi^2, Z = 1/<V V>
    return w_det(t, 2 * a - 1, np.sin(np.pi * a) ** 2 / np.pi ** 2, -1, **kw)

# ---------------- C0: continuation identities ----------------
def C0():
    ok = True
    for b in (1.0, 3.0, 5.0):
        exact = 1 - (b / 2) / math.tan(b / 2)
        def fD(s):                # pi (cosh(bs) - 1)/sinh^2(pi s), overflow-safe: 4 pi (cosh bs - 1) e^{-2 pi s}/(1 - e^{-2 pi s})^2
            if s < 1e-6: return b * b / (2 * math.pi)
            q = math.exp(-2 * math.pi * s)
            return 2 * math.pi * (math.exp((b - 2 * math.pi) * s) + math.exp(-(b + 2 * math.pi) * s) - 2 * q) / (1 - q) ** 2
        num = quad(fD, 0, 60, limit=400, epsabs=1e-15, epsrel=1e-13)[0]
        r = abs(num - exact); ok &= r < 1e-10
        log(f"C0 Dirac beta={b}: integral {num:.15f}  n->1 limit {exact:.15f}  diff {r:.1e} [{'PASS' if r < 1e-10 else 'FAIL'}]")
        exact_s = -b / (4 * math.sin(b / 2))
        def fS(s):                # pi cosh(bs)/cosh^2(pi s) = 2 pi (e^{(b-2pi)s} + e^{-(b+2pi)s})/(1 + e^{-2pi s})^2
            q = math.exp(-2 * math.pi * s)
            return 2 * math.pi * (math.exp((b - 2 * math.pi) * s) + math.exp(-(b + 2 * math.pi) * s)) / (1 + q) ** 2
        num_s = -0.5 * quad(fS, 0, 60, limit=400, epsabs=1e-15, epsrel=1e-13)[0]
        # independent check of the closed-form limit: finite-difference in n of the integer-n Dirichlet sum, continued in n
        G = lambda n: math.sin(b * (n - 1) / (2 * n)) / math.sin(b / (2 * n)) / (2 * (1 - n))
        fd = (G(1 + 1e-5) + G(1 - 1e-5)) / 2
        r2 = abs(num_s - exact_s); ok &= r2 < 1e-10
        log(f"C0 scalar beta={b}: -1/2 integral {num_s:.15f}  n->1 limit {exact_s:.15f} (finite-n check {fd:.10f})  diff {r2:.1e} [{'PASS' if r2 < 1e-10 else 'FAIL'}]")
    return ok

def tier1():
    log("EXP-044 Tier 1"); C0()
    for t in (1e-3, 0.3, 3.0):
        for s in (0.0, 0.5, 2.0):
            t0 = time.time(); wD, dD, fD, m = w_dirac(t, 1j * s); el = time.time() - t0
            wS, dS, fS, _ = w_scalar(t, 0.5 + 1j * s)
            log(f"  t={t} s={s}: m={m}  w_D={complex(wD):.10f} (massless 2s^2={2*s*s:.4f}) det_D={complex(dD):.6e} floor {fD:.1e} | "
                f"w_S={complex(wS):.10f} (massless -1/2-2s^2={-0.5-2*s*s:.4f}) det_S={complex(dS):.6e} floor {fS:.1e}  [{el*1e3:.0f} ms]")

if __name__ == "__main__":
    {"tier1": tier1}[sys.argv[1]]()
