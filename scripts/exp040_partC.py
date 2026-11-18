"""EXP-040 Part C (registration in report.md): is a crossing near D = 3 generic for theories pinned at D = 2?
C1 control: same-C_T-law toy pairs with monotone c-ratio must not cross; a hand-built non-monotone pair must.
C2: scalar/Dirac decomposition r = h q on the Impl-2 c-tables (scripts/exp040_impl2.json).
C3: 12 x 12 scalar-law / Dirac-law toy pairs; fraction crossing in (2, 4) and the spread of D_c.
Toy c(t) = N_p (t/4) K1(2t) + e0 exp(-(t/tau)^p), c(0) = 1/3 per field; Mellin moments in closed form:
  int t^(D-3) N_p (t/4)K1(2t) dt = N_p Gamma(D/2-1) Gamma(D/2)/16;  int t^(D-3) e0 exp(-(t/tau)^p) dt = e0 tau^(D-2) Gamma((D-2)/p)/p."""
import json, math, itertools
import numpy as np
from scipy.special import gamma, k1

TAUS, PS = (0.1, 0.3, 1.0, 3.0), (0.5, 1.0, 2.0)
DG = np.linspace(2.02, 6.0, 400)

def toy(Np, tau, p):
    e0 = 1 / 3 - Np / 8
    M = lambda D: Np * gamma(D / 2 - 1) * gamma(D / 2) / 16 + e0 * tau ** (D - 2) * gamma((D - 2) / p) / p
    c = lambda t: Np * (t / 4) * k1(2 * t) + e0 * math.exp(-(t / tau) ** p)
    return M, c

def crossings(lnr):
    s = np.sign(lnr); idx = np.where(s[:-1] * s[1:] < 0)[0]
    return [float(DG[i] - lnr[i] * (DG[i + 1] - DG[i]) / (lnr[i + 1] - lnr[i])) for i in idx]

def ratio_monotone(cx, cy):
    tg = np.exp(np.linspace(math.log(1e-4), math.log(15), 600))
    r = np.array([cx(t) / cy(t) for t in tg]); d = np.diff(r)
    return bool(np.all(d >= -1e-12) or np.all(d <= 1e-12))

if __name__ == "__main__":
    print("=== C1 control: same-law pairs ===")
    for Np, lab in ((1, "scalar-law"), (2, "Dirac-law")):
        toys = [toy(Np, t, p) for t in TAUS for p in PS]
        n_mono = n_mono_cross = n_non = n_non_cross = 0
        for (Mx, cx), (My, cy) in itertools.combinations(toys, 2):
            lnr = np.array([math.log(Mx(D) / My(D)) for D in DG])
            cr = crossings(lnr)
            if ratio_monotone(cx, cy):
                n_mono += 1; n_mono_cross += bool(cr)
            else:
                n_non += 1; n_non_cross += bool(cr)
        print(f"  {lab}: {n_mono} pairs with monotone c-ratio, {n_mono_cross} cross (must be 0); "
              f"{n_non} non-monotone pairs, {n_non_cross} cross")
    # hand-built non-monotone pair (scalar law): X splits its excess between tau = 0.1 and 3, Y puts it at 0.7
    e0 = 1 / 3 - 1 / 8
    MX = lambda D: gamma(D/2-1)*gamma(D/2)/16 + 0.5*e0*(0.1**(D-2) + 3.0**(D-2))*gamma(D-2)
    MY = lambda D: gamma(D/2-1)*gamma(D/2)/16 + e0*0.7**(D-2)*gamma(D-2)
    cr = crossings(np.array([math.log(MX(D) / MY(D)) for D in DG]))
    print(f"  hand-built non-monotone pair: crossings at {[round(x,3) for x in cr]}  (must be non-empty: {'FIRES' if cr else 'DOES NOT FIRE'})")

    print("\n=== C2: scalar/Dirac on the Impl-2 tables ===")
    J = json.load(open("scripts/exp040_impl2.json"))
    U = np.array(J["U"]); W = np.array(J["W"]); cS = np.array(J["tab"]["S"]["cinf"]); cD = np.array(J["tab"]["D"]["cinf"])
    rat = cD / cS; t = np.exp(U)
    dec = np.where(np.diff(rat) < 0)[0]
    print(f"  c_D/c_S at t = {t[0]:.1e}: {rat[0]:.4f};  t = 1: {np.interp(0, U, rat):.4f};  t = {t[-1]:.1f}: {rat[-1]:.4f}")
    print(f"  P1 monotone increasing on {len(t)} nodes: {'YES' if len(dec) == 0 else 'NO, decreases at t = ' + str([round(float(t[i]),4) for i in dec])}")
    def M(cv, D):
        return float(np.sum(W * np.exp((D - 2) * U) * cv))       # body only; same truncation for both (t >= 1e-5)
    q = np.array([2 * M(cS, D) / M(cD, D) for D in DG]); h = (DG - 1) / 2
    print(f"  q(D) monotone decreasing on the grid: {'YES' if np.all(np.diff(q) < 0) else 'NO'};  q(2.02) = {q[0]:.3f}, q(3) = {np.interp(3, DG, q):.4f}, q(6) = {q[-1]:.4f}")
    print(f"  P2 r(3) = q(3) > 1: {'YES' if np.interp(3, DG, q) > 1 else 'NO'};  crossing of h q = 1 at D = {crossings(np.log(h*q))}")
    print(f"  P3 d ln q/dD near 2 (finite differences, 2.02..2.10): {[round(float(x),2) for x in np.diff(np.log(q))[:8]/np.diff(DG)[:8]]}")

    print("\n=== C3: 12 x 12 scalar-law / Dirac-law toy pairs ===")
    S = [(f"tau{t}_p{p}", *toy(1, t, p)) for t in TAUS for p in PS]
    Dd = [(f"tau{t}_p{p}", *toy(2, t, p)) for t in TAUS for p in PS]
    Dc, none, multi = [], 0, 0
    for (ls, Ms, _), (ld, Md, _) in itertools.product(S, Dd):
        lnr = np.array([math.log((D - 1) * Ms(D) / Md(D)) for D in DG])
        cr = [x for x in crossings(lnr) if x < 4]
        if not cr: none += 1
        else:
            Dc.append(cr[0]); multi += len(cr) > 1
    Dc = np.array(Dc)
    print(f"  pairs crossing in (2, 4): {len(Dc)} of 144 ({none} do not); more than one crossing: {multi}")
    if len(Dc):
        q25, q50, q75 = np.percentile(Dc, [25, 50, 75])
        print(f"  D_c: min {Dc.min():.3f}, quartiles {q25:.3f} / {q50:.3f} / {q75:.3f}, max {Dc.max():.3f}; spread (max-min) {Dc.max()-Dc.min():.3f}, IQR {q75-q25:.3f}")
        print(f"  fraction of crossings in (2, 3): {np.mean(Dc < 3):.3f}")
    # the trio's actual pair, for orientation: one-particle part plus the measured excess
    print("  (the measured scalar/Dirac crossing is reported in Part B)")
