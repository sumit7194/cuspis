"""Fable side check (2026-11-25; UNVERIFIED; small sizes only): E(W,P) = 1/2 t0 - 2 Ny Sum_x Lambda(x) d(x)  (S units),
the per-geometry 'explicit term after its OPE/local-mass subtraction'.  Uses the production functions unchanged
(sigma3d.Strip3D, exp081c_numerics.install / t0_term / coincident_dn_c; Lambda as in exp085c_run.pieces).
Known-answer control: W4P4 and W6P6 must reproduce the stored t0 and X_Lam.  [model: Fable 5.2]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SC = os.path.join(HERE, "..", "..", "scripts"); sys.path.insert(0, SC)
import sigma3d as S3, exp081c_numerics as C
def run(W, P, Wb=None, Ny=None):
    t = time.time(); Wb = P if Wb is None else Wb; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P if Ny is None else Ny
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=False, rank_drop=0)
    B1 = S.B1(); t0 = float(np.real(C.t0_term(S, B1))); d = C.coincident_dn_c(S)
    G0 = np.array([sl.G0 for sl in S.sl], dtype=complex); A = np.array([np.linalg.inv(B1[k]) for k in range(Ny)])
    Lam = (A * G0).sum(axis=0).sum(axis=1) / Ny
    XL = -2 * Ny * float(np.real(np.sum(Lam * d))); sig = np.linalg.solve(B1[0], 2 * d)
    rho = np.linalg.solve(B1[0], np.ones(S.N)).real          # rho_eq(x) = (B_{k=0}^{-1} 1)(x): the 3D row sum of B^-1
    rec = dict(W=W, P=P, Wb=Wb, Lx=Lx, Lt=Lt, Ny=Ny, t0=t0, X_Lam=XL, E=0.5 * t0 + XL, Sigma3D=float(np.real(Ny * np.sum(sig))),
               sum_d=float(np.real(np.sum(d))), rho_mid=float(rho[(Lx // 2) * Lt + P]), rho_min=float(rho.min()), rho_max=float(rho.max()),
               Lam_mid=float(Lam.real[(Lx // 2) * Lt + P]), sec=time.time() - t)
    json.dump(rec, open(os.path.join(HERE, f"E_W{W}P{P}b{Wb}Ny{Ny}.json"), "w"), indent=1)
    print(json.dumps(rec), flush=True); return rec
if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:]]; run(*a)
