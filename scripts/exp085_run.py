"""EXP-085 (registered 75f1513 + amendments 1, 2): is R's 1/a growth the missing O(N^0) critical-coupling counterterm?
Phases (registered order; any control failure exits 1 BEFORE the reading):
  A  lattice constant c: same-lattice FFT check, NORM-T0 (dense periodic), c n-sweep, KA-IR          (no geometry)
  B  normalisation: R-norm (stored S -> stored R_T0), planted (from stored kappa)                    (no geometry)
  C  Sigma-sigma-dot (3D sum) per Stage-1 geometry, residue radius x1, x2, x1/2; tsad reproduction    (geometry builds; ALONE)
  D  test (i-G) and (i-B) at k = 1                                                                    (geometry builds; ALONE)
  E  reading: R_corr, slope g, rho +- 2 sigma, must-fail (-c), zero (c = 0)
Usage: exp085_run.py [A|AB|ABC|ABCD|all]   (default all). Outputs exp081d_results/exp085/. [model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "exp081d_results", "exp085"); os.makedirs(OUT, exist_ok=True)
STAGES = sys.argv[1] if len(sys.argv) > 1 else "all"; STAGES = "ABCDE" if STAGES == "all" else STAGES
KS = [1, 1.5, 2, 2.5]
JD = json.load(open(os.path.join(HERE, "exp081d_results.json")))
FAIL = []
def check(name, ok, detail=""):
    print(f"{name:52s} {'PASS' if ok else 'FAIL'}  {detail}", flush=True)
    if not ok: FAIL.append(name)
def save(name, obj): json.dump(obj, open(os.path.join(OUT, name), "w"), indent=1, default=float)
def norm(k):                                       # R units per unit of Delta S (081d: R = -Delta S / (Ny (1/W1 - 1/W2) kappa))
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); Ny = 4 * P
    return 1.0 / (Ny * (1.0 / W1 - 1.0 / W2) * JD[str(k)]["kappa"])

# ======================= A: lattice constant c (same lattice as production) =======================
def Gk(n):
    k = 2 * np.pi * np.arange(n) / n; E = sum(np.meshgrid(*(2 - 2 * np.cos(k),) * 3, indexing="ij"))
    G = np.zeros_like(E); m = E > 1e-14; G[m] = 1.0 / E[m]; return G          # zero mode excluded (box IR)
def avgconv(A, B):                                 # <A(k) B(k+q)>_k for A even (A(k) = A(-k)); = fftn(ifftn(A) * ifftn(B)) (B real-space)
    return np.real(np.fft.fftn(np.fft.ifftn(A) * np.fft.ifftn(B)))
def T0_parts(n):
    G = Gk(n); Bq = 2 * avgconv(G, G); S2 = avgconv(G * G, G); G2m = np.mean(G * G)
    mask = np.ones_like(G, bool); mask[0, 0, 0] = False                         # q = 0 excluded (zero mode), consistent with G
    Binv = np.zeros_like(Bq); Binv[mask] = 1.0 / Bq[mask]
    c = -4 * np.mean(Binv * (S2 - G * G2m)); T0full = -4 * np.mean(Binv * S2); return c, T0full
if "A" in STAGES:
    # same-lattice check: FFT G = pseudo-inverse of the periodic stencil (diag 6, hops -1), 5 separations, n = 8, 12
    for n in (8, 12):
        V = n ** 3; L = np.zeros((V, V)); idx = lambda x, y, z: ((x % n) * n + (y % n)) * n + (z % n)
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    i = idx(x, y, z); L[i, i] = 6.0
                    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)): j = idx(x + dx, y + dy, z + dz); L[i, j] -= 1; L[j, i] -= 1
        Gp = np.linalg.pinv(L); g = np.real(np.fft.ifftn(Gk(n)))
        seps = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 1), (n // 2, 0, 1)]
        dev = max(abs(Gp[0, idx(*s)] - g[s]) / abs(Gp[0, idx(*s)]) for s in seps)
        check(f"A same-lattice FFT G vs pinv, n={n}", dev <= 1e-12, f"max rel dev {dev:.1e}")
    # NORM-T0: dense periodic n = 6: Tr(B^-1 dB[sigma-dot = 1]) production-style vs V * T0_FFT
    n = 6; V = n ** 3; L = np.zeros((V, V)); idx = lambda x, y, z: ((x % n) * n + (y % n)) * n + (z % n)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = idx(x, y, z); L[i, i] = 6.0
                for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)): j = idx(x + dx, y + dy, z + dz); L[i, j] -= 1; L[j, i] -= 1
    G = np.linalg.pinv(L); B = 2 * G * G; dB = 4 * G * (-(G @ G))                # delta G = -G sigma G with sigma = 1 on every site
    Bp = np.linalg.pinv(B, rcond=1e-12); dense = np.trace(Bp @ dB); fft = V * T0_parts(n)[1]
    check("A NORM-T0 dense Tr(B^-1 dB) vs V*T0_FFT (n=6)", abs(dense - fft) <= 1e-10 * abs(dense), f"dense {dense:.12e} fft {fft:.12e}")
    sweep = {}
    for n in (32, 48, 64, 96, 128):
        t = time.time(); c, T0f = T0_parts(n); sweep[n] = dict(c=c, T0full=T0f); print(f"   c(n={n}) = {c:+.12f}   T0full {T0f:+.6e}  ({time.time()-t:.1f}s)", flush=True)
    sig_c = abs(sweep[128]["c"] - sweep[96]["c"]); conv = sig_c <= 0.01 * abs(sweep[128]["c"])
    check("A c converged (|c128-c96| <= 1% |c|)", conv, f"c {sweep[128]['c']:+.10f} sigma_c {sig_c:.2e}")
    grows = all(abs(sweep[b]["T0full"]) > abs(sweep[a]["T0full"]) for a, b in ((32, 48), (48, 64), (64, 96), (96, 128)))
    check("A KA-IR: unsubtracted T0 grows with n", grows, str({n: f"{v['T0full']:.3e}" for n, v in sweep.items()}))
    save("A.json", dict(sweep=sweep, c=sweep[128]["c"], sigma_c=sig_c, converged=conv))
    if FAIL: print("PHASE A FAIL"); sys.exit(1)

# ======================= B: normalisation controls (stored inputs only) =======================
if "B" in STAGES:
    dev = max(abs(-(JD[str(k)]["S_W1"] - JD[str(k)]["S_W2"]) * norm(k) - JD[str(k)]["R_T0"]) / abs(JD[str(k)]["R_T0"]) for k in KS)
    check("B R-norm: stored S -> stored R_T0", dev <= 1e-12, f"max rel dev {dev:.1e}")
    def corr(k, c, dSig): return 0.5 * c * dSig * norm(k)      # R_corr - R  (registered sign +1/2 c; Sigma = 3D sum)
    exp_pl = 0.5 / (16 * 2 * (1 / 4 - 1 / 8) * JD["2"]["kappa"])  # amendment 1: from the stored kappa
    got = corr(2, 1.0, 1.0)
    check("B planted normalisation (dSig=1, c=1, k=2)", abs(got - exp_pl) <= 1e-12 * exp_pl, f"got {got!r} expected {exp_pl!r}")
    if FAIL: print("PHASE B FAIL"); sys.exit(1)

# ======================= C: Sigma-sigma-dot per geometry (production path) =======================
def build(W, P):
    import sigma3d as S3, exp081c_numerics as C
    Wb = P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
    ck = None
    for d in ("exp081d_results", "exp081c_results"):
        f = os.path.join(HERE, d, f"sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0_ckpt.json")
        if os.path.exists(f): ck = json.load(open(f)); break
    lowrank = ck is not None and "ranks" in ck                                   # 081d checkpoints carry ranks (low-rank residues)
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); U = C.install(S, refine="auto", lowrank=lowrank, rank_drop=0)
    return S, U, ck, lowrank
def d_radius(S, U, f):
    """coincident_dn_c with every residue recomputed at radius f * production radius (production: f = 1)."""
    import sigma3d as S3
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
if "C" in STAGES:
    import exp081c_numerics as C
    for k in KS:
        P = int(4 * k)
        for W in (int(2 * k), int(4 * k)):
            fn = os.path.join(OUT, f"C_W{W}P{P}.json")
            if os.path.exists(fn): continue
            t = time.time(); S, U, ck, lr = build(W, P); B1 = S.B1(); Ny = S.Ny
            d0 = C.coincident_dn_c(S); sig = np.linalg.solve(B1[0], 2 * d0); Sig3D = float(np.real(Ny * np.sum(sig)))
            tsad = C.saddle_term_c(S, B1); ref = None if ck is None else ck.get("tsad")
            rep = None if ref is None else abs(tsad - ref) / abs(ref)
            alt = {}
            for f in (2.0, 0.5):
                dd = d_radius(S, U, f); sg = np.linalg.solve(B1[0], 2 * dd); alt[f] = float(np.real(Ny * np.sum(sg)))
            sigma = max(abs(alt[f] - Sig3D) for f in alt)
            save(f"C_W{W}P{P}.json", dict(W=W, P=P, lowrank=lr, Sigma3D=Sig3D, Sigma_alt=alt, sigma=sigma, tsad=tsad, tsad_ref=ref, tsad_reldev=rep, sec=time.time() - t))
            check(f"C tsad reproduction W{W}P{P} (lowrank={lr})", rep is not None and rep <= 1e-9, f"rel dev {rep}")
            print(f"   Sigma-sigma-dot W{W}P{P}: computed (value withheld until phase E); radius spread {sigma:.2e}; {time.time()-t:.0f}s", flush=True)
            del S, U, B1
    if FAIL: print("PHASE C FAIL"); sys.exit(1)

# ======================= D: test (i-G), (i-B) at k = 1 =======================
if "D" in STAGES:
    import sigma3d as S3, exp081c_numerics as C
    res = {}
    for W in (2, 4):
        S, U, ck, lr = build(W, 4); Ny = S.Ny; N = S.N
        dB = C.coincident_dn_c(S); dB_alt = [d_radius(S, U, f) for f in (2.0, 0.5)]; s_dB = max(np.abs(a - dB).max() for a in dB_alt)
        G0d = np.mean([np.diag(sl.G0) for sl in S.sl], axis=0)
        def dG(b): return np.mean([np.diag(sl.G(b)) - np.diag(sl.G0) for sl in S.sl], axis=0)
        dC16 = S3.C_line(dG, npt=16); dC24 = S3.C_line(dG, npt=24); s_dC = np.abs(dC24 - dC16).max()
        B1 = S.B1(); B1d = np.array([np.diag(B1[k]) for k in range(Ny)])
        dB0 = S.inner_beta0(1.0, dn=True); dB0d = np.mean([np.diag(dB0[k]) for k in range(Ny)], axis=0); del dB0
        def Bd(npt): return lambda b: np.mean([np.diag(m) for m in S.inner(1.0, b, npt)], axis=0) - B1d.mean(axis=0)
        D16 = dB0d + S3.C_line(Bd(40), npt=16); D24 = dB0d + S3.C_line(Bd(60), npt=24)
        GA16 = D16 / (4 * G0d); GA24 = D24 / (4 * G0d); s_GA = np.abs(GA24 - GA16).max()
        iG = np.abs(dC16 - dB).max(); iB = np.abs(GA16 - dB).max()
        res[W] = dict(iG=iG, iB=iB, s_dB=s_dB, s_dC=s_dC, s_GA=s_GA, dmax=float(np.abs(dB).max()))
        check(f"D (i-G) W{W}P4: max|d^C - d^B| <= 10x(s_dB + s_dC)", iG <= 10 * (s_dB + s_dC), f"{iG:.2e} vs 10x({s_dB:.1e}+{s_dC:.1e}); max|d| {res[W]['dmax']:.2e}")
        check(f"D (i-B) W{W}P4: max|G^A - d^B| <= 10x(s_dB + s_GA)", iB <= 10 * (s_dB + s_GA), f"{iB:.2e} vs 10x({s_dB:.1e}+{s_GA:.1e})")
        del S, U, B1
    save("D.json", res)
    TEST_I_OK = not any(n.startswith("D ") for n in FAIL)
    FAIL[:] = [n for n in FAIL if not n.startswith("D ")]        # (i) mismatch is a registered OUTCOME (reading -> INCONCLUSIVE), not a control abort
    save("D_verdict.json", dict(consistent=TEST_I_OK))

# ======================= E: reading =======================
if "E" in STAGES:
    A = json.load(open(os.path.join(OUT, "A.json"))); c, sig_c = A["c"], A["sigma_c"]
    Dv = json.load(open(os.path.join(OUT, "D_verdict.json")))["consistent"]
    Cg = {(W, int(4 * k)): json.load(open(os.path.join(OUT, f"C_W{W}P{int(4*k)}.json"))) for k in KS for W in (int(2 * k), int(4 * k))}
    R = {k: JD[str(k)]["R_T0"] for k in KS}; ks = np.array(KS, float)
    graw = float(np.polyfit(ks, [R[k] for k in KS], 1)[0])
    def series(cc):
        out, sg = {}, {}
        for k in KS:
            W1, W2, P = int(2 * k), int(4 * k), int(4 * k); a, b = Cg[(W1, P)], Cg[(W2, P)]
            dS = a["Sigma3D"] - b["Sigma3D"]; s_dS = np.hypot(a["sigma"], b["sigma"])
            out[k] = R[k] + 0.5 * cc * dS * norm(k); sg[k] = 0.5 * norm(k) * np.hypot(cc * s_dS, sig_c * dS)
        return out, sg
    def slope_and_sigma(out, sg):
        y = np.array([out[k] for k in KS]); g, b0 = np.polyfit(ks, y, 1); Sxx = np.sum((ks - ks.mean()) ** 2)
        ssr = np.sum((y - (g * ks + b0)) ** 2); s_fit = np.sqrt(ssr / (len(ks) - 2) / Sxx)
        w = (ks - ks.mean()) / Sxx; s_prop = np.sqrt(np.sum((w * np.array([sg[k] for k in KS])) ** 2))
        return float(g), float(np.hypot(s_fit, s_prop))
    def band(rho, srho):
        lo, hi = rho - 2 * srho, rho + 2 * srho
        if hi <= 0.1: return "T54 supported"
        if lo > 0.1 and hi < 0.5: return "T54 partial"
        if lo >= 0.5: return "T54 refuted as sole cause"
        return "INCONCLUSIVE (interval straddles a band edge)"
    rows = {}
    for nm, cc in (("registered +c", c), ("MUST-FAIL -c", -c), ("zero c=0", 0.0)):
        out, sg = series(cc); g, sgg = slope_and_sigma(out, sg); rho, srho = abs(g) / graw, sgg / graw
        rows[nm] = dict(Rcorr=out, g=g, sigma_g=sgg, rho=rho, sigma_rho=srho, band=band(rho, srho))
        print(f"E {nm:14s}: R_corr {[round(out[k], 6) for k in KS]}  g {g:+.4f} +- {sgg:.4f}  rho {rho:.4f} +- {srho:.4f}  -> {rows[nm]['band']}", flush=True)
    check("E zero control reproduces g_raw", abs(rows["zero c=0"]["g"] - graw) <= 1e-12 * abs(graw), f"{rows['zero c=0']['g']!r} vs {graw!r}")
    mf = rows["MUST-FAIL -c"]["rho"] >= 1.0
    check("E MUST-FAIL: -c does not flatten (rho >= 1)", mf, f"rho {rows['MUST-FAIL -c']['rho']:.4f}")
    if not A["converged"]: reading = "INCONCLUSIVE (c unconverged)"
    elif not Dv: reading = "INCONCLUSIVE (test (i) mismatch)"
    elif rows["MUST-FAIL -c"]["band"] == "T54 supported" and rows["registered +c"]["band"] != "T54 supported": reading = "DERIVATION REFUTED (-c flattens, +c does not; sec 1.5)"
    else: reading = rows["registered +c"]["band"]
    print(f"\nEXP-085 READING: {reading}   (g_raw {graw:.6f}; c {c:+.10f} +- {sig_c:.1e}; 2 dof)")
    save("E.json", dict(reading=reading, rows=rows, graw=graw, c=c, sigma_c=sig_c, controls_failed=FAIL))
print(f"\nEXP-085 stages {STAGES}: {'controls PASS' if not FAIL else 'FAIL: ' + ', '.join(FAIL)}"); sys.exit(1 if FAIL else 0)
