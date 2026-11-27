"""EXP-095 grader (registration notes/EXP-095_registration.md, 83566e3; SEALED-READ). Written 2026-11-27 and committed WITHOUT running:
it runs only at the opening (path S after a sealed prediction, or path D descriptive), on the Bridge's word. [model: Opus 5.5]
row(P) is exp089_wall.row VERBATIM (as in exp093_p1.py); ck() searches exp081d_results/, then exp081d_results/air_pull/ (the validated pulls:
W2P10 from the Air's main folder, W4P10 from ~/GitHub/fleet-air/corner_function_095b), then exp081c_results/.
Controls first, hard stop (exit 1, nothing graded):
  0. sealed sha: the four outputs (2 GEOM G files, 2 pulled checkpoints) match exp095_sealed_sha256.txt (a mismatch is a protocol FAIL);
  1. row(4), row(6) bitwise vs exp089_wall.json; row(8) bitwise vs exp093_p1.json's r8;
  2. no local W2P10/W4P10 checkpoint shadows the pulls; each pulled checkpoint has n1c + 48 g nodes;
  3. each Air route .out: B2b / t0 refined / residue PASS, no FAIL/STOP/NON-CONVERGED/Traceback, all unconverged counts 0;
  4. runner rc 0: air_route_W2P10 in air_run_095.txt; air_route_W4P10 in air_run_095b.txt ONLY (the main runner's W4P10 STOP rc 98 is the
     ended DUPLICATE, not a result; its files are quarantined on the Air);
  5. stale-file guard: argv[1], argv[2] = the Air mtimes ('%F %T') of the W2P10 / W4P10 checkpoints, each later than its route start line;
  6. G_W2P10 / G_W4P10: 'failed' empty.
Usage: exp095_p1.py "<W2P10 ckpt mtime>" "<W4P10 ckpt mtime>" [S|D]   (S = graded against the sealed bands passed via exp095_seal.json; D = descriptive)"""
import os, sys, json, re, hashlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results"); AP = os.path.join(D, "air_pull")
import exp081d_analyze as AN, exp081b_run as Rn
c = -0.11410550636913405; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:66s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
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
if len(sys.argv) < 3: print(__doc__); sys.exit(2)
MODE = sys.argv[3] if len(sys.argv) > 3 else "D"
CK = {W: f"sigma_W{W}_P10_box10_c2_cp12_sc3.0_dd0_ckpt.json" for W in (2, 4)}
# ---- 0. sealed sha (before ANY file is parsed)
sealed = {}
for line in open(os.path.join(D, "exp095_sealed_sha256.txt")):
    if line.strip() and not line.startswith("#"): h, p = line.split()[:2]; sealed[os.path.basename(p)] = h
want = {"G_W2P10.json": os.path.join(D, "exp085c", "G_W2P10.json"), "G_W4P10.json": os.path.join(D, "exp085c", "G_W4P10.json"),
        CK[2]: os.path.join(AP, CK[2]), CK[4]: os.path.join(AP, CK[4])}
for nm, path in want.items():
    h = hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None
    check(f"0 sealed sha256: {nm}", nm in sealed and h == sealed[nm], f"{(h or 'missing')[:12]} vs {sealed.get(nm, 'not sealed')[:12]}")
if FAIL: print("STOP: sealed-sha protocol FAIL -> no grade", FAIL); sys.exit(1)
# ---- 1. reference rows
ref = json.load(open(os.path.join(D, "exp089_wall.json"))); p1 = json.load(open(os.path.join(D, "exp093_p1.json")))
K = ("kappa", "norm", "R", "YA", "YB", "rhoA", "Gb")
r4, r6 = row(4), row(6)
check("1 KA: row(4) reproduces exp089_wall.json bitwise", all(r4[k] == ref["r4"][k] for k in K))
check("1 KA: row(6) reproduces exp089_wall.json bitwise", all(r6[k] == ref["r6"][k] for k in K))
# ---- 2. checkpoints (shadowing + completeness); row(8) needs the W2P8 pull, so the shadow check for P = 10 only
for W in (2, 4):
    check(f"2 no local {CK[W]} shadows the Air pull", not os.path.exists(os.path.join(D, CK[W])))
    st = json.load(open(os.path.join(AP, CK[W]))); ng = sum(1 for k in st if k.startswith("g|"))
    check(f"2 W{W}P10 (Air pull): n1c present, 48 g nodes", "n1c" in st and ng == 48, f"nodes {ng}")
r8 = row(8)
check("1 KA: row(8) reproduces exp093_p1.json r8 bitwise", all(r8[k] == p1["r8"][k] for k in K))
# ---- 3. route gates; 4. runner rc; 5. stale-file guard
LOGS = {2: ("air_route_W2P10.out", "air_run_095.txt"), 4: ("air_route_W4P10.out", "air_run_095b.txt")}
for i, W in enumerate((2, 4)):
    out = open(os.path.join(AP, LOGS[W][0])).read(); run = open(os.path.join(AP, LOGS[W][1])).read()
    unc = [int(x) for x in re.findall(r"unconverged (\d+)", out)]
    check(f"3 W{W}P10 route: B2b, t0 refined, residue PASS", out.count("[PASS]") >= 2 and "B2b" in out and "-> PASS" in out)
    check(f"3 W{W}P10 route: no FAIL / STOP / NON-CONVERGED / Traceback", not re.search(r"FAIL|STOP|NON-CONVERGED|Traceback", out))
    check(f"3 W{W}P10 route: every unconverged count is 0", len(unc) > 0 and max(unc) == 0, f"{len(unc)} counts")
    check(f"4 runner {LOGS[W][1]}: air_route_W{W}P10 rc 0", f"air_route_W{W}P10 rc 0" in run)
    m = re.search(rf"air_route_W{W}P10 start (\S+ \S+)", run); mt = sys.argv[1 + i]
    check(f"5 stale-file guard W{W}P10: Air ckpt mtime later than route start", bool(m) and mt > m.group(1), f"mtime {mt} start {m.group(1) if m else None}")
for W in (2, 4):
    g = json.load(open(os.path.join(D, "exp085c", f"G_W{W}P10.json"))); check(f"6 G_W{W}P10: failed empty", not g.get("failed"))
if FAIL: print("STOP: controls failed -> no grading", FAIL); sys.exit(1)
# ---- reading
r10 = row(10); dG = r8["Gb"] - r10["Gb"]; f = -(r10["rhoA"] - r8["rhoA"]) / dG; inc = dG < 0.204
print(f"\nP=10: R {r10['R']:.6f} Y_A {r10['YA']:.6f} Y_bulk {r10['YB']:.6f} rho_A {r10['rhoA']:+.6f} G_b {r10['Gb']:.6f} (kappa {r10['kappa']:.9f})")
print(f"P=8:  rho_A {r8['rhoA']:+.6f} G_b {r8['Gb']:.6f};  G_b(8) - G_b(10) = {dG:+.6f} (f INCONCLUSIVE if < 0.204)")
res = dict(r8=r8, r10=r10, dG=dG, f=f, f_inconclusive=inc, mode=MODE, air_ckpt_mtimes=sys.argv[1:3], failed=FAIL)
if MODE == "S":
    seal = json.load(open(os.path.join(D, "exp095_seal.json")))       # {"rhoA": [c, s], "Gb": [c, s], "f": [c, s]}, committed before opening
    for k, v in (("rhoA", r10["rhoA"]), ("Gb", r10["Gb"]), ("f", None if inc else f)):
        cen, s = seal[k]
        if v is None: print(f"ITEM {k}: INCONCLUSIVE (drop {dG:.4f} < 0.204); descriptive f = {f:+.4f}"); continue
        p1s, p2s = abs(v - cen) <= s, abs(v - cen) <= 2 * s; res[f"{k}_pass_1s"], res[f"{k}_in_2s"] = p1s, p2s
        print(f"ITEM {k} = {v:+.6f}: sealed {cen} +- {s} -> {'PASS' if p1s else 'FAIL'}; +-2 sigma: {'inside' if p2s else 'outside'}")
else:
    f46, f68 = json.load(open(os.path.join(D, "exp089_wall.json")))["f"], p1["f"]; mu = 0.5 * (f46 + f68)
    print(f"PATH D (descriptive, NO pass/fail): f(8->10) = {f:+.4f}{' [INCONCLUSIVE by the drop rule]' if inc else ''}; "
          f"within +-0.08 of mean(f(4->6), f(6->8)) = {mu:.4f}: {abs(f - mu) <= 0.08} (band mine, not blind; descriptive)")
    res.update(f46=f46, f68=f68, mean_prev=mu)
json.dump(res, open(os.path.join(D, "exp095_p1.json"), "w"), indent=1, default=float)
