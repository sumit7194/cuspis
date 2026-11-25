"""EXP-088 C POST-HOC (why the registered check fired): central-difference error scaling with eps and Richardson extrapolation
D_R = (4 D(eps/2) - D(eps))/3, at eps in {1e-3, 1e-4, 1e-5}; n = 2 and the n = 1 control. Same code paths as exp088_checks C. [model: Opus 5.5]"""
import sys, os, numpy as np
sys.argv = ["x", "none"]; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "exp088_checks.py")).read(); exec(src.split("mode = sys.argv[1]")[0])
import sigma3d as S3, exp081c_numerics as C
rng = np.random.default_rng(20261125)
for W, P, Wb in ((2, 2, 2), (2, 3, 4)):
    g = H.Geom(W, P, Wbox=Wb, c=2); N, Ny = g.N, g.Ny; J0 = sum(np.diag(x) for x in g.Gn(1)) / Ny; s0 = saddle_target(g, 2, J0)
    for hn, h in (("uniform", np.ones(N)), ("random", rng.normal(size=N))):
        pred = -0.5 * 2 * Ny * float(np.dot(h, s0)); D = {}
        for eps in (2e-3, 1e-3, 1e-4, 5e-5, 1e-5):
            fp = f_lead(g, 2, saddle_target(g, 2, J0 + eps * h, s0), J0 + eps * h); fm = f_lead(g, 2, saddle_target(g, 2, J0 - eps * h, s0), J0 - eps * h); D[eps] = (fp - fm) / (2 * eps)
        e = {k: abs(v - pred) / abs(pred) for k, v in D.items()}; R = (4 * D[1e-3] - D[2e-3]) / 3; R2 = (4 * D[5e-5] - D[1e-4]) / 3
        print(f"W{W}P{P}Wb{Wb} n=2 h={hn}: rel err eps 1e-3 {e[1e-3]:.1e}, 1e-4 {e[1e-4]:.1e}, 1e-5 {e[1e-5]:.1e} (ratio per decade {e[1e-3]/e[1e-4]:.0f}, {e[1e-4]/e[1e-5]:.0f}); Richardson rel err {abs(R-pred)/abs(pred):.1e} / {abs(R2-pred)/abs(pred):.1e}")
    for eps in (1e-3, 1e-4, 1e-5):
        h = np.ones(N); fp = f_lead(g, 1, saddle_target(g, 1, J0 + eps * h), J0 + eps * h); fm = f_lead(g, 1, saddle_target(g, 1, J0 - eps * h), J0 - eps * h)
        print(f"   n=1 control h=uniform eps {eps:.0e}: FD derivative {(fp - fm) / (2 * eps):+.3e} (exact 0)")
