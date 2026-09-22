"""EXP-019: judge the dirac2q result against the pre-registered criterion. Usage: python3 scripts/exp019_check.py"""
import json, sys, numpy as np, io, contextlib
from math import pi
sys.path.insert(0, __file__.rsplit('/',1)[0])
with contextlib.redirect_stdout(io.StringIO()):
    from exp012_sign import fermi, kap, series, ansatz22
res = json.load(open(__file__.rsplit('/',1)[0] + '/exp004_dirac2q_result_n24_24_p15.0_t1.json'))
deg = np.array(res['deg']); s = np.array(res['s']); th = np.radians(deg)
c = fermi[2]; k = kap['fermi'][2]; sig = 1/(64*pi); sigp = (35*pi-8)/(30720*pi**2)
print(f"mode={res['mode']} nodes={res['nodes']} failures={res['failures']}")
tab = {26.565: 0.0955, 45: 0.0503, 63.435: 0.0302, 90: 0.01496, 116.565: 0.006669, 135: 0.003204, 153.435: 0.001085}
worst_hi = worst_lo = 0.0
for d, v in zip(deg, s):
    t = np.radians(d); ref = series(t, c) if d >= 90 else ansatz22(t, c, k); dev = v/ref - 1
    key = [x for x in tab if abs(x-d) < 0.01]
    if d >= 90 and d <= 160: worst_hi = max(worst_hi, abs(dev))
    if key and d < 90: worst_lo = max(worst_lo, abs(dev))
    print(f"  {d:8.3f}  s={v:+.6e}  ref={ref:.6e}  ratio-1={dev:+.2e}" + (f"   Table 2: {tab[key[0]]}" if key else ""))
i = list(deg).index(170.0); e = pi - th[i]; r170 = s[i]/(sig*e**2 + sigp*e**4 + c[2]*e**6) - 1
ok = worst_hi <= 1e-3 and worst_lo <= 2e-3 and abs(r170) <= 1e-4
print(f"worst >= 90 deg: {worst_hi:.2e} (<= 1e-3);  worst at 26.6/45/63.4: {worst_lo:.2e} (<= 2e-3);  170 deg smooth: {r170:+.2e} (<= 1e-4)")
print("PASS" if ok else "FAIL", "against the criterion fixed before the run")
