"""EXP-069 pre-check: complex-twist BIE (exp069_bie_complex) against the Fredholm anchor on the CH07b line.
E_pred(w; a) = -w_S(w, a) / (8 pi a(1-a) w)  [CH05-route identity e = -m w/(8 pi a(1-a) t); w_S from EXP-044's Fredholm det].
Ladder: L in {16, 20, 24} (p=5), p in {5, 6} (L=20), projection radius R in {0.10, 0.16, 0.22} x min(w,1) (L=20, p=6), and the
projection arc theta_max in {0.85, 0.70} pi (conditioning of complex-a modes). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp069_bie_complex as B
from exp044_det import w_scalar
for w, y in ((0.3, 1.0), (0.3, 2.0)):
    a = 0.5 + 1j * y
    wS = complex(w_scalar(w, a)[0]); Epred = -wS / (8 * np.pi * a * (1 - a) * w)
    print(f"w={w} y={y}: E_pred = {Epred:.7f}", flush=True)
    t0 = time.time()
    for L, p in ((16, 5), (20, 5), (24, 5), (20, 6)):
        s = B.TwistedIntervalBIE(w, a, n_layers=L, p=p)
        for Rf in ((0.16,) if (L, p) != (20, 6) else (0.10, 0.16, 0.22)):
            for tm in ((0.85,) if (L, p, Rf) != (20, 6, 0.16) else (0.85, 0.70)):
                dC, E = s.extract_DeltaC_and_E(Rf * min(w, 1.0), theta_max=tm * np.pi)
                print(f"   L={L} p={p} R={Rf} th={tm}: E = {E:.7f}  E/E_pred-1 = {E/Epred-1:+.2e}   DeltaC = {dC:.7f}  [{time.time()-t0:.0f}s]", flush=True)
