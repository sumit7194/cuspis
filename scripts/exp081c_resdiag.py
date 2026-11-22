"""EXP-081c W8P8: why did the registered residue check fire (refined vs unrefined residues, 8.7e-7 rel > 1e-8)? Diagnostic
only; the registered verdict logic is not changed by it. Per unique slice and pole s <= 3 (both Rp and Rm):
  s, contour radius r, rel |R_ref - R_unref| (the registered quantity), rel |R_ref+1 - R_ref| (is the refined residue itself
  converged?), and the same on diag(R) (what enters the saddle's coincident term).
Then T_sad with unrefined residues vs the production T_sad (refined), the one residue consumer N1'''c / t0 do not cover.
[model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
W, P, Wb = 8, 8, 8; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P; T0 = time.time()
st = json.load(open(os.path.join(HERE, "exp081c_results", "sigma_W8_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json")))
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); U = C.install(S, refine=0)
rows = []
rel = lambda A, B: float(np.abs(A - B).max() / np.abs(A).max())
for p, sl in U.items():
    for j, sj in enumerate(sl.s):
        if sj > 3.0: continue
        r = min(1e-6, 0.3 * min([abs(sj - sk) for sk in sl.s if sk != sj] + [1.0]))
        for side, a0, Ru in (("+", 1j * sj, sl.Rp[j]), ("-", -1j * sj, sl.Rm[j])):
            sl.refine = "auto"; Rr = sl.residue(a0, r); sl.extra = 1; Rr1 = sl.residue(a0, r); sl.extra = 0; sl.refine = 0
            row = dict(p=p, j=j, s=sj, side=side, r=r, Rmax=float(np.abs(Rr).max()), rel_unref=rel(Rr, Ru), rel_plus1=rel(Rr1, Rr),
                       diag_rel_unref=rel(np.diag(Rr), np.diag(Ru)), diag_rel_plus1=rel(np.diag(Rr1), np.diag(Rr)))
            rows.append(row)
            print(f"[{time.time()-T0:5.0f}s] p={p:2d} s={sj:.5f}{side} r={r:.1e} |R|max {row['Rmax']:.2e}: ref vs unref {row['rel_unref']:.1e} "
                  f"(diag {row['diag_rel_unref']:.1e}); ref+1 vs ref {row['rel_plus1']:.1e} (diag {row['diag_rel_plus1']:.1e})", flush=True)
B1 = S.B1(); tsad_u = C.saddle_term_c(S, B1)
print(f"T_sad with unrefined residues {tsad_u:+.12f} vs production (refined) {st['tsad']:+.12f}: |d| {abs(tsad_u - st['tsad']):.1e}")
w = max(rows, key=lambda x: x["rel_unref"])
print(f"worst: p={w['p']} s={w['s']:.5f}{w['side']} rel_unref {w['rel_unref']:.1e}; max rel_plus1 over all poles {max(x['rel_plus1'] for x in rows):.1e}; "
      f"poles with rel_unref > 1e-8: {sum(x['rel_unref'] > 1e-8 for x in rows)} of {len(rows)}")
json.dump(dict(rows=rows, tsad_unref=tsad_u, tsad_prod=st["tsad"]), open(os.path.join(HERE, "exp081c_results", "resdiag_W8P8.json"), "w"), indent=1)
