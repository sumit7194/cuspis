"""Tolerance-reference guard (Bridge ruling 2026-11-22, slip 15 = a repeat of slip 13: C2's tolerance 3*dev_a took dev_a from
production's construction path while arm (b) ran on a mirror-aliased path whose sigma = 0 baseline was 2.2x larger).
Mechanism, not promise: any tolerance of the form max(k * dev_ref, floor) goes through ref_tol(), which
  1. measures the structural agreement of the reference path S_ref and the comparison's own path S_own at sigma = 0
     (max over slices of |sorted poles difference| and of the relative residue difference), against a stated bound;
  2. if they agree within `bound`: tol = max(k * dev_ref, floor);
  3. if not: computes dev_own = own_dev() on the comparison's own path, uses the LARGER of dev_ref and dev_own, and logs it
     (never silent). The returned info dict records which branch ran. [model: Opus 5.5]"""
import numpy as np


def path_disagreement(S_ref, S_own):
    ds, dr = 0.0, 0.0
    for a, b in zip(S_ref.sl, S_own.sl):
        if len(a.s) != len(b.s): return np.inf, np.inf
        ia, ib = np.argsort(a.s), np.argsort(b.s)
        if len(ia): ds = max(ds, float(np.max(np.abs(np.asarray(a.s)[ia] - np.asarray(b.s)[ib]))))
        for i, j in zip(ia, ib):
            for Ra, Rb in ((a.Rp[i], b.Rp[j]), (a.Rm[i], b.Rm[j])):
                if Ra is None or Rb is None: continue
                dr = max(dr, float(np.abs(Ra - Rb).max() / max(np.abs(Ra).max(), 1e-300)))
    return ds, dr


def ref_tol(k, dev_ref, floor, S_ref, S_own, own_dev, bound=1e-12, log=print):
    ds, dr = path_disagreement(S_ref, S_own)
    if max(ds, dr) <= bound:
        return max(k * dev_ref, floor), dict(branch="paths agree", ds=ds, dr=dr, dev_ref=dev_ref)
    dev_own = own_dev(); use = max(dev_ref, dev_own)
    log(f"tol_ref: construction paths DIFFER at sigma = 0 (|ds| {ds:.1e}, residue rel {dr:.1e} > bound {bound:.0e}); "
        f"dev_ref {dev_ref:.2e}, dev on own path {dev_own:.2e} -> using {use:.2e}")
    return max(k * use, floor), dict(branch="paths differ: larger used", ds=ds, dr=dr, dev_ref=dev_ref, dev_own=dev_own)
