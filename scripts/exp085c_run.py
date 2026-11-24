"""EXP-085c (registered f3fa752, notes/EXP-085c_registration.md): the counterterm under prescription A (PRIMARY).
Modes:  TORUS        KA-torus: position-space c_A on a periodic n^3 lattice (dense) == c_of_n(n) (FFT path, verbatim from exp085_a4), n = 8, 12
        SECTOR       KA-sector at W2P4: y-sector Lambda and term1 vs a dense 3D build; identity KA + planted break
        GEOM W P     per-geometry pieces (d, sigdot, Lambda, c_A, T_sad two ways) -> exp081d_results/exp085c/G_W{W}P{P}.json
        READ         reading (needs all 8 geometries) [model: Opus 5.5]
c_A(z) = N delta_A(1/g(z)) = -4 sum_{x,y} B1^-1(x,y) G1(x,y) G1(z,x) [G1(y,z) - G1(x,z)]  =  -4 term1(z) + 2 (B_0 Lambda)(z),
term1(z) = (G M G)(z,z) with M = B^-1 o G (3D), Lambda(x) = sum_y M(x,y).  In y-sectors (block circulant, even in Delta):
M_k = (1/Ny) sum_q A_q o G_(k-q) (A_q = B_q^-1), term1 = (1/Ny) sum_k diag(G_k M_k G_k), Lambda = rowsum((1/Ny) sum_k A_k o G_k)."""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "exp081d_results", "exp085c"); os.makedirs(OUT, exist_ok=True)
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); KS = [1, 1.5, 2, 2.5]; FAIL = []; T0 = time.time()
def check(nm, ok, det=""):
    print(f"{nm:66s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def norm(k):                                           # 081d normalisation, stored kappa (same as exp085_run.norm)
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]
mode = sys.argv[1]

# ----------------------------------------------------------------- TORUS
if mode == "TORUS":
    def Gk(n):                                         # verbatim from exp085_a4.py
        k = 2 * np.pi * np.arange(n) / n; E = sum(np.meshgrid(*(2 - 2 * np.cos(k),) * 3, indexing="ij"))
        G = np.zeros_like(E); m = E > 1e-14; G[m] = 1.0 / E[m]; return G
    def avgconv(A, B): return np.real(np.fft.fftn(np.fft.ifftn(A) * np.fft.ifftn(B)))
    def c_of_n(n):
        G = Gk(n); Bq = 2 * avgconv(G, G); S2 = avgconv(G * G, G); return float(-4 * np.mean((1.0 / Bq) * (S2 - G * np.mean(G * G))))
    for n in (8, 12):
        t = time.time(); Gr = np.real(np.fft.ifftn(Gk(n)))                      # position-space G (zero mode excluded)
        idx = np.indices((n, n, n)).reshape(3, -1).T; N3 = len(idx)
        D = (idx[:, None, :] - idx[None, :, :]) % n; Gm = Gr[D[..., 0], D[..., 1], D[..., 2]]; del D
        Bm = 2 * Gm * Gm; Ai = np.linalg.inv(Bm); M = Ai * Gm
        term1 = np.einsum("ij,ji->i", Gm @ M, Gm); Lam = M.sum(axis=1); term2 = (Gm * Gm) @ Lam
        cA = -4 * (term1 - term2); ref = c_of_n(n)
        check(f"KA-torus n={n}: c_A uniform in z", (cA.max() - cA.min()) <= 1e-10 * abs(ref), f"spread {cA.max()-cA.min():.1e}")
        check(f"KA-torus n={n}: c_A == c_of_n(n) (FFT path) to 1e-10 rel", abs(cA.mean() - ref) <= 1e-10 * abs(ref), f"{cA.mean():+.15f} vs {ref:+.15f} ({time.time()-t:.1f}s, N3 {N3})")
    sys.exit(1 if FAIL else 0)

# ----------------------------------------------------------------- geometry helpers
import sigma3d as S3, exp081c_numerics as C
def build(W, P):                                       # verbatim from exp085_run.build
    Wb = P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
    ck = None
    for dd in ("exp081d_results", "exp081c_results"):
        f = os.path.join(HERE, dd, f"sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0_ckpt.json")
        if os.path.exists(f): ck = json.load(open(f)); break
    lowrank = ck is not None and "ranks" in ck
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); U = C.install(S, refine="auto", lowrank=lowrank, rank_drop=0)
    return S, U, lowrank
def pieces(S):
    Ny, N = S.Ny, S.N
    d = C.coincident_dn_c(S); B1 = S.B1(); sig = np.linalg.solve(B1[0], 2 * d)              # sigdot: production path (phase C)
    G0 = np.array([sl.G0 for sl in S.sl], dtype=complex); A = np.array([np.linalg.inv(B1[k]) for k in range(Ny)])
    Lam = (A * G0).sum(axis=0).sum(axis=1) / Ny                                               # rowsum((1/Ny) sum_k A_k o G_k)
    M = np.zeros_like(G0); S.conv_into(M, A, G0, 1.0 / Ny)                                    # M_k = (1/Ny) sum_q A_q o G_(k-q)
    term1 = sum(np.einsum("ij,ji->i", G0[k] @ M[k], G0[k]) for k in range(Ny)) / Ny
    cA = -4 * term1 + 2 * (B1[0] @ Lam); Tz = -4 * term1                                     # T(z) = -4 term1 (tadpole)
    return dict(d=d, B1=B1, sig=sig, Lam=Lam, term1=term1, cA=cA, Tz=Tz, G0=G0, M=M)

# ----------------------------------------------------------------- SECTOR (W2P4)
if mode == "SECTOR":
    W, P = 2, 4; S, U, lr = build(W, P); Ny, N, Lx, Lt = S.Ny, S.N, S.Lx, S.Lt; pc = pieces(S)
    print(f"W2P4 sector pieces ({time.time()-T0:.0f}s)", flush=True)
    # dense 3D: sites (x, t, y), Dirichlet x, t; periodic y; diagonal 6, hopping -1 (H3 has NO cut: n = 1)
    N3 = N * Ny; H = np.zeros((N3, N3)); ix = lambda x, t, y: (y * Lx + x) * Lt + t
    for y in range(Ny):
        for x in range(Lx):
            for t in range(Lt):
                i = ix(x, t, y); H[i, i] = 6.0
                for (x2, t2, y2) in ((x + 1, t, y), (x, t + 1, y), (x, t, (y + 1) % Ny)):
                    if x2 < Lx and t2 < Lt: j = ix(x2, t2, y2); H[i, j] -= 1.0; H[j, i] -= 1.0
    G3 = np.linalg.inv(H); del H; B3 = 2 * G3 * G3; M3 = np.linalg.inv(B3) * G3; del B3
    s0 = np.arange(N)                                   # slice y = 0 sites: (0*Lx + x)*Lt + t == x*Lt + t (matches Strip3D idx)
    Lam3 = M3[s0].sum(axis=1); t13 = np.einsum("ij,ji->i", (G3 @ M3)[s0], G3[:, s0])
    g0 = (pc["G0"].sum(axis=0) / Ny).real
    check("KA-sector: G_3D(y=0 block) == (1/Ny) sum_p G_p", np.abs(G3[np.ix_(s0, s0)] - g0).max() <= 1e-12 * np.abs(g0).max(), f"{np.abs(G3[np.ix_(s0, s0)] - g0).max():.1e}")
    check("KA-sector: Lambda (sectors) == dense 3D", np.abs(pc["Lam"].real - Lam3).max() <= 1e-12 * np.abs(Lam3).max(), f"{np.abs(pc['Lam'].real - Lam3).max():.1e} (max|Lam| {np.abs(Lam3).max():.2e})")
    check("KA-sector: term1 (sectors) == dense 3D", np.abs(pc["term1"].real - t13).max() <= 1e-12 * np.abs(t13).max(), f"{np.abs(pc['term1'].real - t13).max():.1e} (max|t1| {np.abs(t13).max():.2e})")
    Tsad = C.saddle_term_c(S, pc["B1"])                 # production T_sad
    def identity_gap(sig):
        lhs = 0.5 * Tsad; rhs = 0.5 * Ny * float(np.real(np.sum(pc["cA"] * sig))) - 2 * Ny * float(np.real(np.sum(pc["Lam"] * pc["d"])))
        return abs(lhs - rhs), lhs, rhs
    gap, lhs, rhs = identity_gap(pc["sig"])
    check("identity KA: 1/2 T_sad == 1/2 Sum c_A sigdot - 2 Ny Sum Lambda d (1e-12 rel)", gap <= 1e-12 * abs(lhs), f"{lhs!r} vs {rhs!r} (gap {gap:.1e})")
    sp = pc["sig"].copy(); sp[18] *= (1 + 1e-6); gp, _, _ = identity_gap(sp)
    check("identity KA planted break: sigdot[18] x (1+1e-6) must FAIL", gp > 1e-12 * abs(lhs), f"gap {gp:.1e}")
    sys.exit(1 if FAIL else 0)

# ----------------------------------------------------------------- GEOM
if mode == "GEOM":
    W, P = int(sys.argv[2]), int(sys.argv[3]); S, U, lr = build(W, P); Ny, N, Lt = S.Ny, S.N, S.Lt; pc = pieces(S)
    Tsad_prod = C.saddle_term_c(S, pc["B1"]); Tsad_mine = Ny * float(np.real(np.sum(pc["Tz"] * pc["sig"])))
    fref = os.path.join(HERE, "exp081d_results", "exp085", f"C_W{W}P{P}.json"); ref = json.load(open(fref)) if os.path.exists(fref) else None
    check(f"GEOM W{W}P{P}: T_sad (term1 path) == saddle_term_c to 1e-10 rel", abs(Tsad_mine - Tsad_prod) <= 1e-10 * abs(Tsad_prod), f"{Tsad_mine!r} vs {Tsad_prod!r}")
    Sig3D = float(np.real(Ny * np.sum(pc["sig"])))
    if ref is not None:
        check(f"GEOM W{W}P{P}: saddle_term_c == stored 085 C tsad (bitwise)", Tsad_prod == ref["tsad"], f"{Tsad_prod!r} vs {ref['tsad']!r}")
        check(f"GEOM W{W}P{P}: Sigma3D == stored 085 C value (bitwise)", Sig3D == ref["Sigma3D"], f"{Sig3D!r} vs {ref['Sigma3D']!r}")
    else: print(f"GEOM W{W}P{P}: no stored 085 C reference at this geometry (k = 3): bitwise rows SKIPPED; CUSPIS_081E={os.environ.get('CUSPIS_081E')}", flush=True)
    rec = dict(W=W, P=P, Ny=Ny, Lx=S.Lx, Lt=Lt, cutx=list(S.cutx), tcut=S.tcut,
               X_cA=0.5 * Ny * float(np.real(np.sum(pc["cA"] * pc["sig"]))),            # 1/2 Sum_3D c_A sigdot  (S units)
               X_Lam=-2 * Ny * float(np.real(np.sum(pc["Lam"] * pc["d"]))),              # -2 Sum_3D Lambda d      (S units)
               Tsad=Tsad_prod, Sigma3D=Sig3D, cuspis_081e=os.environ.get("CUSPIS_081E"), sumabsLam=float(np.sum(np.abs(pc["Lam"]))), cA=[float(v) for v in pc["cA"].real],
               imag_max=float(max(np.abs(pc["cA"].imag).max(), np.abs(pc["Lam"].imag).max())), failed=FAIL, sec=time.time() - T0)
    json.dump(rec, open(os.path.join(OUT, f"G_W{W}P{P}.json"), "w"), indent=1)
    print(f"GEOM W{W}P{P} written ({time.time()-T0:.0f}s); max imag {rec['imag_max']:.1e}", flush=True); sys.exit(1 if FAIL else 0)

# ----------------------------------------------------------------- READ
if mode == "READ":
    G = {}
    for k in KS:
        for W in (int(2 * k), int(4 * k)):
            f = os.path.join(OUT, f"G_W{W}P{int(4*k)}.json")
            if not os.path.exists(f): print(f"missing {f} -> READ not made"); sys.exit(2)
            G[(W, int(4 * k))] = json.load(open(f))
    ks = np.array(KS, float); R = {k: JD[str(k)]["R_T0"] for k in KS}; sR = {k: JD[str(k)]["sigma"] for k in KS}; comp = {k: JD[str(k)]["components"] for k in KS}
    graw = float(np.polyfit(ks, [R[k] for k in KS], 1)[0])
    def Rop(key, k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return -(G[(W1, P)][key] - G[(W2, P)][key]) * norm(k)
    Y = {k: Rop("X_cA", k) for k in KS}                                                      # R[1/2 Sum c_A sigdot]
    RA1 = {k: R[k] - Y[k] for k in KS}                                                        # route 1 (reading)
    RA2 = {k: comp[k]["t0"] + comp[k]["C"] + Rop("X_Lam", k) for k in KS}                    # route 2 (identity)
    check("reproduction: stored components sum to R_T0", max(abs(sum(comp[k].values()) - R[k]) for k in KS) <= 1e-12 * max(abs(R[k]) for k in KS), "")
    dk = max(abs(RA1[k] - RA2[k]) / max(1.0, abs(RA1[k])) for k in KS)
    check("two-route KA: route 1 == route 2 per k (1e-10 rel)", dk <= 1e-10, f"max rel {dk:.1e}")
    # W4P4 bound in R units BEFORE the reading (registration G)
    g44 = G[(4, 4)]; bound = 2 * g44["Ny"] * g44["sumabsLam"] * 6e-9 * norm(1)
    print(f"W4P4 bound (registration G): |Delta R| <= {bound:.2e}  {'(<= 0.01: no caveat)' if bound <= 0.01 else '(> 0.01: k = 1 CAVEAT in headline)'}", flush=True)
    # 1/a^2 row on Y (084b kfit verbatim)
    X3 = np.column_stack([ks ** 2, ks, np.ones(4)])
    def kfit(Rd, sRd):
        y = np.array([Rd[k] for k in KS]); s = np.maximum(np.array([sRd[k] for k in KS]), 1e-15); Wm = np.diag(1 / s ** 2)
        Am = X3.T @ Wm @ X3; p = np.linalg.solve(Am, X3.T @ Wm @ y); chi2 = float(((y - X3 @ p) / s) @ ((y - X3 @ p) / s))
        cov = max(1.0, chi2 / 1.0) * np.linalg.inv(Am); return float(p[0]), float(np.sqrt(cov[0, 0]))
    c2, sc2 = kfit(Y, sR); row = ("no 1/a^2 remainder" if abs(c2) + 2 * sc2 <= 0.057 else
                                  "A leaves a 1/a^2 remainder -> (P2) fails" if abs(c2) - 2 * sc2 > 0.057 else "INCONCLUSIVE (1/a^2 unresolved)")
    print(f"1/a^2 row: c2(Y) = {c2:+.5f} +- {sc2:.5f} (1 dof; threshold |c2| + 2 sigma <= 0.057) -> {row}", flush=True)
    def slope_and_sigma(out, sg):                                                             # verbatim from exp085_run
        y = np.array([out[k] for k in KS]); g, b0 = np.polyfit(ks, y, 1); Sxx = np.sum((ks - ks.mean()) ** 2)
        ssr = np.sum((y - (g * ks + b0)) ** 2); s_fit = np.sqrt(ssr / (len(ks) - 2) / Sxx)
        w = (ks - ks.mean()) / Sxx; s_prop = np.sqrt(np.sum((w * np.array([sg[k] for k in KS])) ** 2))
        return float(g), float(np.hypot(s_fit, s_prop))
    def sband(r, s):                                                                          # SIGNED bands (registration D)
        lo, hi = r - 2 * s, r + 2 * s
        if hi < -0.1: return "overshoot"
        if lo >= -0.1 and hi <= 0.1: return "supported"
        if lo > 0.1 and hi < 0.5: return "partial"
        if lo >= 0.5: return "refuted as sole cause"
        return "INCONCLUSIVE (straddles a band edge)"
    def show(nm, out):
        g, s = slope_and_sigma(out, sR); r, sr = g / graw, s / graw; b = sband(r, sr)
        print(f"{nm:34s}: R_corr {[round(out[k], 5) for k in KS]}  g {g:+.4f} +- {s:.4f}  rho_s {r:+.4f} +- {sr:.4f} -> {b}", flush=True); return g, r, sr, b
    gA, rA, srA, bA = show("A (PRIMARY, route 1)", RA1)
    gz, _, _, _ = show("control zero (A x 0)", {k: R[k] - 0.0 * Y[k] for k in KS})
    check("zero control reproduces g_raw (bitwise)", gz == graw, f"{gz!r} vs {graw!r}")
    _, _, _, bM = show("control must-fail sign (-Delta S_A)", {k: R[k] + Y[k] for k in KS})
    check("must-fail sign lands in a band different from A's", bM != bA, f"{bM} vs {bA}")
    print("\n--- DESCRIPTIVE (not a reading) ---", flush=True)
    E5 = json.load(open(os.path.join(HERE, "exp081d_results", "exp085", "E.json")))["ends"]
    for tag, cc in E5.items():
        Yb = {k: -(0.5 * cc * (G[(int(2*k), int(4*k))]["Sigma3D"] - G[(int(4*k), int(4*k))]["Sigma3D"])) * norm(k) for k in KS}
        show(f"bulk [{tag}]", {k: R[k] - Yb[k] for k in KS})
        print(f"   box-minus-bulk R[1/2 Sum (c_A - c) sigdot] [{tag}]: {[round(Y[k] - Yb[k], 5) for k in KS]}", flush=True)
    show("full box tadpole (R_t0 + R_C)", {k: comp[k]["t0"] + comp[k]["C"] for k in KS})
    cref = list(E5.values())[0]
    for (W, P), g in sorted(G.items()):
        cA = np.array(g["cA"]); Lt = g["Lt"]; x = np.arange(len(cA)) // Lt; t = np.arange(len(cA)) % Lt; Lx = g["Lx"]
        xm = Lx // 2; inter = cA[(np.abs(x - xm) <= 1) & (np.abs(t - Lt // 2) <= 1)]; wall = cA[(x == 0) | (t == 0)]
        ce = cA[((x == g["cutx"][0] - 1) | (x == g["cutx"][-1] + 1)) & ((t == g["tcut"]) | (t == g["tcut"] + 1))]
        print(f"   c_A/c map W{W}P{P}: interior {inter.mean()/cref:.4f}  wall {wall.mean()/cref:.4f}  next to cut ends {ce.mean()/cref:.4f}  (c = {cref:+.6f})", flush=True)
    head = f"EXP-085c READING (PRIMARY A): {bA if row == 'no 1/a^2 remainder' else row}"
    if bound > 0.01: head += "  [CAVEAT: W4P4 bound > 0.01 at k = 1]"
    print(f"\n{head}   rho_s {rA:+.4f} +- {srA:.4f}; 1/a^2 row: {row}; controls {'PASS' if not FAIL else FAIL}")
    json.dump(dict(reading=head, rhoA=rA, sigma_rhoA=srA, bandA=bA, row=row, c2=c2, sc2=sc2, Y=Y, RA1=RA1, RA2=RA2, bound_W4P4=bound, failed=FAIL),
              open(os.path.join(OUT, "result.json"), "w"), indent=1, default=float)
    sys.exit(1 if FAIL else 0)
