"""notes/fable/dim_spread.py  (Fable side-session, 2026-11-18; untracked scratch, not a registered EXP)

Question: how does the spread of kappa_d / C_T between the three anchor theories (free real scalar, free Dirac
fermion, Einstein holography) depend on the spacetime dimension d?  kappa_d = strip coefficient,
S_strip = area - kappa_d * A / w^(d-2).

Method.
  free fields: dimensional reduction (Casini-Huerta):  kappa_d = Omega_{d-3} / ((d-2) (2 pi)^(d-2)) * M(d),
               M(d) = int_0^inf t^(d-3) c(t) dt,  c(t) = L dS/dL of ONE massive 2d field at t = m L.
               c(t) is measured here on infinite 1d lattices (harmonic chain; staggered-mass hopping chain),
               at L = L1 and 2*L1 with m = t/L, Richardson-extrapolated in 1/L^2.
  Einstein:    closed form (Ryu-Takayanagi strip), any d.
  C_T:         Osborn-Petkou free values; holographic closed form.

Controls frozen BEFORE the d-scan is read (tolerance 0.5%):
  K2a  kappa_3(real scalar)  = 4.179  * 3/(32 pi^2) = 0.039697
  K2b  kappa_3(Dirac, 2-comp)= 3.8005 * 3/(16 pi^2) = 0.072205
  K3   Einstein kappa_3/C_T  = pi^2 Gamma(3/4)^4 / 6 = 3.7092 ; thermal Dirac/Einstein at d=3 = 0.99957
If K2 fails, nothing below the control block is to be read.
"""
import sys, math, json, time
import numpy as np
from scipy.special import zeta, gamma
from scipy.interpolate import CubicSpline
from scipy.integrate import quad

def S_gauss_boson(XA, PA):
    ev, U = np.linalg.eigh(XA)
    Xh = (U * np.sqrt(np.clip(ev, 0, None))) @ U.T
    C = Xh @ PA @ Xh
    nu = np.sqrt(np.clip(np.linalg.eigvalsh((C + C.T) / 2), 0.25, None))
    a, b = nu + 0.5, nu - 0.5
    return float(np.sum(a * np.log(a)) - np.sum(b[b > 1e-15] * np.log(b[b > 1e-15])))

def scalar_S(m, Ls, N):
    k = 2 * np.pi * np.fft.rfftfreq(N)            # 0 .. pi
    w = np.sqrt(m * m + 4 * np.sin(k / 2) ** 2)
    X = np.fft.irfft(1 / (2 * w), n=N)
    P = np.fft.irfft(w / 2, n=N)
    out = {}
    for L in Ls:
        idx = np.abs(np.subtract.outer(np.arange(L), np.arange(L)))
        out[L] = S_gauss_boson(X[idx], P[idx])
    return out

def dirac_S(m, Ls, N):
    k = 2 * np.pi * np.arange(N) / N
    E = np.sqrt(np.sin(k) ** 2 + m * m)
    A = np.fft.ifft(0.5 * (1 - np.sin(k) / E))    # A(r) = (1/N) sum_k e^{ikr} ...
    B = np.fft.ifft(-m / (2 * E))
    out = {}
    for L in Ls:
        i = np.arange(L)
        r = np.subtract.outer(i, i).T              # r[i,j] = j - i
        C = A[r % N] + ((-1.0) ** i)[None, :] * B[r % N]
        C = (C + C.conj().T) / 2
        nu = np.clip(np.linalg.eigvalsh(C), 1e-300, 1 - 1e-16)
        out[L] = float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log1p(-nu)))
    return out

def c_of_t(kind, t, L, h):
    m = t / L
    # memory-light: m*N >= 20 (finite-ring error ~ e^{-20}); cap 2^22 real (scalar) / 2^21 complex (Dirac)
    N = 1 << int(max(16, math.ceil(math.log2(20.0 / m))))
    N = min(N, (1 << 22) if kind == "S" else (1 << 21))
    f = scalar_S if kind == "S" else dirac_S
    S = f(m, [L - h, L + h], N)
    return L * (S[L + h] - S[L - h]) / (2 * h), m * N

def c_rich(kind, t, L1):
    h = 1 if kind == "S" else 2
    c1, mn1 = c_of_t(kind, t, L1, h)
    c2, mn2 = c_of_t(kind, t, 2 * L1, h)
    return (4 * c2 - c1) / 3, c1, c2, min(mn1, mn2)

# ---------- closed forms ----------
def S_d(d): return 2 * math.pi ** (d / 2) / gamma(d / 2)
def CT_scalar(d): return d / ((d - 1) * S_d(d) ** 2)
def CT_dirac_per_comp(d): return d / (2 * S_d(d) ** 2)           # times number of components N_c
def pref(d): return (2 * math.pi ** ((d - 2) / 2) / gamma((d - 2) / 2)) / ((d - 2) * (2 * math.pi) ** (d - 2))
def kappa_over_CT_einstein(d):
    k = (1 / 4) * (2 ** (d - 1) * math.pi ** ((d - 1) / 2) / (d - 2)) * (gamma(d / (2 * d - 2)) / gamma(1 / (2 * d - 2))) ** (d - 1)
    ct = (d + 1) / (d - 1) * gamma(d + 1) / (math.pi ** (d / 2) * gamma(d / 2)) / (8 * math.pi)
    return k / ct
def thermal_over_CT(d):
    sB = d * gamma(d / 2) * zeta(d) / math.pi ** (d / 2)          # entropy density / T^(d-1), per real bosonic dof
    S_ = sB / CT_scalar(d)
    D_ = (1 - 2 ** (1 - d)) * sB / CT_dirac_per_comp(d)            # per component: N_c dof / (N_c * CT_per_comp)
    ct = (d + 1) / (d - 1) * gamma(d + 1) / (math.pi ** (d / 2) * gamma(d / 2)) / (8 * math.pi)
    E_ = (1 / 4) * (4 * math.pi / d) ** (d - 1) / ct
    return S_, D_, E_

if __name__ == "__main__":
    t0 = time.time()
    L1 = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    ts = np.exp(np.linspace(math.log(2.5e-3), math.log(30.0), 52))
    res = {"S": [], "D": []}
    for kind in ("S", "D"):
        for t in ts:
            c, c1, c2, mn = c_rich(kind, float(t), L1)
            res[kind].append((float(t), c, c1, c2, mn))
        print(f"[{kind}] done at {time.time()-t0:.0f}s", flush=True)
    print("\n t        c_S(rich)  c_S(L1)   c_S(2L1)  | c_D(rich)  c_D(L1)   c_D(2L1)   min m*N")
    for a, b in zip(res["S"], res["D"]):
        print(f"{a[0]:9.4g} {a[1]:9.6f} {a[2]:9.6f} {a[3]:9.6f} | {b[1]:9.6f} {b[2]:9.6f} {b[3]:9.6f}  {min(a[4],b[4]):8.1f}")

    lt = np.log(ts)
    spl = {k: CubicSpline(lt, np.array([r[1] for r in res[k]])) for k in res}
    def M(kind, d, col=1):
        sp = spl[kind] if col == 1 else CubicSpline(lt, np.array([r[col] for r in res[kind]]))
        body = quad(lambda x: math.exp((d - 2) * x) * float(sp(x)), lt[0], lt[-1], limit=400)[0]
        tail = float(sp(lt[0])) * ts[0] ** (d - 2) / (d - 2)          # c ~ const below t_min
        return body + tail, tail / (body + tail)

    print("\n=== CONTROLS (read these first) ===")
    kS, _ = M("S", 3.0); kD, _ = M("D", 3.0)
    kS, kD = kS / math.pi, kD / math.pi
    refS, refD = 4.179 * 3 / (32 * math.pi ** 2), 3.8005 * 3 / (16 * math.pi ** 2)
    print(f"K2a kappa_3 scalar = {kS:.6f}  ref {refS:.6f}  rel {kS/refS-1:+.3%}")
    print(f"K2b kappa_3 Dirac  = {kD:.6f}  ref {refD:.6f}  rel {kD/refD-1:+.3%}")
    for col, name in ((2, "L1 only"), (3, "2*L1 only")):
        a = M("S", 3.0, col)[0] / math.pi; b = M("D", 3.0, col)[0] / math.pi
        print(f"    nuisance ({name}): scalar {a/refS-1:+.3%}  Dirac {b/refD-1:+.3%}")
    print(f"K3  Einstein kappa_3/C_T = {kappa_over_CT_einstein(3.0):.5f}  ref {math.pi**2*gamma(0.75)**4/6:.5f}")
    th = thermal_over_CT(3.0)
    print(f"K3  thermal d=3: scalar/C_T {th[0]:.3f} (60.4?)  Dirac/Einstein {th[1]/th[2]:.5f} (0.99957?)")
    print(f"    RT d=4 strip number 2 sqrt(pi) (G(2/3)/G(1/6))^3 = {2*math.sqrt(math.pi)*(gamma(2/3)/gamma(1/6))**3:.5f} (0.0513?)")
    print(f"    c_D(t_min) = {res['D'][0][1]:.5f} (-> 1/3);  c_S(t_min) = {res['S'][0][1]:.5f}; 1/3 + 1/(2 ln t_min) = {1/3 + 1/(2*math.log(ts[0])):.5f}")

    print("\n=== d-scan: kappa_d / C_T, Einstein-normalised ===")
    print("   d    S/E      D/E      S/D    | thermal S/E  D/E   | small-t tail frac (S, D) | k_d scalar   k_d Dirac(per 2 comp)")
    rows = []
    for d in (2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 4.5, 5.0, 6.0):
        MS, tS = M("S", d); MD, tD = M("D", d)
        kS = pref(d) * MS; kD2 = pref(d) * MD                     # Dirac: per pair of components
        rS = kS / CT_scalar(d); rD = kD2 / (2 * CT_dirac_per_comp(d)); rE = kappa_over_CT_einstein(d)
        th = thermal_over_CT(d)
        rows.append(dict(d=d, S_over_E=rS / rE, D_over_E=rD / rE, S_over_D=rS / rD, th_S_over_E=th[0] / th[2],
                         th_D_over_E=th[1] / th[2], kS=kS, kD2=kD2, tailS=tS, tailD=tD))
        print(f"{d:5.2f} {rS/rE:8.4f} {rD/rE:8.4f} {rS/rD:8.4f} | {th[0]/th[2]:8.4f} {th[1]/th[2]:8.4f} |"
              f"  {tS:.3f} {tD:.3f}  | {kS:.6g}  {kD2:.6g}")
    json.dump(dict(L1=L1, c_table=res, rows=rows), open(f"scripts/exp040_impl1_L{L1}.json", "w"), indent=1)
    print(f"\nwall {time.time()-t0:.0f}s")
