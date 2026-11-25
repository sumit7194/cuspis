"""Fable side check (UNVERIFIED): PREDICT the error of inner_beta0(dn=True)-based t0 caused by near-degenerate intra-slice pole
doublets, from the code's own logic, without running t0.  Two mechanisms, for a doublet (s1 < s2, gap g) of slice u, contour radius
rad (production 1e-5), merge tolerance 1e-2*rad:
  A  (1e-2*rad <= g < rad): in the two-tag branch (partner slice q = u or Ny-u, i.e. k = 2u, -2u, 0) each member's contour
     encloses BOTH members, and each member has its own entry -> the doublet's two-tag contribution is counted TWICE.
     extra dB0_k = X_u/Ny per such (p, q),  X_u = sum_{+-} 2 pi i Res_cluster[ 2 G_u(al) o G_u(-al) kdn(al) ].
  B  (g < 1e-2*rad): the two members are merged into ONE entry; in the single-tag branch (q not in {u, Ny-u}) only the nearest
     pole's residue (s1) is used -> the s2 member is DROPPED for every such q, in both tags.
delta_t0 = t0_code - t0_true = sum_k Tr(B_k^-1 delta dB0_k).  Poles/G/residues from sigma3d.Slice.  [model: Fable 5.2]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3
def predict(W, P, Wb=None, Ny=None, rad=1e-5, M=32, s_cut=3.0, verbose=True):
    t = time.time(); Wb = P if Wb is None else Wb; Ny = 4 * P if Ny is None else Ny
    Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; idx = lambda x, tt: x * Lt + tt; N = Lx * Lt; H = Ny // 2
    sl = [S3.Slice(Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), list(range(x0, x0 + W)), P - 1, idx) for p in range(H + 1)]
    U = lambda p: min(p % Ny, Ny - p % Ny)
    Binv = {}
    def Bi(k):
        k = U(k)
        if k not in Binv:
            B = np.zeros((N, N))
            for p in range(Ny): B += sl[U(p)].G0 * sl[U(k - p)].G0
            Binv[k] = np.linalg.inv(B * 2.0 / Ny)
        return Binv[k]
    th = 2 * np.pi * np.arange(M) / M; dA = 0.0; dB = 0.0; rows = []
    for u in range(H + 1):
        s = np.array([v for v in sl[u].s if v <= s_cut]); order = np.argsort(s)
        full = list(sl[u].s)
        for i in range(len(s) - 1):
            a, b = order[i], order[i + 1]; g = s[b] - s[a]
            if g >= rad: continue
            selfm = (u == 0 or u == H)
            if g >= 1e-2 * rad:                                         # ---- mechanism A
                X = np.zeros((N, N), dtype=complex); sc = 0.5 * (s[a] + s[b]); rc = 0.5 * g + 0.5 * rad
                for a0, up in ((1j * sc, True), (-1j * sc, False)):
                    for tt in th:
                        dz = rc * np.exp(1j * tt); al = a0 + dz
                        X += (2j * np.pi) * 2 * sl[u].G(al) * sl[u].G(-al) * S3._kdn(al, up) * dz / M
                X = X.real
                c0 = np.sum(Bi(0).T * X) / Ny; c2 = np.sum(Bi(2 * u).T * X) / Ny
                contrib = c0 if selfm else (2 * c0 + 2 * c2); dA += contrib; rows.append(("A", u, float(g), float(s[a]), float(contrib)))
            else:                                                        # ---- mechanism B: member s2 dropped in single-tag pairs
                j2 = full.index(s[b]); tot = 0.0
                for a0, up, RK in ((1j * s[b], True, sl[u].Rp[j2]), (-1j * s[b], False, sl[u].Rm[j2])):
                    R = sl[u].Rfull(RK); kk = S3._kdn(a0, up)
                    for q in range(Ny):
                        if U(q) == u: continue
                        tot += ((2j * np.pi) * 2 * kk * np.sum(Bi(u + q).T * (R * sl[U(q)].G(-a0)))).real
                contrib = -(1 if selfm else 2) * 2 * tot / Ny; dB += contrib; rows.append(("B", u, float(g), float(s[b]), float(contrib)))
    if verbose:
        for r in rows: print(f"    {r[0]}  slice u={r[1]:2d}  gap {r[2]:.1e}  s {r[3]:.4f}  delta_t0 {r[4]:+.6f}", flush=True)
    rec = dict(W=W, P=P, Wb=Wb, Ny=Ny, rad=rad, dA=float(dA), dB=float(dB), d_t0=float(dA + dB), rows=rows, sec=time.time() - t)
    return rec
if __name__ == "__main__":
    a = sys.argv[1:]; W, P, Wb, Ny = [int(v) for v in a[:4]]
    for rad in [float(v) for v in a[4:]] or [1e-5]:
        r = predict(W, P, Wb, Ny, rad=rad)
        print(f"W{W} P{P} Wb{Wb} Ny{Ny} rad {rad:.0e}: predicted delta_t0 (code - true) = {r['d_t0']:+.6f}   [A {r['dA']:+.6f}, B {r['dB']:+.6f}]  ({r['sec']:.0f}s)", flush=True)
        json.dump(r, open(os.path.join(HERE, f"ART_W{W}P{P}b{Wb}Ny{Ny}_rad{rad:.0e}.json"), "w"), indent=1)
