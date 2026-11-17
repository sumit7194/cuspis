"""EXP-032: upper-bound literature sweep (protocol in report.md, EXP-032).  Method of EXP-027: INSPIRE citer queries by
recid with a count sanity bound (returned == total == citation_count when total <= size) and a positive control where
one is known; arXiv API keyword queries each preceded by an un-dated control that must hit, then the same query
restricted to submissions since 2026-09-01."""
import json, re, time, urllib.request, urllib.parse
SINCE = "submittedDate:[202609010000 TO 202611172359]"
def insp(q, size=250, fields="titles,arxiv_eprints,control_number,citation_count,earliest_date", sort=None):
    p = {"q": q, "size": size, "fields": fields}
    if sort: p["sort"] = sort
    u = "https://inspirehep.net/api/literature?" + urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(u, timeout=90))
def arx(q, n=100):
    u = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": n,
                                                                       "sortBy": "submittedDate", "sortOrder": "descending"})
    x = urllib.request.urlopen(u, timeout=90).read().decode()
    tot = int(re.search(r"<opensearch:totalResults[^>]*>(\d+)<", x).group(1))
    return tot, [(i, re.sub(r"\s+", " ", t)) for i, t in re.findall(r"<entry>.*?<id>http://arxiv.org/abs/([^<]+)</id>.*?<title>(.*?)</title>", x, re.S)]

SEEDS = [("2609.04041", "2609.04302", "LMW26 rectangle/cusp bootstrap"), ("2609.04302", None, "LMW26b eye bounds"),
         ("2609.04035", None, "BCGKM26 cusped defects"), ("2608.28531", None, "Cha26 cusped impurities positivity"),
         ("2608.03704", None, "CGT26 impurities near the light cone"), ("2404.05815", None, "DKPW24 defect fusion/Casimir"),
         ("2307.05164", None, "BCLM23 conformal bounds from EE"), ("1511.04077", None, "BWK16 bounds on corner EE"),
         ("1505.04804", None, "BMW15 corner universality")]
recent = {}
for arxid, control, lab in SEEDS:
    m = insp(f"arxiv:{arxid}")["hits"]["hits"][0]["metadata"]
    c = insp(f"refersto:recid:{m['control_number']}", sort="mostrecent")["hits"]
    ids = [(h["metadata"].get("arxiv_eprints") or [{}])[0].get("value", "-") for h in c["hits"]]
    full = c["total"] <= 250
    san = ("OK" if len(ids) == c["total"] == m["citation_count"] else
           f"MISMATCH(returned {len(ids)}, total {c['total']}, cc {m['citation_count']})") if full else f"TRUNCATED to 250 of {c['total']} (sorted most recent)"
    ctl = "" if not control else f"; control {control} {'present' if control in ids else 'MISSING'}"
    print(f"citers of {arxid} [{lab}] recid {m['control_number']}: {len(ids)} returned, total {c['total']}  [sanity {san}{ctl}]")
    for h, i in zip(c["hits"], ids):
        d = h["metadata"].get("earliest_date", "")
        if d >= "2026-09":
            t = h["metadata"]["titles"][0]["title"]
            recent.setdefault(i, (d, t, set()))[2].add(arxid)
            print(f"    {d}  {i:12s} {t[:110]}")
    time.sleep(2)
print(f"\nUNION of citers dated >= 2026-09 across seeds: {len(recent)}")
for i, (d, t, s) in sorted(recent.items(), key=lambda kv: kv[1][0], reverse=True):
    print(f"  {d}  {i:12s} cites {len(s)} seed(s) {sorted(s)}  {t[:100]}")

QUERIES = [("corner bounds", "ti:corner AND ti:bounds AND abs:entanglement", "1511.04077"),
           ("corner EE + bound", "abs:corner AND abs:entanglement AND abs:bound", "1511.04077"),
           ("twist defect fusion", 'abs:"twist defect" AND abs:fusion', None),
           ("defect fusion Casimir", "abs:defect AND abs:fusion AND abs:Casimir", "2404.05815"),
           ("cusp bootstrap", "abs:cusp AND abs:bootstrap", "2609.04041"),
           ("strip EE bound CFT", "abs:strip AND abs:entanglement AND abs:bound AND abs:conformal", None),
           ("F0 bound EE", 'abs:"free energy" AND abs:entanglement AND abs:bound AND abs:three', "2307.05164"),
           ("Renyi twist defect n->1", 'abs:"twist defect" AND abs:Renyi AND abs:entanglement', None)]
print()
for lab, q, ctrl in QUERIES:
    if ctrl:
        tot, ents = arx(q, 300)
        print(f"arXiv control [{lab}] {q}: total {tot}; control {ctrl} {'HIT' if any(i.startswith(ctrl) for i, _ in ents) else 'MISSED'}")
        time.sleep(3)
    tot, ents = arx(f"({q}) AND {SINCE}")
    print(f"arXiv [{lab}] since 2026-09-01: total {tot}")
    for i, t in ents: print(f"    {i:14s} {t[:110]}")
    time.sleep(3)
