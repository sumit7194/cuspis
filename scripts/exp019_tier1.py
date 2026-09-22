"""EXP-019 Tier 1: does the Dirac vertex term stay finite as m -> 0 at the correct twist a = 1/4 (it blew up as 1/m^2 at a = 1/2)?"""
import sys, io, contextlib
sys.path.insert(0, '.')
import numpy as np, exp004_prod as P
for p in (0.0096, 0.0505, 0.2272):
    M = float(np.sqrt(0.25 + p*p))
    with contextlib.redirect_stdout(io.StringIO()):
        r = P.worker((M, 0.0, 'dirac2q'))
    print(f"m={p:.4f} M={M:.4f} ok={r['ok']} dps={r.get('dps')}: Psi_pi={r['Psi_pi'][0]:+.4e}  Psi(90deg)={r['Psi_re'][13]:+.4e}  Psi(170deg)={r['Psi_re'][24]:+.4e}  F(90)={r['F_re'][13]:+.4e}  [{r['secs']:.1f}s]" if r['ok'] else f"m={p}: FAILED {r['err'][:200]}")
