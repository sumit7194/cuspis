"""EXP-067: check of Neon T26 Steps 1-4 (unverified external), own kernel code. On a = 1/2 + iy:
R(p,p') = E(p)E(p') e^{iy(p-p')}/(2cosh((p-p')/2)), E = e^{-(u/2)cosh p}, discretised with weight h (R_h = h R).
(i) R Hermitian, positive definite; (ii) -dR^T/du = (1/4)(w_R v_L^T + v_R w_L^T) with v_L = e^{ap}E, w_R = e^{(1-a)p}E,
v_R = e^{-ap}E... (exact rank-2, from cosh p + cosh p' = 2cosh((p+p')/2)cosh((p-p')/2)); (iii) H = d/du ln det(1 - lam^2 R^T R)
vs lam^2 <v_L, v_L>_M, M = (1 - lam^2 R^T R)^{-1} R^T; (iv) Cauchy-Schwarz ratio |Q|/((pi/cosh pi y) H), Q = lam <w_L, v_L>_M;
(v) B(y) = (1/(8 pi^2 (1/4+y^2))) Int du (-ln det) vs measured |C+| (EXP-065). [model: Opus 5.5]"""
import numpy as np, math
def build(u, y, h=0.1):
    P = math.acosh(max(2.0, 90.0 / u)) + 1.0; p = np.arange(-P, P + 0.5 * h, h)
    E = np.exp(-0.5 * u * np.cosh(p)); dp = p[:, None] - p[None, :]
    R = (E[:, None] * E[None, :]) * np.exp(1j * y * dp) / (2 * np.cosh(0.5 * dp))
    return p, h, R, E
def logdet(u, y):
    p, h, R, E = build(u, y); lam2 = (np.cosh(np.pi * y) / np.pi) ** 2
    s, ld = np.linalg.slogdet(np.eye(len(p)) - lam2 * h * h * (R.T @ R)); return ld, s
if __name__ == "__main__":
    for y in (0.0, 1.0, 2.0, 3.0):
        u = 1.0; p, h, R, E = build(u, y); a = 0.5 + 1j * y; lam = np.cosh(np.pi * y) / np.pi
        herm = np.abs(R - R.conj().T).max(); mineig = np.linalg.eigvalsh(h * R).min()
        # (ii) rank-2 derivative
        du = 1e-5; Rp = build(u + du, y)[2]; Rm = build(u - du, y)[2]
        dRT_fd = -(Rp.T - Rm.T) / (2 * du)
        vL = np.exp(a * p) * E; wR = np.exp((1 - a) * p) * E; vR = np.exp(-a * p) * E; wL = np.exp((a - 1) * p) * E
        dRT_formula = 0.25 * (np.outer(wR, vL) + np.outer(vR, wL))
        # try the natural pairing; report the max mismatch
        mism = np.abs(dRT_fd - dRT_formula).max() / np.abs(dRT_fd).max()
        # (iii) H
        lp, _ = logdet(u + du, y); lm, _ = logdet(u - du, y); H_fd = (lp - lm) / (2 * du)
        Mmat = np.linalg.solve(np.eye(len(p)) - lam ** 2 * h * h * (R.T @ R), h * R.T)
        H_form = lam ** 2 * h * np.vdot(vL, Mmat @ vL)
        # (iv) CS ratio
        Q = lam * h * np.vdot(wL, Mmat @ vL)
        cs = abs(Q) / ((np.pi / np.cosh(np.pi * y)) * abs(H_fd))
        sgn = logdet(u, y)[1]
        print(f"y={y}: (i) max|R-R^dag| {herm:.1e}, min eig(hR) {mineig:.2e} | (ii) rank-2 rel mismatch {mism:.1e} | "
              f"(iii) H_fd {H_fd:+.6e}  lam^2<vL,vL>_M {H_form.real:+.6e}{H_form.imag:+.1e}j | (iv) CS ratio {cs:.3f} (T26: 0.96/0.90/0.62/0.13) | det sign {sgn.real:+.0f}", flush=True)
    meas = {0: 5.997e-3, 1: 9.201e-3, 2: 7.077e-3, 3: 3.664e-3, 4: 1.527e-3}
    for y, c in meas.items():
        qs = np.linspace(-9.0, math.log(max(40.0, np.pi * y + 12)), 500); us = np.exp(qs)
        f = np.array([-logdet(u, y)[0] * u for u in us])        # integrate in q: du = u dq
        I = np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(qs))
        B = I / (8 * np.pi ** 2 * (0.25 + y * y))
        print(f"(v) y={y}: B(y) = {B:.4e}   measured |C+| {c:.4e}   ratio {c/B:.3f}   [{'bound holds' if c <= B else 'BOUND VIOLATED'}]", flush=True)
