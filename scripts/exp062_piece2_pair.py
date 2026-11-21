"""EXP-062 piece (II)': (II)'(a) = (1/2pi) sum_{q=-Q..Q} Int dk (k tanh(pi k)/(2pi)) D~'(k,|q|) W_q(k; a),
W_q(k; a) = Int dmu P_{-1/2+ik}(cosh rho) P_{a-1/2}(cosh rho) g_{nu_q}(rho), nu_q = a - q (q <= 0), q - a (q >= 1)
(the twisted internal phi; analytic in a). D~' from exp062_piece2_table.npz (alpha-independent). Valid for Re a < 3/4
(absolute convergence of the Parseval pairing). Per-q contributions printed (q-sum convergence). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, mpc, legenp
from exp062_piece2_table import rho_nodes
D0 = os.path.dirname(os.path.abspath(__file__))

def g_c(nu, rho):
    def f(u, part):
        t = rho + u * u
        v = np.exp(-nu * t) * 2 * u / np.sqrt(4 * np.sinh(rho + u * u / 2) * np.sinh(u * u / 2)) if u > 0 else np.exp(-nu * rho) * 2 / np.sqrt(2 * np.sinh(rho))
        return v.real if part == 0 else v.imag
    return (quad(f, 0, 14, args=(0,), limit=400, epsabs=1e-16, epsrel=1e-12)[0]
            + 1j * quad(f, 0, 14, args=(1,), limit=400, epsabs=1e-16, epsrel=1e-12)[0]) / (2 * np.pi)

def deg(x):
    x = mpc(x); return x.real if x.imag == 0 else x

def Pk_cache(kk, R):
    fn = os.path.join(D0, "exp062_Pk_cache.npz")
    if os.path.exists(fn):
        d = np.load(fn)
        if d["k"].shape == kk.shape and d["R"].shape == R.shape and np.allclose(d["k"], kk) and np.allclose(d["R"], R): return d["P"]
    P = np.array([[float(legenp(mpc(-0.5, k), 0, mp.cosh(mpf(r)), type=3).real) for r in R] for k in kk])
    np.savez(fn, k=kk, R=R, P=P); return P

def pair(a, Q=8, rmax=60.0, kmaxs=(20.0, 30.0, 40.0)):
    tab = np.load(os.path.join(D0, "exp062_piece2_table.npz")); kk, wk = tab["k"], tab["wk"]
    R, W = rho_nodes(rmax)
    Pk = Pk_cache(kk, R)
    Pa = np.array([complex(legenp(deg(a - 0.5), 0, mp.cosh(mpf(r)), type=3)) for r in R])
    meas = wk * kk * np.tanh(np.pi * kk) / (2 * np.pi)
    contrib = {km: {} for km in kmaxs}
    for q in range(-Q, Q + 1):
        if f"Dp_{abs(q)}" not in tab: continue
        nu = (a - q) if q <= 0 else (q - a)
        gv = np.array([g_c(nu, r) for r in R])
        Wq = Pk @ (W * 2 * np.pi * np.sinh(R) * Pa * gv)
        for km in kmaxs:
            m = kk <= km + 1e-9
            contrib[km][q] = np.sum((meas * tab[f"Dp_{abs(q)}"] * Wq)[m]) / (2 * np.pi)
    return contrib

if __name__ == "__main__":
    alist = [complex(v) for v in sys.argv[1:]] or [0.35, 0.5]
    for a in alist:
        a = a.real if a.imag == 0 else a
        t0 = time.time(); C = pair(a)
        for km, c in C.items():
            tot = sum(c.values())
            print(f"a={a} kmax={km}: (II)' = {tot.real:+.9f}{tot.imag:+.1e}j   per-q: " + " ".join(f"{q}:{v.real:+.2e}" for q, v in sorted(c.items()))
                  + f"   partial sums |q|<=4,6,8: " + ", ".join(f"{sum(v for q, v in c.items() if abs(q) <= m).real:+.7f}" for m in (4, 6, 8)), flush=True)
        print(f"  [{time.time()-t0:.0f}s]", flush=True)
