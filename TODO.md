# TODO — living list

*Open questions, unverified claims, and deferred work. Rule IX: this file is as important as the
report, because it is what stops an open question from quietly becoming a settled one.*

## Before any derivation

- [ ] **M1 prior-art sweep.** What is known about a(θ) for the free scalar, by whom, with
      identifiers. Report before deriving.
- [ ] **Verify the θ → π limit** claimed in `TASK.md`: the quadratic form, the σ = C_T·π²/24
      relation, its numerical factor, its conditions. *Stated from recollection, unverified.*
- [ ] **Verify the θ → 0 limit**: the κ/θ form and κ's value for the free scalar. *Same.*
- [ ] **Attack the premise.** Is a closed form already known? If yes → outcome E, report and stop.

## Verification infrastructure

- [ ] Build the Tier-1 symbolic limit checker before building anything else.
- [ ] Validate it in BOTH directions: it must reject a deliberately wrong candidate as well as
      accept a correct one. *A checker that has only ever said "no" has not been shown able to say
      "yes" — see `../conjecture_machine` RESULTS.md §127.*
- [ ] Establish which structural constraints (positivity, monotonicity, convexity, reflection)
      actually hold, with sources, before using any as a Tier-2 gate.
- [ ] Pull `../quantum`'s a(60°), a(90°), a(120°) with their across-regulator spreads under both
      the 3- and 4-parameter fits. Record the numbers and their provenance here.

## Unverified claims

*Nothing yet. Every claim entering `report.md` gets a line here until it is graded `verified`.*

## Deferred

*Nothing yet.*
