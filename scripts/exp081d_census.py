"""EXP-081d census gate (registration 963c8f5, row CEN): production pole lists vs the 081b sign-change census at s <= 3 for the given
geometries. Usage: python exp081d_census.py W:P:Wbox ...   (writes exp081d_results/census_<geoms>.json) [model: Opus 5.5]"""
import sys, os, json
from exp081b_census import census, geom
out = {}
for gstr in sys.argv[1:]:
    W, P, B = (int(v) for v in gstr.split(":")); c = census(geom(W, P, Wbox=B), 3.0)
    bad = [dict(p=x["p"], match=x["match"], touch=x["touch"]) for x in c if not x["match"] or x["touch"]]
    out[f"W{W}P{P}b{B}"] = dict(flagged=bad, ok=not bad); print(f"census W{W}P{P}b{B}: {'PASS' if not bad else f'FLAGGED {bad}'}", flush=True)
json.dump(out, open(os.path.join("exp081d_results", "census_" + "_".join(a.replace(":", "-") for a in sys.argv[1:]) + ".json"), "w"), indent=1)
