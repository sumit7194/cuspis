"""EXP-060 (pre-registered in report.md): the round-trip operator lam^2 R R^T on the CH07b line a = 1/2 + iy.
R1 no resolvent poles; R2 characterise 1 - kappa_max; R3 control: w_S stays polynomial. [model: Opus 5.5]"""
import sys, os, time, json, math
import numpy as np
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
from exp044_det import w_det
from exp060_precheck import kappas

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def main():
    ys = np.round(np.arange(0.0, 3.51, 0.25), 2); ts = (0.1, 0.3, 1.0, 3.0)
    out = {}; r1 = True; r3 = True
    for t in ts:
        prev = None
        for y in ys:
            a = 0.5 + 1j * y; lam2 = (np.sin(np.pi * a) ** 2 / np.pi ** 2).real; tol = 1e-13 * max(lam2, 1.0)
            k = kappas(t, a); k2 = kappas(t, a, h=0.05, Pextra=2.0)
            gap, gap2 = 1 - k[0].real, 1 - k2[0].real
            stab = abs(gap2 / gap - 1) if gap >= 1e-10 else float('nan')
            wS, d, fl, m = w_det(t, 2 * a - 1, lam2, -1)
            d = complex(d); wS = complex(wS)
            ok = (np.abs(k.imag).max() <= tol and k.real.min() >= -tol and k[0].real < 1 and d.real > 0
                  and (math.isnan(stab) or stab <= 1e-3))
            ok3 = abs(wS) <= 1 + 2 * y * y
            r1 &= bool(ok); r3 &= bool(ok3)
            gam = -(math.log(gap) - math.log(prev)) / 0.25 if prev is not None and gap > 0 and prev > 0 else float('nan')
            prev = gap
            out[f"t{t}_y{y}"] = dict(gap=gap, gap_fine=gap2, lam2gap=lam2 * gap, gamma=gam, n099=int(np.sum(k.real > 0.99)),
                                     maxIm=float(np.abs(k.imag).max()), minRe=float(k.real.min()), det=d.real, detIm=d.imag, wS=wS.real)
            log(f"t={t} y={y:.2f}: 1-kmax {gap:.6e} (fine {gap2:.6e}, stab {stab:.1e})  lam2*(1-kmax) {lam2*gap:.4e}  local gamma {gam:.3f}  "
                f"#k>0.99 {int(np.sum(k.real>0.99))}  max|Im k| {np.abs(k.imag).max():.1e} (tol {tol:.1e})  det {d.real:.4e}  w_S {wS.real:+.6f}  "
                f"[R1 {'ok' if ok else 'FAIL'}; R3 {'ok' if ok3 else 'FAIL'}]")
    log(f"R1 {'PASS' if r1 else 'FAIL'};  R3 {'PASS' if r3 else 'FAIL'}")
    fires = True
    for t in ts:
        a = 0.5 + 2j; kk = kappas(t, a); c = 1.02 / kk[0].real; kc = kappas(t, a, scale=c)
        _, d, _, _ = w_det(t, 2 * a - 1, c * (np.sin(np.pi * a) ** 2 / np.pi ** 2).real, -1)
        f = kc[0].real >= 1 and complex(d).real < 0; fires &= bool(f)
        log(f"detector control t={t} y=2 (lam^2 x {c:.4f}): kmax {kc[0].real:.5f} det {complex(d).real:+.4e} [{'FIRES' if f else 'does not fire'}]")
    log(f"detector control {'PASS (fires at all t)' if fires else 'FAIL'}")
    kk = kappas(0.3, 0.5 + 3j).real; Sres = float(np.sum(kk / (1 - kk)))
    f3 = Sres > 1 + 2 * 9.0
    log(f"R3 must-fire (resolvent trace sum k/(1-k), no d/dt structure, t=0.3 y=3): {Sres:.4e} vs bound {1+2*9.0:.1f} [{'FIRES' if f3 else 'does not fire'}]")
    out.update(R1=bool(r1), R3=bool(r3), control=bool(fires), R3_mustfire=bool(f3), R3_mustfire_value=Sres)
    json.dump(out, open(os.path.join(D0, "exp060_results.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
