"""Plant guard (Bridge ruling 2026-11-22, after the EXP-083 R3' W2P4 scut_low plant that could not fire; a repeat of slip 12's rule
"pre-check on the real data that the variant triggers the mechanism"). Mechanism, not promise:

  check_plant(S, var, value=None, s_cut=3.0) -> dict   raises PlantInert if the planted variant does NOT change its input at
                                                       this geometry (S = a production sigma3d.Strip3D, unmodified).
  derive_scut_plant(S, s_cut=3.0) -> float             an s_cut that drops >= 1 kept pole of THIS geometry (midway between the
                                                       largest kept distinct pole and the next one below it), instead of one
                                                       value per P.

What "changes its input" means per variant (each is a count on the geometry's own pole data, no physics run):
  scut_low   : #kept (slice, pole) with s <= value  <  #kept with s <= s_cut         (drops >= 1 kept pole)
  merge_tiny : #confluent contours at tol 1e-15*rad <  #confluent at 1e-2*rad        (splits >= 1 merged pair)
  dd1        : #confluent contours at 1e-2*rad >= 1                                  (there is a confluent residue to drop)
  drop_pole, res_scale : slices 1 and Ny-1 each have >= 1 kept pole                  (there is a pole to drop / rescale)
The confluent count replicates sigma3d.Strip3D.inner_beta0's merge loop (rad 1e-5). [model: Opus 5.5]"""
import numpy as np


class PlantInert(RuntimeError):
    pass


def kept(S, s_cut):
    return sum(1 for sl in S.sl for s in sl.s if s <= s_cut)


def n_confluent(S, s_cut, tol_factor, rad=1e-5):
    tot = 0
    for k in range(S.Ny):
        for p in range(S.Ny):
            q = (k - p) % S.Ny; sa, sb = S.sl[p], S.sl[q]
            locs = [(a0, "a") for sj in sa.s if sj <= s_cut for a0 in (1j * sj, -1j * sj)] + \
                   [(a0, "b") for sj in sb.s if sj <= s_cut for a0 in (-1j * sj, 1j * sj)]
            merged = []
            for a0, tag in locs:
                hit = [m for m in merged if abs(m[0] - a0) < tol_factor * rad]
                if hit: hit[0][1].add(tag)
                else: merged.append([a0, {tag}])
            tot += sum(1 for _, tags in merged if len(tags) == 2)
    return tot


def derive_scut_plant(S, s_cut=3.0):
    ss = sorted(set(round(float(s), 9) for sl in S.sl for s in sl.s if s <= s_cut))
    if len(ss) < 2: raise PlantInert(f"derive_scut_plant: fewer than 2 distinct kept poles ({ss}); no s_cut plant possible")
    return 0.5 * (ss[-1] + ss[-2])


def check_plant(S, var, value=None, s_cut=3.0):
    geo = f"Lx{S.Lx} Lt{S.Lt} Ny{S.Ny} W{len(S.cutx)}"
    if var == "scut_low":
        a, b = kept(S, s_cut), kept(S, value)
        if not b < a: raise PlantInert(f"scut_low {value} drops no kept pole at {geo} (kept {a} at s_cut {s_cut}, {b} at {value}; max kept s = {max(s for sl in S.sl for s in sl.s if s <= s_cut):.4f})")
        return dict(var=var, kept=a, kept_plant=b, dropped=a - b)
    if var in ("merge_tiny", "dd1"):
        c_prod = n_confluent(S, s_cut, 1e-2)
        if var == "dd1":
            if c_prod < 1: raise PlantInert(f"dd1: no confluent contour at {geo}")
            return dict(var=var, confluent=c_prod)
        c_tiny = n_confluent(S, s_cut, 1e-15)
        if not c_tiny < c_prod: raise PlantInert(f"merge_tiny splits no merged pair at {geo} (confluent {c_prod} -> {c_tiny})")
        return dict(var=var, confluent=c_prod, confluent_plant=c_tiny)
    if var in ("drop_pole", "res_scale"):
        for p in (1, S.Ny - 1):
            if not any(s <= s_cut for s in S.sl[p].s): raise PlantInert(f"{var}: slice {p} has no kept pole at {geo}")
        return dict(var=var, ok=True)
    return dict(var=var, unchecked=True)


def check_scale_plant(eps, N, Ny, s1, thr=1e-7, factor=10.0, g_abs=None, g_rel_prec=1e-12):
    """EXP-081d planted must-fire (G and residues x (1 + eps) at node s1): predicted dg = 2 eps N Ny must give an impact >= factor x thr
    AND exceed 1e3 x the g precision (g_rel_prec |g|) when |g| is known. Raises PlantInert otherwise."""
    pred = 2 * eps * N * Ny; imp = pred * np.pi / np.cosh(np.pi * s1) ** 2
    if imp < factor * thr * (1 - 1e-9): raise PlantInert(f"scale plant: predicted impact {imp:.2e} < {factor} x {thr:.0e}")
    if g_abs is not None and pred < 1e3 * g_rel_prec * g_abs: raise PlantInert(f"scale plant: predicted dg {pred:.2e} not >> g precision {g_rel_prec * g_abs:.1e}")
    return dict(eps=eps, pred=pred, impact=imp)
