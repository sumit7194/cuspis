"""EXP-083 redesign R1 (a1ef345): adequate-model family M1-M4 and the many-base pencil. [model: Opus 5.5]"""
import numpy as np
def design(ns, singles, n2=(), prods=()):
    ns = np.asarray(ns, float); cols = [ns, np.ones_like(ns)]; derivs = [1.0, 0.0]
    for b in singles: cols += [b ** ns, ns * b ** ns]; derivs += [b * np.log(b), b * (1 + np.log(b))]
    for b in n2: cols += [ns ** 2 * b ** ns]; derivs += [b * (2 + np.log(b))]
    for b in prods: cols += [b ** ns, ns * b ** ns]; derivs += [b * np.log(b), b * (1 + np.log(b))]
    return np.column_stack(cols), np.array(derivs)
def fit(ns, Qs, hold, **kw):
    ns = np.asarray(ns); Qs = np.asarray(Qs); X, dv = design(ns, **kw); tr = np.array([n not in hold for n in ns])
    c, *_ = np.linalg.lstsq(X[tr], Qs[tr], rcond=None); res = np.abs(X[~tr] @ c - Qs[~tr]) / np.maximum(np.abs(Qs[~tr]), 1e-300)
    return float(dv @ c), float(res.max()) if (~tr).any() else 0.0
def models(own_by_slice, Ny, floor):
    """own_by_slice: {p: [s...]} for p <= Ny/2. Returns dict name -> kwargs for fit()."""
    mult = {}
    for p in range(Ny):
        for s in own_by_slice[p if p <= Ny // 2 else Ny - p]:
            key = round(s, 9); mult[key] = mult.get(key, 0) + 1
    singles = sorted({np.exp(-2 * np.pi * s) for k in own_by_slice for s in own_by_slice[k] if np.exp(-2 * np.pi * s) > floor}, reverse=True)
    n2 = [np.exp(-2 * np.pi * s) for s, m in mult.items() if m > 2 and np.exp(-2 * np.pi * s) > floor]
    top = singles[:6]; prods = sorted({a * b for i, a in enumerate(top) for b in top[i:] if a * b > floor}, reverse=True)
    return {"M1": dict(singles=singles), "M2": dict(singles=singles, n2=n2), "M3": dict(singles=singles, prods=prods),
            "M4": dict(singles=singles, n2=n2, prods=prods)}
def pencil(ns, Qs, rank_tol=1e-11, hold=()):
    ns = np.asarray(ns); Qs = np.asarray(Qs); keep = np.array([n not in hold for n in ns]); n_, q_ = ns[keep], Qs[keep]
    d2 = q_[2:] - 2 * q_[1:-1] + q_[:-2]; L = len(d2) // 3
    Y = np.array([d2[i:i + L + 1] for i in range(len(d2) - L)]); U, sv, Vt = np.linalg.svd(Y, full_matrices=False)
    r = int(np.sum(sv > rank_tol * sv[0])); V = Vt[:r].T; z = np.linalg.eigvals(np.linalg.pinv(V[:-1]) @ V[1:])
    z = np.real(z[(np.abs(z.imag) < 1e-6 * np.abs(z)) & (z.real > 1e-14) & (z.real < 1)])
    if len(z) == 0: return np.nan, np.nan, 0
    qp, res = fit(ns, Qs, set(hold), singles=list(z)); return qp, res, len(z)
