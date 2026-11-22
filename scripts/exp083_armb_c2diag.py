"""C2 W4P4 n = 2 FAIL (dev_b 4.3e-10 vs tol 3 dev_a = 3.1e-10): why did it fire? Diagnostic only; the registered verdict stands.
One variable at a time at n = 2, sigma_2 from the C2 checkpoint (|sigma - honest saddle| 3.5e-14):
  arm (b) chain setting (known-answer: must reproduce 4.3e-10), arm (b) s_cut 3.5, arm (b) npt 200; arm (a) s_cut 3.5.
Hypothesis: the s_cut truncation (W4P4 poles 3.011, 3.088 above the cut; the n = 1 floor 5.7e-7) differs with sigma. [model: Opus 5.5]"""
import json, numpy as np, mpmath as mp, exp083_armb as AB, exp083_r3_qcont as QC
from exp083_honest import Geom
g = Geom(4, 4); kw = dict(Mx=48, Mt=160, tmax=8.0); n = 2.0
c2 = json.load(open("exp083_armb/c2_W4P4.json")); sig = np.array(c2["2"]["sigma"])
hb = float(mp.mpf(json.load(open("exp083_r3p/W4P4b.json"))["Q"]["2"])); ha = float(mp.mpf(json.load(open("exp083_r3p/W4P4a.json"))["Q"]["2"]))
def qsad(sig, s_cut=3.0, npt=120):
    ld0 = QC.QCont(AB.strip_sigma(g, None, s_cut), npt=npt, npt0=512).ld1
    Qc = QC.QCont(AB.strip_sigma(g, sig, s_cut), npt=npt, npt0=512); return (Qc.Q(n, **kw) + n * (Qc.ld1 - ld0).sum()).real
out = {}
for lab, a in (("b_chain", {}), ("b_scut3.5", dict(s_cut=3.5)), ("b_npt200", dict(npt=200))):
    d = abs(qsad(sig, **a) - hb); out[lab] = d; print(f"arm (b) n=2 {lab:10s}: dev {d:.2e}", flush=True)
for lab, s_cut in (("a_chain", 3.0), ("a_scut3.5", 3.5)):
    q = QC.QCont(AB.strip_sigma(g, None, s_cut), npt=120, npt0=512).Q(n, **kw).real; d = abs(q - ha); out[lab] = d
    print(f"arm (a) n=2 {lab:10s}: dev {d:.2e}", flush=True)
json.dump(out, open("exp083_armb/c2diag_W4P4.json", "w"), indent=1)
