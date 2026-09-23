"""EXP-029 trend statistic (pre-registered in report.md).  R(theta) = [f(theta)/f(90)] / EMI(theta) on theta >= 20 deg.
T(f) = mean R over S = {20, 26.565, 30, 40} deg  minus  mean R over P = {140, 150, 153.435, 160, 170} deg.
T > +tau: f is relatively heavier toward the sharp end than EMI (kappa/sigma > 3pi direction); T < -tau: lighter (< 3pi); |T| <= tau: flat."""
import json, os, numpy as np
from math import pi
from exp028_extract import DEG, TH
D = os.path.dirname(os.path.abspath(__file__))
EMI = 1 + (pi - TH)/np.tan(TH)
S = [20, 26.565, 30, 40]; P = [140, 150, 153.435, 160, 170]
def T(f):
    f = np.asarray(f); R = (f/f[DEG.index(90)])/EMI
    return np.mean([R[DEG.index(d)] for d in S]) - np.mean([R[DEG.index(d)] for d in P])
if __name__ == "__main__":
    s02 = np.array(json.load(open(f"{D}/exp004_diracA0.0200_result_n24_24_p15.0_t1.json"))["s"])
    s25 = -np.array(json.load(open(f"{D}/exp004_dirac2v_result_n24_24_p15.0_t1.json"))["s"])/2
    t02, t25 = T(s02), T(s25); tau = max(1e-3, 10*abs(t02))
    print(f"T(s(0.02)) = {t02:+.3e}  (A2 proxy: flatness)")
    print(f"tau = max(1e-3, 10|T(s(0.02))|) = {tau:.3e}")
    print(f"T(s(1/4)) = {t25:+.3e}  -> control {'FIRES' if abs(t25) > tau else 'DOES NOT FIRE'} (|T| vs tau)")
    print(f"T(exact EMI) = {T(EMI):+.1e}")
