# corner_function

**Why do conformal field theories that share almost nothing else agree on the normalised corner
function a(θ)/C_T — and by exactly the amount they disagree?**

The collapse across free scalars, free fermions, holographic models and Wilson–Fisher fixed points
is an **observation with no explanation**. There is a proven lower bound that all of them nearly
saturate, and no account of why. **That gap is the task.**

Set up 2026-09-02 as a self-contained workspace for a frontier-model research run, with read-only
access to four sibling research repositories.

## Read in this order

| file | what it is |
|---|---|
| **[TASK.md](TASK.md)** | the problem, what is believed known (**and must be verified**), the frozen three-tier verification protocol, and the five reportable outcomes |
| **[CLAUDE.md](CLAUDE.md)** | the operating contract — loads every session, deliberately short |
| **[SISTERS.md](SISTERS.md)** | the four sibling repos: what each holds, which file to open for what, and the read-only rule |
| **[TODO.md](TODO.md)** | living list of open questions and unverified claims |
| **[report.md](report.md)** | one entry per experiment, required fields enforced |

## The shape of the thing

```
S  =  B · (perimeter/δ)  −  a(θ) · ln(perimeter/δ)  +  O(1)
```

`a(θ)` is **universal** — independent of regulator, lattice, and microscopic detail. Normalise it
by `C_T` and theories with different field content, different spectra, and different couplings
land on nearly the same curve. **Nearly**, not exactly — and the residuals are the whole
quantitative content of the problem.

**This is a reasoning task, not a compute task.** There is no long calculation whose completion
answers it. Numerics verify claims here; they do not produce them.

## How verification works here

The point of this setup is that **a wrong answer is detectable**, which is not true of most open
problems.

```
TIER 1   both known limits reproduced ANALYTICALLY      exact, symbolic, unfoolable
TIER 2   structural constraints a(θ) must satisfy       exact, once established with sources
TIER 3   matches ../quantum's a(60°), a(90°), a(120°)   numerical, three points, weak
```

Tier 3 alone can be passed by a wrong formula. **Tier 1 is the gate.**

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
