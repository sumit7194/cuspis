"""EXP-061 pre-check 3b: Legendre on-shell finite part beyond (0,1): w in {1, 1.5, 2, 3}. The 0<w<1 form
-1/16 - w/2 + w^2/4 predicts -0.3125, -0.25, -0.0625, +0.6875 (stated before the run). [model: Opus 5.5]"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, pi
from exp061_precheck_onshell_leg import fp
mp.dps = 20
for w in (mpf(1), mpf('1.5'), mpf(2), mpf(3)):
    vals = [fp(1j * w, w, mpf(e)) for e in ('1e-6', '1e-8')]
    pred = -mpf(1)/16 - w/2 + w*w/4
    print(f"w={w}: f.p. eps=1e-6,1e-8: {mp.nstr(vals[0],12)}, {mp.nstr(vals[1],12)}   (0<w<1 form predicts {mp.nstr(pred,8)})"
          f"   x(-4/3pi^2)*12pi^2 = {mp.nstr(-16*vals[1],8)}", flush=True)
