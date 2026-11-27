"""EXP-096 amendment 4, step 1: POLE-LIST SCAN (premortem for W12P12). No install, no t0, no G: pole lists only.
[model: Opus 5.5]
Pole lists come from sigma3d.Slice.poles() at construction (CUSPIS_081E read at import: the runner sets it as for the stored runs);
C.install only iterates over them, so Strip3D(...).sl[p].s IS the production list. Usage: exp096_scan.py W P
Fires (registered, amendment 4):
  S1  any pole s <= 1e-5 (s <= s_cut): the radius-1e-5 contour around +-i s would enclose the kernel's pole at alpha = 0.
  S2  any CROSS-slice pole gap |s_a - s_b| < 1e-6 between two distinct slice objects (the 1e-2 rad merge threshold is 1e-7 at rad 1e-5,
      1e-8 at rad 1e-6): a merge that trips near threshold. Bins reported: < 1e-8, [1e-8, 1e-7), [1e-7, 1e-6), [1e-6, 3e-5).
Reported (no fire): S3 same-slice classes at gap < 1e-4 (KA: must reproduce the class lists the route printed) and the smallest
same-slice gap outside them; S4 the count of two-tag entries (same-object pairs) outside vs inside the class discs.
Plant (must FIRE): copies of the lists with one pole at s = 5e-6 added (S1) and one pole of another slice copied at +5e-8 (S2)."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
W, P = int(sys.argv[1]), int(sys.argv[2]); Wb, Ny = P, 4 * P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; SCUT = 3.0
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=SCUT)
uniq = list(range(Ny // 2 + 1))                                          # slice objects p and Ny - p are mirror-equal
L = {p: sorted(float(v) for v in S.sl[p].s if v <= SCUT) for p in uniq}

def scan(L):
    out = {}
    allv = [(v, p) for p in L for v in L[p]]
    out["S1_min_s"] = min(v for v, _ in allv); out["S1_hits"] = [(p, v) for v, p in allv if v <= 1e-5]
    out["S1_near_3e-5"] = [(p, v) for v, p in allv if v < 3e-5]
    bins = {"<1e-8": [], "[1e-8,1e-7)": [], "[1e-7,1e-6)": [], "[1e-6,3e-5)": []}; gmin = (np.inf, None)
    ps = sorted(L)
    for i, p1 in enumerate(ps):
        a = np.array(L[p1])
        for p2 in ps[i + 1:]:
            b = np.array(L[p2])
            if not len(a) or not len(b): continue
            j = np.searchsorted(b, a)
            for ii, jj in enumerate(j):
                for k in (jj - 1, jj):
                    if 0 <= k < len(b):
                        g = abs(a[ii] - b[k])
                        if g < gmin[0]: gmin = (g, (p1, p2, a[ii]))
                        key = "<1e-8" if g < 1e-8 else "[1e-8,1e-7)" if g < 1e-7 else "[1e-7,1e-6)" if g < 1e-6 else "[1e-6,3e-5)" if g < 3e-5 else None
                        if key: bins[key].append((p1, p2, float(a[ii]), float(g)))
    out["S2_min_cross_gap"] = (float(gmin[0]), gmin[1]); out["S2_bins"] = {k: len(v) for k, v in bins.items()}
    out["S2_hits"] = bins["<1e-8"] + bins["[1e-8,1e-7)"] + bins["[1e-7,1e-6)"]
    cls, outside_gap = [], np.inf
    for p in ps:
        s = L[p]; cur = s[:1]; groups = []
        for v in s[1:]:
            if v - cur[-1] < 1e-4: cur.append(v)
            else: groups.append(cur); cur = [v]
        if cur: groups.append(cur)
        for g in groups:
            if len(g) > 1: cls.append((p, len(g), float(g[-1] - g[0]), float(np.mean(g))))
        reps = [g[0] for g in groups]
        if len(reps) > 1: outside_gap = min(outside_gap, float(np.min(np.diff(reps))))
    out["S3_classes"] = cls; out["S3_min_gap_outside_classes"] = outside_gap
    out["fire"] = bool(out["S1_hits"] or out["S2_hits"]); return out

R = scan(L)
# S4: two-tag entries = poles of same-object pairs (k, p) with q = (k - p) % Ny mirror-equal to p; class members' entries vs the rest
cm = {(p, v) for (p, n, sp, c) in R["S3_classes"] for v in L[p] if abs(v - c) <= sp}
obj = lambda x: min(x % Ny, (Ny - x) % Ny)
n_in = n_out = 0
for k in range(Ny):
    for p in range(Ny):
        q = (k - p) % Ny
        if obj(p) != obj(q): continue
        for v in L[obj(p)]:
            if (obj(p), v) in cm: n_in += 2
            else: n_out += 2
R["S4_two_tag_in"] = n_in; R["S4_two_tag_out"] = n_out
# plant (must fire both S1 and S2)
Lp = {p: list(v) for p, v in L.items()}; pa, pb = uniq[1], uniq[2]
Lp[pa] = sorted(Lp[pa] + [5e-6]); Lp[pb] = sorted(Lp[pb] + [Lp[pa][-1] + 5e-8])
RP = scan(Lp)
plant_ok = bool(RP["S1_hits"]) and any(abs(h[3] - 5e-8) < 1e-9 for h in RP["S2_hits"])
print(f"W{W}P{P} (CUSPIS_081E={os.environ.get('CUSPIS_081E', 'unset')}): {sum(len(v) for v in L.values())} poles <= s_cut in {len(uniq)} slice objects")
print(f"  S1 min s = {R['S1_min_s']:.3e}; poles <= 1e-5: {R['S1_hits'] or 'none'}; < 3e-5: {R['S1_near_3e-5'] or 'none'}")
print(f"  S2 min cross-slice gap = {R['S2_min_cross_gap'][0]:.3e} at {R['S2_min_cross_gap'][1]}; bins {R['S2_bins']}")
for h in R["S2_hits"]: print(f"     S2 hit: slices {h[0]},{h[1]} s {h[2]:.6f} gap {h[3]:.2e}")
print(f"  S3 classes (gap < 1e-4): {[(p, n, f'{sp:.1e}', f'{c:.4f}') for p, n, sp, c in R['S3_classes']]}")
print(f"  S3 min same-slice gap outside classes = {R['S3_min_gap_outside_classes']:.3e}")
print(f"  S4 two-tag entries: inside classes {n_in}, outside {n_out} (ratio {n_out / max(n_in, 1):.1f})")
print(f"  plant (s = 5e-6 and a cross copy at +5e-8 must both fire): {'PASS' if plant_ok else 'FAIL'}")
print(f"SCAN W{W}P{P}: {'FIRES -> report to the Bridge before W12P12' if R['fire'] else 'CLEAR'}")
json.dump(dict(W=W, P=P, flag=os.environ.get("CUSPIS_081E"), scan=R, plant=dict(ok=plant_ok, S1=RP["S1_hits"], S2=RP["S2_hits"][:5])),
          open(os.path.join(HERE, "exp081d_results", "exp096", f"scan_W{W}P{P}.json"), "w"), indent=1, default=str)
sys.exit(0 if plant_ok else 2)
