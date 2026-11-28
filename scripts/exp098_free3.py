"""EXP-098 amendment 2: compute the two new-width free values with exp081b_run.free VERBATIM (on the venv). [model: Opus 5.5]
Refuses if either cache already exists (no stored file is overwritten)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exp081b_run as Rn, scipy
for W, P in ((3, 4), (6, 8)):
    f = os.path.join(Rn.OUT, f"free_W{W}_P{P}_box{P}_c2.json")
    if os.path.exists(f): sys.exit(f"REFUSE: {f} already exists")
for W, P in ((3, 4), (6, 8)):
    print(f"free W{W}P{P} box{P}: {Rn.free(W, P, Wbox=P)!r}", flush=True)
