"""EXP-078 (pre-check): as exp077_newton_hp.py, also storing the q=0 sector h0(n) = logdet B_n^(0) - logdet B_1, to split Q'(1) into q=0 and q!=0 parts by the Newton route (T40 claims Q_0'(1) = -1.288192677980, Q_{!=0}'(1) = -0.098679256287). [model: Opus 5.5]
(log det B_n = sum_q log det B_n^(q/n), B_n^(q/n) = (2/n) sum_k G^(k/n) o G^((q-k)/n), G^(a) = H(a)^-1 with the twist phase
e^{2 pi i a} on the cut links), in mpmath at 45 dps, n = 1..NMAX. Then the Newton forward-difference series for Q'(1)
with Wynn acceleration. No Abel-Plana formula of T40 is used. Cross-check: Q(2..4) vs the direct double-precision values.
[model: Opus 5.5]"""
import sys, json, time, mpmath as mp
mp.mp.dps = 45
Lx, Lt, m2, tcut, cutx = 6, 4, mp.mpf("0.5"), 1, (2, 3)
N = Lx * Lt
idx = lambda x, t: t * Lx + x
def H(alpha):
    z = mp.exp(2j * mp.pi * alpha); M = mp.zeros(N, N)
    for x in range(Lx):
        for t in range(Lt):
            i = idx(x, t); M[i, i] = 4 + m2
            if x + 1 < Lx:
                j = idx(x + 1, t); M[i, j] = -1; M[j, i] = -1
            if t + 1 < Lt:
                j = idx(x, t + 1)
                if t == tcut and x in cutx:
                    M[j, i] = -z; M[i, j] = -1 / z      # going up (t -> t+1) carries z
                else:
                    M[i, j] = -1; M[j, i] = -1
    return M
def logdet(M):
    return mp.log(mp.det(M))
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
G1 = mp.inverse(H(0)); B1 = 2 * G1.apply(lambda v: v) ; B1 = mp.matrix([[2 * G1[i, j] ** 2 for j in range(N)] for i in range(N)])
ld1 = logdet(B1)
out = {}; out0 = {}; t0 = time.time()
for n in range(1, NMAX + 1):
    Gs = [mp.inverse(H(mp.mpf(k) / n)) for k in range(n)]
    tot = mp.mpf(0)
    for q in range(n):
        Bq = mp.zeros(N, N)
        for k in range(n):
            A = Gs[k]; Bm = Gs[(q - k) % n]
            for i in range(N):
                for j in range(N):
                    Bq[i, j] += A[i, j] * Bm[i, j]
        Bq *= mp.mpf(2) / n
        lq = logdet(Bq); tot += lq
        if q == 0: h0 = lq - ld1
    Qn = tot - n * ld1
    out[n] = mp.nstr(Qn.real, 40); out0[n] = mp.nstr(h0.real, 40); print(f"n={n} Q={mp.nstr(Qn.real, 25)} Im={mp.nstr(Qn.imag, 3)} [{time.time()-t0:.0f}s]", flush=True)
    json.dump({"Q": out, "h0": out0}, open("exp078_sectors_hp.json", "w"), indent=0)
