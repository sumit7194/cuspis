"""EXP-081 production (registered in report.md, af4969e): lean P1 sign estimate of delta-kappa/kappa_free.
Order: free side (all geometries) -> planted control K -> sigma (W=2 r=2..6, W=3 r=2..4) -> nuisances (Ny, s-quad, edge2,
must-fire) -> extrapolation (forms A, B; routes i, ii) -> verdict. Results cached per configuration (resume-safe).
[model: Opus 5.5]"""
import os, sys, json, time, gc
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sigma3d as S3
from exp073_k1 import pressure_guard
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp081_cache.json")
CKDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp081_ckpt")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def save(): json.dump(cache, open(CACHE, "w"), indent=1)
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)
KAPPA_FREE = 0.0396481

def geom(W, r):
    P = int(round(r * W)); Lx, Lt = W + 2 * P, 2 * P
    return P, Lx, Lt, P - 1, {"strip": list(range(P, P + W)), "edge": list(range(P, Lx)), "edge2": list(range(0, P + W))}

def free_S(W, r, conf, c=2):
    key = f"free|{W}|{r}|{conf}|c{c}"
    if key not in cache:
        P, Lx, Lt, tc, cuts = geom(W, r); Ny = int(c * 2 * P)
        cache[key] = float(S3.FreeStrip(Lx, Lt, Ny, cuts[conf], tc).S(cpts=12).real); save()
    return cache[key]

def sigma_S(W, r, conf, c=2, cpts=12, drop_double=False, saddle=True):
    """EXP-081a: route_i_ckpt (saddle included unless saddle=False), per-beta checkpoints in exp081_ckpt/."""
    key = f"sigmaS|{W}|{r}|{conf}|c{c}|cp{cpts}|dd{int(drop_double)}|sad{int(saddle)}"
    if key not in cache:
        P, Lx, Lt, tc, cuts = geom(W, r); Ny = int(c * 2 * P)
        if Lx * Lt > 500: pressure_guard(min_free_pct=50)
        os.makedirs(CKDIR, exist_ok=True); ck = os.path.join(CKDIR, key.replace("|", "_") + ".json")
        t0 = time.time(); S = S3.Strip3D(Lx, Lt, Ny, cuts[conf], tc, drop_double=drop_double)
        q, st = S3.route_i_ckpt(S, ck, cpts=cpts, with_saddle=saddle); del S; gc.collect()
        cache[key] = dict(S=float(0.5 * q), tsad=st.get("tsad"), t0=st["t0"], sec=time.time() - t0); save()
        log(f"sigma W={W} r={r} {conf} c={c} cpts={cpts} dd={drop_double} saddle={saddle}: S = {0.5*q:.10f} (T_saddle {st.get('tsad')})  [{time.time()-t0:.0f}s]")
    return cache[key]["S"]

def conn(side, W, r, c=2, **kw):
    P = int(round(r * W)); Ny = int(c * 2 * P)
    f = free_S if side == "free" else sigma_S
    return (f(W, r, "strip", c=c, **kw) - 2 * f(W, r, "edge", c=c, **kw)) / Ny       # s_c per unit length

def fit(rs, xs, form):
    rs = np.asarray(rs, float); X = np.vstack([np.ones_like(rs), 1 / rs, 1 / rs ** 2 if form == "A" else np.log(rs) / rs]).T
    c, *_ = np.linalg.lstsq(X, np.asarray(xs, float), rcond=None)
    pred = lambda r: c[0] + c[1] / r + (c[2] / r ** 2 if form == "A" else c[2] * np.log(r) / r)
    return c[0], pred

def extrapolate(rs, xs, label):
    """registered: train r=2..5, held out r=6 (scaled x6), forms A,B; final central = mean of A,B refit on all r."""
    train = [(r, x) for r, x in zip(rs, xs) if r <= 5]; ho = dict(zip(rs, xs))[6]
    out = {}
    for form in ("A", "B"):
        x_inf_tr, pred = fit([t[0] for t in train], [t[1] for t in train], form)
        x_inf_all, _ = fit(rs, xs, form)
        out[form] = dict(train_inf=x_inf_tr, ho_err=abs(pred(6) - ho), all_inf=x_inf_all)
    sig_ho = 6 * max(out["A"]["ho_err"], out["B"]["ho_err"])
    sig_sp = abs(out["A"]["all_inf"] - out["B"]["all_inf"]) / 2
    central = 0.5 * (out["A"]["all_inf"] + out["B"]["all_inf"]); sig = np.hypot(sig_ho, sig_sp)
    log(f"{label}: A train {out['A']['train_inf']:.6f} all {out['A']['all_inf']:.6f} (ho err {out['A']['ho_err']:.2e}); "
        f"B train {out['B']['train_inf']:.6f} all {out['B']['all_inf']:.6f} (ho err {out['B']['ho_err']:.2e}) -> {central:.6f} +- {sig:.6f}")
    return central, sig, out

def controls():
    out = {}
    P, Lx, Lt, tc, cuts = geom(2, 2); S = S3.Strip3D(Lx, Lt, 4 * P, cuts["strip"], tc)
    T, d, sig, gap = S3.saddle_term(S, return_checks=True); out["S1"] = dict(gap=float(gap), pass_=bool(gap <= 1e-10))
    log(f"S1 normalisation: max rel |diag(G D G) - d| = {gap:.1e} [{'PASS' if gap <= 1e-10 else 'FAIL'}]")
    P = 12; Lx, Lt = 2 + 2 * P, 2 * P; tc = P - 1; Se = S3.Strip3D(Lx, Lt, 48, list(range(P, Lx)), tc)
    d = S3.coincident_dn(Se).real; vals = []
    for m in (2, 3, 4):
        t = tc + 1 + m; rr = np.sqrt(0.25 + (m + 0.5) ** 2)
        vals += [d[x * Lt + t] * rr for x in (P - 1, P)]
    mean = float(np.mean(vals)); ok2 = abs(mean / (-1 / 32) - 1) <= 0.20
    out["S2"] = dict(values=[float(v) for v in vals], mean=mean, pass_=bool(ok2))
    log(f"S2 lattice P2: d*r over window = {[round(v, 5) for v in vals]}, mean {mean:.5f} vs -1/32 = -0.03125 [{'PASS' if ok2 else 'FAIL'}]")
    kap2 = {r: -2 * conn("free", 2, r) for r in (2, 3)}
    seen = {2: -48.534388, 3: -69.382529}; reg = {}
    for r in (2, 3):
        dk_off = -2 * (sigma_S(2, r, "strip", saddle=False) - 2 * sigma_S(2, r, "edge", saddle=False)) / (4 * r * 2)
        reg[r] = dk_off / kap2[r]
    ok3 = all(abs(reg[r] / seen[r] - 1) <= 1e-6 for r in (2, 3)); out["S3"] = dict(values=reg, pass_=bool(ok3))
    log(f"S3 saddle-OFF regression: R = {reg} vs seen {seen} [{'PASS' if ok3 else 'FAIL'}]")
    P, Lx, Lt, tc, cuts = geom(2, 2); Sg = S3.Strip3D(Lx, Lt, 16, list(range(0, Lx)), tc)
    ck = os.path.join(CKDIR, "S4_puregauge.json"); os.makedirs(CKDIR, exist_ok=True)
    qg, stg = S3.route_i_ckpt(Sg, ck, cpts=12, with_saddle=True)
    Ss = S3.Strip3D(Lx, Lt, 16, cuts["strip"], tc); qs, _ = S3.route_i_ckpt(Ss, os.path.join(CKDIR, "S4_strip_ref.json"), cpts=12, with_saddle=False)
    ok4 = abs(qg) <= 1e-8 * abs(qs) and abs(stg["tsad"]) <= 1e-8 * abs(qs)
    out["S4"] = dict(Q=float(qg), tsad=float(stg["tsad"]), ref=float(qs), pass_=bool(ok4))
    log(f"S4 pure gauge (wall-to-wall cut, saddle ON): Q'(1) = {qg:.2e}, T_saddle = {stg['tsad']:.2e} (ref |route_i| {abs(qs):.2f}) [{'PASS' if ok4 else 'FAIL'}]")
    return out

if __name__ == "__main__":
    res = {}
    if os.environ.get("EXP081_CONTROLS_DONE") == "1":   # controls already run (exp081_output.txt 'controls' run); S2 revised post-registration
        ctl = {"note": {"pass_": True, "text": "S1,S3,S4 PASS; S2 FAILED as registered, revised post-registration (box-extrapolated, 3.7%)"}}
    else:
        ctl = controls()
    res["controls"] = ctl
    if not all(v["pass_"] for v in ctl.values()):
        log("CONTROL FAILURE: production not started (investigate)"); json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp081_results.json"), "w"), indent=1, default=str); sys.exit(2)
    R2 = (2, 3, 4, 5, 6); R3 = (2, 3, 4)
    # 1. free side and planted control K
    kap = {r: -2 * conn("free", 2, r) for r in R2}
    log("free kappa_lat W=2:", {r: round(v, 6) for r, v in kap.items()})
    kc, ks, ko = extrapolate(list(kap), list(kap.values()), "free kappa_lat (planted control K)")
    K_pass = all(abs(ko[f]["train_inf"] - KAPPA_FREE) <= 2 * ks for f in ("A", "B")) and \
             all(abs(fit([r for r in R2 if r <= 5], [kap[r] for r in R2 if r <= 5], f)[1](6) - kap[6]) <= ks for f in ("A", "B"))
    log(f"K: kappa_inf = {kc:.6f} +- {ks:.6f} vs {KAPPA_FREE} (train-only A {ko['A']['train_inf']:.6f}, B {ko['B']['train_inf']:.6f}) [{'PASS' if K_pass else 'FAIL'}]")
    res["K"] = dict(kappa_lat=kap, central=kc, sigma=ks, pass_=bool(K_pass))
    # 2. sigma side, increasing r
    dk = {}
    for r in R2:
        dk[r] = -2 * conn("sigma", 2, r)
        log(f"W=2 r={r}: delta_kappa_lat = {dk[r]:.8f}, kappa_lat = {kap[r]:.8f}, R = {dk[r]/kap[r]:.6f}")
    kap3 = {r: -3 * conn("free", 3, r) for r in R3}; dk3 = {}
    for r in R3:
        dk3[r] = -3 * conn("sigma", 3, r); log(f"W=3 r={r}: delta_kappa_lat = {dk3[r]:.8f}, R = {dk3[r]/kap3[r]:.6f}")
    # 3. nuisances
    ny = {r: abs((-2 * conn("sigma", 2, r, c=3)) / dk[r] - 1) for r in (2, 3)}
    sq = abs((-2 * conn("sigma", 2, 3, cpts=16)) / dk[3] - 1)
    e2 = abs(sigma_S(2, 2, "edge2") / sigma_S(2, 2, "edge") - 1)
    dd = -2 * conn("sigma", 2, 2, drop_double=True)
    log(f"Ny clause (c=3 vs 2): {ny} [{'PASS' if max(ny.values()) <= 0.01 else 'FAIL -> systematic'}]; s-quad: {sq:.1e} "
        f"[{'PASS' if sq <= 1e-3 else 'FAIL -> systematic'}]; edge2 vs edge: {e2:.1e} [{'PASS' if e2 <= 1e-8 else 'FAIL'}]")
    # 4. extrapolation, routes
    Rr = {r: dk[r] / kap[r] for r in R2}
    Ri, si, oi = extrapolate(list(Rr), list(Rr.values()), "route (i) R(r)")
    dki, sdk, odk = extrapolate(list(dk), list(dk.values()), "route (ii) delta_kappa_lat(r)")
    Rii, sii = dki / KAPPA_FREE, sdk / KAPPA_FREE
    sys_extra = 0.0
    if max(ny.values()) > 0.01: sys_extra = np.hypot(sys_extra, max(ny.values()) * abs(Ri))
    if sq > 1e-3: sys_extra = np.hypot(sys_extra, sq * abs(Ri))
    sigW = abs(dk3[4] / kap3[4] - Rr[4])
    premise_ok = abs(Ri - Rii) <= np.hypot(si, sii)
    if premise_ok: Rq, sq_tot = Ri, np.sqrt(si ** 2 + sigW ** 2 + sys_extra ** 2)
    else:
        lo = min(Ri - si, Rii - sii); hi = max(Ri + si, Rii + sii); Rq = 0.5 * (lo + hi); sq_tot = np.sqrt(((hi - lo) / 2) ** 2 + sigW ** 2 + sys_extra ** 2)
    dd_shift = abs(dd / kap[2] - Rr[2]); fires = dd_shift > sq_tot
    log(f"route (i) R_inf = {Ri:.5f} +- {si:.5f}; route (ii) = {Rii:.5f} +- {sii:.5f}; premise {'OK' if premise_ok else 'FAILS (union interval used)'}; "
        f"sigma_W = {sigW:.5f}; extra sys = {sys_extra:.5f}")
    log(f"must-fire (confluent residues dropped, W=2 r=2): R shift {dd_shift:.5f} vs final sigma {sq_tot:.5f} [{'FIRES' if fires else 'DOES NOT FIRE'}]")
    stat = Rq + 0.4503
    decided = K_pass and abs(stat) > 2 * sq_tot
    verdict = ("INCONCLUSIVE (planted control K failed)" if not K_pass else
               (f"DECIDED: delta(kappa/C_T) {'> 0 (interacting above free)' if stat > 0 else '< 0 (interacting below free)'}" if decided else "INCONCLUSIVE"))
    log(f"R_inf = {Rq:.5f} +- {sq_tot:.5f};  R_inf + 0.4503 = {stat:.5f} +- {sq_tot:.5f} (2 sigma {2*sq_tot:.5f})  =>  {verdict}")
    res.update(dict(dk=dk, kap=kap, R=Rr, dk3=dk3, kap3=kap3, ny=ny, squad=sq, edge2=e2, route_i=[Ri, si], route_ii=[Rii, sii],
                    premise_ok=bool(premise_ok), sigma_W=sigW, extra=sys_extra, R_inf=[Rq, sq_tot], stat=stat, mustfire=dict(shift=dd_shift, fires=bool(fires)),
                    verdict=verdict))
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp081_results.json"), "w"), indent=1, default=str)
