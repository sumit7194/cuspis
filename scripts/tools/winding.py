"""Argument-principle zero count for the 081e touch-slice checker (Bridge suggestion, 2026-11-23). Independent of the QEP eigensolver.

  F_complex(sl)(s)  : F(s) = det(D(z) + M C~(z)), z = exp(-2 pi s), for COMPLEX s (the census F_slice is real-only; same formula)
  winding(F, c, r)  : number of zeros of F inside the circle |s - c| = r, from the total change of arg F along the contour,
                      sampled adaptively (a step is halved until |d arg| < pi/8), returned as (count, raw winding, min |F| / max |F|)
A count is only trusted when raw winding is within 0.05 of an integer and min|F| on the contour is not tiny (a pole ON the contour).
[model: Opus 5.5]"""
import numpy as np


def F_complex(sl):
    W = sl.W; M = sl.M
    def F(s):
        z = np.exp(-2 * np.pi * s); CD = np.zeros((2 * W, 2 * W), dtype=complex); D = np.ones(2 * W, dtype=complex)
        for j in range(W): CD[2 * j + 1, 2 * j] = -(z - 1); CD[2 * j, 2 * j + 1] = -(1 - z); D[2 * j + 1] = z
        return np.linalg.det(np.diag(D) + M @ CD)
    return F


def winding(F, c, r, n0=64, max_halvings=30):
    th = np.linspace(0, 2 * np.pi, n0 + 1)
    f = lambda t: F(c + r * np.exp(1j * t))
    tot = 0.0; fmin = np.inf; fmax = 0.0
    for a, b in zip(th[:-1], th[1:]):
        stack = [(a, b, f(a), f(b), 0)]
        while stack:
            t0, t1, f0, f1, d = stack.pop()
            fmin = min(fmin, abs(f0), abs(f1)); fmax = max(fmax, abs(f0), abs(f1))
            da = np.angle(f1 / f0)
            if abs(da) < np.pi / 8 or d >= max_halvings: tot += da; continue
            tm = 0.5 * (t0 + t1); fm = f(tm)
            stack += [(tm, t1, fm, f1, d + 1), (t0, tm, f0, fm, d + 1)]
    w = tot / (2 * np.pi)
    return int(round(w)), w, fmin / fmax
