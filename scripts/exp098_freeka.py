"""EXP-098 amendment-2 known-answer control for the free side [model: Opus 5.5].
Recomputes the STORED free values that stage 0 uses (k = 1: W2P4, W4P4; k = 2: W4P8, W8P8; box = P),
with exp081b_run.free's own formula verbatim, on the interpreter that runs it, and compares them BITWISE
to the stored JSON. Writes nothing into exp081b_results/. Must fail if the interpreter or code path differs."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, numpy, scipy
OUT = os.path.join(HERE, "exp081b_results"); bad = 0
print("interpreter", sys.version.split()[0], "numpy", numpy.__version__, "scipy", scipy.__version__)
for W, P in ((2, 4), (4, 4), (4, 8), (8, 8)):
    Wbox, c = P, 2; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
    S = float(S3.FreeStrip(Lx, Lt, int(c * 2 * P), list(range(x0, x0 + W)), P - 1).S(cpts=12).real)
    st = json.load(open(os.path.join(OUT, f"free_W{W}_P{P}_box{Wbox}_c{c}.json")))["S"]
    ok = (S == st); bad += (not ok)
    print(f"free W{W}P{P} box{Wbox}: recomputed {S!r} stored {st!r} -> {'BITWISE' if ok else 'MISMATCH %.1e' % (S - st)}")
print("KA-free:", "PASS" if bad == 0 else f"FAIL ({bad})"); sys.exit(1 if bad else 0)
