"""EXP-076 E3': T36's master-formula sector object on Cuspis's pure-gauge 1D toy (exact answer: 0 for every beta).
Toy: N=240, G1 = (-Lap + 0.09)^{-1}, B1 = 2 G1 o G1, twist = step phase on sites >= N/2: G^(a) = U_a G1 U_a^{-1},
U_a = diag(1.., e^{2 pi i a}..). Delta G^(a) = G^(a) - G1 (cut gauge). Honest sector bubble at integer n:
B_n^(q) = (2/n) sum_k G^(k/n) o G^((q-k)/n) = U_{q/n} B1 U_{q/n}^{-1}  ->  log det B^(q) - log det B1 = 0.
T36 (eq. 2-3): Btilde^(beta) = B1 + K1^(beta); entries of Delta G^(a) are (e^{+-2 pi i a} - 1) G1_ij on straddling (i,j), 0 same
side, so they are entire 1-periodic in a and the AP tails vanish identically; K1 = 2 Int_0^1 da DeltaG^(a) o DeltaG^({beta-a}).
[model: Opus 5.5]"""
import numpy as np
N, m2 = 240, 0.09
L = np.diag(np.full(N, 2 + m2)) - np.eye(N, k=1) - np.eye(N, k=-1)
G1 = np.linalg.inv(L); B1 = 2 * G1 * G1
side = (np.arange(N) >= N // 2).astype(float)
D = side[:, None] - side[None, :]          # +1: i up, j down; -1: i down, j up; 0 same side
def dG(a): return (np.exp(2j * np.pi * a * D) - 1) * G1
def K1(beta, na=2000):
    al = (np.arange(na) + 0.5) / na; K = np.zeros((N, N), complex)
    for a in al:
        K += dG(a) * dG((beta - a) % 1.0)
    return 2 * K / na
def honest_Bn(n, q):
    return (2.0 / n) * sum(G1 * (np.exp(2j*np.pi*(k/n)*D)*G1) * 0 + (np.exp(2j*np.pi*(k/n)*D)*G1) * (np.exp(2j*np.pi*(((q-k)/n) % 1.0)*D)*G1) for k in range(n))
s1, ld1 = np.linalg.slogdet(B1)
for n, q in ((2, 1), (3, 1), (4, 3)):
    Bn = honest_Bn(n, q); s, ld = np.linalg.slogdet(Bn)
    print(f"honest n={n} q={q}: logdet B^(q) - logdet B1 = {ld - ld1 + np.log(s/s1):+.2e}  (exact 0 mod 2 pi i)")
for beta in (0.0, 0.25, 0.5, 0.75):
    Bt = B1 + K1(beta); s, ld = np.linalg.slogdet(Bt)
    val = ld - ld1 + np.log(s / s1)
    print(f"T36 Btilde, beta={beta}: logdet(I + B1^-1 K1) = {val:+.6f}   [exact answer 0]  max|K1 - (U B1 U^-1 - B1)| = "
          f"{np.abs(K1(beta) - (np.exp(2j*np.pi*beta*D)*B1 - B1)).max():.3e}")
