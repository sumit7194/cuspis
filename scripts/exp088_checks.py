"""EXP-088 checks (registration notes/EXP-088_registration.md). Modes:
  E   PD check: lambda_min(H_(2,p) + diag sigma_2) > 0 for every sector, at the six stored 084c geometries (concavity => unique RS saddle)
  C   finite-difference test of Q1 on tiny boxes: [f_2(+eps h) - f_2(-eps h)]/2eps == -1/2 n Ny Sum h sigma_2, h in {c_A, uniform, random}
  D   sigdot profile (n -> 1) at W4P8, W8P8: r^2 sigdot by shell (Fable's 'contact term' claim) + the stored-number flatness
  A   sigma_2 at P = 10 (honest saddle) -> grade the seal S_2(2.5) and the l = 2 -> 2.5 bulk ratio (KA: W4P8 honest sum vs stored 084c)
[model: Opus 5.5]"""
import sys, os, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp083_honest as H
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); FAIL = []; T0 = time.time()
def check(nm, ok, det=""):
    print(f"{nm:66s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def norm(k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]
def saddle_target(g, n, target, sig0=None, tol=1e-13, itmax=40):          # exp083_honest.Geom.saddle with an explicit target J(x)
    N, Ny = g.N, g.Ny; sig = np.zeros(N) if sig0 is None else sig0.copy()
    for it in range(itmax):
        G = g.Gn(n, sig); F = sum(np.diag(x)[:N] for x in G) / Ny - target
        if np.abs(F).max() < tol: return sig
        Jm = np.zeros((N, N))
        for x in G:
            for s in range(n): Jm -= x[:N, s * N:(s + 1) * N] ** 2
        sig = sig - np.linalg.solve(Jm / Ny, F)
    raise RuntimeError("saddle did not converge")
def f_lead(g, n, sig, J):                                                # f_n = 1/2 [sum_p logdet H_(n,p)(sigma) - n Ny Sum J sigma]
    tot = 0.0
    for p in range(g.Ny):
        s, ld = np.linalg.slogdet(g.Hn(p, n, sig))
        if s <= 0: raise RuntimeError(f"non-positive det at p={p}")
        tot += ld
    return 0.5 * (tot - n * g.Ny * float(np.dot(J, sig)))
mode = sys.argv[1]
GEOS = [(2, 4), (4, 4), (3, 6), (6, 6), (4, 8), (8, 8)]
if mode == "E":
    for W, P in GEOS:
        g = H.Geom(W, P, Wbox=P, c=2); s2 = np.array(json.load(open(os.path.join(D, "exp084c", f"c84_W{W}P{P}_n2.json")))["sigma"])
        lam = [float(np.linalg.eigvalsh(g.Hn(p, 2, s2)).min()) for p in range(g.Ny // 2 + 1)]
        lam0 = [float(np.linalg.eigvalsh(g.Hn(p, 2, None)).min()) for p in range(g.Ny // 2 + 1)]
        check(f"E W{W}P{P}: lambda_min(H_2 + sigma_2) > 0 in every sector", min(lam) > 0, f"min {min(lam):.4e} (sigma = 0: {min(lam0):.4e}); min sigma_2 {s2.min():+.4f}  ({time.time()-T0:.0f}s)")
if mode == "C":
    import sigma3d as S3, exp081c_numerics as C
    def cA_box(W, P, Wb):                                                # exp085c pieces: c_A = -4 term1 + 2 B_0 Lambda (sectors)
        Lx, Lt, Ny = 2 * P + Wb, 2 * P, 4 * P; x0 = P + (Wb - W) // 2
        S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=False, rank_drop=0)
        B1 = S.B1(); G0 = np.array([sl.G0 for sl in S.sl], dtype=complex); A = np.array([np.linalg.inv(B1[k]) for k in range(Ny)])
        Lam = (A * G0).sum(axis=0).sum(axis=1) / Ny; M = np.zeros_like(G0); S.conv_into(M, A, G0, 1.0 / Ny)
        t1 = sum(np.einsum("ij,ji->i", G0[k] @ M[k], G0[k]) for k in range(Ny)) / Ny
        return (-4 * t1 + 2 * (B1[0] @ Lam)).real
    rng = np.random.default_rng(20261125)
    for W, P, Wb in ((2, 2, 2), (2, 3, 4)):
        g = H.Geom(W, P, Wbox=Wb, c=2); N, Ny = g.N, g.Ny; G1 = g.Gn(1); J0 = sum(np.diag(x) for x in G1) / Ny
        s0 = saddle_target(g, 2, J0); f0 = f_lead(g, 2, s0, J0)
        for hn, h in (("c_A", cA_box(W, P, Wb)), ("uniform", np.ones(N)), ("random", rng.normal(size=N))):
            pred = -0.5 * 2 * Ny * float(np.dot(h, s0)); rows = []
            for eps in (1e-3, 1e-4):
                sp = saddle_target(g, 2, J0 + eps * h, s0); sm = saddle_target(g, 2, J0 - eps * h, s0)
                fp, fm = f_lead(g, 2, sp, J0 + eps * h), f_lead(g, 2, sm, J0 - eps * h)
                rows.append(((fp - fm) / (2 * eps), (fp + fm - 2 * f0) / eps ** 2))
            rel = max(abs(r[0] - pred) / max(abs(pred), 1e-300) for r in rows)
            check(f"C W{W}P{P}Wb{Wb} h={hn}: FD derivative == -1/2 n Ny Sum h sigma_2 (1e-6 rel)", rel <= 1e-6, f"pred {pred:+.10e} FD {rows[0][0]:+.10e}/{rows[1][0]:+.10e} rel {rel:.1e}")
            c2 = [r[1] for r in rows]; check(f"C W{W}P{P}Wb{Wb} h={hn}: second difference ~ eps-independent (no O(eps) term)", abs(c2[0] - c2[1]) <= 0.05 * max(abs(c2[1]), 1e-12), f"curv {c2[0]:+.5e} / {c2[1]:+.5e}")
        f1p = f_lead(g, 1, saddle_target(g, 1, J0 + 1e-4 * np.ones(N)), J0 + 1e-4 * np.ones(N)); f1m = f_lead(g, 1, saddle_target(g, 1, J0 - 1e-4 * np.ones(N)), J0 - 1e-4 * np.ones(N))
        check(f"C W{W}P{P}Wb{Wb}: n = 1 FD derivative == 0 (sigma_1 = 0)", abs((f1p - f1m) / 2e-4) <= 1e-6 * Ny, f"{(f1p - f1m)/2e-4:+.2e}")
if mode == "D":
    import sigma3d as S3, exp081c_numerics as C
    for W, P in ((4, 8), (8, 8)):
        Wb, Lx, Lt, Ny = P, 3 * P, 2 * P, 4 * P; x0 = P + (Wb - W) // 2
        S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=True, rank_drop=0)
        d = C.coincident_dn_c(S); B1 = S.B1(); sd = np.linalg.solve(B1[0], 2 * d).real; Sd = sd.reshape(Lx, Lt)
        s2 = np.array(json.load(open(os.path.join(D, "exp084c", f"c84_W{W}P{P}_n2.json")))["sigma"]).reshape(Lx, Lt)
        cutx = list(range(x0, x0 + W)); tc = P - 1; X, T = np.meshgrid(np.arange(Lx), np.arange(Lt), indexing="ij")
        r = np.minimum(np.hypot(X - (cutx[0] - 0.5), T - (tc + 0.5)), np.hypot(X - (cutx[-1] + 0.5), T - (tc + 0.5)))
        print(f"W{W}P{P}: Sum sigdot {sd.sum():+.6f} (stored Sigma3D/Ny check) | Sum sigma_2 {s2.sum():+.6f}; shell: mean r^2 sigdot | mean r^2 sigma_2 | ratio", flush=True)
        for a, b in zip([0, 0.8, 1.2, 1.7, 2.3, 3.2, 4.5, 6.5], [0.8, 1.2, 1.7, 2.3, 3.2, 4.5, 6.5, 9]):
            m = (r >= a) & (r < b)
            if m.sum(): print(f"   [{a:3.1f},{b:3.1f}) {int(m.sum()):4d}  {(Sd[m] * r[m] ** 2).mean():+.5f} | {(s2[m] * r[m] ** 2).mean():+.5f} | {(Sd[m] * r[m] ** 2).mean() / (s2[m] * r[m] ** 2).mean():+.3f}", flush=True)
    chi = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]["hi c(384)"]
    vals = []
    for k in (1, 1.5, 2, 2.5):
        P = int(4 * k); a, b = (json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json"))) for W in (int(2 * k), int(4 * k)))
        vals.append((2 * a["X_cA"] / a["Ny"] - 2 * b["X_cA"] / b["Ny"]) / (chi * (1 - 2 / P)))
    print(f"stored-number part: W-difference of Sum c_A sigdot / (c (1 - 2/P)) = {np.round(vals, 3)} (Fable: 0.307, 0.308, 0.316, 0.326)")
if mode == "A":
    g = H.Geom(4, 8, Wbox=8, c=2); sK, _ = g.saddle(2); ref = np.array(json.load(open(os.path.join(D, "exp084c", "c84_W4P8_n2.json")))["sigma"])
    check("A KA: honest saddle W4P8 n=2 sum == stored 084c sigma_2 sum (1e-6)", abs(sK.sum() - ref.sum()) <= 1e-6, f"{sK.sum():+.9f} vs {ref.sum():+.9f} (max site diff {np.abs(sK - ref).max():.1e})")
    sig = {}
    for W in (5, 10):
        g = H.Geom(W, 10, Wbox=10, c=2); t = time.time(); sig[W], it = g.saddle(2); print(f"W{W}P10 honest sigma_2: Sum {sig[W].sum():+.6f} ({it} it, {time.time()-t:.0f}s)", flush=True)
        json.dump(dict(W=W, P=10, sigma=list(sig[W])), open(os.path.join(D, f"exp088_sigma2_W{W}P10.json"), "w"))
    cA = {W: np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{W}P10.json")))["cA"]) for W in (5, 10)}
    R2 = json.load(open(os.path.join(D, "exp084", "result.json")))["Rn"]["2"]; Ny = 40
    dA = Ny * (cA[5] @ sig[5] - cA[10] @ sig[10]) * norm(2.5); S25 = R2["2.5"] + dA
    print(f"\nSEAL GRADING: R2(2.5) {R2['2.5']:.4f} + dR2^A(2.5) {dA:+.4f} = S2(2.5) {S25:+.4f}", flush=True)
    print(f"   PRIMARY (seal 68% band [0.162, 0.202]): {'PASS' if 0.162 <= S25 <= 0.202 else 'FAIL'};  SECONDARY (outer [0.14, 0.23]): {'inside' if 0.14 <= S25 <= 0.23 else 'OUTSIDE'};  Fable risk values 0.27 / 0.35", flush=True)
    ends = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]; prev = {"hi c(384)": -4.44993, "lo c(384)+3Delta": -4.85835}
    for t, c in ends.items():
        b25 = Ny * c * (sig[5].sum() - sig[10].sum()) * norm(2.5); ratio = -(b25 - prev[t]) / (R2["2.5"] - R2["2"]); tgt = 1.27 if t.startswith("hi") else 1.39
        print(f"   bulk [{t}]: dR2(2.5) {b25:+.4f}; local ratio l 2 -> 2.5 = {ratio:.4f}  (predicted {tgt} +- 0.03): {'PASS' if abs(ratio - tgt) <= 0.03 else 'FAIL'}", flush=True)
print(f"\nEXP-088 mode {mode}: {'controls PASS' if not FAIL else 'FAIL: ' + ', '.join(FAIL)}  ({time.time()-T0:.0f}s)")
sys.exit(1 if FAIL else 0)
