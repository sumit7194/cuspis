"""Run a command under a whole-process-tree watchdog (macOS).

Samples every --interval seconds:
- tree footprint = sum of top's MEM + CMPRS over the child and all its descendants;
- free disk on the output volume;
- free swap (sysctl vm.swapusage).

It SIGTERMs the child's process group (then SIGKILLs after a grace period) if the tree exceeds --cap-gb, if free disk
falls below --min-disk-gb, or if system memory is genuinely short. Every sample goes to --log, and the peak is printed
at exit.

Memory trigger (bridge fix, 2026-10-03, copied from quantum 955b4c0). macOS grows swap on demand, so low free swap
alone is a false positive. The rules are:
- kill if `memory_pressure` reports system-wide free memory < --min-sysfree-pct (default 10%);
- kill on free swap < --min-swap-mb ONLY when system-wide free memory is also < 20%.

Usage: python3 watchdog.py --log run.wd.log [--cap-gb 5] [--min-disk-gb 5] [--min-swap-mb 512] [--interval 5] -- cmd args...
"""
import argparse, os, re, shutil, signal, subprocess, sys, time

UNITS = {"B": 1, "K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}
def parse_size(s):
    s = s.strip().rstrip("+-")
    m = re.match(r"^([\d.]+)([BKMGT]?)$", s)
    return float(m.group(1)) * UNITS[m.group(2) or "B"] if m else 0.0

def descendants(root):
    out = subprocess.run(["ps", "-A", "-o", "pid=,ppid="], capture_output=True, text=True).stdout
    kids = {}
    for line in out.split("\n"):
        p = line.split()
        if len(p) == 2: kids.setdefault(int(p[1]), []).append(int(p[0]))
    tree, stack = set(), [root]
    while stack:
        q = stack.pop()
        if q in tree: continue
        tree.add(q); stack.extend(kids.get(q, []))
    return tree

def tree_footprint(pids):
    out = subprocess.run(["top", "-l", "1", "-stats", "pid,mem,cmprs"], capture_output=True, text=True).stdout
    mem = cmp = 0.0; seen = 0; hdr = False
    for line in out.split("\n"):
        if line.startswith("PID"): hdr = True; continue
        if not hdr: continue
        p = line.split()
        if len(p) >= 3 and p[0].isdigit() and int(p[0]) in pids:
            mem += parse_size(p[1]); cmp += parse_size(p[2]); seen += 1
    return mem, cmp, seen

def sys_free_pct():
    s = subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout
    m = re.search(r"System-wide memory free percentage:\s*(\d+)%", s)
    return float(m.group(1)) if m else float("nan")

def pressure_level():
    """kern.memorystatus_vm_pressure_level: 1 normal (green), 2 warn (yellow), 4 critical (red)."""
    s = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"], capture_output=True, text=True).stdout.strip()
    return int(s) if s.isdigit() else -1

def swap_free_mb():
    s = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"free\s*=\s*([\d.]+)M", s)
    return float(m.group(1)) if m else float("nan")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True); ap.add_argument("--cap-gb", type=float, default=5.0)
    ap.add_argument("--min-disk-gb", type=float, default=5.0); ap.add_argument("--min-swap-mb", type=float, default=512.0)
    ap.add_argument("--min-sysfree-pct", type=float, default=10.0)
    ap.add_argument("--stop-on-pressure-warn", action="store_true",
                    help="also stop if the system memory-pressure level reaches warn (yellow) or worse (bridge rule, 2026-11-17)")
    ap.add_argument("--interval", type=float, default=5.0); ap.add_argument("--stdout", default=None)
    ap.add_argument("--soft-cap-gb", type=float, default=None,
                    help="soft cap (Sumit 2026-11-22): crossing it only WARNS (printed + logged, again at each +0.5 GB); --cap-gb stays the hard kill")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    outf = open(a.stdout, "w") if a.stdout else None
    child = subprocess.Popen(cmd, start_new_session=True, stdout=outf or None, stderr=subprocess.STDOUT if outf else None)
    log = open(a.log, "w", buffering=1)
    def on_term(signum, frame):   # external stop: take the child's process group down too (it runs in its own session)
        log.write(f"# watchdog received signal {signum}: stopping child group\n")
        try: os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        sys.exit(98)
    signal.signal(signal.SIGTERM, on_term)
    log.write(f"# cmd: {' '.join(cmd)}\n# caps: tree <= {a.cap_gb} GB, disk >= {a.min_disk_gb} GB, free swap >= {a.min_swap_mb} MB\n"
              f"# memory trigger: system free < {a.min_sysfree_pct}%, or free swap < {a.min_swap_mb} MB together with system free < 20%\n"
              f"# pressure trigger: {'stop at level >= 2 (yellow)' if a.stop_on_pressure_warn else 'off'}\n"
              f"# t_s  nproc  MEM_GB  CMPRS_GB  TREE_GB  disk_free_GB  swap_free_MB  sys_free_pct  pressure_level\n")
    peak = (0.0, 0.0, 0.0); t0 = time.time(); reason = None; warned = -1.0
    while child.poll() is None:
        pids = descendants(child.pid); mem, cmp, seen = tree_footprint(pids)
        disk = shutil.disk_usage(os.getcwd()).free/1024**3; swp = swap_free_mb(); sfp = sys_free_pct(); lvl = pressure_level(); tot = (mem + cmp)/1024**3
        if tot > peak[2]: peak = (mem/1024**3, cmp/1024**3, tot)
        log.write(f"{time.time()-t0:8.1f} {seen:5d} {mem/1024**3:7.3f} {cmp/1024**3:8.3f} {tot:7.3f} {disk:12.2f} {swp:12.1f} {sfp:12.0f} {lvl:14d}\n")
        if a.soft_cap_gb is not None and tot > a.soft_cap_gb and tot > warned + 0.5:
            warned = tot; msg = f"# WATCHDOG WARN (soft cap): tree footprint {tot:.2f} GB > soft cap {a.soft_cap_gb} GB at t={time.time()-t0:.0f}s (hard cap {a.cap_gb} GB)"
            log.write(msg + "\n"); log.flush(); print(msg, flush=True)
        if tot > a.cap_gb: reason = f"tree footprint {tot:.2f} GB > cap {a.cap_gb} GB"
        elif disk < a.min_disk_gb: reason = f"free disk {disk:.2f} GB < {a.min_disk_gb} GB"
        elif sfp == sfp and sfp < a.min_sysfree_pct: reason = f"system-wide free memory {sfp:.0f}% < {a.min_sysfree_pct}%"
        elif a.stop_on_pressure_warn and lvl >= 2: reason = f"memory pressure level {lvl} (>= 2, yellow)"
        elif swp == swp and swp < a.min_swap_mb and sfp == sfp and sfp < 20: reason = f"free swap {swp:.0f} MB < {a.min_swap_mb} MB with system free {sfp:.0f}% < 20%"
        if reason:
            log.write(f"# WATCHDOG SIGTERM: {reason}\n")
            try: os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError: pass
            for _ in range(30):
                if child.poll() is not None: break
                time.sleep(1)
            if child.poll() is None:
                try: os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError: pass
            break
        time.sleep(a.interval)
    rc = child.wait()
    summary = (f"# exit {rc}; wall {time.time()-t0:.0f} s; PEAK tree MEM {peak[0]:.3f} GB + CMPRS {peak[1]:.3f} GB = {peak[2]:.3f} GB"
               + (f"; KILLED: {reason}" if reason else ""))
    log.write(summary + "\n"); print(summary)
    sys.exit(rc if not reason else 99)

if __name__ == "__main__":
    main()
