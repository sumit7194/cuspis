"""EXP-033 (pre-registered in report.md): A5 in mutual-information form, tested in the EMI model.
Two wedges with a common apex, scale-covariant framing eps(r) = eta*r: A- = wedge of angle theta-2eta, A+ = the
complementary wedge of angle 2pi-theta-2eta (gaps 2eta on both sides).  EMI: I(A,B) = int_A int_B |x-y|^-4 (C = 1).
Per unit log-scale: Ical(theta,eta) = int_{W1} int_{W2} g(phi2-phi1),  g(psi) = int_0^inf lam dlam /(1+lam^2-2 lam cos psi)^2
                                    = [1 + (pi-psi) cot psi] / (2 sin^2 psi)   (closed form, checked below by quadrature).
Prediction: D(theta,eta) = Ical(theta,eta) - Ical(pi,eta) -> K [1 + (pi-theta) cot theta], one K for all theta.
Control: the 1/eta coefficient is theta-independent."""
import mpmath as mp
mp.mp.dps = 30
pi = mp.pi
def g(p):  # stable form in x = pi - psi (even in x): g = (1 - x cot x)/(2 sin^2 x); series near x = 0 (g(pi) = 1/6)
    x = pi - p
    if abs(x) < mp.mpf('1e-8'):
        return mp.mpf(1)/6 + x**2*(mp.mpf(1)/45 + mp.mpf(1)/9)/2   # (x^2/3 + x^4/45)/(2(x^2 - x^4/3)) to O(x^2)
    return (1 - x*mp.cot(x))/(2*mp.sin(x)**2)
for p in (mp.mpf('0.3'), mp.mpf(2), mp.mpf(4), pi - mp.mpf('1e-9')):        # closed form vs direct quadrature
    q = mp.quad(lambda l: l/(1 + l**2 - 2*l*mp.cos(p))**2, [0, 1, mp.inf])
    print(f"g closed form vs quadrature at psi={p}: rel diff {mp.nstr(abs(g(p)/q - 1), 3)}")

def Ical(th, eta):
    L1, L2 = th - 2*eta, 2*pi - th - 2*eta
    a2 = th/2 + eta
    def w(p):  # overlap length of {phi1 in [-L1/2, L1/2]} with {phi2 - p : phi2 in [a2, a2+L2]}
        return max(mp.mpf(0), min(L1/2, a2 + L2 - p) - max(-L1/2, a2 - p))
    bps = sorted({2*eta, min(th, 2*pi - th), max(th, 2*pi - th), 2*pi - 2*eta})
    return mp.quad(lambda p: g(p)*w(p), bps)

EMI = lambda th: 1 + (pi - th)*mp.cot(th)
thetas = [mp.radians(d) for d in (20, 45, 60, 90, 120, 150)]
etas = [mp.mpf('1e-2'), mp.mpf('1e-3'), mp.mpf('1e-4')]
print("\n1/eta coefficient (control: theta-independent), estimated as eta*Ical at eta=1e-4:")
for th in thetas + [pi]:
    print(f"  theta={mp.nstr(mp.degrees(th),5):>6} deg: eta*Ical = {mp.nstr(etas[-1]*Ical(th, etas[-1]), 12)}")
print("\nD(theta,eta)/EMI(theta) (prediction: one constant K for all theta, as eta -> 0):")
ref = {e: Ical(pi, e) for e in etas}
Ks = []
for th in thetas:
    r = [(Ical(th, e) - ref[e])/EMI(th) for e in etas]
    ext = r[-1] + (r[-1] - r[-2])*(etas[-1]/(etas[-2] - etas[-1]))   # linear-in-eta Richardson step
    Ks.append(ext)
    print(f"  theta={mp.nstr(mp.degrees(th),5):>6} deg: " + "  ".join(mp.nstr(x, 10) for x in r) + f"   -> extrap {mp.nstr(ext, 10)}")
spread = (max(Ks) - min(Ks))/abs(sum(Ks)/len(Ks))
print(f"\nrelative spread of K across theta: {mp.nstr(spread, 3)}   (K mean {mp.nstr(sum(Ks)/len(Ks), 10)})")
fin = [Ical(pi, e) - (etas[-1]*Ical(pi, etas[-1]))/e for e in etas[:2]]
print("finite part of Ical(pi,eta) (is the pi-subtraction needed?):", [mp.nstr(x, 8) for x in fin])
