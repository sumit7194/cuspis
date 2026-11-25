"""EXP-087 production referee at W8P8 (min doublet gap 3.0e-6): rad 1e-6 is free of double counting and above the small-radius floor,
so t0(flag OFF, rad 1e-6) is an INDEPENDENT truth. Same install as exp081d_route (refine auto, low-rank) and C.t0_term. [model: Opus 5.5]
(i) KA: OFF, rad 1e-5 == stored -209.300109928361;  (ii) TRUTH: OFF, rad 1e-6;  (iii) ON, rad 1e-5 == route's -209.279427072581."""
import sys, os, time, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
W = P = Wb = 8; Lx, Lt, Ny = 2 * P + Wb, 2 * P, 4 * P; x0 = P + (Wb - W) // 2; T0 = time.time(); res = {}
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=True, rank_drop=0)
B1 = S.B1(); print(f"installed + B1 ({time.time()-T0:.0f}s)", flush=True)
def t0(flag, rad):
    S3.INNER_BETA0_087 = flag; t = time.time(); dB0 = S.inner_beta0(1.0, rad=rad, dn=True)
    v = float(sum(np.trace(np.linalg.solve(B1[k], dB0[k])) for k in range(Ny)).real); del dB0
    print(f"t0 flag {'ON ' if flag else 'OFF'} rad {rad:.0e}: {v:+.12f}  ({time.time()-t:.0f}s)", flush=True); return v
res["off_1e-5"] = t0(False, 1e-5); print(f"(i) KA vs stored -209.300109928361: diff {res['off_1e-5'] + 209.300109928361:+.1e}", flush=True)
res["off_1e-6"] = t0(False, 1e-6); res["on_1e-5"] = t0(True, 1e-5)
print(f"(iii) ON vs route -209.279427072581: diff {res['on_1e-5'] + 209.279427072581:+.1e}")
print(f"REFEREE: truth(OFF,1e-6) - fixed(ON,1e-5) = {res['off_1e-6'] - res['on_1e-5']:+.2e};  truth - unfixed = {res['off_1e-6'] - res['off_1e-5']:+.6f} (artifact model +0.020126; fix +{res['on_1e-5'] - res['off_1e-5']:.6f})")
json.dump(res, open(os.path.join(HERE, "exp081d_results", "exp087_referee_W8P8.json"), "w"), indent=1)
