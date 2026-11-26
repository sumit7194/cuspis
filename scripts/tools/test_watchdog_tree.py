"""Unit test for the watchdog TREE fix (Bridge 2026-11-26, EXP-095): the tree footprint must equal the kernel phys_footprint
(top's MEM), NOT MEM + CMPRS (top's MEM already includes compressed pages). [model: Opus 5.5]

Arm 1 (fixture, deterministic): the controlled 400 MB compression case measured on the Air (exp081d_results/exp095_memtest_footprint.txt):
  top "60450  405M 295M", footprint phys_footprint 405 MB. watchdog.tree_footprint + tree_total must give 405 MB (+-1 %).
  Must-fire control: the OLD formula (MEM + CMPRS = 700 MB) must be REJECTED by the same tolerance, or the test cannot fail.
Arm 2 (live, this machine): a 400 MB dirty compressible process; tree_total must match `footprint -p` within 3 %. Then SIGSTOP it and
  wait up to LIVE_WAIT s (default 30) for compression (CMPRS >= 50 MB). If compression happens, tree_total must still match and the old
  formula must be off by > 10 % (live discrimination). If it does not happen (a roomy machine), that sub-arm is reported NOT EXERCISED.
Usage: python3 tools/test_watchdog_tree.py   (exit 0 = all exercised arms pass)"""
import os, re, signal, subprocess, sys, time, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watchdog as W
MB = 1024 ** 2; fails = []
def check(name, ok, detail): print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}"); ok or fails.append(name)

# ---- Arm 1: fixture from the Air ----
FAKE_TOP = "Processes: 1 total\n\nPID    MEM   CMPRS\n60450  405M 295M\n99999  12M  1M\n"
real_run = W.subprocess.run
W.subprocess.run = lambda *a, **k: types.SimpleNamespace(stdout=FAKE_TOP)
try: mem, cmp, seen = W.tree_footprint({60450})
finally: W.subprocess.run = real_run
phys = 405 * MB; new = W.tree_total(mem, cmp); old = mem + cmp
check("arm1 parse", seen == 1 and abs(mem - 405 * MB) < 1 and abs(cmp - 295 * MB) < 1, f"MEM {mem/MB:.0f} MB, CMPRS {cmp/MB:.0f} MB, seen {seen}")
check("arm1 new TREE == phys_footprint", abs(new - phys) / phys <= 0.01, f"tree_total {new/MB:.0f} MB vs phys_footprint 405 MB")
check("arm1 must-fire: old MEM+CMPRS is rejected", abs(old - phys) / phys > 0.01, f"old formula {old/MB:.0f} MB ({(old/phys-1)*100:+.0f} %)")

# ---- Arm 2: live ----
def phys_fp(pid):
    out = subprocess.run(["footprint", "-p", str(pid)], capture_output=True, text=True).stdout
    m = re.search(r"phys_footprint:\s+([\d.]+)\s*([KMG]B)", out)
    return float(m.group(1)) * {"KB": 1024, "MB": MB, "GB": 1024 * MB}[m.group(2)] if m else None
code = ("import time,sys\nb=bytearray(b'abcdefgh'*(50*2**20))\nfor i in range(0,len(b),16384): b[i]=i%251\n"
        "print('ready',flush=True)\ntime.sleep(600)")
p = subprocess.Popen([sys.executable, "-I", "-c", code], stdout=subprocess.PIPE, text=True)
try:
    p.stdout.readline(); time.sleep(1)
    mem, cmp, seen = W.tree_footprint({p.pid}); f = phys_fp(p.pid)
    if f is None: check("arm2 live", False, "footprint -p gave no phys_footprint")
    else:
        check("arm2 live running: tree_total == phys_footprint", abs(W.tree_total(mem, cmp) - f) / f <= 0.03,
              f"tree_total {W.tree_total(mem, cmp)/MB:.0f} MB, phys_footprint {f/MB:.0f} MB, CMPRS {cmp/MB:.0f} MB")
        os.kill(p.pid, signal.SIGSTOP); t_end = time.time() + float(os.environ.get("LIVE_WAIT", "30")); done = False
        while time.time() < t_end:
            mem, cmp, seen = W.tree_footprint({p.pid})
            if cmp >= 50 * MB:
                f = phys_fp(p.pid); new, old = W.tree_total(mem, cmp), mem + cmp
                check("arm2 live compressed: tree_total == phys_footprint", abs(new - f) / f <= 0.03, f"tree_total {new/MB:.0f} MB, phys_footprint {f/MB:.0f} MB, CMPRS {cmp/MB:.0f} MB")
                check("arm2 live compressed must-fire: old formula off > 10 %", abs(old - f) / f > 0.10, f"old {old/MB:.0f} MB ({(old/f-1)*100:+.0f} %)")
                done = True; break
            time.sleep(5)
        if not done: print(f"[NOT EXERCISED] arm2 live compressed: no compression (CMPRS {cmp/MB:.0f} MB < 50 MB) within LIVE_WAIT s on this machine")
        os.kill(p.pid, signal.SIGCONT)
finally:
    p.terminate(); p.wait()
print("RESULT:", "FAIL " + ", ".join(fails) if fails else "all exercised arms PASS"); sys.exit(1 if fails else 0)
