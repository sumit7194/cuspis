"""Per-node peak footprint of an exp081d_route run (Bridge 2026-11-25): node windows from the .out 'g(s) done' stamps, peaks from the
watchdog .wd.log tree total (5th field). Usage: node_peaks.py OUT WDLOG. [model: Opus 5.5]"""
import re, sys
out, wd = sys.argv[1], sys.argv[2]
ev = [(float(m.group(1)), m.group(2)) for m in (re.match(r"\[\s*([0-9.]+)s\]\s+(.*)", l) for l in open(out)) if m]
pts = [(float(a[0]), float(a[4]), float(a[2]), float(a[3])) for a in (l.split() for l in open(wd) if re.match(r"^\s*[0-9]+\.[0-9]+\s", l)) if len(a) >= 5]
marks = [(t, txt.split(" done")[0] if " done" in txt else txt.split()[0]) for t, txt in ev if re.match(r"(g\(|t0|tsad|sigma_)", txt)]
prev = 0.0; print(f"{'phase':16s} {'t_end(s)':>9s} {'dur(s)':>7s} {'peak tot':>9s} {'MEM':>6s} {'CMPRS':>6s}")
for t, name in marks:
    w = [p for p in pts if prev < p[0] <= t]
    if w: pk = max(w, key=lambda p: p[1]); print(f"{name[:16]:16s} {t:9.0f} {t-prev:7.0f} {pk[1]:9.3f} {pk[2]:6.3f} {pk[3]:6.3f}")
    prev = t
w = [p for p in pts if p[0] > prev]
if w: pk = max(w, key=lambda p: p[1]); print(f"{'(running)':16s} {w[-1][0]:9.0f} {w[-1][0]-prev:7.0f} {pk[1]:9.3f} {pk[2]:6.3f} {pk[3]:6.3f}")
