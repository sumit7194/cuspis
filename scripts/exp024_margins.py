"""EXP-024 diagnostic (not part of the frozen verdict): does the frozen run actually probe the region where the
added mode would violate C3 and CC on its own?  For each main case, find where the mode alone is negative and report
the family's margin there, relative to the size of the mode's (negative) contribution."""
import mpmath as mp
from exp024_cc_kappa import comp_emi, comp_tail, comp_mode, combine, sig_w, m_of, Fpp
mp.mp.dps = 40; pi = mp.pi
TH = [mp.mpf(10)**(-4 + 4.2*i/1999) for i in range(2000)]          # 1e-4 .. ~1.6 rad
U  = [mp.mpf(10)**(-10 + 9*i/1999) for i in range(2000)]           # 1e-10 .. 0.1
for K in (10, 100, 10**4):
    for smult in (2, 3):
        wv = mp.mpf('0.01')
        while K*sig_w(wv) + m_of(K, wv, smult*wv)/2 > mp.mpf(1)/3000: wv += mp.mpf('0.01')
        s0 = smult*wv; m = m_of(K, wv, s0)
        emi, tail, mode = comp_emi(), comp_tail(wv), comp_mode(m, s0)
        fam = combine([(1, emi), (K, tail), (1, mode)])
        chl = lambda f, t: f[2](t) + f[1](t)/mp.sin(t)
        neg3 = [t for t in TH if chl(mode, t) < 0]
        r3 = min(chl(fam, t)/abs(chl(mode, t)) for t in neg3) if neg3 else None
        negc = [u for u in U if Fpp(*mode, u) < 0]
        rc = min(Fpp(*fam, u)/abs(Fpp(*mode, u)) for u in negc) if negc else None
        print(f"K={K:<6} s0={smult}w (w={mp.nstr(wv,4)}, s0={mp.nstr(s0,4)}):"
              f"  mode alone violates C3 on theta in [{mp.nstr(min(neg3)*180/pi,3)}, {mp.nstr(max(neg3)*180/pi,3)}] deg ({len(neg3)} pts); family CHL / |mode CHL| there >= {mp.nstr(r3,4)};"
              f"  mode alone violates CC on u in [{mp.nstr(min(negc),3)}, {mp.nstr(max(negc),3)}] ({len(negc)} pts); family F'' / |mode F''| there >= {mp.nstr(rc,4)}")
