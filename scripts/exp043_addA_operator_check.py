"""EXP-043 addendum A, reconciliation check for the Bridge's objection (2026-11-20). [model: Opus 5.5]
Claim: the two laws are related by a factor in the Mellin variable D, M^D = (D-1) M^S, which along t is the OPERATOR
e = (1 - t d/dt) e~ (not a factor at fixed t). So profile differences obey f_D = f_S - t f_S', and sign counts in t may
differ between the laws while zeros in D coincide.
Check: invert both laws independently, then compare the D-law difference with (1 - t d/dt) of the S-law difference
(central difference in ln t) at the points where the D-law sign changes sit. Also report the predicted small-t sign:
f_S ~ a t^p with p > 1 gives f_D ~ (1 - p) a t^p, the opposite sign."""
import io, contextlib, math, sys
import numpy as np
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import exp043_profiles as P
    import exp043_addA as A
TMAX = P.TMAX

def prof(name, law, t):
    if name == "Einstein":
        return A.inv(P.M_E_D if law == "D" else P.M_E_S, t) if t < TMAX else 0.0
    if name == "EMI":
        return A.inv(P.M_EMI_D if law == "D" else P.M_EMI_S, t, decay=True)
    if name == "Dirac":
        return A.c_D(t) if law == "D" else A.et_D(t)

def op(fS, t, h=1e-3):            # (1 - t d/dt) f via central difference in u = ln t:  t f'(t) = df/du
    return fS(t) - (fS(t * math.exp(h)) - fS(t * math.exp(-h))) / (2 * h)

for a, b, ts in (("Einstein", "EMI", (2e-4, 3.3e-4, 3.5e-4, 5e-4, 1e-2, 0.3, 0.55, 0.565)),
                 ("Dirac", "Einstein", (2e-5, 5e-5, 1e-4, 1e-2, 0.3))):
    print(f"=== {a} - {b} ===")
    fS = lambda t: prof(a, "S", t) - prof(b, "S", t)
    for t in ts:
        fD = prof(a, "D", t) - prof(b, "D", t); fO = op(fS, t)
        print(f"  t={t:<8g} D-law diff {fD:+.4e}   (1 - t d/dt)(S-law diff) {fO:+.4e}   S-law diff {fS(t):+.4e}   "
              f"rel {abs(fO / fD - 1):.1e}")
