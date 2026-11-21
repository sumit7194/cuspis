"""EXP-081c census gate (registered control table): production pole lists vs own sign-change census at s <= 3 for the 081c
geometries W8P8 box8 and W2P8 box8 (081b census code). [model: Opus 5.5]"""
import json
from exp081b_census import census, geom
out = {}
for W in (8, 2):
    c = census(geom(W, 8, Wbox=8), 3.0); out[f"W{W}P8b8"] = [dict(p=x["p"], match=x["match"], touch=x["touch"]) for x in c if not x["match"] or x["touch"]]
out["ok"] = all(not v for k, v in out.items() if k != "ok")
print(json.dumps(out, indent=1)); json.dump(out, open("exp081c_census_results.json", "w"), indent=1)
