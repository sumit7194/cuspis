"""Second implementation of c_A (085c sector formula) on the n = 1 box, centre sites or all sites. [model: Fable 5.2]  usage: ca_centre.py P [all] [break]
c_A(z) = -4 term1(z) + 2 (B_0 Lambda)(z);  B_k = (2/Ny) sum_p G_p o G_(k-p);  A_k = B_k^-1;  M_k = (1/Ny) sum_q A_q o G_(k-q);
term1(z) = (1/Ny) sum_k (G_k M_k G_k)(z,z);  Lambda = rowsum((1/Ny) sum_k A_k o G_k).  Sites x*Lt + t, Dirichlet in x and t, periodic y in sectors."""
import sys, json, time, resource, numpy as np
P = int(sys.argv[1]); ALL = "all" in sys.argv; BRK = "break" in sys.argv; t0 = time.time()
Lx, Lt, Ny = 3 * P, 2 * P, 4 * P; N = Lx * Lt; nh = Ny // 2
def modes(L):
    j = np.arange(1, L + 1); return 2 - 2 * np.cos(np.pi * j / (L + 1)), np.sqrt(2 / (L + 1)) * np.sin(np.pi * np.outer(j, j) / (L + 1))
ex, Vx = modes(Lx); et, Vt = modes(Lt); V = np.kron(Vx, Vt); e = (ex[:, None] + et[None, :]).ravel()
G = np.empty((nh + 1, N, N))
for p in range(nh + 1): G[p] = (V / (e + 2 - 2 * np.cos(2 * np.pi * p / Ny))) @ V.T
del V
f = lambda p: min(p % Ny, Ny - p % Ny)                       # G_p = G_(-p)
A = np.empty((nh + 1, N, N)); B0 = None
for k in range(nh + 1):
    B = np.zeros((N, N))
    for p in range(Ny): B += G[f(p)] * G[f(k - p)]
    B *= 2.0 / Ny
    if k == 0: B0 = B.copy()
    A[k] = np.linalg.inv(B)
mult = lambda k: 1 if k in (0, nh) else 2
Lam = sum(mult(k) * (A[k] * G[k]).sum(axis=1) for k in range(nh + 1)) / Ny
zs = np.arange(N) if ALL else np.array([x * Lt + t for x in (Lx // 2 - 1, Lx // 2) for t in (Lt // 2 - 1, Lt // 2)])
term1 = np.zeros(len(zs))
for k in range(nh + 1):
    M = np.zeros((N, N))
    for q in range(Ny): M += A[f(q)] * G[f(k - q)]
    M /= Ny; gz = G[k][:, zs]; term1 += mult(k) * np.einsum("iz,iz->z", gz, M @ gz)
term1 /= Ny
cA = -4 * term1 + (1.0 if BRK else 2.0) * (B0 @ Lam)[zs]
c = -0.11410550636913405; out = dict(P=P, zs=zs.tolist(), cA=cA.tolist(), sec=time.time() - t0, peak_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
msg = f"P={P}: centre c_A {cA.mean() if not ALL else cA[[x*Lt+t for x in (Lx//2-1, Lx//2) for t in (Lt//2-1, Lt//2)]].mean():+.8f}"
cen = cA.mean() if not ALL else cA[[x * Lt + t for x in (Lx // 2 - 1, Lx // 2) for t in (Lt // 2 - 1, Lt // 2)]].mean()
print(f"P={P}: centre c_A {cen:+.8f}  ratio c_A/c_hi {cen/c:.5f}  u*P {(1-cen/c)*P:.4f}   [{out['sec']:.1f} s wall, peak {out['peak_MB']:.0f} MB]{'  (BREAK variant)' if BRK else ''}", flush=True)
if P in (4, 6, 8, 10):
    ref = np.array(json.load(open(f'/Users/sumit/Github/corner_function/scripts/exp081d_results/exp085c/G_W{P}P{P}.json'))['cA'])[zs]
    dev = np.abs(cA - ref).max() / np.abs(ref).max(); print(f"   KA vs stored office c_A ({len(zs)} sites): max rel dev {dev:.1e}  {'PASS' if dev <= 1e-8 else 'FAIL'}", flush=True)
if not BRK: json.dump(out, open(f'/Users/sumit/Github/corner_function-fable/notes/fable_AvB/cA_centre_P{P}{"_all" if ALL else ""}.json', 'w'))
