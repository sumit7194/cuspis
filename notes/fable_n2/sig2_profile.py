"""Read-only look at the stored n = 2 saddles sigma_2(x) (office files exp084c/c84_W*P*_n2.json) and c_A (exp085c/G_W*P*.json). [model: Fable 5.2]
Questions: where does sigma_2 live (cut ends vs along the cut), how does it fall with distance r from the nearest cut end, and which region carries
the W-difference of Sum sigma_2 and of Sum c_A sigma_2.  Nothing is recomputed; no P = 10 file is opened."""
import json, numpy as np
R = '/Users/sumit/Github/corner_function/scripts/exp081d_results/'
def load(W, P):
    s = json.load(open(R + f'exp084c/c84_W{W}P{P}_n2.json')); g = json.load(open(R + f'exp085c/G_W{W}P{P}.json'))
    Lx, Lt = g['Lx'], g['Lt']; sig = np.array(s['sigma']); cA = np.array(g['cA'])
    return sig, cA, Lx, Lt, g['cutx'], g['tcut'], g['Ny']
def grid(a, Lx, Lt):
    A = a.reshape(Lx, Lt); B = a.reshape(Lt, Lx).T          # two candidate orderings; pick the one symmetric under x-reflection about the cut centre
    return A, B
out = {}
for (W, P) in [(2, 4), (4, 4), (3, 6), (6, 6), (4, 8), (8, 8)]:
    sig, cA, Lx, Lt, cutx, tc, Ny = load(W, P)
    A, B = grid(sig, Lx, Lt); xc = 0.5 * (cutx[0] + cutx[-1])
    def asym(M):
        tot = 0.0
        for x in range(Lx):
            xr = int(round(2 * xc - x))
            if 0 <= xr < Lx: tot += np.abs(M[x] - M[xr]).sum()
        return tot / np.abs(M).sum()
    aA, aB = asym(A), asym(B); S = A if aA < aB else B; C = (cA.reshape(Lx, Lt) if aA < aB else cA.reshape(Lt, Lx).T)
    # cut ends: the cut links join t = tc and tc+1 for x in cutx; end points sit at x = cutx[0]-1/2 and cutx[-1]+1/2, t = tc+1/2
    X, T = np.meshgrid(np.arange(Lx), np.arange(Lt), indexing='ij')
    eL = (cutx[0] - 0.5, tc + 0.5); eR = (cutx[-1] + 0.5, tc + 0.5)
    r = np.minimum(np.hypot(X - eL[0], T - eL[1]), np.hypot(X - eR[0], T - eR[1]))
    print(f"\nW{W}P{P}: Lx {Lx} Lt {Lt} cutx {cutx[0]}..{cutx[-1]} tcut {tc}; ordering asym (x*Lt+t) {aA:.1e} vs (t*Lx+x) {aB:.1e}; "
          f"Sum s2 {S.sum():+.6f}  Sum cA s2 {(C*S).sum():+.6f}  min {S.min():+.4f} max {S.max():+.4f}")
    imx = np.unravel_index(np.argmax(np.abs(S)), S.shape); print(f"   |s2| max at (x,t) = {imx}, r = {r[imx]:.3f}")
    # radial shells
    edges = [0, 0.8, 1.2, 1.7, 2.3, 3.2, 4.5, 6.5, 9, 13, 99]; row = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (r >= a) & (r < b)
        if m.sum(): row.append((a, b, int(m.sum()), S[m].sum(), S[m].mean(), (S[m] * r[m] ** 2).mean(), (C[m] * S[m]).sum()))
    print("   shell r in [a,b): n sites, Sum s2, mean s2, mean r^2 s2, Sum cA s2")
    for a, b, nn, ss, mm, r2, cs in row: print(f"   [{a:4.1f},{b:4.1f}) {nn:4d} {ss:+.6f} {mm:+.6f} {r2:+.5f} {cs:+.6f}")
    # sites next to the cut but far from both ends (only meaningful for W >= 6)
    mid = [x for x in cutx if min(x - cutx[0], cutx[-1] - x) >= 2]
    if mid: print(f"   along the cut, >= 2 sites from both ends: s2(t=tc) {np.round(S[mid, tc], 5)}  s2(t=tc+1) {np.round(S[mid, tc + 1], 5)}")
    out[(W, P)] = dict(S=S, C=C, r=r, Ny=Ny)
np.save('/private/tmp/claude-501/-Users-sumit-Github-corner-function/608cf772-cd8d-40f9-9656-6871c385aec1/scratchpad/sig2_grids.npy', out, allow_pickle=True)
JD = json.load(open('/Users/sumit/Github/corner_function/scripts/exp081d_results.json'))
print("\nW-differences by region (narrow minus wide), per k; D = Sum s2(W1) - Sum s2(W2), DA = Sum cA s2 (W1) - (W2); dR2^A = Ny*DA*norm")
for k, (g1, g2) in {1: ((2, 4), (4, 4)), 1.5: ((3, 6), (6, 6)), 2: ((4, 8), (8, 8))}.items():
    P = int(4 * k); norm = 1 / (4 * P) / (1 / (2 * k) - 1 / (4 * k)) / JD[str(k)]['kappa']; Ny = 4 * P
    a, b = out[g1], out[g2]; line = []
    for lab, lo, hi in (("core r<1.2", 0, 1.2), ("1.2<=r<3.2", 1.2, 3.2), ("r>=3.2", 3.2, 99), ("all", 0, 99)):
        ma = (a['r'] >= lo) & (a['r'] < hi); mb = (b['r'] >= lo) & (b['r'] < hi)
        D = a['S'][ma].sum() - b['S'][mb].sum(); DA = (a['C'] * a['S'])[ma].sum() - (b['C'] * b['S'])[mb].sum()
        line.append(f"{lab}: D {D:+.5f} DA {DA:+.6f} dR2A {Ny*DA*norm:+.4f}")
    print(f" k={k}: " + " | ".join(line))
