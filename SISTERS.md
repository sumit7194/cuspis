# The four sibling repositories — a reference map

**These are READ-ONLY.** Import from them, read their data, cite their results with attribution.
Never modify them. Never write anything belonging to this project into them.

They were built with **independent roots on purpose**, and are deliberately kept ignorant of each
other. That is the entire reason agreement between two of them is evidence rather than echo. A
result relayed from one to another is *repeated*, not *corroborated* — the originating repo has to
be named in the same sentence as the number.

**This file is a map, not a payload.** Nothing below needs to be in context by default. Open a
path when you need what it holds, and not before.

---

## The one that matters most for this task

### `../quantum` — *vestigium* · verified QM lattice numerics

**This is the referee for `TASK.md`.** It already measures the corner coefficient on real lattices
and can supply the numerical values a candidate closed form must reproduce.

    qsim/corner_angles.py       a(60) and a(120) on a TRIANGULAR lattice, plus the reasoning
                                for why a square lattice can only give 90 degrees cleanly
    qsim/corner_coefficient.py  a(90) on the square lattice -- the original single point
    qsim/corner_s6.py           the s=6 refinement run; gaussian_entropy() is the core kernel
    qsim/hexagon_admissibility.py   which regulators are admissible on the triangular lattice
    README.md                   the project's own honest summary, including what it withdrew

**Read `qsim/corner_angles.py`'s docstring first.** It contains a pre-registration, a demoted
prediction, a control that can genuinely fail, and the geometric reason only three angles are
available. All four are relevant to how you verify anything.

**What it can give you:** `a(60°)`, `a(90°)`, `a(120°)` with across-regulator spreads, under both a
3-parameter and a 4-parameter fit. **What it cannot:** a continuum of angles. The lattice permits
these three cleanly and nothing else.

**Its entropy kernel, if you want to compute your own:**

    gaussian_entropy(XA, PA):  eigh -> Xh = (U*sqrt(ev)) @ U.T ; C = Xh @ PA @ Xh
                               nu = sqrt(clip(eigvalsh((C+C.T)/2), 0.25, None))
                               S = sum[ (nu+1/2)ln(nu+1/2) - (nu-1/2)ln(nu-1/2) ]

*Note the `eigh` route rather than `scipy.linalg.sqrtm`: `XA` is symmetric positive definite by
construction, and the specialised route measured 32% less memory and 2x faster at matched accuracy
(agreement to 2e-10). Use it.*

---

## The other three

### `../conjecture_machine` — *ansatz machine* · exact symbolic GR, deductive

Genetic programming proposes metrics, SymPy verifies them — **theorem or nothing**. Relevant here
only as a source of exact-verification technique and as a worked example of a validated instrument.

    scripts/_kt_exact.py     an exact Killing-tensor prover over GF(p), two primes
    scripts/_kt_metrics.py   the single place that knows what a substrate is
    RESULTS.md               S127 is the model to copy: an instrument that had only ever
                             returned "nothing" was made to return "something" on a
                             substrate whose answer was known in advance
    docs/DECISIONS.md        design rules and what each one cost
    verify.sh                the local gate -- every battery, both directions, one verdict

**Read S127 if you build any verifier.** A checker that has only ever said "no" has not been shown
able to say "yes".

### `../SpaceTime` — *tabula geometrica* · neural geometry from observation, inductive

Trains networks on raw observations and asks whether geometry emerges as the cheapest explanation.
**Its methods writeups are more useful to you than its physics.**

    writeups/silent_nulls.md              45+ measured ways a BUG reads as a RESULT, each with
                                          the diagnostic that caught it. READ THIS BEFORE
                                          BUILDING ANY CONTROL.
    writeups/representability_frontier.md a runnable diagnostic that says whether a cheap legible
                                          code exists / is unique / is global / is linear
    writeups/legibility_law.md            the project's crystallised result
    curvature/                            the live experiments

### `../BlackHole` — *DeepStrain* · real LIGO data, empirical

Real-data searches with sensitivity from injections and significance from measured background.
**Relevant here mainly as the source of the "prior returning itself" and "plateau" failure modes.**

    README.md    the three searches and their honest negatives
    verify.sh    46 regression checks asserting the headline numbers never silently change

### `../TheBridge` — *trivium* · the cross-validation layer

Reads all four read-only and never modifies them. **This is where cross-repo claims belong** — if
you need a result from one sibling to justify something about another, that is a bridge leg, not a
line in this project.

    CAPSTONE.md            program scoreboard, five load-bearing results, honest-miss ledger
    FALSIFICATION_V2.md    twelve standing lessons, each bought by a named failure
    SISTER_REQUESTS.md     how asks are filed and answered; Round-13 is the most recent
                           and shows a prior-art gate killing a framing before compute
    ../.claude-coordination/PROTOCOL.md    the shared inter-session protocol, 24 sections

---

## How to use them from here

Everything is a sibling directory of this one:

    ../quantum  ../conjecture_machine  ../SpaceTime  ../BlackHole  ../TheBridge

Read files directly with relative paths. To run a sibling's code, `cd` into it so its own
environment and imports resolve — for example `cd ../conjecture_machine && ./verify.sh`, or
`cd ../quantum && python3 qsim/corner_angles.py`. **Do not copy their source into this repo;
reference it.** If you need a modified version, write your own here and say in the header which
sibling file it derives from.

**If a sibling's number is load-bearing for a claim of yours, name the repo and the file in the
same sentence as the number.** Attribution drifts to the last speaker unless somebody logs it.

---

## Live sessions

Other Claude sessions may be running in these repos. Two sessions writing one repository is a real
hazard this family has already paid for. Before writing anywhere outside this folder — which the
read-only rule already forbids — check, and prefer messaging over assuming.

**Not every session on this machine belongs to this family.** Several are unrelated office work.
**Identify a session by its working directory, never by its name** — verify with
`lsof -a -p <pid> -d cwd`. A name prefix is not proof.
