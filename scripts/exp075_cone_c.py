"""EXP-075 pre-check: coincident coefficient of the twisted 3D propagator near a single twist line (cone at n=1 continuation),
a^(beta)(r) = G_beta(x,x) - G_0(x,x) = c(beta)/r.  Mode form: c = (1/(2 pi^2)) Int_0^inf du Sum_m [I_nu K_nu(u) - I_|m| K_|m|(u)],
nu = m+beta (m>=0), -(m+beta) (m<0) [regular modes, as exp069 exact_G1].
Route 1: per-mode Mellin regularisation -> c = -(1/(4 pi^2)) T(beta), T = Sum_j [psi(j+beta+1/2) - psi(j+1/2) + psi(j+3/2-beta) - psi(j+3/2)].
Route 2 (independent): direct u-quadrature of the mode-summed integrand, real beta. [model: Opus 5.5]"""
import mpmath as mp
mp.mp.dps = 25
def c_psi(beta):
    T = mp.nsum(lambda j: mp.digamma(j + beta + 0.5) - mp.digamma(j + 0.5) + mp.digamma(j + 1.5 - beta) - mp.digamma(j + 1.5), [0, mp.inf])
    return -T / (4 * mp.pi ** 2)
def c_direct(beta, M=400):
    def S(u):
        s = mp.besseli(0, u) * mp.besselk(0, u) * 0
        tot = 0
        for m in range(-M, M + 1):
            nu = m + beta if m >= 0 else -(m + beta)
            tot += mp.besseli(nu, u) * mp.besselk(nu, u) - mp.besseli(abs(m), u) * mp.besselk(abs(m), u)
        return tot
    return mp.quad(S, [0, 1, 5, 20, 80]) / (2 * mp.pi ** 2)
if __name__ == "__main__":
    for b in (0.5, 0.3):
        print(f"beta={b}: psi route c={mp.nstr(c_psi(b), 12)}", flush=True)
    mp.mp.dps = 15
    print("direct (M=60 modes, u<=80; truncation-limited):", mp.nstr(c_direct(0.3, M=60), 8), flush=True)

def C_line(g, smax=8):
    """C[g] = Int_0^inf ds pi/cosh^2(pi s) g(1/2+is)  (EXP-071 KF0-verified continuation)."""
    return mp.quad(lambda s: mp.pi / mp.cosh(mp.pi * s) ** 2 * g(mp.mpf(0.5) + 1j * s), [0, 1, 3, smax])
def line_report():
    mp.mp.dps = 20
    for s in (0, 0.5, 1, 2, 4):
        v = c_psi(mp.mpf(0.5) + 1j * s); print(f"  c(1/2+{s}i) = {mp.nstr(v, 10)}", flush=True)
    C1 = C_line(c_psi); C3 = C_line(lambda b: c_psi(b) ** 3)
    print(f"  C[c]   = {mp.nstr(C1, 10)}   (honest coincident a_n = (n-1) C[c]/r + O((n-1)^2): linear, as expected)", flush=True)
    print(f"  C[c^3] = {mp.nstr(C3, 10)}   (SC's F1 cubic-log weight; the honest integer-n cubic is d/dn[n a_n^3]|_1 = 0)", flush=True)
    print(f"  ratio C[c^3]/C[c]^3 = {mp.nstr(C3 / C1 ** 3, 6)}", flush=True)
