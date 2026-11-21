"""T46f grading on MY EXP-082 eps-family (hopping-only weak bond, no diagonal shift): T46f continuation T1+T2 (saddle off) and
T1+Tsad+T2 (saddle on) with its stable lambda-1/4, floor 0; noise_tol sensitivity (x10, x0.1). Delivered code, scratch copy, unchanged
except the noise_tol multiplier hook (a source-level replace in a scratch copy for the sensitivity runs only). [model: Opus 5.5]"""
import sys, os, json, importlib.util, numpy as np
src = open(os.path.join(sys.argv[1], "brief_p2_t46f.py")).read()
def load(name, text):
    p = os.path.join(sys.argv[1], name + ".py"); open(p, "w").write(text)
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
mods = {1.0: load("t46f_x1", src)}
for mult in (10.0, 0.1):
    t = src.replace("deltas = np.where(deltas_raw > noise_tol, deltas_raw, 0.0)", f"noise_tol = noise_tol * {mult}\n        deltas = np.where(deltas_raw > noise_tol, deltas_raw, 0.0)")
    assert t != src; mods[mult] = load(f"t46f_x{mult:g}".replace(".", "p"), t)
def my_family(F, eps):
    op = F.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="eps_family", eps_link=1.0)
    j = op.N_mu - 1; i1, i2 = j * op.N_th + op.N_th // 2, j * op.N_th + op.N_th // 2 - 1
    L = op.L0.tolil(); L[i1, i2] = -eps; L[i2, i1] = -eps; op.L0 = L.tocsc(); return op     # hopping only (EXP-082 definition)
honest_off = {1.0: (-0.339, -0.316), 0.1: (-0.0457, -0.0436), 0.01: (-0.00587, -0.00585), 1e-3: (-7.2e-4, -6.9e-4), 1e-4: (-8.6e-5, -7.4e-5)}
out = {}
for eps, h in honest_off.items():
    row = []
    for mult, F in mods.items():
        eng = F.CenteredQEngine(my_family(F, eps), dq=0.5, Q_max=4.0, K_max=2, r_floor=0.0); _, T1, Ts, T0, T2 = eng.eval_K(2, s_max=2.5, n_s1=6, n_s2=4)
        row.append((mult, T1 + T2, T0 + T2, T1, Ts, T2)); out[f"{eps}|{mult}"] = [T1 + T2, T0 + T2, T1, Ts, T2]
    print(f"eps={eps:g}: honest(off) {h[0]:+.3e}/{h[1]:+.3e} | T46f off(T1+T2): " + " ".join(f"x{m:g} {a:+.4e}" for m, a, *_ in row)
          + " | on(T0+T2): " + " ".join(f"x{m:g} {b:+.4e}" for m, _, b, *_ in row) + f" | (x1: T1 {row[0][3]:+.3e} Tsad {row[0][4]:+.3e} T2 {row[0][5]:+.3e})", flush=True)
json.dump(out, open("t46f_gate_results.json", "w"), indent=1)
