import numpy as np, warnings
from scipy.integrate import quad
warnings.filterwarnings("ignore")
def abar(th): return 1+(np.pi-th)/np.tan(th)
def Fbar(u):
    th=4*np.arctan(np.sqrt(u)); return np.sqrt(u)*abar(th)
def Fbarp(u,h=1e-5): return (Fbar(u+h)-Fbar(u-h))/(2*h)

def eye_arc(up):
    Xp=1/np.sqrt(up); cp=(1-Xp**2)/2; rp=1-cp
    a_end=np.arctan2(-cp,-Xp)
    if a_end<np.pi/2: a_end+=2*np.pi
    z=lambda al: rp*np.exp(1j*al)+1j*cp
    dz=lambda al: 1j*rp*np.exp(1j*al)
    return z,dz,np.pi/2,a_end
def ellipse_arc(A):
    z=lambda al: A*np.cos(al)+1j*np.sin(al)
    dz=lambda al: -A*np.sin(al)+1j*np.cos(al)
    return z,dz,np.pi/2,np.pi      # upper-left quarter; lower by symmetry
def R(u,arc):
    zf,dzf,a0,a1=arc; su=np.sqrt(u); k=su/2
    def geo(al):
        z=zf(al); w=(2/su)*np.arctanh(su*z); dw=2*dzf(al)/(1-u*z*z)
        return w.real,w.imag,dw.imag
    def I(V,dphi):
        s2=np.sin(k*dphi)**2; b=1-s2; Y=np.tanh(k*V)
        return quad(lambda y:(1-y*y)/(s2+b*y*y)**2,-1,Y,epsabs=1e-13,epsrel=1e-11,limit=200)[0]/k
    def outer(alp):
        Tp,php,dpp=geo(alp)
        def inner(al):
            T,ph,dp=geo(al); V=T+Tp
            return abs(dp)*(I(V,ph-php)+I(V,-ph-php))
        return abs(dpp)*quad(inner,a0,a1,epsabs=1e-11,epsrel=1e-9,limit=200)[0]
    return 2*(u**2/16)*quad(outer,a0,a1,epsabs=1e-10,epsrel=1e-8,limit=200)[0]
