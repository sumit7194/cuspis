"""EXP-019 regression: the continuation fix must not change a validated node (scalar Renyi-2, a = 1/2, M ~ 3.13)."""
import sys, json, glob, math, io, contextlib
sys.path.insert(0, '.')
import mpmath as mp, exp004_mp as em
from exp004_prod import XG
f = glob.glob('exp004_nodes/renyi2_M3.131*.json')[0]; d = json.load(open(f)); M = d['M']
with contextlib.redirect_stderr(io.StringIO()):
    out, dd = em.integrate_mp(M, 0.5, math.radians(4), XG, branch=-1)
new = [complex(out[x]).real for x in XG]
dev = max(abs(n/o - 1) for n, o in zip(new, d['F_re']))
print(f"renyi2 node M={M:.4f}: max relative change over 25 angles after the fix = {dev:.1e}  (stored at dps {d['dps']})")
