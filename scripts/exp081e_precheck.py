"""EXP-081e pre-checks (registration 6686454, sections E and F.1-F.2). Each plant's observed outcome is compared with the paper-checked
expected outcome in registration column E; any disagreement -> exit 1. Plants act on the INPUTS of the production selection function
(sigma3d.select_081e / wind_check), so they exercise the production path. [model: Opus 5.5]"""
import sys, json, copy, numpy as np, scipy.linalg as sla
import sigma3d as S3
from exp081b_census import geom, census
from tools.winding import winding
FAIL = []; OUT = {}
def check(name, ok, detail):
    print(f"{name:58s} {'PASS' if ok else 'FAIL'}   {detail}", flush=True); OUT[name] = dict(ok=bool(ok), detail=str(detail))
    if not ok: FAIL.append(name)
def qep_ev(sl):
    W = sl.W; n2 = 2 * W; C1 = np.zeros((n2, n2)); C0 = np.zeros((n2, n2)); Cm = np.zeros((n2, n2))
    for j in range(W):
        C1[2*j+1, 2*j] = -1; C0[2*j+1, 2*j] = 1; Cm[2*j, 2*j+1] = -1; C0[2*j, 2*j+1] = 1
    A2, A1, A0 = sl.M @ C1, np.eye(n2) + sl.M @ C0, sl.M @ Cm; Z = np.zeros((n2, n2)); I = np.eye(n2)
    ev = sla.eig(np.block([[Z, I], [-A0, -A1]]), np.block([[I, Z], [Z, A2]]), right=False); return ev[np.isfinite(ev)]
def sel(ev, sl):
    try: m, mu = S3.select_081e(ev, S3.pencil_roots(sl.W, sl.M)); return [S3._s(z) for z in m], mu, None
    except S3.PoleGateError as e: return None, None, str(e)
sin = lambda L: [x for x in L if x <= 3.0]

# ---------------- plants on W10P10b10 p = 8 (S3 flag OFF for building; selection called directly) ----------------
S3.POLE_ADMIT_081E = False
G10 = geom(10, 10, Wbox=10); sl = G10.sl[8]; ev = qep_ev(sl); base, bmu, err = sel(ev, sl)
check("base W10 p=8: selection == production list (bitwise)", err is None and base == list(sl.s), f"{np.round(sin(base),7) if base else err}")
zp = np.exp(-2 * np.pi * 2.0)
r, _, e = sel(np.append(ev, [zp, (1 + 1e-3) / zp]), sl); check("P1 MUST-REJECT pencil-unconfirmed (s=2.0, partner 1e-3)", e is None and r == base, e or "rejected; list unchanged")
r, _, e = sel(np.append(ev, [zp, 1 / zp]), sl); check("P1b MUST-STOP spurious passing the filter", e is not None and e.startswith("PB"), e or f"no stop; list {np.round(sin(r),7)}")
sg = min(base, key=lambda x: abs(x - 2.858532)); zg = np.exp(-2 * np.pi * (sg + 1e-8))
r, _, e = sel(np.append(ev, [zg, (1 + 1e-3) / zg]), sl)
# AMENDMENT 1 (after run 1): the rider borrows the kept genuine pole's reciprocal partner (relative mismatch ~6.3e-8 + 1.5e-7 < 1e-6), is KEPT
# by the filter, and must then STOP at PB (one-to-one leaves it without a pencil partner). Registered expectation "rejected" was wrong in mechanism.
check("P2a rider 1e-8 from KEPT genuine -> PB STOP (amended)", e is not None and e.startswith("PB"), e or f"no stop; list {np.round(sin(r),7)}")
i = int(np.argmin(np.abs(ev - np.exp(-2 * np.pi * 2.858532))))
r, _, e = sel(np.delete(ev, i), sl); check("P3 MUST-STOP deleted genuine (2.858532)", e is not None and e.startswith("PB"), e or f"no stop; list {np.round(sin(r),7)}")
# P6 census must-fire: production list + resolved spurious entry at s = 2.0 (F unchanged)
G6 = copy.copy(G10); G6.sl = list(G10.sl); s6 = copy.copy(G10.sl[8]); s6.s = sorted(list(G10.sl[8].s) + [2.0]); G6.sl[8] = s6
c = {x["p"]: x for x in census(G6, 3.0)}[8]; check("P6 CEN' must-fire (extra entry s=2.0)", (not c["match"]) and not c["touch"], f"match {c['match']} touch {c['touch']}")

# ---------------- F.1 / F.2 invariance + P4 / P5 / P5b / P7 (patched build vs unpatched build) at all 9 geometries ----------------
GEOS = [(3,6,6),(6,6,6),(2,8,8),(4,8,8),(8,8,8),(5,10,10),(10,10,10),(6,12,12),(12,12,12)]
for W, P, B in GEOS:
    S3.POLE_ADMIT_081E = False; Go = geom(W, P, Wbox=B)
    S3.POLE_ADMIT_081E = True
    try: Gn = geom(W, P, Wbox=B); gerr = None
    except S3.PoleGateError as e: Gn = None; gerr = str(e)
    S3.POLE_ADMIT_081E = False
    tag = f"W{W}P{P}b{B}"
    if Gn is None: check(f"F.1 {tag}: patched build (PB/WIND on every real slice)", False, f"GATE FIRED on real data: {gerr}"); continue
    diff = [p for p in range(len(Go.sl)) if list(Go.sl[p].s) != list(Gn.sl[p].s)]
    if (W, P) != (12, 12):
        resid_same = all(all(np.array_equal(a, b) for a, b in zip(Go.sl[p].Rp, Gn.sl[p].Rp)) for p in range(len(Go.sl)))
        check(f"F.1 {tag}: lists bitwise identical, residues identical", not diff and resid_same, f"differing slices {diff}; residues identical {resid_same}")
    else:
        added = {p: sorted(set(np.round(Gn.sl[p].s, 12)) - set(np.round(Go.sl[p].s, 12))) for p in diff}
        exp4 = {7: [2.4778963, 2.4794482], 10: [2.9124682, 2.9126315]}
        Ny = len(Go.sl); mir = {7: 7, 10: 10, Ny - 7: 7, Ny - 10: 10}       # AMENDMENT 1: mirror slices Ny-p are copies of p
        exp4 = {q: exp4[mir[q]] for q in mir}
        ok = sorted(diff) == sorted(mir) and all(np.allclose(added[p], exp4[p], atol=1e-7) for p in diff) and \
             all(set(np.round(Go.sl[p].s, 12)) <= set(np.round(Gn.sl[p].s, 12)) for p in diff)
        # P2b (AMENDMENT 1): admission-path rider next to a REJECTED genuine pole (W12 p = 7, s 2.4778963): both rejected by the filter,
        # they compete for one pencil root; one-to-one admits the nearer (genuine) and not the rider; list == patched production list.
        sl7 = Go.sl[7]; ev7 = qep_ev(sl7); g7 = np.exp(-2 * np.pi * (2.4778963 + 1e-8))
        r7, _, e7 = sel(np.append(ev7, [g7, (1 + 1e-3) / g7]), sl7)
        pr7 = [S3._s(z) for z in S3.pencil_roots(sl7.W, sl7.M)]; root = min(pr7, key=lambda x: abs(x - 2.4778963))
        gen = min((S3._s(z.real) for z in ev7 if abs(z.imag) < 1e-8 * abs(z) and 0 < z.real < 1), key=lambda x: abs(x - 2.4778963))
        print(f"   P2b margin (Bridge): pencil root {root:.12f}; |genuine - root| {abs(gen - root):.2e}; |rider - root| {abs(S3._s(g7) - root):.2e}; ratio {abs(S3._s(g7) - root) / abs(gen - root):.1f}x", flush=True)
        check("P2b rider 1e-8 from REJECTED genuine -> not admitted (amended)", e7 is None and r7 == list(Gn.sl[7].s), e7 or f"list {np.round(sin(r7),7).tolist()}")
        # P7m (amendment 1b, Bridge ruling after it fired at 1e-12: the tolerance ignored conditioning): identical counts AND max |ds| <= 1e-9
        mir_ok, mlog = True, []
        for q in [q for q in mir if q != mir[q]]:
            a, b = sorted(Gn.sl[q].s), sorted(Gn.sl[mir[q]].s)
            if len(a) != len(b): mir_ok = False; mlog.append(f"{q}/{mir[q]} counts {len(a)} {len(b)}"); continue
            for x, y in zip(a, b):
                if x <= 3.0: mlog.append(f"{q}/{mir[q]} z {np.exp(-2*np.pi*x):.1e} |ds| {abs(x-y):.1e}"); mir_ok &= abs(x - y) <= 1e-9
        print("   P7m per-pole: " + "; ".join(mlog), flush=True)
        check("P7m mirror slices: same counts, max |ds| <= 1e-9 (amendment 1b)", mir_ok, "")
        check("P7 / F.1 W12P12b12: lists differ by exactly the 4 poles (P4 admission)", ok, f"added {{{', '.join(f'{p}: {np.round(v,7).tolist()}' for p, v in added.items())}}}")
        # P5 WIND must-fire: p = 14 entries (split 5.6e-8), production rad 1.7e-8 -> 1 each; wrong radius 1e-7 -> 2
        sl14 = Gn.sl[14]; s14 = sin(sl14.s); rads = [min(1e-6, 0.3 * min([abs(a - b) for b in sl14.s if b != a] + [1.0])) for a in sl14.s][:len(s14)]
        try: S3.wind_check(sl14.W, sl14.M, s14, rads, [1] * len(s14)); okp = True
        except S3.PoleGateError: okp = False
        try: S3.wind_check(sl14.W, sl14.M, s14, rads, [1] * len(s14), rad_override=1e-7); fired = False; msg = "did not fire"
        except S3.PoleGateError as e: fired = True; msg = str(e)
        check("P5 WIND radius must-fire (p=14, rad 1e-7 encloses both)", okp and fired, f"production radii pass: {okp}; wrong radius: {msg}")
        # P5b alpha-plane equivalence on production's own contour (alpha = i s, s = -i alpha), every in-cut entry of p = 7, 14, 17
        bad = []
        for p in (7, 14, 17):
            sp = Gn.sl[p]; ss = list(sp.s); rr = [min(1e-6, 0.3 * min([abs(a - b) for b in ss if b != a] + [1.0])) for a in ss]
            def F(sv, W=sp.W, M=sp.M):
                z = np.exp(-2 * np.pi * sv); CD = np.zeros((2 * W, 2 * W), dtype=complex); D = np.ones(2 * W, dtype=complex)
                for j in range(W): CD[2 * j + 1, 2 * j] = -(z - 1); CD[2 * j, 2 * j + 1] = -(1 - z); D[2 * j + 1] = z
                return np.linalg.det(np.diag(D) + M @ CD)
            for a, r in zip(ss, rr):
                if a > 3.0: continue
                n_s = winding(F, a, r)[0]; n_a = winding(lambda al: F(-1j * al), 1j * a, r)[0]
                if n_s != n_a: bad.append((p, a, n_s, n_a))
        check("P5b alpha-plane contour == s-plane circle (counts)", not bad, f"mismatches {bad}")
    if (W, P) == (12, 12): ok2 = any(abs(x - 2.776745) < 1e-5 for x in Gn.sl[9].s) and any(abs(x - 2.777076) < 1e-5 for x in Gn.sl[9].s)
    elif (W, P) == (10, 10): ok2 = any(abs(x - 2.858532) < 1e-5 for x in Gn.sl[8].s) and any(abs(x - 2.860212) < 1e-5 for x in Gn.sl[8].s)
    else: ok2 = None
    if ok2 is not None: check(f"F.2 {tag}: threshold-adjacent pair present and unchanged", ok2 and (W, P) != (10, 10) or (ok2 and not diff), "")
    del Go, Gn
json.dump(OUT, open("exp081d_results/exp081e_precheck.json", "w"), indent=1)
print(f"\nPRECHECK {'PASS' if not FAIL else 'FAIL: ' + ', '.join(FAIL)}"); sys.exit(1 if FAIL else 0)
