"""EXP-085w (registered 1272d17 + pre-run note: tail = poles in (3, 6], s > 6 remainder separate; family prediction at W < Wbox): W4P4 test-(i) diagnosis. H1 = s_cut truncation tail. Usage: exp085w_diag.py W P [plant_site]
Phase-D code copied verbatim from exp085_run.py so the KA reproduces D.json bitwise. Writes exp081d_results/exp085w/W{W}P{P}.json. [model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
OUT = os.path.join(HERE, "exp081d_results", "exp085w"); os.makedirs(OUT, exist_ok=True)
W, P = int(sys.argv[1]), int(sys.argv[2]); PLANT = int(sys.argv[3]) if len(sys.argv) > 3 else None; FAIL = []; T0 = time.time()
def check(nm, ok, det=""):
    print(f"{nm:62s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def build(W, P):                                                    # verbatim from exp085_run.py
    Wb = P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
    ck = None
    for d in ("exp081d_results", "exp081c_results"):
        f = os.path.join(HERE, d, f"sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0_ckpt.json")
        if os.path.exists(f): ck = json.load(open(f)); break
    lowrank = ck is not None and "ranks" in ck
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); U = C.install(S, refine="auto", lowrank=lowrank, rank_drop=0)
    return S, U, ck, lowrank
def d_radius(S, U, f):                                              # verbatim from exp085_run.py
    cache = {}
    for p, u in U.items():
        for j, sj in enumerate(u.s):
            if sj > S.s_cut: continue
            r = f * min(1e-6, 0.3 * min([abs(sj - sk) for sk in u.s if sk != sj] + [1.0]))
            cache[(p, j)] = (np.diag(u.residue(1j * sj, r)), np.diag(u.residue(-1j * sj, r)))
    d = np.zeros(S.N, dtype=complex); Ny = S.Ny
    for q in range(Ny):
        p = q if q <= Ny // 2 else Ny - q; u = U[p]
        for j, sj in enumerate(u.s):
            if sj > S.s_cut: continue
            dp, dm = cache[(p, j)]
            d += (2j * np.pi) * u.scale * dp * S3._kdn(1j * sj, True) + (2j * np.pi) * u.scale * dm * S3._kdn(-1j * sj, False)
    return d / Ny
def per_slice_dB(S, lo_s, hi_s):                                    # coincident_dn_c's formula per slice, poles with lo_s < s <= hi_s
    out = []
    for sp in S.sl:
        d = np.zeros(S.N, dtype=complex)
        for j, sj in enumerate(sp.s):
            if not (lo_s < sj <= hi_s): continue
            for R, a0, up in ((sp.Rp[j], 1j * sj, True), (sp.Rm[j], -1j * sj, False)):
                d += (2j * np.pi) * np.diag(sp.Rfull(R)) * S3._kdn(a0, up)
        out.append(d / S.Ny)
    return np.array(out)
S, U, ck, lr = build(W, P); Ny, N, Lt = S.Ny, S.N, S.Lt
print(f"W{W}P{P}: Lx {S.Lx} Lt {Lt} Ny {Ny} N {N} cut x {S.cutx} lowrank {lr}  ({time.time()-T0:.0f}s)", flush=True)
# ---- phase D, verbatim ----
dB = C.coincident_dn_c(S); dB_alt = [d_radius(S, U, f) for f in (2.0, 0.5)]; s_dB = max(np.abs(a - dB).max() for a in dB_alt)
G0d = np.mean([np.diag(sl.G0) for sl in S.sl], axis=0)
def dG(b): return np.mean([np.diag(sl.G(b)) - np.diag(sl.G0) for sl in S.sl], axis=0)
dC16 = S3.C_line(dG, npt=16); dC24 = S3.C_line(dG, npt=24); s_dC = np.abs(dC24 - dC16).max()
B1 = S.B1(); B1d = np.array([np.diag(B1[k]) for k in range(Ny)])
dB0 = S.inner_beta0(1.0, dn=True); dB0d = np.mean([np.diag(dB0[k]) for k in range(Ny)], axis=0); del dB0
def Bd(npt): return lambda b: np.mean([np.diag(m) for m in S.inner(1.0, b, npt)], axis=0) - B1d.mean(axis=0)
D16 = dB0d + S3.C_line(Bd(40), npt=16); D24 = dB0d + S3.C_line(Bd(60), npt=24)
GA16 = D16 / (4 * G0d); GA24 = D24 / (4 * G0d); s_GA = np.abs(GA24 - GA16).max()
iG = np.abs(dC16 - dB).max(); iB = np.abs(GA16 - dB).max(); tolG, tolB = 10 * (s_dB + s_dC), 10 * (s_dB + s_GA)
print(f"phase D recomputed: iG {iG!r} (tol {tolG:.2e})  iB {iB!r} (tol {tolB:.2e})  ({time.time()-T0:.0f}s)", flush=True)
ref = json.load(open(os.path.join(HERE, "exp081d_results", "exp085", "D.json"))).get(str(W)) if P == 4 else None
if ref: check(f"KA W{W}P{P}: iG, iB reproduce D.json bitwise", iG == ref["iG"] and iB == ref["iB"], f"iG {iG!r} vs {ref['iG']!r}; iB {iB!r} vs {ref['iB']!r}")
# ---- H1: tail ----
lo, hi, rem = per_slice_dB(S, -np.inf, S.s_cut), per_slice_dB(S, S.s_cut, 6.0), per_slice_dB(S, 6.0, np.inf)   # pre-run note: tail = (3, 6]
check("control: per-slice d^B (s<=s_cut) sums to coincident_dn_c", np.abs(lo.sum(0) - dB).max() <= 1e-15 * max(1, np.abs(dB).max()), f"{np.abs(lo.sum(0) - dB).max():.1e}")
tail = hi.sum(0); tmax = float(np.abs(tail).max()); rmax = float(np.abs(rem.sum(0)).max())
print(f"s > 6 remainder (size only): max {rmax:.3e}", flush=True)
if W < P: check(f"family prediction (W < Wbox): |tail(3,6]| <= tolG", tmax <= tolG, f"{tmax:.3e} vs {tolG:.2e}")
h1G = float(np.abs((dC16 - dB) - tail).max()); h1B = float(np.abs((GA16 - dB) - tail).max())
print(f"tail: max|d^B_tail| {tmax:.3e}  (20x tolG = {20*tolG:.2e})", flush=True)
check(f"H1 (i-G): max|(d^C - d^B) - tail| <= tolG", h1G <= tolG, f"{h1G:.3e} vs {tolG:.2e}  (before: {iG:.3e})")
check(f"H1 (i-B): max|(G^A - d^B) - tail| <= tolB", h1B <= tolB, f"{h1B:.3e} vs {tolB:.2e}  (before: {iB:.3e})")
teeth = tmax > 20 * tolG; flip = float(np.abs((dC16 - dB) + tail).max())
if teeth: check("H1 must-fail: sign-flipped tail must FAIL", flip > tolG, f"{flip:.3e} vs {tolG:.2e}")
else: print(f"H1 must-fail NOT GRADED: |tail| {tmax:.2e} <= 20x tol (H1 has no teeth here); flipped {flip:.3e}", flush=True)
# ---- plant (c) ----
if PLANT is not None:
    dBp = dB.copy(); dBp[PLANT] += 5e-9; ip = float(np.abs(dC16 - dBp).max())
    check(f"plant (c): d^B[{PLANT}] += 5e-9 -> (i-G) must FAIL", ip > tolG, f"{ip:.3e} vs {tolG:.2e}")
# ---- descriptive (a)/(b) ----
mis = dC16 - dB; top = np.argsort(-np.abs(mis))[:5]
print("top-5 |d^C - d^B| sites (x, t): " + ", ".join(f"{i}=({i // Lt},{i % Lt}) {abs(mis[i]):.2e}" for i in top), flush=True)
dCp = np.array([S3.C_line(lambda b, sl=sl: (np.diag(sl.G(b)) - np.diag(sl.G0)) / Ny, npt=16) for sl in S.sl])
share = np.abs(dCp - lo).max(axis=1); print("per-slice max|d^C_p - d^B_p|: " + " ".join(f"p{p}:{v:.1e}" for p, v in enumerate(share)), flush=True)
poles = []
for p, sp in enumerate(S.sl):
    s = sorted(sp.s); gap = min([b - a for a, b in zip(s[:-1], s[1:])] + [np.inf]); near = [x for x in s if 3 < x < 4]
    poles.append(dict(p=p, n=len(s), near_3to4=near, min_gap=gap, min_dist_scut=min([abs(x - 3.0) for x in s] + [np.inf])))
    if near or gap < 1e-4: print(f"   p{p}: poles in (3,4) {['%.6f' % x for x in near]}  min gap {gap:.2e}  min|s-3| {poles[-1]['min_dist_scut']:.2e}", flush=True)
cond = float(np.linalg.cond(B1[0])); print(f"cond(B1[0]) = {cond:.3e}", flush=True)
json.dump(dict(W=W, P=P, iG=iG, iB=iB, tolG=tolG, tolB=tolB, s_dB=s_dB, s_dC=s_dC, s_GA=s_GA, tail_max=tmax, rem6_max=rmax, h1G=h1G, h1B=h1B, teeth=teeth, flip=flip,
               top5=[[int(i), int(i // Lt), int(i % Lt), float(abs(mis[i]))] for i in top], slice_share=share.tolist(), poles=poles, condB10=cond,
               failed=FAIL, sec=time.time() - T0), open(os.path.join(OUT, f"W{W}P{P}.json"), "w"), indent=1, default=float)
print(f"\nEXP-085w W{W}P{P}: {'controls PASS' if not FAIL else 'FAIL: ' + ', '.join(FAIL)}  ({time.time()-T0:.0f}s)"); sys.exit(1 if FAIL else 0)
