"""EXP-054 (pre-registered in report.md, 5deecb1): Lemma U gap (b). Complex 2D lattice scalar with unitary twist
e^{2 pi i alpha} on links crossing a cut (A[above,below] = -e^{2 pi i alpha}, A[below,above] = -e^{-2 pi i alpha}),
Dirichlet box. D(alpha) = G_int(x,x) - G_half(x,x) (second-edge effect near edge 1); S(alpha) = G_half - G_0.
[model: Opus 5.5]   Usage: python exp054_twist_tip.py tier1 | run"""
import sys, math, time, json, os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from scipy.special import k0

D0 = os.path.dirname(os.path.abspath(__file__))
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def G_xx(m, box, alpha, cut, j0, w, r):
    L = box; n = L * L
    i0 = L // 2 - 1
    I, J = np.meshgrid(np.arange(L), np.arange(L), indexing="ij"); I = I.ravel(); J = J.ravel(); S = I * L + J
    rows, cols, vals = [], [], []
    msk = J < L - 1                                                     # horizontal links, never cut
    rows += [S[msk], S[msk] + 1]; cols += [S[msk] + 1, S[msk]]; vals += [-np.ones(msk.sum(), complex)] * 2
    msk = I < L - 1                                                     # vertical links (i, i+1)
    up = S[msk] + L; dn = S[msk]
    jend = j0 + w if cut == "int" else L
    c = (I[msk] == i0) & (J[msk] >= j0) & (J[msk] < jend)
    ph = np.exp(2j * math.pi * alpha)
    rows += [up, dn]; cols += [dn, up]; vals += [-np.where(c, ph, 1.0 + 0j), -np.where(c, np.conj(ph), 1.0 + 0j)]
    A = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)) \
        + sp.diags(np.full(n, 4.0 + m * m + 0j))
    x = i0 * L + (j0 - r)
    b = np.zeros(n, complex); b[x] = 1.0
    g = splu(A.tocsc()).solve(b)[x]
    return g

def setup(box, w):
    return box // 2 - w // 2

def slope(a1, v1, a2, v2): return math.log(abs(v2) / abs(v1)) / math.log(a2 / a1)

def tier1():
    t0 = time.time(); box, w, m, r = 128, 32, 1 / 32, 4; j0 = setup(box, w)
    g0 = G_xx(m, box, 0.0, "int", j0, w, r); gi = G_xx(m, box, 0.1, "int", j0, w, r); gh = G_xx(m, box, 0.1, "half", j0, w, r)
    log(f"tier1 box {box}: G0 {g0:.6e}  D(0.1) {gi-gh:.3e}  S(0.1) {gh-g0:.3e}  imag parts {gi.imag:.1e},{gh.imag:.1e}  [{time.time()-t0:.1f} s]")

def run():
    out = {}
    # known-answer control
    box, m, r = 120, 0.1, 8; j0 = 60
    g0 = G_xx(m, box, 0.0, "half", j0, 0, r); gh = G_xx(m, box, 0.025, "half", j0, 0, r)
    ratio = ((gh - g0).real / 0.025); pred = -k0(m * r) ** 2 / (2 * math.pi)
    ok_ka = abs(ratio / pred - 1) <= 0.15
    log(f"known-answer: S/alpha = {ratio:.5f} vs -K0(mr)^2/2pi = {pred:.5f}  rel {ratio/pred-1:+.3f}  [{'PASS' if ok_ka else 'FAIL'}]")
    out["known_answer"] = dict(ratio=ratio, pred=pred, ok=bool(ok_ka))
    # main
    box, w, m = 384, 32, 1 / 32; j0 = setup(box, w); al = [0.025, 0.05, 0.1, 0.2]
    okP = True; okMF = True
    for r in (2, 4):
        g0 = G_xx(m, box, 0.0, "int", j0, w, r)
        triv = G_xx(m, box, 0.0, "half", j0, w, r) - g0
        Dv, Sv = [], []
        for a in al:
            t0 = time.time()
            gi = G_xx(m, box, a, "int", j0, w, r); gh = G_xx(m, box, a, "half", j0, w, r)
            Dv.append((gi - gh).real); Sv.append((gh - g0).real)
            log(f"  r={r} alpha={a}: D {Dv[-1]:+.6e}  S {Sv[-1]:+.6e}  (imag {gi.imag:.1e}, {gh.imag:.1e})  [{time.time()-t0:.0f} s]")
        sD = [slope(al[i], Dv[i], al[i + 1], Dv[i + 1]) for i in range(3)]
        sS = [slope(al[i], Sv[i], al[i + 1], Sv[i + 1]) for i in range(3)]
        pD = all(1.7 <= s <= 2.3 for s in sD[:2]); pS = all(0.7 <= s <= 1.3 for s in sS[:2]); okP &= pD; okMF &= pS
        log(f" r={r}: trivial D(0)=S(0) {abs(triv):.1e}; slopes D {['%.3f'%s for s in sD]} [{'PASS' if pD else 'FAIL'}]; "
            f"slopes S {['%.3f'%s for s in sS]} [{'must-fail PASS' if pS else 'must-fail FAIL'}]; D/alpha^2 {['%.4e'%(d/a**2) for d,a in zip(Dv,al)]}")
        out[f"r{r}"] = dict(alpha=al, D=Dv, S=Sv, slopesD=sD, slopesS=sS, trivial=abs(triv))
    log(f"P (gap b) {'PASS' if okP else 'FAIL'}; must-fail {'PASS' if okMF else 'FAIL'}; known-answer {'PASS' if ok_ka else 'FAIL'}")
    json.dump(out, open(os.path.join(D0, "exp054_results.json"), "w"), indent=1)

if __name__ == "__main__":
    {"tier1": tier1, "run": run}[sys.argv[1]]()
