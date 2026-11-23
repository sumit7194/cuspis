"""EXP-084 (draft, not registered) dry run: (1) known answer: W2P2 (Wbox 4) arm b Q(2), Q(3) in float64 (exp083_honest.Geom) vs the stored
400-digit Arb values (exp083_r2/W2P2b.json); (2) cost/peak of arm b Q(2), Q(3) at ONE k=1 width (W3P6b6) -- no width pair is formed, so
no data of the planned experiment is read before registration. [model: Opus 5.5]"""
import json, time, numpy as np
from mpmath import mpf
import exp083_honest as H
ref = json.load(open("exp083_r2/W2P2b.json"))["Q"]
g = H.Geom(2, 2, Wbox=4, c=2)
for n in (2, 3):
    t = time.time(); q = g.Q(n, saddle=True); r = mpf(ref[str(n)])
    print(f"known answer W2P2 arm b n={n}: float64 {q:.16f}  Arb {float(r):.16f}  |diff| {abs(q - float(r)):.1e}  ({time.time()-t:.1f}s)", flush=True)
g = H.Geom(3, 6, Wbox=6, c=2); ld1 = g.logdetB(g.Gn(1))
for n in (2, 3):
    t = time.time(); sig, it = g.saddle(n); tq = time.time(); q = g.Q(n, saddle=True, ld1=ld1)
    print(f"cost W3P6b6 arm b n={n}: N {g.N} Ny {g.Ny} nN {n*g.N}; saddle it {it}; Q computed (value withheld); wall {time.time()-t:.1f}s", flush=True)
