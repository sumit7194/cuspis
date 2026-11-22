"""C2 W4P4 n = 2 at the EXACT (Arb) saddle (pre-statement d025d51; POST HOC; headline unchanged). Reads the Arb rerun
exp083_armb/arb_W4P4b_n2_saddle.json (known answer: its Q(2) must equal the registered W4P4b.json value), rounds the 40-digit
saddle to float64, evaluates Q_sad(2) on the unaliased path, and re-measures arm (a) (dev_a 1.04e-10) as the control. [model: Opus 5.5]"""
import json, numpy as np, mpmath as mp, exp083_armb as AB, exp083_r3_qcont as QC
from exp083_honest import Geom
g = Geom(4, 4); n = 2.0; kw = dict(Mx=48, Mt=160, tmax=8.0)
reg = json.load(open("exp083_r3p/W4P4b.json")); new = json.load(open("exp083_armb/arb_W4P4b_n2_saddle.json"))
dq = abs(mp.mpf(reg["Q"]["2"]) - mp.mpf(new["Q"]["2"])); print(f"known answer: Arb rerun Q(2) vs registered: |diff| {mp.nstr(dq, 3)}", flush=True)
assert dq < mp.mpf("1e-90"), "Arb rerun does not reproduce the registered Q(2) -> STOP"
hb = float(mp.mpf(reg["Q"]["2"])); ha = float(mp.mpf(json.load(open("exp083_r3p/W4P4a.json"))["Q"]["2"]))
s_ex = np.array([float(mp.mpf(v)) for v in new["sigma"]["2"]]); s_c2 = np.array(json.load(open("exp083_armb/c2_W4P4.json"))["2"]["sigma"])
s_h, _ = g.saddle(2)
print(f"|sigma_exact - C2 sigma_2| max {np.abs(s_ex - s_c2).max():.2e} (mean {np.abs(s_ex - s_c2).mean():.2e}); "
      f"|sigma_exact - float64 honest saddle| max {np.abs(s_ex - s_h).max():.2e}; |sigma_2 - honest| {np.abs(s_c2 - s_h).max():.2e}", flush=True)
S0 = AB.strip_sigma(g, None); Q0 = QC.QCont(S0, npt=120, npt0=512)
def qsad(sig):
    Qs = QC.QCont(AB.strip_sigma(g, sig), npt=120, npt0=512); return (Qs.Q(n, **kw) + n * (Qs.ld1 - Q0.ld1).sum()).real
qa = Q0.Q(n, **kw).real; da = abs(qa - ha); print(f"control arm (a) dev_a {da:.2e} (must be 1.04e-10)", flush=True)
qe = qsad(s_ex); de = abs(qe - hb)
print(f"Q_sad(2) at the exact saddle (float64-rounded): dev_b {de:.2e} (signed {qe - hb:+.2e}); C2 sigma_2: 4.43e-10 -> "
      f"{'CAUSE FOUND' if de <= 3.1e-10 and abs(da - 1.04e-10) <= 0.2e-10 else 'not found'}", flush=True)
json.dump(dict(dq_arb=str(dq), ds_exact_c2=float(np.abs(s_ex - s_c2).max()), ds_exact_honest=float(np.abs(s_ex - s_h).max()),
               dev_a=da, dev_b_exact=de, signed_b_exact=qe - hb), open("exp083_armb/c2exact_W4P4.json", "w"), indent=1)
