"""EXP-027: prior-art sweep for C2a' (Dirac cumulant route), reproducible.  INSPIRE citer queries use recid (not
refersto:arxiv:, which returned junk on the bridge's V6), each with a count sanity bound (returned == citation_count)
and a positive control; arXiv API keyword queries each carry a control that must hit."""
import json, re, time, urllib.request, urllib.parse
def insp(q, size=100, fields="titles,arxiv_eprints,control_number,citation_count"):
    u = "https://inspirehep.net/api/literature?" + urllib.parse.urlencode({"q": q, "size": size, "fields": fields})
    return json.load(urllib.request.urlopen(u, timeout=90))
def arx(q, n=50):
    u = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": n})
    x = urllib.request.urlopen(u, timeout=90).read().decode()
    tot = int(re.search(r"<opensearch:totalResults[^>]*>(\d+)<", x).group(1))
    return tot, [(i, re.sub(r"\s+", " ", t)) for i, t in re.findall(r"<entry>.*?<id>http://arxiv.org/abs/([^<]+)</id>.*?<title>(.*?)</title>", x, re.S)]
for arxid, control in (("2102.06223", "2211.05159"), ("2211.05159", "2408.08364")):
    m = insp(f"arxiv:{arxid}")["hits"]["hits"][0]["metadata"]
    c = insp(f"refersto:recid:{m['control_number']}")["hits"]
    ids = [(h["metadata"].get("arxiv_eprints") or [{}])[0].get("value", "-") for h in c["hits"]]
    print(f"citers of {arxid} (recid {m['control_number']}): returned {len(ids)}, total {c['total']}, citation_count {m['citation_count']}  "
          f"[sanity {'OK' if len(ids) == c['total'] == m['citation_count'] else 'MISMATCH'}; control {control} {'present' if control in ids else 'MISSING'}]")
    for h, i in zip(c["hits"], ids): print(f"    {i:12s} {h['metadata']['titles'][0]['title'][:100]}")
    time.sleep(2)
for lab, q, ctrl in (("control", "abs:corner AND abs:cumulants", "2211.05159"),
                     ("Dirac corner cumulants", "abs:corner AND abs:cumulants AND abs:Dirac", None),
                     ("corner EE + fluctuations + Dirac", "abs:corner AND abs:entanglement AND abs:fluctuations AND abs:Dirac", None),
                     ("corner EE + FCS/cumulant", 'abs:corner AND abs:entanglement AND (abs:"counting statistics" OR abs:cumulant)', None),
                     ("disorder operator + corner", 'abs:"disorder operator" AND abs:corner', None)):
    tot, ents = arx(q)
    print(f"arXiv [{lab}] {q}: total {tot}" + (f"  control {ctrl} {'HIT' if any(i.startswith(ctrl) for i, _ in ents) else 'MISSED'}" if ctrl else ""))
    if not ctrl:
        for i, t in ents: print(f"    {i:14s} {t[:100]}")
    time.sleep(3)
