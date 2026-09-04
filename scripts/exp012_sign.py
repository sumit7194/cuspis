"""
EXP-012: is the sign of the residual  a(theta) - a_BMW(theta)  universal?
Inputs are published numbers only (sources in comments); the only 'computation' is evaluating
closed forms.  Einstein/ECG residuals come from the validated exp001 modules.

Sources:
  smooth-limit coefficients sigma^(p), alpha=1..4:  Helmes et al PRB 94 125142 (2016) Tables 3 (complex boson, 8 coeffs)
                                                    and 4 (Dirac, 7 coeffs).  'All shown digits are significant.'
  kappa_n:  CHL09 Table 1 (n=1: 0.0794 complex scalar, 0.0722 Dirac); BMW15b Table 3 (n=2,3,4).
  BMW trial function: BMW15b eqs (6.2)-(6.7) = Helmes eq (21).
  Helmes 'new ansatz' eq (22): series to order 2M plus geometric tail with sigma^(p) -> 2 kappa/pi^(2p+3).
"""
import numpy as np
from math import pi, sqrt
boson = {  # sigma, sigma', then sigma''*1e5, s3*1e6, s4*1e7, s5*1e8, s6*1e9, s7*1e10
 1: [1/128, (20+3*pi**2)/(9216*pi**2), 5.34655497e-5, 5.40160621e-6, 5.45758486e-7, 5.51156763e-8, 5.57181927e-9, 5.63580458e-10],
 2: [1/(24*pi**2), (5+pi**2)/(480*pi**4), 3.11534753e-5, 3.12412616e-6, 3.14738400e-7, 3.17722233e-8, 3.21122771e-9, 3.24805958e-10],
 3: [1/(54*sqrt(3)*pi), (70*sqrt(3)*pi-81)/(116640*pi**2), 2.55467090e-5, 2.56091169e-6, 2.57924160e-7, 2.60327134e-8, 2.63086369e-9, 2.66084250e-10],
 4: [(8+3*pi)/(576*pi**2), 2.35688862e-4, 2.31261323e-5, 2.31844302e-6, 2.33503767e-7, 2.35676191e-8, 2.38170782e-9, 2.40881642e-10]}
fermi = {
 1: [1/128, (16+3*pi**2)/(9216*pi**2), 4.8129970e-5, 4.8552317e-6, 4.9173353e-7, 4.9777097e-8, 5.0411447e-9],
 2: [1/(64*pi), (35*pi-8)/(30720*pi**2), 3.19426062e-5, 3.18673787e-6, 3.21549955e-7, 3.25431008e-8, 3.29634926e-9],
 3: [5/(216*sqrt(3)*pi), (410*sqrt(3)*pi-891)/(466560*pi**2), 2.75858323e-5, 2.74706275e-6, 2.76940330e-7, 2.80182652e-8, 2.83766869e-9],
 4: [(1+6*sqrt(2))/(768*pi), 2.70052231e-4, 2.55831357e-5, 2.54609628e-6, 2.56597999e-7, 2.59563462e-8, 2.62867463e-9]}
kap = {'boson': {1:0.0794, 2:0.0455996, 3:0.037339, 4:0.033798}, 'fermi': {1:0.0722, 2:0.0472338, 3:0.040662, 4:0.0376674}}
angles = [('26.57',np.arctan(0.5)),('45',pi/4),('63.43',np.arctan(2.0)),('90',pi/2),('116.57',pi-np.arctan(2.0)),('135',3*pi/4),('153.43',pi-np.arctan(0.5))]

def trial(th, k, s):
    l1 = 2*pi*(k-3*pi*s)/(pi**2-6); l2 = -3*(2*k-pi**3*s)/(pi*(pi**2-6))
    return l1*(th-pi)**2/(th*(2*pi-th)) + l2*(1+(pi-th)/np.tan(th)), l1, l2
def series(th, c):   return sum(c[p]*(pi-th)**(2*p+2) for p in range(len(c)))
def ansatz22(th, c, k):
    M=len(c); eps=pi-th
    return series(th,c) + 2*k/pi**(2*M+1)*eps**(2*M+2)/(th*(2*pi-th))
def tail_asym(th, c, k):  # the geometric tail that (22) adds
    M=len(c); eps=pi-th; return 2*k/pi**(2*M+1)*eps**(2*M+2)/(th*(2*pi-th))

# control: reproduce Helmes Table 1/2 'series' and 'ansatz' entries
print("CONTROL (must match Helmes Tables 1-2): boson a=1 series@90 = %.5f (table 0.02367); ansatz22@45 = %.4f (table 0.0810); fermi a=2 series@135 = %.6f (table 0.003204); fermi a=1 ansatz22@26.57 = %.3f (table 0.146)"
      % (series(pi/2,boson[1]), ansatz22(pi/4,boson[1],kap['boson'][1]), series(3*pi/4,fermi[2]), ansatz22(np.arctan(0.5),fermi[1],kap['fermi'][1])))
print()
print("A. Sign near theta=pi:  sigma' (exact) vs sigma'_trial = l1/pi^4 + l2/45.   residual ~ (sigma' - sigma'_trial) eps^4")
for name,tab in (('boson',boson),('fermi',fermi)):
    for a,c in tab.items():
        s,sp=c[0],c[1]; k=kap[name][a]; _,l1,l2=trial(pi/2,k,s)
        spt=l1/pi**4+l2/45; sppt=l1/pi**6+2*l2/945
        print(f"  {name:5s} n={a}: sigma'={sp:.6e} trial={spt:.6e}  (trial-exact)/exact={(spt/sp-1)*100:+.2f}% ;  sigma''={c[2]:.4e} trial={sppt:.4e} {(sppt/c[2]-1)*100:+.2f}%")
print()
print("B. Signed residual (trial - a)/a in %, seven Helmes angles.  theta>=90: a = exact series (truncation < 1e-4 rel).")
print("   theta<90: a = Helmes eq.(22); its own error is one-sided (22 is a LOWER bound) and bounded by r*tail, r = last coefficient's excess over asymptotic.")
for name,tab in (('boson',boson),('fermi',fermi)):
    for a,c in tab.items():
        k=kap[name][a]; s=c[0]; M=len(c)
        r = c[-1]*pi**(2*(M-1)+3)/(2*k) - 1     # excess of the last known coefficient over 2k/pi^(2p+3)
        out=[]
        for lab,th in angles:
            t,_,_=trial(th,k,s)
            if th>=pi/2-1e-9: aval=series(th,c); err=0.0
            else: aval=ansatz22(th,c,k); err=abs(r)*tail_asym(th,c,k)/aval*100
            out.append(f"{lab:>6}:{(t/aval-1)*100:+.2f}" + (f"(±{err:.2f})" if err>0 else ""))
        print(f"  {name:5s} n={a} (r={r:+.3f}): " + "  ".join(out))
