"""EXP-019: one-variable test on the flagged dirac2v node M = 13.58 (series start did not converge at dps 152, N = 30).
Variant: N = 40, everything else as production (a = 1/4, dps = 30 + 9M, delta0 default)."""
import sys, math, io, contextlib, time, json, glob
sys.path.insert(0, '.')
import mpmath as mp, exp004_mp as em
from exp004_prod import XG
f = [g for g in glob.glob('exp004_nodes/dirac2v_M13.5798*.json')][0]; node = json.load(open(f)); M = node['M']
dps = int(30 + 9*M); em.set_prec = (lambda MM: setattr(mp.mp, 'dps', dps)); mp.mp.dps = dps
t0 = time.time()
for N in (40,):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        out, d = em.integrate_mp(M, 0.25, math.radians(4), XG, N=N, branch=-1, verbose=True)
    rn = float(abs(d['_rn'])); sig = math.exp(-2*math.pi*M)
    print(f"M={M:.4f} N={N} dps={dps}: residual {rn:.1e} (residual/signal {rn/sig:.1e}); F5={complex(out[XG[0]]).real:+.4e} F26.6={complex(out[XG[4]]).real:+.4e} F90={complex(out[XG[13]]).real:+.4e} [{time.time()-t0:.0f}s]", flush=True)
print("stored (N=30):", f"F5={node['F_re'][0]:+.4e} residual {node['rn']:.1e}")
