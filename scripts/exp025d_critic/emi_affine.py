# Known-answer control for the claimed n=1 derivation, using the extensive-mutual-information (EMI)
# model, which satisfies SSA, purity and Moebius invariance.  For EMI, f'(0+)-f'(inf) = C*R exactly,
# with R = lim (1/Delta) B(right layer, H_inf \ h).  With a = (C/4) abar, the claim "X(u,u') affine in u,
# X(u',u') = F(u')" becomes:  G(u) := Fbar(u) - 4 R(u,u')  is affine in u (for u<u').
import numpy as np
from scipy.integrate import quad
import sys

def abar(th): return 1+(np.pi-th)/np.tan(th)
def Fbar(u):
    th=4*np.arctan(np.sqrt(u)); return np.sqrt(u)*abar(th)

def make(u,up):
    Xp=1/np.sqrt(up); cp=(1-Xp**2)/2; rp=1-cp
    a_end=np.arctan2(-cp,-Xp)
    su=np.sqrt(u)
    def geo(al):
        z=rp*np.exp(1j*al)+1j*cp
        w=(2/su)*np.arctanh(su*z)
        dw=2j*rp*np.exp(1j*al)/(1-u*z*z)
        return w.real, w.imag, dw.imag
    return geo,a_end

def Iinner(V,dphi,u):
    k=np.sqrt(u)/2; s2=np.sin(k*dphi)**2; b=1-s2
    Y=np.tanh(k*V)
    f=lambda y:(1-y*y)/(s2+b*y*y)**2
    val,err=quad(f,-1,Y,epsabs=1e-13,epsrel=1e-11,limit=200,points=None)
    return val/k

def R(u,up):
    geo,a_end=make(u,up)
    # parameter al in [pi/2, a_end]; upper arc. lower arc: phi -> -phi, T same.
    def integrand_layer(alp):
        Tp,php,dpp=geo(alp)
        def inner(al):
            T,ph,dp=geo(al)
            V=T+Tp
            tot=Iinner(V,ph-php,u)+Iinner(V,-ph-php,u)   # D on upper + lower arc
            return abs(dp)*tot
        v,e=quad(inner,np.pi/2,a_end,epsabs=1e-11,epsrel=1e-9,limit=200)
        return abs(dpp)*v
    v,e=quad(integrand_layer,np.pi/2,a_end,epsabs=1e-10,epsrel=1e-8,limit=200)
    return 2*(u**2/16)*v   # factor 2: layer on upper + lower arc (symmetry)

if __name__=="__main__":
    up=float(sys.argv[1]); us=[float(x) for x in sys.argv[2:]]
    for u in us:
        r=R(u,up)
        print(f"u'={up} u={u:.4f} R={r:.10f} Fbar(u)={Fbar(u):.10f} G=Fbar-4R={Fbar(u)-4*r:.10f}",flush=True)
    print("Fbar(u')=",Fbar(up))
    h=1e-5; print("Fbar'(u')=",(Fbar(up+h)-Fbar(up-h))/(2*h))
