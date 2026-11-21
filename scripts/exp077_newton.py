"""EXP-077 (pre-check, unregistered): a route to Q'(1) on the T37/T40 P4' replica lattice that uses NO Abel-Plana formula:
honest integer-n values Q(n) = logdet B_n - n logdet B_1 on the explicitly glued n-sheet lattice (exp077_p4_reference.py
geometry), n = 1..Nmax, then the Newton forward-difference (Noerlund-Rice) series for the derivative at n = 1:
  Q'(1) = sum_{k>=1} (-1)^{k+1} Delta^k Q(1) / k,
valid for the Carlson-admissible interpolant (exponential type < pi in the right half-plane). Computed in mpmath at 50 dps
from double-precision Q(n) (each ~1e-13), so the k-th difference carries ~2^k * 1e-13 noise: report the partial sums.
T40 claim to test: Q'(1) = -1.386871934267. [model: Opus 5.5]"""
import numpy as np, mpmath as mp
from exp077_p4_reference import H_Mn
mp.mp.dps = 50
def Q(n, ld1):
    G = np.linalg.inv(H_Mn(n)); s, ld = np.linalg.slogdet(2 * G * G); return ld - n * ld1
G1 = np.linalg.inv(H_Mn(1)); ld1 = np.linalg.slogdet(2 * G1 * G1)[1]
Nmax = 34
Qs = [mp.mpf(Q(n, ld1)) for n in range(1, Nmax + 1)]
print("Q(1..6):", [mp.nstr(q, 12) for q in Qs[:6]])
diffs = list(Qs); S = mp.mpf(0)
for k in range(1, Nmax):
    diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
    term = (-1) ** (k + 1) * diffs[0] / k; S += term
    if k <= 6 or k % 4 == 0:
        print(f"k={k:2d}: Delta^k Q(1) = {mp.nstr(diffs[0], 6):>14}  partial Q'(1) = {mp.nstr(S, 14)}")
print("T40 claim: -1.386871934267")

def accelerate(Kmax_list=(20, 24, 28, 31)):
    """Levin-u and Wynn-epsilon on the Newton partial sums (terms ~ C r^k / k, linear convergence)."""
    diffs = list(Qs); terms = []
    for k in range(1, Nmax):
        diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
        terms.append((-1) ** (k + 1) * diffs[0] / k)
    for K in Kmax_list:
        t = terms[:K]
        lev = mp.levin(method="levin", variant="u")
        try:
            v_lev = lev.update_psum([mp.fsum(t[:j + 1]) for j in range(K)])[0]
        except Exception as e:
            v_lev = mp.nan
        S = [mp.fsum(t[:j + 1]) for j in range(K)]
        v_wynn = mp.shanks(S)[-1][-1]
        print(f"  K={K}: raw {mp.nstr(S[-1], 10)}  Levin-u {mp.nstr(v_lev, 10)}  Wynn/Shanks {mp.nstr(v_wynn, 10)}", flush=True)
