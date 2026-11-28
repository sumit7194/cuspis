"""EXP-096 amendment 6 (Bridge ruling 2026-11-28 on W12P12 KA-complete): one-chip KA-complete + localisation. [model: Opus 5.5]
VERBATIM copy of exp096_t0_disc.py lines 1-162 (args, install, classes, off_disc, on_disc, pairs_of), with DIAGNOSTIC edits marked "# A6":
  (1) output name tag "_onoff"; (2) the Strip3D build is split from the install so STEP A (pole lists, no install) is written first;
  (3) the tail below replaces run_class: OFF_d / ON_d only (the od/on block of run_class, verbatim), no "mine".
STEP A: class members on THIS chip vs the Air's (exp096/W12P12Wb12Ny48.json): max |diff| reported; "same" if <= 1e-12.
STEP B: per class ON_d, OFF_d on this chip; KA-complete-1chip = sum(ON_d - OFF_d) - stored t0(ON) - t0(OFF) (exp087_t0_W12P12.json);
  localisation: per class (ON_d - OFF_d)_here - (ON_d - OFF_d)_Air, and ON_d, OFF_d separately.
PLANT (must fire; A6b, replaced after run 1): in class p = 16, disc +i c, the FIRST pair in pairs_of order whose partner q is in pset(16)
  (the two-tag same-object pair, (0,16) at W8P8 and W12P12) has its ON entry replaced by its OFF entry; the planted
  sum must move KA-complete-1chip by > 1e-8 (its |vn - vo| is reported). Usage: exp096_onoff.py 12 12 (CUSPIS_081E=1, as the stored runs); exp096_onoff.py 8 8 (flag unset) is the known-answer control:
  there the cross-chip KA-complete already closed to 1.1e-14, so here it must close too, and the plant must fire."""
import os, sys, json, time, argparse, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C

ap = argparse.ArgumentParser(); ap.add_argument("W", type=int); ap.add_argument("P", type=int)
ap.add_argument("--Ny", type=int, default=None); ap.add_argument("--Wb", type=int, default=None)
ap.add_argument("--classes", default=None); ap.add_argument("--probe", action="store_true"); ap.add_argument("--plant", action="store_true")
ap.add_argument("--tag", default=""); ap.add_argument("--M", type=int, default=32); ap.add_argument("--gdet", type=float, default=1e-4)
ap.add_argument("--budget-h", type=float, default=12.0)            # amendment 1/5: checkpoint PAUSE (resumable) at a class boundary if the projection exceeds it
a = ap.parse_args()
W, P = a.W, a.P; Wb = a.Wb if a.Wb else P; Ny = a.Ny if a.Ny else 4 * P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2
RAD, MRES, M, SCUT = 1e-5, 32, a.M, 3.0
OUT = os.path.join(HERE, "exp081d_results", "exp096"); os.makedirs(OUT, exist_ok=True)
name = f"W{W}P{P}Wb{Wb}Ny{Ny}{a.tag}{'_plant' if a.plant else ''}{'_probe' if a.probe else ''}"  + "_onoff"   # A6 (1)
def log(*x): print(*x, flush=True)
T0 = time.time()
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=SCUT)   # A6 (2): build split from install
AIR = json.load(open(os.path.join(OUT, f"W{W}P{P}Wb{Wb}Ny{Ny}.json")))["classes"]                                        # A6 STEP A
def _cls_here():
    out = []
    for p in range(Ny // 2 + 1):
        s = sorted(v for v in S.sl[p].s if v <= SCUT); cur = s[:1]; groups = []
        for v in s[1:]:
            if v - cur[-1] < a.gdet: cur.append(v)
            else: groups.append(cur); cur = [v]
        if cur: groups.append(cur)
        out += [(p, g) for g in groups if len(g) > 1]
    return out
_h = _cls_here(); _A = {X["p"]: X["members"] for X in AIR}
_same_list = sorted(p for p, _ in _h) == sorted(_A) and all(len(g) == len(_A[p]) for p, g in _h)
_dm = {p: max(abs(x - y) for x, y in zip(g, _A[p])) for p, g in _h if p in _A and len(g) == len(_A[p])}
_ds = {p: (g[-1] - g[0]) - (_A[p][-1] - _A[p][0]) for p, g in _h if p in _A and len(g) == len(_A[p])}
_mx = max(_dm.values()) if _dm else float("nan")
log(f"STEP A: class list here {[p for p, _ in _h]} vs Air {sorted(_A)}: same list {_same_list}; max |member diff| {_mx:.2e} -> "
    f"{'same (<= 1e-12)' if _same_list and _mx <= 1e-12 else 'DIFFER'}")
for p in sorted(_dm): log(f"  p={p:2d}: max |member diff| {_dm[p]:.2e}; span here - span Air {_ds[p]:+.2e}")
json.dump(dict(step="A", same_list=_same_list, max_member_diff=_mx, per_class={p: dict(dm=_dm[p], dspan=_ds[p]) for p in _dm},
               here=[(p, g) for p, g in _h]), open(os.path.join(OUT, f"{name}_stepA.json"), "w"), indent=1)
U = C.install(S, refine="auto", lowrank=True, rank_drop=0)                                                               # A6 (2)
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
    th = 2 * np.pi * np.arange(MRES) / MRES; out = np.zeros((S.N, S.N), dtype=complex); rad = RAD
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

# ---- ON entries inside a disc: copy of sigma3d.Strip3D._ib0_pair_087, plus the marked filter line
def on_disc(sa, sb, clA, clB, ad, r):
    rad, Mr = RAD, MRES
    def entries(sl, cls, tag, sign):
        mem = {v: c for c in cls for v in c}; out, seen = [], set()
        for sj in sl.s:
            if sj > S.s_cut: continue
            grp = mem.get(sj, [sj]); key = (grp[0], grp[-1])
            if key in seen: continue
            seen.add(key); c = 0.5 * (grp[0] + grp[-1])
            for sg in (sign, -sign): out.append((sg * 1j * c, tag, [sg * 1j * v for v in grp]))
        return out
    locs = entries(sa, clA, "a", 1) + entries(sb, clB, "b", -1)
    merged = []
    for a0, tag, mems in locs:
        hit = [m for m in merged if abs(m[0] - a0) < 1e-2 * rad]
        if hit: hit[0][1].add(tag); hit[0][2][tag] = mems
        else: merged.append([a0, {tag}, {tag: mems}])
    allpos = [sg * 1j * v for sl in (sa, sb) for v in sl.s for sg in (1, -1)]
    out = np.zeros((S.N, S.N), dtype=complex)
    for a0, tags, mems in merged:
        if abs(a0 - ad) >= r: continue                                   # EXP-096 FILTER (the only added line)
        up = a0.imag > 0
        if len(tags) == 2:
            pts = mems["a"] + mems["b"]; span = max(abs(x - y) for x in pts for y in pts); rc = 0.5 * span + rad
            S3.refuse_087(a0, rc, pts, allpos)
            off = max(abs(x - a0) for x in pts); ratio = off / rc
            Mc = Mr if ratio < 1e-3 else max(Mr, int(np.ceil(np.log(1e-17) / np.log(ratio))))
            tot = 0
            for t in 2 * np.pi * np.arange(Mc) / Mc:
                dz = rc * np.exp(1j * t); al = a0 + dz
                tot = tot + 2 * sa.G(al) * sb.G(-al) * ker(al, up) * dz
            out += (2j * np.pi) * tot / Mc
        elif "a" in tags:
            for am in mems["a"]:
                j = int(np.argmin([abs(abs(am.imag) - sj) for sj in sa.s]))
                out += (2j * np.pi) * 2 * sa.Rfull(sa.Rp[j] if am.imag > 0 else sa.Rm[j]) * sb.G(-am) * ker(am, am.imag > 0)
        else:
            for am in mems["b"]:
                j = int(np.argmin([abs(abs(am.imag) - sj) for sj in sb.s]))
                R = sb.Rfull(sb.Rp[j] if (-am).imag > 0 else sb.Rm[j])
                out += (2j * np.pi) * 2 * sa.G(am) * (-R) * ker(am, am.imag > 0)
    return out

def pairs_of(X):
    """all (k, p) with p or q = (k - p) % Ny in X's mirror class; each pair once"""
    cls = set(pset(X["p"])); out = []
    for k in range(Ny):
        for p in range(Ny):
            if p in cls or (k - p) % Ny in cls: out.append((k, p))
    obj = lambda x: min(x, Ny - x)                                       # group by the partner slice object, so the G cache hits
    return sorted(out, key=lambda kp: (kp[1] not in cls, obj((kp[0] - kp[1]) % Ny) if kp[1] in cls else obj(kp[1]), kp))


# ---- A6 (3): STEP B, OFF_d / ON_d only (verbatim od/on block of run_class), per pair recorded for class 16's plant
if (W, P) == (8, 8):                                                     # the known-answer control geometry: EXP-087 referee file
    REF = json.load(open(os.path.join(HERE, "exp081d_results", "exp087_referee_W8P8.json"))); FIX = REF["on_1e-5"] - REF["off_1e-5"]
else:
    REF = json.load(open(os.path.join(HERE, "exp081d_results", f"exp087_t0_W{W}P{P}.json"))); FIX = REF["on"] - REF["off"]
AIRC = {X["p"]: X for X in AIR}; cz = lambda v: complex(*v) if isinstance(v, list) else complex(v)
res, tot, plant = [], 0.0, None
def plant_idx(X, prs):                                                  # A6b (registered after run 1's plant could not fire): the FIRST pair
    cls = set(pset(X["p"]))                                              # of class 16 in pairs_of order whose partner q is in pset(16)
    return next(i for i, (k, p) in enumerate(prs) if (k - p) % Ny in cls)
if os.environ.get("PRECHECK") == "1":                                    # A6b pre-check: the plant pair's |ON - OFF| only, then exit
    X = [Y for Y in CL if Y["p"] == 16][0]; prs = pairs_of(X); i = plant_idx(X, prs); k, p = prs[i]; q = (k - p) % Ny; ad = 1j * X["c"]
    vo = tr(k, off_disc(S.sl[p], S.sl[q], ad, X["r1"])) / Ny; vn = tr(k, on_disc(S.sl[p], S.sl[q], on087[p], on087[q], ad, X["r1"])) / Ny
    log(f"PRECHECK A6b: class 16 plant pair {(k, p)} (index {i}, q {q}): |ON - OFF| = {abs((vn - vo).real):.3e} (needs > 1e-8 by a clear margin)")
    json.dump(dict(pair=(k, p), index=i, q=q, dvn=(vn - vo).real), open(os.path.join(OUT, f"{name}_precheck.json"), "w"), indent=1); sys.exit(0)
for X in CL:
    t = time.time(); r = X["r1"]; prs = pairs_of(X); od = on = 0j
    ipl = plant_idx(X, prs) if X["p"] == 16 else -1
    for sgn in (1, -1):
        ad = sgn * 1j * X["c"]
        for ip, (k, p) in enumerate(prs):
            q = (k - p) % Ny; sa, sb = S.sl[p], S.sl[q]
            o = off_disc(sa, sb, ad, r); vo = tr(k, o) / Ny
            vn = tr(k, on_disc(sa, sb, on087[p], on087[q], ad, r)) / Ny if (on087[p] or on087[q]) else vo
            od += vo; on += vn
            if X["p"] == 16 and sgn == 1 and ip == ipl: plant = dict(pair=(k, p), dvn=(vn - vo).real)   # A6b
    d_here = (on - od).real; tot += d_here; A_ = AIRC.get(X["p"])
    d_air = (cz(A_["on_r1"]) - cz(A_["off_r1"])).real if A_ else float("nan")
    rr = dict(p=X["p"], on=on.real, off=od.real, d_here=d_here, d_air=d_air, dd=d_here - d_air,
              d_on=on.real - cz(A_["on_r1"]).real if A_ else None, d_off=od.real - cz(A_["off_r1"]).real if A_ else None, sec=time.time() - t)
    res.append(rr)
    log(f"class p={X['p']:2d}: ON_d-OFF_d here {d_here:+.12e}  Air {d_air:+.12e}  here-Air {rr['dd']:+.2e}  "
        f"(ON here-Air {rr['d_on']:+.2e}, OFF here-Air {rr['d_off']:+.2e}; {rr['sec']:.0f}s)")
ka = tot - FIX; kp = (tot - plant["dvn"]) - FIX if plant else float("nan")
log(f"KA-complete-1chip: sum {tot:+.12f} - stored {FIX:+.12f} = {ka:+.2e} -> {'CLOSES (<= 1e-8)' if abs(ka) <= 1e-8 else 'OPEN'}")
log(f"  sum over classes of (here - Air) = {sum(x['dd'] for x in res):+.3e} (Air KA residual was -7.84e-07)")
log(f"PLANT: class 16 first pair {plant['pair'] if plant else None} |vn - vo| {abs(plant['dvn']) if plant else float('nan'):.2e}; "
    f"planted KA moves by {abs(kp - ka):.2e} -> {'FIRES (PASS)' if plant and abs(kp - ka) > 1e-8 else 'DOES NOT FIRE (FAIL)'}")
rd = ("R-a (cross-chip: closes on one chip)" if abs(ka) <= 1e-8 else
      "R-b (chip-independent: here = Air residual)" if abs(ka - (-7.84e-7)) <= 1e-8 else "UNCLASSIFIED")
log(f"READING: {rd}")
json.dump(dict(name=name, classes=res, fix_stored=FIX, sum=tot, ka=ka, plant=plant, plant_ka=kp, reading=rd,
               stats=dict(C.ExactSlice.STATS, bad=[str(b) for b in C.ExactSlice.STATS.get("bad", [])][:5])),
          open(os.path.join(OUT, f"{name}.json"), "w"), indent=1, default=str)
log(f"done: {len(res)} classes, NG {NG[0]}, unconverged {C.ExactSlice.STATS.get('unconverged')}, wall {time.time() - T0:.0f}s")
