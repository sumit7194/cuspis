"""EXP-043 post-hoc refinement (labelled in report.md): is the S-law Einstein profile et_E monotone near t = 0?
Shift the inversion contour to 1 < Re D < 2 (left of the pinning pole at D = 2): then
et_E(t) - Res = (1/pi) Re int_0^inf M(2+sigma+iy) t^(-sigma-iy) dy with sigma = -0.5, which is suppressed by t^(+1/2).
Also: the residue at D = 2 (must be 1/3), and the same for EMI as a control with a known sign (EMI S-law decreasing)."""
import io, contextlib, math, sys
import numpy as np
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import exp043_profiles as P
for name, M in (("Einstein S-law", P.M_E_S), ("EMI S-law", P.M_EMI_S), ("EMI D-law", P.M_EMI_D)):
    eps = 1e-6; res = float((M(2 + eps) * eps).real)
    print(f"{name}: residue at D = 2: {res:.8f} (1/3 = 0.33333333)")
    segs = P.SEG_E if "Einstein" in name else [(0, 200, 0.01)]
    prev = None
    for t in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.2):
        d = P.inv_mellin(M, t, -0.5, segs)
        print(f"   t={t:7.0e}: profile - 1/3 = {d:+.4e}   (ratio to t: {d/t:+.4f})")
