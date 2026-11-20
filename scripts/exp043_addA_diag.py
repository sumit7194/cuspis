"""EXP-043 addendum A diagnostic (written after the addendum A run of 2026-11-20 showed A2 count FAIL, A2 ends FAIL,
A3 inside FAIL). Asks WHY each fired; changes no criterion. [model: Opus 5.5]
(i)  Einstein vs EMI under the Dirac law: where the two sign changes sit on the A2 nodes, and |difference| there,
     against the Einstein inversion's own error (same nodes recomputed with a finer/longer contour).
(ii) small-t end signs at t = 1e-6, 1e-5, 1e-4 (D-law): profile - 1/3 for Dirac, Einstein, EMI, and the Einstein/EMI
     inversion error estimated the same way.
(iii) A3: the same inside-edge values with the finer/longer contour, to test the amplified-quadrature-floor reading."""
import io, contextlib, math, sys
import numpy as np
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import exp043_profiles as P
    import exp043_addA as A
TMAX = P.TMAX
SEG_FINE = [(0, 400, 0.005), (400, 60000, 0.025)]

def inv_seg(M, t, segs, decay=False):
    if t < 0.05: return 1/3 + P.inv_mellin(M, t, -0.5, segs if not decay else [(0, 200, 0.0025)])
    if decay:
        s = max(0.5, 2*t); Y = 80 + 30*math.sqrt(s); return P.inv_mellin(M, t, s, [(0, Y, 0.005)])
    return P.inv_mellin(M, t, 0.5, segs)

nodes = np.unique(np.concatenate([np.exp(np.linspace(math.log(1e-4), math.log(0.5), 220)), np.linspace(0.5, TMAX - 1e-3, 60),
                                  np.exp(np.linspace(math.log(TMAX + 1e-3), math.log(20.0), 120))]))
print("=== (i) Einstein - EMI, D-law, on the A2 nodes ===")
E = np.array([A.inv(P.M_E_D, t) if t < TMAX else 0.0 for t in nodes])
Mm = np.array([A.inv(P.M_EMI_D, t, decay=True) for t in nodes])
d = E - Mm; s = np.sign(d)
idx = [k for k in range(len(nodes) - 1) if s[k] * s[k + 1] < 0]
for k in idx:
    for j in (k, k + 1):
        t = nodes[j]
        Ef = inv_seg(P.M_E_D, t, SEG_FINE) if t < TMAX else 0.0
        Mf = inv_seg(P.M_EMI_D, t, None, decay=True)
        print(f"  t={t:.6g}: E={E[j]:.12f} EMI={Mm[j]:.12f} d={d[j]:+.3e} | fine contour: E={Ef:.12f} EMI={Mf:.12f} d={Ef - Mf:+.3e}")
print(f"  sign changes at node pairs {idx}; max |d| overall {np.max(np.abs(d)):.3e}")

print("=== (ii) small-t, D-law: profile - 1/3, and inversion error (standard vs fine contour) ===")
for t in (1e-6, 1e-5, 1e-4):
    cD = A.c_D(t) - 1/3
    Es, Ef = A.inv(P.M_E_D, t) - 1/3, inv_seg(P.M_E_D, t, SEG_FINE) - 1/3
    Ms, Mf = A.inv(P.M_EMI_D, t, decay=True) - 1/3, inv_seg(P.M_EMI_D, t, None, decay=True) - 1/3
    print(f"  t={t:g}: Dirac {cD:+.3e} | Einstein {Es:+.3e} (fine {Ef:+.3e}) | EMI {Ms:+.3e} (fine {Mf:+.3e}) | "
          f"Dirac-Einstein {cD - Es:+.3e}  Einstein-EMI {Es - Ms:+.3e}")

print("=== (iii) A3 inside the edge, S-law: standard vs fine contour ===")
for t, sig in ((0.5, (0.5, 5, 20, 80)), (0.3, (0.5, 5, 20))):
    for sg in sig:
        a, b = P.inv_mellin(P.M_E_S, t, sg, P.SEG_E), P.inv_mellin(P.M_E_S, t, sg, SEG_FINE)
        print(f"  t={t} sigma={sg}: standard {a:.10f} fine {b:.10f} diff {a - b:+.1e}  amplification (t_max/t)^sigma {(TMAX/t)**sg:.1e}")
