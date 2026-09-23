"""EXP-020: effect of the failed (skipped) Dirac EE nodes on the assembled s(theta). Two independent fill-ins per failed node:
(i) log-linear extrapolation in t from the two nearest converged t-nodes at the same M; (ii) log-linear interpolation in M
from the nearest converged masses at the same t. Reports each node's weighted contribution relative to s(theta)."""
import json, glob, numpy as np
from math import pi
DEG=[5,10,15,20,26.565,30,40,45,50,60,63.435,70,80,90,100,110,116.565,120,130,135,140,150,153.435,160,170]
n1=n2=24; pmax=15.0; nt=14; tmax=3.2
x1,w1=np.polynomial.legendre.leggauss(n1); x2,w2=np.polynomial.legendre.leggauss(n2)
ps=np.concatenate([2*(x1+1),4+0.5*(pmax-4)*(x2+1)]); wps=np.concatenate([2*w1,0.5*(pmax-4)*w2])
xt,wt=np.polynomial.legendre.leggauss(nt); ts=0.5*tmax*(xt+1); wts=0.5*tmax*wt
Ms=[float(np.sqrt(0.25+p*p)) for p in ps]
recs={}
for f in glob.glob('exp004_nodes/dirac_*.json'):
    d=json.load(open(f)); recs[(round(d['M'],10),round(d['t'],10))]=d
res=json.load(open('exp004_dirac_result_n24_24_p15.0_t14.json')); s=np.array(res['s'])
def good(iM,it):
    r=recs.get((round(Ms[iM],10),round(float(ts[it]),10))); return np.array(r['Psi_re']) if r and r.get('ok') else None
def loglin(a,b,xa,xb,x):
    out=np.empty(25)
    for k in range(25):
        if a[k]*b[k]>0: out[k]=np.sign(a[k])*np.exp(np.log(abs(a[k]))+(np.log(abs(b[k]))-np.log(abs(a[k])))*(x-xa)/(xb-xa))
        else: out[k]=a[k]+(b[k]-a[k])*(x-xa)/(xb-xa)
    return out
failed=[(iM,it) for iM in range(len(Ms)) for it in range(nt) if good(iM,it) is None]
print(f"{len(failed)} failed nodes: " + ", ".join(f"(M={Ms[i]:.3f}, t={ts[j]:.3f})" for i,j in failed))
tot1=np.zeros(25); tot2=np.zeros(25)
for iM,it in failed:
    t=ts[it]; wgt=wts[it]*(1/(2*np.sinh(pi*t)**2))*2*wps[iM]*ps[iM]**2
    lower=[j for j in range(it-1,-1,-1) if good(iM,j) is not None][:2]
    f1=loglin(good(iM,lower[1]),good(iM,lower[0]),ts[lower[1]],ts[lower[0]],t) if len(lower)==2 else np.full(25,np.nan)
    below=[i for i in range(iM-1,-1,-1) if good(i,it) is not None][:1]; above=[i for i in range(iM+1,len(Ms)) if good(i,it) is not None][:1]
    if below and above: f2=loglin(good(below[0],it),good(above[0],it),Ms[below[0]],Ms[above[0]],Ms[iM])
    elif len(below)>=1:
        b2=[i for i in range(iM-1,-1,-1) if good(i,it) is not None][:2]; f2=loglin(good(b2[1],it),good(b2[0],it),Ms[b2[1]],Ms[b2[0]],Ms[iM])
    else: f2=np.full(25,np.nan)
    c1=wgt*f1; c2=wgt*f2; tot1+=np.nan_to_num(c1); tot2+=np.nan_to_num(c2)
    print(f"  M={Ms[iM]:.3f} t={t:.3f}: weight {wgt:.1e}; contribution/s at 20,45,90,135 deg: fill(i) " +
          " ".join(f"{c1[k]/s[k]:+.1e}" for k in (3,7,13,19)) + "  fill(ii) " + " ".join(f"{c2[k]/s[k]:+.1e}" for k in (3,7,13,19)))
print("TOTAL of all failed nodes, relative to s:")
for lab,k in (("5",0),("15",2),("20",3),("26.6",4),("45",7),("90",13),("135",19),("170",24)):
    print(f"  {lab:>5} deg: fill(i) {tot1[k]/s[k]:+.2e}   fill(ii) {tot2[k]/s[k]:+.2e}")
