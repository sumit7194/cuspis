"""EXP-083 Tier-1 feasibility (registered cd9e134), HONEST SIDE ONLY, arm (a), no comparison with the continuation:
pure-gauge must-pass; own poles vs production QEP census; honest Q(n); fixed-base (own poles) and free-base fits with the last n
held out; drift; Kronecker gap (n>=2 data extrapolated to n=1 vs Q(1)=0). P = 2 (W2, W4, n<=20) and P = 4 (W2, W4, n<=12). [model: Opus 5.5]"""
import json, time, numpy as np, sigma3d as S3
from exp083_honest import Geom, fit_Qprime, free_base_fit
out = {}; T0 = time.time()
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)
g = Geom(2, 2, cut="wall"); ld1 = g.logdetB(g.Gn(1))
log("pure-gauge (wall-to-wall) honest Q(n), n=2,3,4:", [f"{g.Q(n, ld1=ld1):+.1e}" for n in (2, 3, 4)])
for P, nmax in ((2, 20), (4, 12)):
    for W in (2, 4):
        g = Geom(W, P); S = S3.Strip3D(g.Lx, g.Lt, g.Ny, g.cutx, g.tcut, s_cut=3.0)
        own = {p: g.own_poles(p) for p in range(g.Ny // 2 + 1)}
        mism = [(p, [round(x, 6) for x in S.sl[p].s if x <= 3.5], [round(x, 6) for x in own[p] if x <= 3.5]) for p in own
                if len([x for x in own[p] if x <= 3.5]) != len([x for x in S.sl[p].s if x <= 3.5])
                or any(abs(a - b) > 1e-6 for a, b in zip(sorted(x for x in own[p] if x <= 3.5), sorted(x for x in S.sl[p].s if x <= 3.5)))]
        log(f"W{W}P{P}: own poles (full-operator scan) vs production QEP, s<=3.5: {'MATCH' if not mism else 'MISMATCH ' + str(mism)}")
        ld1 = g.logdetB(g.Gn(1)); ns = list(range(1, nmax + 1)); Qs = [0.0] + [g.Q(n, ld1=ld1) for n in ns[1:]]
        log(f"W{W}P{P}: honest Q(n) n=2..{nmax}: " + " ".join(f"{q:+.8f}" for q in Qs[1:]))
        allb = sorted({np.exp(-2 * np.pi * s) for p in own for s in own[p]}, reverse=True)
        res = {}
        for floor in (1e-4, 1e-6, 1e-7):
            vis = [b for b in allb if b > floor]
            for conf in (False, True):
                try:
                    qp, rms, ho = fit_Qprime(ns, Qs, vis, conf=(vis if conf else ()), nhold=1)
                    res[f"fixed floor {floor:g} conf {conf}"] = (qp, rms, ho, len(vis))
                except Exception as e: res[f"fixed floor {floor:g} conf {conf}"] = (np.nan, np.nan, np.nan, len(vis))
        for nb in (2, 3, 4):
            fb = free_base_fit(ns, Qs, nb)
            if fb: (qp, rms, ho), z = fb; res[f"free {nb}"] = (qp, rms, ho, len(z))
        for k, (qp, rms, ho, nb_) in res.items(): log(f"   {k:28s}: Q'(1) {qp:+.6f}  ({nb_} bases, rms {rms:.1e}, held-out {ho:.1e})")
        good = [v[0] for v in res.values() if np.isfinite(v[0]) and v[2] < 1e-6]
        drift = (max(good) - min(good)) if good else np.nan
        qp2, _, _ = fit_Qprime(ns[1:], Qs[1:], [b for b in allb if b > 1e-6], nhold=1)
        ns2 = np.array(ns[1:-1], float); X = np.column_stack([ns2, np.ones_like(ns2)] + [b ** ns2 for b in allb if b > 1e-6])
        c, *_ = np.linalg.lstsq(X, np.array(Qs[1:-1]), rcond=None); Q1 = c[0] + c[1] + sum(cc * b for cc, b in zip(c[2:], [b for b in allb if b > 1e-6]))
        log(f"   drift over fits with held-out < 1e-6: {drift:.2e} ({len(good)} fits); Kronecker gap (n>=2 fit extrapolated to n=1, should be 0): {Q1:+.3e}")
        out[f"W{W}P{P}"] = dict(Q=Qs, fits={k: list(map(float, v)) for k, v in res.items()}, drift=float(drift), kron_gap=float(Q1), pole_mismatch=str(mism))
json.dump(out, open("exp083_tier1_results.json", "w"), indent=1)
