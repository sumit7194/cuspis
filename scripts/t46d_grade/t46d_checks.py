"""Grading checks for T46d (Neon, UNVERIFIED): (a) I_f1 / act_tol effect on T46c-graded numbers; (b) pure-gauge g(s) at
production size, s = 2..2.5 (exact answer 0); (c) T0 local slopes vs Q_max and dq. Uses the delivered code unchanged."""
import sys, time; sys.path.insert(0, sys.argv[1]); import numpy as np, brief_p2_t46c as C, brief_p2_t46d as D
part = sys.argv[2]
if part == "a":
    print("(a) same config N_th=16 mu_max=4 dq=0.25 Q=16, s_max=2.5, n_s=(8,4): T0 | T2", flush=True)
    opc = C.ConformalEllipticModel(N_th=16, mu_max=4.0); ec = C.CenteredQEngine(opc, dq=0.25, Q_max=16.0, K_max=16)
    opd = D.ConformalEllipticModel(N_th=16, mu_max=4.0)
    ed1 = D.CenteredQEngine(opd, dq=0.25, Q_max=16.0, K_max=16, act_tol=1e-11); ed0 = D.CenteredQEngine(opd, dq=0.25, Q_max=16.0, K_max=16, act_tol=0.0)
    for z in (2.0, 4.0, 6.0, 8.0):
        K = int(round(z / 0.5)); rc = ec.eval_K(K, s_max=2.5, n_s1=8, n_s2=4); r1 = ed1.eval_K(K, s_max=2.5, n_s1=8, n_s2=4); r0 = ed0.eval_K(K, s_max=2.5, n_s1=8, n_s2=4)
        print(f"  z={z:g}: T46c T0 {rc[3]:+.6f} T2 {rc[4]:+.6f} | T46d act1e-11 T0 {r1[3]:+.6f} T2 {r1[4]:+.6f} | T46d act0 T0 {r0[3]:+.6f} T2 {r0[4]:+.6f}", flush=True)
if part == "b":
    print("(b) pure gauge (closed t=0 cocycle) through production pair_delta_B_exact, k=1, dq=0.5, Q=16: g(s) (exact 0)", flush=True)
    for Nth in (16, 24):
        op = D.ConformalEllipticModel(N_th=Nth, mu_max=3.5, cut_mode="closed_loop"); eng = D.CenteredQEngine(op, dq=0.5, Q_max=16.0, K_max=2, act_tol=0.0)
        m_lo = 1 - eng.M_q; wq = eng.dq / (2 * np.pi)
        B1 = sum(wq * 2.0 * (eng._get_qd(m)['G0'] * eng._get_qd(1 - m)['G0']) for m in range(m_lo, m_lo + 2 * eng.M_q)); cho = D.linalg.cho_factor(B1)
        row = []
        for s in (1.0, 1.5, 2.0, 2.25, 2.5):
            beta = 0.5 + 1j * s
            Br = B1 + sum(wq * D.pair_delta_B_exact(eng._get_qd(m), eng._get_qd(1 - m), 1.0, beta) for m in range(m_lo, m_lo + 2 * eng.M_q))
            up, um = np.exp(1j * beta * op.Phi), np.exp(-1j * beta * op.Phi); sg, lg = np.linalg.slogdet(D.linalg.cho_solve(cho, (up[:, None] * Br) * um[None, :]))
            row.append(f"s={s:g}:{lg:+.1e}")
        print(f"  N_th={Nth} (N={op.N}, W_cut={op.W_cut}): " + " ".join(row), flush=True)
if part == "c":
    print("(c) T0 = T1 + Tsad local slopes vs (dq, Q_max), mu_max=3.5", flush=True)
    for Nth, cfgs in ((16, [(0.5, 16), (0.5, 32), (0.5, 48), (0.25, 32)]), (24, [(0.5, 16), (0.5, 32), (0.5, 48)])):
        op = D.ConformalEllipticModel(N_th=Nth, mu_max=3.5)
        for dq, Q in cfgs:
            t0 = time.time(); zs = [4.0, 6.0, 8.0, 10.0]; eng = D.CenteredQEngine(op, dq=dq, Q_max=Q, K_max=int(round(10 / (2 * dq))), act_tol=0.0)
            T0 = [eng.eval_K(int(round(z / (2 * dq))), s_max=0.0)[3] for z in zs]
            sl = np.diff(T0) / np.diff(np.log(zs))
            print(f"  N_th={Nth} dq={dq} Q={Q}: T0 " + " ".join(f"{z:g}:{v:+.5f}" for z, v in zip(zs, T0)) + " | slopes [4,6] {:+.4f} [6,8] {:+.4f} [8,10] {:+.4f}".format(*sl) + f" ({time.time()-t0:.0f}s)", flush=True)
