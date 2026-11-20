"""EXP-044 G1 diagnostic (after G1 FAILED on the two small-t asymptotic-form checks; changes no gate). [model: Opus 5.5]
(i) determinant vs lattice Renyi-2 at t = 0.01 and 0.03 (the lattice, not the truncated form, as referee);
(ii) does the miss from the truncated forms shrink at the rate of the first neglected term as t -> 0?
    Dirac: miss / (t^2 |ln t|) should tend to a constant; scalar: miss * ln^2 t should tend to a constant."""
import math
import exp044_det as E
for t in (0.01, 0.03):
    dD = -2 * E.w_dirac(t, 0.25)[0].real; dS = -0.5 * E.w_scalar(t, 0.5)[0].real
    lD, tD = E.lat_c2("D", t, 100); lS, tS = E.lat_c2("S", t, 100)
    print(f"t={t}: Dirac det {dD:.7f} lattice {lD:.7f} diff {dD-lD:+.1e} (lattice tol {tD:.1e}) | scalar det {dS:.6f} lattice {lS:.6f} diff {dS-lS:+.1e} (tol {tS:.1e})")
for t in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
    dD = -2 * E.w_dirac(t, 0.25)[0].real; dS = -0.5 * E.w_scalar(t, 0.5)[0].real
    L = math.log(t); mD = dD - 0.25 * (1 - t * t * L * L); mS = dS - (0.25 + 1 / (2 * L))
    print(f"t={t:g}: Dirac miss {mD:+.3e}  miss/(t^2|ln t|) {mD/(t*t*abs(L)):+.4f} | scalar miss {mS:+.4e}  miss*ln^2 t {mS*L*L:+.4f}")
