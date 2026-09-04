# Why do theories that share nothing else agree on a(θ)/C_T?

> **Corrections from EXP-001 (2026-09-04), see `report.md` R3.** Everything below was written from
> recollection; the sweep found it mostly right and inflated in two places:
> 1. The "family of higher-curvature holographic models" of [BM15] has a(θ)/C_T *identically* equal
>    to the Einstein function (both a and C_T rescale by the same constant). It is not independent
>    evidence. The only holographic family with a different shape is cubic gravity [BCV21]; across
>    the allowed coupling range it stays within ±1% of Einstein and lies *below* it for t₄ > 0.
> 2. The Wilson-Fisher points exist at one angle (π/2) with ±8–10% errors, where every theory is
>    within 2% of every other by construction (the value there is pinned by the universal σ). They
>    do not test the collapse. At N = ∞ the WF corner function is exactly N × free scalar [WWS17].
> 3. The bound is right: a(θ) ≥ (π²C_T/3) log[1/sin(θ/2)] [BWK16]. "Nearly saturated" holds for
>    θ ≳ π/2 (7–9% excess at π/2), not at small angles (36–41% below the true values at 26.6°).
> 4. Measured deviations from Einstein: scalar +12.7% (θ→0) → +1.9% (π/2); fermion +2.5% → +0.3%;
>    ECG ±1.0% → ±0.3%. To ≈1% every known curve is fixed by (σ, κ); the collapse *is* the band
>    κ/C_T ∈ [3.672, 4.179].
> 5. Tier 3 as written cannot gate anything: `../quantum`'s a(120°) is below the rigorous bound and
>    its a(60°) is ≈8% low. Use the [CHL09]/[HHCWM16] tables as referee instead.

## The setup, in one paragraph

Take a 3d (2+1 dimensional) conformal field theory in its ground state, pick a spatial region,
and compute the entanglement entropy of the inside with the outside. A **smooth** boundary gives
entropy proportional to the perimeter. A **sharp corner** of opening angle θ adds a *logarithmic*
term whose coefficient is a function of the angle:

    S  =  B · (perimeter/δ)  −  a(θ) · ln(perimeter/δ)  +  O(1)

`a(θ)` is **universal** — independent of the regulator, the lattice, and every microscopic
detail. It is an intrinsic property of the CFT itself.

## The actual problem

Normalise `a(θ)` by `C_T`, the coefficient of the stress-tensor two-point function. Then:

> **The function a(θ)/C_T is very nearly the SAME for the free scalar, the free Dirac fermion,
> strongly-coupled holographic theories, a family of higher-curvature holographic models, and the
> interacting Wilson–Fisher fixed points of the O(N) models.**
> *[EXP-001: three independent curves (scalar, fermion, Einstein) plus a ±1% cubic-gravity band;
> the [BM15] family is identical to Einstein by construction; WF is measured at π/2 only, ±8%.]*

These theories share almost nothing. Different field content, different spectra, different
interactions, free versus strongly coupled, Lagrangian versus not. **And their normalised corner
functions collapse onto each other.**

There is also a proven lower bound, believed to be of the form

    a(π/2)  ≥  (π² ln 2 / 6) · C_T        [verified: BWK16 eq II.4; general form (π²C_T/3) log(1/sin(θ/2))]

**which all known theories nearly saturate.** *[EXP-001: 7–9% excess at π/2; not near saturation
below ~60°.]*

> ### **WHY?**
>
> **This is an observation, not a theorem. Nobody has explained it. That is the task.**

---

## Three ways in. They are not alternatives — a real answer probably touches two.

### ① EXPLAIN THE COLLAPSE

What structural fact forces theories with different spectra and different dynamics to produce
nearly the same normalised corner function?

**The bar is quantitative, not narrative.** The theories do not agree *exactly* — they agree
*nearly*. **Any explanation must predict the size and the sign of the residual deviations**, and
those deviations are measured. An argument that explains why they agree, without explaining why
they disagree by exactly as much as they do, is incomplete and should be labelled as such.

*A plausible-sounding mechanism that cannot be turned into a number is worth very little here.
Say so if that is what you have.*

### ② BREAK IT

**Find or construct a CFT where a(θ)/C_T departs substantially from the collapse.**

This is the counterexample-first route (rule M3) and it is the one recent frontier results have
most often succeeded on. Two outcomes, both real:

- **A counterexample exists** → the near-universality is an accident of the theories anyone has
  looked at, and you have shown which structural feature they all happened to share.
- **Every attempt fails in the same way** → the failures localise the hypothesis. *A theorem is
  hiding, and the shape of the failures tells you what its conditions are.* **Report the failed
  constructions with their reasons. A silent failed attempt is invisible to everyone.**

Candidate directions worth considering — establish for yourself whether each is even admissible:
theories with large numbers of fields, theories with unusual central-charge ratios, non-unitary
CFTs, theories with higher-spin currents, deformations that move C_T without moving the corner
structure.

### ③ SHARPEN THE BOUND

The lower bound is nearly saturated by everything known. **Is it tight? Is there a matching upper
bound? Is near-saturation itself the thing that needs explaining, rather than a coincidence?**

If a two-sided bound can be established with a small enough gap, **the near-universality stops
being mysterious and becomes a corollary** — that would be the cleanest possible resolution and
it is a legitimate target.

---

## Where the difficulty sits

**As far as anyone knows, the obstruction here is conceptual rather than computational.** The
numbers exist — the corner functions have been computed, for several theories, by several groups.
What is missing is an account of why they land where they do. **No calculation currently on the
table produces that account by finishing.**

That is a statement about the state of the problem, **not a restriction on you.** If you conclude
that a substantial computation *is* the way in — a new theory's corner function, a large symbolic
derivation, a systematic search over some space — **do it, and say why the reasoning route was
insufficient.** Discovering that this problem has a computational core after all would itself be a
finding, and a surprising one.

**One epistemic point that is a real constraint, and it is about inference rather than cost:** a
pattern that emerges from a scan is a hypothesis, not a result. **A number is not an explanation.**
If a computation produces something suggestive, it still needs an independent argument before it
counts — and see the note on inference-versus-verification in `CLAUDE.md`, which was bought at the
price of two convincing fictions.

**It is not a literature review.** The prior-art sweep is a prerequisite, not the deliverable.

---

## Before anything: M1, and it is a real gate

**Do the prior-art sweep first and report before deriving.** Verify every citation against the
actual source.

**Everything stated above is written from an assistant's recollection and is UNVERIFIED.** The
bound's exact form and coefficient, which theories have been checked, how close the collapse
actually is, and whether an explanation already exists — **all of it must be checked against
sources before you build on it.** If any of it is wrong, correcting it is a result and you should
report it rather than quietly routing around it.

**Specifically establish:** how large the deviations between theories actually are, at which
angles, and with what error bars. **You cannot explain a collapse whose magnitude you have not
measured.**

---

## Verification protocol — frozen before any result

    TIER 1  EXACT      Does the claim reproduce known exact results symbolically -- the
                       theta -> pi limit, the theta -> 0 limit, the bound at pi/2, and the
                       exact values for the free scalar and free fermion where they exist?
                       Symbolically equal, not numerically close.
                       [EXP-001: exact closed forms exist for sigma (1/256, 1/128) and sigma'
                       ((20+3pi^2)/(9216pi^2) per complex scalar, (16+3pi^2)/(9216pi^2) per Dirac);
                       a(pi/2) etc. are 4-digit numerics; kappa is an integral of the 2d c-function.]

    TIER 2  STRUCTURAL Does it respect the constraints a(theta) must satisfy -- positivity,
                       monotonicity, convexity, any reflection property? Establish WHICH of
                       these actually hold, with sources, before using any as a gate.

    TIER 3  NUMERICAL  Does it reproduce the measured deviations between theories, in SIZE
                       and in SIGN? ../quantum can supply a(60), a(90), a(120) for a free
                       scalar on two lattices with across-regulator spreads.
                       [EXP-001: ../quantum's a(120) violates the BWK16 bound by 13% and a(60) is
                       ~8% low; use CHL09 Table 1 and HHCWM16 Tables 1-2 as the referee instead.]

**Grade every claim `verified` / `partially verified` / `unverified`.** A mechanism that passes
Tier 2 and fails Tier 1 is `unverified`, however elegant.

---

## Outcomes, ranked, all reportable

    A  An explanation of the collapse that predicts the residual deviations in size and sign.
    B  A counterexample: a CFT where a(theta)/C_T departs substantially, with the structural
       reason the collapse fails there.
    C  A two-sided bound tight enough to make the near-universality a corollary.
    D  A sharpened one-sided bound, or a new exact value, or a new term in an expansion.
    E  A proof that a stated class of explanations CANNOT work, with the obstruction named.
    F  A verified finding that this is already resolved in the literature, with the citation.
       REPORT IT AND STOP -- this is a result, not a failure.

**E is worth more than it looks.** *"No argument of this type can produce the observed deviation
sizes, and here is why"* is a real contribution and is often reachable when A is not.

---

## What would make the work worthless

- An explanation with no number attached to it.
- A mechanism fitted to the collapse after seeing it, with no independent prediction.
- Any claim about which theories agree, or by how much, that was not checked against a source.
- A citation written from memory.
- Treating the two-limit asymptotics as *given* rather than as the first thing to verify.
- **Reporting agreement without reporting the disagreement.** The deviations are the signal here.
  A collapse quoted as "they all agree" has thrown away the entire quantitative content.
