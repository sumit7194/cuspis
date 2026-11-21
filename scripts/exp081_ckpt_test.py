"""Crash-then-resume test for route_i_ckpt (required before the night run): W=2 r=2 Ny=8 strip, saddle ON.
(1) uninterrupted reference in a fresh checkpoint; (2) a subprocess killed mid-way, then resumed; results must be identical.
[model: Opus 5.5]"""
import os, sys, json, time, subprocess, signal
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import sigma3d as S3
P, W = 4, 2; Lx, Lt = W + 2 * P, 2 * P
def run(ck):
    S = S3.Strip3D(Lx, Lt, 8, list(range(P, P + W)), P - 1); return S3.route_i_ckpt(S, ck, cpts=12, with_saddle=True)[0]
for f in ("ckA.json", "ckB.json"):
    if os.path.exists(os.path.join(HERE, f)): os.remove(os.path.join(HERE, f))
t0 = time.time(); ref = run(os.path.join(HERE, "ckA.json")); tref = time.time() - t0
code = f"import sys; sys.path.insert(0, {HERE!r}); import exp081_ckpt_test_child"
open(os.path.join(HERE, "exp081_ckpt_test_child.py"), "w").write(
    f"import sys; sys.path.insert(0, {HERE!r}); import sigma3d as S3\n"
    f"S = S3.Strip3D({Lx}, {Lt}, 8, list(range({P}, {P + W})), {P - 1}); S3.route_i_ckpt(S, {os.path.join(HERE, 'ckB.json')!r}, cpts=12, with_saddle=True)\n")
p = subprocess.Popen([sys.executable, "-u", "-W", "ignore", os.path.join(HERE, "exp081_ckpt_test_child.py")])
time.sleep(max(2.0, 0.45 * tref)); p.send_signal(signal.SIGKILL); p.wait()
n_saved = len(json.load(open(os.path.join(HERE, "ckB.json")))) if os.path.exists(os.path.join(HERE, "ckB.json")) else 0
res = run(os.path.join(HERE, "ckB.json"))
print(f"reference {ref:.12f} ({tref:.0f}s); killed child after ~{0.45*tref:.0f}s with {n_saved} checkpoint entries; resumed {res:.12f}; "
      f"diff {abs(res-ref):.1e} [{'PASS' if abs(res-ref) <= 1e-12 * abs(ref) and 0 < n_saved < 50 else 'CHECK'}]")
