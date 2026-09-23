"""EXP-026 side check (for proposing C11): EMI rectangles satisfy H_rect?
EMI: S = (c/2) closed-boundary double integral of n.n'/|x-y|^2.  For a T x L rectangle (y = T/L, L fixed), the finite part gives
g(y) = S'(y) + kappa = 2c[(1 + 1/y^2) arctan(1/y) - 1/y]  (kappa = pi c).  Claim: g = 2c * Laplace[mu](y) with
mu(t) = t Si(t) + sin(t)/t + cos(t) - 2 >= 0, so g is completely monotone.  Checked: (i) the closed form of g against direct
quadrature of the EMI double integral; (ii) the Laplace identity; (iii) mu >= 0."""
import mpmath as mp
mp.mp.dps = 30
c = 1
def S_emi(T, L):   # finite, L-fixed part of the EMI rectangle entropy (self-terms' log pieces + opposite-side pairs), up to constants
    pair = lambda a, d: 2*(a/d*mp.atan(a/d) - mp.log(1 + (a/d)**2)/2)      # int_0^a int_0^a dx dx'/((x-x')^2 + d^2)
    return (c/2)*(-4*mp.log(T) - 4*mp.log(L) - 2*pair(T, L) - 2*pair(L, T))
g_closed = lambda y: 2*c*((1 + 1/y**2)*mp.atan(1/y) - 1/y)
# (i) direct check: g = dS/dy + kappa at L = 1, including a quadrature re-evaluation of the opposite-pair integral
for y in (0.3, 1, 3, 10):
    dS = mp.diff(lambda t: S_emi(t, 1), y)
    quad_pair = mp.quad(lambda x: mp.quad(lambda xp: 1/((x - xp)**2 + 1), [0, x, y]), [0, y])
    print(f"y={y:>4}: g_closed = {mp.nstr(g_closed(y),12)}  dS/dy + pi c = {mp.nstr(dS + mp.pi*c,12)}   pair closed {mp.nstr(2*(y*mp.atan(y) - mp.log(1+y**2)/2),10)} vs quadrature {mp.nstr(quad_pair,10)}")
mu = lambda t: t*mp.si(t) + mp.sin(t)/t + mp.cos(t) - 2
# (ii) Laplace identity
for y in (0.5, 1, 2, 5):
    lap = mp.quad(lambda t: mp.e**(-y*t)*mu(t), [0, 1, 10, mp.inf])
    print(f"y={y}: 2c*Laplace[mu] = {mp.nstr(2*c*lap,12)}   g_closed = {mp.nstr(g_closed(y),12)}")
# (iii) mu >= 0
ts = [mp.mpf(10)**(-3 + 6*i/5999) for i in range(6000)]
m = min((mu(t)/t**2 if t < 1 else mu(t), t) for t in ts)
print(f"min over t in [1e-3, 1e3] of (mu/t^2 for t<1, mu for t>=1) = {mp.nstr(m[0],6)} at t = {mp.nstr(m[1],6)};  mu ~ t^2/3 at small t: mu(1e-3)/1e-6 = {mp.nstr(mu(mp.mpf('1e-3'))/mp.mpf('1e-6'),8)}")
print(f"mu'(t) = Si(t) + cos(t)/t - sin(t)/t^2 at t=0.5,2,5: {[mp.nstr(mp.diff(mu, t), 5) for t in (0.5, 2, 5)]}")
