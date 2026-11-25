"""S-b consistency checks for the A-vs-bulk brief. NOT blind: k <= 2.5 stored numbers only. No P = 12 file, no addendum. [model: Fable 5.2]
Stated before running, what would contradict the seals (c615773):
 (1) raw g_b(k) not approaching a constant: a k-linear or log fit beating g_inf - beta/k + gamma/k^2;
 (2) u(x) = 1 - c_A(x)/c not falling off from the walls (no ~1/d profile), or the interior not ~ a/P;
 (3) wall layer (distance to nearest wall d <= 2) carrying more than 5% of Sum u*sigma_2 (sigma_2 used as a proxy weight: sigdot per site is not stored)."""
import json, numpy as np, time, resource
t0 = time.time(); R = '/Users/sumit/Github/corner_function/scripts/exp081d_results/'
c = json.load(open(R + 'exp085/E.json'))['ends']['hi c(384)']; ks = np.array([1, 1.5, 2, 2.5])
gb = np.array([0.17603, 0.21676, 0.24490, 0.26248])          # raw g_b, hi c (notes/fable_n2/gb_n1_output.txt)
print("(1) forms fitted to raw g_b(k), k = 1..2.5 (4 points):")
for lab, cols in (("g_inf - beta/k", [np.ones(4), -1 / ks]), ("a + b k", [np.ones(4), ks]), ("a + b ln k", [np.ones(4), np.log(ks)]),
                  ("g_inf - beta/k + gamma/k^2", [np.ones(4), -1 / ks, 1 / ks ** 2])):
    A = np.column_stack(cols); co = np.linalg.lstsq(A, gb, rcond=None)[0]; rms = np.sqrt(np.mean((A @ co - gb) ** 2))
    k3 = {"g_inf - beta/k": co[0] - co[1] / 3, "a + b k": co[0] + 3 * co[1], "a + b ln k": co[0] + co[1] * np.log(3)}.get(lab, co[0] - co[1] / 3 + (co[2] / 9 if len(co) > 2 else 0))
    print(f"    {lab:28s} coeffs {np.round(co, 4)}  rms {rms:.1e}  -> value at k = 3: {k3:.4f}")
print("(2) u(x) = 1 - c_A/c_hi versus distance d to the nearest wall (W-wide strip of each P; c_A does not know the cut):")
for (W, P) in [(4, 4), (6, 6), (8, 8), (10, 10)]:
    g = json.load(open(R + f'exp085c/G_W{W}P{P}.json')); Lx, Lt = g['Lx'], g['Lt']; u = 1 - np.array(g['cA']).reshape(Lx, Lt) / c
    X, T = np.meshgrid(np.arange(Lx), np.arange(Lt), indexing='ij'); d = np.minimum(np.minimum(X + 1, Lx - X), np.minimum(T + 1, Lt - T))
    row = [f"d={dd}: {u[d == dd].mean():.3f} (u*d {u[d == dd].mean() * dd:.2f})" for dd in range(1, int(d.max()) + 1)]
    ctr = u[Lx // 2 - 1:Lx // 2 + 1, Lt // 2 - 1:Lt // 2 + 1].mean()
    print(f"    P={P}: centre u {ctr:.4f} (u*P {ctr * P:.3f}) | " + "  ".join(row))
    if (W, P) != (10, 10):
        s2 = np.array(json.load(open(R + f'exp084c/c84_W{W}P{P}_n2.json'))['sigma']).reshape(Lx, Lt); tot = (u * s2).sum()
        print(f"       (3) proxy weight sigma_2: share of Sum u*sigma_2 from d <= 1: {(u*s2)[d <= 1].sum()/tot:.4f}; d <= 2: {(u*s2)[d <= 2].sum()/tot:.4f}; "
              f"sigma_2 mean at d = 1: {s2[d == 1].mean():+.2e} (overall min {s2.min():+.3f})")
print("    centre c_A extrapolated in 1/P (quadratic through P = 6, 8, 10) vs the bracket [%.5f, %.5f]:" % (c, json.load(open(R + 'exp085/E.json'))['ends']['lo c(384)+3Delta']))
cen = []
for (W, P) in [(4, 4), (6, 6), (8, 8), (10, 10)]:
    g = json.load(open(R + f'exp085c/G_W{W}P{P}.json')); Lx, Lt = g['Lx'], g['Lt']; cen.append(np.array(g['cA']).reshape(Lx, Lt)[Lx // 2 - 1:Lx // 2 + 1, Lt // 2 - 1:Lt // 2 + 1].mean())
cen = np.array(cen); v = 1 / np.array([4, 6, 8, 10.])
q = np.polyfit(v[1:], cen[1:], 2); l2 = np.polyfit(v[2:], cen[2:], 1); print(f"    centre c_A: {np.round(cen, 6)}; quadratic (6,8,10) -> c_Ainf {q[2]:+.5f}, value at P = 12 {np.polyval(q, 1/12):+.5f} (ratio {np.polyval(q, 1/12)/c:.4f}); "
      f"linear (8,10) -> {l2[1]:+.5f}; cubic (4..10) -> {np.polyfit(v, cen, 3)[3]:+.5f}")
print(f"wall time {time.time()-t0:.2f} s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.0f} MB")
