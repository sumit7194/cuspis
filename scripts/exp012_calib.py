import sys, glob, json, math, time
sys.path.insert(0, '.')
import mpmath as mp, exp004_mp as em
from exp004_prod import DEG, XG, branch_by_continuation
from multiprocessing import Pool
f = sorted(glob.glob('exp004_nodes/ee_M11.24*_t0.5003*.json'))[0]; node = json.load(open(f)); M = node['M']; t = node['t']
a = complex(0.5, -t); N = int(2*round((1.6*M + 8)/2))
def run(dps):
    em.set_prec = (lambda MM: setattr(mp.mp, 'dps', dps)); mp.mp.dps = dps
    sign, guess, flips = branch_by_continuation(M, t, N, 0.5, 'ee'); t0 = time.time()
    out, d = em.integrate_mp(M, a, math.radians(4), XG, branch=sign, guess=guess)
    return dps, time.time()-t0, [complex(out[XG[i]]).real for i in (0,2,4,7,13,24)], complex(d['H'][1]).real
if __name__ == '__main__':
    print(f"node M={M:.5f} t={t:.5f} N={N} rule dps={int(25+3*M)}; stored F(5)={node['F_re'][0]:+.4e} F(15)={node['F_re'][2]:+.4e} F(26.6)={node['F_re'][4]:+.4e} F(45)={node['F_re'][7]:+.4e} F(90)={node['F_re'][13]:+.4e}", flush=True)
    with Pool(4) as pool:
        for dps, secs, F, H1 in pool.imap_unordered(run, [59, 80, 100, 120]):
            print(f"dps={dps:3d}: {secs:6.0f}s  F(5)={F[0]:+.4e} F(15)={F[1]:+.4e} F(26.6)={F[2]:+.4e} F(45)={F[3]:+.4e} F(90)={F[4]:+.4e} F(170)={F[5]:+.4e} H1={H1:+.6e}", flush=True)
    print("CALIB DONE", flush=True)
