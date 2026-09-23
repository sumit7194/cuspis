"""EXP-025d: re-run (by the main session) of the independent reviewer's EMI known-answer check.
Reviewer's scripts are preserved verbatim in scripts/exp025d_critic/ (written by an adversarial review agent, 2026-09-24).
Claim tested: in the EMI model (SSA, purity, Moebius invariance hold exactly), the n = 1 construction of EXP-025 O3 gives
G(u) = Fbar(u) - 4 R(u,u') equal to the tangent line of Fbar at u' (for the u'-eye trial), for u on BOTH sides of u';
and for a non-eye trial (half-ellipse) G is affine but does NOT touch Fbar (the check can fail)."""
import sys, time, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/exp025d_critic')
from emi_general import Fbar, Fbarp, R, eye_arc, ellipse_arc
t0 = time.time()
print("EYE TRIAL (prediction: G - tangent = 0 up to quadrature/finite-difference error)")
for up, us in ((0.5, (0.1, 0.3, 0.8, 2.0)), (1.5, (0.7, 3.0))):
    print(f" u'={up}: Fbar={Fbar(up):.9f} Fbar'={Fbarp(up):.9f}", flush=True)
    for u in us:
        r = R(u, eye_arc(up)); G = Fbar(u) - 4*r; t = Fbar(up) + Fbarp(up)*(u - up)
        print(f"   u={u:<4} ({'u<u' if u < up else 'u>u'}') G={G:.10f} tangent={t:.10f} G-tangent={G-t:+.2e}   [{time.time()-t0:.0f}s]", flush=True)
print("CONTROL: half-ellipse trial A=1.5 (prediction: G affine in u, strictly below Fbar)")
us = [0.02, 0.05, 0.1, 0.15, 0.2]; Gs = []
for u in us:
    r = R(u, ellipse_arc(1.5)); Gs.append(Fbar(u) - 4*r)
c = np.polyfit(us, Gs, 1)
print(f"   affine fit residual max {np.max(abs(np.polyval(c, us) - np.array(Gs))):.1e};  min(Fbar - G) = {min(Fbar(u) - g for u, g in zip(us, Gs)):.4f} (> 0 means not touching)   [{time.time()-t0:.0f}s]")
