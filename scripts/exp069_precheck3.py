"""EXP-069 pre-check 3: projection stabilisation at (w = 0.3, y = 2), one p = 7, L = 20 solve; K_modes in {5, 8, 11},
theta_max in {0.70, 0.80, 0.85} pi, R = 0.16 w. [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp069_bie_complex as B
from exp044_det import w_scalar
w, y = 0.3, 2.0; a = 0.5 + 1j * y
Epred = -complex(w_scalar(w, a)[0]) / (8 * np.pi * a * (1 - a) * w)
s = B.TwistedIntervalBIE(w, a, n_layers=20, p=7); t0 = time.time()
for K in (5, 8, 11):
    for tm in (0.70, 0.80, 0.85):
        n_ang = max(25, 4 * K + 5)
        dC, E = s.extract_DeltaC_and_E(0.16 * w, theta_max=tm * np.pi, K_modes=K, n_ang=n_ang)
        print(f"K={K} th={tm} n_ang={n_ang}: E/E_pred-1 = {E/Epred-1:+.2e}   DeltaC = {dC:.6f}  [{time.time()-t0:.0f}s]", flush=True)
