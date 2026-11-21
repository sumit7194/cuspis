"""EXP-083 R2 A3 feasibility gate (registered ac1e325): own complete pole solve of the EXP-082 family at eps = 1 for every q used
(9 values), via sign changes of F(s) = z^W det H_q(is) / det H_q(0) in Arb (step 2e-3 on (0, 12], local refinement at near-touch
minima); count bases r = e^{-2 pi s}; identifiability at 400 bits: base b visible for n <= 110/|log10 b|; columns per base 2 (single +
confluent). Non-identifiable if, for some window v, columns of bases with visibility <= v exceed the data points n = 2..v. [model: Opus 5.5]"""
import sys, os, json, importlib.util, numpy as np
from flint import acb_mat, arb, ctx
ctx.prec = 400
sys.path.insert(0, "."); import exp082_honest_eps as H0      # (module runs its EXP-082 loop on import: deterministic, ~6 s)
op = H0.model(1.0); N = op.N; L = op.L0.toarray(); W = op.weights
pairs = sorted({(it, ib) for it, ib in zip(op.cut_top, op.cut_bot)})
qs = sorted({round(q, 8) for p in H0.pairs for q in p} | {round((m + 0.5) * 0.5, 8) for m in range(8)})
def F(q, s):
    z = (-2 * arb.pi() * arb(s)).exp(); rows = [[arb(float(L[i, j]) + (q * q * W[i] if i == j else 0.0)) for j in range(N)] for i in range(N)]
    for it, ib in pairs: rows[it][ib] = arb(float(L[it, ib])) * z; rows[ib][it] = arb(float(L[ib, it])) / z
    return float((acb_mat(rows).det().real * z ** len(pairs)).mid())
out = {}; allb = []
for q in qs:
    d0 = F(q, 0.0); g = np.arange(1, 6001) * 2e-3; v = np.array([F(q, x) / d0 for x in g]); roots = []
    for i in range(len(g) - 1):
        if v[i] * v[i + 1] < 0: roots.append(0.5 * (g[i] + g[i + 1]))
    av = np.abs(v)
    for i in range(1, len(g) - 1):
        if av[i] < av[i - 1] and av[i] < av[i + 1] and not any(abs(r - g[i]) < 4e-3 for r in roots):
            gg = np.linspace(g[i - 1], g[i + 1], 401); vv = np.array([F(q, x) / d0 for x in gg])
            roots += [0.5 * (gg[j] + gg[j + 1]) for j in range(400) if vv[j] * vv[j + 1] < 0]
    roots = sorted(roots); out[q] = roots; allb += [np.exp(-2 * np.pi * s) for s in roots]
    print(f"q={q:5.2f}: {len(roots)} poles, s in [{min(roots) if roots else 0:.3f}, {max(roots) if roots else 0:.3f}]; r = {[f'{np.exp(-2*np.pi*s):.1e}' for s in roots]}", flush=True)
allb = sorted(allb, reverse=True); vis = [min(200, int(110 / abs(np.log10(b)))) for b in allb]
print(f"TOTAL bases {len(allb)}; r > 1e-6: {sum(b > 1e-6 for b in allb)}; 1e-20 < r <= 1e-6: {sum(1e-20 < b <= 1e-6 for b in allb)}; r <= 1e-20: {sum(b <= 1e-20 for b in allb)}", flush=True)
bad = []
for v in sorted(set(vis)):
    cols = 2 * sum(1 for x in vis if x <= v); dat = max(0, v - 1)
    if cols > dat: bad.append((v, cols, dat))
print(f"identifiability: {'OK' if not bad else 'FAILS at windows (visibility n<=v, columns, data points): ' + str(bad[:6])}", flush=True)
near = min(allb, key=lambda b: abs(np.log(b / 6.934e-5))); print(f"own base nearest 6.934e-5: {near:.4e}", flush=True)
json.dump(dict(poles={str(k): v for k, v in out.items()}, bases=allb, vis=vis, bad=bad), open("exp083_a3_feas_results.json", "w"), indent=1)
