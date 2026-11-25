"""Fable side check (UNVERIFIED): the zero-mode piece  T_rho = Ny Sum_x rho(x) K'(x,x)  of  E = 1/2 t0 - 2 Sum_3D Lambda d,
computed WITHOUT the full t0: only the 3D diagonal of d_n B^(0) is needed, and that is a per-site scalar pole sum:
  gamma(a; x) = (1/Ny) sum_p G_p^(a)(x,x),   d = D[gamma],   d_n B^(0)_3D(x,x) = 2 D[gamma(a) gamma(-a)],
  K'(x,x) = D[gamma(a) gamma(-a)] - 2 gamma(0) d,   D[f] = sum over pole locations a0 = +-i s (s <= 3) of 2 pi i Res[f(a) kdn(a)]
(residues by small contours; kernels verbatim from sigma3d._kdn).  rho = B_{k=0}^{-1} 1.  Poles/G from sigma3d.Slice (no ExactSlice).
Known answers (full engine, kprime.py/krad.py): W4P4 Sum K' 0.009328, Sum rho K' 0.025052; W5P5 0.011295, 0.024873; W2P4 0.008946, 0.023022.
[model: Fable 5.2]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3
def run(W, P, M=8, rad=2e-5, s_cut=3.0):
    t = time.time(); Lx, Lt = 3 * P, 2 * P; x0 = P + (P - W) // 2; Ny = 4 * P; idx = lambda x, tt: x * Lt + tt; N = Lx * Lt
    sl = [S3.Slice(Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), list(range(x0, x0 + W)), P - 1, idx) for p in range(Ny // 2 + 1)]
    mult = np.array([1 if p in (0, Ny // 2) else 2 for p in range(Ny // 2 + 1)], float)
    for s in sl: s._dg = np.diag(s.G0).copy()
    g0 = sum(m * s._dg for m, s in zip(mult, sl)) / Ny
    def gam(a):
        out = np.zeros(N, dtype=complex)
        for m, s in zip(mult, sl): out += m * (s._dg - ((s.A @ s.K(a)) * s.A).sum(axis=1))
        return out / Ny
    ss = sorted(sj for s in sl for sj in s.s if sj <= s_cut); loc = []
    for v in ss:
        if not loc or v - loc[-1] > 1e-7: loc.append(v)
    gaps = np.diff(loc); assert len(gaps) == 0 or gaps.min() > 5 * rad, f"pole gap {gaps.min():.1e} too small for rad {rad}"
    th = 2 * np.pi * np.arange(M) / M; d = np.zeros(N, dtype=complex); dB = np.zeros(N, dtype=complex)
    for sj in loc:
        for a0, up in ((1j * sj, True), (-1j * sj, False)):
            for tt in th:
                dz = rad * np.exp(1j * tt); al = a0 + dz; ga = gam(al); gb = gam(-al); k = S3._kdn(al, up)
                d += (2j * np.pi) * ga * k * dz / M; dB += (2j * np.pi) * 2 * ga * gb * k * dz / M
    d = d.real; K0 = 0.5 * dB.real - 2 * g0 * d
    B0 = sum(m * (s.G0 * s.G0) for m, s in zip(mult, sl)) * 2.0 / Ny; rho = np.linalg.solve(B0, np.ones(N))
    xs, ts = np.divmod(np.arange(N), Lt); r = np.minimum(np.hypot(xs - (x0 - 0.5), ts - (P - 0.5)), np.hypot(xs - (x0 + W - 0.5), ts - (P - 0.5)))
    rec = dict(W=W, P=P, Ny=Ny, npole=len(loc), sumK=float(K0.sum()), sum_rhoK=float(np.sum(rho * K0)), T_rho=float(Ny * np.sum(rho * K0)),
               Sigma3D=float(2 * Ny * np.sum(rho * d)), sum_d=float(d.sum()), minK=float(K0.min()), rho_hot=float(rho[r < 0.8].mean()), K_hot=float(K0[r < 0.8].mean()),
               shells=[float(np.sum(rho[(r >= lo) & (r < hi)] * K0[(r >= lo) & (r < hi)])) for lo, hi in ((0, .8), (.8, 1.7), (1.7, 2.6), (2.6, 4), (4, 6), (6, 99))],
               imag=float(np.abs(dB.imag).max()), sec=time.time() - t)
    json.dump(rec, open(os.path.join(HERE, f"T_W{W}P{P}.json"), "w"), indent=1); return rec
if __name__ == "__main__":
    for a in sys.argv[1:]:
        v = [int(q) for q in a.split(",")]; W, P = v[0], v[1]; r = run(W, P, M=(v[2] if len(v) > 2 else 8))
        print(f"W{W:<2d}P{P:<2d} poles {r['npole']:3d}  Sum K' {r['sumK']:.6f}  Sum rho K' {r['sum_rhoK']:.6f}  T_rho {r['T_rho']:.6f}  Sigma3D {r['Sigma3D']:.6f}  "
              f"rho_hot {r['rho_hot']:.4f} K_hot {r['K_hot']:.6f}  shells {np.round(r['shells'],5)}  ({r['sec']:.0f}s)", flush=True)
