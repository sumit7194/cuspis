"""EXP-083 R2 edit 2: sector-decomposed Q(n) vs DIRECT n-sheet manifold Q(n) (float64), both arms; P = 2 n = 2..6, P = 4 n = 2, 3.
Pass: <= 1e-9 (absolute on Q(n), and relative reported); else STOP. Also compares the saddle sigma_n from both forms. [model: Opus 5.5]"""
import time, json, numpy as np
from exp083_honest import Geom
import exp083_sector as SEC
T0 = time.time(); worst = 0.0; out = {}
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)
for P, ns in ((2, range(2, 7)), (4, (2, 3))):
    for W in (2, 4):
        g = Geom(W, P); ld1d = g.logdetB(g.Gn(1)); ld1s = SEC.sector_logdet(g, 1, SEC.sector_G(g, 1))
        log(f"W{W}P{P}: log det B1 direct {ld1d:+.12f} sector {ld1s:+.12f} diff {abs(ld1d-ld1s):.1e}")
        for n in ns:
            for arm in ("a", "b"):
                if arm == "a":
                    qd = g.logdetB(g.Gn(n)) - n * ld1d; qs = SEC.sector_logdet(g, n, SEC.sector_G(g, n)) - n * ld1s; ds = ""
                else:
                    sd, _ = g.saddle(n); qd = g.logdetB(g.Gn(n, sd)) - n * ld1d
                    ss, Gs, _ = SEC.sector_saddle(g, n); qs = SEC.sector_logdet(g, n, Gs) - n * ld1s; ds = f" | sigma diff {np.abs(sd-ss).max():.1e}"
                d = abs(qd - qs); worst = max(worst, d); out[f"W{W}P{P}n{n}{arm}"] = [qd, qs, d]
                log(f"   n={n} arm ({arm}): direct {qd:+.12f} sector {qs:+.12f} |diff| {d:.1e}{ds}")
log(f"WORST |diff| {worst:.1e} -> {'PASS' if worst <= 1e-9 else 'FAIL -> STOP'}; max |arg det| in sector form {SEC.PHASE[0]:.1e}")
json.dump(dict(rows=out, worst=worst, pass_=bool(worst <= 1e-9)), open("exp083_r2_validate_results.json", "w"), indent=1)
