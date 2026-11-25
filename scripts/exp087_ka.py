"""EXP-087 KAs (registration notes/EXP-087_registration.md), tiny boxes + W4P4. Each row can fail. [model: Opus 5.5]
0 planted refusal; 1 bitwise invariance (no clusters) W6P3 tiny + W4P4; 2 TRUTH KA W8P3 vs rad-sweep -35.769860 (1e-5);
3 CONSISTENCY KA (fix vs bug MODEL) W10P3 vs artifact -35.82407 (1e-4); 4 fixed - unfixed == -artifact delta at W8P3 (1e-5 abs)."""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:66s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
# 0 planted refusal
try: S3.refuse_087(1j * 1.0, 0.5 * 2e-6 + 1e-5, [1j * 1.0, 1j * (1 + 2e-6)], [1j * 1.0, 1j * (1 + 2e-6), 1j * (1 + 5e-6), -1j * 1.0]); r0 = False
except S3.PoleGateError: r0 = True
check("0 planted refusal: third pole inside 1.5*rc must RAISE", r0)
try: S3.refuse_087(1j * 1.0, 0.5 * 2e-6 + 1e-5, [1j * 1.0, 1j * (1 + 2e-6)], [1j * 1.0, 1j * (1 + 2e-6), 1j * 1.01, -1j * 1.0]); r1 = True
except S3.PoleGateError: r1 = False
check("0 clean case: no non-member nearby must NOT raise", r1)
def t0_of(W, P, Wb, Ny, on, lowrank=False):
    Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=lowrank, rank_drop=0)
    B1 = S.B1(); A = [np.linalg.inv(B1[k]) for k in range(Ny)]; out = {}
    for flag in on:
        S3.INNER_BETA0_087 = flag; dB0 = S.inner_beta0(1.0, dn=True); out[flag] = float(sum(np.trace(A[k] @ dB0[k]).real for k in range(Ny)))
    S3.INNER_BETA0_087 = False; return out
r = t0_of(6, 3, 6, 16, (False, True)); check("1 bitwise invariance W6P3 tiny (no clusters): on == off", r[True] == r[False], f"{r[False]!r} vs {r[True]!r}")
r = t0_of(4, 4, 4, 16, (False, True), lowrank=True); check("1 bitwise invariance W4P4 (production size, no clusters): on == off", r[True] == r[False], f"{r[False]!r} vs {r[True]!r}")
r8 = t0_of(8, 3, 8, 16, (False, True))
check("  (unfixed W8P3 reproduces the stored sweep value -35.787540656)", abs(r8[False] + 35.787540656) <= 1e-8, f"{r8[False]!r}")
check("2 TRUTH KA W8P3: fixed t0 == -35.769860 (rad-sweep converged) to 1e-5", abs(r8[True] + 35.769860) <= 1e-5, f"{r8[True]!r}")
check("4 fixed - unfixed == -artifact delta (+0.017677) at W8P3 to 1e-5", abs((r8[True] - r8[False]) - 0.017677) <= 1e-5, f"{r8[True] - r8[False]:+.7f}")
r10 = t0_of(10, 3, 10, 16, (False, True))
check("3 CONSISTENCY KA (fix vs bug MODEL) W10P3: fixed == -35.82407 to 1e-4", abs(r10[True] + 35.82407) <= 1e-4, f"{r10[True]!r} (unfixed {r10[False]!r}; diff {r10[True]-r10[False]:+.6f} vs model +0.101513)")
print(f"\nEXP-087 KAs: {'ALL PASS' if not FAIL else 'FAIL: ' + ', '.join(FAIL)}"); sys.exit(1 if FAIL else 0)
