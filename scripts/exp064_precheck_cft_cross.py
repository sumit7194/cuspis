"""EXP-064 pre-check: exact CFT test of the CH05-route sigma machinery in the cross channel.
Route: e(t) = (m/(16 pi a(1-a))) Int_t^inf (h + u^2) dt'  (same sigma-matching and reflection sign as dc/dL = -m^2 b u/(8 pi a(1-a))).
CFT (massless two-tip, conformal map w = (z-L1)/(z-L2)): e = 1/(4 pi L) exactly, for every a. So 4 pi L e = 4 pi t e(t)/m -> 1 as t -> 0
(scalar: approach in 1/log t). Must-fail: the opposite reflection sign gives -1. Computed directly from Int (h+u^2) (not via the w identity),
with w(t) from the same ODE shown alongside. [model: Opus 5.5]"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp063_precheck_ratio as RR
for a in (0.3, 0.5, 0.2):
    sol = RR.run(a, False, t0=16.0, t1=1e-6)
    ts = np.geomspace(1e-6, 16.0, 40001)
    hu = []
    for t in ts:
        u, v, H, *_ = sol.sol(t); hu.append(H / t ** 2 + u * u)
    hu = np.array(hu)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (hu[1:] + hu[:-1]) * np.diff(ts))])
    tail = cum[-1] - cum                                   # Int_t^16 (h+u^2)
    for t in (1.0, 1e-2, 1e-4, 1e-6):
        i = np.argmin(abs(ts - t)); e = tail[i] / (16 * np.pi * a * (1 - a))
        print(f"a={a} t={t:g}: 4 pi t e(t) = {4*np.pi*ts[i]*e:+.6f}   (CFT limit +1; planted sign flip would give {-4*np.pi*ts[i]*e:+.6f})", flush=True)
