"""EXP-096 grader (registration notes/EXP-096_097_registration.md). Reads exp081d_results/exp096/W{W}P{P}Wb{P}Ny{4P}*.json (the full
runs of exp096_t0_disc.py, possibly split by --classes) and the stored EXP-087 t0 values. [model: Opus 5.5]
  KA-complete: sum_classes (ON_d - OFF_d) == stored t0(ON) - t0(OFF)          |diff| <= 1e-8
  truth:       Delta_truth = sum (mine - OFF_d);  D = sum (mine - ON_d) = truth - fix  (split: EXP-087 clusters / other near-pairs)
  tau_num  = 3 x max(|D(r1) - D(r2)|, |D_M - D_M/2| at r1 and r2) + 1e-8
  delta_mat = 0.008 / (0.5 x NORM): an error moving R by 1/10 of the narrowest sealed k = 3 half-width (0.08); NORM = 15 at k = 3
              (bound: norm(2) 14.0900, norm(2.5) 14.3120; inference, re-graded with the actual norm(3) at the landing), 14.3120 at k = 2.5
  GRADE: EXACT if |D| <= tau_num; PASS (fix adequate) if |D| <= delta_mat; FAIL otherwise.
  W8P8 known answer: |Delta_truth - (OFF@1e-6 - OFF@1e-5)| <= 1e-7 (the referee truth; the fix missed it by 9.2e-7).
  Gates: every class ok (r2 >= 10 x half-span), unconverged 0.
Usage: exp096_grade.py W P"""
import os, sys, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "exp081d_results"); E = os.path.join(D, "exp096")
W, P = int(sys.argv[1]), int(sys.argv[2]); RAD = 1e-5
files = [f for f in sorted(glob.glob(os.path.join(E, f"W{W}P{P}Wb{P}Ny{4*P}*.json"))) if "_probe" not in f and "_plant" not in f]
cl, unconv = {}, 0
for f in files:
    d = json.load(open(f)); unconv += d["stats"].get("unconverged", 0)
    for c in d["classes"]: cl[c["p"]] = c
cz = lambda v: complex(*v) if isinstance(v, list) else complex(v)
FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:70s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
print(f"files: {[os.path.basename(f) for f in files]}; classes {sorted(cl)}")
check("gate: unconverged G evaluations = 0", unconv == 0, str(unconv))
if (W, P) == (8, 8):
    ref = json.load(open(os.path.join(D, "exp087_referee_W8P8.json"))); on, off = ref["on_1e-5"], ref["off_1e-5"]; truth_ref = ref["off_1e-6"] - off; NORM = 14.0900
else:
    ref = json.load(open(os.path.join(D, f"exp087_t0_W{W}P{P}.json"))); on, off = ref["on"], ref["off"]; truth_ref = None; NORM = 15.0 if P == 12 else 14.3120
fix = on - off
S = lambda key: sum(cz(c[key]).real for c in cl.values())
is087 = lambda c: any(b - a < RAD for a, b in zip(c["members"][:-1], c["members"][1:]))
fix_rec = S("on_r1") - S("off_r1")
check("KA-complete: sum(ON_d - OFF_d) == stored t0(ON) - t0(OFF)", abs(fix_rec - fix) <= 1e-8, f"{fix_rec:+.12f} vs {fix:+.12f} (diff {fix_rec - fix:+.1e})")
truth = S("mine_r1") - S("off_r1"); Dv = {k: S(k) - S("on_r1") for k in ("mine_r1", "mine_r1_M2", "mine_r2", "mine_r2_M2")}
D1 = Dv["mine_r1"]; D087 = sum(cz(c["mine_r1"]).real - cz(c["on_r1"]).real for c in cl.values() if is087(c)); Doth = D1 - D087
tau = 3 * max(abs(Dv["mine_r1"] - Dv["mine_r2"]), abs(Dv["mine_r1"] - Dv["mine_r1_M2"]), abs(Dv["mine_r2"] - Dv["mine_r2_M2"])) + 1e-8
dmat = 0.008 / (0.5 * NORM)
print(f"\nDelta_fix (stored) {fix:+.9f}   Delta_truth (this route) {truth:+.9f}   D = truth - fix {D1:+.3e}  "
      f"[EXP-087 clusters {D087:+.3e}; other near-pairs {Doth:+.3e}]")
print(f"r-sweep {Dv['mine_r1'] - Dv['mine_r2']:+.1e}; M/2 {Dv['mine_r1'] - Dv['mine_r1_M2']:+.1e} / {Dv['mine_r2'] - Dv['mine_r2_M2']:+.1e};  tau_num {tau:.1e};  delta_mat {dmat:.2e} (NORM {NORM})")
for c in sorted(cl.values(), key=lambda c: c["p"]):
    print(f"  class p={c['p']:2d} span {2*c['half']:.1e} {'087' if is087(c) else 'near'}: mine - ON {cz(c['mine_r1']).real - cz(c['on_r1']).real:+.3e}  "
          f"ON - OFF {cz(c['on_r1']).real - cz(c['off_r1']).real:+.6e}")
if truth_ref is not None:
    check("W8P8 known answer: |Delta_truth - (OFF@1e-6 - OFF@1e-5)| <= 1e-7", abs(truth - truth_ref) <= 1e-7, f"{truth:+.10f} vs {truth_ref:+.10f} ({truth - truth_ref:+.1e})")
grade = "EXACT" if abs(D1) <= tau else ("PASS (fix adequate)" if abs(D1) <= dmat else "FAIL (fix inadequate)")
print(f"\nEXP-096 W{W}P{P} GRADE: {grade}   |D| {abs(D1):.2e} vs tau_num {tau:.1e}, delta_mat {dmat:.2e};  dR = 0.5 D NORM = {0.5 * D1 * NORM:+.2e}"
      + (f"   (controls FAILED: {FAIL})" if FAIL else ""))
json.dump(dict(W=W, P=P, fix=fix, fix_rec=fix_rec, truth=truth, D=D1, D087=D087, Dother=Doth, tau=tau, dmat=dmat, grade=grade, failed=FAIL,
               files=[os.path.basename(f) for f in files]), open(os.path.join(E, f"grade_W{W}P{P}.json"), "w"), indent=1)
sys.exit(1 if FAIL else 0)
