"""EXP-081e F.3 bitwise check: g at the hardest node (s = 5.9723) recomputed with the 081e patch (CUSPIS_081E=1, route --production-only
--nodes 47:48 --tag-suffix _081e_bw) must equal the stored value EXACTLY. Usage: exp081e_bitwise.py W P Wb <reference ckpt> [model: Opus 5.5]"""
import sys, json, numpy as np
W, P, Wb, ref = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
new = json.load(open(f"exp081d_results/sigma_W{W}_P{P}_box{Wb}_c2_cp12_sc3.0_dd0_081e_bw_ckpt.json")); old = json.load(open(ref))
k = [x for x in new if x.startswith("g|")]; assert len(k) == 1, k; k = k[0]
a, b = new[k], old[k]; same = (a == b)
print(f"F.3 W{W}P{P}b{Wb} {k}: patched {a!r} vs stored {b!r} -> {'BITWISE IDENTICAL' if same else 'DIFFERENT (diff %.3e)' % abs(a - b)}")
sys.exit(0 if same else 1)
