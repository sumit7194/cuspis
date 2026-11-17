"""EXP-034a (addendum to EXP-034; pre-registered in report.md before any run).  Same model, same frozen thresholds.
Changes from EXP-034, each stated in the registration:
  (1) correlators: X from an N = 8192 periodic lattice (k = 0 excluded) PLUS the zero-mode constant
      C = X_inf(0) - X_N(0), so that X approximates the infinite-lattice state the model names.  The box artifact was
      measured to be a constant to ~1e-6 (design calibration, report.md EXP-034a); without C the long-range
      correlations at r = 160-640 are 25-60% of their infinite-lattice values for alpha = 1.5.
  (2) run A: the EXP-034 geometry (eta 0.40/0.25/0.15, R 40/56/80) with the corrected correlators (one-variable control).
  (3) run B: eta down to 0.05 with R = k r0, r0 = 2/eta, k in {4, 4 sqrt 2, 8} (same geometry in units of r0 at every eta).
Memory-lean entropy: chunked submatrix build, in-place Cholesky on the F-ordered view, in-place triangular products
(dtrmm), so the peak is ~2 n x n float64 blocks.  Checkpointed to exp034a_ckpt.jsonl.  Run with BLAS threads = 1."""
import json, os, subprocess, sys, time
import numpy as np
from scipy.integrate import quad
from scipy.linalg import cholesky, eigvalsh
from scipy.linalg.blas import dtrmm
import exp034_wedge_mi as m0          # wedge(), tables(), the old entropy (for the Tier-1 implementation check)

D = os.path.dirname(os.path.abspath(__file__))
CK = os.path.join(D, "exp034a_ckpt.jsonl")
N = 8192
ALPHAS, THETAS = (1.0, 1.5, 0.5), (90, 180)
ETAS_A, RS_A = (0.40, 0.25, 0.15), (40, 56, 80)
ETAS_B, KS_B = (0.40, 0.25, 0.15, 0.10, 0.05), (4.0, 4.0 * np.sqrt(2), 8.0)
RMAX = max(max(RS_A), max(k * 2 / e for e in ETAS_B for k in KS_B))
KEEP = int(np.ceil(2 * RMAX)) + 2

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def submat(T, s, chunk=512):
    s = s.astype(np.int64); n = len(s); out = np.empty((n, n))
    for i in range(0, n, chunk):
        out[i:i + chunk] = T[np.abs(s[i:i + chunk, None, 0] - s[None, :, 0]), np.abs(s[i:i + chunk, None, 1] - s[None, :, 1])]
    return out

def entropy_sites(X, P, s):
    """S of the Gaussian state on sites s; X, P are the (|dx|, |dy|) tables.  Peak ~ 2 n^2 float64."""
    A = submat(X, s).T                                   # symmetric: the transpose is an F-ordered view, no copy
    L = cholesky(A, lower=True, overwrite_a=True, check_finite=False); del A
    B = submat(P, s).T
    B = dtrmm(1.0, L, B, side=0, lower=1, trans_a=1, overwrite_b=1)   # B <- L^T P
    B = dtrmm(1.0, L, B, side=1, lower=1, trans_a=0, overwrite_b=1)   # B <- L^T P L
    del L
    nu = np.sqrt(np.clip(eigvalsh(B, overwrite_a=True, check_finite=False), 0.25, None)); del B
    a, b = nu + 0.5, nu - 0.5
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(b > 1e-300, b * np.log(b), 0.0)
    return float(np.sum(a * np.log(a) - t))

# ---------------- zero-mode constant: two implementations ----------------
def X0_quad(al):
    def inner(phi):
        c, s = np.cos(phi), np.sin(phi)
        f = lambda r: 0.5 if r < 1e-12 else (r ** 2 / (4 * np.sin(r * c / 2) ** 2 + 4 * np.sin(r * s / 2) ** 2)) ** (al / 2) / 2
        return quad(f, 0, np.pi / c, weight="alg", wvar=(1 - al, 0), epsabs=1e-13, epsrel=1e-12, limit=200)[0]
    return 8 * quad(inner, 0, np.pi / 4, epsabs=1e-13, epsrel=1e-12, limit=200)[0] / (4 * np.pi ** 2)

def axis_box(al, n, rs, chunk=1024):
    """On-axis X_n(r, 0) for a periodic n-lattice with k = 0 excluded (row sums first: O(n) memory per chunk)."""
    k = 2 * np.pi * np.arange(n) / n; s2 = 4 * np.sin(k / 2) ** 2; g = np.zeros(n)
    for i in range(0, n, chunk):
        w = (s2[i:i + chunk, None] + s2[None, :]) ** (al / 2)
        with np.errstate(divide="ignore"):
            g[i:i + chunk] = np.where(w > 0, 1 / (2 * w), 0.0).sum(1)
    return np.array([(g * np.cos(k * r)).sum() / n ** 2 for r in rs])

def tables_corrected(al):
    f = os.path.join(D, f"exp034a_tables_a{al}.npz")
    if not os.path.exists(f):
        subprocess.run([sys.executable, "-c", f"import numpy as np, exp034_wedge_mi as m; X, P, _, _ = m.tables({al}, n={N}, keep={KEEP}); "
                        f"np.savez(r'{f}', X=X, P=P)"], cwd=D, check=True)
    z = np.load(f); return z["X"], z["P"]

def wedge(eta, R, axis):
    """As exp034_wedge_mi.wedge, but on an INTEGER grid for non-integer R (fix after run 1 crashed: np.arange(-R, R+1)
    with fractional R gave non-integer y, hence duplicate sites after the int cast and a singular X).  The radial cut
    r <= R keeps the float R.  Identical to the EXP-034 wedge for integer R (checked in Tier 1)."""
    Ri = int(np.ceil(R)); r0 = 2.0 / eta
    xs, ys = np.meshgrid(np.arange(0, Ri + 1), np.arange(-Ri, Ri + 1), indexing="ij")
    r = np.hypot(xs, ys); ang = np.arctan2(ys, xs)
    msk = (r >= r0) & (r <= R) & (np.abs(ang) <= eta + 1e-12)
    s = np.stack([xs[msk], ys[msk]], axis=1)
    if axis == "+x": return s
    if axis == "-x": return np.stack([-s[:, 0], s[:, 1]], axis=1)
    if axis == "+y": return np.stack([s[:, 1], s[:, 0]], axis=1)
    raise ValueError(axis)

def load_ck():
    d = {}
    if os.path.exists(CK):
        for line in open(CK):
            j = json.loads(line); d[j["key"]] = j["S"]
    return d

def main():
    log(f"EXP-034a start; threads OMP={os.environ.get('OMP_NUM_THREADS')} VECLIB={os.environ.get('VECLIB_MAXIMUM_THREADS')}; N={N} KEEP={KEEP}")
    # ---- Tier 1a: purity (as EXP-034) ----
    for al in ALPHAS:
        _, _, Xf, Pf = m0.tables(al, n=24, mass=0.3, keep=24)
        xy = np.array([(i, j) for i in range(24) for j in range(24)]); inA = (xy[:, 0] < 9) & (xy[:, 1] < 13)
        def per(s):
            dx = (s[:, None, 0] - s[None, :, 0]) % 24; dy = (s[:, None, 1] - s[None, :, 1]) % 24
            return Xf[dx, dy], Pf[dx, dy]
        sA, sAc = m0.entropy(*per(xy[inA])), m0.entropy(*per(xy[~inA]))
        rel = abs(sA - sAc) / sA
        log(f"Tier-1 purity alpha={al}: rel diff {rel:.2e} [{'PASS' if rel < 1e-8 else 'FAIL'}]")
        if rel >= 1e-8: log("ABORT"); sys.exit(2)
    for eta in ETAS_A + ETAS_B:     # Tier 1e: the integer-grid wedge equals the EXP-034 wedge at integer R; no duplicates anywhere
        for R in RS_A:
            assert np.array_equal(wedge(eta, R, "+x"), m0.wedge(eta, R, "+x")), (eta, R)
        for k in KS_B:
            w = wedge(eta, k * 2 / eta, "+x"); assert len(np.unique(w, axis=0)) == len(w) and w.dtype.kind == "i", (eta, k)
    log("Tier-1 wedge: integer-grid builder == EXP-034 builder at integer R; no duplicate sites at any B radius [PASS]")
    ck = load_ck(); fck = open(CK, "a")
    def S(key, X, P, s):
        if key not in ck:
            t0 = time.time(); ck[key] = entropy_sites(X, P, s)
            fck.write(json.dumps({"key": key, "S": ck[key]}) + "\n"); fck.flush()
            log(f"  {key}: n={len(s)} S = {ck[key]:.10f}  ({time.time() - t0:.0f} s)")
        return ck[key]
    rs_chk = (0, 40, 160, 320, 640)
    # Phase 0 (reordered after run 2 was killed by the 4 GB cap at an alpha transition: the table-build subprocess and
    # the 32768 axis sums overlapped a main process still holding ~2 GB from the last large entropy).  All tables and
    # all correlator gates now run first, while the main process is small.  Numerics unchanged.
    consts = {}
    for al in ALPHAS:
        q = 2.0 ** (-(2 - al))
        b16, b32 = axis_box(al, 16384, [0], chunk=256)[0], axis_box(al, 32768, [0], chunk=256)[0]
        x0q, x0r = X0_quad(al), b32 + (b32 - b16) * q / (1 - q)
        log(f"Tier-1 X_inf(0) alpha={al}: quadrature {x0q:.13f}  Richardson(16k,32k) {x0r:.13f}  |diff| {abs(x0q - x0r):.1e} "
            f"[{'PASS' if abs(x0q - x0r) < 1e-10 else 'FAIL'}]")
        if abs(x0q - x0r) >= 1e-10: log("ABORT"); sys.exit(3)
        t0 = time.time(); X, P = tables_corrected(al); C = x0q - X[0, 0]; X = X + C; consts[al] = C
        log(f"alpha={al}: tables N={N} built ({time.time() - t0:.0f} s); zero-mode constant C = {C:.10f} ({C / x0q:.2%} of X(0))")
        ref = axis_box(al, 32768, rs_chk, chunk=256); ref = ref + (x0q - ref[0])
        rel = np.abs(X[list(rs_chk), 0] - ref) / ref
        log(f"Tier-1 correlator alpha={al}: X_corr(r,0)/X_inf(r,0) - 1 at r={rs_chk}: {np.array2string(rel, precision=2)} "
            f"[{'PASS' if rel.max() < 0.01 else 'FAIL'}]  (uncorrected box would be off by {np.array2string(C / ref, precision=2)})")
        if rel.max() >= 0.01: log("ABORT"); sys.exit(4)
        if al == 1.0:
            log(f"  known answer, alpha=1: X_corr(640,0) * 4 pi 640 = {X[640, 0] * 4 * np.pi * 640:.5f} (continuum 1/(4 pi r) -> 1)")
        del X, P
    for al in ALPHAS:
        X, P = tables_corrected(al); X = X + consts[al]
        # ---- Tier 1d: lean entropy == EXP-034 entropy on the same matrices ----
        if al == ALPHAS[0]:
            s = m0.wedge(0.40, 40, "+x"); s2 = np.concatenate([s, m0.wedge(0.40, 40, "+y")])
            for ss in (s, s2):
                old = m0.entropy(m0.submat(X, ss), m0.submat(P, ss)); new = entropy_sites(X, P, ss)
                log(f"Tier-1 entropy implementations n={len(ss)}: old {old:.12f} new {new:.12f} rel {abs(old - new) / old:.1e} "
                    f"[{'PASS' if abs(old - new) / old < 1e-10 else 'FAIL'}]")
                if abs(old - new) / old >= 1e-10: log("ABORT"); sys.exit(5)
        for run, etas in (("A", ETAS_A), ("B", ETAS_B)):
            for eta in etas:
                Rs = RS_A if run == "A" else tuple(k * 2 / eta for k in KS_B)
                for iR, R in enumerate(Rs):
                    g1 = wedge(eta, R, "+x")
                    s1 = S(f"{run}_a{al}_e{eta}_R{R:.3f}_G1", X, P, g1)
                    for th in THETAS:
                        g2 = wedge(eta, R, "+y" if th == 90 else "-x")
                        if iR == 0:
                            s2 = S(f"{run}_a{al}_e{eta}_R{R:.3f}_G2_th{th}", X, P, g2)
                            log(f"Tier-1 symmetry {run} alpha={al} eta={eta} th={th}: {abs(s1 - s2) / s1:.1e} "
                                f"[{'PASS' if abs(s1 - s2) / s1 < 1e-8 else 'FAIL'}]")
                        S(f"{run}_a{al}_e{eta}_R{R:.3f}_U_th{th}", X, P, np.concatenate([g1, g2]))
        del X, P
    log("all entropies done; analysis:")
    analyse(load_ck())

def analyse(ck):
    iG = {}
    for run, etas in (("A", ETAS_A), ("B", ETAS_B)):
        for al in ALPHAS:
            for eta in etas:
                Rs = RS_A if run == "A" else tuple(k * 2 / eta for k in KS_B)
                lr = np.log(np.array(Rs, float))
                for th in THETAS:
                    I = np.array([2 * ck[f"{run}_a{al}_e{eta}_R{R:.3f}_G1"] - ck[f"{run}_a{al}_e{eta}_R{R:.3f}_U_th{th}"] for R in Rs])
                    sl = np.polyfit(lr, I, 1)[0]; two = np.diff(I) / np.diff(lr); iG[(run, al, eta, th)] = sl
                    log(f"{run} alpha={al} eta={eta:.2f} th={th}: I = {np.round(I, 6)}  i_G (LSQ) = {sl:.6f}  two-point = {np.round(two, 6)}")
    log("verdict quantities (frozen criteria, report.md EXP-034 / EXP-034a):")
    for run, lo, hi in (("A", 0.15, 0.40), ("B", 0.05, 0.15), ("B", 0.15, 0.40)):
        tag = {"A": "run A (secondary, one-variable control)", "B": "run B"}[run] + f" r = i_G({lo})/i_G({hi})"
        if run == "B" and lo == 0.15: tag += " (descriptive only)"
        for al in ALPHAS:
            log(f"  {tag}: alpha={al}: " + "  ".join(f"th={th}: {iG[(run, al, lo, th)] / iG[(run, al, hi, th)]:.4f}" for th in THETAS))
        log(f"  {tag}: scalar |i_G(90)-i_G(180)|: at {hi}: {abs(iG[(run, 1.0, hi, 90)] - iG[(run, 1.0, hi, 180)]):.6f}; "
            f"at {lo}: {abs(iG[(run, 1.0, lo, 90)] - iG[(run, 1.0, lo, 180)]):.6f}")

if __name__ == "__main__":
    analyse(load_ck()) if sys.argv[1:] == ["--analyse"] else main()
