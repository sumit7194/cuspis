"""EXP-062 pre-check 3: on-shell finite part of the image piece (I): f.p. Int 2 pi sinh(rho) P_{a-1/2} d_nR drho
= lim [ I(rho0) - 2 pi A / rho0 ], A = -(2/pi) d_n dG (pre-check 2, analytic). d_nR by central differences at
delta = 1e-3 and 2e-3, Richardson-combined (O(delta^2)). Note: piece (I) alone depends on the frequency-interpolation
family of D_1 (Gamma family here); only (I)+(II)'+(III) is physical. [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, mpc, legenp
from exp062_precheck_image import R
from exp062_precheck_shift import dG

def dnR(a, r):
    d1 = (R(a, r, 1.001) - R(a, r, 0.999)) / 0.002; d2 = (R(a, r, 1.002) - R(a, r, 0.998)) / 0.004
    return d1 + (d1 - d2) / 3, abs(d1 - d2)

def image_fp(a, rmax=22.0, nper=10):
    A = float(-(2 / mp.pi) * (dG(1 + mpf('1e-6'), mpf(a)) - dG(1 - mpf('1e-6'), mpf(a))) / mpf('2e-6'))
    xs, ws = np.polynomial.legendre.leggauss(nper); panels = []
    el = [0.005, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]
    for lo, hi in zip(el[:-1], el[1:]):
        L0, L1 = np.log(lo), np.log(hi); t = 0.5 * (L1 - L0) * xs + 0.5 * (L1 + L0)
        panels.append((lo, np.exp(t), 0.5 * (L1 - L0) * ws * np.exp(t)))
    ed = np.linspace(1, rmax, 15)
    for lo, hi in zip(ed[:-1], ed[1:]):
        panels.append((lo, 0.5 * (hi - lo) * xs + 0.5 * (hi + lo), 0.5 * (hi - lo) * ws))
    contrib = []; maxstep = 0.0
    for lo, Rg, W in panels:
        v = 0
        for r, w in zip(Rg, W):
            P = complex(legenp(mpc(a) - mpf(0.5), 0, mp.cosh(mpf(r)), type=3))
            d, e = dnR(a, r); maxstep = max(maxstep, e / max(abs(d), 1e-300))
            v += w * 2 * np.pi * np.sinh(r) * P * d
        contrib.append((lo, v))
    return A, {r0: sum(v for lo, v in contrib if lo >= r0 - 1e-12) - 2 * np.pi * A / r0 for r0 in (0.02, 0.01, 0.005)}, maxstep

if __name__ == "__main__":
    alist = [float(v) for v in sys.argv[1:]] or [0.35, 0.5]
    for a in alist:
        t0 = time.time(); A, o, ms = image_fp(a)
        print(f"a={a}: A={A:+.10e}; f.p.[image] at rho0 " + ", ".join(f"{k}: {v.real:+.9f}{v.imag:+.1e}j" for k, v in o.items())
              + f"  (max rel step-diff {ms:.1e})  [{time.time()-t0:.0f}s]", flush=True)
