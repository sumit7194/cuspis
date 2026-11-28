"""EXP-081d route (registration: report.md "EXP-081d ... REGISTRATION"). One geometry per process, 081c numerics (exact integer H,
adaptive refinement with divergence guard, R1 tiers) with LOW-RANK residues (exp081c_numerics lowrank=True; control: low-rank vs full
at k = 1, 2). Production: t0 (inner_beta0, dn), T_sad (full-matrix residue diagonals; linear-solve sigdot, option (a)), g at the 48
C-nodes of route_b (cpts 12, panels 0-0.5-1.5-3-6, npt 40). Checkpointed in exp081d_results/<tag>_ckpt.json.
Reliability / must-fire checks (all geometries):
  N1'''c   : g at the 5 checkpoint nodes from UNREFINED G and unrefined residues; per-node impact |dg| pi/cosh^2(pi s) (081b rule)
  t0       : t0 refined vs unrefined, <= 2e-6
  residue  : graded by IMPACT (slip-13 rule): (1/2)|T_sad(unrefined residues) - T_sad| <= 1e-7 (S units); N1'''c covers g, t0 covers t0
  planted  : G and residues x (1 + eps_k) at the s = 0.937 node, eps_k = 1e-6 / (2 N Ny pi/cosh^2(pi s1)) so the predicted impact is
             1e-6 (10x threshold) at EVERY geometry; must fire and match the predicted dg = 2 eps N Ny within 10 %; guarded (plant_guard
             style) before the run: predicted dg >= 1e3 x the g precision 1e-12 |g|
  B2b      : converged vs converged + 1 extra step at s = 1.974, <= 1e-12 rel
  Woodbury : production sigma3d (081b numerics: inv(G0) + Woodbury) g at the 5 checkpoint nodes vs 081d; reported only
Usage: python exp081d_route.py W P Wbox [--full] [--rank-drop R] [--tag-suffix X]   [model: Opus 5.5]
EXP-100 COPY (exp100_route.py): geometry as arguments --gL --gR --hT --Ny (defaults = convention A: gL = P + (Wb - W)//2,
gR = 2P + Wb - gL - W, hT = P, Ny = 4P), tcut = hT - 1; any explicit geometry adds _gL.._gR.._hT.._Ny.. to the tag.
--probe: install + B1 + ONE g node, prints wall times only, reads/writes no checkpoint and prints no value."""
import sys, os, json, time, argparse, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
ap = argparse.ArgumentParser(); ap.add_argument("W", type=int); ap.add_argument("P", type=int); ap.add_argument("Wb", type=int)
ap.add_argument("--full", action="store_true", help="full-matrix residues (low-rank control arm)")
ap.add_argument("--rank-drop", type=int, default=0, help="planted low-rank truncation control")
ap.add_argument("--tag-suffix", default=""); ap.add_argument("--production-only", action="store_true")
ap.add_argument("--nodes", default=None, help="i:j subset of the 48 C-nodes (Stage-2 splitting); t0/tsad/checks only when i == 0")
for _g in ("--gL", "--gR", "--hT", "--Ny"): ap.add_argument(_g, type=int, default=None)
ap.add_argument("--probe", action="store_true")
a = ap.parse_args(); W, P, Wb = a.W, a.P, a.Wb
OUT = os.path.join(HERE, "exp081d_results"); os.makedirs(OUT, exist_ok=True)
gL = a.gL if a.gL is not None else P + (Wb - W) // 2; gR = a.gR if a.gR is not None else 2 * P + Wb - gL - W
hT = a.hT if a.hT is not None else P; NyA = a.Ny if a.Ny is not None else 4 * P
GEO = "" if all(v is None for v in (a.gL, a.gR, a.hT, a.Ny)) else f"_gL{gL}_gR{gR}_hT{hT}_Ny{NyA}"
tag = f"sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0" + ("_full" if a.full else "") + (f"_rd{a.rank_drop}" if a.rank_drop else "") + GEO + a.tag_suffix
ck = os.path.join(OUT, tag + "_ckpt.json"); st = json.load(open(ck)) if (os.path.exists(ck) and not a.probe) else {}
def put(k, v):
    st[k] = v; tmp = ck + ".tmp"; json.dump(st, open(tmp, "w")); os.replace(tmp, ck)
T0 = time.time()
def log(*x): print(f"[{time.time()-T0:7.0f}s]", *x, flush=True)
Lx, Lt = gL + W + gR, 2 * hT; x0 = gL; Ny = NyA; N = Lx * Lt; TC = hT - 1
LR = dict(lowrank=not a.full, rank_drop=a.rank_drop)
def geom(refine, extra=0, **kw):
    C.ExactSlice.reset_stats()
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), TC, s_cut=3.0); U = C.install(S, refine=refine, **dict(LR, **kw))
    for sl in U.values(): sl.extra = extra
    return S, U
def stats(): s_ = C.ExactSlice.STATS; return dict(calls=s_["calls"], unconverged=s_["unconverged"], maxsteps=s_["maxsteps"], hist={str(k): v for k, v in s_.get("hist", {}).items()}, bad=[str(b) for b in s_.get("bad", [])[:5]])
TIER = 2.986170475685039
x, w = np.polynomial.legendre.leggauss(12); NODES = []
for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
    for xi, wi in zip(x, w):
        si = 0.5 * (hi - lo) * (xi + 1) + lo; NODES.append((si, 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2))
NODES.sort(); CHK = [min(NODES, key=lambda n: abs(n[0] - t))[0] for t in (1, 2, 3, 4, 5)]
key = lambda s: f"g|{s:.15f}"
i0, i1 = (0, len(NODES)) if a.nodes is None else tuple(int(v) for v in a.nodes.split(":"))
MYNODES = NODES[i0:i1]; FIRST = (i0 == 0)
# ---- planted-eps guard (before any compute; plant_guard rule: the plant must change its input measurably at THIS geometry) ----
s1 = CHK[0]; EPS = 1e-6 / (2 * N * Ny * np.pi / np.cosh(np.pi * s1) ** 2); PRED = 2 * EPS * N * Ny
if FIRST and not a.production_only:
    from tools.plant_guard import check_scale_plant; check_scale_plant(EPS, N, Ny, s1)   # raises PlantInert if the plant cannot fire
    log(f"planted guard: eps {EPS:.3e}, predicted dg {PRED:.4e}, predicted impact {PRED*np.pi/np.cosh(np.pi*s1)**2:.2e} (10x 1e-7)")
if a.probe:
    t1 = time.time(); S, U = geom("auto"); ti = time.time() - t1; t2 = time.time(); B1 = S.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]; tb = time.time() - t2
    t3 = time.time(); _ = C.g_node(S, CHK[1], ld1); tg = time.time() - t3; del _
    print(f"PROBE {tag}: N {N} Ny {Ny} Lx {Lx} Lt {Lt}: install {ti:.1f} s, B1 {tb:.1f} s, one g node (s={CHK[1]:.3f}) {tg:.1f} s; value discarded", flush=True); sys.exit(0)
# ---------------- production ----------------
need = (FIRST and (("t0" not in st) or ("tsad" not in st))) or any(key(s) not in st for s, _ in MYNODES)
if need:
    t1 = time.time(); S, U = geom("auto"); put("stats|install", stats()); rk = [r for u in U.values() for r in u.ranks]
    put("ranks", dict(max=max(rk) if rk else 0, hist={str(r): rk.count(r) for r in sorted(set(rk))}))
    log(f"{tag}: N {N} Ny {Ny}; 081c numerics installed ({len(U)} unique slices, {'full' if a.full else 'low-rank'} residues"
        + (f", rank-drop {a.rank_drop}" if a.rank_drop else "") + f"; ranks {st['ranks']}) {stats()['calls']} G, unconverged {stats()['unconverged']} ({time.time()-t1:.0f}s)")
    if st["stats|install"]["unconverged"]: log("NON-CONVERGED G in residues -> STOP (R1)"); sys.exit(4)
    B1 = S.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]
    if FIRST:
        for nm, fn in (("t0", lambda: C.t0_term(S, B1)), ("tsad", lambda: C.saddle_term_c(S, B1))):
            if nm not in st:
                C.ExactSlice.reset_stats(); t1 = time.time(); put(nm, fn()); put(f"stats|{nm}", dict(stats(), sec=time.time() - t1))
                log(f"{nm} {st[nm]:+.12f}  G calls {st['stats|'+nm]['calls']} unconverged {st['stats|'+nm]['unconverged']} ({time.time()-t1:.0f}s)")
                if st[f"stats|{nm}"]["unconverged"]: log(f"NON-CONVERGED G in {nm} -> STOP (R1)"); sys.exit(4)
    for s, _ in MYNODES:
        if key(s) not in st:
            C.ExactSlice.reset_stats(); t1 = time.time(); put(key(s), C.g_node(S, s, ld1)); put(f"stats|{s:.15f}", dict(stats(), sec=time.time() - t1))
            sn = st[f"stats|{s:.15f}"]; log(f"g({s:.4f}) done: {sn['calls']} G, steps hist {sn['hist']}, unconverged {sn['unconverged']} ({sn['sec']:.0f}s)")
            if sn["unconverged"] and s < TIER: log(f"NON-CONVERGED G at s={s:.4f} < {TIER:.3f} -> STOP (R1)"); sys.exit(4)
    del S, U, B1
if a.production_only or not FIRST or a.nodes is not None and i1 < len(NODES): log("production part done"); sys.exit(0)
if any(key(s) not in st for s, _ in NODES): log("not all nodes present (split run): checks run after the last part"); sys.exit(0)
Sval = 0.5 * (st["t0"] + st["tsad"] + sum(wt * st[key(s)] for s, wt in NODES)); put("S_all", Sval)
log(f"{tag}: production complete; S (all nodes) {Sval:+.12f}")
# ---------------- reliability / must-fire checks ----------------
if "planted" not in st:
    S, U = geom("auto"); B1 = S.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]
    for sl in U.values(): sl.scale = 1.0 + EPS
    gp = C.g_node(S, s1, ld1); dg = gp - st[key(s1)]; impact = abs(dg) * np.pi / np.cosh(np.pi * s1) ** 2
    put("planted", dict(s=s1, eps=EPS, dg=dg, pred=PRED, impact=impact, fires=bool(impact > 1e-7), match=bool(abs(dg / PRED - 1) <= 0.1)))
    log(f"planted must-fire s={s1:.4f}: dg {dg:.4e} (pred {PRED:.4e}, ratio {dg/PRED:.4f}), impact {impact:.2e} -> "
        f"{'FIRES' if impact > 1e-7 else 'DOES NOT FIRE'}, match {'OK' if abs(dg/PRED-1) <= 0.1 else 'FAIL'}")
    del S, U, B1
if "b2b" not in st:
    S2, U2 = geom("auto", extra=1); B12 = S2.B1(); ld12 = [S3.logdet(B12[k]) for k in range(Ny)]
    g2 = C.g_node(S2, CHK[1], ld12); rel = abs(g2 - st[key(CHK[1])]) / abs(g2)
    put("b2b", dict(s=CHK[1], g_plus1=g2, rel=rel, pass_=bool(rel <= 1e-12))); log(f"B2b s={CHK[1]:.4f}: converged+1 vs converged rel {rel:.1e} -> {'PASS' if rel <= 1e-12 else 'FAIL'}")
    del S2, U2, B12
if "n1c" not in st:
    S0, U0 = geom(0); B1 = S0.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]
    t0u = C.t0_term(S0, B1); tsu = C.saddle_term_c(S0, B1); arms = {}
    for s in CHK: arms[f"{s:.15f}"] = C.g_node(S0, s, ld1); log(f"N1'''c unrefined arm g({s:.4f}) done")
    put("n1c", dict(arms=arms, t0_unref=t0u, tsad_unref_res=tsu)); del S0, U0, B1
if "woodbury" not in st:
    Sw = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), TC, s_cut=3.0); B1w = Sw.B1(); ldw = [S3.logdet(B1w[k]) for k in range(Ny)]
    put("woodbury", {f"{s:.15f}": C.g_node(Sw, s, ldw) for s in CHK}); del Sw, B1w
n1 = st["n1c"]; rows = [(s, abs(st[key(s)] - n1["arms"][f"{s:.15f}"]), abs(st[key(s)] - n1["arms"][f"{s:.15f}"]) * np.pi / np.cosh(np.pi * s) ** 2) for s in CHK]
wrows = [(s, abs(st[key(s)] - st["woodbury"][f"{s:.15f}"]) * np.pi / np.cosh(np.pi * s) ** 2) for s in CHK]
res_imp = 0.5 * abs(n1["tsad_unref_res"] - st["tsad"])
summary = dict(n1c_rows=rows, t0_check=abs(st["t0"] - n1["t0_unref"]), residue_impact=res_imp, residue_ok=bool(res_imp <= 1e-7),
               woodbury_mustfire=wrows, woodbury_fires=bool(max(r[1] for r in wrows) > 1e-7), S=Sval)
put("summary", summary)
log("N1'''c (refined vs unrefined): " + "; ".join(f"s={s:.3f} |dg| {d:.1e} impact {i:.1e}" for s, d, i in rows))
log(f"t0 refined vs unrefined |dt0| {summary['t0_check']:.1e} [{'PASS' if summary['t0_check'] <= 2e-6 else 'FAIL'}]; "
    f"residue impact (1/2)|T_sad(unref res) - T_sad| {res_imp:.1e} [{'PASS' if res_imp <= 1e-7 else 'FAIL'}]")
log("Woodbury must-fire (081b numerics g vs 081d): " + "; ".join(f"s={s:.3f} impact {i:.1e}" for s, i in wrows) +
    f" -> {'FIRES' if summary['woodbury_fires'] else 'does not fire (reported only)'}")
