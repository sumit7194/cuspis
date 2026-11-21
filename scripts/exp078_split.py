"""EXP-078: Newton-route split of Q'(1) on P4' into the q=0 sector h0 and the q!=0 remainder, from 45-digit honest data
(exp078_sectors_hp.json). Two estimators per piece: Levin-u on Newton partial sums (K=40,59) and raw Newton summation with
linear extension of the data beyond n=60 (the Bridge's route; valid where the piece is linear to precision). [model: Opus 5.5]"""
import json, mpmath as mp
mp.mp.dps = 45
d = json.load(open("exp078_sectors_hp.json"))
Q = [mp.mpf(d["Q"][str(n)]) for n in range(1, 61)]; H0 = [mp.mpf(d["h0"][str(n)]) for n in range(1, 61)]
QN = [q - h for q, h in zip(Q, H0)]
def coeffs(v):
    D = list(v); a = [v[0]]
    for k in range(1, len(v)):
        D = [D[i + 1] - D[i] for i in range(len(D) - 1)]; a.append(D[0])
    return a
def levin(v, K):
    a = coeffs(v); t = [(-1) ** (k + 1) * a[k] / k for k in range(1, K + 1)]
    S = [mp.fsum(t[:j]) for j in range(1, K + 1)]
    return mp.levin(method="levin", variant="u").update_psum(S)[0], all(x < 0 for x in t) or all(x > 0 for x in t)
def raw_extended(v, Kmax=115):
    slope = v[-1] - v[-2]; ext = list(v) + [v[-1] + slope * j for j in range(1, Kmax - len(v) + 2)]
    a = coeffs(ext); return mp.fsum((-1) ** (k + 1) * a[k] / k for k in range(1, Kmax + 1)), abs(ext[40] - ext[39] - slope)
for name, v, claim in (("total Q", Q, "-1.386871934267"), ("q=0 h0", H0, "-1.288192677980"), ("q!=0 rest", QN, "-0.098679256287")):
    l40, s40 = levin(v, 40); l59, s59 = levin(v, 59); r, lin = raw_extended(v)
    print(f"{name:10s}: Levin K=40 {mp.nstr(l40, 12)}  K=59 {mp.nstr(l59, 12)}  raw-extended k<=115 {mp.nstr(r, 12)}  "
          f"(linearity residual at n=40: {mp.nstr(lin, 3)}; terms one-signed: {s59})   T40 claims {claim}", flush=True)
