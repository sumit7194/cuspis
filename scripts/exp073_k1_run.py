"""EXP-073(b) production: registered in report.md (see 'EXP-073(b) ... pre-registration'). [model: Opus 5.5]"""
import json, time, math, numpy as np
from scipy.optimize import brentq
from exp073_k1 import Kfree, cfh_eigs, top, pressure_guard
def logdet_IK(Ks): return complex(np.sum(np.log(np.linalg.eigvals(np.eye(len(Ks)) - Ks))))
def fit3(Ws, f):
    f = np.asarray(f, float); r = (f[0] - f[1]) / (f[1] - f[2]) if f[1] != f[2] else np.nan
    g = lambda p: (Ws[0] ** -p - Ws[1] ** -p) / (Ws[1] ** -p - Ws[2] ** -p) - r
    ps = np.linspace(0.02, 8, 4000); v = np.array([g(p) for p in ps])
    roots = [brentq(g, ps[i], ps[i + 1]) for i in range(len(ps) - 1) if np.isfinite(v[i]) and np.sign(v[i]) != np.sign(v[i + 1])]
    if not roots: return np.nan, np.nan
    p = roots[0]; c = (f[0] - f[1]) / (Ws[0] ** -p - Ws[1] ** -p); return f[0] - c * Ws[0] ** -p, p
res = {}; Ws = (8, 16, 32, 64); allpass = True; inconcl = False
for a in (0.3, 0.5 + 0.5j):
    for t in (1.0, 2.0):
        key = f"a={a},t={t}"; cf = top(cfh_eigs(t, a, h=0.05)); cfp = top(cfh_eigs(t, a, h=0.05, scale_t=1.03))
        cfdet = complex(np.sum(np.log(1 - cfh_eigs(t, a, h=0.05))))
        rows = {}
        for W in Ws:
            pressure_guard(); t0 = time.time(); Ks, info = Kfree(W, t, a); ev = top(np.linalg.eigvals(Ks)); ld = logdet_IK(Ks)
            rows[W] = (ev, ld)
            print(f"{key} W={W} N={info['N']} |P|={info['P']}: top3 {np.round(ev, 7)}  logdet(I-K) {ld:+.7e}  "
                  f"rel to CFH {np.round(np.abs(ev/cf-1), 4)}  [{time.time()-t0:.0f}s]", flush=True)
        # nuisance at W=32
        pressure_guard(); Ksn, _ = Kfree(32, t, a, pad_over_m=6.0, D_over_m=6.0); evn = top(np.linalg.eigvals(Ksn))
        nuis = float(np.max(np.abs(evn / rows[32][0] - 1)))
        ext = []; ps = []
        for k in range(3):
            seq = [rows[W][0][k] for W in Ws[1:]]
            val = [s.real for s in seq] if abs(a.imag if isinstance(a, complex) else 0) == 0 else [abs(s) for s in seq]
            fi, p = fit3(np.array(Ws[1:], float), val); ext.append(fi); ps.append(p)
        ref = [c.real for c in cf] if not isinstance(a, complex) else [abs(c) for c in cf]
        refp = cfp[0].real if not isinstance(a, complex) else abs(cfp[0])
        relext = [abs(e / r - 1) for e, r in zip(ext, ref)]
        mono = all(abs(abs(rows[Ws[i + 1]][0][0]) / abs(cf[0]) - 1) < abs(abs(rows[Ws[i]][0][0]) / abs(cf[0]) - 1) for i in range(3))
        sign_ok = all(np.sign(rows[64][0][k].real) == np.sign(cf[k].real) for k in range(3))
        dseq = [rows[W][1].real for W in Ws[1:]]; dfi, dp = fit3(np.array(Ws[1:], float), dseq)
        p_ok = all(np.isfinite(ps)) and nuis <= 1e-3
        spec_pass = p_ok and sign_ok and mono and max(relext) <= 0.02
        planted_apart = abs(refp / ext[0] - 1) > 0.02 if np.isfinite(ext[0]) else False
        if not p_ok: inconcl = True
        allpass &= spec_pass
        print(f"  => extrap top3 {np.round(ext, 7)} (p {np.round(ps, 3)}) vs CFH {np.round(ref, 7)} rel {np.round(relext, 4)}; "
              f"monotone {mono}; same sign {sign_ok}; nuisance {nuis:.1e}; K1-spec [{'PASS' if spec_pass else ('INCONCLUSIVE' if not p_ok else 'FAIL')}]; "
              f"planted told apart {planted_apart}; K1-det extrap {dfi:+.6e} (p {dp:.3f}) vs CFH {cfdet.real:+.6e} rel {abs(dfi/cfdet.real-1):.3f}", flush=True)
        res[key] = dict(cfh=[str(c) for c in cf], cfh_planted=str(cfp[0]), rows={W: ([str(e) for e in rows[W][0]], str(rows[W][1])) for W in Ws},
                        extrap=ext, p=ps, relext=relext, mono=mono, sign_ok=sign_ok, nuis=nuis, spec_pass=spec_pass,
                        planted_apart=planted_apart, det_extrap=dfi, det_p=dp, cfh_det=str(cfdet))
print("OVERALL K1-spec:", "INCONCLUSIVE" if inconcl else ("PASS" if allpass else "FAIL"), flush=True)
json.dump(res, open("exp073_k1_results.json", "w"), indent=1, default=str)
