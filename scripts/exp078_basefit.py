"""EXP-078 fit referee (Bridge's held-out design): Q(n) = A n + B + sum_b P_b(n) b^n, b in products of the exact lattice
pole bases a_j = e^{-2 pi s_j} (det H(i s_j) = 0, computed here at 120 dps), P_b polynomials. Fit on n = 1..ntrain,
score max |residual| on held-out n = ntrain+1..90; Q'(1) and Q(1.5) from each fitted (type-0, Carlson-admissible) model.
Accept only when held-out residual and Q'(1) have stopped moving as bases are added. [model: Opus 5.5]"""
import json, mpmath as mp
mp.mp.dps = 120
Lx, Lt, m2, tcut, cutx = 6, 4, mp.mpf("0.5"), 1, (2, 3)
N = Lx * Lt; idx = lambda x, t: t * Lx + x
def H(z):
    M = mp.zeros(N, N)
    for x in range(Lx):
        for t in range(Lt):
            i = idx(x, t); M[i, i] = 4 + m2
            if x + 1 < Lx:
                j = idx(x + 1, t); M[i, j] = -1; M[j, i] = -1
            if t + 1 < Lt:
                j = idx(x, t + 1)
                if t == tcut and x in cutx: M[j, i] = -z; M[i, j] = -1 / z
                else: M[i, j] = -1; M[j, i] = -1
    return M
# z^2 det H(z) is a quartic: interpolate on 5 roots of unity
zs = [mp.exp(2j * mp.pi * k / 5) for k in range(5)]
V = mp.matrix([[z ** p for p in range(5)] for z in zs]); rhs = mp.matrix([z ** 2 * mp.det(H(z)) for z in zs])
c = mp.lu_solve(V, rhs)
roots = mp.polyroots([c[4 - i] for i in range(5)], maxsteps=200, extraprec=200)
pos = sorted([mp.re(r) for r in roots if abs(mp.im(r)) < mp.mpf(10) ** -80 and mp.re(r) > 0])
inside = sorted([r for r in pos if r < 1], reverse=True)          # z = e^{-2 pi s}: the two roots inside the unit circle
a1, a2 = inside[0], inside[1]; s = [-mp.log(a1) / (2 * mp.pi), -mp.log(a2) / (2 * mp.pi)]
print("roots z:", [mp.nstr(r, 15) for r in roots]); print("s1, s2 =", mp.nstr(s[0], 20), mp.nstr(s[1], 20), " 1/a1, 1/a2 =", mp.nstr(1 / a1, 15), mp.nstr(1 / a2, 15))
d = json.load(open("exp078_sectors_hp120.json")); NMAX = max(int(k) for k in d["Q"])
Q = {n: mp.mpf(d["Q"][str(n)]) for n in range(1, NMAX + 1)}
def fit(bases, ntrain):
    cols = [lambda n: mp.mpf(n), lambda n: mp.mpf(1)]
    for (b, deg) in bases:
        for p in range(deg + 1):
            cols.append((lambda b, p: (lambda n: mp.mpf(n) ** p * b ** n))(b, p))
    rows = list(range(1, ntrain + 1))
    raw = [[f(n) for f in cols] for n in rows]
    scale = [max(abs(raw[r][c]) for r in range(len(rows))) for c in range(len(cols))]   # column normalisation
    A = mp.matrix([[raw[r][c] / scale[c] for c in range(len(cols))] for r in range(len(rows))]); y = mp.matrix([Q[n] for n in rows])
    coef = mp.qr_solve(A, y)[0]; coef = [coef[c] / scale[c] for c in range(len(cols))]
    model = lambda x: mp.fsum(coef[i] * cols[i](x) for i in range(len(cols)))
    held = max(abs(model(n) - Q[n]) for n in range(ntrain + 1, NMAX + 1)) if ntrain < NMAX else mp.nan
    train = max(abs(model(n) - Q[n]) for n in rows)
    return mp.diff(model, 1), model(mp.mpf("1.5")), train, held, len(cols)
base3 = [(a1, 1), (a2, 1), (a1 ** 2, 2), (a1 * a2, 2)]
ladder = [
  ("a1(1),a2(1)",            [(a1, 1), (a2, 1)]),
  ("+a1^2(2)",               [(a1, 1), (a2, 1), (a1 ** 2, 2)]),
  ("+a1a2(2)",               base3),
  ("+a2^2(1)",               base3 + [(a2 ** 2, 1)]),
  ("+a2^2(1),a1^3(1)",       base3 + [(a2 ** 2, 1), (a1 ** 3, 1)]),
  ("+a2^2(2),a1^3(2)",       base3 + [(a2 ** 2, 2), (a1 ** 3, 2)]),
  ("+a2^2(2),a1^3(2),a1^2a2(1)", base3 + [(a2 ** 2, 2), (a1 ** 3, 2), (a1**2 * a2, 1)]),
]
def safe(bases, ntrain):
    try: return fit(bases, ntrain)
    except ValueError: return None
for ntrain in (20, 30):
    print(f"--- training n = 1..{ntrain}, held-out n = {ntrain+1}..{NMAX} ---")
    for name, bases in ladder:
        r = safe(bases, ntrain)
        if r is None: print(f'  {name:32s} singular (unidentifiable at {mp.mp.dps} dps)'); continue
        dq, q15, tr, ho, ncol = r
        print(f"  {name:32s} ncol={ncol:2d}  train {mp.nstr(tr, 3):>9}  HELD-OUT {mp.nstr(ho, 3):>9}  Q'(1) = {mp.nstr(dq, 14)}  Q(1.5) = {mp.nstr(q15, 12)}", flush=True)
print("T40 Q_cont: Q'(1) = -1.386871934267, Q(1.5) = -0.403056284")
