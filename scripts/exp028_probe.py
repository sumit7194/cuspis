"""EXP-028 probe (bridge-approved): ONE node, one process, at the heaviest stored mass node, mode diracA0.2500.
Doubles as the regression check of the new single-sector mode: its Psi values must equal the validated dirac2v node at the
same M (same a = 1/4; the new mode selects the branch by real-axis continuation instead of the fixed -1)."""
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp004_prod as P
M = 14.9818754492
t0 = time.time()
rec = P.worker((M, 0.0, "diracA0.2500"))
ref = json.load(open(f"{P.OUT}/dirac2v_M{M:.10f}_t0.0000000000.json"))
print(f"probe node: ok={rec['ok']} secs={rec.get('secs', 0):.1f} dps={rec.get('dps')} branch={rec.get('branch')} flips={rec.get('flips')} rn/signal={rec.get('rn_over_signal')}")
if rec["ok"]:
    d = max(abs(x - y) for x, y in zip(rec["Psi_re"], ref["Psi_re"])); sc = max(abs(y) for y in ref["Psi_re"])
    dF = max(abs(x - y) for x, y in zip(rec["F_re"], ref["F_re"]))
    print(f"regression vs dirac2v node: max|dPsi| = {d:.3e} (scale {sc:.3e}); max|dF| = {dF:.3e}  -> {'PASS' if d <= 1e-12*max(1, sc) else 'FAIL'}")
print(f"wall {time.time()-t0:.1f} s")
