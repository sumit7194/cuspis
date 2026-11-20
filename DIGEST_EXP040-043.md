# Digest: the corner-coefficient band seen across spacetime dimension (EXP-040 to EXP-043)

**Status:** reviewed by the Bridge, 2026-11-20 (6ed2893); not ready for outreach (§10).
**Provenance:** human direction: Sumit.
- Fable 5.2, in the side session "Cuspis-personal": the exploratory d-scan; the one-particle decomposition; the
  Stirling prediction of the edge π/(2e); the EXP-043 registration and results; the A1 one-crossing proof (drafted).
- Opus 5.5, in Cuspis-personal: EXP-040 Parts A to C; EXP-041; EXP-042 Part A; the grade wording.
- Opus 5.5, in Cuspis: the EXP-043 addendum A run, its diagnostic, the D-law/S-law reconciliation, and this digest.
- The Bridge: reviews of EXP-041 (the base-rate rule) and of addendum A (the reconciliation, checked by hand).
- Full table: report.md, "Model provenance for EXP-040 to EXP-043".

**Pointers:** report.md EXP-040 to EXP-043 (with addendum A); RESULT.md §10 items (14) to (16); scripts `exp040_*`,
`exp041_*`, `exp042_baserate.py`, `exp043_*`.

## 1. Why it matters

**Scope of the band.** Every 3d CFT whose von Neumann corner coefficient κ has been computed has κ/C_T in
[3.672, 4.179]:
- the free scalar (4.179) and the free Dirac fermion (3.80);
- Einstein holography (3.709); every quadratic or f(R) holographic model equals Einstein (BM15);
- Einsteinian cubic gravity spans 3.672 to 3.747 over its whole allowed coupling range (BCV21), so it stays in the band.
- The large-N Wilson–Fisher model is the one interacting entry: at leading order its entropy equals that of N free
  scalars (WWS17, full text read), so κ = Nκ_free. C_T = N·C_T,free at the same order (argued: at N = ∞ the theory is N free scalars), so κ/C_T is the free-scalar value.
  It is not a separate data point; no 1/N correction to κ is in print.

Bueno and Witczak-Krempa asked why the band is narrow (BWK16 §IX).

This project had shown that the known general constraints do not explain the band; they allow κ/C_T anywhere in
(2.28, ∞). This digest **reframes the question rather than answering it**: the right null is the same theories at
other D. What the work supports (grades in §7), for the free scalar, free Dirac and Einstein continued in spacetime dimension D:
- **(a)** They agree exactly at D = 2 (the anomaly) and end at large D in the reverse order, so pairwise crossings in
  (2, ∞) are forced.
- **(b)** For scalar/Dirac the crossing is forced into (2, 3).
- **(c)** The Einstein-pair crossings land at 2.849 and 2.944, and that location is **unexplained**.
- **(d)** The observed configuration is **non-generic** against a registered toy base rate: 0 of 17 toy curves have all
  their crossings in the window.

The narrow band at D = 3 is the same fact as "the pairwise crossings sit just below 3". So the sharp open question is
(c): why the Einstein crossings land where they do.

Who would care: people working on corner and strip entanglement in CFTs, and on bounds on κ (the free-scalar
extremality conjectures, κ/F₀ bounds).

What changes if it's right: the band of the computed theories is no longer, by itself, evidence for a missing universal
constraint. A proposed constraint would have to explain why it holds at D = 3 but not at D = 4, where the same theories
differ by ×3.3. It says nothing either way about interacting CFTs beyond leading large N.

Already known, as far as our sweep found: the ingredients.
- Free-field κ_D by dimensional reduction, with integer-D tables (CH09).
- Holographic κ and C_T in general d.
- A k/F₀ hierarchy at integer d = 3, 4, 5 (BFGLM26).
- CH09 already notes the one-particle large-d law.

Not found: a C_T-normalised comparison across D, non-integer D, the D = 2 pinning, or the crossings.

## 2. The result, stated carefully

**Hypotheses.**
- κ_D is the strip coefficient (S ⊃ −κ_D·A/w^{D−2}). At D = 3 it equals the sharp-corner κ (CH07).
- Free fields are continued in D through the Casini–Huerta dimensional reduction, using the 2d massive c-functions.
- Einstein is continued through the Ryu–Takayanagi closed form. C_T is continued through the standard free-field and
  holographic formulas; for Dirac, tr 1 = 2 is held fixed, and the ratio κ/C_T does not depend on that choice.
- EMI is a model, not a CFT. Its C_T(d) is our derived formula, 2(d² − 1)(d − 2)κ/π².

**Claim.**
1. Under these continuations, (D − 2)κ_D/C_T agrees at D → 2 for all four curves.
2. The curves cross pairwise exactly once in D > 2:

   | pair | crossing D |
   |---|---|
   | scalar = Dirac | 2.7513 |
   | scalar = Einstein | 2.8487 |
   | Dirac = Einstein | 2.9435 |
   | EMI = scalar | 2.809 |
   | EMI = Einstein | 2.892 |
   | EMI = Dirac | 3.659 |

3. For scalar/Dirac, a crossing in (2, 3) is structurally forced: equal C_T per 2d particle at D = 3, c_S < c_D < 2c_S,
   and the scalar's IR logarithm. Its location is not forced.
   **EMI's role.**
   - EMI is a **test curve**: a model, not a CFT, and not in the band set. Einsteinian cubic gravity, which is in the
     band, was not continued in D.
   - EMI crosses the scalar (2.809) and Einstein (2.892) inside the window. With Dirac it crosses only at 3.659, so at
     D = 3 EMI and Dirac have **not** crossed; there "just past their crossings" does not hold. The two stay within 2.2%
     of each other over (2, 4). That is a second way into the band: never separating.
   - It is **not a counterexample** to a CFT claim, because EMI is not a CFT. It **is** a counterexample to "every
     pinned curve's crossings sit just below 3" as a general rule.
   - EMI was not covered by the base-rate rule, which was adopted after EXP-041, so it counts as neither a pass nor a
     fail of the clustering.
4. Writing each curve as a Mellin transform in D of a profile e(t) with e(0⁺) = ⅓:
   - κ/C_T at D = 3 is the area under the profile, so the band is "equal profile widths to 13%";
   - Einstein's profile vanishes beyond t = π/(2e) with edge exponent 3/2.

**Not claimed.**
- Anything about interacting CFTs. No interacting curve exists. The only von Neumann interacting κ in print is large-N
  Wilson–Fisher at leading order, which equals N free scalars (WWS17); nothing exists beyond that order.
- That the band is explained for theories outside the computed set.
- Why the crossings sit near D = 3; for the Einstein pairs this is unexplained.
- Any upper bound on κ.
- That κ_D at non-integer D is an observable of a physical theory; it is an analytic continuation.
- That π/(2e) is related to the free-field mass scale.
- That the EMI C_T(d) definition is canonical.

## 3. How you could have found it

1. The band is three separate theories, and every constraint we tested fails to localise κ. Three data points
   cannot support a "discovery engine" across theories. So change the axis to one along which all three are computable
   exactly. Spacetime dimension is the obvious one: all three exist for continuous D.
2. At D = 2 the strip becomes an interval, and (D − 2)κ/C_T is fixed by c. So the curves must agree there. The natural
   question: is D = 3 "close to 2", or something else?
3. Scan D. The surprise is that the order reverses: below about 2.75 the scalar is lowest, at D = 3 it is highest. So
   there are crossings, and they sit just below 3.
4. Is a crossing generic after pinning? Test toy pairs: no, only 25% of pinned toy pairs cross at all in (2, 4), at
   widely spread D. *This is a different statistic from §7's "16% per crossing": that one is the fraction of toy-vs-real
   crossings landing inside the window [2.75, 2.95], in EXP-042's ensemble.* So look for structure.
   For scalar/Dirac, the C_T per particle is equal at D = 3, which forces the crossing into (2, 3).
5. Add a fourth curve, EMI, to test the pattern. Before any fifth curve, register a base rate.
6. Ask why each pair crosses exactly once. Write each curve as a Mellin transform in D, and count the sign changes of
   the profile differences. Einstein's transform has a pure power-law decay with phase e^{iy ln(π/2e)} (Stirling), which
   predicts compact support at π/(2e). Check it numerically (partially verified).

## 4. The key idea in one paragraph

The three theories everyone compares are not three separate samples at D = 3. They are three curves in D that are
forced to coincide at D = 2. They drift apart above 2 in one order and end at large D in the opposite order, so they
must cross. They happen to cross between 2.75 and 2.94. Looking at D = 3, just past the crossings, you see them bunched
within 13%. At D = 4 the same theories differ by a factor of 3.3. The right null for "is the band surprising?" is the
same theories at other D, not the abstract range allowed by the constraints.

## 5. Why this target

Alternatives considered on 2026-11-18:
- A discovery engine across theories: three biased points, and the target is a bound. Rejected.
- A proposer–verifier for new inequalities: any tight conjecture is saturated by the free scalar by construction.
  Rejected.
- An interacting κ numerically (Ising): about 200 CPU-years for Rényi-2 alone (KHSM19). Out of reach.
- A ceiling via new constraints: no non-pointwise constraint was in hand.

The D-axis was chosen because:
- the data are free and exact;
- the known answers are published at integer D (CH09);
- the D = 2 agreement is a theorem;
- the first scan took 5 seconds.

What made it doable: Casini–Huerta's dimensional reduction, plus closed forms for Einstein and EMI.

## 6. Physical-meaning check

- **κ_D is the strip coefficient.** It is the corner κ only at D = 3 (CH07, full text read). The digest compares strip
  coefficients across D. It does not compare corner functions at D ≠ 3.
- **Non-integer D is a continuation of formulas, not a theory.** For free fields it is the standard reduction integral
  with t^{D−3}. For Einstein it is the RT strip formula. The D = 2 agreement is a check of the continuation (E4:
  2π²/3 reproduced, with the scalar 0.8% low from its known log approach). It is not physics at D = 2.5.
- **C_T at non-integer D:** the standard formulas. The Dirac trace choice cancels in κ/C_T.
- **Normalisation conventions.**
  - The crossings are invariant under any D-dependent factor common to all curves; for example, the overall strip and
    κ normalisation drops out of the ratios.
  - They would move under a theory-dependent, D-dependent convention. The only such conventions that enter are the
    Dirac trace, which cancels, and EMI's C_T definition, which is flagged below.
  - The relative normalisation of free fields and Einstein is anchored separately at integer D (CH09's table against the
    RT and BFGLM26 formulas), and both reproduce the common D = 2 value 2π²/3 (E4).
- **EMI's C_T** is defined through FLP's planar entanglement density, a choice for a model without a stress tensor. At
  d = 3 it agrees with the corner definition used elsewhere (E3), and it matches published values at d = 3, 4, 5.
- **Profiles are a Mellin device, not a spectrum.** Einstein's D-law profile is not monotone, so it is not a
  c-function. The "edge" is a property of a transform. The failure mode to name: claims about profiles must be claims
  about the curves (zeros in D), never about the profiles' t-structure as physics. Addendum A showed this concretely:
  the two profile conventions give different sign counts in t but the same zeros in D.

## 7. What is checked, and how

| ingredient | experiment | outcome | level |
|---|---|---|---|
| Free-field κ_D table at D = 3 to 6 | EXP-040 B, K1 | PASS (Impl-2, 8/8); Impl-1 as run failed one entry by 0.015%, kept | numerical vs published (CH09) |
| Small- and large-t c-function forms | EXP-040 B, K2/K3 | PASS | numerical vs published |
| Einstein κ_D/C_T formula | EXP-040 B, K4 | PASS to 4·10⁻¹⁶ | certified vs published formulas |
| Crossing dimensions | EXP-040 B | two implementations agree to ≤ 0.0022 | numerical, one physical route |
| Crossings not generic after pinning | EXP-040 C, C1/C3 | control fires; 25% of toys cross | numerical, toy ensemble |
| Scalar/Dirac crossing forced into (2, 3) | EXP-040 C | facts 1–2 checked, fact 3 argued (P3 VOID) | partial |
| EMI C_T(d) | EXP-041 E1–E5 + addendum | PASS at d = 3, 4, 5 after two diagnosed check fixes | derived; numerical at integer d |
| Base rate for a fifth curve | EXP-042 A | 16% per crossing; 0/17 all-in-window | numerical, registered before any curve |
| Profiles, pinning, round trips | EXP-043 K1–K5 | PASS | numerical |
| Einstein edge π/(2e), exponent 3/2 | EXP-043 P1/P2; addendum A3 | PASS outside the edge; inside-edge contour test FAIL as registered | argued (Stirling) + numerical |
| One sign change per pair | EXP-043 P4; addendum A2 | S-law PASS 6/6; D-law FAIL (2 pairs, real); reconciled | numerical + argued |
| One-crossing lemma | EXP-043 A1 | elementary proof | argued |

## 8. What we learned, including our mistakes

- **Surprise:** the order reversal. The first expectation (Fable's) was a monotone drift away from D = 2.
- **A hypothesis of ours failed:** "a crossing near D ≈ 3 is generic after pinning" (Cuspis's guess). The toy ensemble
  rejected it.
- **A link we proposed was withdrawn:** the floor/one-particle link (π²/3 appears in both the one-particle value and the 2.280 floor). It was shared
  normalisation.
- **A side-session test was VOID:** the Rényi test assumed a one-particle term that does not exist at n ≥ 2.
- **Registered checks that failed, kept with diagnoses:**
  - EXP-040 P1, on a noise floor (post-failure restriction, labelled); P3 VOID (the table cannot reach the effect).
  - EXP-041 E4/E5 run 1, on check artefacts (one variable fixed each).
  - EXP-043's main monotonicity check could not fail; a refinement found a 1.6·10⁻⁴ hump.
  - Addendum A: the D-law count FAILED as registered, and is real; the inside-edge test FAILED (quadrature floor times
    amplification).
- **Lesson repeated:** measure the error floor before fixing a tolerance (EXP-039 V3, EXP-043 A3).
- **A novelty claim corrected:** the side session's one-particle closed form is CH09's large-d formula rewritten, so it
  is not new.

## 9. Open items, in order of value

1. **Weakest link (corrected 2026-11-20 after the second-route prior-art sweep; agreed by the Bridge).** The earlier
   wording ("every free-field number rests on one physical route, which a second route would remove") was wrong.
   - For free fields the dimensional reduction is an exact identity: transverse Fourier decomposition into 2d fields of
     mass |k_⊥|.
   - At non-integer D it is the definition of κ_D, so a "route without it" is ill-posed.
   - The real weak points are **(i) the 2d c-functions, which both implementations compute on lattices**, and
     **(ii) the choice of continuation in D**.
   - **Done in EXP-044 (2026-11-20):** both weak points closed for the free fields (report.md EXP-044 results). The
     crossings are verified by evaluation by a lattice route and a lattice-free route; the continuation is unique in
     Carlson's class (argued). Remaining open items move up.
   - *Was:* EXP-044.
     - (i) A lattice-free c-function from the Painlevé V characterisation (Casini–Fosco–Huerta 2005 for Dirac; Casini–
       Huerta 2005 for the scalar), starting with the Dirac/Einstein crossing.
     - (ii) A uniqueness argument for the continuation (Carlson-type growth).
2. π/(2e): structure or numerology? Kill test: deform something it should track.
3. The interacting fifth curve, via 1/N. It is the only route to new physics, and it is expensive. Registered
   rule: base rate first.
4. The Paley–Wiener write-up for the edge, and the zero-counting lemma checked by someone else.
5. The prior-art sweep's holes: citer lists truncated at 250 for three seeds, and the keyword control missed.

## 10. Talk test

- **Can we explain every step, Fable's included?** Mostly.
  - The scan, the pinning, the crossings, the scalar/Dirac forcing and the one-crossing lemma: yes.
  - The edge: we can sketch it. Stirling gives |M_E/(D − 1)| ~ |y|^{−5/2} with phase e^{iy ln(π/2e)} along Re D = const.
    But the step from that to compact support (Paley–Wiener) is not written, and the inside-edge numerical check failed
    at its registered tolerance.
  - We cannot yet explain why the Einstein crossings sit near 2.85 and 2.94.
- **Missing before any outreach:**
  - the lattice-free c-function check (item 1, EXP-044);
  - the Paley–Wiener argument;
  - a fuller prior-art sweep (untruncated citers of CH09, RT06 and Liu–Mezei), and a re-check of the BWK16 §IX
    quotation;
  - a references.md entry for each new source, at stated depth;
  - explicit attribution of Fable's contributions.
- **Not ready.**

## 11. Prior work, at the depth read

- **CH07, CH09:** full text read. CH09 was read for its §"Dimensional reduction" and its κ table.
- **BWK16:** full text read.
- **WWS17 (large-N Wilson–Fisher):** full text read, §II.3.
- **BFGLM26 (arXiv:2604.01436):** TeX source, §§3–4 and App. B, per EXP-040 Part A. *references.md listed it as
  "abstract"; corrected to match the report.*
- **Casini–Fosco–Huerta 2005, Casini–Huerta 2005 (the 2d c-function asymptotics):** read at source for the forms used.
- **FLP16:** abstract only.
- **KHSM19:** abstract and text via a research agent.
- **Ngai et al. (2512.00382):** abstract page only.
- **Metlitski–Fuertes–Sachdev (0904.4477):** title and search summary only.
