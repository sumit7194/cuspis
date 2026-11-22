"""EXP-081c POST HOC reading (Bridge, 2026-11-22; written AFTER the W8P8 target was read). The registered verdict is the one in
exp081c_results.json (INCONCLUSIVE, residue clause) and stays the record. This script changes exactly one input to the
registered `decide`: the residue clause is graded by downstream impact instead of the flat 1e-8 relative threshold.
  residue impact (exp081c_resdiag.py): T_sad |d| 4.1e-9 (on 220.1), g <= 3.4e-11 (N1'''c arm uses unrefined residues),
  t0 1.1e-8 -- graded against the registered 1e-7 impact rule. Every other gate and number: unchanged, from the registered run.
Slip 13 (Bridge): the 1e-8 tolerance sat inside the unrefined comparison arm's own known error (Step 0: 2e-9..1.3e-7).
Usage: python exp081c_posthoc.py   [model: Opus 5.5]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exp081c_analyze import decide
reg = json.load(open(os.path.join(HERE, "exp081c_results.json")))
rd = json.load(open(os.path.join(HERE, "exp081c_results", "resdiag_W8P8.json")))
tc = json.load(open(os.path.join(HERE, "exp081c_results", "sigma_W8_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json")))
impacts = dict(tsad=abs(rd["tsad_unref"] - rd["tsad_prod"]), g_max=max(r[2] for r in tc["summary"]["n1c_rows"]), t0=tc["summary"]["t0_check"])
g = dict(reg["gates"]); g["residue_ok"] = all(v <= 1e-7 for v in impacts.values())
for t in ("T0", "T1"): g["R48"][t] = float(g["R48"][t])
ph = decide(g)
out = dict(LABEL="POST HOC (residue clause graded by impact; registered verdict = INCONCLUSIVE, residue clause)", residue_impacts=impacts,
           residue_ok_by_impact=g["residue_ok"], registered_verdict=reg["verdict"], posthoc_verdict=ph["verdict"], tails=ph["tails"],
           rho=ph["rho"], rho_label=ph["rho_label"], richardson_DESCRIPTIVE=ph["richardson_DESCRIPTIVE"],
           R24_b8=reg["R24_b8"], resolution_part=reg["resolution_part"], box_part=reg["box_part"], W8_s_max=reg["W8_s_max"])
json.dump(out, open(os.path.join(HERE, "exp081c_posthoc_results.json"), "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
