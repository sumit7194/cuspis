"""EXP-083 R3' arm (b), comparison C1 (registered before any number): production T_sad (sigma3d.saddle_term, s_cut 3) vs an
independent finite difference of the continued replica saddle.
  sigma(1 +- h) from the continued gap (exp083_armb.Gap, s_cut 3, target 'self'; quasi-Newton with J0 = -(1/Ny) sum_p G0_p o G0_p
  from direct inverses), h in {4e-3, 2e-3, 1e-3}; sigdot = Richardson of central differences.
  T_lin = d/dt sum_k logdet B1_k(t sigdot) |_0 and T_dir = d/dh sum_k logdet B1_k(sigma(1+h)) with B1 from exp083_honest.Geom
  (direct inverses, independent of Strip3D), both Richardson-extrapolated; drifts recorded.
Plants (production side): P1 -T, P2 0, P3 sigdot/2, P4 production saddle_term source-patched B1[0] -> B1[1] (k-index).
P <= 10: production recomputed (and stored 081b tsad compared); P = 12: stored tsad only (memory), P4 skipped.
Usage: python exp083_armb_c1.py W P Wbox c   [model: Opus 5.5]"""
import sys, os, json, time, importlib.util, numpy as np
from exp083_honest import Geom
import sigma3d as S3, exp083_armb as AB
W, P, WB, C = (int(a) for a in sys.argv[1:5]); g = Geom(W, P, Wbox=WB, c=C); T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "exp083_armb"); os.makedirs(OUT, exist_ok=True)
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)
res = dict(W=W, P=P, Wbox=WB, c=C, N=g.N, Ny=g.Ny)
stored = None
for d in ("exp081d_results", "exp081b_results", "exp081c_results", "exp083_r2"):   # 081d first (EXP-081d C1 control)
    f = os.path.join(HERE, d, f"sigma_W{W}_P{P}_box{WB}_c{C}_cp12_sc3.0_dd0_ckpt.json")
    if os.path.exists(f): stored = json.load(open(f)).get("tsad"); res["stored_from"] = f; break
if P == 2: stored = json.load(open(os.path.join(HERE, "exp083_r2", f"prod_W{W}P2_sc3.0_dd0_ckpt.json")))["tsad"]
res["T_stored"] = stored
# ---- production side ----
if P <= 10:
    S0 = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0); B1 = S0.B1()
    T_prod, d, sd_prod, gapchk = S3.saddle_term(S0, B1, return_checks=True); T_prod = float(T_prod.real); sd_prod = sd_prod.real
    src = open(os.path.join(HERE, "sigma3d.py")).read(); t = src.replace("sig = np.linalg.solve(B1[0], 2 * d)", "sig = np.linalg.solve(B1[1], 2 * d)")
    assert t != src; pth = os.path.join(OUT, "_sigma3d_kindex.py"); open(pth, "w").write(t)
    spec = importlib.util.spec_from_file_location("s3k", pth); S3k = importlib.util.module_from_spec(spec); spec.loader.exec_module(S3k)
    T_P4 = float(S3k.saddle_term(S0, B1).real); del B1, S0
    res.update(T_prod=T_prod, gapcheck=float(gapchk), T_P4=T_P4)
    log(f"production T_sad {T_prod:+.12f} (stored {stored}); gapcheck {gapchk:.1e}; planted k-index T {T_P4:+.12f}")
else:
    T_prod = stored; sd_prod = None; res.update(T_prod=T_prod, T_P4=None); log(f"production T_sad (stored, P = 12) {T_prod:+.12f}")
# ---- independent FD side ----
G1 = g.Gn(1); J0 = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
L = lambda sig: g.logdetB(g.Gn(1, sig))
def sigdot(gap, hs, nc=1e-12):
    sd = {}
    for h in hs:
        sp, ip = gap.solve(1 + h, J=J0, tol=1e-14, noise_ceiling=nc); sm, im_ = gap.solve(1 - h, J=J0, tol=1e-14, noise_ceiling=nc)
        sd[h] = ((sp - sm) / (2 * h), sp, sm, max(ip["F"], im_["F"]), max(ip["it"], im_["it"]))
    return sd
gap = AB.Gap(g, s_cut=3.0, target="self"); hs = (4e-3, 2e-3, 1e-3); sd = sigdot(gap, hs)
R1 = (4 * sd[2e-3][0] - sd[4e-3][0]) / 3; R2 = (4 * sd[1e-3][0] - sd[2e-3][0]) / 3
sdot = R2; sd_drift = float(np.abs(R2 - R1).max() / np.abs(R2).max())
log(f"sigdot: |sigdot| {np.abs(sdot).max():.4e}; Richardson drift {sd_drift:.1e}; gap |F| <= {max(v[3] for v in sd.values()):.1e}, it <= {max(v[4] for v in sd.values())}")
def Tlin(ts=(1e-3, 5e-4)):
    v = {t: (L(t * sdot) - L(-t * sdot)) / (2 * t) for t in ts}; return (4 * v[ts[1]] - v[ts[0]]) / 3, v
T_lin, vl = Tlin(); T_lin2, _ = Tlin((2e-3, 1e-3))
dirv = {h: (L(sd[h][1]) - L(sd[h][2])) / (2 * h) for h in hs}
T_dir = (4 * dirv[1e-3] - dirv[2e-3]) / 3; T_dir1 = (4 * dirv[2e-3] - dirv[4e-3]) / 3
drift = max(abs(T_lin - T_lin2), abs(T_dir - T_dir1), abs(T_lin - T_dir)) / abs(T_lin)
res.update(T_lin=T_lin, T_lin2=T_lin2, T_dir=T_dir, T_dir1=T_dir1, fd_drift=drift, sd_drift=sd_drift)
log(f"FD: T_lin {T_lin:+.12f} (t-halved {T_lin2:+.12f}); T_dir {T_dir:+.12f} (h-shifted {T_dir1:+.12f}); FD drift (rel) {drift:.1e}")
gi = AB.Gap(g, s_cut=np.inf, target="self"); sdi = sigdot(gi, (2e-3, 1e-3), nc=1e-10); sdot_inf = (4 * sdi[1e-3][0] - sdi[2e-3][0]) / 3
# deviation (W8P8 run 1): the all-pole (s_cut = inf) gap has a noise floor ~1e-11 at W8 > the 1e-12 ceiling; auxiliary arm only -> 1e-10
res["sdot_scut_effect"] = float(np.abs(sdot_inf - sdot).max() / np.abs(sdot).max())
# ---- comparison and plants ----
tau = max(1e-6, 10 * drift) * abs(T_prod); res["tau"] = tau; dlt = abs(T_lin - T_prod); res["delta"] = dlt
res["verdict"] = "PASS" if dlt <= tau else "FAIL"
if stored is not None:   # EXP-081d: the T_sad that enters R(k) is the checkpoint value (081c numerics); graded with the same tau
    res["delta_stored"] = abs(T_lin - stored); res["verdict_stored"] = "PASS" if res["delta_stored"] <= tau else "FAIL"
if drift > 1e-7: res["verdict"] += " (precision-limited: FD drift > 1e-7)"
plants = dict(P1_signflip=-T_prod, P2_off=0.0, P3_half=T_prod / 2, P4_kindex=res["T_P4"])
res["plants"] = {k: (None if v is None else dict(T=v, delta=abs(T_lin - v), ratio=abs(T_lin - v) / tau, fires=bool(abs(T_lin - v) > 10 * tau))) for k, v in plants.items()}
if sd_prod is not None:
    res["sdot_vec_rel"] = float(np.abs(sdot - sd_prod).max() / np.abs(sd_prod).max())
log(f"C1 W{W}P{P}box{WB}c{C}: |T_FD - T_prod| = {dlt:.2e} (rel {dlt/abs(T_prod):.1e}) vs tau {tau:.2e} -> {res['verdict']}; "
    f"sigdot vector rel {res.get('sdot_vec_rel', float('nan')):.1e}; s_cut 3 vs inf on sigdot {res['sdot_scut_effect']:.1e}")
for k, v in res["plants"].items():
    log(f"   plant {k}: " + ("skipped (P = 12)" if v is None else f"|T_FD - T_plant| / tau = {v['ratio']:.1e} -> {'FIRES' if v['fires'] else 'DOES NOT FIRE'}"))
json.dump(res, open(os.path.join(OUT, f"c1_W{W}P{P}box{WB}c{C}.json"), "w"), indent=1)
