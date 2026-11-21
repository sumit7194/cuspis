"""EXP-078 route (a): raw Newton derivative series to k = 360 on 120-digit honest Q(n) (n <= 90, linear extension beyond;
R(90) ~ 90 a1^90 ~ 1e-172 below precision). Rounding grows like 2^k * 1e-120, fine to k ~ 370. Also Q(1.5). Shanks on
post-crossing windows. [model: Opus 5.5]"""
import json, mpmath as mp
mp.mp.dps = 120
d = json.load(open("exp078_sectors_hp120.json")); NMAX = max(int(k) for k in d["Q"])
Q = [mp.mpf(d["Q"][str(n)]) for n in range(1, NMAX + 1)]
KMAX = 360; slope = Q[-1] - Q[-2]
ext = Q + [Q[-1] + slope * j for j in range(1, KMAX + 2 - NMAX)]
D = list(ext); a = [ext[0]]
for k in range(1, KMAX + 1):
    D = [D[i + 1] - D[i] for i in range(len(D) - 1)]; a.append(D[0])
S = []; S15 = []; s = mp.mpf(0); s15 = a[0]
for k in range(1, KMAX + 1):
    s += (-1) ** (k + 1) * a[k] / k; S.append(s); s15 += mp.binomial(mp.mpf("0.5"), k) * a[k]; S15.append(s15)
for k in (59, 85, 109, 110, 120, 160, 200, 250, 300, 303, 330, 360):
    print(f"k={k:3d}: term {mp.nstr((-1)**(k+1)*a[k]/k, 4):>11}  Q'(1) partial {mp.nstr(S[k-1], 12)}   Q(1.5) partial {mp.nstr(S15[k-1], 12)}")
for lo, hi in ((160, 200), (200, 260), (260, 320), (300, 360)):
    print(f"Shanks[{lo}:{hi}]: Q'(1) {mp.nstr(mp.shanks(S[lo:hi])[-1][-1], 12)}   Q(1.5) {mp.nstr(mp.shanks(S15[lo:hi])[-1][-1], 12)}")
print("T40 Q_cont: Q'(1) = -1.386871934267, Q(1.5) = -0.403056284")
