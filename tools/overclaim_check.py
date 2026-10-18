#!/usr/bin/env python3
"""Overclaim guard (user-approved 2026-10-18; a mechanism for a slip seen three times: 'clean' leak scan, 'strict'
bound, 'strongest' inequality, each later corrected).

Run as the git commit-msg hook: overclaim_check.py <commit-msg-file>. Checks the commit message and every ADDED line of
staged *.md files. A strong-claim word is accepted only if a grade or qualifier sits on the same line or an adjacent
one; otherwise the commit is refused and every hit is printed. Override, deliberately and with a reason, by putting
'[overclaim-ok: <reason>]' in the commit message.
Self-test: overclaim_check.py --selftest"""
import re, subprocess, sys

CLAIM = re.compile(r"\b(strongest|strict(ly)?|proved|proven|proof of|clean|independent(ly)?|rigorous(ly)?|"
                   r"definitive(ly)?|settled|establish(ed|es)?|confirm(ed|s)?)\b", re.I)
GRADE = re.compile(r"(\bverified|unverified|\bargued\b|conjectur|not a theorem|physics[- ]level|from memory|"
                   r"\bpremises?\b|under P\d|conditional on|within-session|not independent|was wrong|not proved|"
                   r"not settled)", re.I)
# Deliberately NOT qualifiers: 'corrected', 'correction', 'superseded' -- the 2026-09 slip (fda21ac) passed a looser
# list because 'corrected' elsewhere on the line referred to a different claim.
OVERRIDE = re.compile(r"\[overclaim-ok:\s*[^\]]{4,}\]", re.I)


def hits(lines, origin):
    out = []
    for i, ln in enumerate(lines):
        if not CLAIM.search(ln):
            continue
        ctx = " ".join(lines[max(0, i - 1): i + 2])
        if not GRADE.search(ctx):
            out.append(f"{origin}:{i + 1}: {ln.strip()[:160]}")
    return out


def staged_md_added():
    diff = subprocess.run(["git", "diff", "--cached", "-U0", "--", "*.md"], capture_output=True, text=True).stdout
    res, cur, block = [], None, []
    for ln in diff.splitlines():
        if ln.startswith("+++ "):
            if block: res += hits(block, cur)
            cur, block = ln[6:], []
        elif ln.startswith("+") and not ln.startswith("+++"):
            block.append(ln[1:])
        elif ln.startswith("@@") and block:
            res += hits(block, cur); block = []
    if block: res += hits(block, cur)
    return res


def main(msgfile):
    msg = open(msgfile).read()
    body = [l for l in msg.splitlines() if not l.startswith("#")]
    if OVERRIDE.search(msg):
        print("overclaim_check: override present, commit allowed:", OVERRIDE.search(msg).group(0)); return 0
    found = hits(body, "commit-message") + staged_md_added()
    if not found:
        return 0
    print("overclaim_check: strong-claim words without a grade/qualifier nearby (verified / partially verified /\n"
          "unverified / argued / under premises ...). Add the grade, soften the word, or override with\n"
          "'[overclaim-ok: <reason>]' in the commit message.\n")
    for f in found: print("  " + f)
    return 1


def selftest():
    must_fire = ["Quantum copy: CF-2 misattribution corrected (bridge-approved wording, leak scan clean); S16: EMI "
                 "satisfies C11 exactly",  # the real fda21ac message
                 "leak scan clean", "This is the strongest inequality.", "a strict upper bound on the tail",
                 "independent review of S14"]
    must_pass = ["Q is implied by C2 + C3 (verified, exact identity)",
                 "the strongest inequality is C3 (partially verified: tip-fixed deformations only)",
                 "derived at physics level; not a theorem", "EXP-031 results table", "no claim words here"]
    bad = [s for s in must_fire if not hits([s], "t")] + [s for s in must_pass if hits([s], "t")]
    print("selftest:", "PASS" if not bad else f"FAIL on {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if sys.argv[1:] == ["--selftest"] else main(sys.argv[1]))
