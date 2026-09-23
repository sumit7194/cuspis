"""EXP-028 extractor for kappa and sigma from a corner function sampled on the instrument's angle grid (DEG in exp004_prod).
kappa: theta*A(theta) fitted by a polynomial in theta over the small-angle points; sigma: A/(pi-theta)^2 fitted by a polynomial in
eps^2 over the near-pi points.  Variants (nuisance sweep) are reported with their spread."""
import numpy as np
from math import pi
DEG = [5,10,15,20,26.565,30,40,45,50,60,63.435,70,80,90,100,110,116.565,120,130,135,140,150,153.435,160,170]
TH = np.radians(DEG)
K_VARIANTS = {"cubic 5-20": ([5,10,15,20], 3), "quad 5-15": ([5,10,15], 2), "cubic LSQ 5-26.6": ([5,10,15,20,26.565], 3), "quartic 5-26.6": ([5,10,15,20,26.565], 4)}
S_VARIANTS = {"eps^4 150-170": ([150,153.435,160,170], 2), "eps^2 153-170": ([153.435,160,170], 1), "eps^6 140-170": ([140,150,153.435,160,170], 3)}
def kappa(A, variant):
    degs, deg = K_VARIANTS[variant]; idx = [DEG.index(d) for d in degs]; th = TH[idx]
    return np.polyfit(th, th*np.asarray(A)[idx], deg)[-1]
def sigma(A, variant):
    degs, deg = S_VARIANTS[variant]; idx = [DEG.index(d) for d in degs]; e = pi - TH[idx]
    return np.polyfit(e**2, np.asarray(A)[idx]/e**2, deg)[-1]
def ratio_table(A):
    out = {}
    for kv in K_VARIANTS:
        for sv in S_VARIANTS: out[(kv, sv)] = kappa(A, kv)/sigma(A, sv)
    return out
if __name__ == "__main__":
    emi = 1 + (pi - TH)/np.tan(TH)
    r = ratio_table(emi)
    print("KNOWN-ANSWER TEST of the extractor on exact EMI samples (target 3pi = %.10f):" % (3*pi))
    for k, v in r.items(): print(f"   {k[0]:18s} | {k[1]:14s}: kappa/sigma = {v:.8f}   abs err {v-3*pi:+.2e}   rel {v/(3*pi)-1:+.2e}")
    print(f"   kappa (cubic 5-20) = {kappa(emi,'cubic 5-20'):.8f} vs pi;  sigma (eps^4 150-170) = {sigma(emi,'eps^4 150-170'):.10f} vs 1/3")
