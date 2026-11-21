"""EXP-072 pre-check (Tier 1 machinery): (P1) per-slice self-energy Sigma_k(rho) = Int dy e^{iky} Sigma(sqrt(rho^2+y^2)),
Sigma(x) = -1/(pi^3 |x|^5)  =>  closed form -(2k^2/(3 pi^3 rho^2)) K_2(k rho). (P2) finite-part 2D trace of Sigma_k against a
rank-1 Gaussian F(x',x) = g(x')g(x), g = e^{-|x|^2/(2s^2)}: position-space f.p. (subtract the Taylor terms of g(x') about x up to
2nd order, which carry the rho^-4 and rho^-2 singularities) vs the Fourier form Int d^2p/(2pi)^2 Sigma~_k(p)|g^(p)|^2 with
Sigma~_k(p) = -(1/(3pi^2))(k^2+p^2) log(k^2+p^2) (dim-reg, local terms dropped). The two differ by a LOCAL term
c1 Int g^2 + c2 Int |grad g|^2 + c3 k^2 Int g^2 (scheme); test that the difference is exactly of that form by varying s. [model: Opus 5.5]"""
import numpy as np, math
from scipy.integrate import quad
from scipy.special import kv
# P1
for k, rho in ((0.5, 0.3), (2.0, 1.0)):
    num = quad(lambda y: math.cos(k * y) * (-1 / (math.pi ** 3 * (rho * rho + y * y) ** 2.5)), 0, np.inf, limit=400)[0] * 2
    cl = -(2 * k * k / (3 * math.pi ** 3 * rho * rho)) * kv(2, k * rho)
    print(f"(P1) k={k} rho={rho}: numeric {num:.12e}  closed {cl:.12e}  rel {num/cl-1:+.1e}")
