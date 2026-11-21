"""(e) sensitivity of T46d to its r -> 0 threshold (hard-coded 1e-10 in I_f1, tail loops, dB/dn, d_vec): scratch copies of the
delivered code with only that literal changed. N_th=16 mu_max=4 dq=0.25 Q=16, z = 4, 8, s_max 2.5. Also counts modes with 0 < r <= 1e-8."""
import sys, os, importlib.util, numpy as np
src = open(os.path.join(sys.argv[1], "brief_p2_t46d.py")).read()
for thr in ("1e-8", "1e-10", "1e-12", "1e-14"):
    path = os.path.join(sys.argv[2], f"t46d_thr_{thr}.py"); open(path, "w").write(src.replace("1e-10", thr))
    spec = importlib.util.spec_from_file_location(f"t{thr}", path); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
    op = D.ConformalEllipticModel(N_th=16, mu_max=4.0); eng = D.CenteredQEngine(op, dq=0.25, Q_max=16.0, K_max=16, act_tol=0.0)
    if thr == "1e-8":
        rs = np.concatenate([D.mode_params(q['lams'])[1] for q in eng.qcache]); print(f"  modes with 0 < r <= 1e-8: {int(np.sum((rs > 0) & (rs <= 1e-8)))}, r == 0: {int(np.sum(rs == 0))}, of {rs.size}", flush=True)
    out = [eng.eval_K(K, s_max=2.5, n_s1=8, n_s2=4) for K in (8, 16)]
    print(f"  threshold {thr}: z=4 T0 {out[0][3]:+.6f} T2 {out[0][4]:+.6f} | z=8 T0 {out[1][3]:+.6f} T2 {out[1][4]:+.6f}", flush=True)
