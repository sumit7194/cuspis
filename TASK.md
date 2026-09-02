# The corner function a(θ) for a free scalar

## The problem

Take a 3d (2+1 dimensional) conformal field theory in its ground state. Pick a spatial region,
trace out everything outside it, and compute the entanglement entropy of what remains.

For a region with a **smooth** boundary the entropy scales with the perimeter. Introduce a **sharp
corner** of opening angle θ and the corner contributes an additional, **logarithmic** term:

    S  =  B · (perimeter / δ)  −  a(θ) · ln(perimeter / δ)  +  O(1)

with δ the short-distance cutoff. The coefficient **a(θ)** is the object of interest.

**Why it matters.** `a(θ)` is *universal*: independent of the regulator, of the lattice, and of the
microscopic details. It is an intrinsic fingerprint of the CFT, and it appears across condensed
matter, holography, and quantum information as a way to identify which theory one is looking at.

**The open part.** For the **free massless scalar** — the simplest field theory there is — `a(θ)`
is not known in closed form. It is computed numerically, angle by angle. Two limits are believed
known; the interior is not.

> **THE TASK: find a closed form for a(θ) for the free scalar, or establish something new and
> checkable about it.**

---

## Before anything else — M1

**Do the prior-art sweep first and report it before deriving anything.** State what is known, by
whom, and with what identifier, and flag anything that would make this task already solved or
already impossible.

**Everything in the next section is stated as BELIEVED, not as given.** It is written from
recollection, has not been verified against sources by whoever wrote this file, and is exactly the
kind of thing rule III exists for. **Verify each item against the literature and correct this file
before using any of it.** If a stated limit turns out to be wrong or to have a different
coefficient, that discovery is itself worth more than a fast start.

---

## What is believed known — VERIFY BEFORE USE

**The smooth limit, θ → π.** `a(θ)` is believed to vanish quadratically as the corner flattens:

    a(θ)  →  σ · (π − θ)²

and σ is believed to be fixed by the stress-tensor two-point function coefficient C_T, via a
relation of the form σ = C_T · π²/24 — associated with Bueno, Myers and Witczak-Krempa (~2015).
**Verify the relation, its numerical factor, and its conditions of validity.**

**The sharp limit, θ → 0.** `a(θ)` is believed to diverge, faster than quadratically, with a
leading behaviour of the form κ/θ. **Verify the form and the value of κ for the free scalar.**

**The interior.** Numerical values exist in the literature and in the sibling repo `../quantum`.
No closed form is known to the author of this file. **This is the claim most worth attacking
first, because if it is false the task is over in an hour and that is a good outcome.**

---

## Verification protocol — pre-registered, frozen before any result

A proposed closed form is graded on three tiers. **Tier 1 is symbolic and unfoolable. Tier 3 is
numerical and weak. Do not let a Tier-3 pass stand in for a Tier-1 failure.**

    TIER 1  (exact, symbolic)   Does the candidate reproduce BOTH known limits analytically --
                                the correct power AND the correct coefficient? Not numerically
                                close: symbolically equal, after the prior-art sweep has
                                established what the limits actually are.

    TIER 2  (exact, structural) Does it satisfy the constraints a(θ) must obey on general
                                grounds -- positivity, monotonicity, any known convexity or
                                reflection property? Establish which of these hold, with
                                sources, before using them as gates.

    TIER 3  (numerical)         Does it match ../quantum's measured a(60°), a(90°), a(120°)
                                within their stated across-regulator spread, under BOTH the
                                3-parameter and 4-parameter fits?

**Tier 3 is three points with error bars in the tens of percent.** A wrong formula can pass it.
Treat a Tier-3 agreement as necessary and nowhere near sufficient — and remember that a plateau
recruits you while a blow-up announces itself.

### Grading

Every claim is labelled `verified` / `partially verified` / `unverified`, and no unverified claim
travels without its label. **A closed form that passes Tier 3 but fails Tier 1 is `unverified`,
however good the plot looks.**

### The failure mode this protocol exists to catch

*A derivation containing an error — a missing factor of two, a dropped boundary term — whose
output nonetheless looks plausible.* The guard is a verification script that checks the candidate
against an independent computation, not a re-reading of the derivation.

---

## Outcomes, ranked, and all four are reportable

    A   A closed form passing Tier 1 and Tier 3.                        The full result.
    B   A closed form for a restricted range, or an exact value at a
        special angle not previously known.                             A real result.
    C   A new term in one of the asymptotic expansions, or a sharpened
        bound on the interior.                                          A real result.
    D   A demonstration that no closed form of a stated class can
        reproduce both limits.                                          A real result, and the
                                                                        one most likely to be
                                                                        provable.
    E   A verified statement that the problem is already solved in the
        literature, with the citation.                                  ALSO A RESULT. Report it
                                                                        immediately and stop.

**E is not a failure and must not be treated as one.** Two recent efforts in this family of
projects were correct computations of results that already existed, and both were caught late.

---

## What would make this worthless

- A closed form asserted without the prior-art sweep.
- A formula fitted to `../quantum`'s three angles. **That is inference, not verification** — three
  points can be fitted by many wrong functions, and the fit will look excellent.
- A limit "checked numerically" rather than symbolically. Tier 1 is exact or it is not Tier 1.
- Any coefficient extracted from numerical data by fitting a series, without a sweep over the
  nuisance parameter showing the coefficient is stable. **A recent case in this family produced
  three real coefficients and two convincing fictions this way.**
- A citation written from memory.
