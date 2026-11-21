"""EXP-081a diagnosis: numerical reliability of the edge g(s) = sum_k [logdet B~_k(1/2+is) - logdet B1_k] vs s, at W=2 r=3
(edge cut, Ny=24). Variants: G via Woodbury vs direct dense inverse; logdet plain vs after scipy matrix_balance (diagonal
similarity, det-preserving). Also the strip for contrast. [model: Opus 5.5]"""
import numpy as np, scipy.linalg as sla, sigma3d as S3
def build(conf, direct):
    P, W = 6, 2; Lx, Lt = W + 2 * P, 2 * P; cut = list(range(P, Lx)) if conf == "edge" else list(range(P, P + W))
    S = S3.Strip3D(Lx, Lt, 4 * P, cut, P - 1)
    if direct:
        for sl in S.sl:
            H0 = np.linalg.inv(sl.G0); links = sl.links
            def Gd(a, H0=H0, links=links):
                z = np.exp(2j * np.pi * a); H = H0.astype(complex)
                for (l, u) in links: H[u, l] += -(z - 1); H[l, u] += -(1 / z - 1)
                return np.linalg.inv(H)
            sl.G = Gd
    return S
def ld_bal(M):
    Mb, _ = sla.matrix_balance(M, permute=False); s, ld = np.linalg.slogdet(Mb); return ld
for conf in ("strip", "edge"):
    Sw, Sd = build(conf, False), build(conf, True); B1 = Sw.B1(); ld1 = [np.linalg.slogdet(B1[k])[1] for k in range(Sw.Ny)]
    print(f"--- {conf} (W=2 r=3) ---", flush=True)
    for s in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
        b = 0.5 + 1j * s; Bw = Sw.inner(1.0, b); Bd = Sd.inner(1.0, b)
        gw = sum(np.linalg.slogdet(Bw[k])[1] - ld1[k] for k in range(Sw.Ny)); gwb = sum(ld_bal(Bw[k]) - ld1[k] for k in range(Sw.Ny))
        gd = sum(np.linalg.slogdet(Bd[k])[1] - ld1[k] for k in range(Sw.Ny)); gdb = sum(ld_bal(Bd[k]) - ld1[k] for k in range(Sw.Ny))
        print(f"s={s}: g woodbury {gw:+.6f} | woodbury+bal {gwb:+.6f} | direct {gd:+.6f} | direct+bal {gdb:+.6f} | max|B| {np.abs(Bw).max():.1e}", flush=True)
