"""EXP-069 pre-check 2: at the hard point (w = 0.3, y = 2) probe panel order p in {6, 7, 8} and projection arc theta_max in
{0.55, 0.70} pi, R = 0.16 w, L = 20. Purpose: choose the registered ladder (pre-check 1 showed p and the arc dominate). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp069_bie_complex as B
from exp044_det import w_scalar
w, y = 0.3, 2.0; a = 0.5 + 1j * y
Epred = -complex(w_scalar(w, a)[0]) / (8 * np.pi * a * (1 - a) * w)
print(f"E_pred = {Epred.real:.7f}", flush=True); t0 = time.time()
for p in (6, 7, 8):
    s = B.TwistedIntervalBIE(w, a, n_layers=20, p=p)
    for tm in (0.55, 0.70):
        for Rf in (0.12, 0.16):
            dC, E = s.extract_DeltaC_and_E(Rf * w, theta_max=tm * np.pi)
            print(f"   p={p} th={tm} R={Rf}: E/E_pred-1 = {E/Epred-1:+.2e}   DeltaC = {dC:.6f}  [{time.time()-t0:.0f}s]", flush=True)
