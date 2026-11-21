import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
import t46g_ntf as T
for eps in (0.1, 1.0):
    op = T.CheckerEpsModel(eps_link=eps); T.DREC.clear()
    s = T.eval_exact_n1_slope(op); tot = s['T1'] + s['T_sad'] + s['T2']
    d = np.concatenate([x.real for x in T.DREC]); a = np.abs(d)
    hist = [int(((a > 10.0**(-k-1)) & (a <= 10.0**(-k))).sum()) for k in range(8, 17)]
    print(f"NTF={T.NTF:g} eps={eps}: slope {tot:+.12f}  T1 {s['T1']:+.10f} Tsad {s['T_sad']:+.10f} T2 {s['T2']:+.10f} | min|delta| {a.min():.1e}, neg {int((d<0).sum())}, count in decades 1e-8..1e-17: {hist}", flush=True)
