"""R3 Tier-1, known-bad control: T46d's n-general THRESHOLD continuation on the EXP-082 eps-family (eps = 1), route (ii)
Q_cont(n) = g_n(1) + n int_eps^{1-eps} g_n + tail (eps = 1/(2n)), g_n(b) = log det(B1^-1 D(b) [B1 + sum_pairs w dB(n, b)] D(b)^-1),
D-scaled as in T46d (det-invariant), phase unwrapped along paths. Checks: Q_cont(1), integers n = 2, 3 vs honest (EXP-082);
then |Q_cont(c + i t)|, c = 1, 1.5, 3, t <= 20. [model: Opus 5.5]"""
import sys, os, json, time, importlib.util, numpy as np
from scipy import linalg
from numpy.polynomial.legendre import leggauss
spec = importlib.util.spec_from_file_location("t46d", os.path.join(sys.argv[1], "brief_p2_t46d.py")); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
T0 = time.time(); eps_link = 1.0
op = D.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="closed_loop_broken"); eng = D.CenteredQEngine(op, dq=0.5, Q_max=4.0, K_max=2, act_tol=0.0)
w = 0.5 / (2 * np.pi); m_lo = 1 - eng.M_q; prs = [(eng._get_qd(m), eng._get_qd(1 - m)) for m in range(m_lo, m_lo + 2 * eng.M_q)]
B1 = sum(w * 2.0 * (a['G0'] * b['G0']) for a, b in prs); cho = linalg.cho_factor(B1)
def g(n, b):
    B = B1 + sum(w * D.pair_delta_B_exact(a, c, n, b) for a, c in prs); up, um = np.exp(1j * b * op.Phi), np.exp(-1j * b * op.Phi)
    s, l = np.linalg.slogdet(linalg.cho_solve(cho, (up[:, None] * B) * um[None, :])); return l + 1j * np.angle(s)
def unwrap(v): v = np.array(v); return v.real + 1j * np.unwrap(v.imag)
def Q(n, Mx=24, Mt=48, tmax=2.5, nseg=8):          # tail capped at 2.5: T46d's float formulas break at Im beta >= 3 (its item 0)
    if n == 1.0: return g(1.0, 1.0)                  # empty sector sum at n = 1
    e = 1.0 / (2.0 * n); x, wx = leggauss(Mx); bs = 0.5 * (1 - 2 * e) * x + 0.5
    gb = unwrap([g(n, b) for b in bs]); Ire = n * np.sum(0.5 * (1 - 2 * e) * wx * gb)
    tg, wg = leggauss(Mt // nseg); ts, ws = [], []
    for s in range(nseg):
        a, b = s * tmax / nseg, (s + 1) * tmax / nseg; ts += list(0.5 * (b - a) * (tg + 1) + a); ws += list(0.5 * (b - a) * wg)
    gp = unwrap([g(n, e)] + [g(n, e + 1j * t) for t in ts])[1:]; gm = unwrap([g(n, e)] + [g(n, e - 1j * t) for t in ts])[1:]
    It = sum(wi * (-2j * n) * (gp[i] - gm[i]) / (np.exp(2 * np.pi * n * ti) + 1.0) for i, (ti, wi) in enumerate(zip(ts, ws)))
    return g(n, 1.0) + Ire + It
hon = json.load(open("exp082_results.json"))["1.0"]["Q"]
print(f"Q_cont(1) = {Q(1.0):.3e}; n=2: {Q(2.0).real:+.10f} vs honest {hon['2']:+.10f}; n=3: {Q(3.0).real:+.10f} vs honest {hon['3']:+.10f}  ({time.time()-T0:.0f}s)", flush=True)
for c in (1.0, 1.5, 3.0):
    row = []
    for t in (1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20.0):
        try: q = Q(complex(c, t)); row.append(f"t={t:g}: |Q| {abs(q):.3e} log|Q|/t {np.log(abs(q))/t:+.3f}")
        except Exception as ex: row.append(f"t={t:g}: FAIL {type(ex).__name__}")
    print(f"T46d threshold (known-bad) Re n={c}: " + " | ".join(row) + f"  ({time.time()-T0:.0f}s)", flush=True)
