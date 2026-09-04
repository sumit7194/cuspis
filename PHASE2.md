# Phase 2 — the two things the first run left open

**Set up 2026-09-05. Do not read this before `RESULT.md`.** Phase 1 is finished, it settled seven
things, and it named what it could not reach. **This page adds no new framing: the targets below
are quoted from §10 of `RESULT.md`, written by the run that stopped, before anyone knew what would
come next.** That is deliberate — a follow-on task written by an outsider after seeing the result
would be a task shaped by hindsight.

---

## What is already settled — do not re-derive it

From `RESULT.md` §10. **All seven are done. Re-deriving any of them is the failure mode this family
has paid for twice.**

1. The prior-art sweep, with two corrections to the original task statement (EXP-001).
2. **The reframe:** to ≈1% the collapse *is* the statement `κ/C_T ∈ [3.672, 4.179]`; the ≈1% shape
   residual is a separate, open fact.
3. The t₄ obstruction: equal-t₄ theories differ in κ/C_T by up to 11.5% (EXP-002).
4. **The theorem of §4:** no general entropic constraint bounds κ/C_T or a(θ)/C_T above. Analytic,
   with a falsifiable numerical companion. *Independently verified by `../quantum`, commit dbd443a.*
5. What a bound must use (§5), and why d = 2 has it while d = 3 does not (§6).
6. The solvable instance read to the bottom: κ₂ and the UV datum are different moments of one
   positive function (§6, EXP-008/011).
7. The Dirac–Einstein `c_S/C_T` near-coincidence is chance on a known loose pattern (EXP-010).

---

## Target A — the shape residual

> **"(a) The shape residual: why the (σ, κ) trial function reproduces every curve to ≈1%, and
> whether its sign is universal."** — `RESULT.md` §10, ranked first for value

**In one line:** two numbers should not be enough to reproduce a whole function, and they nearly
are. Phase 1 showed the *band* in κ/C_T is not forced by the known constraints. It did not explain
why, once σ and κ are fixed, **the rest of the curve follows to about a percent for every theory
anyone has computed.**

**The bar is quantitative and it is stated in `TASK.md`:** an explanation must predict the residual
in **size and sign**. *"Any explanation must predict the size and the sign of the residual
deviations, and those deviations are measured."*

**And there is a specific, cheap, checkable sub-question inside it** — *whether the sign is
universal*. That is a fact about existing published curves, decidable from tables, and it is the
kind of question whose answer constrains every candidate mechanism before any mechanism is built.
**Establish it first.**

*Note from §10 on the parked instrument:* `scripts/exp004_*` is a validated double-precision and
arbitrary-precision solver for the Casini–Huerta–Leitao ODE system, built because no four-digit
free-field `a(θ)` below 45° is published. **§10 says: resume it only if the shape residual becomes
the target, and re-run its known-answer controls first.** The shape residual is now the target.
The controls still come first.

---

## Target B — what a bound on κ would actually need

> **"(b) The real input for any bound on κ: a growth condition on the bulk-channel density of the
> two-defect function from outside the tail — either a second positive expansion with a universal
> lowest state (shown absent for two balls in d ≥ 3) or an analyticity-plus-growth argument for
> defect fusion, which does not yet exist."** — `RESULT.md` §10

**This is the harder one and the one that would close the problem rather than describe it.** §4
proved no general entropic constraint bounds κ/C_T above; §5 says what a bound would have to use;
§6 says why the d = 2 analogue has it and d = 3 does not. **B is the missing ingredient itself.**

Phase 1 narrowed it to two routes and reported one of them dead — *a second positive expansion with
a universal lowest state is **shown absent** for two balls in d ≥ 3.* **That leaves one live route
and it does not exist yet.** Constructing it, or proving it cannot exist, is the result.

**If you take B, take §6's named falsifier with you:** *"a third bridge that supplies a growth
condition at the tail end."* An attack that does not engage with it is attacking §6's conclusion
rather than its argument.

---

## Where to push if you want to attack Phase 1 instead

§10 says exactly where, and it is worth reading as an instruction rather than a caveat:

> *"If you want to attack the theorem, the place to push is **not the inequalities** (they are all
> positivity) **but the scope line of §0**: exhibit a **unitary CFT** constraint that some positive
> spectral density violates."*

**That is a legitimate third target.** The theorem's strength is exactly the width of its scope
line, and the run that proved it named its own weakest point rather than defending it.

*Also open and explicitly harmless:* **(c)** the ECG t₄ sign discrepancy between [BCV21] and
[BCR18]. §10 records that it *"does not affect any conclusion here."* Resolving it is bookkeeping,
not physics — do not spend the run on it.

---

## Everything else is unchanged

`CLAUDE.md` is the operating contract and still governs. `TASK.md` holds the original problem, the
frozen three-tier protocol and the outcome ladder — **and its Tier 3 is still retired**: the
sibling's `a(120°)` violates a rigorous lower bound, so use [CHL09] Table 1 and [HHCWM16]
Tables 1–2 as referee. `report.md` continues from EXP-011. `references.md` has 52 verified entries
and records, for each, **what was actually read** — abstract, table, or full text. Keep that
distinction; it is why the sweep is trustworthy.

**One rule bought since Phase 1 ran, and it applies directly to `scripts/exp004_*`:**

> **A known-fail control tests the mechanism. Only contact with real data tests the rule.** A
> control built from your own understanding cannot contain the case that understanding omits. When
> the parked solver's controls pass, that establishes it responds — not that it is asking the right
> question. Run it against a published value before trusting it on an unpublished one, and treat
> its first disagreement with a table as evidence about the solver.
