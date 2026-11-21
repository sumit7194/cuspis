"""EXP-081b N2 extended-precision referee (registered 0ab92d4): W=4 strip in the P=4 pair box (12x8), Ny=8, s in {1,2,3}.
Same formulas at 40 digits (mpmath): per-slice G0 by mp inverse, Woodbury K = (C^{-1}+M)^{-1} away from z=1, poles refined by
mp.findroot on det(I + M C(z)), residues by 40-digit contours. Compares the double-precision production on
 (a) every tail ingredient G_q(beta -+ i s_j) (all slices q, all poles s_j of all slices) and
 (b) the k=0 bubble B~_0(beta) (npt=24) and its logdet,
and the production N1'' checks for this geometry. Pass: relative agreement <= 1e-8 wherever N1'' calls production reliable.
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
        self.G0 = mp.inverse(H0); self.links = sl.links; self.W = len(self.links)
        sites = [s for lu in self.links for s in lu]
        self.A = mp.matrix([[self.G0[i, j] for j in sites] for i in range(N)]); self.M = mp.matrix([[self.G0[i, j] for j in sites] for i in sites])
        self.s = []
        for sj in sl.s:                                                    # refine poles: det(I + M C(z)) = 0, z = e^{-2 pi s}
            f = lambda z: mp.det(mp.eye(2 * self.W) + self.M * self.C(z))
            z = mp.findroot(f, mp.mpf(np.exp(-2 * np.pi * sj)), tol=mp.mpf(10) ** -35)
            self.s.append(-mp.log(mp.re(z)) / (2 * mp.pi))
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
log("building 40-digit slices ..."); MS = [MPSlice(S.sl[p], p) for p in range(Ny)]; log("done")
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
        for sj_d, sj_m in zip(S.sl[p].s, MS[p].s):
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
    res[s] = dict(tail_ingredients=worst, B0=rb, logdet=rl)
    log(f"s={s}: (a) max rel err of tail ingredients G(beta -+ i s_j) = {worst:.1e};  (b) B~_0 max rel err {rb:.1e}, logdet rel err {rl:.1e}")
smax = pr["s_max"]
ok = all((v["tail_ingredients"] <= 1e-8 and v["B0"] <= 1e-8 and v["logdet"] <= 1e-8) for s, v in res.items() if s <= smax)
log(f"N2 referee: {'PASS' if ok else 'FAIL'} (criterion applied at s <= s_max = {smax:.2f})")
json.dump(dict(res={str(k): v for k, v in res.items()}, s_max=smax, checks=pr["checks"], pass_=bool(ok)),
          open(os.path.join(HERE, "exp081b_referee_results.json"), "w"), indent=1)
