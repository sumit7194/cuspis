"""EXP-044, labelled follow-up to the FAILED registered n = 1 asymptotic check (added after the FAIL, per the Bridge):
does c_D - (1/3 - t^2 ln^2 t / 3) shrink at the rate of the first neglected term, miss/(t^2 |ln t|) -> const?
Also: the constant A = max_t c(t)/(t K1(2t)) used in the P2 growth bound. [model: Opus 5.5]"""
import math, json, numpy as np
from scipy.special import k1
import exp044_det as E
for t in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
    c = E.c_vn("D", t); L = math.log(t); m = c - (1/3 - t * t * L * L / 3)
    print(f"t={t:g}: c_D {c:.12f}  miss {m:+.3e}  miss/(t^2|ln t|) {m/(t*t*abs(L)):+.4f}")
R = json.load(open("exp044_results.json")); U = np.array(R["U"]); t = np.exp(U)
for k, c in (("D", np.array(R["cD"])), ("S", np.array(R["cS"]))):
    r = c / (t * k1(2 * t)); print(f"A_{k} = max c/(t K1(2t)) on the run grid = {r.max():.5f} at t = {t[r.argmax()]:.3g}; limits: t->0 {r[0]:.4f}, t=8 {r[-1]:.4f}")
