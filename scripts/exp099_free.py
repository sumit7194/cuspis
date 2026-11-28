"""EXP-099 free-side sweep (registration notes/EXP-099_registration.md, 1ac1ad1). [model: Opus 5.5]
Controls FIRST (KA-sweep on all stored free caches, KA-base and negative arm wiring, plants 1 and 2); readings only if all PASS.
Geometry G = (W, gL, gR, hT, Ny): Lx = gL + W + gR, Lt = 2 hT, tcut = hT - 1, cut columns gL .. gL + W - 1.
S(G) = sigma3d.FreeStrip(Lx, Lt, Ny, cols, tcut).S(cpts=12).real, the call exp081b_run.free makes. Output exp081d_results/exp099_free.json."""
import os, sys, json, time, glob, re, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, numpy, scipy
OUT = os.path.join(HERE, "exp081d_results", "exp099_free.json"); FB = os.path.join(HERE, "exp081b_results")
T0 = time.time(); CACHE, TIMES = {}, {}; FAILS = []
def S(W, gL, gR, hT, Ny):
    key = (W, gL, gR, hT, Ny)
    if key not in CACHE:
        t = time.time(); Lx, Lt = gL + W + gR, 2 * hT
        CACHE[key] = float(S3.FreeStrip(Lx, Lt, Ny, list(range(gL, gL + W)), hT - 1).S(cpts=12).real); TIMES[key] = time.time() - t
    return CACHE[key]
def gA(W, P): gL = P + (P - W) // 2; return gL, 3 * P - gL - W            # convention A (Wb = P)
def A(W, P): gL, gR = gA(W, P); return S(W, gL, gR, P, 4 * P)
def B(W, P, g): return S(W, g, g, P, 4 * P)
def C(W, P, h): gL, gR = gA(W, P); return S(W, gL, gR, h, 4 * P)
def Dy(W, P, n): gL, gR = gA(W, P); return S(W, gL, gR, P, n)
def E(W, P): return S(W, 8 * P, 8 * P, 4 * P, 16 * P)
def check(name, ok, detail=""):
    print(f"{name:78s} {'PASS' if ok else 'FAIL'}  {detail}", flush=True)
    if not ok: FAILS.append(name)
print(f"[{time.time()-T0:5.0f}s] interpreter {sys.version.split()[0]} numpy {numpy.__version__} scipy {scipy.__version__}", flush=True)

# ---------------- controls
stored = sorted(glob.glob(os.path.join(FB, "free_W*_P*_box*_c2.json"))); n_ok = 0
for f in stored:
    W, P, Wb = map(int, re.match(r"free_W(\d+)_P(\d+)_box(\d+)_c2\.json", os.path.basename(f)).groups())
    gL = P + (Wb - W) // 2; v = S(W, gL, 2 * P + Wb - gL - W, P, 4 * P); st = json.load(open(f))["S"]; n_ok += (v == st)
    if v != st: print(f"   KA-sweep MISMATCH {os.path.basename(f)}: {v!r} vs {st!r}")
check(f"KA-sweep: {len(stored)} stored free caches reproduced bitwise", n_ok == len(stored) and len(stored) == 23, f"{n_ok}/{len(stored)}")
for k in (1, 2, 3):
    P = 4 * k
    check(f"KA-base k={k}: B(g=P) at W=P == A (bitwise)", B(P, P, P) == A(P, P))
    for W in (P // 2, 3 * P // 4, P):
        check(f"KA-base k={k} W={W}: C(hT=P) == A and Dy(Ny=4P) == A (bitwise)", C(W, P, P) == A(W, P) and Dy(W, P, 4 * P) == A(W, P))
    a = A(P, P)
    for nm, v in (("B(2P)", B(P, P, 2 * P)), ("C(2P)", C(P, P, 2 * P)), ("Dy(8P)", Dy(P, P, 8 * P))):
        check(f"wiring-neg k={k}: {nm} at W=P differs from A (> 1e-12 rel)", abs(v - a) > 1e-12 * abs(a), f"{v - a:+.3e}")
s0 = B(2, 4, 4); s1 = S(2, 5, 3, 4, 16)
check("Plant 1: strip shifted one column (gL+1, gR-1) at W2P4, g=P changes S (> 1e-9 rel) -> FIRES", abs(s1 - s0) > 1e-9 * abs(s0), f"{s1 - s0:+.3e}")
gL, gR = gA(2, 4); s2 = float(S3.FreeStrip(gL + 2 + gR, 8, 16, list(range(gL, gL + 2)), 4 - 2).S(cpts=12).real); s3 = A(2, 4)
check("Plant 2: cut row tcut = hT - 2 at W2P4 (A) changes S (> 1e-9 rel) -> FIRES", abs(s2 - s3) > 1e-9 * abs(s3), f"{s2 - s3:+.3e}")
if FAILS:
    print(f"CONTROLS FAILED: {FAILS} -> STOP, no reading printed"); sys.exit(1)
print(f"[{time.time()-T0:5.0f}s] all controls PASS -> readings", flush=True)

# ---------------- readings
def kap(Sa, Sb, a, b, Ny): return -(Sa - Sb) / Ny / (1 / a - 1 / b)
def fam(k, fn, Ny):
    P = 4 * k; W1, W3, W2 = P // 2, 3 * P // 4, P; s = {W: fn(W, P) for W in (W1, W3, W2)}
    k13, k32, k12 = kap(s[W1], s[W3], W1, W3, Ny), kap(s[W3], s[W2], W3, W2, Ny), kap(s[W1], s[W2], W1, W2, Ny)
    return dict(S={str(W): v for W, v in s.items()}, kappa13=k13, kappa32=k32, kappa12=k12, df=(k13 - k32) / k12)
R = {}
for k in (1, 2, 3):
    P = 4 * k; r = {"A": fam(k, A, 4 * P)}
    for m in (1, 2, 4, 8): r[f"B_g{m}P"] = fam(k, lambda W, P_: B(W, P_, m * P_), 4 * P)
    for m in (1, 2, 4): r[f"C_h{m}P"] = fam(k, lambda W, P_: C(W, P_, m * P_), 4 * P)
    for m in (4, 8, 16): r[f"Dy_{m}P"] = fam(k, lambda W, P_: Dy(W, P_, m * P_), m * P)
    r["E"] = fam(k, E, 16 * P)
    ex = {}
    for W in (P // 2, 3 * P // 4, P):
        d = [B(W, P, m * P) - B(W, P, 2 * m * P) for m in (1, 2, 4)]
        a1 = math.log2(d[0] / d[1]) if d[0] * d[1] > 0 else float("nan"); a2 = math.log2(d[1] / d[2]) if d[1] * d[2] > 0 else float("nan")
        ex[str(W)] = dict(dS=d, a_P_2P_4P=a1, a_2P_4P_8P=a2, drift=abs(a1 - a2), stable=abs(a1 - a2) <= 0.3)
    r["edge_exponent_B"] = ex; R[str(k)] = r
def verdict(arm_key):
    v = [abs(R[str(k)][arm_key]["df"]) for k in (1, 2, 3)]; a = [abs(R[str(k)]["A"]["df"]) for k in (1, 2, 3)]
    if all(x <= 0.10 for x in v): return "REMOVED", v
    if all(x >= 0.5 * y for x, y in zip(v, a)): return "NOT REMOVED", v
    return "PARTIAL", v
V = {"x (b) B_g8P": verdict("B_g8P"), "t (c) C_h4P": verdict("C_h4P"), "y (d) Dy_16P": verdict("Dy_16P")}
eE = [abs(R[str(k)]["E"]["df"]) for k in (1, 2, 3)]; aA = [abs(R[str(k)]["A"]["df"]) for k in (1, 2, 3)]
intrinsic = all(v[0] == "NOT REMOVED" for v in V.values()) and all(x >= 0.5 * y for x, y in zip(eE, aA))
for k in (1, 2, 3):
    print(f"\nk = {k} (P = {4*k}; W = {2*k}, {3*k}, {4*k}): df by family  [kappa13 / kappa32 / kappa12]")
    for nm, r in R[str(k)].items():
        if nm.startswith("edge"): continue
        print(f"   {nm:8s} df {r['df']:+.4f}   [{r['kappa13']:.6f} / {r['kappa32']:.6f} / {r['kappa12']:.6f}]")
    for W, e in R[str(k)]["edge_exponent_B"].items():
        print(f"   edge exponent (B, W={W}): a(P,2P,4P) {e['a_P_2P_4P']:+.3f}  a(2P,4P,8P) {e['a_2P_4P_8P']:+.3f}  drift {e['drift']:.3f} -> {'stable' if e['stable'] else 'NO stable exponent'} (descriptive)")
print("\nVERDICTS (registered criteria, section 4):")
for nm, (v, xs) in V.items(): print(f"   {nm:14s} {v:12s} |df| at k=1,2,3: {', '.join(f'{x:.4f}' for x in xs)}")
print(f"   (e) all large (descriptive): |df| {', '.join(f'{x:.4f}' for x in eE)};  INTRINSIC: {intrinsic}")
json.dump(dict(registration="1ac1ad1", readings=R, verdicts={k: dict(verdict=v[0], absdf=v[1]) for k, v in V.items()},
               E_absdf=eE, A_absdf=aA, intrinsic=intrinsic, times={str(k): t for k, t in TIMES.items()},
               W9P12_note="free(9,12) seen here does NOT amend seal fb6060f; the D(3) census gate stands"), open(OUT, "w"), indent=1)
print(f"\n[{time.time()-T0:5.0f}s] {len(CACHE)} geometries; slowest {max(TIMES.values()):.1f} s at {max(TIMES, key=TIMES.get)}; wrote {os.path.relpath(OUT, HERE)}")
