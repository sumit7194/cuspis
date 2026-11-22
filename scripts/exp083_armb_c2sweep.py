"""C2 W4P4 n = 2 one-variable sweep (pre-statement 110c946; POST HOC; headline unchanged). Unaliased path, stored sigma_2.
Knobs one at a time: Mt 320; npt0 1024; n*Delta_ld1 at 30 digits (mpmath log det of each slice's float64 B1 matrix, i.e. the
log-det evaluation only, not B1's construction). Baseline re-measured as the known-answer control (dev_b 4.43e-10, dev_a 1.04e-10).
Cause found: dev_b <= 3.1e-10 with dev_a unchanged (within 0.2e-10). [model: Opus 5.5]"""
import json, numpy as np, mpmath as mp, exp083_armb as AB, exp083_r3_qcont as QC
from exp083_honest import Geom
g = Geom(4, 4); n = 2.0
hb = float(mp.mpf(json.load(open("exp083_r3p/W4P4b.json"))["Q"]["2"])); ha = float(mp.mpf(json.load(open("exp083_r3p/W4P4a.json"))["Q"]["2"]))
sig = np.array(json.load(open("exp083_armb/c2_W4P4.json"))["2"]["sigma"])
S0, Ss = AB.strip_sigma(g, None), AB.strip_sigma(g, sig)
def run(Mt=160, npt0=512):
    kw = dict(Mx=48, Mt=Mt, tmax=8.0)
    Q0 = QC.QCont(S0, npt=120, npt0=npt0); Qs = QC.QCont(Ss, npt=120, npt0=npt0)
    qb = (Qs.Q(n, **kw) + n * (Qs.ld1 - Q0.ld1).sum()).real; qa = Q0.Q(n, **kw).real
    return qb, qa, Qs, Q0
verdict = lambda db, da: "CAUSE FOUND" if (db <= 3.1e-10 and abs(da - 1.04e-10) <= 0.2e-10) else "no"
out = {}
for lab, a in (("baseline", {}), ("Mt320", dict(Mt=320)), ("npt0_1024", dict(npt0=1024))):
    qb, qa, Qs, Q0 = run(**a); db, da = abs(qb - hb), abs(qa - ha); out[lab] = dict(dev_b=db, dev_a=da, signed_b=qb - hb, signed_a=qa - ha)
    print(f"{lab:10s}: dev_b {db:.2e} (signed {qb - hb:+.2e})   dev_a {da:.2e}   -> {verdict(db, da)}", flush=True)
    if lab == "baseline": qb0, qa0, Qs0, Q00 = qb, qa, Qs, Q0
mp.mp.dps = 30
def ld_mp(S):
    B = S.B1(); tot = mp.mpf(0)
    for k in range(S.Ny): tot += mp.re(mp.log(mp.det(mp.matrix(B[k].tolist()))))
    return tot
d_mp = ld_mp(Ss) - ld_mp(S0); d_f = (Qs0.ld1 - Q00.ld1).sum().real
shift = float(n * (d_mp - mp.mpf(d_f))); qb_mp = qb0 + shift; db = abs(qb_mp - hb)
out["dld1_30digit"] = dict(float=d_f, mp=mp.nstr(d_mp, 25), n_shift=shift, dev_b=db, signed_b=qb_mp - hb)
print(f"n*Dld1 30-digit: Dld1 float64 {d_f:+.16e} vs 30-digit {mp.nstr(d_mp, 20)}; n*difference {shift:+.2e}; "
      f"dev_b {db:.2e} (dev_a unchanged by construction: Dld1 = 0 at sigma = 0) -> {verdict(db, 1.04e-10)}", flush=True)
json.dump(out, open("exp083_armb/c2sweep_W4P4.json", "w"), indent=1)
