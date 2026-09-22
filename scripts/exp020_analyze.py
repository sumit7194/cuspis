"""EXP-020: Dirac entanglement run, analysed exactly as frozen in EXP-019 addendum 3.
Order: (1) known answers; (2) residual sign against the (sigma, kappa) trial function; (3) a0 fit and verdict.
Usage: python3 scripts/exp020_analyze.py [result.json]"""
import json, sys, numpy as np, io, contextlib
from math import pi
sys.path.insert(0, __file__.rsplit('/',1)[0])
with contextlib.redirect_stdout(io.StringIO()):
    from exp012_sign import fermi, kap, series, ansatz22, trial
fn = sys.argv[1] if len(sys.argv) > 1 else __file__.rsplit('/',1)[0] + '/exp004_dirac_result_n24_24_p15.0_t14.json'
res = json.load(open(fn)); deg = np.array(res['deg']); s = np.array(res['s']); th = np.radians(deg)
c = fermi[1]; k = kap['fermi'][1]; CT = 3/(16*pi**2); sig = c[0]
print(f"mode={res['mode']} nodes={res['nodes']} failures={res['failures']} nt={res['nt']} t_max={res['t_max']}")
print("\n(1) KNOWN ANSWERS [HHCWM16 Tab. 2/4 alpha=1 exact series >= 90 deg, eq (22) below; CHL09 at 90, 135]")
chl = {90: 0.02329, 135: 0.005022}; tab = {26.565: 0.146, 45: 0.0776, 63.435: 0.0468, 90: 0.02329, 116.565: 0.01043, 135: 0.005022, 153.435: 0.001703}
w_hi = w_lo = 0.0
for d, v in zip(deg, s):
    t = np.radians(d); ref = series(t, c) if d >= 90 else ansatz22(t, c, k); dev = v/ref - 1
    if 63 <= d <= 160: w_hi = max(w_hi, abs(dev))
    if d in (26.565, 45): w_lo = max(w_lo, abs(dev))
    extra = (f"  CHL09 {chl[int(d)]} ({v/chl[int(d)]-1:+.1e})" if int(d) in chl and d == int(d) else "") + (f"  Table2 {tab[d]}" if d in tab else "")
    print(f"  {d:8.3f}  s={v:+.6e}  ref={ref:.6e}  ratio-1={dev:+.2e}{extra}")
i = list(deg).index(170.0); e = pi - th[i]; r170 = s[i]/(sig*e**2 + c[1]*e**4 + c[2]*e**6) - 1
ok = w_hi <= 1e-3 and w_lo <= 2e-3
print(f"  worst 63.4-160: {w_hi:.2e} (<= 1e-3); worst 26.6/45: {w_lo:.2e} (<= 2e-3); 170 deg smooth: {r170:+.2e}  ->  {'KNOWN ANSWERS PASS' if ok else 'KNOWN ANSWERS FAIL: stop, do not look at the fit'}")
if not ok: sys.exit(0)
print("\n(2) RESIDUAL (trial - s)/s in %  (predicted: positive at every angle, no node)")
prev = None
for d, v in zip(deg, s):
    if d < 15: continue
    tr, _, _ = trial(np.radians(d), k, sig); r = (tr/v - 1)*100
    print(f"  {d:8.3f}: {r:+.3f}%" + ("  <-- SIGN CHANGE" if prev is not None and np.sign(r) != np.sign(prev) else "")); prev = r
print("\n(3) a0 with kappa fixed at 0.0722 (CHL09); model A3 decides; A and B2 reported only")
verdicts = []
for lo, hi in ((20, 50), (20, 60), (26, 60), (20, 70)):
    m = (deg >= lo) & (deg <= hi); x = th[m]; y = s[m] - k/x
    out = []
    for name, cols in (("A3", lambda x: [np.ones_like(x), x, x**2, x**3]), ("A", lambda x: [np.ones_like(x), x, x**2]), ("B2", lambda x: [np.log(x), np.ones_like(x), x, x**2])):
        A = np.vstack(cols(x)).T
        if A.shape[1] >= m.sum(): out.append(f"{name}: n/a"); continue
        cf, *_ = np.linalg.lstsq(A, y, rcond=None); rms = np.sqrt(np.mean((y - A@cf)**2))
        a0 = cf[1] if name == "B2" else cf[0]
        out.append(f"{name}: a0 = {a0/CT:+.3f} C_T" + (f", b = {cf[0]/CT:+.3f} C_T" if name == "B2" else "") + f" (rms {rms:.1e})")
        if name == "A3": verdicts.append(a0/CT)
    print(f"  window {lo}-{hi}: " + "; ".join(out))
v = np.array(verdicts)
verdict = "CONFIRMED" if np.all(np.abs(v) < 0.05) else ("REFUTED" if np.all(np.abs(v) > 0.1) else "INCONCLUSIVE")
print(f"\n  model A3 a0 across windows: {', '.join(f'{x:+.3f}' for x in v)} C_T  ->  prediction a0 = 0: {verdict}  (rule: all |a0| < 0.05 confirm; all > 0.1 refute)")
print(f"  for scale: trial-function a0~ = {-0.75*2*pi*(k-3*pi*sig)/(pi**2-6)/CT:+.3f} C_T; free scalar measured ~ -0.3 C_T")
