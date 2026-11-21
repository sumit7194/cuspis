"""EXP-060 pre-check (unregistered characterisation, run BEFORE the registration): can the EXP-044 Fredholm
determinant det(1 - lam^2 R R^T), scalar convention (theta = 2a-1, lam^2 = sin^2(pi a)/pi^2), show zeros?
Line Re a = 1/2 (claim: none) vs line Re a = 0 (mechanism predicts zeros). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
from exp044_det import w_det

def det(t, a, h=0.1):
    _, d, fl, m = w_det(t, 2 * a - 1, np.sin(np.pi * a) ** 2 / np.pi ** 2, -1, h=h)
    return complex(d), fl, m

if __name__ == "__main__":
    ys = np.arange(0.0, 4.01, 0.25)
    for t in (0.03, 0.3, 1.0, 3.0):
        for re in (0.5, 0.0):
            row = []
            for y in ys:
                d, fl, m = det(t, re + 1j * y); row.append(d)
            row = np.array(row)
            sc = int(np.sum(np.diff(np.sign(row.real)) != 0))
            print(f"t={t} Re a={re}: m={m} min|det|={np.abs(row).min():.3e} max|Im/det|={np.max(np.abs(row.imag)/np.abs(row)):.1e} "
                  f"sign changes of Re det along y: {sc}", flush=True)
            print("   Re det:", " ".join(f"{v.real:+.3e}" for v in row[::2]), flush=True)
    # discretisation check at one point per line
    for re in (0.5, 0.0):
        a = re + 2.0j
        d1, _, _ = det(0.3, a, 0.1); d2, _, _ = det(0.3, a, 0.05)
        print(f"h-halving t=0.3 a={a}: {d1:.10e} vs {d2:.10e} rel {abs(d1/d2-1):.1e}", flush=True)

# ---- pre-check 2 (added before registration): eigenvalues of lam^2 A on Re a = 1/2, and the detector control ----
def kappas(t, a, h=0.1, Pextra=0.0, scale=1.0):
    import math
    P = math.acosh(max(2.0, 90.0 / t)) + Pextra; p = np.arange(-P, P + 0.5 * h, h)
    ch = np.cosh(p); E = np.exp(-0.5 * t * ch); dp = p[:, None] - p[None, :]
    th = 2 * a - 1
    R = np.exp(0.5 * th * dp) * (E[:, None] * E[None, :]) / (2.0 * np.cosh(0.5 * dp))
    lam2 = np.sin(np.pi * a) ** 2 / np.pi ** 2
    ev = np.linalg.eigvals(scale * lam2 * h * h * (R @ R.T))
    return ev[np.argsort(-ev.real)]

if __name__ == "__main__":
    print("--- pre-check 2 ---")
    for t in (0.3, 1.0):
        for y in (1.0, 2.0, 3.0):
            k1 = kappas(t, 0.5 + 1j * y); k2 = kappas(t, 0.5 + 1j * y, h=0.05, Pextra=2.0)
            print(f"t={t} y={y}: 1-kmax {1-k1[0].real:.6e} (h/2,P+2: {1-k2[0].real:.6e})  max|Im k| {np.abs(k1.imag).max():.1e}  "
                  f"min Re k {k1.real.min():.1e}  #k>0.99: {int(np.sum(k1.real>0.99))}", flush=True)
    k = kappas(1.0, 0.5 + 2j); c = 1.02 / k[0].real
    kc = kappas(1.0, 0.5 + 2j, scale=c)
    _, d, _, _ = w_det(1.0, 2 * (0.5 + 2j) - 1, c * np.sin(np.pi * (0.5 + 2j)) ** 2 / np.pi ** 2, -1)
    print(f"detector control (lam^2 x {c:.4f} at t=1,y=2): kmax {kc[0].real:.5f}  det {complex(d):.4e}  "
          f"[{'FIRES' if kc[0].real >= 1 and complex(d).real < 0 else 'does not fire'}]", flush=True)
