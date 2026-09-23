"""C2a' recorded number (bridge, 2026-09-24): non-Gaussian fraction of the free-Dirac EE corner function. Not a test.
CONTROL FIRST: A2(theta) (fitted from the four diracA runs) must equal the closed form -EMI(theta)/8 to <= 1e-3 on theta >= 20.
Closed form: ESW21 eq (9) + definitions: C2 corner = -(sigma_cond/pi^2)(1+(pi-t)cot t) log, sigma_cond = pi^2 C_J/2, free 2-component Dirac
C_J = 1/(8 pi^2) (equal-time <rho rho>_c = -1/(8 pi^2 r^4)); log Z_a = -(2 pi a)^2 C2/2 + ..., log Z_a ~ -s_A(a) log  =>  A2 = -EMI/8.
Gaussian part of the EE (instrument's EE mode: s_EE = Int dt s_A(-it) pi / sinh^2(pi t)):  G = -pi A2 Int t^2/sinh^2(pi t) dt = -A2/6 = EMI/48
(= (pi^2/3) C2, the leading Klich-Levitov term).  NG = s_EE - G."""
import json, os, numpy as np
from math import pi
from exp028_analyze import load, fit
from exp028_extract import DEG, TH
from exp029_trend import T
D = os.path.dirname(os.path.abspath(__file__))
EMI = 1 + (pi - TH)/np.tan(TH); M20 = np.array(DEG) >= 20
runs = load(); A2 = fit(runs, sorted(runs), [2, 4])[2]
dev = np.max(np.abs(A2/(-EMI/8) - 1)[M20])
print(f"CONTROL: max |A2/(-EMI/8) - 1| on theta >= 20 = {dev:.2e}  -> {'PASS' if dev <= 1e-3 else 'FAIL'}")
print("   A2 at 20,45,90,135,170:", np.round(A2[[DEG.index(d) for d in (20,45,90,135,170)]], 6), " closed form:", np.round((-EMI/8)[[DEG.index(d) for d in (20,45,90,135,170)]], 6))
if dev > 1e-3:
    print("CONTROL FAILED: the fraction is not reported."); raise SystemExit
sEE = np.array(json.load(open(f"{D}/exp004_dirac_result_n24_24_p15.0_t14.json"))["s"])
G = -A2/6; NG = sEE - G; frac = NG/sEE
print("\ns_EE (Dirac, EXP-020) at 20,45,90,135,170:", np.round(sEE[[DEG.index(d) for d in (20,45,90,135,170)]], 6))
print("G = EMI/48 (Gaussian)            at same :", np.round(G[[DEG.index(d) for d in (20,45,90,135,170)]], 6))
print("non-Gaussian fraction NG/s_EE on theta >= 20:")
for d in (20, 26.565, 30, 45, 60, 90, 120, 135, 150, 170): print(f"   {d:>7}: {frac[DEG.index(d)]:+.4f}")
print(f"T(NG) = {T(NG):+.4e}  (EXP-029 statistic; tau = 1e-3)   T(s_EE) = {T(sEE):+.4e}   T(G) = {T(G):+.1e}")
