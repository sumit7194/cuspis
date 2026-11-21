"""Sealed-derivation check (b): T46d engine under P1 (n->1 at fixed r, no threshold: every 1e-10 -> 0.0) + P2 (lambda - 1/4
from S - 1/4 = M-^(1/2)[(Gs-Ga)/2 - Gs Ga]M-^(-1/2), Gs - Ga from the cross-cut block directly; r = (4 lam-1)/(2 sqrt lam+1)^2;
f = 1/[(lam-1/4) + 1/(4 sin^2 pi a)]) on the T46d-grade configuration, vs the delivered threshold code. Scratch only."""
import sys, os, importlib.util, numpy as np
from scipy import linalg, sparse
from scipy.sparse.linalg import splu
src = open(os.path.join(sys.argv[1], "brief_p2_t46d.py")).read()
def load(name, text):
    p = os.path.join(sys.argv[2], name + ".py"); open(p, "w").write(text)
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
D0 = load("t46d_orig", src); P = load("t46d_p1p2", src.replace("1e-10", "0.0"))
class LamArr(np.ndarray):
    def __new__(cls, lam, lm14): o = np.asarray(lam, float).view(cls); o.lm14 = np.asarray(lm14, float); return o
    def __array_finalize__(self, obj): self.lm14 = getattr(obj, "lm14", None)
    def __getitem__(self, idx):
        out = super().__getitem__(idx)
        if isinstance(out, LamArr) and self.lm14 is not None: out.lm14 = self.lm14[idx]
        return out
def mode_params(lams):
    lm = getattr(lams, "lm14", None); lam = np.asarray(lams, float)
    if lm is None: lm = lam - 0.25
    lm = np.maximum(lm, 0.0); lam = 0.25 + lm; sq = np.sqrt(lam)
    rho = 4 * lm / (2 * sq + 1) ** 2
    return sq, rho, 2.0 / (sq * (2 * sq + 1)), -2.0 / (sq * (2 * sq + 1) ** 2), 2.0 / ((2 * sq + 1) ** 2)
def f_h_eval(lams, alpha):
    if abs(alpha - round(np.real(alpha))) < 1e-13 and abs(np.imag(alpha)) < 1e-13:
        z = np.zeros(len(lams), complex); return z, z
    lm = getattr(lams, "lm14", None); lm = np.asarray(lams, float) - 0.25 if lm is None else np.maximum(lm, 0.0)
    sn = np.sin(np.pi * alpha); gamma = 0.5j * np.cos(np.pi * alpha) / sn
    den = lm + 1.0 / (4.0 * sn * sn); return 1.0 / den, gamma / den
def solve_q(self, q, act_tol=0.0):
    Hq = self.L0 + sparse.diags((q ** 2) * self.weights, format='csc'); G0 = splu(Hq).solve(np.eye(self.N))
    GPs, GPa = G0 @ self.P_s, G0 @ self.P_a; Gs, Ga = self.P_s.T @ GPs, self.P_a.T @ GPa
    t, b = np.array(self.cut_top), np.array(self.cut_bot); X = G0[np.ix_(t, b)]; dsa = X + X.T     # Gs - Ga, no subtraction
    Gs, Ga, dsa = 0.5 * (Gs + Gs.T), 0.5 * (Ga + Ga.T), 0.5 * (dsa + dsa.T)
    Mm = 0.5 * np.eye(self.W_cut) - Ga; em, Qm = linalg.eigh(Mm); em = np.maximum(em, 1e-15)
    Mh, Mih = (Qm * np.sqrt(em)) @ Qm.T, (Qm / np.sqrt(em)) @ Qm.T
    T = Mh @ (0.5 * dsa - Gs @ Ga) @ Mih; lm, Y = linalg.eigh(0.5 * (T + T.T))
    return dict(q=q, G0=G0, lams=LamArr(0.25 + np.maximum(lm, 0.0), lm), Phi_s=GPs @ (Mh @ Y), Psi_a=GPa @ (Mih @ Y), lm_raw=lm)
P.mode_params = mode_params; P.f_h_eval = f_h_eval; P.BaseSymmetricCutOperator.solve_q = solve_q
for name, M in (("delivered (threshold 1e-10)", D0), ("P1+P2 (no threshold, stable lambda-1/4)", P)):
    op = M.ConformalEllipticModel(N_th=16, mu_max=4.0); eng = M.CenteredQEngine(op, dq=0.25, Q_max=16.0, K_max=16, act_tol=0.0)
    if M is P:
        lm = np.concatenate([q['lm_raw'] for q in eng.qcache]); print(f"  P2 spectrum: {lm.size} modes; lambda-1/4 <= 0 (round-off floor): {int(np.sum(lm <= 0))}; "
              f"0 < lambda-1/4 < 1e-14: {int(np.sum((lm > 0) & (lm < 1e-14)))}; min positive {lm[lm > 0].min():.1e}", flush=True)
    try:
        out = [eng.eval_K(K, s_max=2.5, n_s1=8, n_s2=4) for K in (8, 16)]
        print(f"  {name}: z=4 T0 {out[0][3]:+.6f} T2 {out[0][4]:+.6f} | z=8 T0 {out[1][3]:+.6f} T2 {out[1][4]:+.6f}", flush=True)
    except Exception as e: print(f"  {name}: FAILED {type(e).__name__}: {e}", flush=True)
