"""EXP-020 Tier 1 for the Dirac entanglement mode: a few nodes at small and moderate t, low and high M."""
import sys, io, contextlib, numpy as np
sys.path.insert(0, '.'); import exp004_prod as P
xt, wt = np.polynomial.legendre.leggauss(14); ts = 0.5*3.2*(xt+1)
for p, it in ((0.0096, 0), (0.0096, 6), (2.0, 3), (9.0, 1)):
    M = float(np.sqrt(0.25 + p*p)); t = float(ts[it])
    with contextlib.redirect_stdout(io.StringIO()):
        r = P.worker((M, t, 'dirac'))
    if r['ok']:
        print(f"M={M:.4f} t={t:.4f} dps={r['dps']} branch={r['branch']} flips={r['flips']} res/signal={r.get('rn_over_signal', float('nan')):.1e}: Psi(5)={r['Psi_re'][0]:+.4e} Psi(90)={r['Psi_re'][13]:+.4e} Psi(170)={r['Psi_re'][24]:+.4e} Psi_im(90)={r['Psi_im'][13]:+.1e} [{r['secs']:.0f}s]", flush=True)
    else: print(f"M={M:.4f} t={t:.4f} FAILED: {r['err'][:200]}", flush=True)
