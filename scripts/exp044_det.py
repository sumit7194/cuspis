"""EXP-044 (pre-registered in report.md, d669fbd): lattice-free von Neumann c-functions from the Fredholm determinant
det(1 - lam^2 R R^T) (CFH05 (58)-(60)) and the n -> 1 continuation (CH07b (42); scalar weight derived in the
registration). Nystrom/trapezoid quadrature in p = ln u (Born10). [model: Opus 5.5]
Usage: python exp044_det.py tier1 | gates | run"""
import sys, math, time, json, os
import numpy as np
from scipy.integrate import quad
from scipy.special import k1

D0 = os.path.dirname(os.path.abspath(__file__))

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

# ---------------- determinant ----------------
def w_det(t, theta, lam2, sign, h=0.1, P=None):
    """w = sign * t d/dt log det(1 - lam2 * R R^T); returns (w, det, roundoff_floor, m)."""
    if P is None:
        P = math.acosh(max(2.0, 90.0 / t))
    p = np.arange(-P, P + 0.5 * h, h)
    ch = np.cosh(p); E = np.exp(-0.5 * t * ch)
    dp = p[:, None] - p[None, :]
    R = np.exp(0.5 * theta * dp) * (E[:, None] * E[None, :]) / (2.0 * np.cosh(0.5 * dp))
    dR = -0.5 * (ch[:, None] + ch[None, :]) * R
    RT = R.T
    A = h * h * (R @ RT)
    dA = h * h * (dR @ RT + R @ dR.T)
    M = np.eye(len(p)) - lam2 * A
    sgn, ld = np.linalg.slogdet(M)
    dlog = -lam2 * np.trace(np.linalg.solve(M, dA))
    detv = sgn * np.exp(ld)
    floor = math.sqrt(len(p)) * np.linalg.norm(lam2 * A) * 2.0 ** -53 / max(abs(detv), 1e-300)
    return sign * t * dlog, detv, floor, len(p)

def w_dirac(t, a, **kw):          # a may be complex; theta = 2a, lam^2 = -sin^2(pi a)/pi^2
    return w_det(t, 2 * a, -np.sin(np.pi * a) ** 2 / np.pi ** 2, +1, **kw)

def w_scalar(t, a, **kw):         # theta = 2a - 1, lam^2 = sin^2(pi a)/pi^2, Z = 1/<V V>
    return w_det(t, 2 * a - 1, np.sin(np.pi * a) ** 2 / np.pi ** 2, -1, **kw)

# ---------------- C0: continuation identities ----------------
def C0():
    ok = True
    for b in (1.0, 3.0, 5.0):
        exact = 1 - (b / 2) / math.tan(b / 2)
        def fD(s):                # pi (cosh(bs) - 1)/sinh^2(pi s), overflow-safe: 4 pi (cosh bs - 1) e^{-2 pi s}/(1 - e^{-2 pi s})^2
            if s < 1e-6: return b * b / (2 * math.pi)
            q = math.exp(-2 * math.pi * s)
            return 2 * math.pi * (math.exp((b - 2 * math.pi) * s) + math.exp(-(b + 2 * math.pi) * s) - 2 * q) / (1 - q) ** 2
        num = quad(fD, 0, 60, limit=400, epsabs=1e-15, epsrel=1e-13)[0]
        r = abs(num - exact); ok &= r < 1e-10
        log(f"C0 Dirac beta={b}: integral {num:.15f}  n->1 limit {exact:.15f}  diff {r:.1e} [{'PASS' if r < 1e-10 else 'FAIL'}]")
        exact_s = -b / (4 * math.sin(b / 2))
        def fS(s):                # pi cosh(bs)/cosh^2(pi s) = 2 pi (e^{(b-2pi)s} + e^{-(b+2pi)s})/(1 + e^{-2pi s})^2
            q = math.exp(-2 * math.pi * s)
            return 2 * math.pi * (math.exp((b - 2 * math.pi) * s) + math.exp(-(b + 2 * math.pi) * s)) / (1 + q) ** 2
        num_s = -0.5 * quad(fS, 0, 60, limit=400, epsabs=1e-15, epsrel=1e-13)[0]
        # independent check of the closed-form limit: finite-difference in n of the integer-n Dirichlet sum, continued in n
        G = lambda n: math.sin(b * (n - 1) / (2 * n)) / math.sin(b / (2 * n)) / (2 * (1 - n))
        fd = (G(1 + 1e-5) + G(1 - 1e-5)) / 2
        r2 = abs(num_s - exact_s); ok &= r2 < 1e-10
        log(f"C0 scalar beta={b}: -1/2 integral {num_s:.15f}  n->1 limit {exact_s:.15f} (finite-n check {fd:.10f})  diff {r2:.1e} [{'PASS' if r2 < 1e-10 else 'FAIL'}]")
    return ok

def tier1():
    log("EXP-044 Tier 1"); C0()
    for t in (1e-3, 0.3, 3.0):
        for s in (0.0, 0.5, 2.0):
            t0 = time.time(); wD, dD, fD, m = w_dirac(t, 1j * s); el = time.time() - t0
            wS, dS, fS, _ = w_scalar(t, 0.5 + 1j * s)
            log(f"  t={t} s={s}: m={m}  w_D={complex(wD):.10f} (massless 2s^2={2*s*s:.4f}) det_D={complex(dD):.6e} floor {fD:.1e} | "
                f"w_S={complex(wS):.10f} (massless -1/2-2s^2={-0.5-2*s*s:.4f}) det_S={complex(dS):.6e} floor {fS:.1e}  [{el*1e3:.0f} ms]")

# ---------------- lattice Renyi-2 (G1); conventions of exp040_impl1_dim_spread.py, entropy swapped for S_2 ----------------
def lat_S2_scalar(m, Ls, N):
    k = 2 * np.pi * np.fft.rfftfreq(N); w = np.sqrt(m * m + 4 * np.sin(k / 2) ** 2)
    X = np.fft.irfft(1 / (2 * w), n=N); P = np.fft.irfft(w / 2, n=N); out = {}
    for L in Ls:
        idx = np.abs(np.subtract.outer(np.arange(L), np.arange(L)))
        ev, U = np.linalg.eigh(X[idx]); Xh = (U * np.sqrt(np.clip(ev, 0, None))) @ U.T
        C = Xh @ P[idx] @ Xh; nu = np.sqrt(np.clip(np.linalg.eigvalsh((C + C.T) / 2), 0.25, None))
        out[L] = float(np.sum(np.log(2 * nu)))                      # S_2 = sum log((nu+1/2)^2 - (nu-1/2)^2)
    return out

def lat_S2_dirac(m, Ls, N):
    k = 2 * np.pi * np.arange(N) / N; E = np.sqrt(np.sin(k) ** 2 + m * m)
    A = np.fft.ifft(0.5 * (1 - np.sin(k) / E)); B = np.fft.ifft(-m / (2 * E)); out = {}
    for L in Ls:
        i = np.arange(L); r = np.subtract.outer(i, i).T
        C = A[r % N] + ((-1.0) ** i)[None, :] * B[r % N]; C = (C + C.conj().T) / 2
        nu = np.clip(np.linalg.eigvalsh(C), 1e-300, 1 - 1e-16)
        out[L] = float(-np.sum(np.log(nu ** 2 + (1 - nu) ** 2)))    # S_2 = -sum log(nu^2 + (1-nu)^2)
    return out

def lat_c2(kind, t, L1):
    def one(L):
        h = 1 if kind == "S" else 2; m = t / L
        N = min(1 << int(max(16, math.ceil(math.log2(20.0 / m)))), (1 << 21))
        S = (lat_S2_scalar if kind == "S" else lat_S2_dirac)(m, [L - h, L + h], N)
        return L * (S[L + h] - S[L - h]) / (2 * h)
    c1, c2 = one(L1), one(2 * L1); cr = (4 * c2 - c1) / 3
    return cr, 3 * abs(cr - c2) + 1e-6

# ---------------- c(t) from the continuation ----------------
def c_vn(kind, t, ns=48, smax=5.0, h=0.1, dP=0.0, lamfac=1.0):
    x, wq = np.polynomial.legendre.leggauss(ns); s = 0.5 * smax * (x + 1); wq = 0.5 * smax * wq
    P = math.acosh(max(2.0, 90.0 / t)) + dP; tot = 0.0
    for si, wi in zip(s, wq):
        if kind == "D":
            th, l2, sg, wt = 2j * si, lamfac * np.sinh(np.pi * si) ** 2 / np.pi ** 2, +1, np.pi / np.sinh(np.pi * si) ** 2
            tot += wi * wt * w_det(t, th, l2, sg, h=h, P=P)[0].real
        else:
            th, l2, sg, wt = 2j * si, lamfac * np.cosh(np.pi * si) ** 2 / np.pi ** 2, -1, np.pi / np.cosh(np.pi * si) ** 2
            tot += -0.5 * wi * wt * w_det(t, th, l2, sg, h=h, P=P)[0].real
    return tot

# ---------------- moments and crossings (EXP-040 formula, Impl-1 prefactors) ----------------
with __import__("contextlib").redirect_stdout(__import__("io").StringIO()):
    import exp040_impl1_dim_spread as I1
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
small = {"D": lambda u: 1/3 - math.exp(2 * u) * u * u / 3, "S": lambda u: 1/3 + 1 / (2 * u)}
large = {"D": lambda t: 0.5 * t * k1(2 * t), "S": lambda t: 0.25 * t * k1(2 * t)}
def moment(kind, d, U, C):
    sp = CubicSpline(U, np.exp((d - 2) * U) * C); body = sp.integrate(U[0], U[-1])
    lo = -max(200.0, 60.0 / (d - 2))
    tail_lo = quad(lambda u: math.exp((d - 2) * u) * small[kind](u), lo, U[0], limit=400)[0]
    tail_hi = quad(lambda t: t ** (d - 3) * large[kind](t), math.exp(U[-1]), 60, limit=200)[0]
    return body + tail_lo + tail_hi
def ratio(kind, d, U, C):
    M = moment(kind, d, U, C)
    return I1.pref(d) * M / (I1.CT_scalar(d) if kind == "S" else 2 * I1.CT_dirac_per_comp(d))
def crossings(US, CS, UD, CD):
    E = I1.kappa_over_CT_einstein
    f = {"D/E": lambda d: ratio("D", d, UD, CD) - E(d), "S/E": lambda d: ratio("S", d, US, CS) - E(d),
         "S/D": lambda d: ratio("S", d, US, CS) - ratio("D", d, UD, CD)}
    br = {"D/E": (2.85, 3.05), "S/E": (2.75, 2.95), "S/D": (2.65, 2.85)}
    return {k: brentq(f[k], *br[k], xtol=1e-9) for k in f}

def gates():
    out = {}
    log("=== K-mom: moment code on the Impl-2 tables must give 2.9435 / 2.7513 / 2.8487 to 2e-4 ===")
    J = json.load(open(os.path.join(D0, "exp040_impl2.json"))); U = np.array(J["U"])
    mk = np.exp(U) <= 8.0
    cr = crossings(U[mk], np.array(J["tab"]["S"]["cinf"])[mk], U[mk], np.array(J["tab"]["D"]["cinf"])[mk])
    ref = {"D/E": 2.9435, "S/D": 2.7513, "S/E": 2.8487}
    for k in ref: log(f"  {k}: {cr[k]:.5f} vs {ref[k]}  [{'PASS' if abs(cr[k]-ref[k]) <= 2e-4 else 'FAIL'}]")
    out["Kmom"] = cr
    log("=== G1: n = 2 pipeline gate (determinant vs lattice Renyi-2) ===")
    g1 = True
    for t in (0.3, 1.0, 2.0):
        dD = -2 * w_dirac(t, 0.25)[0].real; dS = -0.5 * w_scalar(t, 0.5)[0].real
        lD, tD = lat_c2("D", t, 100); lS, tS = lat_c2("S", t, 100)
        okD, okS = abs(dD - lD) <= tD, abs(dS - lS) <= tS; g1 &= okD and okS
        log(f"  t={t}: Dirac det {dD:.7f} lattice {lD:.7f} (tol {tD:.1e}) [{'PASS' if okD else 'FAIL'}] | "
            f"scalar det {dS:.7f} lattice {lS:.7f} (tol {tS:.1e}) [{'PASS' if okS else 'FAIL'}]")
    t = 0.01; dD = -2 * w_dirac(t, 0.25)[0].real; dS = -0.5 * w_scalar(t, 0.5)[0].real
    fD = 0.25 * (1 - t * t * math.log(t) ** 2); fS = 0.25 + 1 / (2 * math.log(t))
    g1 &= abs(dD - fD) < 1e-4 and abs(dS - fS) < 0.02
    log(f"  t=0.01 small-t forms: Dirac {dD:.7f} vs {fD:.7f} | scalar {dS:.5f} vs {fS:.5f} (weak, tol 0.02)")
    log(f"  G1 {'PASS' if g1 else 'FAIL -- STOP'}"); out["G1"] = g1
    if not g1 and "--g1prime" not in sys.argv: return out
    if not g1: log("  proceeding under G1' (post-failure replacement accepted by the Bridge; report.md EXP-044)")
    log("=== G2: solver floor first, then halving (h, P) -> (h/2, P+2) ===")
    g2 = True
    for t in (0.3, 3.0):
        for s in (0.0, 1.0, 3.0):
            for kind in ("D", "S"):
                a = s * 1j if kind == "D" else 0.5 + s * 1j; fn = w_dirac if kind == "D" else w_scalar
                if kind == "D" and s == 0.0: continue                  # w_D(0) = 0 identically
                w1, d1, fl, m = fn(t, a); P0 = math.acosh(max(2.0, 90.0 / t))
                w2, d2, _, m2 = fn(t, a, h=0.05, P=P0 + 2)
                rel = abs(w1.real / w2.real - 1); im = abs(d1.imag) / abs(d1)
                ok = rel <= 1e-8 and im <= 1e-10; g2 &= ok
                log(f"  {kind} t={t} s={s}: w {w1.real:.12f} -> {w2.real:.12f} rel {rel:.1e}; Im(det)/|det| {im:.1e}; floor {fl:.1e}; m {m}->{m2} [{'PASS' if ok else 'FAIL'}]")
    log(f"  G2 {'PASS' if g2 else 'FAIL'}"); out["G2"] = g2
    log("=== G4: consistency with Impl-2 lattice c_D, and asymptotic checks ===")
    cD = np.array(J["tab"]["D"]["cinf"]); two = np.array(J["tab"]["D"]["two"]); g4 = True
    for tt in (0.1, 0.3, 1.0, 2.0, 4.0):
        i = int(np.argmin(abs(U - math.log(tt)))); t = float(math.exp(U[i])); v = c_vn("D", t)
        tol = 3 * abs(cD[i] - two[i]) + 1e-6; ok = abs(v - cD[i]) <= tol; g4 &= ok
        log(f"  t={t:.5f}: det {v:.8f} lattice {cD[i]:.8f} diff {v-cD[i]:+.2e} tol {tol:.1e} [{'PASS' if ok else 'FAIL'}]")
    log(f"  G4 {'PASS' if g4 else 'FAIL'}"); out["G4"] = g4
    a1 = c_vn("D", 1e-3); a2 = c_vn("D", 5.0); r1 = abs(a1 - (1/3 - 1e-6 * math.log(1e-3) ** 2 / 3)); r2 = abs(a2 / (2.5 * k1(10.0)) - 1)
    log(f"  asymptotics: |c_D(1e-3) - (1/3 - t^2 ln^2 t/3)| = {r1:.1e} (<1e-6: {'PASS' if r1 < 1e-6 else 'FAIL'});  c_D(5)/(1/2 t K1(2t)) - 1 = {r2:.1e} (<1e-3: {'PASS' if r2 < 1e-3 else 'FAIL'})")
    out["asym"] = [r1, r2]
    return out

def run(nt=160):
    t0 = time.time(); res = {}
    U = np.linspace(math.log(1e-5), math.log(8.0), nt)
    base = {"D": np.array([c_vn("D", math.exp(u)) for u in U]), "S": np.array([c_vn("S", math.exp(u)) for u in U])}
    log(f"base c(t) on {nt} nodes done ({time.time()-t0:.0f} s); c_D(1e-5) {base['D'][0]:.8f}, c_S(1e-5) {base['S'][0]:.6f}")
    cr0 = crossings(U, base["S"], U, base["D"]); res["base"] = cr0
    log(f"P1/P1b base crossings: " + "  ".join(f"{k} {v:.5f}" for k, v in cr0.items()))
    var = {}
    U2 = np.linspace(math.log(1e-5), math.log(8.0), 2 * nt - 1)
    var["t-grid x2"] = crossings(U2, np.array([c_vn("S", math.exp(u)) for u in U2]), U2, np.array([c_vn("D", math.exp(u)) for u in U2]))
    Ux = np.linspace(math.log(2e-5), math.log(4.0), nt)
    var["patches x2"] = crossings(Ux, np.array([c_vn("S", math.exp(u)) for u in Ux]), Ux, np.array([c_vn("D", math.exp(u)) for u in Ux]))
    var["s: 96 nodes, smax 7"] = crossings(U, np.array([c_vn("S", math.exp(u), ns=96, smax=7) for u in U]), U, np.array([c_vn("D", math.exp(u), ns=96, smax=7) for u in U]))
    Uc = U[::2]
    cS_c = np.array([c_vn("S", math.exp(u)) for u in Uc]); cD_c = np.array([c_vn("D", math.exp(u)) for u in Uc])
    cS_h = np.array([c_vn("S", math.exp(u), h=0.05, dP=2) for u in Uc]); cD_h = np.array([c_vn("D", math.exp(u), h=0.05, dP=2) for u in Uc])
    a, b = crossings(Uc, cS_c, Uc, cD_c), crossings(Uc, cS_h, Uc, cD_h)
    var["det (h/2, P+2) [on half grid]"] = {k: cr0[k] + (b[k] - a[k]) for k in cr0}
    for k, v in var.items(): log(f"  variant {k}: " + "  ".join(f"{p} {v[p]:.5f} (d {v[p]-cr0[p]:+.1e})" for p in cr0))
    cD3 = np.array([c_vn("D", math.exp(u), lamfac=1.05) for u in U])
    # run-1 fix (one variable): scan D for the D/E sign change instead of a fixed brentq bracket, which the moved
    # crossing left. A missing crossing in [2.2, 4.5] counts as the control firing.
    E = I1.kappa_over_CT_einstein; grid = np.arange(2.2, 4.5001, 0.01)
    fv = [ratio("D", d, U, cD3) - E(d) for d in grid]; sc = [i for i in range(len(grid) - 1) if fv[i] * fv[i + 1] < 0]
    G3 = {"D/E": brentq(lambda d: ratio("D", d, U, cD3) - E(d), grid[sc[0]], grid[sc[0] + 1], xtol=1e-9) if sc else float("nan"),
          "n_crossings_in_[2.2,4.5]": len(sc), "ratio_at_3": fv[80] + E(3.0), "E_at_3": E(3.0)}
    log(f"G3 scan: {len(sc)} D/E sign change(s) in [2.2, 4.5]; Dirac kappa/C_T at D=3 {G3['ratio_at_3']:.5f} vs base {ratio('D', 3.0, U, base['D']):.5f}")
    g3c = [c_vn("D", 1e-3, lamfac=1.05), c_vn("D", 4.0, lamfac=1.05) / (2.0 * k1(8.0))]
    log(f"G3 must-fail (lambda^2 x 1.05, Dirac): c_D(1e-3) = {g3c[0]:.6f} (1/3 miss {abs(g3c[0]-1/3):.1e}); c_D(4)/(1/2tK1) = {g3c[1]:.4f}; D/E crossing {G3['D/E']:.5f} (moved {G3['D/E']-cr0['D/E']:+.4f})")
    ref = {"D/E": 2.9435, "S/D": 2.7513, "S/E": 2.8487}; spread = {"D/E": 0.0013, "S/D": 0.0022, "S/E": 0.0006}
    for p in ref:
        comb = spread[p] + sum(abs(v[p] - cr0[p]) for v in var.values())
        d = cr0[p] - ref[p]
        log(f"{'P1 ' if p == 'D/E' else 'P1b'} {p}: determinant {cr0[p]:.5f} vs EXP-040 {ref[p]}  diff {d:+.5f}  combined error {comb:.5f}  "
            f"[{'PASS' if abs(d) <= comb else 'FAIL'}]")
    g3ok = (abs(g3c[0] - 1/3) > 1e-3 or abs(g3c[1] - 1) > 0.01) and (math.isnan(G3["D/E"]) or abs(G3["D/E"] - cr0["D/E"]) > spread["D/E"]) + sum(abs(v["D/E"] - cr0["D/E"]) for v in var.values())
    log(f"G3 {'PASS (control fires)' if g3ok else 'FAIL (control does not fire: P1 VOID)'}")
    res.update(variants=var, G3=dict(cross=G3, c=g3c), U=U.tolist(), cD=base["D"].tolist(), cS=base["S"].tolist())
    json.dump(res, open(os.path.join(D0, "exp044_results.json"), "w"), indent=0)
    log(f"done ({time.time()-t0:.0f} s)")

if __name__ == "__main__":
    {"tier1": tier1, "gates": gates, "run": run}[sys.argv[1]]()
