"""EXP-069 (pre-registered in report.md): complex-twist BIE validation on the CH07b line a = 1/2 + iy.
Points (w, y): (0.3, 0.5), (0.3, 1), (0.3, 2), (1.0, 1), (0.1, 1). Ladder: p in {7, 8} (L = 20), theta_max in {0.70, 0.80} pi,
R in {0.12, 0.16} x min(w,1), K_modes = 8, n_ang = 37. Best = (p=8, 0.75 pi, 0.14 w)... see report; error = sum of spreads.
V1: |E/E_pred - 1| <= max(3 err_rel, 2e-3), E_pred = -w_S/(8 pi a(1-a) w) (EXP-044 Fredholm). V2: k(w) = DeltaC/Int_w^inf bhat u (CH05)
constant over w in {0.1, 0.3, 1} at y = 1 within 3 x combined error. V3: spreads and |Im E|/|E| vs y (descriptive). P: planted 2%. [model: Opus 5.5]"""
import sys, os, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp069_bie_complex as B
from exp044_det import w_scalar
import exp063_precheck_ratio as RR
def ladder(w, y, scale=1.0):
    a = 0.5 + 1j * y; vals = {}
    for p in (7, 8):
        s = B.TwistedIntervalBIE(w, a, n_layers=20, p=p)
        for tm in (0.70, 0.75, 0.80):
            for Rf in (0.12, 0.14, 0.16):
                if (tm == 0.75) != (Rf == 0.14): continue          # best point (0.75, 0.14) + the 2x2 corners
                vals[(p, tm, Rf)] = s.extract_DeltaC_and_E(Rf * min(w, 1.0), theta_max=tm * np.pi, K_modes=8, n_ang=37, proj_norm_scale=scale)
    best = vals[(8, 0.75, 0.14)]
    def spread(i):
        sp_p = abs(vals[(8, 0.75, 0.14)][i] - vals[(7, 0.75, 0.14)][i])
        corners = [vals[(8, t, r)][i] for t in (0.70, 0.80) for r in (0.12, 0.16)]
        sp_pr = max(abs(c - best[i]) for c in corners)
        return sp_p + sp_pr
    return best, spread(0), spread(1), vals
def tail_bu(a, ws):
    sol = RR.run(a, False, t0=16.0, t1=min(ws) * 0.5); out = {}
    for w in ws:
        ss = np.geomspace(w, 16.0, 20001); v = []
        for s in ss:
            u, _, _, lbr, lbi, _, _ = sol.sol(s); v.append(np.exp(lbr + 1j * lbi) * np.exp(-s) * s ** -1.5 * u)
        out[w] = np.trapezoid(np.array(v), ss)
    return out
if __name__ == "__main__":
    pts = [(0.3, 0.5), (0.3, 1.0), (0.3, 2.0), (1.0, 1.0), (0.1, 1.0)]; res = {}; v1 = True; t0 = time.time()
    for w, y in pts:
        a = 0.5 + 1j * y; Ep = -complex(w_scalar(w, a)[0]) / (8 * np.pi * a * (1 - a) * w)
        (dC, E), eC, eE, _ = ladder(w, y); rel = abs(E / Ep - 1); tol = max(3 * eE / abs(E), 2e-3); ok = rel <= tol; v1 &= ok
        res[(w, y)] = dict(dC=dC, eC=eC, E=E, eE=eE, Ep=Ep)
        print(f"(w={w}, y={y}): E = {E:.7f} +- {eE:.1e}  E_pred = {Ep.real:.7f}  |E/Ep-1| = {rel:.2e} (tol {tol:.1e}) [{'PASS' if ok else 'FAIL'}]"
              f"  |ImE|/|E| = {abs(E.imag)/abs(E):.1e}  DeltaC = {dC:.6f} +- {eC:.1e}  [{time.time()-t0:.0f}s]", flush=True)
    print(f"V1 {'PASS' if v1 else 'FAIL'}", flush=True)
    tb = tail_bu(0.5 + 1j, [0.1, 0.3, 1.0]); ks = {w: res[(w, 1.0)]['dC'] / tb[w] for w in (0.1, 0.3, 1.0)}
    km = np.mean(list(ks.values())); dev = max(abs(k - km) for k in ks.values())
    comb = max(abs(res[(w, 1.0)]['eC'] / tb[w]) for w in (0.1, 0.3, 1.0))
    v2 = dev <= 3 * comb
    print("V2 k(w) at y=1: " + "  ".join(f"w={w}: {k:.6f}" for w, k in ks.items()) + f"   max dev {dev:.2e} vs 3x err {3*comb:.2e} [{'PASS' if v2 else 'FAIL'}]", flush=True)
    (dCp, Epl), _, eEp, _ = ladder(0.3, 1.0, scale=1.02); d = abs(Epl - res[(0.3, 1.0)]['E'])
    print(f"P planted 2% at (0.3, 1): |dE| = {d:.2e} = {d/res[(0.3,1.0)]['eE']:.1f} sigma [{'FIRES' if d > 3*res[(0.3,1.0)]['eE'] else 'does not fire'}]", flush=True)
    json.dump({f"{w}_{y}": {k: [complex(v).real, complex(v).imag] for k, v in r.items()} for (w, y), r in res.items()},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp069_results.json"), "w"), indent=1)
