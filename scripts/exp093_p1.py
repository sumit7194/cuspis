"""EXP-093 (P-1) grader, registration notes/EXP-093_094_registration.md (f874dac, amendment 1 e8a1c06). row(P) is exp089_wall.row
VERBATIM; ck() searches exp081d_results/, then exp081d_results/air_pull/ (the validated pull of the Air's W2P8 route), then exp081c_results/.
Controls first (hard stop): row(4), row(6) bitwise vs exp089_wall.json; G_b(8) bitwise vs exp093_gb8.json; W2P8 checkpoint has n1c + 48 nodes;
Air route gates from the pulled .out (B2b/t0/residue PASS, no FAIL/STOP, all unconverged 0); Air runner rc 0; stale-file guard
(argv[1] = the checkpoint's mtime on the Air, '%F %T', must be later than the route's start line). [model: Opus 5.5]"""
import os, sys, json, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results"); AP = os.path.join(D, "air_pull")
import exp081d_analyze as AN, exp081b_run as Rn
c = -0.11410550636913405; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:62s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def ck(W, P):
    for d in (D, AP, os.path.join(HERE, "exp081c_results")):
        f = os.path.join(d, f"sigma_W{W}_P{P}_box{P}_c2_cp12_sc3.0_dd0_ckpt.json")
        if os.path.exists(f):
            st = json.load(open(f))
            if "n1c" in st: return st
    raise FileNotFoundError(f"no n1c checkpoint for W{W}P{P}")
def row(P):                                                        # verbatim from exp089_wall.row
    Ny = 4 * P; kap = Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=2, W2=4, Wbox=P); nm = 1.0 / (Ny * (1 / 2 - 1 / 4) * kap)
    s2, s4 = AN.S_T(ck(2, P)), AN.S_T(ck(4, P)); g2, g4 = (json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json"))) for W in (2, 4))
    R = -(s2["S_T0"] - s4["S_T0"]) * nm; YA = -(g2["X_cA"] - g4["X_cA"]) * nm; YB = -(c / 2) * (g2["Sigma3D"] - g4["Sigma3D"]) * nm
    return dict(P=P, kappa=kap, norm=nm, R=R, YA=YA, YB=YB, rhoA=R - YA, Gb=YB - YA)
ref = json.load(open(os.path.join(D, "exp089_wall.json"))); gb8 = json.load(open(os.path.join(D, "exp093_gb8.json")))
K = ("kappa", "norm", "R", "YA", "YB", "rhoA", "Gb")
r4, r6 = row(4), row(6)
check("KA: row(4) reproduces exp089_wall.json bitwise", all(r4[k] == ref["r4"][k] for k in K))
check("KA: row(6) reproduces exp089_wall.json bitwise", all(r6[k] == ref["r6"][k] for k in K))
assert not os.path.exists(os.path.join(D, "sigma_W2_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json")), "a local W2P8 file would shadow the Air pull"
st = json.load(open(os.path.join(AP, "sigma_W2_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json")))
ng = sum(1 for k in st if k.startswith("g|")); check("W2P8 (Air pull): n1c present, 48 g nodes", "n1c" in st and ng == 48, f"nodes {ng}")
out = open(os.path.join(AP, "air_route_W2P8.out")).read()
unc = [int(x) for x in re.findall(r"unconverged (\d+)", out)]
check("Air route: B2b, t0 refined, residue all PASS", out.count("[PASS]") >= 2 and "B2b" in out and "-> PASS" in out and "B2b" not in "".join(l for l in out.splitlines() if "B2b" in l and "PASS" not in l))
check("Air route: no FAIL / STOP / NON-CONVERGED lines", not re.search(r"FAIL|STOP|NON-CONVERGED|Traceback", out))
check("Air route: census, every unconverged count is 0", len(unc) > 0 and max(unc) == 0, f"{len(unc)} counts")
run = open(os.path.join(AP, "air_run_093.txt")).read()
check("Air runner: air_route_W2P8 rc 0", "air_route_W2P8 rc 0" in run)
m = re.search(r"air_route_W2P8 start (\S+ \S+)", run); mt = sys.argv[1] if len(sys.argv) > 1 else ""
check("stale-file guard: Air checkpoint mtime later than route start", bool(m) and mt > m.group(1), f"mtime {mt} start {m.group(1) if m else None}")
r8 = row(8)
check("G_b(8) from row(8) equals exp093_gb8.json bitwise", r8["Gb"] == gb8["r8"]["Gb"] and r8["norm"] == gb8["r8"]["norm"])
if FAIL: print("STOP: controls failed -> no grading", FAIL); sys.exit(1)
dG = r6["Gb"] - r8["Gb"]; f = -(r8["rhoA"] - r6["rhoA"]) / dG
inc = dG < 0.285; ra = r8["rhoA"]
print(f"\nP=8: R {r8['R']:.6f} Y_A {r8['YA']:.6f} Y_bulk {r8['YB']:.6f} rho_A {ra:+.6f} G_b {r8['Gb']:.6f} (kappa {r8['kappa']:.9f})")
print(f"P=6: rho_A {r6['rhoA']:+.6f} G_b {r6['Gb']:.6f};  G_b(6) - G_b(8) = {dG:+.6f} (f INCONCLUSIVE if < 0.285)")
print(f"ITEM rho_A(8): sealed -0.05 +- 0.04 -> {'PASS' if -0.09 <= ra <= -0.01 else 'FAIL'} ([-0.09, -0.01]); +-2 sigma [-0.13, +0.03]: {'inside' if -0.13 <= ra <= 0.03 else 'outside'}")
if inc: print(f"ITEM f(6->8): INCONCLUSIVE (drop {dG:.4f} < 0.285); descriptive f = {f:+.4f}")
else: print(f"ITEM f(6->8) = {f:+.4f}: sealed 0.21 +- 0.08 -> {'PASS' if 0.13 <= f <= 0.29 else 'FAIL'} ([0.13, 0.29]); +-2 sigma [0.05, 0.37]: {'inside' if 0.05 <= f <= 0.37 else 'outside'}")
print(f"ITEM G_b(8) (graded earlier): {r8['Gb']:.4f} -> {'PASS' if gb8['Gb_pass_1s'] else 'FAIL'}")
json.dump(dict(r6=r6, r8=r8, dG=dG, f=f, f_inconclusive=inc, rhoA8_pass_1s=-0.09 <= ra <= -0.01, rhoA8_in_2s=-0.13 <= ra <= 0.03,
               f_pass_1s=(not inc) and 0.13 <= f <= 0.29, f_in_2s=(not inc) and 0.05 <= f <= 0.37, air_ckpt_mtime=mt, failed=FAIL),
          open(os.path.join(D, "exp093_p1.json"), "w"), indent=1, default=float)
