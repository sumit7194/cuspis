"""EXP-037 (pre-registered in report.md): P3 / A5' for the free massless Dirac fermion in 2+1, by dilatation reduction.

Ground state C = <psi psi^dag> = 1/2 (1 - S), S = sigma.k/|k| = [[0, e^{-i phi_k}], [e^{i phi_k}, 0]].
Position space: K = C - 1/2 delta = -(i/4pi) sigma.(x-y)/|x-y|^3.  Psi has Delta = 1 = d/2, so the unitary map f -> r f
alone makes the state u-translation invariant (no extra canonical rescaling).  Mellin-Hankel (as EXP-035) gives, on
(up: angular l, down: angular l+1), the per-(s,l) symbol S = [[0, B'], [B, 0]] with
   B(s,l)  = (-i)^|l|   i^|l+1| g(-1+is, l)   g(-1-is, l+1),
   B'(s,l) = (-i)^|l+1| i^|l|   g(-1+is, l+1) g(-1-is, l),       g(lam, l) = 2^(lam+1) Gamma((|l|+lam+2)/2)/Gamma((|l|-lam)/2).
Down components are re-phased by e^{-i phi} (a local unitary: spectra unchanged) so all blocks are circulant.
i_G = (1/2pi) int_{-inf}^{inf} ds I_s.  Thin-arc prediction (argued, EXP-037):
   I_s ~= ((2 eta)^2 (2 pi)^2 / 6) ||K_s(theta)||_F^2   =>   i_G ~= (eta^2/6) [1 + (pi - theta) cot theta] / sin^2 theta."""
import json, os, sys, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import loggamma, polygamma
from scipy.integrate import quad

D0 = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D0, "exp037_results.json")
ETAS = (0.40, 0.25, 0.15, 0.10, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001)
NPS = (16, 32, 64, 128)            # 128 added in the EXP-037 addendum (gate refinement); q = 24 only at 128
NODES = (12, 24)                      # Gauss-Legendre nodes per panel
PANELS = ((0, 1), (1, 3), (3, 7), (7, 12), (12, 20))   # s in [0, 20]; |K_s(theta)| ~ e^{-s psi}, psi >= pi/2 - 2 eta

def snodes(n):
    t, w = leggauss(n); S, W = [], []
    for a, b in PANELS:
        S += list(0.5 * (b - a) * (t + 1) + a); W += list(0.5 * (b - a) * w)
    return np.array(S), np.array(W)

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def lg(lam, l):   # log g(lam, l), complex
    l = np.abs(l)
    return (lam + 1) * np.log(2) + loggamma((l + lam + 2) / 2) - loggamma((l - lam) / 2)

def Bp(s, l):     # B'(s, l): maps the down component (angular l+1) to up (angular l)
    ph = (-1j) ** np.abs(l + 1) * (1j) ** np.abs(l)
    return ph * np.exp(lg(-1 + 1j * s, l + 1) + lg(-1 - 1j * s, l))

def B(s, l):
    ph = (-1j) ** np.abs(l) * (1j) ** np.abs(l + 1)
    return ph * np.exp(lg(-1 + 1j * s, l) + lg(-1 - 1j * s, l + 1))

def Bp_inf(l):     # large-|l| limit of B' (exact at s = 0): -i sgn(l + 1/2)
    return -1j * np.sign(np.asarray(l) + 0.5)

def row_ud(s, M, K=8):
    """Cell-averaged (piecewise-constant Galerkin) compression of the EXACT continuum projector: no band limit, hence no
    staggered doubler.  Entry d = (1/M) sum_l (-1/2 B'(l)) sinc^2(pi l/M) e^{2 pi i l d/M}, all l.  The non-decaying part
    B'_inf is summed over all aliases in closed form (trigamma); the remainder R = B' - B'_inf ~ s/|l| over |k| <= K aliases."""
    l0 = np.fft.fftfreq(M, 1.0 / M).astype(np.int64)
    a = np.mod(l0, M).astype(float); x = a / M
    with np.errstate(divide="ignore", invalid="ignore"):
        ainf = 0.5j * np.sin(np.pi * x) ** 2 / np.pi ** 2 * (polygamma(1, x) - polygamma(1, 1 - x))
    ainf[l0 == 0] = 0.5j                                  # l = 0: -1/2 * B'_inf(0) * sinc^2(0) = i/2; other aliases vanish
    aR = np.zeros(M, complex)
    for k in range(-K, K + 1):
        l = l0 + k * M
        sinc2 = np.where(l == 0, 1.0, np.sin(np.pi * l / M) ** 2 / np.where(l == 0, 1, np.pi * l / M) ** 2)
        aR += -0.5 * (Bp(s, l) - Bp_inf(l)) * sinc2
    return np.fft.ifft(ainf + aR)

def kud_symbol(s, psi, L=400000):
    """Continuum cross kernel from the symbol: remainder summed directly, B'_inf part by its distributional value
    (1/2pi) sum_l (-1/2)(-i sgn(l+1/2)) e^{il psi} = (1/2pi)(-1/2)(-i + cot(psi/2))."""
    l = np.arange(-L, L)
    return (np.sum(-0.5 * (Bp(s, l) - Bp_inf(l)) * np.exp(1j * l * psi)) - 0.5 * (-1j + 1 / np.tan(psi / 2))) / (2 * np.pi)

def kud_direct(s, psi, sign=+1):
    """Position-space cross kernel r r' K_ud e^{i phi'} = -(i/4pi)(e^{u/2} e^{-i psi} - e^{-u/2})/D^{3/2}, Fourier in u."""
    D = lambda u: 4 * (np.sinh(u / 2) ** 2 + np.sin(psi / 2) ** 2)
    f = lambda u: (np.exp(u / 2) * np.exp(-1j * psi) - np.exp(-u / 2)) / D(u) ** 1.5 * np.exp(sign * 1j * s * u) * (-1j / (4 * np.pi))
    pts = ((-60, -1), (-1, 0), (0, 1), (1, 60))
    re = sum(quad(lambda u: f(u).real, a, b, limit=400, epsabs=1e-13)[0] for a, b in pts)
    im = sum(quad(lambda u: f(u).imag, a, b, limit=400, epsabs=1e-13)[0] for a, b in pts)
    return re + 1j * im

def entropy(C):
    c = np.clip(np.linalg.eigvalsh(C), 1e-300, 1 - 1e-16)
    return float(-np.sum(c * np.log(c) + (1 - c) * np.log1p(-c)))

def geometry(eta, n_p):
    M = 4 * int(np.ceil(np.pi * n_p / (4 * eta)))
    return M, np.pi * n_p / M

def cmat(r, idx, M):
    d = (idx[:, None] - idx[None, :]) % M
    n = len(idx); C = np.empty((2 * n, 2 * n), complex)
    C[:n, :n] = 0.5 * np.eye(n); C[n:, n:] = 0.5 * np.eye(n)
    C[:n, n:] = r[d]; C[n:, :n] = r[d].conj().T
    return C

def mi_both(s, n_p, M):
    r = row_ud(s, M); a = np.arange(n_p)
    s1 = entropy(cmat(r, a, M)); out = []
    for sep in (M // 4, M // 2):
        out.append(2 * s1 - entropy(cmat(r, np.concatenate([a, a + sep]), M)))
    return np.array(out)

def iG(eta, n_p, nodes):
    M, ee = geometry(eta, n_p)
    S, W = snodes(nodes)
    acc = np.zeros(2)
    for si, wi in zip(S, W):
        acc += wi * (mi_both(si, n_p, M) + mi_both(-si, n_p, M))   # full line, |s| <= 20
    return acc / (2 * np.pi), M, ee

def tail_ratio():
    M, _ = geometry(0.4, 16)
    return max(abs(mi_both(20.0, 16, M)) / mi_both(0.0, 16, M))

def lead(eta, th):
    return eta ** 2 / 18 if th == np.pi else eta ** 2 / 6 * (1 + (np.pi - th) / np.tan(th)) / np.sin(th) ** 2

def tier1():
    l = np.arange(-50, 50)
    for s in (0.0, 0.7, 3.0):
        e1 = np.max(np.abs(np.abs(B(s, l)) - 1)); e2 = np.max(np.abs(Bp(s, l) - B(s, l).conj()))
        log(f"Tier-1 symbol s={s}: max||B|-1| {e1:.1e}, max|B' - conj B| {e2:.1e} (S^2 = 1, S hermitian) "
            f"[{'PASS' if max(e1, e2) < 1e-12 else 'FAIL'}]")
        if max(e1, e2) >= 1e-12: sys.exit(2)
    for s in (0.0, 0.7):          # two implementations of the cross kernel: symbol Fourier sum vs position-space u-integral
        for psi in (np.pi / 2, np.pi, 1.0):
            a = kud_symbol(s, psi); bp, bm = kud_direct(s, psi, +1), kud_direct(s, psi, -1)
            ok = min(abs(a - bp), abs(a - bm)) / abs(a)
            log(f"Tier-1 kernel s={s} psi={psi:.4f}: symbol {a:.10f}  direct(+s) {bp:.10f}  direct(-s) {bm:.10f}  "
                f"best rel {ok:.1e} [{'PASS' if ok < 1e-5 else 'FAIL'}]")
            if ok >= 1e-5: sys.exit(3)
    for s_ in (0.0, 0.7, 3.0):    # cell-averaged row at d = M/4, M/2 vs the point kernel (differ by O(delta^2))
        M = 4096; r = row_ud(s_, M)
        for d in (M // 4, M // 2):
            pt = kud_symbol(s_, 2 * np.pi * d / M) * 2 * np.pi / M; rel = abs(r[d] - pt) / abs(pt)
            log(f"Tier-1 cell vs point kernel s={s_} d={d}/{M}: rel {rel:.1e} [{'PASS' if rel < 1e-4 else 'FAIL'}]")
            if rel >= 1e-4: sys.exit(4)
        A = np.concatenate([np.arange(40), np.arange(40) + M // 4]); ev = np.linalg.eigvalsh(cmat(r, A, M))
        log(f"Tier-1 state validity s={s_}: eigenvalues of C_A in [{ev.min():.3e}, {1 - ev.max():.3e} from 1] [{'PASS' if ev.min() > -1e-12 and ev.max() < 1 + 1e-12 else 'FAIL'}]")
        if not (ev.min() > -1e-12 and ev.max() < 1 + 1e-12): sys.exit(6)
    # Parseval: (1/2pi) int ds ||K_s(theta)||^2 * (2pi)^2 (2eta)^2/6 == lead  <=>  int ds ||K_s||^2 = [1+(pi-th)cot th]/(8 pi sin^2 th)
    S, W = snodes(24)
    for th in (np.pi / 2, np.pi):
        num = sum(wi * 2 * (abs(kud_symbol(si, th, 2000000)) ** 2 + abs(kud_symbol(-si, th, 2000000)) ** 2) for si, wi in zip(S, W))
        cl = 1 / (24 * np.pi) if th == np.pi else (1 + (np.pi - th) / np.tan(th)) / (8 * np.pi * np.sin(th) ** 2)
        log(f"Tier-1 Parseval theta={np.degrees(th):.0f}: symbol int ds ||K_s||^2 = {num:.9f}  closed form {cl:.9f}  rel {abs(num / cl - 1):.1e} "
            f"[{'PASS' if abs(num / cl - 1) < 1e-4 else 'FAIL'}]")
        if abs(num / cl - 1) >= 1e-4: sys.exit(5)

def main():
    log("EXP-037 start"); tier1()
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for eta in ETAS:
        for n_p in NPS:
            for q in NODES:
                k = f"e{eta}_np{n_p}_q{q}"
                if k in res or (n_p == 128 and q == NODES[0]): continue
                t0 = time.time(); v, M, ee = iG(eta, n_p, q)
                res[k] = {"i90": v[0], "i180": v[1], "M": M, "eta_eff": ee}; json.dump(res, open(OUT, "w"), indent=0)
                log(f"  {k}: M={M} ({time.time() - t0:.0f} s)")
    analyse(res)

def analyse(res):
    g = lambda e, th, n=NPS[-1], q=NODES[-1]: res[f"e{e}_np{n}_q{q}"]["i90" if th == 90 else "i180"]
    wq = max(abs(g(e, th, n=64, q=NODES[0]) / g(e, th, n=64) - 1) for e in ETAS for th in (90, 180))
    tr = tail_ratio(); log(f"gate tail: I_s at s = 20 relative to s = 0 (eta = 0.4, n_p = 16): {tr:.1e} [{'PASS' if tr < 1e-6 else 'FAIL'}]")
    wn = max(abs(g(e, th, n=NPS[-2]) / g(e, th) - 1) for e in ETAS for th in (90, 180))
    log(f"gate s-quadrature 12 vs 24 nodes/panel: {wq:.2e} [{'PASS' if wq < 1e-3 else 'FAIL'}];  gate n_p {NPS[-2]} vs {NPS[-1]}: {wn:.2e} [{'PASS' if wn < 0.02 else 'FAIL'}]")
    for th, thr in ((90, np.pi / 2), (180, np.pi)):
        log(f"theta={th}:")
        for e in ETAS:
            ee = res[f"e{e}_np{NPS[-1]}_q{NODES[-1]}"]["eta_eff"]
            log(f"  eta={e:<6g} i_G={g(e, th):.6e}  drift(n_p 16,32,64,128)={[f'{g(e, th, n=n):.6e}' for n in NPS]}  "
                f"prediction(eta_eff) {lead(ee, thr):.6e}  pred/num {lead(ee, thr) / g(e, th):.5f}")
        log(f"  R2 = i_G(0.001)/i_G(0.01) = {g(0.001, th) / g(0.01, th):.5f};  R1 = i_G(0.01)/i_G(0.1) = {g(0.01, th) / g(0.1, th):.5f}")
    log(f"|i_G(90) - i_G(180)|: at 0.01 {abs(g(0.01, 90) - g(0.01, 180)):.3e}, at 0.001 {abs(g(0.001, 90) - g(0.001, 180)):.3e}")

if __name__ == "__main__":
    analyse(json.load(open(OUT))) if sys.argv[1:] == ["--analyse"] else main()
