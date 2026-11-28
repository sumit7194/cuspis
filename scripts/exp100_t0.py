"""EXP-087 recompute: t0 at a production geometry, flag OFF (KA: must equal the stored route t0) then ON (corrected), one install
(same as exp081d_route: refine auto, low-rank; C.t0_term). Usage: exp100_t0.py W P STORED_T0 gL gR hT Ny. [model: Opus 5.5]
EXP-100 part B: an exact-text COPY of exp087_t0.py with the geometry as arguments (convention-A values give the same expressions). Output tagged by geometry."""
import sys, os, time, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
W, P = int(sys.argv[1]), int(sys.argv[2]); stored = float(sys.argv[3]); gL, gR, hT, Ny = (int(v) for v in sys.argv[4:8]); Lx, Lt = gL + W + gR, 2 * hT; x0 = gL; T0 = time.time()
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), hT - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=True, rank_drop=0)
B1 = S.B1(); print(f"W{W}P{P}: installed + B1 ({time.time()-T0:.0f}s)", flush=True); res = {}
for flag in (False, True):
    S3.INNER_BETA0_087 = flag; t = time.time(); v = C.t0_term(S, B1); res["on" if flag else "off"] = v
    print(f"t0 flag {'ON ' if flag else 'OFF'}: {v:+.12f}  ({time.time()-t:.0f}s)", flush=True)
    if not flag: print(f"KA OFF vs stored {stored!r}: diff {v - stored:+.1e} -> {'PASS' if abs(v - stored) <= 1e-10 * abs(stored) else 'FAIL'}", flush=True)
print(f"fixed - unfixed = {res['on'] - res['off']:+.6f}")
json.dump(dict(W=W, P=P, gL=gL, gR=gR, hT=hT, Ny=Ny, stored=stored, **res), open(os.path.join(HERE, "exp081d_results", f"exp100_t0_W{W}P{P}_gL{gL}_gR{gR}_hT{hT}_Ny{Ny}.json"), "w"), indent=1)
