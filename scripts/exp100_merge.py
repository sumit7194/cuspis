"""EXP-100 part B: merge node-split route checkpoints into one checkpoint that the unsplit route then completes (checks stage).
Why separate files: exp100_route.put() rewrites the WHOLE in-memory dict on every write, so two processes on one checkpoint file
silently drop each other's nodes. Each part therefore runs with its own --tag-suffix, and this script merges them.
Usage: exp100_merge.py OUT PART0 PART1 ... (PART0 = the part with i == 0, the only one allowed to carry t0 / tsad)
       exp100_merge.py --selftest      (negative controls; each planted defect must be REFUSED)
Refuses (rc 2) on: OUT exists; a part missing; a g| node in two parts; the union not exactly the 48 C-nodes; t0/tsad missing from
PART0 or present in another part; install ranks differing between parts; any check-stage key (planted/b2b/n1c/woodbury/summary/S_all)
in a part. Values are copied, never recomputed. [model: Opus 5.5]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
CHECK_KEYS = ("planted", "b2b", "n1c", "woodbury", "summary", "S_all")
def nodes48():
    import exp081d_analyze as A81; return [f"{s:.15f}" for s, _ in A81.nodes48()]
def merge(parts, N48):
    """parts: list of dicts, parts[0] the i == 0 part. Returns the merged dict or raises ValueError."""
    out = {}; seen = {}
    for i, p in enumerate(parts):
        bad = [k for k in CHECK_KEYS if k in p]
        if bad: raise ValueError(f"part {i} carries check-stage keys {bad}")
        if i > 0 and ("t0" in p or "tsad" in p): raise ValueError(f"part {i} carries t0/tsad (only part 0 may)")
        if p.get("ranks") != parts[0].get("ranks"): raise ValueError(f"part {i} install ranks differ from part 0")
        for k, v in p.items():
            if k.startswith("g|"):
                if k in seen: raise ValueError(f"node {k} in parts {seen[k]} and {i}")
                seen[k] = i; out[k] = v; s = k[2:]
                if f"stats|{s}" not in p: raise ValueError(f"part {i}: node {k} without its stats")
                out[f"stats|{s}"] = p[f"stats|{s}"]
    for k in ("t0", "tsad", "stats|t0", "stats|tsad", "stats|install", "ranks"):
        if k not in parts[0]: raise ValueError(f"part 0 lacks {k}")
        out[k] = parts[0][k]
    got = sorted(k[2:] for k in out if k.startswith("g|"))
    if got != sorted(N48): raise ValueError(f"node union is not the 48 C-nodes ({len(got)} present)")
    return out
def selftest():
    N = [f"{0.1 * i:.15f}" for i in range(48)]
    def part(idx, first):
        p = {"ranks": {"max": 1}, "stats|install": {"calls": 1}}
        for i in idx: p[f"g|{N[i]}"] = float(i); p[f"stats|{N[i]}"] = {"unconverged": 0}
        if first: p.update(t0=1.0, tsad=2.0, **{"stats|t0": {}, "stats|tsad": {}})
        return p
    good = [part(range(0, 6), True), part(range(6, 20), False), part(range(20, 34), False), part(range(34, 48), False)]
    m = merge(good, N); ok = [len([k for k in m if k.startswith("g|")]) == 48 and m["t0"] == 1.0]
    print(f"selftest good split: merged 48 nodes + t0 -> {'PASS' if ok[0] else 'FAIL'}")
    cases = {"overlap": lambda g: g[1].update({f"g|{N[0]}": 9.0, f"stats|{N[0]}": {}}),
             "missing node": lambda g: (g[3].pop(f"g|{N[47]}"), g[3].pop(f"stats|{N[47]}")),
             "t0 in part 2": lambda g: g[2].update(t0=1.0),
             "ranks differ": lambda g: g[1].update(ranks={"max": 2}),
             "check key in part": lambda g: g[0].update(n1c={}),
             "part 0 without tsad": lambda g: g[0].pop("tsad")}
    for nm, f in cases.items():
        g = [json.loads(json.dumps(p)) for p in good]; f(g)
        try: merge(g, N); r = False
        except ValueError as e: r = True; why = str(e)
        print(f"selftest planted '{nm}': {'REFUSED -> PASS' if r else 'ACCEPTED -> FAIL'}" + (f" ({why})" if r else "")); ok.append(r)
    return all(ok)
if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]: sys.exit(0 if selftest() else 1)
    out, parts = sys.argv[1], sys.argv[2:]
    if os.path.exists(out): print(f"REFUSE: {out} exists"); sys.exit(2)
    miss = [p for p in parts if not os.path.exists(p)]
    if miss: print(f"REFUSE: missing parts {miss}"); sys.exit(2)
    try: m = merge([json.load(open(p)) for p in parts], nodes48())
    except ValueError as e: print(f"REFUSE: {e}"); sys.exit(2)
    tmp = out + ".tmp"; json.dump(m, open(tmp, "w")); os.replace(tmp, out)
    print(f"merged {len(parts)} parts -> {os.path.relpath(out, HERE)}: 48 nodes + t0 + tsad")
