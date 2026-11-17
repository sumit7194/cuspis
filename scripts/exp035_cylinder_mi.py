"""EXP-035 (pre-registered in report.md before any i_G is computed): P3 in the continuum by dilatation reduction.

Scale-invariant pure Gaussian state in the plane, X(k) = 1/(2|k|^alpha), P(k) = |k|^alpha/2, Delta = (2-alpha)/2.
With u = log r and the canonical rescaling phi -> r^(1-Delta) phi, pi -> r^(Delta-1) pi (spectrum of X_A P_A unchanged), the
state is translation invariant on the cylinder (u, varphi) with symbol (verified vs 2D quadrature, report.md EXP-035)
    Xhat(s, m) = 1/2 * 2^(2 Delta - 2) |Gamma((|m| + Delta + i s)/2)|^2 / |Gamma((|m| + 2 - Delta + i s)/2)|^2,
    Phat(s, m) = 1/(4 Xhat(s, m))      (purity on the full plane).
Two wedges with a common apex are (arc) x R on the cylinder, so the MI per unit log scale is
    i_G(theta, eta) = (1/pi) int_0^inf ds I_s,   I_s = MI of two arcs (width 2 eta, centres theta apart) for the 1D state
with symbol Xhat(s, .) on the circle.  The circle is discretised into M sites with modes |m| <= M/2 (band-limited
regularisation; MI of separated arcs is UV finite, convergence in points-per-arc n_p is a registered gate).
s-integral: Gauss-Legendre in t, s = t/(1-t), 48 and 96 nodes (registered gate)."""
import json, os, sys, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import loggamma
from scipy.linalg import cholesky, eigvalsh

D0 = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D0, "exp035_results.json")
ALPHAS = (1.0, 1.5, 0.5)
ETAS = (0.40, 0.25, 0.15, 0.10, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001)
NPS = (32, 64, 128)
NODES = (48, 96)
LATTICE_B = {  # EXP-034a run B (scripts/exp034a_output.txt), i_G at (alpha, eta, theta): the known-answer comparison
    (1.0, 0.40, 90): 0.043918, (1.0, 0.40, 180): 0.019999, (1.0, 0.25, 90): 0.025868, (1.0, 0.25, 180): 0.013609,
    (1.5, 0.40, 90): 0.115931, (1.5, 0.40, 180): 0.065428, (1.5, 0.25, 90): 0.084917, (1.5, 0.25, 180): 0.055810,
    (0.5, 0.40, 90): 0.010604, (0.5, 0.40, 180): 0.003846, (0.5, 0.25, 90): 0.004889, (0.5, 0.25, 180): 0.002017}

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def xhat(al, s, m):
    D = (2 - al) / 2; m = np.abs(m)
    lg = 2 * (loggamma((m + D + 1j * s) / 2).real - loggamma((m + 2 - D + 1j * s) / 2).real)
    return 0.5 * 2.0 ** (2 * D - 2) * np.exp(lg)

def rows(al, s, M):
    """Circulant rows x[d], p[d], d = 0..M-1, for the band-limited M-site circle."""
    m = np.fft.fftfreq(M, 1.0 / M)            # 0..M/2-1, -M/2..-1
    xh = xhat(al, s, m)
    return np.fft.ifft(xh).real, np.fft.ifft(0.25 / xh).real

def entropy(X, P):
    L = cholesky(X, lower=True)
    nu = np.sqrt(np.clip(eigvalsh(L.T @ P @ L), 0.25, None))
    a, b = nu + 0.5, nu - 0.5
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(b > 1e-300, b * np.log(b), 0.0)
    return float(np.sum(a * np.log(a) - t))

def geometry(eta, n_p):
    M = 4 * int(np.ceil(np.pi * n_p / (4 * eta)))    # site spacing 2 pi/M; arc = n_p sites; M % 4 == 0 for theta = 90
    return M, np.pi * n_p / M                        # eta_eff = half-width actually used

def mi_both(x, p, n_p, M):
    """MI between two n_p-site arcs whose starts are M/4 (theta = 90) and M/2 (theta = 180) sites apart."""
    a = np.arange(n_p)
    def blk(row, idx):
        d = np.abs(idx[:, None] - idx[None, :]); d = np.minimum(d, row.size - d)
        return row[d]
    s1 = entropy(blk(x, a), blk(p, a))
    out = []
    for sep in (M // 4, M // 2):
        u = np.concatenate([a, a + sep])
        out.append(2 * s1 - entropy(blk(x, u), blk(p, u)))
    return np.array(out)

def iG(al, eta, n_p, nodes):
    M, ee = geometry(eta, n_p)
    t, w = leggauss(nodes); t = 0.5 * (t + 1); w = 0.5 * w
    s = t / (1 - t); jac = 1 / (1 - t) ** 2
    acc = np.zeros(2)
    for si, wi, ji in zip(s, w, jac):
        x, p = rows(al, si, M)
        acc += wi * ji * mi_both(x, p, n_p, M)
    return acc / np.pi, M, ee

def tier1():
    # (a) closed form vs the flat-space normalisation at large m: Xhat -> 1/2 |m|^(2 Delta - 2) (1D chain with |m|^alpha)
    for al in ALPHAS:
        D = (2 - al) / 2; mm = 1e6
        r = xhat(al, 0.3, mm) / (0.5 * mm ** (2 * D - 2))
        log(f"Tier-1 large-m symbol alpha={al}: Xhat / (|m|^(2D-2)/2) at m=1e6: {r:.8f} [{'PASS' if abs(r - 1) < 1e-5 else 'FAIL'}]")
        if abs(r - 1) >= 1e-5: sys.exit(2)
    # (b) purity of the M-site circle state: S(arc) = S(complement) (code check of the circulant construction)
    for al in ALPHAS:
        M = 96; x, p = rows(al, 0.7, M)
        def blk(row, idx):
            d = np.abs(idx[:, None] - idx[None, :]); d = np.minimum(d, M - d); return row[d]
        A = np.arange(17); Ac = np.arange(17, M)
        sa, sc = entropy(blk(x, A), blk(p, A)), entropy(blk(x, Ac), blk(p, Ac))
        log(f"Tier-1 purity alpha={al}: S(A)={sa:.12f} S(Ac)={sc:.12f} rel {abs(sa - sc) / sa:.1e} [{'PASS' if abs(sa - sc) / sa < 1e-8 else 'FAIL'}]")
        if abs(sa - sc) / sa >= 1e-8: sys.exit(3)

def main():
    log("EXP-035 start")
    tier1()
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for al in ALPHAS:
        for eta in ETAS:
            for n_p in NPS:
                for nodes in NODES:
                    key = f"a{al}_e{eta}_np{n_p}_q{nodes}"
                    if key in res: continue
                    t0 = time.time(); v, M, ee = iG(al, eta, n_p, nodes)
                    res[key] = {"i90": v[0], "i180": v[1], "M": M, "eta_eff": ee}
                    json.dump(res, open(OUT, "w"), indent=0)
                    log(f"  {key}: M={M} eta_eff={ee:.6f}  done ({time.time() - t0:.0f} s)")
    log("all done; analysis:")
    analyse(res)

def analyse(res):
    g = lambda al, eta, th, n_p=NPS[-1], q=NODES[-1]: res[f"a{al}_e{eta}_np{n_p}_q{q}"]["i90" if th == 90 else "i180"]
    log("gates:")
    worst_q = max(abs(g(al, e, th, q=NODES[0]) / g(al, e, th) - 1) for al in ALPHAS for e in ETAS for th in (90, 180))
    log(f"  s-quadrature 48 vs 96 nodes, max rel diff over all: {worst_q:.2e} [{'PASS' if worst_q < 1e-3 else 'FAIL'}]")
    worst_n = 0.0
    for al in ALPHAS:
        for e in ETAS:
            for th in (90, 180):
                d = abs(g(al, e, th, n_p=NPS[-2]) / g(al, e, th) - 1); worst_n = max(worst_n, d)
    log(f"  points-per-arc 64 vs 128, max rel diff over all: {worst_n:.2e} [{'PASS' if worst_n < 0.02 else 'FAIL'}]")
    for al in ALPHAS:
        for e in ETAS:
            log(f"    n_p drift alpha={al} eta={e}: " + "  ".join(
                f"th={th}: {[round(g(al, e, th, n_p=n), 7) for n in NPS]}" for th in (90, 180)))
    worst_l = 0.0
    for (al, e, th), lat in LATTICE_B.items():
        c = g(al, e, th); worst_l = max(worst_l, abs(c / lat - 1))
        log(f"    known answer alpha={al} eta={e} th={th}: continuum {c:.6f} lattice(EXP-034a B) {lat:.6f} ratio {c / lat:.4f}")
    log(f"  continuum vs lattice at eta = 0.40, 0.25: max |ratio - 1| = {worst_l:.3f} [{'PASS' if worst_l < 0.15 else 'FAIL'}]")
    log("i_G table (n_p = 128, 96 nodes):")
    for al in ALPHAS:
        for th in (90, 180):
            log(f"  alpha={al} th={th}: " + "  ".join(f"{e}:{g(al, e, th):.6g}" for e in ETAS))
    log("verdict quantities (frozen thresholds; report.md EXP-035):")
    for al in ALPHAS:
        log(f"  alpha={al}: R1 = i_G(0.01)/i_G(0.1): " + "  ".join(f"th={th}: {g(al, 0.01, th) / g(al, 0.1, th):.4f}" for th in (90, 180))
            + "   R2 = i_G(0.001)/i_G(0.01): " + "  ".join(f"th={th}: {g(al, 0.001, th) / g(al, 0.01, th):.4f}" for th in (90, 180)))
    log(f"  scalar |i_G(90)-i_G(180)| at 0.01: {abs(g(1.0, 0.01, 90) - g(1.0, 0.01, 180)):.3e}; at 0.001: {abs(g(1.0, 0.001, 90) - g(1.0, 0.001, 180)):.3e}")
    for th in (90, 180):
        log(f"  descriptive, scalar th={th}: i_G * ln^2(1/eta): " + "  ".join(f"{e}:{g(1.0, e, th) * np.log(1 / e) ** 2:.5f}" for e in ETAS))

if __name__ == "__main__":
    analyse(json.load(open(OUT))) if sys.argv[1:] == ["--analyse"] else main()
