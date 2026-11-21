"""EXP-081c route (registered 8fcfb84): one geometry per process, 081c numerics (exp081c_numerics, refine = 1).
Usage: python exp081c_route.py W P Wbox mode      mode = "posctl" (positive control vs 081b) | "target" (W8P8 + checks)
Production: t0 (inner_beta0, dn), T_saddle (full-matrix residue diagonals), g at the 48 C-nodes of route_b (cpts 12,
panels 0-0.5-1.5-3-6, npt 40); checkpointed in exp081c_results/<tag>_ckpt.json.
posctl: compare with the EXP-081b checkpoint of the same geometry: per-node impact |dg| pi/cosh^2(pi s) <= 1e-7,
        |dt0|, |dtsad| <= 2e-6, |dS| <= 1e-6 (S = (t0 + tsad + sum_all-nodes wt g)/2).
target: N1'''c arms at the 5 checkpoint nodes nearest s = 1..5 (unrefined G and unrefined residues), t0 refined vs
        unrefined (<= 2e-6), residues refined vs unrefined (<= 1e-8 rel), planted must-fire (eps = 1.2e-9 on G and
        residues at s = 0.937.., predicted dg = 2 eps N Ny, 10% match), B2b (refine 2 vs 1 at s = 1.974.., <= 1e-12 rel),
        Woodbury must-fire (081b stored g at the checkpoint nodes; reported only). [model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
W, P, Wb = (int(a) for a in sys.argv[1:4]); mode = sys.argv[4]
OUT = os.path.join(HERE, "exp081c_results"); os.makedirs(OUT, exist_ok=True)
tag = f"sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0"; ck = os.path.join(OUT, tag + "_ckpt.json")
st = json.load(open(ck)) if os.path.exists(ck) else {}
def put(k, v):
    st[k] = v; tmp = ck + ".tmp"; json.dump(st, open(tmp, "w")); os.replace(tmp, ck)
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)
Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
def geom(refine):
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); U = C.install(S, refine=refine); return S, U
x, w = np.polynomial.legendre.leggauss(12); NODES = []
for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
    for xi, wi in zip(x, w):
        si = 0.5 * (hi - lo) * (xi + 1) + lo; NODES.append((si, 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2))
NODES.sort(); CHK = [min(NODES, key=lambda n: abs(n[0] - t))[0] for t in (1, 2, 3, 4, 5)]
key = lambda s: f"g|{s:.15f}"

# ---------------- production ----------------
need = ("t0" not in st) or ("tsad" not in st) or any(key(s) not in st for s, _ in NODES)
if need:
    S, U = geom(1); log(f"{tag}: 081c numerics installed (refine 1, {len(U)} unique slices, residues by contour)")
    B1 = S.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]
    if "t0" not in st: put("t0", C.t0_term(S, B1)); log(f"t0 {st['t0']:+.12f}")
    if "tsad" not in st: put("tsad", C.saddle_term_c(S, B1)); log(f"tsad {st['tsad']:+.12f}")
    for s, _ in NODES:
        if key(s) not in st: put(key(s), C.g_node(S, s, ld1)); log(f"g({s:.4f}) done")
    del S, U, B1
Sval = 0.5 * (st["t0"] + st["tsad"] + sum(wt * st[key(s)] for s, wt in NODES))
log(f"{tag}: production complete; S (all nodes) computed")

if mode == "posctl":
    ref = json.load(open(os.path.join(HERE, "exp081b_results", tag + "_ckpt.json")))
    imp = max(abs(st[key(s)] - ref[key(s)][0]) * np.pi / np.cosh(np.pi * s) ** 2 for s, _ in NODES)
    worst_node = max(NODES, key=lambda n: abs(st[key(n[0])] - ref[key(n[0])][0]) * np.pi / np.cosh(np.pi * n[0]) ** 2)[0]
    dt0, dts = abs(st["t0"] - ref["t0"]), abs(st["tsad"] - ref["tsad"])
    Sref = 0.5 * (ref["t0"] + ref["tsad"] + sum(wt * ref[key(s)][0] for s, wt in NODES)); dS = abs(Sval - Sref)
    ok = imp <= 1e-7 and dt0 <= 2e-6 and dts <= 2e-6 and dS <= 1e-6
    res = dict(max_node_impact=imp, worst_node=worst_node, dt0=dt0, dtsad=dts, dS=dS, pass_=bool(ok), aliasing=True)
    put("posctl", res)
    log(f"POSITIVE CONTROL {tag} (mirror aliasing ON) vs EXP-081b: max node impact {imp:.1e} (at s={worst_node:.3f}), "
        f"|dt0| {dt0:.1e}, |dtsad| {dts:.1e}, |dS| {dS:.1e} -> {'PASS' if ok else 'FAIL -> STOP'}")
    sys.exit(0 if ok else 3)

# ---------------- target checks (W8P8) ----------------
if "planted" not in st:
    S, U = geom(1); B1 = S.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]; eps = 1.2e-9; s1 = CHK[0]
    for sl in U.values(): sl.scale = 1.0 + eps
    gp = C.g_node(S, s1, ld1); dg = gp - st[key(s1)]; pred = 2 * eps * S.N * Ny
    impact = abs(dg) * np.pi / np.cosh(np.pi * s1) ** 2
    put("planted", dict(s=s1, dg=dg, pred=pred, impact=impact, fires=bool(impact > 1e-7), match=bool(abs(dg / pred - 1) <= 0.1)))
    log(f"planted must-fire at s={s1:.4f}: dg {dg:.4e} (pred {pred:.4e}, ratio {dg/pred:.4f}), impact {impact:.2e} -> "
        f"{'FIRES' if impact > 1e-7 else 'DOES NOT FIRE'}, match {'OK' if abs(dg/pred-1) <= 0.1 else 'FAIL'}")
    if "b2b" not in st:
        S2, U2 = geom(2); B12 = S2.B1(); ld12 = [S3.logdet(B12[k]) for k in range(Ny)]
        g2 = C.g_node(S2, CHK[1], ld12); rel = abs(g2 - st[key(CHK[1])]) / abs(g2)
        put("b2b", dict(s=CHK[1], g_refine2=g2, rel=rel, pass_=bool(rel <= 1e-12))); log(f"B2b at s={CHK[1]:.4f}: refine 2 vs 1 rel {rel:.1e} -> {'PASS' if rel <= 1e-12 else 'FAIL'}")
        del S2, U2, B12
    del S, U, B1
if "n1c" not in st:
    S0, U0 = geom(0); B1 = S0.B1(); ld1 = [S3.logdet(B1[k]) for k in range(Ny)]
    rres = 0.0                                                    # residues: refined (recomputed per slice) vs unrefined
    for p, sl in U0.items():
        for j, sj in enumerate(sl.s):
            if sj > 3.0: continue
            r = min(1e-6, 0.3 * min([abs(sj - sk) for sk in sl.s if sk != sj] + [1.0]))
            sl.refine = 1; Rr = sl.residue(1j * sj, r); sl.refine = 0
            rres = max(rres, np.abs(Rr - sl.Rp[j]).max() / np.abs(Rr).max())
    t0u = C.t0_term(S0, B1); arms = {}
    for s in CHK: arms[f"{s:.15f}"] = C.g_node(S0, s, ld1); log(f"N1'''c unrefined arm g({s:.4f}) done")
    put("n1c", dict(arms=arms, t0_unref=t0u, residue_rel=rres)); del S0, U0, B1
n1 = st["n1c"]; rows = []
for s in CHK:
    d = abs(st[key(s)] - n1["arms"][f"{s:.15f}"]); rows.append((s, d, d * np.pi / np.cosh(np.pi * s) ** 2))
wb = json.load(open(os.path.join(HERE, "exp081b_results", tag + "_ckpt.json")))
wrows = [(s, abs(st[key(s)] - wb[key(s)][0]) * np.pi / np.cosh(np.pi * s) ** 2) for s in CHK]
summary = dict(n1c_rows=rows, t0_check=abs(st["t0"] - n1["t0_unref"]), residue_rel=n1["residue_rel"],
               woodbury_mustfire=wrows, woodbury_fires=bool(max(r[1] for r in wrows) > 1e-7), S=Sval)
put("summary", summary)
log("N1'''c (refined vs unrefined): " + "; ".join(f"s={s:.3f} |dg| {d:.1e} impact {i:.1e}" for s, d, i in rows))
log(f"t0 refined vs unrefined |dt0| {summary['t0_check']:.1e} [{'PASS' if summary['t0_check'] <= 2e-6 else 'FAIL'}]; "
    f"residues rel {n1['residue_rel']:.1e} [{'PASS' if n1['residue_rel'] <= 1e-8 else 'FAIL'}]")
log("Woodbury must-fire (081b stored g vs 081c): " + "; ".join(f"s={s:.3f} impact {i:.1e}" for s, i in wrows) +
    f" -> {'FIRES' if summary['woodbury_fires'] else 'does not fire (reported only)'}")
