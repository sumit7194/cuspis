"""EXP-100 part A: free-side IR convergence along the box chain T(m) (registration notes/EXP-100_registration.md, 4dbbf5a + am. 1 d9edfa5).
T(m): hT = mP, g = Lt = 2hT, Ny = 2Lt = 4hT; arms g in {Lt/2, 2Lt}, Ny = 4Lt. Controls first. [model: Opus 5.5]"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, numpy, scipy
KF = 0.0396481; OUT = os.path.join(HERE, "exp081d_results", "exp100_free.json"); T0 = time.time(); TIMES = {}; CACHE = {}; FAILS = []
def S(W, g, hT, Ny):
    key = (W, g, hT, Ny)
    if key not in CACHE:
        t = time.time(); CACHE[key] = float(S3.FreeStrip(W + 2 * g, 2 * hT, Ny, list(range(g, g + W)), hT - 1).S(cpts=12).real); TIMES[key] = time.time() - t
    return CACHE[key]
def kap(Sa, Sb, a, b, Ny): return -(Sa - Sb) / Ny / (1 / a - 1 / b)
def check(n, ok, det=""):
    print(f"{n:76s} {'PASS' if ok else 'FAIL'} {det}", flush=True)
    if not ok: FAILS.append(n)
print(f"interpreter {sys.version.split()[0]} numpy {numpy.__version__} scipy {scipy.__version__}", flush=True)
J99 = json.load(open(os.path.join(HERE, "exp081d_results", "exp099_free.json")))["readings"]
for k in (1, 2, 3):
    P = 4 * k; v = S(P, P, P, 4 * P); st = J99[str(k)]["B_g1P"]["S"][str(P)]
    check(f"KA-sweep subset k={k}: S(W=P, g=P, hT=P, Ny=4P) == stored EXP-099 B_g1P (bitwise)", v == st)
    base = S(P, 2 * P, P, 4 * P)
    for nm, x in (("g=Lt/2", S(P, P, P, 4 * P)), ("g=2Lt", S(P, 4 * P, P, 4 * P)), ("Ny=4Lt", S(P, 2 * P, P, 8 * P))):
        check(f"wiring-neg k={k}: arm {nm} at T(1) changes S (> 1e-12 rel)", abs(x - base) > 1e-12 * abs(base), f"{x - base:+.2e}")
    a, b = S(P // 2, 2 * P, P, 4 * P), base; k0, k1 = kap(a, b, P // 2, P, 4 * P), kap(a, b, P // 2, P, 1.01 * 4 * P)
    check(f"plant k={k}: 1.01*Ny in the slope gives kappa/1.01 (1e-12 rel)", abs(k1 * 1.01 / k0 - 1) <= 1e-12, f"{k1 * 1.01 / k0 - 1:+.1e}")
if FAILS: print(f"CONTROLS FAILED {FAILS} -> STOP"); sys.exit(1)
print(f"[{time.time()-T0:.0f}s] controls PASS -> chain", flush=True)
R = {}
for k in (1, 2, 3):
    P = 4 * k; Ws = (P // 2, 3 * P // 4, P); R[str(k)] = {}; mmax = 16 if k < 3 else 8; prev_t = None; m = 1
    while m <= mmax:
        if prev_t is not None and prev_t * 8 > 900:
            print(f"k={k} m={m}: NOT SCHEDULED (predecessor {prev_t:.0f} s x 8 > 900 s)", flush=True); R[str(k)][f"m{m}"] = dict(scheduled=False, pred_time=prev_t); m *= 2; continue
        hT = m * P; Lt = 2 * hT; t = time.time(); r = {}
        for nm, (g, Ny) in (("T", (Lt, 2 * Lt)), ("g_half", (Lt // 2, 2 * Lt)), ("g_double", (2 * Lt, 2 * Lt)), ("Ny_double", (Lt, 4 * Lt))):
            s = {W: S(W, g, hT, Ny) for W in Ws}; W1, W3, W2 = Ws
            k12, k13, k32 = kap(s[W1], s[W2], W1, W2, Ny), kap(s[W1], s[W3], W1, W3, Ny), kap(s[W3], s[W2], W3, W2, Ny)
            r[nm] = dict(g=g, hT=hT, Ny=Ny, S={str(W): v for W, v in s.items()}, kappa12=k12, kappa13=k13, kappa32=k32, df=(k13 - k32) / k12, ratio_free=k12 / KF)
        ttime = time.time() - t; prev_t = sum(TIMES[(W, Lt, hT, 2 * Lt)] for W in Ws)
        r.update(scheduled=True, time=ttime, chain_time=prev_t, d_g_half=r["g_half"]["kappa12"] / r["T"]["kappa12"] - 1,
                 d_g_double=r["g_double"]["kappa12"] / r["T"]["kappa12"] - 1, d_Ny_double=r["Ny_double"]["kappa12"] / r["T"]["kappa12"] - 1)
        R[str(k)][f"m{m}"] = r
        print(f"k={k} m={m:2d} (hT {hT}, Lt {Lt}, Lx {P+2*Lt}, Ny {2*Lt}): kappa12 {r['T']['kappa12']:.6f} (/kf {r['T']['ratio_free']:.4f}) df {r['T']['df']:+.4f} | g->2Lt {r['d_g_double']:+.2e} g->Lt/2 {r['d_g_half']:+.2e} Ny->4Lt {r['d_Ny_double']:+.2e} [{ttime:.0f}s]", flush=True)
        m *= 2
V = {}
for k in (1, 2, 3):
    pts = [(int(mk[1:]), v) for mk, v in R[str(k)].items() if v.get("scheduled")]; pts.sort(); conv = None; steps = []
    for (m, v), nxt in zip(pts, pts[1:] + [None]):
        if nxt is None: break
        dT = nxt[1]["T"]["kappa12"] / v["T"]["kappa12"] - 1; steps.append((m, dT))
        if conv is None and abs(dT) < 0.01 and abs(v["d_g_double"]) < 0.01 and abs(v["d_Ny_double"]) < 0.01: conv = m
    if conv is None:
        V[str(k)] = dict(verdict="NOT CONVERGED within the affordable chain", steps=steps, last_m=pts[-1][0], last_ratio_free=pts[-1][1]["T"]["ratio_free"])
    else:
        rf = R[str(k)][f"m{conv}"]["T"]["ratio_free"]
        V[str(k)] = dict(verdict=f"CONVERGED at m* = {conv}", m_star=conv, steps=steps, uv_bracket=rf, mismatch_flag=not (0.85 <= rf <= 1.05))
    print(f"VERDICT k={k}: {V[str(k)]['verdict']}; chain steps (m -> 2m) {', '.join(f'{m}:{d:+.2e}' for m, d in steps)}"
          + (f"; UV bracket kappa_lat/kappa_free {V[str(k)]['uv_bracket']:.4f}, mismatch flag {V[str(k)]['mismatch_flag']}" if "uv_bracket" in V[str(k)] else ""), flush=True)
json.dump(dict(registration="4dbbf5a+d9edfa5", kappa_free=KF, chain=R, verdicts=V, times={str(k): t for k, t in TIMES.items()}), open(OUT, "w"), indent=1)
print(f"[{time.time()-T0:.0f}s] {len(CACHE)} geometries; slowest {max(TIMES.values()):.0f} s; wrote {os.path.relpath(OUT, HERE)}")
