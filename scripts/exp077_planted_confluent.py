"""EXP-077 planted control, extended (Bridge's request, after its retraction): a CONFLUENT remainder R(n) = (c + d n) a^n,
not completely monotone, with a = e^{-2 pi s1} = 1/86.02388 (the P4' lattice pole), plus a second base a2 = 1/302.7581.
Same pipeline as exp077_newton_hp (Levin-u on Newton derivative partial sums, K=40,59; raw sums to K). Known exact Q'(1).
Shows whether the earlier '-1.4207, stable to 2e-8, all terms negative' could be a false convergence. [model: Opus 5.5]"""
import mpmath as mp
mp.mp.dps = 160
a1, a2 = 1 / mp.mpf("86.02388"), 1 / mp.mpf("302.7581")
def run(name, R, Kmax=300, B=mp.mpf("-0.29855273")):
    Qs = [B * n + R(n) - (B + R(1)) for n in range(1, Kmax + 2)]
    D = list(Qs); a = [Qs[0]]
    for k in range(1, Kmax + 1):
        D = [D[i + 1] - D[i] for i in range(len(D) - 1)]; a.append(D[0])
    t = [(-1) ** (k + 1) * a[k] / k for k in range(1, Kmax + 1)]
    S = [mp.fsum(t[:j]) for j in range(1, Kmax + 1)]
    exact = B + mp.diff(R, 1)
    lev = {K: mp.levin(method="levin", variant="u").update_psum(S[:K])[0] for K in (40, 59)}
    flip = next((k + 1 for k, x in enumerate(t) if x > 0), None)
    print(f"{name}: exact {mp.nstr(exact, 10)} | Levin K=40 {mp.nstr(lev[40], 10)}, K=59 {mp.nstr(lev[59], 10)} | raw S59 {mp.nstr(S[58], 8)}, "
          f"min over k {mp.nstr(min(S), 8)} at k={S.index(min(S))+1}, S150 {mp.nstr(S[149], 10)} S200 {mp.nstr(S[199], 10)} S300 {mp.nstr(S[-1], 10)} | first positive term at k={flip}", flush=True)
run("confluent (c + d n) a1^n", lambda n: (mp.mpf("0.05") + mp.mpf("20") * n) * a1 ** n)
run("confluent + a2 base     ", lambda n: (mp.mpf("0.05") + mp.mpf("20") * n) * a1 ** n + (mp.mpf("1") + mp.mpf("10") * n) * a2 ** n)
run("pure n a1^n             ", lambda n: mp.mpf("25.7") * n * a1 ** n)
