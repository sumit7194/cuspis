"""EXP-098 SEAL: the k = 3 prediction from D(1), D(2) by the method fixed in registration section 5 (243b079), verbatim. [model: Opus 5.5]
Reads exp098_stage0.json only. Written BEFORE free(9, 12) or any W9 value exists."""
import json, math, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); f = os.path.join(HERE, "exp081d_results", "exp098_stage0.json")
raw = open(f, "rb").read(); J = json.loads(raw)["readings"]; r1, r2 = J["1"], J["2"]; RC3 = 11.7582
d1, d2, sd1, sd2 = r1["d"], r2["d"], r1["sigma_d"], r2["sigma_d"]
dp = d2 + (d2 - d1); sp = math.hypot(abs(d2 - d1), sd2 + sd1)
q1, q2, sq1, sq2 = r1["q"], r2["q"], r1["sigma_qrel"], r2["sigma_qrel"]
qp = q2 + (q2 - q1); sqp = math.hypot(abs(q2 - q1), sq2 + sq1)
out = dict(input=os.path.relpath(f, HERE), input_sha256=hashlib.sha256(raw).hexdigest(), Rc3=RC3,
           d_pred=dp, sigma_d_pred=sp, D_pred=dp * RC3, sigma_D_pred=sp * RC3,
           band_W3=[(dp - 2 * sp) * RC3, (dp + 2 * sp) * RC3],
           q_pred=qp, sigma_q_pred=sqp, Rq_pred=RC3 * (1 + qp), sigma_Rq_pred=RC3 * sqp)
json.dump(out, open(os.path.join(HERE, "exp081d_results", "exp098_SEAL.json"), "w"), indent=1)
for k, v in out.items(): print(f"{k:14s} {v}")
