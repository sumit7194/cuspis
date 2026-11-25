"""h0(P) = P (G_inf(0) - G1_box(centre, centre)) for the n = 1 box (Lx = 3P, Lt = 2P, Dirichlet; Ny = 4P periodic), by mode sums. [model: Fable 5.2]
Then the H-log test and a constrained refit of my centre c_A values. Leading-order lattice sums only."""
import numpy as np, json, time, resource
t0 = time.time(); GINF = 0.2527310098586630                    # simple cubic lattice Green function at the origin for H = 6 - hops (Watson); checked below
def modes(L):
    j = np.arange(1, L + 1); return 2 - 2 * np.cos(np.pi * j / (L + 1)), np.sqrt(2 / (L + 1)) * np.sin(np.pi * np.outer(j, j) / (L + 1))
def gbox(P, Ny=None):
    Lx, Lt = 3 * P, 2 * P; Ny = Ny or 4 * P; ex, Vx = modes(Lx); et, Vt = modes(Lt); m = 2 - 2 * np.cos(2 * np.pi * np.arange(Ny) / Ny); out = []
    for x in (Lx // 2 - 1, Lx // 2):
        for t in (Lt // 2 - 1, Lt // 2):
            w = np.outer(Vx[x] ** 2, Vt[t] ** 2); out.append(np.mean([(w / (ex[:, None] + et[None, :] + mm)).sum() for mm in m]))
    return float(np.mean(out))
# control: a big periodic cube must reproduce GINF (zero mode excluded -> approaches from below like 1/L)
for n in (64, 128):
    k = 2 - 2 * np.cos(2 * np.pi * np.arange(n) / n); E = k[:, None, None] + k[None, :, None] + k[None, None, :]; E[0, 0, 0] = np.inf
    print(f"control: periodic {n}^3 mean 1/E = {(1 / E).mean():.9f}  (G_inf {GINF:.9f}; difference {(GINF - (1/E).mean())*n:.4f}/n)")
Ps = np.array([4, 6, 8, 10, 12, 14, 20, 28, 40, 56]); h = np.array([P * (GINF - gbox(P)) for P in Ps])
print("P :", Ps.tolist()); print("h0(P) = P (G_inf - G_box(centre)):", np.round(h, 5))
A = np.column_stack([np.ones(4), 1.0 / Ps[-4:], 1.0 / Ps[-4:] ** 2]); co = np.linalg.lstsq(A, h[-4:], rcond=None)[0]; h0 = co[0]; y1 = 32 / (3 * np.pi ** 2)
print(f"h0(inf) = {h0:.5f} (from P = 20..56, with 1/P, 1/P^2);  y1 = {y1:.4f};  H-log prediction gL = y1*h0 = {y1*h0:.5f}   [free fits gave 0.0736-0.0769]")
P = np.array([4, 6, 8, 10, 12, 14.]); cA = []
for p in P.astype(int):
    j = json.load(open(f'cA_centre_P{p}{"_all" if p in (4, 6) else ""}.json')); a = np.array(j['cA'])
    cA.append(a.reshape(3 * p, 2 * p)[3 * p // 2 - 1:3 * p // 2 + 1, p - 1:p + 1].mean() if p in (4, 6) else a.mean())
cA = np.array(cA); gL = y1 * h0
for idx, lab in (([2, 3, 4, 5], "P = 8..14"), ([1, 2, 3, 4, 5], "P = 6..14"), ([3, 4, 5], "P = 10..14 (exact)")):
    p = P[idx]; A = np.column_stack([np.ones(len(p)), 1 / p, 1 / p ** 2]); y = cA[idx] - gL * np.log(p) / p; co = np.linalg.lstsq(A, y, rcond=None)[0]
    print(f"   gL FIXED = {gL:.4f}: c_A = c_inf + (g1 + gL ln P)/P + g2/P^2, {lab}: c_inf {co[0]:+.5f}  g1 {co[1]:+.4f}  g2 {co[2]:+.4f}  rms {np.sqrt(np.mean((A@co-y)**2)):.1e}")
    A0 = np.column_stack([np.ones(len(p)), 1 / p, 1 / p ** 2]); c0 = np.linalg.lstsq(A0, cA[idx], rcond=None)[0]
    print(f"   {'no log':17s}: c_A = c_inf + g1/P + g2/P^2,              {lab}: c_inf {c0[0]:+.5f}  rms {np.sqrt(np.mean((A0@c0-cA[idx])**2)):.1e}")
print(f"wall {time.time()-t0:.1f} s, peak {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.0f} MB")
