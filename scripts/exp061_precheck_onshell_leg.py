"""EXP-061 pre-check 3 (characterisation): on-shell value of the n = 1 self-energy in the Legendre continuation,
Sigma~_Leg(k, w) = -(4/(3 pi^2)) f.p. Int_1^inf P_{-1/2+ik}(c) Q''_{w-1/2}(c) dc.
Near c = 1: P Q'' = 1/(2(c-1)^2) + B/(c-1) + integrable, B = -(k^2+w^2)/4 (derived; vanishes on-shell k = i w).
f.p. = lim_{eps->0} [ I(1+eps) - 1/(2 eps) + B ln eps ];  eps swept as the nuisance. [model: Opus 5.5]"""
from mpmath import mp, mpf, mpc, quad, exp, legenp, legenq, re, log, pi, ceil, log10
mp.dps = 20
def Qpp(nu, c):
    extra = int(ceil(2 * max(0, -log10(c - 1)))) + 10
    with mp.workdps(mp.dps + extra):
        c = mpf(c); Q0 = re(legenq(nu, 0, c, type=3)); Q1 = re(legenq(nu + 1, 0, c, type=3))
        Qp = (nu + 1) * (Q1 - c * Q0) / (c * c - 1)
        v = (2 * c * Qp - nu * (nu + 1) * Q0) / (1 - c * c)
    return +v
def Iint(mu, nu, eps):
    f = lambda s: exp(s) * re(legenp(mu, 0, 1 + exp(s), type=3)) * Qpp(nu, 1 + exp(s))
    return quad(f, [log(eps), -8, -3, 0, 3, 8, 20, 40])
def fp(k, w, eps):
    mu = mpc(-0.5, 0) + 1j * k; mu = re(mu) if abs(mu.imag) < 1e-30 else mu; nu = w - mpf(0.5); B = -(k * k + w * w) / 4
    return re(Iint(mu, nu, eps) - 1 / (2 * eps) + B * log(eps))
if __name__ == "__main__":
    PRED = {'0.5': mpf(-1)/16 - mpf('0.25') + mpf('0.0625'), '0.65': mpf('-0.281875'), '0.8': mpf('-0.3025')}  # stated before this run from the 3-point form -1/16 - w/2 + w^2/4
    for w in (mpf('0.1'), mpf('0.2'), mpf('0.35'), mpf('0.5'), mpf('0.65'), mpf('0.8')):
        for k, lab in ((1j * w, "on-shell k=i w"), (mpf(1), "off-shell k=1")):
            vals = [fp(k, w, mpf(e)) for e in ('1e-4', '1e-6', '1e-8')]
            print(f"w={w} {lab}: f.p. at eps=1e-4,1e-6,1e-8: " + ", ".join(mp.nstr(v, 12) for v in vals)
                  + f"   -> Sigma~_Leg = {mp.nstr(-4/(3*pi**2)*vals[-1], 10)}"
                  + (f"   [unseen-point prediction {mp.nstr(PRED[mp.nstr(w,3)],8)}: diff {mp.nstr(vals[-1]-PRED[mp.nstr(w,3)],3)}]" if (lab.startswith('on') and mp.nstr(w,3) in PRED) else ""), flush=True)
