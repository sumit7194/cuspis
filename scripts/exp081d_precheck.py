"""EXP-081d pre-checks (before registration; existing geometries only, no new-k number): evidence that each control CAN fire, and the
known-answer controls. Reads checkpoints written by exp081d_route.py runs (see run_081d_precheck.sh). [model: Opus 5.5]
  KA1  k = 1 (W2P4b4, W4P4b4), 081d pipeline (low-rank) vs 081b stored, posctl tolerances: node impact <= 1e-7, |dt0|, |dtsad| <= 2e-6, |dS| <= 1e-6
  LR   k = 1 low-rank vs full residues: |dS| / |S| <= 1e-12 (and tol_ref structural agreement)
  LRp  plant: rank-drop 1 must move S by > 1e3 x the LR tolerance
  KA2  k = 2 W8P8: low-rank t0, tsad, g(node 0) vs the stored 081c (full residues) values, <= 1e-12 rel
  RESp plant for the residue-impact check: residues x (1 + 1e-6) at k = 1 W4P4b4 must give (1/2)|dT_sad| > 1e-7"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
D = os.path.join(HERE, "exp081d_results"); B = os.path.join(HERE, "exp081b_results"); out = {}
x, w = np.polynomial.legendre.leggauss(12); NODES = []
for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
    for xi, wi in zip(x, w):
        si = 0.5 * (hi - lo) * (xi + 1) + lo; NODES.append((si, 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2))
key = lambda s: f"g|{s:.15f}"; g_ = lambda v: v[0] if isinstance(v, list) else v
L = lambda t: json.load(open(os.path.join(D, t + "_ckpt.json")))
Sof = lambda d: 0.5 * (d["t0"] + d["tsad"] + sum(wt * g_(d[key(s)]) for s, wt in NODES))
for W in (2, 4):
    tag = f"sigma_W{W}_P4_box4_c2_cp12_sc3.0_dd0"; n = L(tag); r = json.load(open(os.path.join(B, tag + "_ckpt.json")))
    imp = max(abs(n[key(s)] - g_(r[key(s)])) * np.pi / np.cosh(np.pi * s) ** 2 for s, _ in NODES)
    dt0, dts, dS = abs(n["t0"] - r["t0"]), abs(n["tsad"] - r["tsad"]), abs(Sof(n) - Sof(r))
    ok = imp <= 1e-7 and dt0 <= 2e-6 and dts <= 2e-6 and dS <= 1e-6
    f = L(tag + "_full"); dlr = abs(Sof(n) - Sof(f)) / abs(Sof(f)); p = L(tag + "_rd1"); dpl = abs(Sof(p) - Sof(f)) / abs(Sof(f))
    out[f"W{W}P4"] = dict(KA1=dict(node_impact=imp, dt0=dt0, dtsad=dts, dS=dS, pass_=ok), LR=dict(rel=dlr, pass_=dlr <= 1e-12),
                          LRp=dict(rel=dpl, fires=dpl > 1e3 * 1e-12), ranks=n.get("ranks"), summary=n.get("summary"), planted=n.get("planted"), b2b=n.get("b2b"))
    print(f"KA1 W{W}P4b4 vs 081b: max node impact {imp:.1e}, |dt0| {dt0:.1e}, |dtsad| {dts:.1e}, |dS| {dS:.1e} -> {'PASS' if ok else 'FAIL'}")
    print(f"LR  W{W}P4b4 low-rank vs full: |dS|/|S| {dlr:.1e} -> {'PASS' if dlr <= 1e-12 else 'FAIL'};  LRp rank-drop 1: |dS|/|S| {dpl:.1e} -> {'FIRES' if dpl > 1e-9 else 'DOES NOT FIRE'}; ranks {n.get('ranks')}")
    sm = n["summary"]; pl = n["planted"]
    print(f"    checks at W{W}P4b4: planted ratio {pl['dg']/pl['pred']:.4f} impact {pl['impact']:.1e} fires {pl['fires']}; B2b {n['b2b']['rel']:.1e}; "
          f"N1'''c max impact {max(r_[2] for r_ in sm['n1c_rows']):.1e}; t0 {sm['t0_check']:.1e}; residue impact {sm['residue_impact']:.1e}; Woodbury fires {sm['woodbury_fires']}")
k2 = L("sigma_W8_P8_box8_c2_cp12_sc3.0_dd0_ka"); r2 = json.load(open(os.path.join(HERE, "exp081c_results", "sigma_W8_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json")))
s0 = NODES[0][0]; rel = {nm: abs(k2[nm] - r2[nm]) / abs(r2[nm]) for nm in ("t0", "tsad")}; rel["g0"] = abs(k2[key(s0)] - r2[key(s0)]) / abs(r2[key(s0)])
out["KA2"] = dict(rel, pass_=all(v <= 1e-12 for v in rel.values()), ranks=k2.get("ranks"))
print(f"KA2 W8P8 low-rank vs stored 081c (full): " + ", ".join(f"{k_} {v:.1e}" for k_, v in rel.items()) + f" -> {'PASS' if out['KA2']['pass_'] else 'FAIL'}; ranks {k2.get('ranks')}")
# RESp: residue plant for the impact-graded residue check
P_, W_, Wb_ = 4, 4, 4; Lx, Lt = 2 * P_ + Wb_, 2 * P_; x0 = P_ + (Wb_ - W_) // 2; Ny = 4 * P_
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W_)), P_ - 1, s_cut=3.0); U = C.install(S, refine="auto", lowrank=True); B1 = S.B1()
t_ref = C.saddle_term_c(S, B1)
for u in U.values():
    u.Rp = [None if R is None else (R[0] * (1 + 1e-6), R[1]) for R in u.Rp]; u.Rm = [None if R is None else (R[0] * (1 + 1e-6), R[1]) for R in u.Rm]
t_pl = C.saddle_term_c(S, B1); ri = 0.5 * abs(t_pl - t_ref); out["RESp"] = dict(impact=ri, fires=bool(ri > 1e-7))
print(f"RESp residues x(1+1e-6) at W4P4b4: (1/2)|dT_sad| {ri:.1e} -> {'FIRES' if ri > 1e-7 else 'DOES NOT FIRE'} (threshold 1e-7)")
# tol_ref structural agreement, low-rank vs full path (k = 1 W4P4b4)
from tools.tol_ref import path_disagreement
Sf = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W_)), P_ - 1, s_cut=3.0); C.install(Sf, refine="auto")
Sl = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W_)), P_ - 1, s_cut=3.0); C.install(Sl, refine="auto", lowrank=True)
class V:   # view with Rfull-expanded residues so path_disagreement compares like with like
    def __init__(s, S_): s.sl = [type("o", (), dict(s=x_.s, Rp=[None if R is None else x_.Rfull(R) for R in x_.Rp], Rm=[None if R is None else x_.Rfull(R) for R in x_.Rm])) for x_ in S_.sl]
ds, dr = path_disagreement(V(Sf), V(Sl)); out["tol_ref"] = dict(ds=ds, dr=dr); print(f"tol_ref low-rank vs full path at W4P4b4: |ds| {ds:.1e}, residue rel {dr:.1e}")
# T0p: plant for the t0 refined-vs-unrefined check (threshold 2e-6): t0 with G and residues x (1 + 1e-7) at W4P4b4 must move t0 by > 2e-6
t_a = C.t0_term(S, B1)
for u in U.values(): u.scale = 1.0 + 1e-7
t_b = C.t0_term(S, B1); out["T0p"] = dict(dt0=abs(t_b - t_a), fires=bool(abs(t_b - t_a) > 2e-6)); print(f"T0p t0 with x(1+1e-7): |dt0| {abs(t_b - t_a):.1e} -> {'FIRES' if abs(t_b - t_a) > 2e-6 else 'DOES NOT FIRE'} (threshold 2e-6)")
# B2b can fire: the stored 081c W8P8 unrefined arm at s = 1.974 vs refined (the B2b comparison type, threshold 1e-12 rel)
s2 = 1.974126375751365; gref = r2[key(s2)]; gun = r2["n1c"]["arms"][f"{s2:.15f}"]; rb = abs(gref - gun) / abs(gref)
out["B2b_canfire"] = dict(rel=rb, fires=bool(rb > 1e-12)); print(f"B2b can-fire evidence (081c W8P8, unrefined vs refined at s=1.974): rel {rb:.1e} -> {'FIRES' if rb > 1e-12 else 'DOES NOT FIRE'} at 1e-12")
# planted-scale guard at every 081d geometry (plant_guard.check_scale_plant)
from tools.plant_guard import check_scale_plant
out["scale_plant_guard"] = {}
for k in (1, 1.5, 2, 2.5, 3):
    for Wg in (int(2 * k), int(4 * k)):
        Pg = int(4 * k); Ng = (2 * Pg + Pg) * 2 * Pg; Nyg = 4 * Pg; s1 = 0.937383295744266
        e = 1e-6 / (2 * Ng * Nyg * np.pi / np.cosh(np.pi * s1) ** 2); gd = check_scale_plant(e, Ng, Nyg, s1); out["scale_plant_guard"][f"W{Wg}P{Pg}b{Pg}"] = gd
        print(f"scale-plant guard W{Wg}P{Pg}b{Pg}: eps {gd['eps']:.2e}, predicted dg {gd['pred']:.2e}, impact {gd['impact']:.1e} -> can fire")
json.dump(out, open(os.path.join(D, "precheck_results.json"), "w"), indent=1, default=str)
