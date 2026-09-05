# corner_function

**Why do conformal field theories that share almost nothing else agree on the normalised corner
function a(θ)/C_T — and by exactly the amount they disagree?**

The collapse across free scalars, free fermions, holographic models and Wilson–Fisher fixed points
is an **observation with no explanation**. There is a proven lower bound that all of them nearly
saturate, and no account of why. **That gap is the task.**

Set up 2026-09-02 as a self-contained workspace for a frontier-model research run, with read-only
access to four sibling research repositories.

## Outcome so far (2026-09-05)

**[RESULT.md](RESULT.md) — the general entropic constraints do not localise κ/C_T.** Reframed, the
collapse is the statement that κ/C_T lies in a 13% band, plus a separate ≈1% shape residual. The
band is *not* a consequence of the known constraints: every value of κ/C_T in (0, ∞) is admissible,
and a(θ)/C_T is unbounded above at every angle. This answers, in the negative, a question left open
in the literature, and it means the collapse needs an explanation the constraints cannot give.
Phase 2 (2026-09-05): the residual's sign is set by one number at each end of the interval and is
not universal; the free scalar's sharp-end constant was measured and its predicted node found at 27°;
and the missing bridge for a bound on κ exists in the 2026 cusp-bootstrap literature — a rectangle
crossing giving κ ≥ (2π/3)a(π/2), hence κ/C_T ≥ 2.39 — and is provably one-sided, so the upper edge of
the band is still explained by nothing. Start at RESULT.md; §10 is the handover.

## Read in this order

| file | what it is |
|---|---|
| **[PHASE2.md](PHASE2.md)** | **what Phase 1 left open** — the two targets, quoted from RESULT.md §10 rather than reframed. Read RESULT.md first. |
| **[RESULT.md](RESULT.md)** | **the result** — standalone: statement, scope, proof, mechanism, prior work, handover |
| **[TASK.md](TASK.md)** | the problem, what is believed known (**and must be verified**), the frozen three-tier verification protocol, and the five reportable outcomes |
| **[CLAUDE.md](CLAUDE.md)** | the operating contract — loads every session, deliberately short |
| **[SISTERS.md](SISTERS.md)** | the four sibling repos: what each holds, which file to open for what, and the read-only rule |
| **[TODO.md](TODO.md)** | living list of open questions and unverified claims |
| **[report.md](report.md)** | one entry per experiment (EXP-001 … EXP-011), required fields enforced |
| **[references.md](references.md)** | 52 verified references, each with *what was actually read* (abstract / table / full text) |
| **[scripts/README.md](scripts/README.md)** | the checks, the parked instrument, and how to re-fetch the source texts |

## The shape of the thing

```
S  =  B · (perimeter/δ)  −  a(θ) · ln(perimeter/δ)  +  O(1)
```

`a(θ)` is **universal** — independent of regulator, lattice, and microscopic detail. Normalise it
by `C_T` and theories with different field content, different spectra, and different couplings
land on nearly the same curve. **Nearly**, not exactly — and the residuals are the whole
quantitative content of the problem.

**The obstruction is believed to be conceptual rather than computational** — the numbers exist for
several theories; the account of why they agree does not. That is a description of the problem's
current state, not a restriction: if a large computation turns out to be the way in, take it and
say why the reasoning route was insufficient.

## How verification works here

The point of this setup is that **a wrong answer is detectable**, which is not true of most open
problems.

```
TIER 1   both known limits reproduced ANALYTICALLY      exact, symbolic, unfoolable
TIER 2   structural constraints a(θ) must satisfy       exact, once established with sources
TIER 3   matches ../quantum's a(60°), a(90°), a(120°)   numerical, three points, weak
```

Tier 3 alone can be passed by a wrong formula. **Tier 1 is the gate.**

**Tier 3's referee did not survive the run.** `../quantum`'s a(120°) sits 13% *below* a rigorous
lower bound that follows from strong subadditivity, Lorentz invariance and C_T alone — so the
lattice number, not the bound, is the suspect. Details and extraction parameters are in
[TODO.md](TODO.md) under *Handed off*; the sibling is read-only and was not modified. Use
[CHL09] Table 1 and [HHCWM16] Tables 1–2 as the referee instead.

## The sibling repositories

Four projects with deliberately independent roots, kept ignorant of each other so that agreement
between two of them is evidence rather than echo. **All read-only.**

```
../quantum              vestigium        the referee -- measures a(60°), a(90°), a(120°)
../conjecture_machine   ansatz machine   exact symbolic GR; the model for a validated instrument
../SpaceTime            tabula           silent_nulls.md: 45+ ways a bug reads as a result
../BlackHole            DeepStrain       real LIGO data; source of the "plateau" failure mode
../TheBridge            trivium          the cross-validation layer and the lessons ledger
```

`SISTERS.md` says which file to open for what. **Nothing there needs to be loaded by default** —
go and get what you need when you need it.

## Ground rules, in one line each

- **Prior art first.** Two recent efforts in this family were correct computations of results that
  already existed. Finding this one is already solved is a *result*, not a failure.
- **Grade every claim** `verified` / `partially verified` / `unverified`, and never let an
  unverified one travel without its label.
- **Do not fit a formula to three points and call it verified.** That is inference, not
  verification.
- **The siblings are read-only.** Cite them by repo and file in the same sentence as the number.
