"""EXP-092 amendment b grader: P = 24 against the predictions committed in 01ac42a (exp092b_pred_P24.json), by the registered rule;
then the DESCRIPTIVE P = 8-24 refits (rms ratio, free gL, c_inf sweep). [model: Opus 5.5]"""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "exp081d_results")
pr = json.load(open(os.path.join(D, "exp092b_pred_P24.json"))); m = json.load(open(os.path.join(D, "exp092_cA_P24.json")))["centre"]
pi, pii = pr["pred"]["i_P8-20"]["P24"], pr["pred"]["ii_P8-20"]["P24"]; gap = abs(pii - pi); ei, eii = abs(m - pi), abs(m - pii)
if eii < ei and eii <= 0.5 * gap: rd = "FREE LOG HOLDS OUT OF SAMPLE"
elif ei < eii and ei <= 0.5 * gap: rd = "NO-LOG HOLDS OUT OF SAMPLE"
elif ei > gap and eii > gap: rd = "NEITHER FORM EXTRAPOLATES"
else: rd = "UNDECIDED"
print(f"P = 24 measured {m:+.12f}")
print(f"  (i) no-log  {pi:+.10f}  e_i  {ei:.3e}\n  (ii) free log {pii:+.10f}  e_ii {eii:.3e}\n  gap {gap:.3e}, half-gap {0.5*gap:.3e}")
print(f"  (iii) fixed gL {pr['pred']['iii_P8-20']['P24']:+.10f}  e {abs(m - pr['pred']['iii_P8-20']['P24']):.3e}  [reported]")
hl, nl = pr["pred"]["Hlog3_P8-14"]["P24"], pr["pred"]["nolog3_P8-14"]["P24"]; dL, dN, g2 = abs(m - hl), abs(m - nl), abs(hl - nl)
sec = "H-log supported" if (dL < dN and dL <= 0.5 * g2) else ("H-log contradicted" if dN < dL else "undecided")
print(f"  sec.2 pair (P = 8-14): H-log {hl:+.10f} d_L {dL:.3e}; no-log {nl:+.10f} d_N {dN:.3e}; gap {g2:.3e} -> {sec} [secondary]")
print(f"PRIMARY READING (registered 01ac42a): {rd}")
C = dict(pr["inputs"]); C = {int(k): v for k, v in C.items()}; C[24] = m; GL = 0.0611
def fit(Ps, form):
    P = np.array(Ps, float); y = np.array([C[p] for p in Ps])
    X = {"i": np.vstack([np.ones_like(P), 1/P, 1/P**2, 1/P**3]).T, "ii": np.vstack([np.ones_like(P), 1/P, np.log(P)/P, 1/P**2]).T,
         "iii": np.vstack([np.ones_like(P), 1/P, 1/P**2]).T}[form]
    off = GL * np.log(P) / P if form == "iii" else 0 * P
    c = np.linalg.lstsq(X, y - off, rcond=None)[0]; res = y - off - X @ c
    return c, float(np.sqrt(np.mean(res ** 2)))
desc = {}
for Ps in ((8, 10, 12, 14, 16, 20, 24), (10, 12, 14, 16, 20, 24)):
    lab = f"P={Ps[0]}-24"; row = {}
    for f in ("i", "ii", "iii"):
        c, rms = fit(Ps, f); row[f] = dict(cinf=float(c[0]), rms=rms, **({"gL": float(c[2])} if f == "ii" else {}))
    desc[lab] = row
    print(f"[descriptive] {lab}: rms (i) {row['i']['rms']:.2e}, (ii) {row['ii']['rms']:.2e} (gL {row['ii']['gL']:+.4f}), (iii) {row['iii']['rms']:.2e};  "
          f"ratio (ii)/(i) {row['ii']['rms']/row['i']['rms']:.3f};  c_inf (i) {row['i']['cinf']:+.5f} (ii) {row['ii']['cinf']:+.5f} (iii) {row['iii']['cinf']:+.5f}")
json.dump(dict(measured=m, e_i=ei, e_ii=eii, gap=gap, reading=rd, secondary=sec, d_L=dL, d_N=dN, descriptive=desc), open(os.path.join(D, "exp092b_grade.json"), "w"), indent=1)
