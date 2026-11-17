"""EXP-036 (pre-registered in report.md): analytic thin-arc asymptotics of the wedge MI, checked by EVALUATION.

Theory (argued in report.md EXP-036), per dilatation mode s, two arcs (half-width eta, centres theta apart):
  I_s ~= -1/2 ln(1 - rho_s^2),  rho_s = x_s(theta) / E_s(eta)            (monopole, classical phi-channel)
  x_s(psi) = (1/2pi) sum_m Xhat(s,m) e^{i m psi}  = int du e^{isu} c_X [2(cosh u - cos psi)]^(-Delta)
  Delta = 1/2:  E_s(eta) = (1/2pi) ln(2/eta) + k_s,   k_s = (1/2pi)[Xhat(s,0) + 2 sum_{m>=1} (Xhat(s,m) - 1/(2m))]
  Delta = 1/4:  E_s(0) = x_s(0) finite  ->  plateau  i_inf(theta) = (1/pi) int ds -1/2 ln(1 - x_s(theta)^2/x_s(0)^2)
  i_pred = (1/pi) int_0^inf ds I_s.   Leading order (Parseval): i_G ~ (pi - theta)/(8 sin theta) / ln^2(1/eta).
No parameter is fitted.  Numerics to compare: EXP-035 (eta >= 1e-3) and NEW runs at eta = 1e-4, 1e-5 (computed here,
after the predictions are written to exp036_predictions.json)."""
import json, os, sys, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
import exp035_cylinder_mi as e35

D0 = os.path.dirname(os.path.abspath(__file__))
PRED, NEWNUM = os.path.join(D0, "exp036_predictions.json"), os.path.join(D0, "exp036_new_numerics.json")
from scipy.special import gamma as G
CX = {al: (1 / (4 * np.pi)) * 2 ** (1 - al) * G((2 - al) / 2) / G(al / 2) for al in (1.0, 1.5, 0.5)}
THETAS = (np.pi / 2, np.pi)
ETAS_OLD = (0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001)
ETAS_NEW = (1e-4, 1e-5)
MMAX = 200000

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def xs_fourier(al, s, psi):
    m = np.arange(1, MMAX + 1); xh = e35.xhat(al, s, m); x0 = e35.xhat(al, s, np.array([0.0]))[0]
    if al == 1.0:   # subtract the 1/(2m) tail exactly: sum cos(m psi)/m = -ln|2 sin(psi/2)|
        return (x0 + 2 * np.sum((xh - 0.5 / m) * np.cos(m * psi)) - np.log(abs(2 * np.sin(psi / 2)))) / (2 * np.pi)
    # alpha = 1.5: tail ~ (1/2) m^(-3/2), summed to MMAX then the remainder by the integral estimate (psi = 0 only used)
    tail = 0.5 * 2 * (2 / np.sqrt(MMAX)) if psi == 0 else 0.0
    return (x0 + 2 * np.sum(xh * np.cos(m * psi)) + tail) / (2 * np.pi)

def xs_quad(al, s, psi):
    D = (2 - al) / 2
    f = lambda u: np.cos(s * u) * (4 * (np.sinh(u / 2) ** 2 + np.sin(psi / 2) ** 2)) ** (-D)
    pts = [0, 1e-6, 1e-3, 0.1, 1, 5, 20, 80 / D]
    return 2 * CX[al] * sum(quad(f, a, b, limit=400, epsabs=1e-14, epsrel=1e-12)[0] for a, b in zip(pts[:-1], pts[1:]))

def ks(s):
    m = np.arange(1, MMAX + 1)
    return (e35.xhat(1.0, s, np.array([0.0]))[0] + 2 * np.sum(e35.xhat(1.0, s, m) - 0.5 / m)) / (2 * np.pi)

def ks_quad(s, psi=1e-5):
    return xs_quad(1.0, s, psi) + np.log(psi) / (2 * np.pi)

def s_integral(f, nodes=96):
    t, w = leggauss(nodes); t = 0.5 * (t + 1); w = 0.5 * w; s = t / (1 - t); jac = 1 / (1 - t) ** 2
    return sum(wi * ji * f(si) for si, wi, ji in zip(s, w, jac))

def predictions():
    out = {}
    # (P-a) leading coefficient C(theta) = (pi - theta)/(8 sin theta): closed form vs numeric (1/pi) int ds (1/2)(2 pi x_s)^2
    for th in THETAS:
        closed = 1 / 8 if th == np.pi else (np.pi - th) / (8 * np.sin(th))
        num = s_integral(lambda s: 0.5 * (2 * np.pi * xs_fourier(1.0, s, th)) ** 2) / np.pi
        out[f"C_{round(np.degrees(th))}"] = {"closed": closed, "numeric": num}
        log(f"P-a C(theta={np.degrees(th):.0f}): closed {closed:.10f} numeric {num:.10f} rel {abs(num / closed - 1):.1e} "
            f"[{'PASS' if abs(num / closed - 1) < 1e-6 else 'FAIL'}]")
    # (P-0) two implementations of x_s and k_s
    for s in (0.0, 0.8, 3.0):
        for th in THETAS:
            a, b = xs_fourier(1.0, s, th), xs_quad(1.0, s, th)
            log(f"P-0 x_s alpha=1 s={s} th={np.degrees(th):.0f}: Fourier {a:.12f} quad {b:.12f} rel {abs(a / b - 1):.1e}")
        a, b = ks(s), ks_quad(s)
        log(f"P-0 k_s s={s}: Fourier {a:.10f}  quad(psi=1e-5) {b:.10f}  diff {abs(a - b):.1e} (O(psi^2 ln psi) expected)")
        a, b = xs_fourier(1.5, s, 0.0), xs_quad(1.5, s, 0.0)
        log(f"P-0 x_s(0) alpha=1.5 s={s}: Fourier+tail {a:.10f} quad {b:.10f} rel {abs(a / b - 1):.1e}")
    # (P-b) Delta = 1/2 prediction at every eta (no fitted parameter); cache k_s, x_s on the nodes
    t, w = leggauss(96); t = 0.5 * (t + 1); w = 0.5 * w; S = t / (1 - t); J = 1 / (1 - t) ** 2
    K = np.array([ks(s) for s in S]); X = {th: np.array([xs_fourier(1.0, s, th) for s in S]) for th in THETAS}
    for eta in ETAS_OLD + ETAS_NEW:
        E = np.log(2 / eta) / (2 * np.pi) + K
        for th in THETAS:
            rho = X[th] / E
            v = np.sum(w * J * (-0.5 * np.log1p(-rho ** 2))) / np.pi
            lead = (1 / 8 if th == np.pi else (np.pi - th) / (8 * np.sin(th))) / np.log(1 / eta) ** 2
            out[f"pred_a1.0_e{eta}_th{round(np.degrees(th))}"] = {"full": v, "leading": lead}
    # (P-c) Delta = 1/4 plateau
    X0 = np.array([xs_fourier(1.5, s, 0.0) for s in S])
    for th in THETAS:
        Xt = np.array([xs_fourier(1.5, s, th) for s in S])
        v = np.sum(w * J * (-0.5 * np.log1p(-(Xt / X0) ** 2))) / np.pi
        out[f"plateau_a1.5_th{round(np.degrees(th))}"] = v
    json.dump(out, open(PRED, "w"), indent=1)
    log(f"predictions frozen to {PRED}")
    return out

def new_numerics():
    res = json.load(open(NEWNUM)) if os.path.exists(NEWNUM) else {}
    for al in (1.0, 1.5):
        for eta, nps in ((1e-4, (32, 64)), (1e-5, (16, 32))):
            for n_p in nps:
                key = f"a{al}_e{eta}_np{n_p}_q96"
                if key in res: continue
                t0 = time.time(); v, M, ee = e35.iG(al, eta, n_p, 96)
                res[key] = {"i90": v[0], "i180": v[1], "M": M, "eta_eff": ee}; json.dump(res, open(NEWNUM, "w"), indent=0)
                log(f"  new numerics {key}: M={M} ({time.time() - t0:.0f} s)")
    return res

def compare(pred, new):
    old = json.load(open(os.path.join(D0, "exp035_results.json")))
    num = lambda al, eta, th: (old.get(f"a{al}_e{eta}_np128_q96") or new[f"a{al}_e{eta}_np{64 if eta == 1e-4 else 32}_q96"])[
        "i90" if th == 90 else "i180"]
    log("n_p gate at the new eta (rel diff between the two n_p; must be < 2%):")
    for al in (1.0, 1.5):
        for eta, (a, b) in ((1e-4, (32, 64)), (1e-5, (16, 32))):
            for th in ("i90", "i180"):
                d = abs(new[f"a{al}_e{eta}_np{a}_q96"][th] / new[f"a{al}_e{eta}_np{b}_q96"][th] - 1)
                log(f"  alpha={al} eta={eta} {th}: {d:.2e} [{'PASS' if d < 0.02 else 'FAIL'}]")
    log("P-b  Delta = 1/2: prediction / numerics (frozen criterion: |ratio-1| decreasing in eta, <= 0.15 at 1e-3, <= 0.10 at 1e-5):")
    for th in (90, 180):
        row = []
        for eta in ETAS_OLD + ETAS_NEW:
            p = pred[f"pred_a1.0_e{eta}_th{th}"]; n = num(1.0, eta, th)
            row.append((eta, n, p["full"], p["full"] / n, p["leading"] / n))
        for eta, n, pf, r, rl in row:
            log(f"  th={th} eta={eta:g}: numerics {n:.6e}  predicted {pf:.6e}  ratio {r:.4f}   (leading-order-only ratio {rl:.4f})")
        dev = [abs(r[3] - 1) for r in row]
        mono = all(dev[i + 1] <= dev[i] + 1e-12 for i in range(len(dev) - 1))
        log(f"  th={th}: monotone decrease of |ratio-1|: {mono}; at 1e-3: {dev[ETAS_OLD.index(0.001)]:.4f}; at 1e-5: {dev[-1]:.4f}")
    log("P-c  Delta = 1/4 plateau: predicted i_inf vs numerics (frozen: |ratio-1| decreasing in eta, <= 0.10 at 1e-5):")
    for th in (90, 180):
        p = pred[f"plateau_a1.5_th{th}"]
        log(f"  th={th}: predicted plateau {p:.6f};  numerics " + "  ".join(
            f"{eta:g}:{num(1.5, eta, th):.6f} (ratio {p / num(1.5, eta, th):.4f})" for eta in ETAS_OLD + ETAS_NEW))

if __name__ == "__main__":
    if sys.argv[1:] == ["--predict"]:
        predictions()
    else:
        pred = json.load(open(PRED)); new = new_numerics(); compare(pred, new)
