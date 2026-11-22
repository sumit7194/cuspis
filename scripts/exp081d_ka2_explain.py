"""Why KA2 is bitwise-exact at W8P8 (a zero is not trusted unexplained): same process, low-rank vs full residues -> max residue
reconstruction error, max |d_lowrank - d_full| (coincident term), T_sad both ways. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3, exp081c_numerics as C
P, W, Wb = 8, 8, 8; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
mk = lambda lr: S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
Sf = mk(0); Uf = C.install(Sf, refine="auto"); Sl = mk(1); Ul = C.install(Sl, refine="auto", lowrank=True)
err = max(np.abs(Ul[p].Rfull(Rl) - Uf[p].Rfull(Rf)).max() / np.abs(Uf[p].Rfull(Rf)).max() for p in Uf for Rl, Rf in zip(Ul[p].Rp + Ul[p].Rm, Uf[p].Rp + Uf[p].Rm) if Rf is not None)
df, dl = C.coincident_dn_c(Sf), C.coincident_dn_c(Sl); B1 = Sf.B1()
tf, tl = C.saddle_term_c(Sf, B1), C.saddle_term_c(Sl, B1)
print(f"max residue reconstruction rel error {err:.1e}; max |d_lr - d_full| {np.abs(dl - df).max():.1e} (|d| max {np.abs(df).max():.1e}); "
      f"T_sad full {tf!r} low-rank {tl!r} diff {tl - tf:.1e} (ulp at 220: {np.spacing(220.0):.1e})")
