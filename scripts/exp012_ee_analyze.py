"""EXP-012: analyse an EXP-004 result file for the real scalar (mode ee, or renyi2 as a dry run).
Order is fixed in advance: (1) contact with published values; (2) smooth limit; (3) residual vs the BMW trial
function at all angles (sign, node); (4) a0 from the sharp end with kappa FIXED, drift under window and degree.
Usage: exp012_ee_analyze.py result.json"""
import sys, json, numpy as np
from math import pi
sys.path.insert(0, __file__.rsplit('/',1)[0])
from exp012_sign import boson, kap, series, ansatz22, trial
res=json.load(open(sys.argv[1])); mode=res['mode']; deg=np.array(res['deg']); s=np.array(res['s']); th=np.radians(deg)
n = 1 if mode in ('ee','eehp') else 2
c=[x/2 for x in boson[n]]            # complex -> real scalar
k=kap['boson'][n]/2; sig=c[0]; sigp=c[1]
CT=3/(32*pi**2)
print(f"mode={mode} (real scalar, n={n}) nodes={res['nodes']} failures={res['failures']} nt={res['nt']} t_max={res['t_max']}")
if mode in ('ee','eehp'): print(f"sigma from H1: {res['sigma_from_H1']:.10e} exact 1/256={1/256:.10e} ratio {res['sigma_from_H1']*256:.8f};  sigma' from H3: {res['sigmap_from_H3']:.10e} exact {sigp:.10e} ratio {res['sigmap_from_H3']/sigp:.8f}")
print("\n(1) CONTACT WITH PUBLISHED VALUES  [HHCWM16 Table 1 alpha=%d, complex/2; series exact to <1e-4 at >=90, 7e-4 at 63.4; eq22 below; CHL09 exact at 90,135 for n=1]"%n)
chl = {90:0.02366/2, 135:0.005040/2} if n==1 else {}
worst=0
for d,v in zip(deg,s):
    t=np.radians(d)
    if d>=63: ref=series(t,c); kind='series'
    else: ref=ansatz22(t,c,k); kind='eq22'
    line=f"  {d:8.3f}  s={v:.6e}  ref={ref:.6e}  ratio-1={v/ref-1:+.2e} ({kind})"
    if int(d) in chl and abs(d-int(d))<1e-9: line+=f"   CHL09 {chl[int(d)]:.6e} ratio-1={v/chl[int(d)]-1:+.2e}"
    if 63<=d<=160: worst=max(worst,abs(v/ref-1))
    print(line)
print(f"  worst |ratio-1| vs exact series on 63.4-160 deg: {worst:.2e}   -> P3 {'PASS' if worst<2e-3 else 'FAIL'} (criterion 2e-3; series itself 7e-4 at 63.4)")
# below 63.4: eq22 is a LOWER bound with one-sided error <= r*tail; r = last coefficient's excess over 2k/pi^(2p+3)
M=len(c); r=c[-1]*pi**(2*(M-1)+3)/(2*k)-1
print(f"  15-45 deg vs eq22 (lower bound; its one-sided error <= r*tail with r={r:+.4f}):")
for d in (15.0,20.0,26.565,30.0,40.0,45.0):
    i=list(deg).index(d); t=th[i]; ref=ansatz22(t,c,k); tail=2*k/pi**(2*M+1)*(pi-t)**(2*M+2)/(t*(2*pi-t)); bound=abs(r)*tail/ref
    dev=s[i]/ref-1; ok = (-1e-4 <= dev <= bound+1e-4)
    print(f"    {d:7.3f}: s/eq22-1 = {dev:+.2e}   allowed [-1e-4, +{bound:.1e}]  {'ok' if ok else 'OUT'}")
print("\n(2) SMOOTH LIMIT")
for d in (170.0,160.0,150.0):
    i=list(deg).index(d); e=pi-th[i]; ref=sum(c[p]*e**(2*p+2) for p in range(len(c)))
    print(f"  {d}: s/series-1 = {s[i]/ref-1:+.2e}")
print("\n(3) RESIDUAL vs BMW TRIAL (sigma, kappa) = (%.6g, %.6g): (trial - s)/s in %%; sign changes flagged" % (sig,k))
prev=None
for d,v in zip(deg,s):
    t=np.radians(d); tr,_,_=trial(t,k,sig); r=(tr/v-1)*100
    flag = "  <-- SIGN CHANGE" if (prev is not None and np.sign(r)!=np.sign(prev)) else ""
    print(f"  {d:8.3f}  trial={tr:.6e}  s={v:.6e}  residual={r:+.3f}%{flag}"); prev=r
print("\n(4) SHARP END: a0 with kappa FIXED = %.5g (CHL09/2). Fit s - kappa/theta = a0 + a1 th + a2 th^2 (+ a3 th^3) on windows; drift is the uncertainty." % k)
resid = s - k/th
print('  (5 and 10 deg are excluded: the M<=15 mass truncation makes them 8% and 0.5% low at n=2, measured against eq22 in the dry run)')
for lo,hi in ((15,30),(15,40),(15,45),(20,50),(26,60)):
    m=(deg>=lo)&(deg<=hi); x=th[m]; y=resid[m]
    for degp in (2,3):
        A=np.vstack([x**j for j in range(degp+1)]).T; coef,*_=np.linalg.lstsq(A,y,rcond=None)
        print(f"  window {lo:2d}-{hi:2d} deg, degree {degp}: a0 = {coef[0]:+.5f}  (units of a; /C_T = {coef[0]/CT:+.4f})   a1={coef[1]:+.4f}")
print("  cross-check with kappa FREE (15-45 deg, kappa/theta + a0 + a1 th + a2 th^2):")
m=(deg>=15)&(deg<=45); x=th[m]; A=np.vstack([1/x, np.ones_like(x), x, x**2]).T; coef,*_=np.linalg.lstsq(A,s[m],rcond=None)
print(f"    kappa_fit = {coef[0]:.5f} (fixed value {k:.5f}, ratio {coef[0]/k:.4f}); a0 = {coef[1]:+.5f}")
a0trial = -0.75*2*pi*(k-3*pi*sig)/(pi**2-6)
print(f"\n  trial function's a0~ = {a0trial:+.5f} (= {a0trial/CT:+.4f} C_T).  P1: a0 <= 0 ?   P2: node iff a0 > {-a0trial:+.5f}")
