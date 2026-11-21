"""EXP-074: Richardson re-analysis of the EXISTING EXP-073(b) cache with the tip-exponent ladder (argued):
lattice corrections ~ (a_lat/w)^{2 nu}, nu in {a, 1-a, 1+a, ...} (regular tip modes), plus W^-1 (edge position).
Real a:    model A = f + c1 W^-2a + c2 W^-1            (LSQ, 4 points, 1 dof)
           model B = A + c3 W^-2(1-a)                    (exact, 4 unknowns)
Complex a (a = 1/2 + i y): W^-2a, W^-2(1-a) = W^-1 e^{-/+ i y' ln W}, y' = 2 Im a:
           model A = f + W^-1 (A cos(y' ln W) + B sin(y' ln W))   (LSQ, 1 dof)
           model B = A + C W^-1                                   (exact)
Central value: model B; sigma_sys = |f_A - f_B|. [model: Opus 5.5]"""
import numpy as np
def basis(W, a, model):
    W = np.asarray(W, float); cols = [np.ones_like(W)]
    if isinstance(a, complex) and a.imag != 0:
        yp = 2 * a.imag
        cols += [np.cos(yp * np.log(W)) / W, np.sin(yp * np.log(W)) / W]
        if model == "B": cols += [1 / W]
    else:
        cols += [W ** (-2 * a), 1 / W]
        if model == "B": cols += [W ** (-2 * (1 - a))]
    return np.vstack(cols).T
def extrap(W, f, a):
    out = {}
    for m in ("A", "B"):
        X = basis(W, a, m); c, *_ = np.linalg.lstsq(X, np.asarray(f, float), rcond=None)
        out[m] = (c[0], float(np.abs(X @ c - f).max()))
    return out["B"][0], abs(out["A"][0] - out["B"][0]), out
if __name__ == "__main__":
    # Controls run ALONE (before touching the real cache): known-answer synthetic sequences, incl. a next-order term
    # beyond both models; and a must-fail with a wrong true exponent.
    rng = np.random.default_rng(7); W = np.array([8, 16, 32, 64.])
    print("KNOWN-ANSWER (true ladder + unmodelled W^-2 term; 200 random draws per twist, sizes like the data):")
    for a in (0.3, 0.5 + 0.5j):
        ok = 0; worst = 0
        for _ in range(200):
            L = 1.0
            if isinstance(a, complex):
                f = L + (rng.uniform(-0.6, 0.6) * np.cos(np.log(W)) + rng.uniform(-0.6, 0.6) * np.sin(np.log(W))) * 8 / W \
                    + rng.uniform(-0.3, 0.3) * 8 / W + rng.uniform(-0.5, 0.5) * 64 / W ** 2
            else:
                f = L - rng.uniform(0.3, 0.8) * (W / 8) ** (-0.6) + rng.uniform(-0.2, 0.2) * 8 / W \
                    + rng.uniform(-0.2, 0.2) * (W / 8) ** (-1.4) + rng.uniform(-0.3, 0.3) * 64 / W ** 2
            fB, s, _ = extrap(W, f, a); ok += abs(fB - L) <= 3 * max(s, 1e-15); worst = max(worst, abs(fB - L))
        print(f"  a={a}: recovered within 3 sigma_sys in {ok}/200; worst |f-L| = {worst:.3f}")
    print("MUST-FAIL (real a=0.3 model, but true leading exponent 0.3 instead of 0.6):")
    fired = 0
    for _ in range(200):
        f = 1.0 - rng.uniform(0.3, 0.8) * (W / 8) ** (-0.3) + rng.uniform(-0.2, 0.2) * 8 / W
        fB, s, _ = extrap(W, f, 0.3); fired += (abs(fB - 1.0) > 3 * s) or (s > 0.02)
    print(f"  flagged (|f-L| > 3 sigma_sys or sigma_sys > 2%) in {fired}/200")
