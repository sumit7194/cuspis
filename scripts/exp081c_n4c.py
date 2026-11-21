"""EXP-081c N4c (registered 8fcfb84 section 7 + amendment C): s_cut 3.0 vs 3.5 at P = 6 (W = 2 and 4, box 4, 081b numerics),
census complete to 3.5 required. dR = R(3.5) - R(3.0) with R = delta_kappa_lat / kappa_lat(6), impact rule.
Systematic rule: pass if |dR| <= 0.1 sigma_route, else add 2|dR| in quadrature. Prediction check: |dR| <= 1e-4.
Runs the 081b worker for the s_cut = 3.5 geometries (results in exp081b_results/, tagged sc3.5). [model: Opus 5.5]"""
import os, sys, json, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exp081b_run as R, exp081b_analyze as A
from exp081b_census import census, geom
cen = {}
for W in (2, 4):
    S = geom(W, 6); S.s_cut = 3.5; c = census(S, 3.5); cen[W] = all(x["match"] and not x["touch"] for x in c)
    tag = f"sigma_W{W}_P6_box4_c2_cp12_sc3.5_dd0"
    if not os.path.exists(os.path.join(R.OUT, tag + ".json")):
        subprocess.run([sys.executable, "-u", "-W", "ignore", os.path.join(HERE, "exp081b_worker.py"), str(W), "6", "4", "2", "12", "3.5", "0"], check=True)
f = lambda sc: R.pair(lambda W, P, **kw: A.S_from_ckpt(f"sigma_W{W}_P{P}_box4_c2_cp12_sc{sc}_dd0", "impact")["S_T0"], 6)
kap6 = R.pair(lambda W, P, **kw: R.free(W, P, **kw), 6)
dR = (f(3.5) - f(3.0)) / kap6; si = json.load(open(os.path.join(HERE, "exp081b_results_impact.json")))["S_T0"]["route_i"][1]
res = dict(dR=dR, census_to_3p5=cen, census_ok=all(cen.values()), sys_pass=bool(abs(dR) <= 0.1 * si), prediction_ok=bool(abs(dR) <= 1e-4))
print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(HERE, "exp081c_n4c_results.json"), "w"), indent=1)
