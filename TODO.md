# TODO — living list

*Open questions, unverified claims, and deferred work. Consolidated 2026-09-05 after EXP-011: nothing
settled is listed here. Settled items live in `report.md` (EXP-001 … EXP-011) and `RESULT.md` §10.*

## RESUME NOTES — 2026-10-18 (HOLD for the Mac restart; everything committed and pushed)

- **State.** No cuspis runs or agents are active. The latest work, all pushed:
  - EXP-030 addendum: the t₄ range is verified at source;
  - EXP-031: tip-fixed corner QNEC adds nothing beyond C3 and is closed under tail addition;
  - the two guards (blind hook on SendMessage, commit-msg overclaim check).
- **Outside the repo.** The three heavy-research prompts (2026-10-17) and the on-hold I-08 Fable brief were
  DROPPED by the user on 2026-11-17. Their folder `fable_briefs/` no longer exists. They were never run, so nothing
  is lost from the record.
- **Open embargo.** `quantum-smallangle-and-C2a-prime` (`tools/EMBARGOES.json`) stays until quantum lifts it.
- **After the restart.**
  - Check that the commit-msg hook still exists in `.git/hooks`.
  - Check that the SendMessage hook loads in the new session (`~/.claude/blind_hook.log`).
  - Ask the bridge for the next item. Low-priority leftovers are the EXP-031 items below.

## Next session — picked 2026-09-23, deferred until the machine is free

All four chosen, in this order of dependence: (1) independent route to a₀ without the ODE solver,
together with the tip-dimension question — DONE as EXP-015 (structural answer; magnitude route replaced); (2) shape-residual
mechanism — DONE as EXP-016 (sharp-end mechanism; smooth end and size open); (3) upper bound on κ versus the pure-Casimir solution — DONE as EXP-017 (closure under dressing); (4) instrument repairs — the M ≥ 14
one-node diagnosis, then the Dirac vertex term against its exact fast check. Items (1)–(3) need almost
no CPU; (4) needs the machine. Housekeeping on the way in: the first item below still asks whether
the residual's sign is universal (answered in EXP-012), and "independence hygiene" belongs under
caveats, not tasks.

## Open — actionable, unowned

*The full ranked backlog, with scores and the 2026-09-23 literature sweep, is `BACKLOG.md`.*

- [ ] **Guards (2026-10-18).**
  - The SendMessage blind hook is verified live (2026-10-18, same session). It blocked a real outgoing draft to the
    bridge that named the sealed S7a statement; the resend without it went through.
  - The embargo `quantum-smallangle-and-C2a-prime` stays until quantum lifts it.
  - The commit-msg overclaim hook is local: reinstall it after a fresh clone (see the `tools/overclaim_check.py`
    header).
- [ ] **EXP-032 follow-up (reading only).** Read Jia 2611.03630 in full. It gives a replica-free n = 1 long-distance
  mutual-information expansion. Check whether it treats the short-distance limit or half-planes; that is the missing
  channel of the two-sided route.
- [ ] **EXP-031 leftovers (low priority).**
  - (α) Vertex-moving QNEC deformations with a controlled tip. The verifier's dimensional argument says these add no
    log constraint; partially verified.
  - The first law / relative entropy as a *completeness* statement: argued only.
  - The Fawzi–Renner characterisation was used from memory.
- [x] **EXP-031 (2026-10-17).** Tip-fixed corner QNEC: the cross-edge SSA term reproduces C3, and the QNEC-only
  inequalities hold for every ρ ≥ 0. So QNEC is closed under tail addition and cannot bound κ/C_T. The t₄ range
  is verified at source (EXP-030 addendum). Reported to the bridge.

- [x] **CF-22 / bridge C17 (EXP-022):** the eye inequalities hold on every curve here; eq. (37) with margins
      of 3 to 4. New theorem: a₀ ≤ 0 at integer n ≥ 2 (corrects EXP-015). Helmes eq. (22) unreliable below
      a few degrees. Next in the bounds chain: CF-24, the cuboid under Casimir dressing.
- [x] **CF-9 / bridge (EXP-025, 2026-09-24).** Outcomes:
  - at n = 1, κ ≥ 2a(π/2) from SSA, so κ/C_T ≥ 2.280 unconditionally;
  - the full rectangle bound reduces to [CH12] conditional positivity (obstruction named);
  - conformal concavity at n = 1 is derived from SSA plus conformal flows (reviewed; EMI check to 10⁻¹⁰);
  - given it, κ ≥ 2.538·a(π/2) and κ/C_T ≥ 2.894.

  Reported to the bridge.
- [x] **EXP-024 (2026-09-24): outcome (a), no bound.** CC plus a₀ = 0, eq. (37) and the θ²-sign do not bound κ/σ
      (explicit family up to 3·10⁴; controls fire; the mode's violation region is probed). The theorem survives with a
      new witness. Open: an all-K analytic proof (the scaling suggests it holds).
- [ ] **C11 (reflected-rectangle positivity at n = 1).** EMI satisfies it exactly (EXP-026 §4; S16), so it cannot
      be the test. The next step is RT rectangles, held by the bridge as a hedge in case V7 finds a gap in S14.
- [x] **C2a′ DONE (EXP-027–029):** the variance half is re-confirmed (A₂ = EMI to 10⁻⁵ at θ ≥ 20°); P1 and P2 hold (trend-based, not blind, free Dirac only); EXP-028 closed inconclusive (instrument-limited). Open: a registered magnitude test. (Original entry follows.)
- [ ] **C2a′ (Dirac cumulant route; bridge-assigned 2026-09-24).** Step 1 is the prior-art sweep, reported to the
      bridge before anything else. If "variance EMI-shaped, higher cumulants = deviation" is already in print for
      corners, the item is settled by the literature. Otherwise pre-register a prediction that can fail, sealed toward
      quantum. EXP-026 item 3(b) stays "unverified, abstracts only" and may not serve as a premise.
- [ ] **Independent second model for O3's step 4.** EMI confirms the n = 1 identity "F(u) − ∫q = tangent line"
      to 10⁻¹⁰. A holographic (Ryu–Takayanagi) check of the same identity would be independent of EMI's
      extensivity. Also: re-derive the EMI reduction formula f′(0⁺) − f′(∞) = C·R, which so far has only been
      re-run.
- [ ] **Rigour for O3.** Assumptions A1–A7 (report.md EXP-025) are physics-standard. For a theorem, A3 (a
      Weyl-covariant regulator) and A6 (shape-differentiability) need an algebraic formulation. Candidate: CMI of
      von Neumann algebras plus the unitary conformal group.
- [ ] **Sharpen the n = 1 κ bound.** Add a₀ ≤ 0 (now n = 1) and [LMW26b] eq. (37) to the EXP-025c intercept
      argument. Small-angle material; keep it out of the quantum copy.
- [ ] **Quantum copy.** Only the bridge-approved general statement (CC holds at n = 1) was added to
      SHARED_BACKLOG_QUANTUM.md. The κ-bound upgrades to S4 are held pending the bridge's decision, because their
      derivation passes through F(0) = κ/4.
- [x] **Bridge job 2:** [BCLM23] positioned in RESULT.md §0 and §8 (κ/F₀ conjecture compatible with the
      theorem; no collapse at all under F₀ normalisation).

- [ ] **The shape residual** (EXP-012, EXP-016). Sharp-end half has a mechanism: the trial function's
      constant is its Lifshitz component's, so for theories without a dimension-1 fusion operator the
      sharp-end residual is ã₀ exactly (ECG a₀ = 0 confirmed out of sample). Open: (a) the smooth-end
      sign, an empirical regularity sign(σ̃′ − σ′) = sign(3π − κ/σ) whose zero is family-dependent
      (ECG ≈ 9.19, Dirac ≈ 9.43); (b) why computed theories sit near the EMI point at all — the same open
      fact as the κ band, since an admissible function with Einstein's σ and κ is 8% off at 45°.
- [ ] **An upper bound on κ** (EXP-013, EXP-017). Every constraint in hand is invariant under Casimir
      dressing 𝒟 → 𝒟e^{E(y+1/y)}, which raises κ at any fixed corner dimension; so any candidate must
      fail to be dressing-invariant. Unchecked: [LMW26]'s cuboid equations and other gluings — test each
      against dressing first. ~~Also open: [LMW26]'s bound at n → 1 is assumed, not proved.~~ Settled by EXP-025 (see below).
- [ ] **Instrument, if anyone re-runs it** (what would make the scalar EE result clean rather than
      corrected): keep the 14-node t-grid on [0, 3.2] (the 10-node grid cost a uniform −1.87·10⁻⁴) and
      the rule dps = 50 + 5M; use M ≤ 13.1. The five masses M ≥ 14 are garbage at 120–125 digits —
      *not* a precision failure; candidates: the series-start convergence (residual not stored in the
      node record — store it), the N = 1.6M + 8 order, δ₀ = 0.01/M. Diagnose on one node
      (M = 14.02, t = 0.03) by varying N and δ₀ separately before any production.
- [x] Dirac EE (EXP-020): a₀ = 0.00 ± 0.02 C_T, prediction confirmed; known answers pass to ≤ 4·10⁻⁵
      from 20° to 170°. Instrument item left: 16 nodes at t ≥ 2.7, M ≥ 11.9 raise a singular starting
      Jacobian (probably branch transitions); measured immaterial (≤ 4·10⁻⁷), not fixed.
- [ ] **Independence hygiene (EXP-014).** `../quantum` holds a file-level copy of this workspace
      including a byte-identical solver, and its repaired a(120°) was accepted against a bound this
      repo supplied. Consequences to carry: never cite their post-repair lattice values as
      corroboration here, and do not source the independent re-implementation below from that copy.
- [ ] **An external check on a₀ and the node** (raised by the bridge): below 45° the instrument is
      refereed only by [HHCWM16] eq (22), to ≤ 5·10⁻⁴ at 20°, 2.6·10⁻⁴ at 26.6°; a₀ and the node
      position live at 10⁻⁴. Routes not through the CHL ODE system: (a) compute the tip-operator
      dimension ∂_nΔ_tip|₁ of the free-scalar twist pair directly from the fusion/strip spectrum
      ([KRS25] eq 10 structure, [CHK24] eq 2.12) — prediction to test: +0.0032 (units of a); (b) a
      second instrument (lattice at small angles with the `../quantum` extraction repaired; or the
      heat-kernel route of [CH07] extended one order past κ/θ). Until one exists, quote the node and
      a₀ with the §0 caveat attached.
- [x] Is the tip constant a₀ a defect-creation dimension? **No** (EXP-015): the twist pair fuses to the
      trivial defect, whose endpoint dimension is zero. A θ⁰ term needs a dimension-1 operator in the
      pair-fusion channel; unitarity does not fix its sign.
- [ ] **Independent route to the magnitude of a₀** (replaces the ∂ₙΔ_tip route, which targeted a
      quantity that vanishes): the coefficient of the marginal bilinears φᵢφⱼ, φᵢ² in the fusion of two
      parallel free-scalar twist lines at n → 1, plus the one-loop beta function of the φ² line coupling
      in d = 3. Decides whether a log θ term exists (b in EXP-015) and fixes a₀. Prior art first: [HMS14]
      twist one-point functions; the free φ² line defect's RG flow.
- [x] Pre-registered Dirac prediction a₀ = 0 exactly: CONFIRMED (EXP-020).
- [ ] **ECG t₄ sign.** [BCV21] Fig. 1 caption pairs μ = +0.00312 with t₄ = +4; [BCR18] eq. 129 gives
      t₄ = −1260 μ f∞²/(1−3μ f∞²), the opposite pairing. Adopted BCR18. EXP-002's obstruction is
      sign-independent; the fermion-side conflict is 3.5% (BCR18) or 1.4% (BCV21). An independent
      t₄(μ) for ECG would settle it.
- [ ] What orders scalar > fermion > ECG(t₄=−4) > Einstein > ECG(t₄=+4) in κ/C_T? Not t₄ (EXP-002).

## Caveats that travel with RESULT.md

- C4 at n = 1 (reflection positivity of the entropy correlation matrices, [CH12]) is a conjecture,
  checked there for free fields to 6×6 determinants. The negative result does not depend on it; any
  positive use of the spectral density ρ(s) would.
- O(N) Wilson–Fisher a₁(π/2)/C_T = 1.36(14), 1.3(1), 1.3(1) ([BMW15], [BWK16]): the Ising value behind
  1.36(14) is not printed in the cited [KHSM13]. *Partially verified.* Carries no information about κ.
- No four-digit free-field a(θ)/C_T exists below 45° (only [HHCWM16] ansatz/lattice pairs, ±1.3% at
  26.6°). The small-angle region is where the theories differ.
- Rényi-2 QMC ([LSZM24], [NCRCLM26]) disagrees with 2013–14 NLCE at 2–4σ; do not cite the old table.
- The Dirac/Rarita–Schwinger "same κ₄, different head" pair (EXP-011) is [AM26]'s statement; the
  edge-mode status of the spin-3/2 entropy was not examined.

## Parked — resume only on instruction

- **EXP-004 instrument** (parked 2026-09-05). Validated: `scripts/exp004_ch_solver.py` (double) on four
  exact smooth-limit coefficients to 7 digits and on published Rényi-2 values at 90°–153°;
  `scripts/exp004_mp.py` (mpmath, 25+3M digits, N-continuation) past the double-precision floor at
  M ≈ 4. Exists: Rényi-2 result to M = 15 (`scripts/exp004_renyi2_result_n24_24_p15.0_t1.json`);
  145 EE checkpoint nodes for M ≲ 1 in `scripts/exp004_nodes/`. To resume: run the known-answer
  controls first (σ = 1/256, s(π/2) = 0.01183, s(3π/4) = 0.002520, κ = 0.0397 for the real scalar —
  each is the [CHL09] Table 1 complex-scalar entry halved (1/128, 0.02366, 0.005040, 0.0794);
  σ = 1/128, s(π/2) = 0.02329, κ = 0.0722 for Dirac), then check smoothness of F in t at fixed M
  (branch flips), then decide the M > 15 tail (contaminates 5° by 8% and 10° by 0.5%; clean from 15°
  up, measured at n = 2). Justified
  only if the shape residual becomes the target.
- Closed form of κ₂^f = (2/π)∫₀^∞ y² u²_{1/4}(y) dy (EXP-011): a Painlevé connection-type integral;
  integrable-systems curiosity; no bearing on the bound.
- Cross-dimensional log-convexity of the free-field κ_d (Mellin moments of one c-function, [AM26]
  eq. 4.17): free-field only; the [CH09] table needed to check it did not survive text conversion.
  Unchecked.

## For the bridge (2026-09-24): report on C17 and the BCLM23 job — DELIVERED by message 2026-09-24 when the bridge returned

Both jobs are done (commit 2554c92; EXP-022 was pre-registered at 1123c1d before any number was computed).
- **C17 / CF-22.** All the known-answer controls pass. Eq. (37) of 2609.04302, which in corner language
  reads a₁ ≤ −κ_n/12, holds by a factor of 3 to 4 in every applicable case. It is dressing-invariant, so it
  is not a route to an absolute bound. ECG concavity is new; the free-field and Einstein checks at n = 1
  repeat the paper's Fig. 2. Helmes eq. (22) is non-convex at 3–4° for the n = 1 fermion, an artifact of its
  constructed tail.
- **New theorem, to carry to quantum:** proven conformal concavity forces a₀ ≤ 0 at every integer n ≥ 2, and
  at n = 1 if it continues. Any precision a₀ quantum produces must respect it. This corrects EXP-015.
- **BCLM23** is positioned in RESULT.md §0 and §8. Its κ/F₀ ≤ 0.6223 is compatible with the theorem. Under
  F₀ normalisation the known κ values span a factor of 2.7, so the collapse is a C_T statement specifically.
- Next in my bounds chain: CF-24, the cuboid under Casimir dressing, unless redirected.

## For the bridge (2026-09-05, EXP-013): the cusp papers are about this object

PHASE2 records `../quantum`'s filing of the 2026 cusp-bootstrap papers as "a different object — cusped
line defects, not entangling-surface corners". In d = 3 the entangling corner *is* a cusp on the
replica twist line defect, and [LMW26] derive corner bounds explicitly (their eqs 35–40:
Γ^{(n)}_twist = (1−n)a_n, κ_n ≥ (2π/3)a_n(π/2), κ_EE ≥ π⁵C_T/144). The filing checked the noun
against the wrong object. The direction they reported (lower bounds) is right. Not modified there;
recorded here for the bridge to carry back.

## Handed off — RESOLVED 2026-09-05 by `../quantum` (their commit `afc7ace`)

> **The bound was right and the lattice was wrong. The corrected value is CONSISTENT WITH the bound
> at the level the method can resolve — not PASS, and not FAIL.** Verified independently by the
> bridge; every figure reproduces.

    bound  a_min(120) = (1/32) log(2/sqrt3)  = 0.0044950     [pi^2 C_T/3 = 1/32 EXACTLY]
    committed      0.0038956   0.867x   13.3% below
    N=1024         0.0043706   0.972x
    N=2048         0.0044650   0.993x
    a(60)          0.0242324 -> 0.0256670  (+5.9%); vs expected 0.0264, was 8.2% low, now 2.8%

    3-param, m->0 extrapolated   0.0044915   0.9992x   marginally BELOW
    4-param, measured m=0.00125  0.0045195   1.0054x   ABOVE
      the two models differ 1.22% like-for-like at that window, and the bound sits INSIDE the gap
      correction to the committed value: +14.6% measured, +15.3% extrapolated

**~~PASS, m->0 = 0.0045099 at 1.003x~~ RETRACTED (`04db813`).** *That extrapolation imported
`r = 3.1` increments-per-halving, measured at the fixed R=4..14 window and carried to the plateau
without being re-measured there.* **The verdict is decided by that constant, not by the data:**

    r=2.0 -> 1.0143x   r=3.1 -> 1.0033x   r=4.0 -> 1.0003x   r=4.56 -> 0.9992x   r=5.0 -> 0.9986x
                                                     the sign flips at r ~ 4.3

**A third plateau point at m=0.005, N=512 — chosen so `xi/N = 0.391` matches the 0.39 of the other
two, so m varies alone at fixed geometry — measures `r = 4.56`, not 3.1.** *With only two plateau
points r was unconstrained.*

> **The deficit falls from 13.3% to 0.08%, into the residual model ambiguity, and that is the whole
> of what measurement supports.**

### Forward guidance from `../quantum` (`6ec989f`) — read this before resuming

    remaining deficit vs the bound       0.0786%
    3-param / 4-param gap, same window   1.2206%
    model ambiguity dominates by         15.5x

> **Pushing m lower CANNOT decide PASS or FAIL, however far it is taken.** The next halving needs
> N = 4096 and would refine a 0.08% term while a **1.22% term sits unresolved.**
> **The limiting factor is the fit model, not the m→0 limit.** What would settle it is a
> better-conditioned extraction — more subleading terms constrained over a longer lever arm in R —
> **not a smaller mass.**

*Their reason for flagging it, which is the part to keep:* **refining m is the intuitive move and it
would be the same error a fourth time — working the axis that is already converged while the
dominant one is untouched.** *That is this study's original defect (uncertainty quoted across
regulators while 61% sat in m) restated as forward guidance rather than as a post-mortem.*

**THE CAUSE, and it was not the short fit window this file proposed.** The extraction needs
`R << xi << N`. The committed run had `Rmax/xi = 0.14` (fine) but **`xi/N = 0.62` — the correlation
length was 62% of the BOX, so the box and not the mass was the IR cutoff and the softest modes went
unregulated.** Varying N alone moves a(120) by 2.3%; varying m alone by **61%**.

*This file's window hypothesis is refuted by the data: extending R makes it monotonically worse —
0.0038960, 0.0030028, 0.0004281, and **−0.0046760**, which is unphysical. The collapse was the clue,
not the answer.*

**A better plateau criterion than either fit alone, found on the way:** the 3- and 4-parameter fits
now **bracket** the answer and converge (5.5e-05 apart and narrowing); the committed pair **diverged**
(0.0038960 vs 0.0035869). *Confirmed on a second angle and shape, because a fix that only repairs the
number it was designed around is not a fix.*

**AND THE FIFTH INSTANCE OF THE CLASS, which is the transferable part.** The study quoted its
uncertainty as the **across-regulator spread, 1.85%** — and all four regulators shared the same N,
the same m and the same fit window. **That control could not have failed.** The real systematics are
orthogonal to it: **61% in m, ~12% in the window, 2.3% in N.**

> **The quoted precision measured the one axis that did not matter.**

**PROCESS DEFECT WORTH CARRYING.** `corner_angles.json` stored only fitted coefficients and never the
raw `S(R)` — so *"what happens if you refit over another window"* could not be asked without a full
re-run. **That is why the diagnosis took four scripts instead of one refit.** Store the raw data, not
just the fit.

*The shape-independence control was sound and is NOT implicated — it constrains the area coefficient,
not the log coefficient. It passed for the right reasons.*

**A correction the bridge owes:** this file cited *"the sibling's README puts the zero mode at ~20% of
B."* **Their README retracts that figure** — the 22–41% number is recorded there as an artifact of the
kernel set, moved 3.5× by one further admissible kernel, and the systematic was renamed
*bulk-coupling* because the mode is identical across admissible kernels by construction. **The
conclusion never depended on it; the number should not be carried onward.**

---

## Handed off — for the bridge, not for this session to fix

- **`../quantum` corner numbers vs the rigorous bound.**
  *The number:* `../quantum/qsim/corner_angles.json` gives, for a real massless scalar on a
  triangular lattice, a(120°) = 0.0038955 (3-parameter fit, mean over four regulators;
  per-regulator 0.003848–0.003920; 4-parameter fit 0.003499–0.003587) and a(60°) = 0.024232
  (4-parameter 0.024746–0.024934); `corner_coefficient.json` / `corner_s6.json` give
  a(90°) = 0.011604 (s=1) and 0.011673 (s=6) on the square lattice.
  *The bound:* for any CFT with finite C_T, a(θ) ≥ (π²C_T/3) log[1/sin(θ/2)] [BWK16] eq (II.2),
  a consequence of a'' ≥ −a'/sinθ (strong subadditivity + Lorentz invariance, [CHL09]) and of
  σ = π²C_T/24 (theorem, [FLP16]). For a real scalar C_T = 3/(32π²), so
  𝔞_min(120°) = (1/32) log(2/√3) = 0.004495, 𝔞_min(60°) = (1/32) log 2 = 0.02166,
  𝔞_min(90°) = (1/32) log √2 = 0.01083.
  *The comparison:* a(120°) is 13.3% BELOW the bound under the 3-parameter fit and 20–22%
  below under the 4-parameter fit; a(60°) passes the bound but is ≈8% below the expected
  value ≈0.0264; a(90°) passes and is 1.9% (s=1) / 1.3% (s=6) below the exact 0.011830 ([CHL09] Table 1 complex-scalar entry 0.02366, halved).
  *Extraction parameters* (`qsim/corner_angles.py`): N = 160, m = 0.01 (ξ = 100, i.e. 0.6 N),
  triangles l ∈ {8,…,28} (3 corners, perimeter 3l), hexagons R ∈ {4,…,14} (6 corners,
  perimeter 6R), fit S = A·perimeter + B·ln(size) + C [+ D/size], a = −B/(number of corners);
  the shape-independence control (A from triangles vs hexagons) passed at < 0.05%.
  *Why the bound is the theorem and the lattice is the suspect:* the bound has no free
  parameter and uses only SSA, Lorentz invariance and C_T; the same code family gives the
  square-lattice a(90°) 1–2% low, and the triangular numbers come from smaller regions (R ≤ 14)
  with a log-fit over ln R ∈ [1.4, 2.6]. Candidate causes, not diagnosed: finite-size 1/size and
  zero-mode (k = 0) contamination (the sibling's README puts it at ~20% of B); the short ln-range
  making B degenerate with C and D. Not modified (read-only).

## EXP-034a follow-ups (2026-11-17; inconclusive scalar, live test)
- [ ] If Sumit wants P3 resolved: dilatation reduction (MI per unit log-scale -> two arcs on S^1 x R, 1D-translation
      invariant Gaussian; thin arcs cheap). Prior-art sweep FIRST (M1). Known-answer control: reproduce EXP-034a's i_G.
- [ ] Alternative: bound Gaussian MI by canonical correlations of smeared fields between thin wedges; try to prove -> 0 for Delta >= 1/2.
- [ ] Not recommended: bigger lattice (eta 0.03 needs ~8 GB, few h, only a factor ~1.7 more in eta).

## EXP-035 follow-up (2026-11-17)
- [x] (done, EXP-036: PASS) Analytic thin-arc asymptotics of I_s for the Delta = 1/2 cylinder symbol: predict C/(ln(1/eta)+b)^2 (C, b from theory),
      then EVALUATE at the EXP-035 points (verification, not a fit).  If it matches, A5' for the free scalar can be
      upgraded from "inconclusive" to "supported analytically + numerically".

## EXP-036 follow-ups (2026-11-17)
- [ ] Derive the O(1/ln) quantum excess (residual 9% -> 6% from 1e-3 to 1e-5, ~0.69/ln(2/eta) by inference) to close steps 1-2.
- [ ] Why is the Delta=1/4 plateau at theta=180 exactly 1/32 (to 6 digits)?  Observation only.
- [x] (done, EXP-037: PASS, 2026-11-18) A5' beyond Gaussian theories (Dirac fermion next: same reduction, fermionic covariance) -- only if Sumit wants it.

## EXP-037 follow-ups (2026-11-18)
- [ ] A5' for an interacting CFT (e.g. large-N / holographic sector MI of 1511.00244 gives zero at O(N^2) for thin sectors?
      check what is known at O(1)); this is the step that would matter for 2.894 beyond free fields.
- [ ] Note: the n_p gate passed at 1.93% (near the 2% line); a 256-cell run would tighten the Dirac coefficient check.

## EXP-038 follow-ups (2026-11-18)
- [ ] Cancellation-free Gaussian MI (relative entropy via log1p of near-identity dets) to resolve Delta = 0.9 at eta <= 1e-4 (EXP-038 Part C void there).
- [ ] O(1) holographic correction to the thin-sector MI (bulk MI between thin entanglement wedges) -- argued only.
- [ ] Block-sum step of the general argument (Cardy pairwise law summed over a thin strip) -- the one argued link for interacting CFTs.

## EXP-039 HOLD (bridge, 2026-11-18 night)
- [x] DONE 2026-11-18 (run 3, PASS; report.md EXP-039). Was: HOLD until the bridge's morning check (~8 AM): Quantum's approved G3 worker (PID 6018, ~4.4 GB) must not be pushed
      into pressure yellow, because a stopped G3 task is not retried.  Then relaunch `scripts/exp039_mp_mi.py` under the
      watchdog with --cap-gb 2.5 (other guards as before), only with pressure at level 1 and the bridge's go.
      V1 and V2 already passed (run 1); the run restarts from validation (no checkpoint yet).

## EXP-039 follow-ups (2026-11-18)
- [ ] Input-rounding floor: computing the X, P rows in mp (not double) would remove the ~2e-16 floor in I_s. Not needed at
      η ≥ 1e-5 (floor/i_G ≤ 4.3e-4 at n_p = 32), but it would be needed for Δ = 0.9 at η ≤ 1e-6.
- [x] Prereg wording: "input rounding does not matter" was only approximately true (EXP-039 run-2 diagnostic). Checked
      2026-11-18 (Cuspis-personal): the argument appears only in EXP-039's prereg (report.md, "Why rounding the inputs does
      not matter") and its own correction. EXP-034–038 make no insensitivity claim; EXP-038 already records its double
      floor as noise. Nothing else to correct.

## HANDOVER 2026-11-18: work continues in the session "Cuspis-personal" (Sumit's other account, Opus 5.5)
This session (Cuspis) stops here. Plan agreed with Sumit, to be done in Cuspis-personal:
- [x] 1. Prior-art sweep (M1) — DONE, EXP-040 Part A: outcome (B).: has κ_d/C_T (strip coefficient) been compared across dimensions d for free scalar, free
      Dirac and Einstein holography? If known, cite it and move on.
- [x] 2. Make the d-scan solid — DONE, EXP-040 Part B: crossings 2.7513 / 2.8487 / 2.9435, partially verified.: a second implementation (different method) of notes/fable/dim_spread.py's κ_d/C_T scan, the
      d = 4 values checked against source, then register it as an EXP in report.md (pre-registration first).
- [x] 3. Generic-crossing test — DONE, EXP-040 Part C: not generic; S/D crossing in (2, 3) forced, location dynamical.: do toy pairs pinned at d = 2 with different c(t) shapes cross at d − 2 = O(1)? If yes,
      the band of the three known theories needs no further explanation.
- [ ] 4. Decide afterwards (Sumit): interacting theories (Ising / O(N)) on or near the crossing. Expensive; lattice or
      tensor-network numerics.
- [x] Side item (EXP-039 follow-up above): done 2026-11-18, not used elsewhere (see the EXP-039 follow-ups).
- notes/fable/ (sections 1–6; committed with EXP-040, folded into report.md with attribution) holds the d-scan, the π²/3 one-particle decomposition (verified by hand
  in Cuspis) and the withdrawn floor/π²/3 link. Fold it into report.md with attribution when registering step 2.
- scripts/exp034a.pid is a stale untracked leftover; safe to delete after a look.

## EXP-040 follow-ups (2026-11-18)
- [ ] Sumit decides: interacting CFT relative to the crossings (handover item 4), or the cheaper EMI fourth curve first
      (EMI pinned to the free fermion at D = 2; its general-d C_T must be read at source before registering).
- [ ] P3 (the scalar's log making r_SD dip at D → 2⁺) is argued only; a continuum evaluation of c_S to t ~ 1e-30 would
      test it.
- [ ] The two Einstein crossings (2.849, 2.944) have no structural account.
- [ ] Bridge offer (2026-11-18, on receipt of EXP-040, logged 978b97c): a separate check by a route that avoids the reduction (unverified until run),
      direct D = 3 and D = 4 lattice values without the dimensional reduction. Not requested yet; Sumit's call. The Bridge
      agreed the grade "partially verified". An Ising/O(N) run would need a slot request with measured cost first.
- [x] EXP-041 (2026-11-18): EMI as a fourth curve. C_T,EMI(d) = 2(d^2-1)(d-2) kappa/pi^2 (partially verified). EMI crosses
      scalar at 2.809, Einstein at 2.892, Dirac at 3.659 (EMI/Dirac within 2.2% on (2, 4)).
- [x] EXP-041 E5 at d = 4, 5: PASS (addendum A). C_T,EMI verified at d = 3, 4, 5; partially verified for continuous d.
- [ ] BINDING before any fifth curve (Bridge rule, adopted 2026-11-18, report.md EXP-041): register the prediction "its
      crossings with the four fall in [2.75, 2.95]", the toy-ensemble base rate for that window, and what counts against.
- [x] EXP-043 (2026-11-18): mass profiles. Einstein's profile has a sharp edge at t = pi/(2e) (edge exponent 3/2); every
      pair of profiles crosses once, so each pair of curves crosses exactly once in D > 2 (partially verified).
- [ ] EXP-043 follow-ups: read the zero-counting theorem (Karlin, Total Positivity) at source; write the Paley-Wiener
      argument for compact support; is there a reason the holographic edge pi/(2e) = 0.578 sits at the free-field scale?
- [ ] Interacting route (EXP-042 Part A) parked 2026-11-18 by this session's judgement: B and C are multi-session, low odds;
      D out of reach. Still Sumit's call.

## PAUSE 2026-11-18 (Cuspis-personal, Opus 5.5): work returns to the "Cuspis" session on the other account
Everything is committed and pushed. Nothing is running. Where things stand:
- EXP-040 to EXP-043 are done and reported to The Bridge; model provenance table in report.md (5033cb6).
- **Next, ready to run:** EXP-043 addendum A (registered 687d739 + 115bb50). Run it only at memory pressure green:
      nice -n 12 .venv/bin/python scripts/tools/watchdog.py --log scripts/exp043_addA.wd.log --cap-gb 1.5 \
        --min-disk-gb 5 --stop-on-pressure-warn -- .venv/bin/python scripts/exp043_addA.py > scripts/exp043_addA_output.txt 2>&1
  Expected a few minutes and < 0.2 GB. Then write A2/A3 results against the registered criteria, regrade EXP-043,
  and tell The Bridge (it asked for the lemma check and for the model to be named in each commit message).
- Open choices for Sumit: the interacting route (EXP-042: B = 1/N, C = epsilon-expansion; D out of reach); EXP-043
  follow-ups (Paley-Wiener write-up; why pi/(2e) sits at the free-field scale); the Bridge's offer of a check without
  the dimensional reduction.

## 2026-11-20 (Cuspis session, Opus 5.5): EXP-043 addendum A done
- [x] Addendum A run (bridge GO, 106 s). A2: K PASS; count and end signs FAIL as registered, in the D-law only
      (Dirac/Einstein and Einstein/EMI each change sign twice; diagnosed as genuine). The S-law passes all six pairs.
      A3: outside PASS, inside FAIL (amplified quadrature floor; converges with a finer contour, not demonstrated at 1e-7).
      One crossing per pair survives via the S-law (both laws share zeros in D): a post-failure argument. Results in
      report.md; RESULT.md (16) corrected.
- [ ] Optional: register an A3 re-run with the y-step set from the measured ~1e-11 floor, and an A2 count down to t = 1e-6
      in both laws.
- [ ] Open choices for Sumit unchanged: interacting route (1/N or epsilon-expansion); why π/(2e) sits at the free-field
      scale; the Bridge's offer of a check without the dimensional reduction.

## 2026-11-20 evening (Cuspis, Opus 5.5): the δκ (O(N⁰) strip coefficient) line, parked for Sumit's decision
- [x] EXP-044 lattice-free crossings (done); EXP-045 π/(2e) dropped; EXP-046 holographic couplings: largely known;
      EXP-047 1/N note; EXP-048 groundwork (a), the reading.
- [ ] Groundwork (b), only on Sumit's go (the Bridge's suggested order):
      1. read MFS09's surface-coupling β-function (eqs. 40–55) and the n → n* vs L → ∞ non-commutation at source; it
         was summary-depth for the large-N section;
      2. half-space first: reproduce MST15's double-trace one-loop formula, and pin down the ν ≥ ½ divergence (a
         replica instability, a regulator or boundary-condition artefact, or the alternate-quantisation edge);
      3. only then the strip: does the pathology reach the universal 1/w^{D−2} term? If not, that is the argument the
         strip needs; if it does, the naive GFF difference is dead.
- [ ] Fable, only if (b) gets stuck and Sumit asks, in the personal account. Working folder
      /Users/sumit/Github/fable_work/corner_dkappa/ (outside every repo); BRIEF.md reviewed by the Bridge; statuses
      SURE/CHECKED/UNSURE/LIT; verification under our own prereg and our own code. Never launched from cuspis on the
      office account.
- [ ] Digest §10 still open: the Paley–Wiener write-up for the edge; untruncated citer sweep (CH09, RT06, Liu–Mezei).
- [ ] δκ plan after EXP-049 (the Bridge's order, 2026-11-20; awaiting Sumit's go):
      1. Opus: (i) the first-order-in-(n−1) formula ∂ₙ log det Bₙ|₁ = Tr(B₁⁻¹ ∂ₙBₙ|₁), with ∂ₙGₙ|₁ as a modular-flow
         insertion. GATE: the same formula on the sphere (via CHM) must reproduce δS = +ζ(3)/(8π²). If it fails, the
         mismatch identifies the contact terms, and that becomes the sharp Fable question.
      2. Opus: (iii) the UV subtraction isolating L/w, with the n = 2 numerical cone test and a convergence study
         (floor first).
      3. Fable (personal account, only if Opus cannot settle it): (ii) prove that the irrelevant surface operator
         stays out of the universal term, or find a counterexample, with the sphere-validated formula inline in the
         brief.
- [x] 2026-11-20 late (Cuspis, Opus 5.5): δκ step 1 (EXP-050: formula; sphere gate PASS for conventions only; two plan
      corrections accepted by the Bridge; MFS09 numbers read at source). Step-2 foundation EXP-051: twisted lattice
      solver reproduces the Fredholm w at 6 points (partially verified; sign amendment labelled; must-fail FAIL as
      registered at 5.9 vs 10 tol).
- [ ] δκ next (when Sumit resumes):
      (a) design a feasible strip-trace formulation: the dense lattice route needs ~11 GB per propagator, so it is
          infeasible;
      (b) the floor-first log test registration (Bridge: ≥ 2 decades, minimum detectable log stated, outcome tree with
          both branches informative);
      (c) (ii) as a defect-OPE statement: why the Δ̂ = 1 channel's coefficient vanishes for free fields (the strip κ
          is finite), and whether that survives at O(N⁰). This is the candidate Fable brief. **Fable only on Sumit's
          explicit word; never from this account.**
- [x] 2026-11-21 (Cuspis, Opus 5.5): EXP-052, an outside referee pass (Gemini 4 Neon, via the Bridge) on the crux.
      - Cone coincident-propagator shift verified by evaluation (−π/8, +π/6 to 2·10⁻²⁰). The gap-equation closure
        reproduces MFS09's α′(1) = −1/4.
      - **EXP-049 §3 / EXP-050 (i) justification was wrong:** the saddle acts at O(n−1) via the m = 0 exponent.
      - The formula survives for the universal term (argued: the saddle enters as a flat UV tadpole × w-independent ∫μ).
      - The free-field puzzle is resolved (k = 0 sector decouples).
      - Crux reframed by the MI argument: δκ is a pure number; the question is replica/ε-limit commutation.
- [ ] δκ next, updated by EXP-052 (supersedes (b) and (c) above where they differ):
      (a) the feasible strip-trace formulation. Candidate: the referee's bipolar (x, τ) grid at fixed k_y, needing an
          own cost estimate at Tier 1 first;
      (b) register the log test as a **replica-limit commutation test** (floor-first; a detected log is a finding about
          the method). Adopt the physical must-fail control: an n-independent defect mass must produce a log;
      (c) the open Fable-grade question is now: does the cone (angle-rescaling) continuation of ½Tr(B₁⁻¹∂ₙB̃ₙ) equal
          the true n → 1 limit (the referee's q ≠ 0 caveat)? **Fable only on Sumit's explicit word; never from this
          account.**
      (d) unverified referee items: ∫d²x_⊥ μ_total = 0 (not needed for §3), and α₂ = −0.165146553846 (own check
          optional).
- [ ] 2026-11-21: HOLD on any Fable brief for EXP-052 (c) (Bridge): Neon is working the q ≠ 0 / continuation caveat
      in the same session; wait for its result (the Bridge relays it), then do the Opus-first pass. The Bridge
      accepted EXP-052's scale-invariance argument over ∫μ_total = 0.
- [ ] 2026-11-21: Neon follow-up on the q ≠ 0 caveat received (Bridge summary outside the repo; UNVERIFIED). To do
      when resuming, in the Bridge's order:
      1. Verify the claimed collapse identity by algebra first:
         T_n^(1) = ½Σ_q Tr[(B_cone^(q))⁻¹Δ_strip B^(q)] = 2Σ_{k=1}^{n−1} Tr(Σ_{φ,n}^{cone,(k)} Δ_strip G^(k/n)), up to
         UV-finite ΔG·ΔG terms, using Δ_strip G^(0) ≡ 0.
         Also check its premise that only the linear trace can carry log(w/ε), since p ≥ 2 terms need Δ̂ ≥ 1.
      2. Then the single-cone lemma on Opus: is Σ_{φ,n}^{cone,(α)} uniform as (α, n) → (0, 1)? If it sticks, it is the
         Fable brief, on Sumit's word only.
      3. **Bears on EXP-050 (i):** Neon claims global angle rescaling FAILS on the strip (bipolar coordinates give n
         separate infinities). If true, EXP-050's θ̃ = θ/n step holds for the single cone only, and the strip formula
         must go through the q-sectors. Check this before relying on EXP-050 (i) for the strip.
      4. Neon's numerics (w/a ≤ 8, n = 2–4; no ln w growth after a tadpole subtraction; defect-mass must-fail fires
         at ~50× the step size) are indicative only. No n → 1 extrapolation was done.
- [x] 2026-11-21: EXP-053: own cone gap equation reproduces MFS09 Table I (all four) and α′(1) = −¼; it agrees with
      Neon's α₂ to 10 digits. Assessment of Neon's T7 (Lemma U) gaps recorded in report.md.
- [ ] Lemma U, still owed (each needs pre-registration):
      (1) a direct near-tip extraction of C₊(α) on the EXP-051 twisted lattice. Prediction O(α²). Must-fail: a
          single-edge (half-line cut) run, where the O(|α|) term should be present;
      (2) the ω_q ≠ 0 sum (Gap c): the only piece with neither a computation nor an argument;
      (3) a write-up of the contour continuation for Gap (e): the reduction to (a)+(b)+strip analyticity of g.
      Fable brief only if (2) sticks, and only on Sumit's word.
- [x] 2026-11-21: EXP-054 (gap b, lattice) ran. All registered checks FAIL, diagnosed as lattice analyticity: G is even
      and analytic in α on any finite lattice, and the continuum |α| law needs α ln(r/a) ≫ 1. The run is
      uninformative on (b), and the must-fail caught it. Pre-registration arithmetic slip recorded.
- [ ] (b) redesign, to pre-register:
      - continuum-first (lattice r → ∞ at fixed α ≥ 0.15, with the exact mode-sum S(α) as known-answer); or
      - better, the Fredholm route: O(sin²πα) at fixed t, plus the k_y → 0 crossover bound O(e^{−1/α}).
      Then (c).
- [x] 2026-11-21: EXP-055 (gap b, Fredholm). Registered P1/P2 FAIL: tolerances ignored the O(α) dependence of θ, a
      rule-VIII lapse. The must-fail fires. Post-registration closed form: W₃⁽¹⁾/λ² = −(π/2)Γ(½+2α)Γ(5/2−2α)
      (verified, 3 routes). The full W₃ approaches it (residual 3.6% → 0.11%), so W₃/α² → −3π²/8: the integrated (b)
      holds (partially verified). The near-tip C₊ is still owed and needs a continuum method.
- [ ] Gap (c), the ω_q ≠ 0 sum: scope it next. It needs the σ propagator on H² × S¹ in twisted sectors.
- [x] 2026-11-21: EXP-056. Gap (c): no zeros of B̃ₙ(k, q) in the strip below threshold at 8 (n, q), so the uniform gap
      holds with an O(n − 1) loss (partially verified). The EXP-055 closed form passed as a registered prediction.
      Three instrument-bug runs are kept (memory, k = 0 corner, overflow).
- [ ] Lemma U remaining:
      (1) a direct near-tip C₊(α), by a continuum method;
      (2) a write-up of (e)'s CH07b contour continuation;
      (3) optional: (c) at q ≥ 3 and n → 1.01;
      (4) check Neon's (a)–(e) reply against EXP-053–056 when it lands.
- [x] 2026-11-21: EXP-057 (Neon T10).
      - (b): reconciled; C₊ is linear (argued), and the EXP-055 scope sentence is corrected.
      - (e): Neon's general S_h(1) = 0 claim is false as stated (counterexample sin²(πα)); its prototype closed form is
        wrong, but there is no log; the ζ(2) aside is verified.
      - Crux sharpened: the first-order tip term is log-free iff h₁ obeys the Abel–Plana growth bound o(e^{2π|Im α|})
        uniformly in L.
- [ ] Next for Lemma U:
      - the growth of Σ̃′_{φ}(iα) along Im α, which needs the σ self-energy machinery (EXP-056's B̃ plus D_σ = 1/B̃
        convolved with twisted G). This is a candidate compact Fable brief, on Sumit's word only.
      - Optional: a numerical continuum check of C₊ = −|α|/8.
