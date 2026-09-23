"""Run a command under a whole-process-tree watchdog (macOS).

Samples every --interval seconds:
- tree footprint = sum of top's MEM + CMPRS over the child and all its descendants;
- free disk on the output volume;
- free swap (sysctl vm.swapusage).

It SIGTERMs the child's process group (then SIGKILLs after a grace period) if the tree exceeds --cap-gb, if free disk
falls below --min-disk-gb, or if free swap falls below --min-swap-mb. Every sample goes to --log, and the peak is
printed at exit.

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

def swap_free_mb():
    s = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    m = re.search(r"free\s*=\s*([\d.]+)M", s)
    return float(m.group(1)) if m else float("nan")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True); ap.add_argument("--cap-gb", type=float, default=5.0)
    ap.add_argument("--min-disk-gb", type=float, default=5.0); ap.add_argument("--min-swap-mb", type=float, default=512.0)
    ap.add_argument("--interval", type=float, default=5.0); ap.add_argument("--stdout", default=None)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    outf = open(a.stdout, "w") if a.stdout else None
    child = subprocess.Popen(cmd, start_new_session=True, stdout=outf or None, stderr=subprocess.STDOUT if outf else None)
    log = open(a.log, "w", buffering=1)
    log.write(f"# cmd: {' '.join(cmd)}\n# caps: tree <= {a.cap_gb} GB, disk >= {a.min_disk_gb} GB, free swap >= {a.min_swap_mb} MB\n"
              f"# t_s  nproc  MEM_GB  CMPRS_GB  TREE_GB  disk_free_GB  swap_free_MB\n")
    peak = (0.0, 0.0, 0.0); t0 = time.time(); reason = None
    while child.poll() is None:
        pids = descendants(child.pid); mem, cmp, seen = tree_footprint(pids)
        disk = shutil.disk_usage(os.getcwd()).free/1024**3; swp = swap_free_mb(); tot = (mem + cmp)/1024**3
        if tot > peak[2]: peak = (mem/1024**3, cmp/1024**3, tot)
        log.write(f"{time.time()-t0:8.1f} {seen:5d} {mem/1024**3:7.3f} {cmp/1024**3:8.3f} {tot:7.3f} {disk:12.2f} {swp:12.1f}\n")
        if tot > a.cap_gb: reason = f"tree footprint {tot:.2f} GB > cap {a.cap_gb} GB"
        elif disk < a.min_disk_gb: reason = f"free disk {disk:.2f} GB < {a.min_disk_gb} GB"
        elif swp == swp and swp < a.min_swap_mb: reason = f"free swap {swp:.0f} MB < {a.min_swap_mb} MB"
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
