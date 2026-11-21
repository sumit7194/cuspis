"""EXP-079 Stage P0 (registered in report.md, 6906e70): the sigma engine on stand-ins, every clause through the engine.
Clauses: G1, F2, G2, P1/P2 (+F1), P3 (+counting must-fail), P4' (+F3), P5 (both outer routes; planted confluent drop must
fire), R (engine vs T40 code, run from a scratch copy), C (2-slice q-convolution; dropped slice must fire). [model: Opus 5.5]"""
import sys, os, math, json, time, importlib.util
import numpy as np, mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sigma_engine as E
res = {}; T0 = time.time()
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)

# ---------------- G1 / F2: 1D pure-gauge toy (no poles; G entire and 1-periodic in a) ----------------
class Toy1D:
    def __init__(self, N=240, m2=0.09):
        H = np.diag(np.full(N, 2 + m2)) - np.eye(N, k=1) - np.eye(N, k=-1)
        self.G1 = np.linalg.inv(H); side = (np.arange(N) >= N // 2).astype(float)
        self.D = side[:, None] - side[None, :]; self.s, self.Rp, self.Rm = [], [], []
    def G(self, a): return np.exp(2j * np.pi * a * self.D) * self.G1
T = Toy1D(); B1 = 2 * T.G1 * T.G1; ld1 = E.logdet(B1)
g1max = 0
for beta in (0.25, 0.5, 0.5 + 1j, 0.5 + 2j):
    d = E.logdet(E.inner_pair(T, T, 1.0, beta)) - ld1; d = complex(d.real, (d.imag + np.pi) % (2 * np.pi) - np.pi)
    g1max = max(g1max, abs(d)); log(f"G1 beta={beta}: logdet ratio {d:.2e}")
K1 = sum(2 * (T.G(a) - T.G1) * (T.G(-a) - T.G1) for a in (np.arange(400) + 0.5) / 400) / 400   # T36's cut-gauge K1 at beta=0
f2 = E.logdet(B1 + K1) - ld1
res["G1"] = dict(max=g1max, pass_=g1max <= 1e-10); res["F2"] = dict(value=str(f2), fires=abs(f2.real - 0.904289) < 1e-3)
log(f"G1 {'PASS' if g1max <= 1e-10 else 'FAIL'} (max {g1max:.1e});  F2 T36 K1: {f2:.6f} [{'FIRES' if res['F2']['fires'] else 'does not fire'}]")

# ---------------- G2: scalar straddle covariance (inner_general), plus its integer-n validation ----------------
mp.mp.dps = 30
r = lambda z: z * (1 - z)
g = lambda z: mp.exp(2j * mp.pi * z) * (1 + r(z)); gt = lambda z: 1 + r(z)
gper = lambda z: g(z - mp.floor(mp.re(z))) if mp.im(z) == 0 else g(z)
gtper = lambda z: gt(z - mp.floor(mp.re(z))) if mp.im(z) == 0 else gt(z)
vmax = 0
for n in (2, 3, 4):
    for q in range(1, n):
        vmax = max(vmax, abs(E.inner_general(g, n, mp.mpf(q) / n) - E.honest_inner_scalar(gper, n, q)))
cmax = 0
for beta in (mp.mpf("0.25"), mp.mpf("0.5"), mp.mpc("0.5", "1")):
    cmax = max(cmax, abs(E.inner_general(g, 1, beta) - mp.exp(2j * mp.pi * beta) * E.inner_general(gt, 1, beta)))
r0 = abs(E.inner_general(lambda z: mp.exp(2j * mp.pi * z), 1, mp.mpf("0.25")) - 2 * mp.exp(2j * mp.pi * mp.mpf("0.25")))
res["G2"] = dict(integer_check=float(vmax), covariance=float(cmax), r0=float(r0), pass_=bool(cmax <= 1e-20 and vmax <= 1e-20))
log(f"G2 integer-n check {float(vmax):.1e}; covariance at n=1 {float(cmax):.1e}; r=0 gives 2e^(2pi i b): {float(r0):.1e} [{'PASS' if res['G2']['pass_'] else 'FAIL'}]")

# ---------------- P1/P2 (+F1): cone function c(a) through ap_single ----------------
# POST-REGISTRATION FIX (run 1 kept as exp079_p0_output_run1_testfn_bug.txt): c has a removable singularity at a = 1/2;
# mpmath gave 0 * tan(pi/2) = 0 there instead of the limit -1/(4 pi^2), which the honest n = 2 sum hits exactly.
c = lambda a: (-1 / (4 * mp.pi ** 2)) if abs(a - mp.mpf("0.5")) < mp.mpf(10) ** -25 else -(mp.mpf(1) / (4 * mp.pi)) * (mp.mpf("0.5") - a) * mp.tan(mp.pi * a)
I1 = E.ap_single(c, 1, f0=mp.mpf(0), f1=mp.mpf(0))
h = mp.mpf("1e-10"); dI = (E.ap_single(c, 1 + h, f0=0, f1=0) - E.ap_single(c, 1 - h, f0=0, f1=0)) / (2 * h)
c3 = E.C_line(lambda b: c(b) ** 3, mpmode=True)
honest_I = max(abs(E.ap_single(c, n, f0=0, f1=0) - mp.fsum(c(mp.mpf(k) / n) for k in range(n)) / n) for n in (2, 3, 4))
res["P1P2"] = dict(I1=float(abs(I1)), dI=float(mp.re(dI)), honest=float(honest_I), F1=float(mp.re(c3)),
                   pass_=bool(abs(I1) <= 1e-20 and abs(dI + mp.mpf(1) / 32) <= 1e-12 and honest_I <= 1e-20))
log(f"P1 I_1[c] = {float(abs(I1)):.1e}; P2 dI/dn = {mp.nstr(mp.re(dI), 15)} (+1/32 -> {float(abs(dI + mp.mpf(1)/32)):.1e}); I_n integer check {float(honest_I):.1e}; "
    f"F1 C[c^3] = {mp.nstr(mp.re(c3), 8)} [{'PASS' if res['P1P2']['pass_'] else 'FAIL'}; F1 {'FIRES' if abs(c3) > 1e-6 else 'no'}]")

# ---------------- P3: K-free through the engine's C_line ----------------
import exp044_det as X
def kap(nt, factor=0.5):
    U = np.linspace(math.log(1e-3), math.log(6.0), nt)
    C = np.array([-factor * E.C_line(lambda a: complex(X.w_scalar(math.exp(u), a)[0]).real) for u in U])
    return X.ratio("S", 3.0, U, C)
k60, k120 = kap(60), kap(120); kmf = kap(120, factor=1.0)
res["P3"] = dict(k60=k60, k120=k120, mustfail=kmf, pass_=abs(k120 / 4.173987 - 1) <= 1e-5)
log(f"P3 kappa/C_T = {k120:.7f} (nt=60: {k60:.7f}) vs 4.173987: rel {abs(k120/4.173987-1):.1e} [{'PASS' if res['P3']['pass_'] else 'FAIL'}]; counting 1: {kmf:.4f} [{'FIRES' if abs(kmf/k120-2)<0.01 else 'no'}]")

# ---------------- P4' (+F3), P5 (+planted), on the 6x4 replica stand-in ----------------
L = E.Lattice(6, 4, 0.5, cut_links=[(2, 1), (3, 1)])
honest = {n: E.honest_Q(L, n).real for n in range(2, 7)}
p4 = {n: abs(E.lattice_Qcont_route_ii(L, n).real - honest[n]) for n in range(2, 7)}
def honest_drop_k0(n):
    Gs = [L.G(k / n) for k in range(n)]; B1 = 2 * Gs[0] * Gs[0]; ld = E.logdet(B1)
    return (sum(E.logdet((2.0 / n) * sum(Gs[k] * Gs[(q - k) % n] for k in range(1, n))) for q in range(n)) - n * ld).real
f3 = {n: abs(honest_drop_k0(n) - honest[n]) for n in (2, 3, 4)}
res["P4"] = dict(err={str(k): v for k, v in p4.items()}, pass_=max(p4.values()) <= 1e-10, F3={str(k): v for k, v in f3.items()})
log(f"P4' route(ii) vs honest n=2..6: max {max(p4.values()):.1e} [{'PASS' if res['P4']['pass_'] else 'FAIL'}]; F3 drop k=0: {min(f3.values()):.1f} [FIRES]")
q15 = E.lattice_Qcont_route_ii(L, 1.5).real
dq_i, t0 = E.lattice_Qprime_route_i(L); dq_i = dq_i.real
dq_ii = {hh: ((E.lattice_Qcont_route_ii(L, 1 + hh) - E.lattice_Qcont_route_ii(L, 1 - hh)) / (2 * hh)).real for hh in (1e-3, 1e-4)}
p5 = abs(q15 + 0.4030563) <= 1e-7 and abs(dq_i + 1.3869) <= 3e-4 and all(abs(v + 1.3869) <= 3e-4 for v in dq_ii.values())
q15_bad = E.lattice_Qcont_route_ii(L, 1.5, drop_confluent=True).real
dq_bad = ((E.lattice_Qcont_route_ii(L, 1 + 1e-4, drop_confluent=True) - E.lattice_Qcont_route_ii(L, 1 - 1e-4, drop_confluent=True)) / 2e-4).real
fires = not (abs(q15_bad + 0.4030563) <= 1e-7 and abs(dq_bad + 1.3869) <= 3e-4)
res["P5"] = dict(Q15=q15, dq_route_i=dq_i, q0_trace=t0.real, dq_route_ii={str(k): v for k, v in dq_ii.items()}, pass_=bool(p5),
                 planted=dict(Q15=q15_bad, dq=dq_bad, fires=bool(fires)))
log(f"P5 Q(1.5) = {q15:.10f} (target -0.4030563 +-1e-7); Q'(1) route(i) = {dq_i:.10f} [q=0 trace {t0.real:.10f}], route(ii) FD = "
    f"{', '.join(f'{v:.10f}' for v in dq_ii.values())} (target -1.3869 +-3e-4) [{'PASS' if p5 else 'FAIL'}]")
log(f"P5 planted (confluent residues of B_n^(0) dropped): Q(1.5) = {q15_bad:.8f}, Q'(1) = {dq_bad:.6f} [{'FIRES' if fires else 'DOES NOT FIRE'}]")

# ---------------- R: engine vs T40's code (scratch copy of its P4' section, transposed link convention) ----------------
scr = "/private/tmp/claude-501/-Users-sumit-Github-corner-function/c9ec831f-1e60-4339-b54f-389fe70e25f7/scratchpad/t40run/t40_p4.py"
spec = importlib.util.spec_from_file_location("t40_p4", scr); T40 = importlib.util.module_from_spec(spec); spec.loader.exec_module(T40)
rmax = 0
for beta in (0.3, 0.5, 0.5 + 1j):
    mine = E.inner_lattice(L, 1.0, beta); theirs = T40.B_cont_p4(1.0, beta)
    rel = np.abs(mine - theirs.T).max() / np.abs(theirs).max(); rmax = max(rmax, rel); log(f"R beta={beta}: max|B_mine - B_T40^T|/max|B| = {rel:.1e}")
res["R"] = dict(max_rel=rmax, pass_=rmax <= 1e-10); log(f"R {'PASS' if rmax <= 1e-10 else 'FAIL'}")

# ---------------- C: 2-slice q-convolution layer ----------------
Ls = [E.Lattice(4, 3, 0.3, cut_links=[(1, 1)]), E.Lattice(4, 3, 0.8, cut_links=[(1, 1)])]; Ny = len(Ls)
def honest_slices(n):
    tot = 0
    for kk in range(Ny):
        B1k = (2.0 / Ny) * sum(Ls[p].G(0.0) * Ls[(kk - p) % Ny].G(0.0) for p in range(Ny)); ld = E.logdet(B1k)
        for q in range(n):
            Bq = (2.0 / (n * Ny)) * sum(Ls[p].G(k / n) * Ls[(kk - p) % Ny].G(((q - k) % n) / n) for p in range(Ny) for k in range(n))
            tot += E.logdet(Bq) - ld
    return tot.real
def cont_slices(n, drop=False):
    tot = 0
    for kk in range(Ny):
        ps = [0] if drop else range(Ny)
        B1k = (2.0 / Ny) * sum(Ls[p].G(0.0) * Ls[(kk - p) % Ny].G(0.0) for p in range(Ny)); ld = E.logdet(B1k)
        tot += E.logdet((1.0 / Ny) * sum(E.inner_pair_beta0(Ls[p], Ls[(kk - p) % Ny], n) for p in ps)) - ld
        for q in range(1, n):
            tot += E.logdet((1.0 / Ny) * sum(E.inner_pair(Ls[p], Ls[(kk - p) % Ny], n, q / n) for p in ps)) - ld
    return tot.real
cerr = max(abs(cont_slices(n) - honest_slices(n)) for n in (2, 3)); cbad = min(abs(cont_slices(n, drop=True) - honest_slices(n)) for n in (2, 3))
res["C"] = dict(err=cerr, dropped=cbad, pass_=cerr <= 1e-10, fires=cbad > 1e-3)
log(f"C 2-slice continuation vs honest (n=2,3): {cerr:.1e} [{'PASS' if cerr <= 1e-10 else 'FAIL'}]; dropped slice: {cbad:.2e} [{'FIRES' if cbad > 1e-3 else 'no'}]")

allpass = all(v.get("pass_", True) for v in res.values())
musts = [res["F2"]["fires"], res["P5"]["planted"]["fires"], res["C"]["fires"]]
log(f"OVERALL P0: {'ACCEPT' if allpass and all(musts) else 'NOT ACCEPTED'}")
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp079_p0_results.json"), "w"), indent=1, default=str)
