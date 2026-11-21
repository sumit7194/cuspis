"""EXP-074 run: registered in report.md (3583ffa). [model: Opus 5.5]"""
import json, numpy as np
from exp074_richardson import extrap
from exp073_k1 import cfh_eigs, top
c = json.load(open("exp073_k1_cache.json")); W = np.array([8, 16, 32, 64.])
verdicts = []; res = {}
for a in (0.3, 0.5 + 0.5j):
    for t in (1.0, 2.0):
        cf = top(cfh_eigs(t, a, h=0.05)); cfp = top(cfh_eigs(t, a, h=0.05, scale_t=1.03))
        for k in (0, 1):
            f = np.array([abs(complex(*c[f"{a}|{t}|{int(w)}|8.0|8.0"]["ev"][k])) for w in W])
            e8 = abs(complex(*c[f"{a}|{t}|32|8.0|8.0"]["ev"][k])); e6 = abs(complex(*c[f"{a}|{t}|32|6.0|6.0"]["ev"][k]))
            nuis = abs(e6 / e8 - 1)
            fB, ssys, det = extrap(W, f, a); lam = abs(cf[k]); lamp = abs(cfp[k])
            stot = np.hypot(ssys, nuis * lam)
            if stot / lam > 0.02: v = "INCONCLUSIVE"
            elif abs(fB - lam) <= 3 * stot: v = "PASS" if abs(fB - lamp) > 3 * stot else "INCONCLUSIVE(planted not apart)"
            else: v = "FAIL"
            verdicts.append(v)
            print(f"a={a} t={t} lam{k+1}: f_B={fB:.6e} f_A={det['A'][0]:.6e} (A resid {det['A'][1]:.1e}) CFH={lam:.6e} "
                  f"rel={fB/lam-1:+.4f} sigma_tot/lam={stot/lam:.4f} |f_B-CFH|/sigma_tot={abs(fB-lam)/stot:.2f} "
                  f"planted rel={lamp/lam-1:+.3f} -> {v}", flush=True)
            res[f"{a}|{t}|{k+1}"] = dict(fB=fB, fA=det['A'][0], cfh=lam, planted=lamp, sigma_tot=stot, nuis=nuis, verdict=v)
overall = "PASS" if all(v == "PASS" for v in verdicts) else ("FAIL" if "FAIL" in verdicts else "INCONCLUSIVE")
print("OVERALL:", overall); json.dump(res, open("exp074_results.json", "w"), indent=1)
