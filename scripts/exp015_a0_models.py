"""EXP-015: model dependence of the free-scalar sharp-end constant a0.
Fits y = s - kappa/theta (kappa fixed at CHL09's 0.0397) on the eehp result assembled with M <= 13.1, after
the two known corrections of EXP-012 addendum 6 (uniform t-grid normalisation; mass-cutoff deficit at 15-26.6 deg).
Models: pure power series (A, A3) versus power series plus log(theta) (B, B2) versus 1/log(theta) (C).
Runtime: milliseconds. Usage: python3 scripts/exp015_a0_models.py"""
import json, numpy as np
from math import pi
CT = 3/(32*pi**2)
res = json.load(open(__file__.rsplit('/',1)[0] + '/exp004_eehp_result_Mcut13.1.json'))
deg = np.array(res['deg']); s = np.array(res['s']); th = np.radians(deg)
off = res['sigma_from_H1']*256 - 1
cut = {15.0: -1.6e-3, 20.0: -1.0e-4, 26.565: -2e-5}
st = np.array([v/(1+off)/(1+cut.get(float(d), 0.0)) for d, v in zip(deg, s)])
k = 0.0397
models = {
    "A : a0 + a1 th + a2 th^2":            lambda x: [np.ones_like(x), x, x**2],
    "A3: a0 + a1 th + a2 th^2 + a3 th^3":  lambda x: [np.ones_like(x), x, x**2, x**3],
    "B : b log th + a0 + a1 th":           lambda x: [np.log(x), np.ones_like(x), x],
    "B2: b log th + a0 + a1 th + a2 th^2": lambda x: [np.log(x), np.ones_like(x), x, x**2],
    "C : b/log th + a0 + a1 th":           lambda x: [1/np.log(x), np.ones_like(x), x],
}
for lo, hi in ((20, 50), (20, 60), (26, 60), (20, 70)):
    m = (deg >= lo) & (deg <= hi); x = th[m]; y = st[m] - k/x
    print(f"--- window {lo}-{hi} deg, {m.sum()} points")
    for name, f in models.items():
        A = np.vstack(f(x)).T
        if A.shape[1] >= m.sum(): continue
        c, *_ = np.linalg.lstsq(A, y, rcond=None); rms = np.sqrt(np.mean((y - A@c)**2))*1e6
        i0 = 1 if name.startswith(("B", "C")) else 0
        extra = f"  b = {c[0]/CT:+.3f} C_T" if name.startswith(("B", "C")) else ""
        print(f"   {name:38s} a0 = {c[i0]/CT:+.3f} C_T   rms {rms:6.2f}e-6{extra}")
