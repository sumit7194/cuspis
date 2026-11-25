"""Fable side check (UNVERIFIED): census of near-coincident pole pairs between DIFFERENT y-slices, the configurations that
inner_beta0 treats as two separate simple poles (merge only below 1e-2*rad = 1e-7).  Poles from sigma3d.Slice._poles (QEP),
no production object touched.  Reports, per geometry, how many cross-slice pairs (s_a of slice p, s_b of slice q, s <= 3)
lie within delta, and a proxy  sum_pairs w(s)/delta^2  with the n-derivative weight w(s) = 2 pi s e^{-2 pi s}/(1-e^{-2 pi s})^2.
[model: Fable 5.2]"""
import sys, os, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3
def census(W, P):
    Wb = P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P; idx = lambda x, t: x * Lt + t
    sl = {p: S3.Slice(Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), list(range(x0, x0 + W)), P - 1, idx) for p in range(Ny // 2 + 1)}
    s_of = lambda p: np.array([s for s in sl[p if p <= Ny // 2 else Ny - p].s if s <= 3.0])
    w = lambda s: 2 * np.pi * s * np.exp(-2 * np.pi * s) / (1 - np.exp(-2 * np.pi * s)) ** 2
    cnt = {d: 0 for d in (1e-3, 1e-4, 1e-5, 1e-6)}; proxy = 0.0; dmin = 1.0; npairs = 0; worst = []
    for p in range(Ny):
        for q in range(Ny):
            pp, qq = min(p, Ny - p), min(q, Ny - q)
            if pp == qq: continue                       # identical slices: exact coincidence, merged and done by contour
            a, b = s_of(p), s_of(q)
            if len(a) == 0 or len(b) == 0: continue
            D = np.abs(a[:, None] - b[None, :]); npairs += D.size
            for d in cnt: cnt[d] += int((D < d).sum())
            m = D < 1e-3
            if m.any():
                ss = np.broadcast_to(a[:, None], D.shape)[m]; proxy += float(np.sum(w(ss) / D[m] ** 2))
                i = np.argmin(np.where(m, D, 1)); ia, ib = np.unravel_index(i, D.shape)
                worst.append((float(D[ia, ib]), float(a[ia]), pp, qq))
            dmin = min(dmin, float(D.min()))
    worst = sorted(set(worst))[:3]
    npoles = sum(len(s_of(p)) for p in range(Ny))
    return dict(W=W, P=P, npoles_le3=npoles, npairs=npairs, cnt=cnt, dmin=dmin, proxy=proxy, worst=worst)
if __name__ == "__main__":
    for W, P in [(2, 4), (4, 4), (5, 5), (3, 6), (6, 6), (4, 8), (8, 8), (5, 10), (10, 10), (6, 12), (12, 12)]:
        t = time.time(); r = census(W, P)
        print(f"W{W:<2d}P{P:<2d} poles(s<=3) {r['npoles_le3']:5d} cross-slice pairs {r['npairs']:8d}  within 1e-3/1e-4/1e-5/1e-6: "
              f"{r['cnt'][1e-3]:5d} {r['cnt'][1e-4]:4d} {r['cnt'][1e-5]:3d} {r['cnt'][1e-6]:3d}  min sep {r['dmin']:.2e}  proxy sum w/d^2 {r['proxy']:.3e}  "
              f"closest (d, s, p, q): {[(f'{d:.1e}', round(s,3), p, q) for d, s, p, q in r['worst']]}  ({time.time()-t:.0f}s)", flush=True)
