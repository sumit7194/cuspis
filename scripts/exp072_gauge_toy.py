"""EXP-072 pre-check P3 (gauge toy, known answer). Pure-gauge twist: U = diag(1 on sites < N/2, e^{i phi} on sites >= N/2).
Twisted propagator G^a = U G1 U^dag is gauge-equivalent to G1, so every exact (gauge-invariant) quantity equals its flat value:
  (A) half-twisted bubble: log det(B^(b)) - log det(B1) = 0, with B^(b) = 2 G1 o G^b (Hadamard), X = B1^{-1}(B^(b) - B1).
  (B) q=0 term: T = Tr(B1^{-1} 2(G^a o G^{-a} - G1 o G1)) = 0 exactly (phases cancel pointwise).
Claim under test (argued in report): the LINEAR truncations are NOT zero, i.e. linear-in-DeltaG pieces are gauge artefacts:
  Tr X != 0 although log det(1+X) = 0, and in T the linear part L = 2Tr(Sigma(dG^a + dG^-a)) is cancelled by the quadratic
  part Q = 2Tr(B1^{-1} dG^a o dG^-a): Q/L = -1 exactly (from c + cbar + |c|^2 = 0 at the straddle).
Must-fail control: with U = identity (no twist) everything is 0 including the linear terms (the check can fire).
G1: lattice (-Lap + m^2)^{-1} in 1D; positive, so B1 = 2 G1 o G1 is positive definite (Schur product). [model: Opus 5.5]"""
import numpy as np
N, m = 240, 0.3
L = 2 * np.eye(N) - np.eye(N, k=1) - np.eye(N, k=-1) + m * m * np.eye(N)
G1 = np.linalg.inv(L)
B1 = 2 * G1 * G1
B1i = np.linalg.inv(B1)
def run(phi):
    u = np.ones(N, complex); u[N // 2:] = np.exp(1j * phi)
    Ga = u[:, None] * G1 / u[None, :]          # U G1 U^{-1} (U^{-1} = U^dag only for real phi)
    Gm = (1 / u)[:, None] * G1 * u[None, :]
    dGa, dGm = Ga - G1, Gm - G1
    X = B1i @ (2 * G1 * dGa)
    sgn, ld = np.linalg.slogdet(np.eye(N) + X)
    lin = np.trace(X)
    quad = -0.5 * np.trace(X @ X)
    nrm = np.linalg.norm(X, 2)
    Lq = np.trace(B1i @ (2 * G1 * (dGa + dGm)))
    Qq = np.trace(B1i @ (2 * dGa * dGm))
    Tex = np.trace(B1i @ (2 * (Ga * Gm - G1 * G1)))
    return ld + np.log(sgn), lin, quad, nrm, Lq, Qq, Tex
for phi in (0.0, 0.5, np.pi / 2, np.pi, np.pi + 1j * 0.5):
    ld, lin, quad, nrm, Lq, Qq, Tex = run(phi)
    print(f"phi={phi!s:>18}: (A) logdet(1+X)={ld:+.2e}  TrX={lin:+.4f}  -TrX^2/2={quad:+.4f}  ||X||_2={nrm:.3f}   "
          f"(B) L={Lq:+.4f} Q={Qq:+.4f} L+Q={Lq+Qq:+.1e} exact T={Tex:+.1e}" + (f"  Q/L={Qq/Lq:+.6f}" if abs(Lq) > 1e-12 else ""))
# The first run (kept in exp072_gauge_toy_output_v1_bug.txt) used U^dag for the complex-phi row: a toy bug (not a gauge map
# for complex twist). Fixed to U^{-1}; the real-phi rows are unchanged by construction.
