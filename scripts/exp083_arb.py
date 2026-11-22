"""EXP-083 R2 (+A1 5d5c87f): honest integer-n Q(n) in Arb (python-flint 0.9.0, 400 bits) via the exact replica-sector decomposition.
G_p(q/n) = direct Arb inverse of the single-sheet twisted operator (H[u,l] = -z, H[l,u] = -1/z, z = e^{2 pi i q/n}; diag 4 + m2_p + sigma).
Sector sums by separable 2D cyclic DFT over (p, q) (checked against the direct double sum). Arm (b): float64 sector saddle refined by
quasi-Newton with an Arb residual. Usage: python exp083_arb.py W P nmax arm out.json   [model: Opus 5.5]"""
import sys, json, time, numpy as np
from flint import acb_mat, acb, arb, arb_mat, ctx
from exp083_honest import Geom
import exp083_sector as SEC
ctx.prec = 400
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)

class ArbGeom:
    def __init__(self, g):
        self.g = g; self.N, self.Ny = g.N, g.Ny; self.nz = list(zip(*np.nonzero(g.A)))
    def m2(self, p): return 2 - 2 * arb.cos_pi(arb(2 * p) / self.Ny)
    def H(self, p, q, n, sigma=None):
        N = self.N; rows = [[acb(0)] * N for _ in range(N)]; m2 = self.m2(p)
        for i in range(N): rows[i][i] = acb(4) + m2 + (sigma[i] if sigma is not None else 0)
        for i, j in self.nz: rows[i][j] = acb(-1)
        z = acb.exp_pi_i(acb(2 * q) / n)
        for (l, u) in self.g.links: rows[u][l] = -z; rows[l][u] = -1 / z
        return acb_mat(rows)
    def Gs(self, n, sigma=None):
        U = {p: [self.H(p, q, n, sigma).inv() for q in range(n)] for p in range(self.Ny // 2 + 1)}
        return [U[p if p <= self.Ny // 2 else self.Ny - p] for p in range(self.Ny)]
    @staticmethod
    def had(A, B):
        r, c = A.nrows(), A.ncols(); return acb_mat([[A[i, j] * B[i, j] for j in range(c)] for i in range(r)])
    def logdet_sectors(self, A, n, direct=False):
        """A[p][q] (p over Ny, q over n). Returns sum_{Q,k} log det B^(Q,k) and the max ball radius of the log dets."""
        Ny, N = self.Ny, self.N; scale = acb(2) / (n * Ny); tot = arb(0); rmax = 0.0
        if direct:
            Bs = {(k, Q): sum((self.had(A[p][q], A[(k - p) % Ny][(Q - q) % n]) for p in range(Ny) for q in range(n)), acb_mat(N, N)) for k in range(Ny) for Q in range(n)}
        else:
            wn = [acb.exp_pi_i(acb(2 * b) / n) for b in range(n)]; wy = [acb.exp_pi_i(acb(2 * a) / Ny) for a in range(Ny)]
            A1 = [[sum((A[p][q] * wn[(b * q) % n] for q in range(n)), acb_mat(N, N)) for b in range(n)] for p in range(Ny)]
            Ah = [[sum((A1[p][b] * wy[(a * p) % Ny] for p in range(Ny)), acb_mat(N, N)) for b in range(n)] for a in range(Ny)]
            C = [[self.had(Ah[a][b], Ah[a][b]) for b in range(n)] for a in range(Ny)]
            C1 = [[sum((C[a][b] * wn[(-b * Q) % n] for b in range(n)), acb_mat(N, N)) for Q in range(n)] for a in range(Ny)]
            Bs = {(k, Q): sum((C1[a][Q] * wy[(-a * k) % Ny] for a in range(Ny)), acb_mat(N, N)) * (acb(1) / (n * Ny)) for k in range(Ny) for Q in range(n)}
        for key, B in Bs.items():
            ld = (B * scale).det().log(); tot += ld.real; rmax = max(rmax, float(ld.real.rad()))
        return tot, rmax
    def saddle(self, n, tol=arb("1e-100"), itmax=12):
        g = self.g; N, Ny = self.N, self.Ny
        s0, _, _ = SEC.sector_saddle(g, n); G1 = self.Gs(1)
        target = [sum((G1[p][0][x, x] for p in range(Ny)), acb(0)) / Ny for x in range(N)]
        Gf = SEC.sector_G(g, n, s0); getf = lambda p: Gf[p if p <= Ny // 2 else Ny - p]; J = np.zeros((N, N))
        for p in range(Ny):
            for d in range(n):
                Gd = sum(np.exp(-2j * np.pi * q * d / n) * getf(p)[q] for q in range(n)) / n; J -= np.real(Gd) ** 2
        Jinv = np.linalg.inv(J / Ny); sig = [arb(float(v)) for v in s0]
        for it in range(itmax):
            G = self.Gs(n, sig); F = [(sum((G[p][q][x, x] for p in range(Ny) for q in range(n)), acb(0)) / (n * Ny) - target[x]).real for x in range(N)]
            fmax = max(abs(float(f.mid())) + float(f.rad()) for f in F)
            if fmax < float(tol): return sig, G, it, fmax
            sig = [sig[x] - sum((arb(float(Jinv[x, y])) * F[y] for y in range(N)), arb(0)) for x in range(N)]
        raise RuntimeError(f"Arb saddle did not converge (n={n}, |F|={fmax:.1e})")

if __name__ == "__main__":
    W, P, nmax, arm, outf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    g = Geom(W, P); ag = ArbGeom(g); out = {"W": W, "P": P, "arm": arm, "prec": ctx.prec, "Q": {}, "rad": {}}
    A1 = ag.Gs(1); ld1, r1 = ag.logdet_sectors([[A1[p][0]] for p in range(g.Ny)], 1)
    if P == 2 and arm == "a":                                   # DFT identity check vs direct double sum (A1 registration)
        for n in (2, 3):
            A = ag.Gs(n); a_, _ = ag.logdet_sectors(A, n); b_, _ = ag.logdet_sectors(A, n, direct=True)
            log(f"DFT check n={n}: |DFT - direct| = {float(abs(a_ - b_).mid()):.1e} (+rad {float(abs(a_ - b_).rad()):.1e})")
            if float(abs(a_ - b_).mid()) > 1e-100: raise SystemExit("DFT identity check FAILED -> STOP")
    for n in range(2, nmax + 1):
        if arm == "b": sig, A, it, fm = ag.saddle(n)
        else: A = ag.Gs(n)
        ldn, rn = ag.logdet_sectors(A, n); Qn = ldn - n * ld1
        out["Q"][n] = Qn.mid().str(110, radius=False); out["rad"][n] = float(Qn.rad())
        if arm == "b": out.setdefault("sigma", {})[n] = [x.mid().str(40, radius=False) for x in sig]   # stored saddle (2026-11-22, C2 W4P4 diagnosis)
        if out["rad"][n] > 1e-60: raise SystemExit(f"ball radius {out['rad'][n]:.1e} > 1e-60 at n={n} -> STOP")
        log(f"W{W}P{P} arm {arm} n={n}: Q = {Qn.mid().str(25, radius=False)}  (rad {out['rad'][n]:.1e})" + (f" saddle it {it} |F| {fm:.1e}" if arm == "b" else ""))
        json.dump(out, open(outf, "w"), indent=1)
