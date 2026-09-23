"""EXP-029 analysis, exactly as pre-registered (report.md; commit c8d2cea). Sealed toward quantum."""
import numpy as np
from math import pi
from exp028_analyze import load, fit
from exp028_extract import DEG, TH
from exp029_trend import T, EMI
TAU = 1.0e-3
M20 = np.array(DEG) >= 20
runs = load(); alist = sorted(runs)
print("twists:", alist, " failures:", [runs[a][1] for a in alist])
fits = {"A2+A4, all a": fit(runs, alist, [2, 4]),
        "A2+A4, drop largest a": fit(runs, alist[:-1], [2, 4]),
        "A2+A4+A6, all a": fit(runs, alist, [2, 4, 6])}
print(f"\nGATE (each fit: |T(A2)| <= tau = {TAU:g} and A2 shape = EMI to <= 1e-3 on theta >= 20)")
ok = True
for n, c in fits.items():
    A2 = c[2]; sh = (A2/A2[DEG.index(90)])/EMI; dev = np.max(np.abs(sh - 1)[M20]); t2 = T(A2)
    g = abs(t2) <= TAU and dev <= 1e-3; ok &= g
    print(f"   {n:24s}: T(A2) = {t2:+.2e}, max shape dev = {dev:.2e} -> {'PASS' if g else 'FAIL'}")
if not ok:
    print("\nGATE FAILED: stop (as registered)."); raise SystemExit
print("\nP1 (A4/A2 < 0 at every theta >= 20) and P2 (T(A4) < -tau), all three fits side by side")
res = []
for n, c in fits.items():
    r = (c[4]/c[2])[M20]; t4 = T(c[4])
    p1 = bool(np.all(r < 0)); res.append((p1, t4))
    print(f"   {n:24s}: A4/A2 in [{r.min():+.4f}, {r.max():+.4f}] -> P1 {'holds' if p1 else 'fails'};  T(A4) = {t4:+.4e} -> {'< -tau' if t4 < -TAU else ('> +tau' if t4 > TAU else 'flat')}")
    print(f"      A4 shape / EMI at 20,30,45,90,135,170: {np.round(((c[4]/c[4][DEG.index(90)])/EMI)[[DEG.index(d) for d in (20,30,45,90,135,170)]], 4)}")
    if 6 in c: print(f"      (A6/A2 range on theta >= 20: [{(c[6]/c[2])[M20].min():+.3f}, {(c[6]/c[2])[M20].max():+.3f}])")
P1 = "HOLDS" if all(p for p, _ in res) else ("FAILS" if not any(p for p, _ in res) else "INCONCLUSIVE")
P2 = "HOLDS" if all(t < -TAU for _, t in res) else ("FAILS" if all(t > TAU for _, t in res) else "INCONCLUSIVE")
print(f"\nVERDICT (trend-based, no kappa extrapolation; not blind): P1 {P1}; P2 {P2}")
