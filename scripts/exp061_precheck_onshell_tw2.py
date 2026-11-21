"""EXP-061 pre-check 4b: unseen-point test of the Delta-part closed form f.p.[Delta] = -32 a(1-a)/(12 pi^2), conjectured
from a = 0.2, 0.35, 0.5 (pre-check 4). Predictions stated before this run: a=0.1, 0.9 -> -0.0243171; a=0.27 -> -0.0532549.
rho0 swept down to 0.005. [model: Opus 5.5]"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from exp061_precheck_onshell_tw import onshell
for a in (0.1, 0.27, 0.9, 0.5):
    c, res = onshell(a, rho0s=(0.02, 0.01, 0.005))
    pred = -32 * a * (1 - a) / (12 * np.pi ** 2)
    print(f"a={a}: f.p.[Delta] at rho0=" + ", ".join(f"{r0}: {v:+.9f}" for r0, v in res) + f"   prediction {pred:+.9f}  diff(0.005) {res[-1][1]-pred:+.1e}", flush=True)
