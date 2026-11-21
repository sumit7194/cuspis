"""EXP-081c B2a independent build. Written by a sub-agent from the physics specification in its brief only, without reading or copying any production code (sigma3d.py, exp081*), report.md or any other repository file.

Conventions
-----------
* Sites (x, t), 0 <= x < Lx, 0 <= t < Lt; linear index i = x*Lt + t (t fastest);
  N = Lx*Lt.
* H = (minus discrete Laplacian) + m2 with Dirichlet boundary conditions:
      (H phi)_i = (4 + m2) phi_i - sum_{j nn of i, j in box} T_{ij} phi_j .
  The diagonal is 4 + m2 at every site (edge sites included); neighbours
  outside the box contribute nothing.  So H[i, i] = 4 + m2 and
  H[i, j] = -T_{ij} for in-box nearest neighbours j.
* Twist: z = exp(2*pi*1j*alpha), alpha complex.  For each x in cutx the
  vertical link l = (x, tcut) -> u = (x, tcut+1) carries
      T_{u l} = z      (lower field into the upper site's equation)  => H[u, l] = -z
      T_{l u} = 1/z    (upper field into the lower site's equation)  => H[l, u] = -1/z
  All other hops have T = 1.
* wrong_link=True (must-fail control): the first cut link x0 = cutx[0] is left
  untwisted, and the twist is placed instead on the vertical link
  (x0, tcut+1) -> (x0, tcut+2) with the same convention.  Requires tcut+2 < Lt.

Only numpy and the standard library are used.
"""

import numpy as np


def _idx(x, t, Lt):
    return x * Lt + t


def build_H(Lx, Lt, m2, cutx, tcut, alpha, wrong_link=False):
    """Dense complex128 (N, N) twisted Dirichlet lattice operator."""
    Lx = int(Lx)
    Lt = int(Lt)
    N = Lx * Lt
    cutx = [int(c) for c in cutx]
    z = np.exp(2j * np.pi * complex(alpha))

    # T[(i, j)] = hop factor from site j into equation at site i (default 1).
    twist = {}

    def put_twist(x, t_low):
        lo = _idx(x, t_low, Lt)
        up = _idx(x, t_low + 1, Lt)
        twist[(up, lo)] = z
        twist[(lo, up)] = 1.0 / z

    for k, x in enumerate(cutx):
        if not (0 <= x < Lx):
            raise ValueError("cut x out of range: %d" % x)
        if not (0 <= tcut and tcut + 1 < Lt):
            raise ValueError("tcut out of range")
        if wrong_link and k == 0:
            if not (tcut + 2 < Lt):
                raise ValueError("wrong_link requires tcut + 2 < Lt")
            put_twist(x, tcut + 1)
        else:
            put_twist(x, tcut)

    H = np.zeros((N, N), dtype=np.complex128)
    for x in range(Lx):
        for t in range(Lt):
            i = _idx(x, t, Lt)
            H[i, i] = 4.0 + m2
            for dx, dt in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xn, tn = x + dx, t + dt
                if 0 <= xn < Lx and 0 <= tn < Lt:
                    j = _idx(xn, tn, Lt)
                    H[i, j] = -twist.get((i, j), 1.0)
    return H


if __name__ == "__main__":
    np.set_printoptions(linewidth=140)
    ok_all = True

    def report(name, ok, extra=""):
        global ok_all
        ok_all = ok_all and bool(ok)
        print("[%s] %s %s" % ("PASS" if ok else "FAIL", name, extra))

    cases = [
        dict(Lx=5, Lt=4, m2=0.5, cutx=[1, 2], tcut=1),
        dict(Lx=6, Lt=7, m2=0.0, cutx=[0, 3, 5], tcut=3),
        dict(Lx=3, Lt=5, m2=1.3, cutx=[2], tcut=0),
    ]

    # Test 1: alpha = 0
    for c in cases:
        Lx, Lt, m2 = c["Lx"], c["Lt"], c["m2"]
        H0 = build_H(alpha=0.0, **c)
        N = Lx * Lt
        real = np.max(np.abs(H0.imag)) == 0.0
        sym = np.array_equal(H0, H0.T)
        diag = np.all(np.diag(H0) == 4.0 + m2)
        # Independent neighbour check by coordinate distance.
        offok = True
        for i in range(N):
            xi, ti = divmod(i, Lt)
            for j in range(N):
                if i == j:
                    continue
                xj, tj = divmod(j, Lt)
                expect = -1.0 if abs(xi - xj) + abs(ti - tj) == 1 else 0.0
                if H0[i, j] != expect:
                    offok = False
        report("T1 alpha=0 real/symmetric/diag/offdiag %s" % c,
               real and sym and diag and offok,
               "(real=%s sym=%s diag=%s offdiag=%s)" % (real, sym, diag, offok))

    # Test 2: real alpha -> Hermitian
    for c in cases:
        for a in (0.3, 0.5, 0.77):
            H = build_H(alpha=a, **c)
            err = np.max(np.abs(H - H.conj().T))
            report("T2 Hermitian alpha=%g %s" % (a, c), err < 1e-14, "(max|H-H^dag|=%.2e)" % err)
        # control: complex alpha should NOT be Hermitian (check can fire)
        Hc = build_H(alpha=0.5 + 0.7j, **c)
        errc = np.max(np.abs(Hc - Hc.conj().T))
        report("T2-control complex alpha is non-Hermitian %s" % c, errc > 1e-3, "(max|H-H^dag|=%.2e)" % errc)

    # Test 3: alpha = 1 equals alpha = 0
    for c in cases:
        H0 = build_H(alpha=0.0, **c)
        H1 = build_H(alpha=1.0, **c)
        err = np.max(np.abs(H1 - H0))
        report("T3 alpha=1 == alpha=0 %s" % c, err < 1e-14, "(max diff=%.2e)" % err)

    # Test 4: small example
    Lx, Lt, m2, cutx, tcut = 5, 4, 0.5, [1, 2], 1
    alpha = 0.5 + 0.7j
    z = np.exp(2j * np.pi * alpha)
    H = build_H(Lx, Lt, m2, cutx, tcut, alpha)
    Hw = build_H(Lx, Lt, m2, cutx, tcut, alpha, wrong_link=True)
    print("T4: z = exp(2 pi i alpha) = %r, 1/z = %r" % (z, 1 / z))
    for x in cutx:
        l = _idx(x, tcut, Lt)
        u = _idx(x, tcut + 1, Lt)
        print("  cut x=%d: l=(%d,%d) idx %d, u=(%d,%d) idx %d" % (x, x, tcut, l, x, tcut + 1, u))
        print("    H[u,l] = %r   (expect -z   = %r)" % (H[u, l], -z))
        print("    H[l,u] = %r   (expect -1/z = %r)" % (H[l, u], -1 / z))
        report("T4 entries x=%d" % x,
               abs(H[u, l] + z) < 1e-12 * abs(z) and abs(H[l, u] + 1 / z) < 1e-12 * abs(1 / z))
    diff = np.argwhere(H != Hw)
    print("  wrong_link differs at %d entries:" % len(diff))
    for i, j in diff:
        print("    (%d,%d) site%s<-site%s: correct %r, wrong %r"
              % (i, j, divmod(i, Lt), divmod(j, Lt), H[i, j], Hw[i, j]))
    report("T4 wrong_link differs in exactly 4 entries", len(diff) == 4)

    print("ALL PASS" if ok_all else "SOME FAILED")
