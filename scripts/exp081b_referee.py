"""EXP-081b N2 extended-precision referee (registered 0ab92d4): W=4 strip in the P=4 pair box (12x8), Ny=8, s in {1,2,3}.
Same formulas at 40 digits (mpmath): per-slice G0 by mp inverse, Woodbury K = (C^{-1}+M)^{-1} away from z=1, poles refined by
mp.findroot on det(I + M C(z)), residues by 40-digit contours. Compares the double-precision production on
 (a) every tail ingredient G_q(beta -+ i s_j) (all slices q, all poles s_j of all slices) and
 (b) the k=0 bubble B~_0(beta) (npt=24) and its logdet,
and the production N1'' checks for this geometry. Pass: relative agreement <= 1e-8 wherever N1'' calls production reliable.
RUN 2 (the Bridge's terms: own poles from a root-finder-free sign-change scan, compared with production; a missing/extra pole
below s_cut fires N2'; a seeded version was started and stopped, output kept as *_run2seeded_stopped*) (after run 1 fired for referee-side reasons, diagnosed in exp081b_refdiag*.py; run 1 kept as exp081b_referee_run1.py and
*_run1.*): (i) own poles: sign-change scan of F(s) = z^W det(I + M C(z)) (O(1) as z -> 0), not findroot in z on the unscaled det
(which converged to wrong roots for s_j >~ 1.7 in run 1); (ii) the same s_cut as production in (a) and
(b) (run 1 used all poles in B~_0, production drops s_j > s_cut); (iii) N2' impact rel x |logdet| x pi/cosh^2(pi s) <= 1e-7
evaluated here; (iv) must-fire: production with one residue (slice 0, lowest pole) scaled by 1 + 1e-4.
[model: Opus 5.5]"""
import os, sys, json, time
import numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
from numpy.polynomial.legendre import leggauss
mp.mp.dps = 40
W, P, Wbox, Ny = 4, 4, 4, 8; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2; tc = P - 1
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), tc, s_cut=3.0); N = S.N
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)

class MPSlice:
    def __init__(self, sl, p):
        idx = lambda x, t: x * Lt + t; m2 = 2 - 2 * mp.cos(2 * mp.pi * p / Ny)
        H0 = mp.zeros(N, N)
        for x in range(Lx):
            for t in range(Lt):
                i = idx(x, t); H0[i, i] = 4 + m2
                if x + 1 < Lx: j = idx(x + 1, t); H0[i, j] = H0[j, i] = -1
                if t + 1 < Lt: j = idx(x, t + 1); H0[i, j] = H0[j, i] = -1
        self.G0 = mp.inverse(H0); self.links = [(idx(x, tc), idx(x, tc + 1)) for x in range(x0, x0 + W)]   # own geometry
        self.W = len(self.links); sites = [s for lu in self.links for s in lu]
        self.A = mp.matrix([[self.G0[i, j] for j in sites] for i in range(N)]); self.M = mp.matrix([[self.G0[i, j] for j in sites] for i in sites])
        # run 2 (the Bridge's terms): OWN poles, root-finder-free. Sign-change scan of the O(1)-scaled
        # F(s) = z^W det(I + M C(z)), z = e^{-2 pi s}, at 50 digits on a 1/2000 grid over [0, s_cut]; each bracket refined by a
        # bracketing solver. Near-touch minima of |F| without a sign change (possible double/close pairs) are reported.
        with mp.workdps(50):
            F = lambda s: mp.re(mp.exp(-2 * mp.pi * s) ** self.W * mp.det(mp.eye(2 * self.W) + self.M * self.C(mp.exp(-2 * mp.pi * s))))
            ng = int(round(float(S.s_cut) * 2000)); grid = [mp.mpf(k) / 2000 for k in range(ng + 1)]; v = [F(x) for x in grid]
            self.s = [mp.findroot(F, (grid[i], grid[i + 1]), solver="anderson", tol=mp.mpf(10) ** -40)
                      for i in range(ng) if v[i] * v[i + 1] < 0]
            scale = max(abs(x) for x in v)
            self.touch = [float(grid[i]) for i in range(1, ng) if abs(v[i]) < abs(v[i - 1]) and abs(v[i]) < abs(v[i + 1])
                          and v[i - 1] * v[i + 1] > 0 and v[i] * v[i - 1] > 0 and abs(v[i]) < 1e-6 * scale]
        self.Rp = [self.resK(1j * sj) for sj in self.s]; self.Rm = [self.resK(-1j * sj) for sj in self.s]
    def C(self, z):
        Cm = mp.zeros(2 * self.W, 2 * self.W)
        for j in range(self.W): Cm[2 * j + 1, 2 * j] = -(z - 1); Cm[2 * j, 2 * j + 1] = -(1 / z - 1)
        return Cm
    def K(self, a):
        z = mp.exp(2j * mp.pi * a); Cm = self.C(z)
        if abs(z - 1) <= 0.5: return Cm * mp.inverse(mp.eye(2 * self.W) + self.M * Cm)
        Ci = mp.zeros(2 * self.W, 2 * self.W)
        for j in range(self.W): Ci[2 * j, 2 * j + 1] = 1 / Cm[2 * j + 1, 2 * j]; Ci[2 * j + 1, 2 * j] = 1 / Cm[2 * j, 2 * j + 1]
        return mp.inverse(Ci + self.M)
    def G(self, a):
        return self.G0 - self.A * self.K(a) * self.A.T
    def resK(self, a0, rad=mp.mpf("1e-12"), M=24):
        acc = mp.zeros(2 * self.W, 2 * self.W)
        for m in range(M):
            dz = rad * mp.exp(2j * mp.pi * m / M); acc += self.K(a0 + dz) * dz
        return -(self.A * (acc / M) * self.A.T)                          # full residue matrix Res G
log("building 40-digit slices (own poles by sign-change scan) ..."); MS = [MPSlice(S.sl[p], p) for p in range(Ny)]; log("done")
pole_ok = True; pole_rep = []
for p in range(Ny):
    prod = sorted(x for x in S.sl[p].s if x <= S.s_cut); own = sorted(float(x) for x in MS[p].s)
    same = len(prod) == len(own) and all(abs(a - b) <= 1e-6 for a, b in zip(prod, own))
    pole_ok &= same and not MS[p].touch
    pole_rep.append(dict(p=p, prod=prod, own=own, maxdiff=(max(abs(a - b) for a, b in zip(prod, own)) if len(prod) == len(own) and prod else None),
                         near_touch=MS[p].touch, match=bool(same)))
    log(f"slice {p}: production {[round(x, 10) for x in prod]}  referee {[round(x, 10) for x in own]}  "
        f"{'MATCH' if same else 'MISMATCH'}" + (f"  near-touch minima {MS[p].touch}" if MS[p].touch else ""))
log(f"pole census (s <= s_cut = {S.s_cut}): {'PASS' if pole_ok else 'FIRES N2-prime'}")
# census must-fire: slice 4 scanned to 4.0 vs production's list <= 4.0 (production missed s = 3.9476 there) -> must MISMATCH
with mp.workdps(50):
    m4 = MS[4]; F4 = lambda s: mp.re(mp.exp(-2 * mp.pi * s) ** m4.W * mp.det(mp.eye(2 * m4.W) + m4.M * m4.C(mp.exp(-2 * mp.pi * s))))
    g4 = [mp.mpf(k) / 2000 for k in range(8001)]; v4 = [F4(x) for x in g4]
    own4 = [float(mp.findroot(F4, (g4[i], g4[i + 1]), solver="anderson")) for i in range(8000) if v4[i] * v4[i + 1] < 0]
prod4 = sorted(x for x in S.sl[4].s if x <= 4.0); fired4 = not (len(prod4) == len(own4) and all(abs(a - b) <= 1e-6 for a, b in zip(prod4, own4)))
log(f"census must-fire (slice 4, s <= 4): production {[round(x, 6) for x in prod4]} referee {[round(x, 6) for x in own4]} -> {'FIRES' if fired4 else 'DOES NOT FIRE (control failed)'}")
def rel(Gd, Gm):
    Gm_np = np.array(Gm.tolist(), dtype=complex); return float(np.abs(Gd - Gm_np).max() / np.abs(Gm_np).max())
def hadamard(A, B): return mp.matrix([[A[i, j] * B[i, j] for j in range(N)] for i in range(N)])
res = {}
# production N1'' checks for this geometry
pr = S3.route_b(S, os.path.join(HERE, "exp081b_results", "referee_geom_ckpt.json"), cpts=12)
log("production N1'' checks:", pr["checks"], "s_max", pr["s_max"])
x, w = leggauss(24); u = 0.5 * (x + 1); wu = 0.5 * w
for s in (1.0, 2.0, 3.0):
    beta = mp.mpf("0.5") + 1j * mp.mpf(s); bd = 0.5 + 1j * s
    worst = 0.0                                                          # (a) tail ingredients
    for p in range(Ny):
        for sj_m in MS[p].s:
            sj_d = float(sj_m)
            for q in range(Ny):
                for sg in (-1, 1):
                    worst = max(worst, rel(S.sl[q].G(bd + sg * 1j * sj_d), MS[q].G(beta + sg * 1j * sj_m)))
    # (b) B~_0 via the inner formula at k=0 (pairs p, -p), npt=24
    Bm = mp.zeros(N, N)
    for ui, wi in zip(u, wu):
        for a1, a2, ww in ((ui * beta, (1 - ui) * beta, wi * beta), (beta + ui * (1 - beta), 1 - ui * (1 - beta), wi * (1 - beta))):
            for p in range(Ny):
                Bm += 2 * ww * hadamard(MS[p].G(a1), MS[(-p) % Ny].G(a2))
    for p in range(Ny):
        q = (-p) % Ny
        for j, sj in enumerate(MS[p].s):
            f = 2j * mp.pi / mp.expm1(2 * mp.pi * sj)
            Bm += 4 * f * (hadamard(MS[p].Rp[j], MS[q].G(beta - 1j * sj)) - hadamard(MS[p].Rm[j], MS[q].G(beta + 1j * sj)))
    Bm /= Ny
    Bd = S.inner(1.0, bd, npt=24)[0]
    ldm = mp.log(mp.det(Bm)); ldd = S3.logdet(Bd)
    rb = rel(Bd, Bm); rl = float(abs(mp.re(ldm) - ldd.real) / abs(mp.re(ldm)))
    imp = float(abs(mp.re(ldm) - ldd.real)) * np.pi / np.cosh(np.pi * s) ** 2
    sl0 = S.sl[0]; keep = sl0.Rp[0].copy(); sl0.Rp[0] = keep * (1 + 1e-4)          # must-fire: one perturbed residue
    ldf = S3.logdet(S.inner(1.0, bd, npt=24)[0]); sl0.Rp[0] = keep
    impf = float(abs(mp.re(ldm) - ldf.real)) * np.pi / np.cosh(np.pi * s) ** 2
    res[s] = dict(tail_ingredients=worst, B0=rb, logdet=rl, logdet_mp=float(mp.re(ldm)), impact=imp, mustfire_impact=impf)
    log(f"s={s}: (a) max rel err of tail ingredients G(beta -+ i s_j) = {worst:.1e};  (b) B~_0 max rel err {rb:.1e}, logdet rel err {rl:.1e}; "
        f"N2' impact {imp:.1e} [{'PASS' if imp <= 1e-7 else 'FAIL'}]; must-fire (residue x(1+1e-4)) impact {impf:.1e} [{'FIRES' if impf > 1e-7 else 'does not fire'}]")
smax = pr["s_max"]
ok = all((v["tail_ingredients"] <= 1e-8 and v["B0"] <= 1e-8 and v["logdet"] <= 1e-8) for s, v in res.items() if s <= smax)
log(f"N2 referee (orig rule): {'PASS' if ok else 'FAIL'} (criterion applied at s <= s_max = {smax:.2f})")
ok2 = pole_ok and all(v["impact"] <= 1e-7 for v in res.values())
log(f"N2' referee (impact rule + own-pole census, primary): {'PASS' if ok2 else 'FAIL -> VOID'}")
json.dump(dict(res={str(k): v for k, v in res.items()}, s_max=smax, checks=pr["checks"], pass_=bool(ok), pass_impact=bool(ok2), pole_census=pole_rep, pole_ok=bool(pole_ok), census_mustfire=bool(fired4)),
          open(os.path.join(HERE, "exp081b_referee_results.json"), "w"), indent=1)
