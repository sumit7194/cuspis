"""EXP-093 amendment 1 IDENTITY: Air W2P6 route checkpoint (pulled to exp081d_results/air_pull/) vs the stored W2P6 checkpoint (EXP-089).
PASS iff t0, tsad, all 48 g nodes and n1c arms agree <= 1e-10 rel AND row(6) (Air W2P6 + stored W4P6) reproduces exp089_wall.json r6 to 1e-4.
Exit 0 PASS, 1 FAIL, 2 'between 1e-10 and 1e-4' (Bridge decides). [model: Opus 5.5]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp081d_analyze as AN
name = "sigma_W2_P6_box6_c2_cp12_sc3.0_dd0_ckpt.json"
air, ref = json.load(open(os.path.join(D, "air_pull", name))), json.load(open(os.path.join(D, name)))
rel = lambda a, b: abs(a - b) / max(abs(b), 1e-300); worst = []
for k in ("t0", "tsad"): worst.append((k, rel(air[k], ref[k])))
nodes = [f"g|{s:.15f}" for s, _ in AN.nodes48()]
miss = [k for k in nodes if k not in air]; worst += [(k, rel(air[k], ref[k])) for k in nodes if k in air]
arms_a, arms_r = air.get("n1c", {}).get("arms", {}), ref["n1c"]["arms"]
worst += [(f"arm {k}", rel(arms_a[k], v)) for k, v in arms_r.items() if k in arms_a]; miss += [f"arm {k}" for k in arms_r if k not in arms_a]
mx = max(worst, key=lambda t: t[1])
print(f"nodes/arms missing on the Air: {miss if miss else 'none'};  max rel dev {mx[1]:.2e} at {mx[0]};  t0 {worst[0][1]:.1e} tsad {worst[1][1]:.1e}")
w4 = json.load(open(os.path.join(D, "sigma_W4_P6_box6_c2_cp12_sc3.0_dd0_ckpt.json"))); W89 = json.load(open(os.path.join(D, "exp089_wall.json")))["r6"]
nm = W89["norm"]; R = -(AN.S_T(air)["S_T0"] - AN.S_T(w4)["S_T0"]) * nm
print(f"row(6) R from Air W2P6 + stored W4P6: {R:.10f} vs exp089 {W89['R']:.10f} (diff {R - W89['R']:+.1e})")
ok10 = not miss and mx[1] <= 1e-10; ok4 = abs(R - W89["R"]) <= 1e-4
lab = "PASS" if ok10 and ok4 else ("BETWEEN 1e-10 and 1e-4 (Bridge decides)" if ok4 and not miss else "FAIL")
print(f"IDENTITY: {lab}"); sys.exit(0 if lab == "PASS" else (2 if lab.startswith("BETWEEN") else 1))
