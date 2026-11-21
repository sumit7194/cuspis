"""EXP-069 instrument: complex-twist extension of Neon's T25 BIE (copied from neon_work/dkappa/T25_code/run_bie_benchmark.py,
sha256 88c296c1..., read in full and verified at real twist in EXP-066). Changes by Cuspis (Opus 5.5), all marked "# CUSPIS":
complex twist a allowed; modified Bessel functions of complex order via mpmath (scipy iv/kv take real order only); the
'main' benchmark removed. The BIE assembly (K0 kernels, Maue's identity, graded mesh) is unchanged; a enters only via
kappa = -(i/2)cot(pi a) (= -(1/2)tanh(pi y) on a = 1/2 + iy), the G1 subtraction and the projection. [model: Opus 5.5]"""


import time
import json
import numpy as np
from scipy.special import (
    k0, k1, iv, kv, gamma as sp_gamma,
    roots_legendre, roots_jacobi,
)
from scipy.linalg import lu_factor, lu_solve
import mpmath as _mp  # CUSPIS

def _iv(nu, x):  # CUSPIS: complex-order I
    x=np.atleast_1d(np.asarray(x,dtype=float)); return np.array([complex(_mp.besseli(nu, float(t))) for t in x.ravel()]).reshape(x.shape)

def _kv(nu, x):  # CUSPIS: complex-order K
    x=np.atleast_1d(np.asarray(x,dtype=float)); return np.array([complex(_mp.besselk(nu, float(t))) for t in x.ravel()]).reshape(x.shape)



def make_graded_mesh(w, n_layers, sigma=0.22, h_max=0.35):
    half_grade = min(0.5 * w, 1.0)
    pts_tip = np.zeros(n_layers + 1)
    for k in range(1, n_layers + 1):
        pts_tip[k] = half_grade * (sigma ** (n_layers - k))
    left = -w + pts_tip
    right = -pts_tip[::-1]
    if 0.5 * w > half_grade + 1e-12:
        mid_len = w - 2.0 * half_grade
        n_mid = max(2, int(np.ceil(mid_len / h_max)))
        interior = np.linspace(-w + half_grade, -half_grade, n_mid + 1)
        return np.concatenate([left[:-1], interior[:-1], right])
    return np.concatenate([left[:-1], right])


def lobatto_nodes_and_bary(p):
    if p == 1:
        x = np.array([-1.0, 1.0])
    elif p == 2:
        x = np.array([-1.0, 0.0, 1.0])
    else:
        xi, _ = roots_jacobi(p - 1, 1, 1)
        x = np.concatenate(([-1.0], xi, [1.0]))
    w_bary = np.ones(p + 1)
    for i in range(p + 1):
        for j in range(p + 1):
            if i != j:
                w_bary[i] /= (x[i] - x[j])
    return x, w_bary


def eval_lagrange_and_deriv(nodes, w_bary, t):
    t = np.asarray(t, dtype=float)
    p1 = len(nodes)
    nt = len(t)
    L = np.zeros((nt, p1))
    dL = np.zeros((nt, p1))
    for k in range(p1):
        others = np.delete(nodes, k)
        denom = np.prod(nodes[k] - others)
        diff = t[:, None] - others[None, :]
        L[:, k] = np.prod(diff, axis=1) / denom
        dsum = np.zeros(nt)
        for j in range(p1 - 1):
            mask = np.ones(p1 - 1, dtype=bool)
            mask[j] = False
            dsum += np.prod(diff[:, mask], axis=1)
        dL[:, k] = dsum / denom
    return L, dL


def eval_legendre_basis(p_disc, t):
    t = np.asarray(t, dtype=float)
    B = np.zeros((len(t), p_disc))
    B[:, 0] = 1.0
    if p_disc > 1:
        B[:, 1] = t
    for n in range(1, p_disc - 1):
        B[:, n + 1] = ((2 * n + 1) * t * B[:, n] - n * B[:, n - 1]) / (n + 1)
    for n in range(p_disc):
        B[:, n] *= np.sqrt((2 * n + 1) / 2.0)
    return B


def dyadic_gl_01(n_sub=18, n_gl=8):
    gx, gw = roots_legendre(n_gl)
    edges = [0.0] + [2.0 ** (-k) for k in range(n_sub, -1, -1)]
    xs, ws = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        xs.append(0.5 * (a + b) + 0.5 * (b - a) * gx)
        ws.append(0.5 * (b - a) * gw)
    return np.concatenate(xs), np.concatenate(ws)


def self_panel_quad(h, p, p_disc, n_gl=12):
    lob_x, lob_w = lobatto_nodes_and_bary(p)
    u, wu = dyadic_gl_01(n_sub=18, n_gl=8)
    gl_x, gl_w = roots_legendre(n_gl)
    v, wv = 0.5 * (gl_x + 1.0), 0.5 * gl_w

    U, V = u[:, None], v[None, :]
    T = (1.0 - U) * V
    S = T + U
    W_flat = ((wu[:, None] * (1.0 - U)) * wv[None, :] * (k0(h * U) / (2.0 * np.pi))).ravel()

    s_flat, t_flat = (2.0 * S - 1.0).ravel(), (2.0 * T - 1.0).ravel()
    Ls, dLs = eval_lagrange_and_deriv(lob_x, lob_w, s_flat)
    Lt, dLt = eval_lagrange_and_deriv(lob_x, lob_w, t_flat)
    Qs = eval_legendre_basis(p_disc, s_flat)
    Qt = eval_legendre_basis(p_disc, t_flat)

    S_pp = (h ** 2) * ((Ls * W_flat[:, None]).T @ Lt)
    S_dpp = 4.0 * ((dLs * W_flat[:, None]).T @ dLt)
    S_qq = (h ** 2) * ((Qs * W_flat[:, None]).T @ Qt)
    return S_pp + S_pp.T, S_dpp + S_dpp.T, S_qq + S_qq.T


def adj_panel_quad(h1, h2, p, p_disc, n_gl=12):
    lob_x, lob_w = lobatto_nodes_and_bary(p)
    rho, wrho = dyadic_gl_01(n_sub=16, n_gl=8)
    gl_x, gl_w = roots_legendre(n_gl)
    s, ws = 0.5 * (gl_x + 1.0), 0.5 * gl_w

    n_rho = len(rho)
    RHO, SS = rho[:, None], s[None, :]
    S_pp = np.zeros((p + 1, p + 1))
    S_dpp = np.zeros((p + 1, p + 1))
    S_qq = np.zeros((p_disc, p_disc))

    for tri in (1, 2):
        if tri == 1:
            A = np.broadcast_to(RHO, (n_rho, n_gl))
            B = RHO * SS
        else:
            A = RHO * SS
            B = np.broadcast_to(RHO, (n_rho, n_gl))
        dist = h1 * A + h2 * B
        xi1 = (1.0 - 2.0 * A).ravel()
        xi2 = (2.0 * B - 1.0).ravel()
        W = ((wrho[:, None] * RHO) * ws[None, :] * (k0(dist) / (2.0 * np.pi))).ravel()

        L1, dL1 = eval_lagrange_and_deriv(lob_x, lob_w, xi1)
        L2, dL2 = eval_lagrange_and_deriv(lob_x, lob_w, xi2)
        Q1 = eval_legendre_basis(p_disc, xi1)
        Q2 = eval_legendre_basis(p_disc, xi2)

        S_pp += (h1 * h2) * ((L1 * W[:, None]).T @ L2)
        S_dpp += 4.0 * ((dL1 * W[:, None]).T @ dL2)
        S_qq += (h1 * h2) * ((Q1 * W[:, None]).T @ Q2)

    return S_pp, S_dpp, S_qq


def exact_G1_matrix(z1, z2, a, nmax=55):
    r1, r2 = np.abs(z1), np.abs(z2)
    th1, th2 = np.angle(z1), np.angle(z2)
    rmin = np.minimum(r1[:, None], r2[None, :])
    rmax = np.maximum(r1[:, None], r2[None, :])
    dth = th1[:, None] - th2[None, :]
    out = np.zeros((len(z1), len(z2)), dtype=np.complex128)
    for n in range(-nmax, nmax + 1):
        nu = (n + a) if n >= 0 else -(n + a)   # CUSPIS: analytic |n+a| for complex a
        out += np.exp(1j * (n + a) * dth) * _iv(nu, rmin) * _kv(nu, rmax)
    return out / (2.0 * np.pi)


class TwistedIntervalBIE:
    def __init__(self, w, a, n_layers=16, p=5, sigma=0.22, h_max=0.35):
        self.w = float(w)
        self.a = complex(a) if complex(a).imag != 0 else float(np.real(a))  # CUSPIS
        self.n_layers = int(n_layers)
        self.p = int(p)
        self.p_disc = int(p)
        self.sigma = float(sigma)
        self.kappa = -0.5j / np.tan(np.pi * self.a)

        self.nodes = make_graded_mesh(self.w, self.n_layers, self.sigma, h_max=h_max)
        self.n_pan = len(self.nodes) - 1
        self.h = np.diff(self.nodes)
        self.mid = 0.5 * (self.nodes[:-1] + self.nodes[1:])
        self.n_phi = self.n_pan * self.p - 1
        self.n_psi = self.n_pan * self.p_disc
        self.n_gl_far = p + 6
        self._assemble_and_factor()

    def _phi_dof_map(self, ip):
        base = ip * self.p - 1
        loc, glob = [], []
        for k in range(self.p + 1):
            g = base + k
            if 0 <= g < self.n_phi:
                loc.append(k)
                glob.append(g)
        return np.array(loc, dtype=int), np.array(glob, dtype=int)

    def _assemble_and_factor(self):
        p, pd, n_pan = self.p, self.p_disc, self.n_pan
        lob_x, lob_w = lobatto_nodes_and_bary(p)
        gl_x, gl_w = roots_legendre(self.n_gl_far)
        L_gl, dL_gl = eval_lagrange_and_deriv(lob_x, lob_w, gl_x)
        Q_gl = eval_legendre_basis(pd, gl_x)

        # Near-panel composite GL for accurate off-cut evaluation & RHS
        gx_f, gw_f = roots_legendre(16)
        edges = np.linspace(-1.0, 1.0, 5)
        self.fine_x = np.concatenate([0.5*(a+b) + 0.5*(b-a)*gx_f for a, b in zip(edges[:-1], edges[1:])])
        self.fine_w = np.concatenate([0.5*(b-a)*gw_f for a, b in zip(edges[:-1], edges[1:])])
        self.L_fine, _ = eval_lagrange_and_deriv(lob_x, lob_w, self.fine_x)
        self.Q_fine = eval_legendre_basis(pd, self.fine_x)

        A_pp = np.zeros((self.n_phi, self.n_phi), dtype=float)
        S_qq = np.zeros((self.n_psi, self.n_psi), dtype=float)
        M_pq = np.zeros((self.n_phi, self.n_psi), dtype=float)

        for ip in range(n_pan):
            loc, glob = self._phi_dof_map(ip)
            M_loc = (0.5 * self.h[ip]) * ((L_gl * gl_w[:, None]).T @ Q_gl)
            M_pq[np.ix_(glob, np.arange(ip * pd, (ip + 1) * pd))] += M_loc[loc, :]

        for i in range(n_pan):
            loci, globi = self._phi_dof_map(i)
            qi = np.arange(i * pd, (i + 1) * pd)
            Spp, Sdpp, Sqq = self_panel_quad(self.h[i], p, pd)
            A_pp[np.ix_(globi, globi)] += Spp[np.ix_(loci, loci)] + Sdpp[np.ix_(loci, loci)]
            S_qq[np.ix_(qi, qi)] += Sqq

            if i + 1 < n_pan:
                j = i + 1
                locj, globj = self._phi_dof_map(j)
                qj = np.arange(j * pd, (j + 1) * pd)
                Spp, Sdpp, Sqq = adj_panel_quad(self.h[i], self.h[j], p, pd)
                blk_p = Spp[np.ix_(loci, locj)] + Sdpp[np.ix_(loci, locj)]
                A_pp[np.ix_(globi, globj)] += blk_p
                A_pp[np.ix_(globj, globi)] += blk_p.T
                S_qq[np.ix_(qi, qj)] += Sqq
                S_qq[np.ix_(qj, qi)] += Sqq.T

            xi_pts = self.mid[i] + 0.5 * self.h[i] * gl_x
            wi_scale = 0.5 * self.h[i] * gl_w
            for j in range(i + 2, n_pan):
                locj, globj = self._phi_dof_map(j)
                qj = np.arange(j * pd, (j + 1) * pd)
                xj_pts = self.mid[j] + 0.5 * self.h[j] * gl_x
                wj_scale = 0.5 * self.h[j] * gl_w
                dist = np.abs(xi_pts[:, None] - xj_pts[None, :])
                K = k0(dist) / (2.0 * np.pi)
                KW = K * (wi_scale[:, None] * wj_scale[None, :])
                KW_d = K * (gl_w[:, None] * gl_w[None, :])

                Spp = L_gl.T @ KW @ L_gl
                Sdpp = dL_gl.T @ KW_d @ dL_gl
                Sqq = Q_gl.T @ KW @ Q_gl

                blk_p = Spp[np.ix_(loci, locj)] + Sdpp[np.ix_(loci, locj)]
                A_pp[np.ix_(globi, globj)] += blk_p
                A_pp[np.ix_(globj, globi)] += blk_p.T
                S_qq[np.ix_(qi, qj)] += Sqq
                S_qq[np.ix_(qj, qi)] += Sqq.T

        N = self.n_phi + self.n_psi
        Mat = np.zeros((N, N), dtype=np.complex128)
        Mat[:self.n_phi, :self.n_phi] = A_pp
        Mat[:self.n_phi, self.n_phi:] = self.kappa * M_pq
        Mat[self.n_phi:, :self.n_phi] = self.kappa * M_pq.T
        Mat[self.n_phi:, self.n_phi:] = S_qq

        d_scale = np.sqrt(np.maximum(np.abs(np.diag(Mat)), 1e-300))
        self.inv_d = 1.0 / d_scale
        Mat_eq = Mat * (self.inv_d[:, None] * self.inv_d[None, :])
        self.lu = lu_factor(Mat_eq)
        self.gl_x, self.gl_w, self.L_gl, self.Q_gl = gl_x, gl_w, L_gl, Q_gl

    def eval_G_matrix(self, z1, z2):
        m2 = len(z2)
        zp_x, zp_y = np.real(z2), np.imag(z2)
        z1_x, z1_y = np.real(z1), np.imag(z1)
        N = self.n_phi + self.n_psi
        rhs = np.zeros((N, m2), dtype=np.complex128)
        pd = self.p_disc

        for ip in range(self.n_pan):
            loc, glob = self._phi_dof_map(ip)
            dmin = np.min(np.hypot(np.maximum(0.0, np.maximum(self.nodes[ip] - zp_x, zp_x - self.nodes[ip+1])), zp_y))
            if dmin < 1.5 * self.h[ip]:
                qx, qw, Lq, Qq = self.fine_x, self.fine_w, self.L_fine, self.Q_fine
            else:
                qx, qw, Lq, Qq = self.gl_x, self.gl_w, self.L_gl, self.Q_gl
            x_pts = self.mid[ip] + 0.5 * self.h[ip] * qx
            wx = 0.5 * self.h[ip] * qw
            dx = x_pts[:, None] - zp_x[None, :]
            dy = -zp_y[None, :]
            rr = np.hypot(dx, dy)
            G0_mat = k0(rr) / (2.0 * np.pi)
            dG0_mat = (-dy / (2.0 * np.pi * rr)) * k1(rr)
            rhs[glob, :] += Lq[:, loc].T @ (wx[:, None] * dG0_mat)
            q_sl = slice(self.n_phi + ip * pd, self.n_phi + (ip + 1) * pd)
            rhs[q_sl, :] += Qq.T @ (wx[:, None] * G0_mat)

        sol = lu_solve(self.lu, rhs * self.inv_d[:, None]) * self.inv_d[:, None]
        phi, psi = sol[:self.n_phi, :], sol[self.n_phi:, :]

        G_mat = (k0(np.abs(z1[:, None] - z2[None, :])) / (2.0 * np.pi)).astype(np.complex128)
        for ip in range(self.n_pan):
            loc, glob = self._phi_dof_map(ip)
            dmin = np.min(np.hypot(np.maximum(0.0, np.maximum(self.nodes[ip] - z1_x, z1_x - self.nodes[ip+1])), z1_y))
            if dmin < 1.5 * self.h[ip]:
                qx, qw, Lq, Qq = self.fine_x, self.fine_w, self.L_fine, self.Q_fine
            else:
                qx, qw, Lq, Qq = self.gl_x, self.gl_w, self.L_gl, self.Q_gl
            x_pts = self.mid[ip] + 0.5 * self.h[ip] * qx
            wx = 0.5 * self.h[ip] * qw
            phi_vals = Lq[:, loc] @ phi[glob, :]
            psi_vals = Qq @ psi[ip * pd:(ip + 1) * pd, :]
            dx = z1_x[:, None] - x_pts[None, :]
            dy = z1_y[:, None]
            rr = np.hypot(dx, dy)
            G0_ev = k0(rr) / (2.0 * np.pi)
            dyxi_G0 = (dy / (2.0 * np.pi * rr)) * k1(rr)
            G_mat += (dyxi_G0 * wx[None, :]) @ phi_vals - (G0_ev * wx[None, :]) @ psi_vals
        return G_mat

    def extract_DeltaC_and_E(self, R, theta_max=0.85 * np.pi, K_modes=5, n_ang=25, proj_norm_scale=1.0):
        r1, r2 = 0.8 * R, R
        thetas = np.linspace(-theta_max, theta_max, n_ang)
        z1 = r1 * np.exp(1j * thetas)
        z2 = r2 * np.exp(1j * thetas)

        Greg = self.eval_G_matrix(z1, z2) - exact_G1_matrix(z1, z2, self.a, nmax=55)
        modes = np.arange(-K_modes, K_modes + 1)
        V1 = np.exp(1j * thetas[:, None] * (modes[None, :] + self.a))
        V2 = np.exp(-1j * thetas[:, None] * (modes[None, :] + self.a))
        A = (np.linalg.pinv(V1) @ Greg @ np.linalg.pinv(V2).T) * proj_norm_scale

        idx0, idxm1 = K_modes, K_modes - 1
        Ia1, Ia2, I1ma2 = _iv(self.a, r1)[0], _iv(self.a, r2)[0], _iv(1.0 - self.a, r2)[0]  # CUSPIS
        DeltaC = A[idx0, idx0] / (Ia1 * Ia2)
        c_0m1 = A[idx0, idxm1] / (Ia1 * I1ma2)
        E_val = c_0m1 / (2.0 * sp_gamma(1.0 + self.a) * sp_gamma(2.0 - self.a))
        return DeltaC, E_val  # CUSPIS: complex values kept


def run_ladder(w, a, proj_norm_scale=1.0):
    """
    3-rung refinement ladder in each of:
      - mesh grading L in {12, 16, 20} (at p = 5, R_frac = 0.16)
      - panel order  p in {4, 5, 6}    (at L = 16, R_frac = 0.16)
      - proj radius  R_frac in {0.10, 0.16, 0.22} (at finest L = 20, p = 6)
    Returns dict with best estimate (at L=20, p=6, R_frac=0.16) and conservative error bar
    = spread_L + spread_p + spread_R.
    """
    w_eff = min(w, 1.0)
    R_mid = 0.16 * w_eff
    R_rungs = [0.10 * w_eff, 0.16 * w_eff, 0.22 * w_eff]

    # L ladder at p = 5
    dC_L, E_L = [], []
    for L in (12, 16, 20):
        s = TwistedIntervalBIE(w, a, n_layers=L, p=5)
        dC, E = s.extract_DeltaC_and_E(R_mid, proj_norm_scale=proj_norm_scale)
        dC_L.append(dC)
        E_L.append(E)

    # p ladder at L = 16 (reuse middle rung p = 5 from above)
    dC_p = [None, dC_L[1], None]
    E_p = [None, E_L[1], None]
    for idx, p in ((0, 4), (2, 6)):
        s = TwistedIntervalBIE(w, a, n_layers=16, p=p)
        dC, E = s.extract_DeltaC_and_E(R_mid, proj_norm_scale=proj_norm_scale)
        dC_p[idx], E_p[idx] = dC, E

    # Finest (L = 20, p = 6) with 3 projection radii R_rungs
    s_fine = TwistedIntervalBIE(w, a, n_layers=20, p=6)
    dC_R, E_R = [], []
    for R in R_rungs:
        dC, E = s_fine.extract_DeltaC_and_E(R, proj_norm_scale=proj_norm_scale)
        dC_R.append(dC)
        E_R.append(E)

    # Best value: finest (L=20, p=6, R_mid)
    dC_best = dC_R[1]
    E_best = E_R[1]

    # Conservative error bar: sum of top-rung spreads across L, p, and full spread across R
    err_dC_L = max(abs(dC_L[2] - dC_L[1]), abs(dC_best - dC_p[2]))
    err_dC_p = max(abs(dC_p[2] - dC_p[1]), abs(dC_best - dC_L[2]))
    err_dC_R = max(dC_R) - min(dC_R)
    err_dC = err_dC_L + err_dC_p + err_dC_R

    err_E_L = max(abs(E_L[2] - E_L[1]), abs(E_best - E_p[2]))
    err_E_p = max(abs(E_p[2] - E_p[1]), abs(E_best - E_L[2]))
    err_E_R = max(E_R) - min(E_R)
    err_E = err_E_L + err_E_p + err_E_R

    return {
        "w": w, "a": a,
        "DeltaC": dC_best, "err_DeltaC": err_dC,
        "E": E_best, "err_E": err_E,
        "dC_L": dC_L, "dC_p": dC_p, "dC_R": dC_R,
        "E_L": E_L, "E_p": E_p, "E_R": E_R,
    }


