"""Fable side check (UNVERIFIED): structure of the kernel K'(x,y) = 1/2 d_n B^(0)(x,y) - 2 G(x,y) d(x), with
E = 1/2 t0 - 2 Sum_3D Lambda d = Sum_{x,y in 3D} B^-1(x,y) K'(x,y)   (exact, algebraic).
Checks: (a) the sum reproduces E; (b) diagonal identity K'(x,x) = -G(x,x) d(x)  [i.e. d_n B^(0)(x,x) = 2 G d];
(c) profile of K'(x, x + Delta e_y) along the periodic direction; (d) split E = T_rho + T_grad,
T_rho = Ny Sum_x rho(x) K'(x,x), rho = B_{k=0}^{-1} 1 (the 3D row sum of B^-1), so T_rho = -Ny Sum rho G d.  [model: Fable 5.2]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3, exp081c_numerics as C
W, P = int(sys.argv[1]), int(sys.argv[2]); t = time.time()
Lx, Lt = 3 * P, 2 * P; x0 = P + (P - W) // 2; Ny = 4 * P
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=False, rank_drop=0)
N = S.N; B1 = S.B1(); dB0 = S.inner_beta0(1.0, dn=True); d = C.coincident_dn_c(S).real
G0 = np.array([sl.G0 for sl in S.sl]); A = np.array([np.linalg.inv(B1[k]) for k in range(Ny)])
t0 = float(sum(np.trace(A[k] @ dB0[k]) for k in range(Ny)).real)
Lam = ((A * G0).sum(axis=0).sum(axis=1) / Ny).real; XL = -2 * Ny * float(np.sum(Lam * d)); E = 0.5 * t0 + XL
G3 = lambda D: (np.cos(2 * np.pi * np.arange(Ny) * D / Ny)[:, None] * np.array([np.diag(g) for g in G0])).sum(axis=0) / Ny   # G_3D(x,x;Delta)
hB = lambda D: (np.cos(2 * np.pi * np.arange(Ny) * D / Ny)[:, None] * np.array([np.diag(b).real for b in dB0])).sum(axis=0) / Ny * 0.5
Kd = {D: hB(D) - 2 * G3(D) * d for D in range(0, Ny // 2 + 1)}
gdiag = G3(0); rho = np.linalg.solve(B1[0], np.ones(N)).real
ident = np.max(np.abs(Kd[0] + gdiag * d)); T_rho = Ny * float(np.sum(rho * Kd[0])); sig = np.linalg.solve(B1[0], 2 * d).real
Sig3D = Ny * float(np.sum(sig)); Gw = float(np.sum(rho * gdiag * d) / np.sum(rho * d))
# E_diag: the y=x term of the 3D sum; B^-1_3D(x,x) = (1/Ny) sum_k A_k(x,x)
Binv_diag = np.array([np.diag(a).real for a in A]).sum(axis=0) / Ny; E_diag = Ny * float(np.sum(Binv_diag * Kd[0]))
idx = lambda x, tt: x * Lt + tt
probes = [(x0 - 2, P), (x0 - 1, P), (x0 + W // 2, P + 1), (x0 + W // 2, P + 2), (Lx // 2, P + P // 2)]
print(f"W{W}P{P}: t0 {t0:.9f}  X_Lam {XL:.9f}  E {E:.9f}   ({time.time()-t:.0f}s)")
print(f"  diagonal identity max|K'(x,x) + G(x,x) d(x)| = {ident:.2e}   (max|G d| = {np.max(np.abs(gdiag*d)):.3e})")
print(f"  T_rho = Ny Sum rho K'(x,x) = {T_rho:.6f};  -1/2 <G>_w Sigma3D = {-0.5*Gw*Sig3D:.6f}  (<G>_w = {Gw:.5f}, Sigma3D = {Sig3D:.6f});  T_grad = E - T_rho = {E - T_rho:.6f};  E_diag = {E_diag:.4f}")
for (x, tt) in probes:
    i = idx(x, tt); row = [Kd[D][i] for D in range(0, min(7, Ny // 2 + 1))]
    print(f"  K'(x,x+Delta e_y) at (x,t)=({x},{tt}), d={d[i]:+.5f}, -G d={-gdiag[i]*d[i]:+.6f}: " + " ".join(f"{v:+.6f}" for v in row))
json.dump(dict(W=W, P=P, t0=t0, X_Lam=XL, E=E, T_rho=T_rho, T_grad=E - T_rho, Gw=Gw, Sigma3D=Sig3D, E_diag=E_diag, ident=float(ident)),
          open(os.path.join(HERE, f"K_W{W}P{P}.json"), "w"), indent=1)
