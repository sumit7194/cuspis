"""EXP-085w2a (registration notes/EXP-085w2_registration.md): phase D at W4P4 with Strip3D s_cut = 6 (the ONE variable; was 3).
Controls: (1) d^C bitwise identical at s_cut 3 and 6 (d^C does not use s_cut); (2) d^B(6) - d^B(3) == 085w on-demand tail(3,6] within s_dB
(two implementations: install residues vs on-demand residues); (3) plant (c) 5e-9 at site 18 must FAIL (i-G). Prediction: (i-G) <= tolG, (i-B) <= tolB.
Phase-D code verbatim from exp085_run.py. [model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
OUT = os.path.join(HERE, "exp081d_results", "exp085w"); os.makedirs(OUT, exist_ok=True)
W, P, SITE = 4, 4, 18; FAIL = []; T0 = time.time()
def check(nm, ok, det=""):
    print(f"{nm:66s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def build(W, P, s_cut):                                             # exp085_run.build with s_cut as the one variable
    Wb = P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
    f = os.path.join(HERE, "exp081d_results", f"sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0_ckpt.json")
    ck = json.load(open(f)) if os.path.exists(f) else None; lowrank = ck is not None and "ranks" in ck
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=s_cut); U = C.install(S, refine="auto", lowrank=lowrank, rank_drop=0)
    return S, U, lowrank
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
def tail_on_demand(S, lo_s, hi_s):                                  # verbatim logic of exp085w_diag.per_slice_dB, summed
    d = np.zeros(S.N, dtype=complex)
    for sp in S.sl:
        for j, sj in enumerate(sp.s):
            if not (lo_s < sj <= hi_s): continue
            r = min(1e-6, 0.3 * min([abs(sj - sk) for sk in sp.s if sk != sj] + [1.0]))
            for a0, up in ((1j * sj, True), (-1j * sj, False)): d += (2j * np.pi) * sp.scale * np.diag(sp.residue(a0, r)) * S3._kdn(a0, up)
    return d / S.Ny
def dC_of(S):
    def dG(b): return np.mean([np.diag(sl.G(b)) - np.diag(sl.G0) for sl in S.sl], axis=0)
    return S3.C_line(dG, npt=16), S3.C_line(dG, npt=24)
# ---- s_cut = 3 (cheap pieces only) ----
S3c, U3, lr = build(W, P, 3.0); dB3 = C.coincident_dn_c(S3c); dC3, _ = dC_of(S3c); tail3 = tail_on_demand(S3c, 3.0, 6.0)
print(f"s_cut 3 pieces done ({time.time()-T0:.0f}s); lowrank {lr}", flush=True); del S3c, U3
# ---- s_cut = 6: full phase D, verbatim ----
S, U, _ = build(W, P, 6.0); Ny = S.Ny
dB = C.coincident_dn_c(S); dB_alt = [d_radius(S, U, f) for f in (2.0, 0.5)]; s_dB = max(np.abs(a - dB).max() for a in dB_alt)
G0d = np.mean([np.diag(sl.G0) for sl in S.sl], axis=0)
dC16, dC24 = dC_of(S); s_dC = np.abs(dC24 - dC16).max()
check("control 1: d^C bitwise identical at s_cut 3 and 6", np.array_equal(dC16, dC3), f"max diff {np.abs(dC16 - dC3).max():.1e}")
dtail = float(np.abs((dB - dB3) - tail3).max())
check("control 2: d^B(6) - d^B(3) == on-demand tail(3,6] within s_dB", dtail <= max(s_dB, 1e-15), f"{dtail:.2e} vs s_dB {s_dB:.1e} (|tail| {np.abs(tail3).max():.2e})")
if os.environ.get("TIER1"): print(f"TIER1 exit before inner ({time.time()-T0:.0f}s)"); sys.exit(0)
B1 = S.B1(); B1d = np.array([np.diag(B1[k]) for k in range(Ny)])
dB0 = S.inner_beta0(1.0, dn=True); dB0d = np.mean([np.diag(dB0[k]) for k in range(Ny)], axis=0); del dB0
def Bd(npt): return lambda b: np.mean([np.diag(m) for m in S.inner(1.0, b, npt)], axis=0) - B1d.mean(axis=0)
D16 = dB0d + S3.C_line(Bd(40), npt=16); D24 = dB0d + S3.C_line(Bd(60), npt=24)
GA16 = D16 / (4 * G0d); GA24 = D24 / (4 * G0d); s_GA = np.abs(GA24 - GA16).max()
iG = float(np.abs(dC16 - dB).max()); iB = float(np.abs(GA16 - dB).max()); tolG, tolB = 10 * (s_dB + s_dC), 10 * (s_dB + s_GA)
dBp = dB.copy(); dBp[SITE] += 5e-9; ip = float(np.abs(dC16 - dBp).max())
check(f"plant (c): d^B[{SITE}] += 5e-9 -> (i-G) must FAIL", ip > tolG, f"{ip:.3e} vs {tolG:.2e}")
check("PREDICTION (i-G) at s_cut 6: max|d^C - d^B| <= tolG", iG <= tolG, f"{iG:.3e} vs {tolG:.2e}  (s_cut 3: 5.785e-09)")
check("PREDICTION (i-B) at s_cut 6: max|G^A - d^B| <= tolB", iB <= tolB, f"{iB:.3e} vs {tolB:.2e}  (s_cut 3: 3.367e-09)")
json.dump(dict(iG=iG, iB=iB, tolG=tolG, tolB=tolB, s_dB=s_dB, s_dC=s_dC, s_GA=s_GA, ctrl2=dtail, plant=ip, failed=FAIL, sec=time.time() - T0),
          open(os.path.join(OUT, "W4P4_scut6.json"), "w"), indent=1, default=float)
ctrl = [f for f in FAIL if not f.startswith("PREDICTION")]
print(f"\nEXP-085w2a: controls {'PASS' if not ctrl else 'FAIL: ' + ', '.join(ctrl)}; predictions {'PASS' if not any(f.startswith('PREDICTION') for f in FAIL) else 'FAIL'}  ({time.time()-T0:.0f}s)")
sys.exit(1 if FAIL else 0)
