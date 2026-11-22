"""POST HOC (labelled; Bridge 2026-11-22): C2 W4P4 n = 2 rerun on strip_sigma WITHOUT aliasing. Registered headline unchanged
(arm (b) UNVALIDATED as registered). (i) stored sigma_2 (aliased gap; = honest saddle to 3.5e-14), strip unaliased -- one variable;
(ii) sigma_2 re-solved on the unaliased gap + unaliased strip (the post-slip-15 code end to end). Known answer: the aliased strip
must reproduce 4.32e-10. Decision (Bridge): dev_b ~ 1e-10 and < 3.1e-10 -> aliasing is the whole cause; ~4.3e-10 -> it is not. [model: Opus 5.5]"""
import json, numpy as np, mpmath as mp, sigma3d as S3, exp083_armb as AB, exp083_r3_qcont as QC
from exp083_honest import Geom
g = Geom(4, 4); kw = dict(Mx=48, Mt=160, tmax=8.0); n = 2.0
hb = float(mp.mpf(json.load(open("exp083_r3p/W4P4b.json"))["Q"]["2"]))
sig_stored = np.array(json.load(open("exp083_armb/c2_W4P4.json"))["2"]["sigma"])
def qsad(sig, alias):
    ld0 = QC.QCont(AB.strip_sigma(g, None, alias=alias), npt=120, npt0=512).ld1
    Qc = QC.QCont(AB.strip_sigma(g, sig, alias=alias), npt=120, npt0=512); return (Qc.Q(n, **kw) + n * (Qc.ld1 - ld0).sum()).real
out = {}
d = abs(qsad(sig_stored, True) - hb); out["aliased_control"] = d; print(f"control: aliased strip, stored sigma_2: dev_b {d:.2e} (must be 4.32e-10)", flush=True)
d = abs(qsad(sig_stored, False) - hb); out["i_unaliased_strip"] = d; print(f"(i)  unaliased strip, stored sigma_2: dev_b {d:.2e}", flush=True)
G1 = g.Gn(1); J0 = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
gap = AB.Gap(g, s_cut=3.0, target="direct", alias=False); s2, info = gap.solve(n, J=J0)
sh, _ = g.saddle(2); out["ii_sigma_vs_honest"] = float(np.abs(s2 - sh).max()); out["ii_sigma_vs_stored"] = float(np.abs(s2 - sig_stored).max())
d = abs(qsad(s2, False) - hb); out["ii_unaliased_all"] = d
print(f"(ii) unaliased gap + strip: |sigma_2 - honest saddle| {out['ii_sigma_vs_honest']:.1e}, vs stored {out['ii_sigma_vs_stored']:.1e}; dev_b {d:.2e}", flush=True)
json.dump(out, open("exp083_armb/c2diag3_W4P4.json", "w"), indent=1)
