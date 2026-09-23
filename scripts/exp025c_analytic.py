"""EXP-025c: analytic form of the EXP-025b LP optima (given CC at n = 1, plus C3, C5).
For admissible a:  kappa/4 = F(0) >= F(v) - v F'(v) = (sqrt v/2) a(theta_v) + (2v/(1+v)) b(theta_v),  b = -a',  theta_v = 4 arctan sqrt v.
C3 + C5  =>  g = b tan(theta/2) nonincreasing, g -> 4 sigma at pi  =>  b >= 4 sigma cot(theta/2), a >= a_min = 8 sigma log(1/sin(theta/2)).
With tau = tan(theta/4):  kappa >= 16 sigma * phi(tau),  phi(tau) = tau [ log((1+tau^2)/(2 tau)) + (1-tau^2)/(1+tau^2) ].
For a(pi/2) normalisation (maximiser below 90 deg): on [theta, pi/2], g >= g(pi/2) >= a(pi/2)/ln 2  =>  kappa/a(pi/2) >= 4 phi*/ln 2.
The extremal (a = c a_min above theta*, F linear in u below) attains both, so they are optimal for {CC, C2, C3, C5}."""
import mpmath as mp
mp.mp.dps = 40
phi = lambda t: t*(mp.log((1 + t**2)/(2*t)) + (1 - t**2)/(1 + t**2))
tstar = mp.findroot(lambda t: mp.diff(phi, t), 0.37)
ps = phi(tstar); thstar = 4*mp.atan(tstar)
print(f"tau*   = {mp.nstr(tstar, 20)}   theta* = {mp.nstr(thstar*180/mp.pi, 15)} deg")
print(f"phi*   = {mp.nstr(ps, 20)}")
print(f"kappa/sigma   >= 16 phi*          = {mp.nstr(16*ps, 15)}      (LP2 at N = 3200: 7.036437)")
print(f"kappa/C_T     >= (2 pi^2/3) phi*   = {mp.nstr(2*mp.pi**2/3*ps, 15)}      (LP2 x pi^2/24: 2.89362)")
print(f"kappa/a(pi/2) >= 4 phi*/ln 2       = {mp.nstr(4*ps/mp.log(2), 15)}      (LP1 at N = 3200: 2.537858)")
print(f"theta* < 90 deg (needed for the a(pi/2) form): {thstar < mp.pi/2}")
# check that the maximiser is interior and unique on a grid
import numpy as np
ts = np.linspace(1e-4, 1 - 1e-4, 200001); vals = ts*(np.log((1 + ts**2)/(2*ts)) + (1 - ts**2)/(1 + ts**2))
print(f"grid max phi = {vals.max():.12f} at tau = {ts[vals.argmax()]:.6f};  phi(1) = {vals[-1]:.3e} (-> 0 at the smooth end)")
# the extremal: a = c*a_min on [theta*, pi], F linear in u below, tangent at u* -- check C2, C3 on the linear part
from math import pi
sig = 1.0; ust = float(tstar)**2
Fmin = lambda u: np.sqrt(u)*8*sig*np.log(1/np.sin(2*np.arctan(np.sqrt(u))))
h = 1e-7; dF = (Fmin(ust + h) - Fmin(ust - h))/(2*h)
Flin = lambda u: Fmin(ust) + dF*(u - ust)
th = np.linspace(0.01, 4*np.arctan(np.sqrt(ust)) - 1e-3, 4000); u = np.tan(th/4)**2
a = Flin(u)/np.sqrt(u)
ap = np.gradient(a, th); app = np.gradient(ap, th)
chl = app + ap/np.sin(th)
print(f"extremal on the linear part (theta < theta*): a decreasing {np.all(ap < 0)}, convex {np.all(app[2:-2] > 0)}, C3 margin min CHL[a]/|a''| = {np.min(chl[2:-2]/np.abs(app[2:-2])):+.3e}")
print(f"extremal kappa/sigma = 4 F(0) = {4*Flin(0.0):.10f}")
