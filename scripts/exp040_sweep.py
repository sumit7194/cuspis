"""EXP-040 Part A: prior-art sweep for a cross-dimension comparison of the strip coefficient kappa_d/C_T (protocol in
report.md EXP-040 Part A). Method of EXP-027/032: INSPIRE citer queries by recid with a count sanity bound; arXiv API
keyword queries each preceded by a positive control that must hit."""
import json, re, time, urllib.request, urllib.parse
def insp(q, size=250, fields="titles,arxiv_eprints,control_number,citation_count,earliest_date,abstracts", sort=None):
    p = {"q": q, "size": size, "fields": fields}
    if sort: p["sort"] = sort
    return json.load(urllib.request.urlopen("https://inspirehep.net/api/literature?" + urllib.parse.urlencode(p), timeout=120))
def arx(q, n=200):
    u = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": n})
    x = urllib.request.urlopen(u, timeout=120).read().decode()
    tot = int(re.search(r"<opensearch:totalResults[^>]*>(\d+)<", x).group(1))
    return tot, [(i, re.sub(r"\s+", " ", t)) for i, t in re.findall(r"<entry>.*?<id>http://arxiv.org/abs/([^<]+)</id>.*?<title>(.*?)</title>", x, re.S)]
SEEDS = [("0905.2562", "Casini-Huerta free-QFT EE review"), ("hep-th/0605073", "Ryu-Takayanagi aspects of HEE"),
         ("1202.2070", "Liu-Mezei refinement of EE"), ("1409.1937", "Giombi-Klebanov interpolating a and F"),
         ("2608.23692", "Abate-Martinek all-d Dirac RMI")]
PAT = re.compile(r"(strip|slab|thin|dimension)", re.I); PAT2 = re.compile(r"entangl", re.I)
hits = {}
for arxid, lab in SEEDS:
    r = insp(f"arxiv:{arxid}")["hits"]["hits"]
    if not r: print(f"SEED {arxid} [{lab}]: NOT FOUND"); continue
    m = r[0]["metadata"]; print(f"SEED {arxid} [{lab}] -> title on record: {m['titles'][0]['title']!r}; recid {m['control_number']}; cc {m.get('citation_count')}")
    c = insp(f"refersto:recid:{m['control_number']}", sort="mostrecent")["hits"]
    n = len(c["hits"]); full = c["total"] <= 250
    san = ("OK" if n == c["total"] == m.get("citation_count") else f"MISMATCH(returned {n}, total {c['total']}, cc {m.get('citation_count')})") if full else f"TRUNCATED to 250 of {c['total']} (most recent)"
    k = 0
    for h in c["hits"]:
        md = h["metadata"]; t = md["titles"][0]["title"]; ab = (md.get("abstracts") or [{}])[0].get("value", "")
        if PAT.search(t + " " + ab) and PAT2.search(t + " " + ab) and re.search(r"(strip|slab)", t + " " + ab, re.I) and re.search(r"dimension", t + " " + ab, re.I):
            i = (md.get("arxiv_eprints") or [{}])[0].get("value", "-"); k += 1
            hits.setdefault(i, [md.get("earliest_date", ""), t, set()])[2].add(arxid)
    print(f"   citers: {n} returned, total {c['total']} [sanity {san}]; filter (strip|slab)&dimension&entangl: {k}")
    time.sleep(2)
print(f"\nUNION of filtered citers: {len(hits)}")
for i, (d, t, s) in sorted(hits.items(), key=lambda kv: (-len(kv[1][2]), kv[1][0])):
    print(f"  {d[:10]}  {i:16s} cites {sorted(s)}  {t[:120]}")
QUERIES = [("strip/dim/free/holo", "abs:strip AND abs:entanglement AND abs:dimensions AND abs:free AND abs:holographic", None),
           ("c-function + dim red", 'abs:"c-function" AND abs:"dimensional reduction" AND abs:entanglement', "0905.2562"),
           ("continuous dimension EE", 'abs:"continuous dimension" AND abs:entanglement', None),
           ("strip + stress tensor + dimension", 'abs:strip AND abs:entanglement AND abs:"stress tensor" AND abs:dimension', None),
           ("strip coefficient free fields", 'abs:strip AND abs:entanglement AND abs:"free fields" AND abs:dimensions', None),
           ("arbitrary dimensions strip", 'abs:"arbitrary dimensions" AND abs:entanglement AND abs:strip', None)]
print()
for lab, q, ctrl in QUERIES:
    tot, ents = arx(q)
    ctl = "" if not ctrl else f"; control {ctrl} {'HIT' if any(i.startswith(ctrl) for i, _ in ents) else 'MISSED'}"
    print(f"arXiv [{lab}] {q}: total {tot}{ctl}")
    for i, t in ents: print(f"    {i:16s} {t[:120]}")
    time.sleep(3)
