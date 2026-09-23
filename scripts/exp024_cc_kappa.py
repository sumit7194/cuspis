"""EXP-024: does conformal concavity (plus the fusion small-angle structure) bound kappa?  Frozen in report.md
(pre-registration c9e3566, implementation note c4b06f9).  Family: a = a_EMI + K a_w + a_delta(s0), sigma-free units.
Checks: C2, C3, CC (F'' >= 0 in u), and the expansion coefficients a0 = 0, a1 <= -kappa/12, theta^2 coefficient >= 0."""
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def comp_emi():
    a   = lambda t: 1 + (pi - t)*mp.cot(t)
    da  = lambda t: -mp.cot(t) - (pi - t)*mp.csc(t)**2
    d2a = lambda t: 2*mp.csc(t)**2*(1 + (pi - t)*mp.cot(t))
    return a, da, d2a

def comp_tail(w):
    g   = lambda t: mp.e**(-w*t)/t
    dg  = lambda t: -mp.e**(-w*t)*(w/t + 1/t**2)
    d2g = lambda t: mp.e**(-w*t)*(w**2/t + 2*w/t**2 + 2/t**3)
    c = 2*mp.e**(-w*pi)/pi
    a   = lambda t: g(t) + g(2*pi - t) - c
    da  = lambda t: dg(t) - dg(2*pi - t)
    d2a = lambda t: d2g(t) + d2g(2*pi - t)
    return a, da, d2a

def comp_mode(m, s0):
    a   = lambda t: m*(mp.cosh(s0*(pi - t)) - 1)/s0**2
    da  = lambda t: -m*mp.sinh(s0*(pi - t))/s0
    d2a = lambda t: m*mp.cosh(s0*(pi - t))
    return a, da, d2a

def combine(parts):
    return (lambda t: sum(c*p[0](t) for c, p in parts),
            lambda t: sum(c*p[1](t) for c, p in parts),
            lambda t: sum(c*p[2](t) for c, p in parts))

sig_w = lambda w: mp.e**(-w*pi)*(w**2/pi + 2*w/pi**2 + 2/pi**3)
c_w   = lambda w: -w + mp.e**(-2*pi*w)/(2*pi) - 2*mp.e**(-w*pi)/pi

def m_of(K, w, s0): return -K*c_w(w)*s0**2/(mp.cosh(s0*pi) - 1)

def expansion(K, w, s0, m):
    """closed-form theta^0, theta^1, theta^2 coefficients of a - kappa/theta at theta -> 0"""
    g2, dg2, d2g2 = (lambda t: mp.e**(-w*t)/t)(2*pi), -mp.e**(-2*pi*w)*(w/(2*pi) + 1/(2*pi)**2), mp.e**(-2*pi*w)*(w**2/(2*pi) + 2*w/(2*pi)**2 + 2/(2*pi)**3)
    # mirror h(t) = g(2pi - t): h(0) = g(2pi), h'(0) = -g'(2pi), h''(0) = g''(2pi)
    a0 = 0 + K*(-w + g2 - 2*mp.e**(-w*pi)/pi) + m*(mp.cosh(s0*pi) - 1)/s0**2
    a1 = -pi/3 + K*(w**2/2 - dg2) - m*mp.sinh(s0*pi)/s0
    a2 = mp.mpf(1)/3 + K*(-w**3/6 + d2g2/2) + m*mp.cosh(s0*pi)/2
    return a0, a1, a2

# grids
TH = [mp.mpf(10)**(-6 + 5.5*i/2999) for i in range(3000)] + [mp.mpf('0.003162') + (pi - mp.mpf('1e-6') - mp.mpf('0.003162'))*i/2999 for i in range(3000)]
U  = [mp.mpf(10)**(-12 + 10*i/2999) for i in range(3000)] + [mp.mpf('0.01') + (1 - mp.mpf('1e-9') - mp.mpf('0.01'))*i/2999 for i in range(3000)]

def Fpp(a, da, d2a, u):
    su = mp.sqrt(u); t = 4*mp.atan(su)
    tp = 2/(su*(1 + u)); tpp = -u**(-1.5)/(1 + u) - 2/(su*(1 + u)**2)
    A, Ap, App = a(t), da(t)*tp, d2a(t)*tp**2 + da(t)*tpp
    return -u**(-1.5)*A/4 + Ap/su + su*App

def checks(a, da, d2a, label):
    worst = {}
    c2a = min(a(t) for t in TH); c2b = max(da(t) for t in TH); c2c = min(d2a(t) for t in TH)
    chl = [(d2a(t) + da(t)/mp.sin(t), t) for t in TH]; c3 = min(chl, key=lambda x: x[0])
    fpp = [(Fpp(a, da, d2a, u), u) for u in U]; cc = min(fpp, key=lambda x: x[0])
    ok2 = c2a >= 0 and c2b <= 0 and c2c >= 0; ok3 = c3[0] >= 0; okc = cc[0] >= 0
    print(f"   {label:46s} C2 {'ok' if ok2 else 'FAIL'} (min a {mp.nstr(c2a,3)}, max a' {mp.nstr(c2b,3)}, min a'' {mp.nstr(c2c,3)});"
          f"  C3 {'ok' if ok3 else 'FAIL'} (min {mp.nstr(c3[0],3)} at {mp.nstr(c3[1]*180/pi,4)} deg);"
          f"  CC {'ok' if okc else 'FAIL'} (min F'' {mp.nstr(cc[0],3)} at u={mp.nstr(cc[1],3)})")
    return ok2, ok3, okc

if __name__ == "__main__":
    emi = comp_emi()
    print("CONTROLS (each must behave as stated)")
    # k1: no mode -> a0 and a1 checks must fail
    K, w = 10, mp.mpf(3)
    a0, a1, a2 = expansion(K, w, 1, 0)
    k1 = (abs(a0) > 1e-20) and not (a1 <= -(pi + K)/12)
    print(f"   k1 no mode (K=10,w=3): a0 = {mp.nstr(a0,6)} (must be != 0), a1 = {mp.nstr(a1,6)} vs -kappa/12 = {mp.nstr(-(pi+K)/12,6)} (must violate) -> {'fires' if k1 else 'DOES NOT FIRE'}")
    amin = (lambda t: 8*mp.log(1/mp.sin(t/2)), lambda t: -4*mp.cot(t/2), lambda t: 2*mp.csc(t/2)**2)
    k2 = checks(*combine([(1, emi), (1, amin)]), "k2 EMI + a_min (CC must FAIL)")
    k3 = checks(*combine([(1, emi), (10, comp_mode(1, mp.mpf('0.3')))]), "k3 EMI + 10 mode(s=0.3) (C3 must FAIL)")
    k4 = checks(*emi, "k4 EMI alone (all must pass)")
    ctrl = k1 and (not k2[2]) and (not k3[1]) and all(k4)
    print(f"   controls -> {'PASS' if ctrl else 'FAIL'}")

    print("\nFROZEN FAMILY a = a_EMI + K a_w + a_delta(s0), m fixed by a0 = 0, w = smallest (0.01 grid) with added mass <= 1e-3/3")
    rows = []
    for K in (10, 100, 10**4):
        for smult in (2, 3):
            def added(wv):
                s0 = smult*wv; return K*sig_w(wv) + m_of(K, wv, s0)/2
            wv = mp.mpf('0.01')
            while added(wv) > mp.mpf(1)/3000: wv += mp.mpf('0.01')
            for wlab, wuse in (("w", wv), ("1.5w", wv*mp.mpf('1.5'))):
                s0 = smult*wuse; m = m_of(K, wuse, s0)
                a0, a1, a2 = expansion(K, wuse, s0, m)
                kap = pi + K; sig = mp.mpf(1)/3 + K*sig_w(wuse) + m/2
                fam = combine([(1, emi), (K, comp_tail(wuse)), (1, comp_mode(m, s0))])
                # numerical cross-check of a0 from the function itself
                a0num = 2*(fam[0](mp.mpf('1e-8')) - kap/mp.mpf('1e-8')) - (fam[0](mp.mpf('2e-8')) - kap/mp.mpf('2e-8'))
                ok2, ok3, okc = checks(*fam, f"K={K} s0={smult}{wlab} (w={mp.nstr(wuse,4)}, s0={mp.nstr(s0,4)})")
                ok_a0 = abs(a0) < mp.mpf(10)**(-30); ok_a1 = a1 <= -kap/12; ok_a2 = a2 >= 0
                print(f"      kappa/sigma = {mp.nstr(kap/sig,6)};  added mass/sigma_EMI = {mp.nstr(3*(K*sig_w(wuse)+m/2),3)};  a0 = {mp.nstr(a0,3)} (numerical {mp.nstr(a0num,3)});"
                      f"  a1 = {mp.nstr(a1,5)} vs -kappa/12 = {mp.nstr(-kap/12,5)};  theta^2 coeff = {mp.nstr(a2,5)}")
                allok = ok2 and ok3 and okc and ok_a0 and ok_a1 and ok_a2
                print(f"      -> {'ALL PASS' if allok else 'FAIL'}")
                rows.append((K, smult, wlab, allok, ok3, okc))
    main = [r for r in rows if r[2] == "w"]
    for smult in (2, 3):
        rs = [r for r in main if r[1] == smult]
        print(f"\ns0 = {smult}w: all checks pass at every K: {all(r[3] for r in rs)}")
    sweep = [r for r in rows if r[2] == "1.5w"]
    print(f"nuisance sweep (w x 1.5, not in the verdict): all pass: {all(r[3] for r in sweep)}")
