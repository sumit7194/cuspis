"""EXP-096 amendment 4, step 2: WHOLE-SUM referee rad sweep at W8P8 (the outside-entry 7.8e-7). [model: Opus 5.5]
Lines from "import os" to the end of pairs_of_diag are exp096_diag_rad.py verbatim (itself exp096_t0_disc.py verbatim plus 3 marked
DIAGNOSTIC edits), except the output name. Then:
  whole OFF t0(rad) = sum_k Tr(B1_k^{-1} dB0_k), dB0 = S.inner_beta0(1, rad=rad, dn=True), flag 087 OFF (as exp087_referee_W8P8.py),
      at rad 1e-6 (KA: equals the Mac referee -209.27942615304573 to <= 2.1e-8 abs = 1e-10 x 209.3, the cross-platform TOL),
      2e-6 and 5e-7;
  class OFF_d at rad 1e-6 (KA: bitwise against exp096/W8P8Wb8Ny32_diagrad.json, same platform) and 2e-6 (new);
      class OFF_d at 5e-7 is taken from that JSON (same code, same platform).
  out(rad) = whole(rad) - sum_classes OFF_d(rad): the part of t0 outside the 9 class discs.
Readings (registered, amendment 4): d1 = out(2e-6) - out(1e-6), d2 = out(5e-7) - out(1e-6).
  R-real : |d2| <= 1e-7  -> the outside part is stable below 1e-6: the referee's 7.8e-7 is a REAL rad dependence of production t0
           outside the clusters (rad 1e-5 vs small rad); d1 says whether the step lies above or below 2e-6.
  R-noise: |d2| >= 3e-7  -> the whole-sum referee is noise-limited at that level; the 7.8e-7 is not a measured truth.
  else   : UNCLASSIFIED.  Prints values (a debug diagnostic of a failed control; no sealed band rides on it)."""
import os, sys, json, time, argparse, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C

ap = argparse.ArgumentParser(); ap.add_argument("W", type=int); ap.add_argument("P", type=int)
ap.add_argument("--Ny", type=int, default=None); ap.add_argument("--Wb", type=int, default=None)
ap.add_argument("--classes", default=None); ap.add_argument("--probe", action="store_true"); ap.add_argument("--plant", action="store_true")
ap.add_argument("--tag", default=""); ap.add_argument("--M", type=int, default=32); ap.add_argument("--gdet", type=float, default=1e-4)
ap.add_argument("--budget-h", type=float, default=12.0)            # amendment 1: checkpoint stop at a class boundary if the projection exceeds it
ap.add_argument("--rads", default="1e-5,1e-6,5e-7,3e-7")            # DIAGNOSTIC: rad values for the OFF entries
a = ap.parse_args()
W, P = a.W, a.P; Wb = a.Wb if a.Wb else P; Ny = a.Ny if a.Ny else 4 * P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2
RAD, MRES, M, SCUT = 1e-5, 32, a.M, 3.0
OUT = os.path.join(HERE, "exp081d_results", "exp096"); os.makedirs(OUT, exist_ok=True)
name = f"W{W}P{P}Wb{Wb}Ny{Ny}{a.tag}_refsweep"
def log(*x): print(*x, flush=True)
T0 = time.time()
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=SCUT); U = C.install(S, refine="auto", lowrank=True, rank_drop=0)
B1 = S.B1(); T_INST = time.time() - T0; log(f"{name}: installed + B1 ({T_INST:.0f}s), N {S.N}")
for k in range(Ny): B1[k] = np.linalg.inv(B1[k]).T          # in place: Binv_T[k] = inv(B1_k)^T, so Tr(B1_k^{-1} X) = sum(Binv_T[k] * X)
BT = B1; del B1
def tr(k, X): return complex(np.dot(BT[k].ravel(), X.ravel()))

# ---- G cache (keyed by slice object and alpha; mirror slices are one object) shared by all three evaluations
_cache = collections.OrderedDict(); CMAX = 12; NG = [0]
def Gc(sl, al):
    key = (id(sl), complex(al))
    if key in _cache: _cache.move_to_end(key); return _cache[key]
    v = C.ExactSlice.G(sl, al).copy(); NG[0] += 1; _cache[key] = v
    if len(_cache) > CMAX: _cache.popitem(last=False)
    return v
uniq = {id(s): s for s in S.sl}
for s in uniq.values(): s.G = (lambda al, _s=s: Gc(_s, al))           # the copied production code below calls sa.G(.)
C.ExactSlice.reset_stats()

def ker(al, up):                                                         # inner_beta0 ker, n = 1, dn = True (verbatim)
    n = 1.0; e = np.exp(-2j * np.pi * n * al) if up else np.exp(2j * np.pi * n * al)
    return 2j * np.pi * al * e / (e - 1) ** 2

# ---- own cluster detection (independent of clusters_087): single linkage at gap < gdet, per unique slice class
def classes_of():
    out = []
    for p in range(Ny // 2 + 1):
        s = sorted(v for v in S.sl[p].s if v <= SCUT); cur = s[:1]
        groups = []
        for v in s[1:]:
            if v - cur[-1] < a.gdet: cur.append(v)
            else: groups.append(cur); cur = [v]
        if cur: groups.append(cur)
        for g in groups:
            if len(g) > 1: out.append(dict(p=p, members=g, c=float(np.mean(g)), half=0.5 * (g[-1] - g[0])))
    allp = sorted(v for p in range(Ny // 2 + 1) for v in S.sl[p].s if v <= SCUT)
    for X in out:
        others = [v for v in allp if min(abs(v - m) for m in X["members"]) > 1e-12]
        X["dmin"] = float(min(abs(v - X["c"]) for v in others)); X["r1"] = min(1e-3, X["dmin"] / 3); X["r2"] = max(X["r1"] / 3, 10 * X["half"])   # amendment 1: r2 >= 10 x half-span
        X["ok"] = X["r2"] <= X["r1"] / 1.5                                               # the r-sweep must still span >= 1.5x
    return out
CL = classes_of()
on087 = [S3.clusters_087(sl.s, RAD, SCUT) for sl in S.sl]
for p in range(Ny):                                                      # every EXP-087 cluster must sit inside one of my discs
    for g in on087[p]:
        pc = p if p <= Ny // 2 else Ny - p
        assert any(X["p"] == pc and all(abs(v - X["c"]) < X["r2"] for v in g) for X in CL), f"087 cluster {g} at slice {p} not covered"
log(f"classes: {[(X['p'], len(X['members']), f'{2*X['half']:.1e}', f'{X['c']:.4f}', f'{X['r1']:.1e}', X['ok']) for X in CL]}")
bad = [X for X in CL if not X["ok"]]
if bad: log(f"REFUSE: 10 x half-span > r1/1.5 for classes {[X['p'] for X in bad]}"); sys.exit(3)
pset = lambda p: sorted({p % Ny, (Ny - p) % Ny})

# ---- OFF entries inside a disc: copy of sigma3d.Strip3D.inner_beta0 inner loop (one pair), plus the marked filter line
def off_disc(sa, sb, ad, r):
    th = 2 * np.pi * np.arange(MRES) / MRES; out = np.zeros((S.N, S.N), dtype=complex); rad = RADX[0]   # DIAGNOSTIC: rad from RADX
    locs = [(a0, "a") for sj in sa.s if sj <= S.s_cut for a0 in (1j * sj, -1j * sj)] + \
           [(a0, "b") for sj in sb.s if sj <= S.s_cut for a0 in (-1j * sj, 1j * sj)]
    merged = []
    for a0, tag in locs:
        hit = [m for m in merged if abs(m[0] - a0) < 1e-2 * rad]
        if hit: hit[0][1].add(tag)
        else: merged.append([a0, {tag}])
    for a0, tags in merged:
        if abs(a0 - ad) >= r: continue                                   # EXP-096 FILTER (the only added line)
        up = a0.imag > 0
        if len(tags) == 2:
            tot = 0
            for t in th:
                dz = rad * np.exp(1j * t); al = a0 + dz
                tot = tot + 2 * sa.G(al) * sb.G(-al) * ker(al, up) * dz
            out += (2j * np.pi) * tot / MRES
        elif "a" in tags:
            j = int(np.argmin([abs(abs(a0.imag) - sj) for sj in sa.s]))
            out += (2j * np.pi) * 2 * sa.Rfull(sa.Rp[j] if up else sa.Rm[j]) * sb.G(-a0) * ker(a0, up)
        else:
            j = int(np.argmin([abs(abs(a0.imag) - sj) for sj in sb.s]))
            R = sb.Rfull(sb.Rp[j] if (-a0).imag > 0 else sb.Rm[j])
            out += (2j * np.pi) * 2 * sa.G(a0) * (-R) * ker(a0, up)
    return out

def pairs_of_diag(X):   # verbatim copy of pairs_of
    """all (k, p) with p or q = (k - p) % Ny in X's mirror class; each pair once"""
    cls = set(pset(X["p"])); out = []
    for k in range(Ny):
        for p in range(Ny):
            if p in cls or (k - p) % Ny in cls: out.append((k, p))
    obj = lambda x: min(x, Ny - x)                                       # group by the partner slice object, so the G cache hits
    return sorted(out, key=lambda kp: (kp[1] not in cls, obj((kp[0] - kp[1]) % Ny) if kp[1] in cls else obj(kp[1]), kp))


RADX = [RAD]
REFD = {X["p"]: X for X in json.load(open(os.path.join(OUT, f"W{W}P{P}Wb{Wb}Ny{Ny}{a.tag}_diagrad.json")))["classes"]}
REFW = json.load(open(os.path.join(HERE, "exp081d_results", "exp087_referee_W8P8.json")))
res = dict(name=name, whole={}, cls={}, sec={})
def classes_at(rv):
    RADX[0] = rv; tot = 0.0
    for X in CL:
        prs = pairs_of_diag(X); od = 0j
        for sgn in (1, -1):
            ad = sgn * 1j * X["c"]
            for (k, p) in prs:
                q = (k - p) % Ny; od += tr(k, off_disc(S.sl[p], S.sl[q], ad, X["r1"])) / Ny
        res["cls"].setdefault(f"{rv:.0e}", {})[str(X["p"])] = od.real; tot += od.real
    return tot
def whole_at(rv):
    S3.INNER_BETA0_087 = False; t = time.time(); dB0 = S.inner_beta0(1.0, rad=rv, dn=True)
    v = float(sum(tr(k, dB0[k]) for k in range(Ny)).real); del dB0; res["sec"][f"whole_{rv:.0e}"] = time.time() - t; return v
c6 = classes_at(1e-6)
ka1 = max(abs(res["cls"]["1e-06"][str(p)] - REFD[p]["off_1e-06"]) for p in REFD)
log(f"KA-1 class OFF_d(1e-6) bitwise vs diagrad JSON: {'PASS' if ka1 == 0.0 else 'FAIL'} max {ka1:.1e}")
c2 = classes_at(2e-6); c5 = sum(REFD[p]["off_5e-07"] for p in REFD)
dump = lambda: json.dump(res, open(os.path.join(OUT, f"{name}.json"), "w"), indent=1)
w6 = whole_at(1e-6); res["whole"]["1e-06"] = w6; dump()
ka2 = abs(w6 - REFW["off_1e-6"]); log(f"KA-2 whole OFF(1e-6) vs Mac referee {REFW['off_1e-6']:+.12f}: {'PASS' if ka2 <= 2.1e-8 else 'FAIL'} |diff| {ka2:.1e}")
w2 = whole_at(2e-6); res["whole"]["2e-06"] = w2; dump()
w5 = whole_at(5e-7); res["whole"]["5e-07"] = w5; dump()
out = {"1e-06": w6 - c6, "2e-06": w2 - c2, "5e-07": w5 - c5}
c10 = sum(json.load(open(os.path.join(OUT, f"W{W}P{P}Wb{Wb}Ny{Ny}{a.tag}.json")))["classes"][i]["off_r1"][0] for i in range(len(CL)))
out["1e-05"] = REFW["off_1e-5"] - c10                                    # mixed platform (Mac whole, Air classes): ~2e-8
d1, d2 = out["2e-06"] - out["1e-06"], out["5e-07"] - out["1e-06"]
rd = "R-real" if abs(d2) <= 1e-7 else "R-noise" if abs(d2) >= 3e-7 else "UNCLASSIFIED"
res.update(out=out, d1=d1, d2=d2, reading=rd, ka=dict(ka1=ka1, ka2=ka2)); dump()
log("out(rad) = whole - classes: " + "  ".join(f"{k} {v:+.10e}" for k, v in out.items()))
log(f"out(1e-6) - out(1e-5) = {out['1e-06'] - out['1e-05']:+.3e} (the referee gap, +7.8e-7 expected to ~2e-8);  d1 = {d1:+.3e}  d2 = {d2:+.3e}  ->  {rd}")
log(f"done: unconverged {C.ExactSlice.STATS.get('unconverged')}, wall {time.time()-T0:.0f}s")
