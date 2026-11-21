"""EXP-081b worker (one geometry per fresh process): strip of width W centred in the pair box (Lx = 2P + Wbox, Lt = 2P),
sigma S^(0) via route_b (saddle, stable K, s_cut, N1' reliability, T0/T1 tails), result json into exp081b_results/.
Usage: python exp081b_worker.py W P Wbox c cpts s_cut drop_double  [model: Opus 5.5]"""
import sys, os, json, time
import sigma3d as S3
W, P, Wbox, c, cpts = (int(a) for a in sys.argv[1:6]); s_cut = float(sys.argv[6]); dd = sys.argv[7] == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "exp081b_results"); os.makedirs(OUT, exist_ok=True)
tag = f"sigma_W{W}_P{P}_box{Wbox}_c{c}_cp{cpts}_sc{s_cut}_dd{int(dd)}"
Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2; Ny = int(c * 2 * P)
t0 = time.time()
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=s_cut, drop_double=dd)
res = S3.route_b(S, os.path.join(OUT, tag + "_ckpt.json"), cpts=cpts)
res.update(dict(W=W, P=P, Wbox=Wbox, Ny=Ny, sec=time.time() - t0))
json.dump(res, open(os.path.join(OUT, tag + ".json"), "w"), indent=1)
print(tag, json.dumps(res), flush=True)
