"""EXP-084c (registered 2295d7d): route (ii) Q_cont^sad(n) (EXP-083 C2 construction) vs honest Q_n at the 084 geometries.
Level 1 (exactness): |dev| <= max(3 dev_a, 1e-10), dev_a on route (ii)'s OWN path (strip_sigma at sigma = 0, alias False) vs honest arm a.
Level 2 (relevance): max |Delta R_n(k)| <= 0.01, through the 084 normalisation with stored kappa.
Usage: exp084c_run.py KA                 -> known answer (stored C2 W2P2 n=2) + planted normalisation only
       exp084c_run.py W P N [N ...]      -> one geometry (Wbox = P), the listed n (checkpointed per (W, P, n))
       exp084c_run.py READ               -> Level 1 / Level 2 reading + sized plants (needs all 8 geometries x n = 2, 3, 4)
[model: Opus 5.5]"""
import sys, os, json, time, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "exp081d_results", "exp084c"); os.makedirs(OUT, exist_ok=True)
O84, O84b = os.path.join(HERE, "exp081d_results", "exp084"), os.path.join(HERE, "exp081d_results", "exp084b")
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); KS = [1, 1.5, 2, 2.5]; NS = [2, 3, 4]
KW = dict(Mx=48, Mt=160, tmax=8.0); T0 = time.time(); FAIL = []
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)
def check(nm, ok, det=""):
    log(f"{nm:56s} {'PASS' if ok else 'FAIL'}  {det}")
    if not ok: FAIL.append(nm)
def norm(k):                          # the 084 normalisation, stored kappa
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]
def dR(n, k, d1, d2): return -(0.5 / (n - 1)) * (d1 - d2) * norm(k)      # Delta Q at (W1, W2) -> Delta R_n(k)
def honest(n, W, P, arm="b"):
    if n in (2, 3):
        d = json.load(open(os.path.join(O84, f"Q_W{W}P{P}b{P}.json")))[str(n)]; return d["QA"] if arm == "b" else d["armA"]
    f = os.path.join(O84b, f"Q{n}_W{W}P{P}b{P}.json")
    if arm == "b": return json.load(open(f))["QA"]
    fa = os.path.join(OUT, f"honestA{n}_W{W}P{P}.json")
    if not os.path.exists(fa):
        import exp083_honest as H
        g = H.Geom(W, P, Wbox=P, c=2); q = g.Q(n, saddle=False); json.dump(dict(Qa=q), open(fa, "w"))
    return json.load(open(fa))["Qa"]
mode = sys.argv[1]
if mode == "KA":
    import exp083_honest as H, exp083_armb as AB, exp083_r3_qcont as QC
    ref = json.load(open(os.path.join(HERE, "exp083_armb", "c2_W2P2.json")))["2"]
    g = H.Geom(2, 2); gap = AB.Gap(g, s_cut=3.0, target="direct"); G1 = g.Gn(1); J0 = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
    ld0 = QC.QCont(AB.strip_sigma(g, None), npt=120, npt0=512).ld1; s2, info = gap.solve(2.0, J=J0)
    Qc = QC.QCont(AB.strip_sigma(g, s2), npt=120, npt0=512); q = (Qc.Q(2.0, **KW) + 2.0 * (Qc.ld1 - ld0).sum()).real
    check("KA route (ii) W2P2 n=2 vs stored EXP-083 C2", abs(q - ref["qsad"]) <= 1e-12 * max(1, abs(ref["qsad"])), f"{q!r} vs {ref['qsad']!r}")
    k = 2; W1, W2, P = 4, 8, 8; exp = -0.5 * 1.0 / (4 * P * (1 / W1 - 1 / W2) * JD["2"]["kappa"])     # independent recomputation
    got = dR(2, k, 1.0, 0.0); check("planted normalisation dQ(W1)=1, k=2, n=2", abs(got - exp) <= 1e-12 * abs(exp), f"{got!r} vs {exp!r}")
    sys.exit(1 if FAIL else 0)
if mode == "KA_ALIAS":     # diagnosis of the fired KA: does the ALIASED path (pre-slip-15 default) reproduce the stored C2 value bitwise?
    import exp083_honest as H, exp083_armb as AB, exp083_r3_qcont as QC
    ref = json.load(open(os.path.join(HERE, "exp083_armb", "c2_W2P2.json")))["2"]
    g = H.Geom(2, 2); gap = AB.Gap(g, s_cut=3.0, target="direct", alias=True); G1 = g.Gn(1); J0 = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
    ld0 = QC.QCont(AB.strip_sigma(g, None, alias=True), npt=120, npt0=512).ld1; s2, info = gap.solve(2.0, J=J0)
    Qc = QC.QCont(AB.strip_sigma(g, s2, alias=True), npt=120, npt0=512); q = (Qc.Q(2.0, **KW) + 2.0 * (Qc.ld1 - ld0).sum()).real
    log(f"KA_ALIAS route (ii) W2P2 n=2 aliased path: {q!r} vs stored {ref['qsad']!r}: diff {abs(q - ref['qsad']):.2e} -> {'BITWISE' if q == ref['qsad'] else ('<=1e-12' if abs(q - ref['qsad']) <= 1e-12 else 'DIFFERENT')}")
    sys.exit(0)
if mode == "READ":
    rows, missing = [], []
    for k in KS:
        W1, W2, P = int(2 * k), int(4 * k), int(4 * k)
        for n in NS:
            f1, f2 = (os.path.join(OUT, f"c84_W{W}P{P}_n{n}.json") for W in (W1, W2))
            if not (os.path.exists(f1) and os.path.exists(f2)): missing.append((k, n)); continue
            a, b = json.load(open(f1)), json.load(open(f2))
            rows.append(dict(k=k, n=n, dR=dR(n, k, a["dev_signed"], b["dev_signed"]), L1=(a["dev"] <= a["tol"] and b["dev"] <= b["tol"]),
                             dR_sigma0=dR(n, k, a["plant_sigma0_signed"], b["plant_sigma0_signed"]), probe=[a.get("probe"), b.get("probe")], tol=[a["tol"], b["tol"]], dev=[a["dev"], b["dev"]]))
    if missing: log(f"missing (k, n): {missing}  -> reading INCONCLUSIVE for those (registered)")
    mx = max(abs(r["dR"]) for r in rows)
    for r in rows: log(f"k={r['k']} n={r['n']}: dR {r['dR']:+.3e}  L1 {'PASS' if r['L1'] else 'FAIL'} (dev {r['dev'][0]:.1e}/{r['dev'][1]:.1e} tol {r['tol'][0]:.1e}/{r['tol'][1]:.1e})  plant sigma0 dR {r['dR_sigma0']:+.2e}")
    check("plant sigma=0 must FAIL Level 2", all(abs(r["dR_sigma0"]) > 0.01 for r in rows), f"min |dR| {min(abs(r['dR_sigma0']) for r in rows):.2e}")
    pr = [p for r in rows for p in r["probe"] if p is not None]
    check("plant sigma_n(1+1e-6) fires Level 1 (probe dev > tol)", all(p["dev"] > p["tol"] for p in pr), f"{len(pr)} probes")
    big = [abs(r["dR"] - 0.05) for r in rows]; check("sized plant 0.05 must FAIL Level 2", all(b > 0.01 for b in big), f"min {min(big):.3e}")
    small = [abs(r["dR"] - 0.002) for r in rows]
    if mx <= 0.008: check("sized plant 0.002 must PASS Level 2 (valid: unplanted <= 0.008)", all(s <= 0.01 for s in small), f"max {max(small):.3e}")
    else: log(f"sized plant 0.002: NOT GRADED (unplanted max |dR| {mx:.3e} > 0.008, registered condition); outcome max {max(small):.3e}")
    lab = ("INCONCLUSIVE (missing geometries)" if missing else ("agree (P2 false at the relevant precision)" if mx <= 0.01 else "disagree (continuation implicated directly)"))
    l1 = "all PASS" if all(r["L1"] for r in rows) else f"{sum(not r['L1'] for r in rows)} FAIL (exactness residual, reported)"
    log(f"\nEXP-084c READING: {lab}   max|dR| {mx:.3e} (Level 2 threshold 0.01); Level 1: {l1}; controls {'PASS' if not FAIL else FAIL}")
    json.dump(dict(rows=rows, max_dR=mx, reading=lab, level1=l1, controls_failed=FAIL), open(os.path.join(OUT, "result.json"), "w"), indent=1, default=float)
    sys.exit(1 if FAIL else 0)
# ---- one geometry ----
import exp083_honest as H, exp083_armb as AB, exp083_r3_qcont as QC
W, P = int(sys.argv[1]), int(sys.argv[2]); nlist = [int(x) for x in sys.argv[3:]]
g = H.Geom(W, P, Wbox=P, c=2); gap = AB.Gap(g, s_cut=3.0, target="direct"); G1 = g.Gn(1); J = -sum(G1[p] * G1[p] for p in range(g.Ny)) / g.Ny
S_own = AB.strip_sigma(g, None); Q0 = QC.QCont(S_own, npt=120, npt0=512); ld0 = Q0.ld1; sig = None
def qsad(n, s):
    Qc = QC.QCont(AB.strip_sigma(g, s), npt=120, npt0=512); return (Qc.Q(n, **KW) + n * (Qc.ld1 - ld0).sum()).real
for n in sorted(nlist):
    f = os.path.join(OUT, f"c84_W{W}P{P}_n{n}.json")
    if os.path.exists(f): sig = np.array(json.load(open(f))["sigma"]); continue
    t = time.time(); s_n, info = gap.solve(float(n), sig0=sig, J=J); J = info["J"]
    q = qsad(float(n), s_n); hb = honest(n, W, P, "b"); ha = honest(n, W, P, "a")
    qa = Q0.Q(float(n), **KW).real; dev_a = abs(qa - ha); tol = max(3 * dev_a, 1e-10)
    rec = dict(W=W, P=P, n=n, qsad=q, honest=hb, dev_signed=q - hb, dev=abs(q - hb), qa_route=qa, honest_a=ha, dev_a=dev_a, tol=tol,
               plant_sigma0_signed=qa - hb, gapF=info["F"], sigma=list(s_n), sec=None)
    if n in (2, 3): qp = qsad(float(n), s_n * (1 + 1e-6)); rec["probe"] = dict(dev=abs(qp - hb), tol=tol)
    rec["sec"] = time.time() - t; json.dump(rec, open(f, "w"), indent=1)
    log(f"W{W}P{P} n={n}: |dev| {rec['dev']:.2e} (tol {tol:.1e}) {'PASS' if rec['dev'] <= tol else 'FAIL'} L1; gap |F| {info['F']:.1e}; {rec['sec']:.0f}s"); sig = s_n
