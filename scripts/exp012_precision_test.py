"""EXP-012: one-variable test of the small-angle failure at complex a. Node M~7.13, t=0.1145 (first garbage node).
Variants: (dps rule 25+3M = 46, default tol) -> must reproduce the stored garbage; (70, default); (100, default); (70, tol x 1e-8)."""
import sys, glob, json, math, time
sys.path.insert(0, '.')
import mpmath as mp, exp004_mp as em
from exp004_prod import DEG, XG, branch_by_continuation
from multiprocessing import Pool
f = sorted(glob.glob('exp004_nodes/ee_M7.13*_t0.1145*.json'))[0]; node = json.load(open(f)); M = node['M']; t = node['t']
a = complex(0.5, -t); N = int(2*round((1.6*M + 8)/2))
idx = {5:0, 26.565:4, 90:13, 170:24}
def run(args):
    dps, tolscale = args
    em.set_prec = (lambda MM: setattr(mp.mp, 'dps', dps))
    mp.mp.dps = dps
    tolA = mp.mpf(10)**(-(12 + 2.8*M)) * mp.mpf(tolscale)
    tol = [mp.mpf('1e-14')*mp.mpf(tolscale), tolA, tolA, tolA, tolA, tolA, mp.mpf('1e-14')*mp.mpf(tolscale)]
    sign, guess, flips = branch_by_continuation(M, t, N, 0.5, 'ee')
    t0 = time.time()
    out, d = em.integrate_mp(M, a, math.radians(4), XG, branch=sign, guess=guess, tol=tol)
    F = {k: complex(out[XG[i]]) for k, i in idx.items()}
    return dps, tolscale, mp.mp.dps, time.time()-t0, F, complex(d['H'][1])
if __name__ == '__main__':
    print(f"node {f}: M={M:.6f} t={t:.6f} N={N}; stored F(5)={node['F_re'][0]:+.4e} F(26.6)={node['F_re'][4]:+.4e} F(90)={node['F_re'][13]:+.4e} F(170)={node['F_re'][24]:+.4e} H1={node['H1']:+.6e} (stored dps={node['dps']})", flush=True)
    print("expected physical F(5) ~ 1.05 x F(5; t=0.02) =", end=' ')
    g = json.load(open(sorted(glob.glob('exp004_nodes/ee_M7.13*_t0.0219*.json'))[0])); print(f"{1.052*g['F_re'][0]:+.4e}  (t=0.02 node: F(5)={g['F_re'][0]:+.4e}, F(26.6)={g['F_re'][4]:+.4e})", flush=True)
    with Pool(4) as pool:
        for dps, ts, used, secs, F, H1 in pool.imap_unordered(run, [(46,1),(70,1),(100,1),(70,1e-8)]):
            print(f"dps={dps:3d} tol x{ts:g}: {secs:6.0f}s  F(5)={F[5].real:+.4e}  F(26.6)={F[26.565].real:+.4e}  F(90)={F[90].real:+.4e}  F(170)={F[170].real:+.4e}  H1={H1.real:+.6e}", flush=True)
