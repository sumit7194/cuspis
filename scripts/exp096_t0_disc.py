"""EXP-096 (registration notes/EXP-096_097_registration.md): independent truth route for the EXP-087 t0 cluster correction.
[model: Opus 5.5]

t0 = sum_k Tr(B1_k^{-1} dB0_k), dB0 = S.inner_beta0(1, dn=True): per pair (k, p), q = (k - p) % Ny, a sum over pole entries a0 of
2 pi i Res_{a0}[2 G_p(a) o G_q(-a) ker(a)] / Ny.  The production code (OFF) and the EXP-087 fix (ON) evaluate the entries at a
same-slice pole CLUSTER from stored near-pole residues (radius 0.3 x gap) and small contours (rad = 1e-5).
This route replaces, for every pair touching a cluster, ALL entries inside a WIDE disc (radius r_X, set from the pole lists: far from
every other pole, >= 10 x the cluster half-span (r2 = r1/3)) by ONE trapezoid contour of the full integrand on that disc: no residues, no pole
positions inside the disc, no rad, no cluster bookkeeping. The cluster detection is its own (single linkage at gap < 1e-4).
Per disc it also evaluates the OFF and ON entries inside the disc (copies of sigma3d.inner_beta0 / _ib0_pair_087, with ONE added
filter line), so that:  KA-complete: sum(ON_d - OFF_d) == stored t0(ON) - t0(OFF);  D = sum(mine - ON_d) = truth - fix.
Usage: exp096_t0_disc.py W P [--Ny N] [--Wb B] [--classes i,j,..] [--probe] [--plant] [--tag T]
  --probe: install + B1 + timing of 8 contour G evaluations and one class at r1 (footprint/time measure), writes *_probe.json
  --plant: must-fail control: every disc centre shifted by 3 r_X along the real axis (encloses no pole) -> mine must lose the cluster."""
import os, sys, json, time, argparse, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C

ap = argparse.ArgumentParser(); ap.add_argument("W", type=int); ap.add_argument("P", type=int)
ap.add_argument("--Ny", type=int, default=None); ap.add_argument("--Wb", type=int, default=None)
ap.add_argument("--classes", default=None); ap.add_argument("--probe", action="store_true"); ap.add_argument("--plant", action="store_true")
ap.add_argument("--tag", default=""); ap.add_argument("--M", type=int, default=32); ap.add_argument("--gdet", type=float, default=1e-4)
a = ap.parse_args()
W, P = a.W, a.P; Wb = a.Wb if a.Wb else P; Ny = a.Ny if a.Ny else 4 * P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2
RAD, MRES, M, SCUT = 1e-5, 32, a.M, 3.0
OUT = os.path.join(HERE, "exp081d_results", "exp096"); os.makedirs(OUT, exist_ok=True)
name = f"W{W}P{P}Wb{Wb}Ny{Ny}{a.tag}{'_plant' if a.plant else ''}{'_probe' if a.probe else ''}"
def log(*x): print(*x, flush=True)
T0 = time.time()
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=SCUT); U = C.install(S, refine="auto", lowrank=True, rank_drop=0)
B1 = S.B1(); log(f"{name}: installed + B1 ({time.time()-T0:.0f}s), N {S.N}")
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
        X["dmin"] = float(min(abs(v - X["c"]) for v in others)); X["r1"] = min(1e-3, X["dmin"] / 3); X["r2"] = X["r1"] / 3
        X["ok"] = X["r2"] >= 10 * X["half"]
    return out
CL = classes_of()
on087 = [S3.clusters_087(sl.s, RAD, SCUT) for sl in S.sl]
for p in range(Ny):                                                      # every EXP-087 cluster must sit inside one of my discs
    for g in on087[p]:
        pc = p if p <= Ny // 2 else Ny - p
        assert any(X["p"] == pc and all(abs(v - X["c"]) < X["r2"] for v in g) for X in CL), f"087 cluster {g} at slice {p} not covered"
log(f"classes: {[(X['p'], len(X['members']), f'{2*X['half']:.1e}', f'{X['c']:.4f}', f'{X['r1']:.1e}', X['ok']) for X in CL]}")
bad = [X for X in CL if not X["ok"]]
if bad: log(f"REFUSE: r2 < 10 x half-span for classes {[X['p'] for X in bad]}"); sys.exit(3)
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

def run_class(X, radii=("r1", "r2"), npts=None):
    """mine (wide-disc contour, M and M/2 grids), OFF_d and ON_d inside the disc, for both discs (+i c, -i c) of class X"""
    t = time.time(); res = dict(p=X["p"], members=X["members"], c=X["c"], half=X["half"], dmin=X["dmin"])
    prs = pairs_of(X); cls = set(pset(X["p"]))
    shift = 3 * X["r1"] if a.plant else 0.0
    for rk in radii:
        r = X[rk]; acc = {"M": 0j, "M2": 0j}
        for sgn in (1, -1):                                              # disc centres +i c and -i c
            ad = sgn * 1j * X["c"] + shift; up = sgn > 0
            mlist = range(M) if npts is None else range(npts)
            for m in mlist:
                dz = r * np.exp(2j * np.pi * m / M); al = ad + dz; w = (2j * np.pi) * 2 * ker(al, up) * dz / M / Ny
                for (k, p) in prs:                                       # mirror-equal slices hit the G cache
                    q = (k - p) % Ny
                    v = w * tr(k, Gc(S.sl[p], al) * Gc(S.sl[q], -al))
                    acc["M"] += v
                    if m % 2 == 0: acc["M2"] += 2 * v
        res[f"mine_{rk}"] = acc["M"]; res[f"mine_{rk}_M2"] = acc["M2"]
        if npts is not None: break
        if a.plant or rk != "r1": continue                               # OFF/ON entries inside r1 and r2 are the same set (r1 <= dmin/3)
        od = on = 0j; nentries = 0
        for sgn in (1, -1):
            ad = sgn * 1j * X["c"]
            for (k, p) in prs:
                q = (k - p) % Ny; sa, sb = S.sl[p], S.sl[q]
                o = off_disc(sa, sb, ad, r); vo = tr(k, o) / Ny
                vn = tr(k, on_disc(sa, sb, on087[p], on087[q], ad, r)) / Ny if (on087[p] or on087[q]) else vo
                od += vo; on += vn
        res[f"off_{rk}"] = od; res[f"on_{rk}"] = on
    res["sec"] = time.time() - t; res["npairs"] = len(prs); return res

if a.probe:
    X = CL[0] if a.classes is None else [Y for Y in CL if Y["p"] == int(a.classes.split(",")[0])][0]
    t = time.time(); n0 = NG[0]
    for m in range(8): Gc(S.sl[X["p"]], 1j * X["c"] + X["r1"] * np.exp(2j * np.pi * m / M) + 0.123)   # 8 fresh evaluations
    tg = (time.time() - t) / max(NG[0] - n0, 1)
    rc = run_class(X, radii=("r1",), npts=2); log(f"probe: {tg:.3f} s per G eval; class {X['p']} 2 points x {rc['npairs']} pairs in {rc['sec']:.0f}s")
    json.dump(dict(name=name, N=S.N, Ny=Ny, sec_install=None, sec_per_G=tg, classes=[dict(p=Y["p"], n=len(Y["members"]), c=Y["c"], half=Y["half"],
              dmin=Y["dmin"], r1=Y["r1"]) for Y in CL], class_probe=dict(p=X["p"], sec_2pts=rc["sec"], npairs=rc["npairs"]), wall=time.time() - T0,
              stats=dict(C.ExactSlice.STATS, bad=[str(b) for b in C.ExactSlice.STATS.get("bad", [])][:5])),
              open(os.path.join(OUT, f"{name}.json"), "w"), indent=1, default=str)
    sys.exit(0)

sel = CL if a.classes is None else [X for X in CL if X["p"] in [int(c) for c in a.classes.split(",")]]
allres = []
for X in sel:
    rc = run_class(X); allres.append(rc)
    log(f"class p={X['p']:2d} ({len(X['members'])} members, span {2*X['half']:.1e}, r1 {X['r1']:.1e}): "
        + " ".join(f"{kk} {v.real:+.12e}" for kk, v in rc.items() if kk.startswith(("mine", "off", "on")))
        + f"  ({rc['sec']:.0f}s, {rc['npairs']} pairs)")
    json.dump(dict(name=name, classes=allres, NG=NG[0], stats=dict(C.ExactSlice.STATS, bad=[str(b) for b in C.ExactSlice.STATS.get("bad", [])][:5])),
              open(os.path.join(OUT, f"{name}{'_c' + a.classes.replace(',', '-') if a.classes else ''}.json"), "w"), indent=1,
              default=lambda z: [z.real, z.imag] if isinstance(z, complex) else str(z))
log(f"done: {len(allres)} classes, {NG[0]} G evaluations, unconverged {C.ExactSlice.STATS.get('unconverged')}, wall {time.time()-T0:.0f}s")
