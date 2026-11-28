"""EXP-099 timing probe (before registration): time FreeStrip.S at STORED geometries only (no new value is computed),
and check each against its stored cache bitwise. [model: Opus 5.5]"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
for W, P, Wb in ((4, 4, 4), (8, 8, 8), (12, 12, 12), (4, 12, 4)):
    Lx, Lt, Ny = 2 * P + Wb, 2 * P, 4 * P; x0 = P + (Wb - W) // 2; t = time.time()
    S = float(S3.FreeStrip(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1).S(cpts=12).real); dt = time.time() - t
    st = json.load(open(os.path.join(HERE, "exp081b_results", f"free_W{W}_P{P}_box{Wb}_c2.json")))["S"]
    print(f"W{W}P{P}b{Wb}: N = Lx*Lt = {Lx*Lt}, Ny {Ny}, 2W {2*W}: {dt:.2f} s; stored match {'BITWISE' if S == st else 'MISMATCH'}", flush=True)
