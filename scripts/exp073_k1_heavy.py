"""EXP-073(b): one deferred registered step (W=64, t=1) for one twist a, written to the same cache as exp073_k1_run.py
(same key format). Usage: python exp073_k1_heavy.py 0.3 | python exp073_k1_heavy.py 0.5+0.5j  [model: Opus 5.5]"""
import sys, json, os, time, numpy as np
from exp073_k1 import Kfree, top, pressure_guard
a = complex(sys.argv[1]); a = a.real if a.imag == 0 else a
W, t = 64, 1.0; CACHE = "exp073_k1_cache.json"
k = f"{a}|{t}|{W}|8.0|8.0"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
if k in cache: print("already cached", k); sys.exit(0)
free = pressure_guard(min_free_pct=60); print(f"guard ok, free {free}%", flush=True)
t0 = time.time(); Ks, info = Kfree(W, t, a)
ev = top(np.linalg.eigvals(Ks)); ld = complex(np.sum(np.log(np.linalg.eigvals(np.eye(len(Ks)) - Ks))))
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
cache[k] = dict(ev=[[e.real, e.imag] for e in ev], ld=[ld.real, ld.imag], N=info['N'], P=info['P'], sec=time.time() - t0)
json.dump(cache, open(CACHE, "w"), indent=1)
print(f"done {k}: N={info['N']} |P|={info['P']} [{time.time()-t0:.0f}s]", flush=True)
