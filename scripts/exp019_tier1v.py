import sys, io, contextlib, numpy as np
sys.path.insert(0, '.'); import exp004_prod as P
for p in (0.0096, 7.1141):
    M = float(np.sqrt(0.25 + p*p))
    with contextlib.redirect_stdout(io.StringIO()):
        r = P.worker((M, 0.0, 'dirac2v'))
    print(f"M={M:.4f} ok={r['ok']} dps={r.get('dps')} rn/signal={r.get('rn_over_signal', float('nan')):.1e}: F(5)={r['F_re'][0]:+.4e} F(26.6)={r['F_re'][4]:+.4e} Psi(90)={r['Psi_re'][13]:+.4e} [{r['secs']:.0f}s]" if r['ok'] else f"FAILED {r['err'][:200]}", flush=True)
