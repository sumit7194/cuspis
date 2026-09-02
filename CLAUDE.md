# Operating contract

**Read `TASK.md` for the problem, `SISTERS.md` for the four sibling repos and how to use them.
This file is the working discipline and it loads every session. It is short on purpose.**

---

## The three principles these rules were written under

1. **Explicit over implicit.** Instructions are followed literally. An implicit expectation
   ("obviously you would record that") is reliably violated. State it or lose it.
2. **Falsifiable over aspirational.** *"Be rigorous"* is not a rule. *"Change exactly one variable
   per experiment"* is — both you and a reader can check compliance.
3. **Failure-driven over theory-driven.** Every rule below exists because someone watched that
   failure happen, not because it sounded desirable.

*(Adapted from Zimmer, Pelleriti, Roux & Pokutta, arXiv:2603.15914, plus the four sibling repos'
own lesson ledgers. Where the two agree independently, the rule is in bold.)*

---

## Rules

**I. Never break a promise.** If you say "I will now run X", run it, or say up front that you are
deferring it and why.

**II. Never manipulate evaluation.** Do not change metrics, tolerances, test cases, or the problem
definition to make a result look better. Do not hard-code an answer or pick a favourable seed.

**III. Never fabricate a citation.** Verify every reference against the actual source — exact title,
full author list, year, identifier. **If you cannot find it, say so. Never cite from memory alone.**

**IV. Finish autonomous work before reporting.** Do not stop to ask whether to continue when the
plan already says what comes next. Report once, with all of it.

**V. Make it work before moving on.** *A crash is a bug, not a bad idea.* Do not discard an approach
because the first implementation failed. Investigate, fix, re-run.

**VI. One variable per experiment.** If two things change and the result improves, you have learned
nothing about which one did it.

**VII. Evaluate in tiers.** Tier 1 (seconds): does it run? Tier 2 (minutes): any signal on a small
case? Tier 3: the real number that goes in the report. **Never conclude from a Tier-1 or Tier-2 run.**

**VIII. Bound your expectations.** Before implementing a fix, work out the theoretical best case. A
small improvement reported without knowing how much was available is not a result.

**IX. Record everything.** Every experiment gets an entry in `report.md` with Goal / Hypothesis /
Method / Implementation / Results / Analysis / Next Steps. **If it is not in the report it did not
happen.** Keep `TODO.md` as a living list of open questions, unverified claims, and deferred work.

**X. Verify before claiming.** **Assume you are wrong until verified.** Write verification scripts,
not explanations. Actively try to falsify your own result: test edge cases, randomise inputs, hunt
counterexamples. **Grade every claim `verified` / `partially verified` / `unverified` and never let
an unverified one travel without its label.**

### Mathematics-specific

**M1. Prior art before derivation.** Search the literature *first*, and say what you found. The two
most recent failures in this family of projects were both a correct computation of a result that
already existed. **A prior-art sweep is the cheapest possible way to not spend a week.**

**M2. Precise notation.** Define every symbol before first use — dimensions, ranges, scalar vs
tensor, index conventions. Apply the same rigour to negative results as to positive ones.

**M3. Counterexample first.** Before attempting a proof or committing to a closed form, actively
try to break it: random inputs, boundary cases, small instances enumerated exhaustively. If a
counterexample exists you find it faster than a failed proof does. **If none survives, the search
usually exposes the structural fact that makes the proof work.**

---

## Rules bought by this family of projects specifically

**A check that cannot fail is not a check.** Four independent instances were found in one evening,
two of them *correct statements doing no work*. Before trusting a control, ask what input would make
it fire. If nothing would, it is decoration. *Related: a pre-registration can name a failure mode
precisely and still be unable to detect it — naming and detecting are separate acts.*

**A blow-up announces itself; a plateau recruits you.** A number that explodes gets caught in
minutes. A number that looks like convergence can be an artifact of the fit and survive for hours.
**Sweep the nuisance parameter (fit degree, fit range, grid) and report the drift. A quantity that
moves when a non-physical parameter moves is not a measurement.**

**Extracting series coefficients from numerics is inference, not verification.** In a recent case it
yielded three real coefficients and two convincing fictions. **Evaluating a candidate closed form at
points is verification. Inferring its coefficients from points is not.** Know which you are doing.

**State which of their premises you are keeping.** When correcting someone's number, name the
assumption you are carrying over. If you cannot name one, you have checked the arithmetic and not
the argument.

**Report the failed replication, with the reason.** A silent one is invisible to everyone and is the
easiest thing in any day's work to skip.

---

## The read-only rule

`SISTERS.md` lists four sibling repositories. **They are READ-ONLY.** Import from them, read their
data, cite their results with attribution — never modify them, and never write anything of this
project into them. They were built with independent roots on purpose, which is the only reason
agreement between them counts as evidence rather than echo.
