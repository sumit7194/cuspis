"""Run a command under a whole-process-tree watchdog (macOS).

Samples every --interval seconds:
- tree footprint = sum of top's MEM over the child and all its descendants. MEM is the kernel phys_footprint, which ALREADY INCLUDES
  compressed memory; CMPRS is logged for information only (it is a part of MEM). FIX 2026-11-26 (Bridge, EXP-095): before this date
  TREE_GB was MEM + CMPRS, which counts compressed pages twice. HISTORICAL TREE_GB values (logs, holds, declared peaks) are therefore
  overstated by the compressed part (~40-60 % on the 8 GB Air); the MEM_GB column of old logs is the true footprint. Evidence:
  exp081d_results/exp095_memtest_footprint.txt; test: tools/test_watchdog_tree.py;
- free disk on the output volume;
- free swap (sysctl vm.swapusage).

NEVER KILLS (Sumit's standing rule 2026-11-25: no job-ending caps anywhere; the old kill paths are DELETED, not disabled).
- Disk: inform < 10 GB free, SIGSTOP the child's process group < 5 GB, SIGCONT > 6 GB, CRITICAL alert < 2 GB.
- Memory: inform at yellow/red; SIGSTOP after --red-grace s of continuous red, SIGCONT after --green-resume s green; PAUSE-LONG note.
- The old flags (--cap-gb, --min-disk-gb, --min-sysfree-pct, --min-swap-mb, --stop-on-pressure-warn, --pressure-stop-level) are
  accepted for compatibility and IGNORED. --soft-cap-gb only informs. Every sample goes to --log; the peak is printed at exit.
- The only SIGTERM left is on_term: it forwards a TERM sent to the watchdog itself to the child group.

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

def tree_total(mem, cmp):
    """True tree footprint in bytes: top's MEM (= phys_footprint, compressed pages included). CMPRS is NOT added (fix 2026-11-26)."""
    return mem

def sys_free_pct():
    s = subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout
    m = re.search(r"System-wide memory free percentage:\s*(\d+)%", s)
    return float(m.group(1)) if m else float("nan")

def pressure_level():
    fk = os.environ.get("WD_FAKE_LEVEL_FILE")
    if fk:
        try: return int(open(fk).read().strip())
        except Exception: pass
    return _pressure_level_real()
def _pressure_level_real():
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
    ap.add_argument("--pressure-stop-level", type=int, default=None, choices=(2, 4),
                    help="stop when the pressure level reaches this value (2 yellow, 4 red); overrides --stop-on-pressure-warn (Sumit, 2026-11-23: routes stop at red)")
    ap.add_argument("--pause-on-red", action="store_true", help="Sumit 2026-11-23: never kill for memory; inform at yellow/red, SIGSTOP only after --red-grace s of continuous red, SIGCONT after --green-resume s green")
    ap.add_argument("--disk-pause", action="store_true", help="(accepted for compatibility; ALWAYS on) disk < 10 GB inform, < 5 GB SIGSTOP the job group, > 6 GB SIGCONT, < 2 GB CRITICAL alert; NEVER kill")
    ap.add_argument("--pause-long", type=float, default=1800.0); ap.add_argument("--red-grace", type=float, default=300.0); ap.add_argument("--green-resume", type=float, default=60.0)
    ap.add_argument("--inform-pressure", action="store_true", help="print/log a WARN when pressure rises to yellow or worse (below the stop level)")
    ap.add_argument("--interval", type=float, default=5.0); ap.add_argument("--stdout", default=None)
    ap.add_argument("--soft-cap-gb", type=float, default=None,
                    help="soft cap (Sumit 2026-11-22): crossing it only WARNS (printed + logged, again at each +0.5 GB); --cap-gb stays the hard kill")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(); INFORM = a.inform_pressure; _last_lvl = [1]; _dp, _dw, _dc = [False], [99.0], [False]; _red, _green, _paused = [None], [None], [False]; _pt, _pl = [None], [False]; PL = a.pressure_stop_level if a.pressure_stop_level else (2 if a.stop_on_pressure_warn else None)
    a.disk_pause = True; a.pause_on_red = True; INFORM = True   # Sumit 2026-11-25: NO job-ending caps anywhere (no opt-out exists)
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
              f"# disk mode: {'NO-KILL (Sumit 2026-11-25): disk inform < 10 GB, pause < 5, resume > 6, CRITICAL < 2; memory pause-on-red; caps/kill flags are accepted but ignored'}; caller pid {os.getppid()}\n"
              f"# pressure trigger: {('stop at level >= %d (%s)' % (PL, {2: 'yellow', 4: 'red'}[PL])) if PL else 'off'}\n"
              f"# TREE_GB = MEM_GB (phys_footprint; CMPRS_GB is part of it; fixed 2026-11-26, older logs: TREE = MEM + CMPRS, a double count)\n# t_s  nproc  MEM_GB  CMPRS_GB  TREE_GB  disk_free_GB  swap_free_MB  sys_free_pct  pressure_level\n")
    peak = (0.0, 0.0, 0.0); t0 = time.time(); reason = None; warned = -1.0
    while child.poll() is None:
        pids = descendants(child.pid); mem, cmp, seen = tree_footprint(pids)
        disk = shutil.disk_usage(os.getcwd()).free/1024**3
        fkd = os.environ.get("WD_FAKE_DISK_FILE")                  # test hook: last line of the file = fake free disk (GB)
        if fkd and os.path.exists(fkd):
            try: disk = float(open(fkd).read().split()[-1])
            except Exception: pass
        swp = swap_free_mb(); sfp = sys_free_pct(); lvl = pressure_level(); tot = tree_total(mem, cmp)/1024**3
        if tot > peak[2]: peak = (mem/1024**3, cmp/1024**3, tot)
        log.write(f"{time.time()-t0:8.1f} {seen:5d} {mem/1024**3:7.3f} {cmp/1024**3:8.3f} {tot:7.3f} {disk:12.2f} {swp:12.1f} {sfp:12.0f} {lvl:14d}\n")
        if a.soft_cap_gb is not None and tot > a.soft_cap_gb and tot > warned + 0.5:
            warned = tot; msg = f"# WATCHDOG WARN [{time.strftime('%F %T')}] level {lvl} (soft cap): tree footprint {tot:.2f} GB > soft cap {a.soft_cap_gb} GB at t={time.time()-t0:.0f}s (hard cap {a.cap_gb} GB)"
            log.write(msg + "\n"); log.flush(); print(msg, flush=True)
        if INFORM and lvl >= 2 and lvl > _last_lvl[0] and not (PL and lvl >= PL):   # Sumit 2026-11-23: inform, do not kill, below the stop level
            msg = f"# WATCHDOG WARN [{time.strftime('%F %T')}] (pressure {({2: 'yellow', 4: 'red'}).get(lvl, lvl)}): level {lvl} at t={time.time() - t0:.0f}s, tree {tot:.2f} GB -- close other apps?"
            log.write(msg + "\n"); log.flush(); print(msg, flush=True)
        _last_lvl[0] = lvl
        if a.disk_pause:                                           # disk: inform < 10, pause < 5, resume > 6, kill only < 1 (GB)
            if disk < 10 and disk < _dw[0] - 1.0:
                _dw[0] = disk; msg = f"# WATCHDOG WARN-DISK [{time.strftime('%F %T')}]: free disk {disk:.2f} GB < 10 GB (pause at < 5; never killed)"
                log.write(msg + "\n"); log.flush(); print(msg, flush=True)
            if disk >= 10: _dw[0] = 99.0
            if disk < 2.0 and not _dc[0]:
                _dc[0] = True; msg = f"# WATCHDOG CRITICAL-DISK [{time.strftime('%F %T')}]: free disk {disk:.2f} GB < 2 GB -> job stays PAUSED; tell the Bridge NOW (never killed)"
                log.write(msg + "\n"); log.flush(); print(msg, flush=True)
            if disk >= 2.5: _dc[0] = False
            if disk < 5.0 and not _dp[0]:
                try: os.killpg(child.pid, signal.SIGSTOP); _dp[0] = True
                except ProcessLookupError: pass
                msg = f"# WATCHDOG PAUSE-DISK [{time.strftime('%F %T')}]: free disk {disk:.2f} GB < 5 GB -> SIGSTOP job group (resume > 6 GB)"; log.write(msg + "\n"); log.flush(); print(msg, flush=True)
            elif _dp[0] and disk > 6.0 and not _paused[0]:
                try: os.killpg(child.pid, signal.SIGCONT); _dp[0] = False
                except ProcessLookupError: pass
                msg = f"# WATCHDOG RESUME-DISK [{time.strftime('%F %T')}]: free disk {disk:.2f} GB > 6 GB -> SIGCONT"; log.write(msg + "\n"); log.flush(); print(msg, flush=True)
        if a.pause_on_red:                                         # pause/resume instead of any memory kill
            now = time.time()
            if lvl >= 4: _red[0] = _red[0] or now; _green[0] = None
            elif lvl <= 1: _green[0] = _green[0] or now; _red[0] = None
            else: _red[0] = None; _green[0] = None
            if not _paused[0] and _red[0] and now - _red[0] >= a.red_grace:
                try: os.killpg(child.pid, signal.SIGSTOP); _paused[0] = True
                except ProcessLookupError: pass
                msg = f"# WATCHDOG PAUSE [{time.strftime('%F %T')}] level {lvl} (red pressure {a.red_grace:.0f} s): job SIGSTOPped at t={now - t0:.0f}s, tree {tot:.2f} GB -- please close apps; resumes after {a.green_resume:.0f} s green"
                log.write(msg + "\n"); log.flush(); print(msg, flush=True)
            if _paused[0] and _green[0] and now - _green[0] >= a.green_resume:
                try:
                    if not _dp[0]: os.killpg(child.pid, signal.SIGCONT)
                    _paused[0] = False
                except ProcessLookupError: pass
                msg = f"# WATCHDOG RESUME [{time.strftime('%F %T')}] level {lvl} ({a.green_resume:.0f} s green): job SIGCONTinued at t={now - t0:.0f}s"
                log.write(msg + "\n"); log.flush(); print(msg, flush=True)
            if _paused[0]:
                _pt[0] = _pt[0] or now
                if now - _pt[0] >= a.pause_long and not _pl[0]:              # Bridge 2026-11-23: a pause > 30 min is reported (the session waiter relays it)
                    _pl[0] = True; msg = f"# WATCHDOG PAUSE-LONG [{time.strftime('%F %T')}] level {lvl}: paused > {a.pause_long:.0f} s (since t={_pt[0] - t0:.0f}s)"
                    log.write(msg + "\n"); log.flush(); print(msg, flush=True)
            else: _pt[0] = None; _pl[0] = False
        time.sleep(a.interval)
    rc = child.wait()
    summary = (f"# exit {rc}; wall {time.time()-t0:.0f} s; PEAK tree footprint {peak[2]:.3f} GB (MEM = phys_footprint; CMPRS {peak[1]:.3f} GB of it compressed)"
               + (f"; KILLED: {reason}" if reason else ""))
    log.write(summary + "\n"); print(summary)
    sys.exit(rc if not reason else 99)

if __name__ == "__main__":
    main()
