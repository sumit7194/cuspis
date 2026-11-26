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
- [x] 2026-11-21: EXP-058. The collapse identity is verified (an exact linear-order identity); the registered must-fail
      could not fire (my error); the post-registration k = 0 control fires. EXP-056's decay wording is corrected:
      D_σ ~ e^{−(½+κ*)ρ}, κ* > κ₀.
- [ ] Before the Σ̃ build: re-read T5b item 2 (the p ≥ 2 terms carry no log) with C₊ linear.
- [ ] Σ̃ build, staged:
      A) inverse Mehler–Fock D_q at n = 1 against the closed form −(2/π)e^{−|q|ρ}(|q|sinh ρ + cosh ρ)/sinh³ρ;
      B) ∂ₙΣ̃(iα, α) at real α, with the C-symmetry check;
      C) growth along α = ½ + iy, with the L·sin²(πα) planted must-fail pre-checked.
- [x] 2026-11-21: EXP-059 stage A PASS. B̃₁ is a Gamma ratio (verified); the inverse-MF-with-subtraction machinery is
      verified; the D₁ position form continues to non-integer frequency (verified).
- [ ] Stage B (pre-register first):
      - ΔD̃ = D̃ₙ − D̃₁^Γ: a decay pre-check in k;
      - ∂ₙΣ̃(iα, α) at real α ∈ (0, 1), with the zero-frequency alternate-branch continuation (EXP-059 design note 2);
      - C-symmetry α ↔ 1 − α as the internal check;
      - UV-cutoff independence as the nuisance.
- [ ] Stage C: growth along α = ½ + iy; the must-fail is a planted L·sin²(πα).
- [ ] **Checkpoint 2026-11-21 ~04:00: the Σ̃ build is paused before stage B.** Resume from report.md "Stage-B instrument
      pre-check, and a checkpoint". Every new pre-registration carries a control table with a pre-check file per
      must-fail (the mechanism for tonight's four registration slips).
- [x] 2026-11-21 morning: resumed on the Bridge's relay of Sumit's word (Opus, stage B then C, no Fable). Inserted
      EXP-060 (the resummation gap: the round-trip spectrum on a = ½ + iy) before stage B. It is cheap, and it tests
      T17's ASSUMED part.
- [ ] Open after EXP-060 (whatever its outcome): C₊ at complex α as an actual resolvent matrix element. It needs the
      near-tip coupling vector in the CFH05 rapidity representation, which I have not derived. The control is Neon's
      Born closed form (T17, unverified) and the α → 0 limit −α/8 (EXP-057, argued).
- [x] 2026-11-21: EXP-060.
      - No resolvent poles on the CH07b line: partially verified, with 1 of 60 points VOID at round-off.
      - The resolvent norm grows ~e^{2πy} (inference), so the norm bound does not close (e).
      - w_S stays polynomial (R3 PASS).
      - The det-sign detector is blind to even crossings (my design error; the κ clause carries R1).
- [ ] **Crux of (e) now:** C₊(½ + iy) as a resolvent matrix element. Derive the near-tip coupling vector in the
      rapidity form. Controls: Neon's Born closed form (T17, unverified) at first order in λ, and −α/8 as α → 0.
- [ ] Stage-B pre-checks (EXP-061 series) found a 2nd T7 continuation gap.
      - Σ̃₁(iα, α) = 0 is a property of the Legendre continuation. The physical twisted family differs by
        D·δG_tw(α) (coefficient verified to 1.3e-5).
      - Next: (i) verify the Legendre on-shell zero; (ii) compute the twisted on-shell value via the finite part of
        Δ's transform.
      - Then re-pose the h₁ framework as f₀ + (n−1)h₁ if f₀ ≠ 0.
- [x] 2026-11-21 (EXP-061 pre-checks 3–4): T7 claim 3 fails in both continuations.
      - In a covariant scheme (argued), Σ̃_tw,1(iα, α) = −2α(1−α)/π² (non-local part verified by evaluation).
      - So f₀ = f(1, α) ≠ 0, and the tip term = d/dn S_{f₀} + S_{h₁}.
      - The crux stays C₊'s growth along ½ + iy, now for both f₀ and h₁.
- [ ] Second implementation of the twisted on-shell total: per-q finite parts plus a zeta-regularised q-sum with
      analytic large-q coefficients. Needed before "partially verified" can become "verified".
- [ ] Re-derive the h₁ framework with f₀ ≠ 0, i.e. Σ̃′ on top of a non-zero n = 1 value. Stage B's target is still
      ∂ₙΣ̃ₙ(iα, α) in the twisted family.
- [x] EXP-061 pre-checks 5–7.
      - The twisted kernel is verified by two implementations (τ-space vs frequency sum, 3e-12).
      - The twisted on-shell total is verified by two routes (2e-6).
      - On the CH07b line, the n = 1 factor grows like y² (verified at y = 0.5, 1, 2).
- [ ] Remaining for Lemma U (e):
      (i) C₊(½ + iy), the crux; waits on the Neon integrands (queued, pending Sumit) or my own rapidity derivation;
      (ii) Σ̃′ (∂ₙ at n = 1, twisted family) growth: the stage B/C build.
          - Plan: image form of the Riemann-sum derivative (argued: UV-finite, since the j = 0 image does not depend on n);
          - the zero-mode term −(1/4π)D₁(α; ρ)ġ;
          - ∂ₙD at fixed frequency via −D̃₁²B̃′.
- [x] 2026-11-21: stage B/C for Σ̃′ (twisted family, EXP-062 series).
      - (II)′ input verified by two implementations to linear order.
      - Σ̃′(α = 0.35) ≈ 0.091 and Σ̃′(½) ≈ 0.130 (±10⁻³, partially verified).
      - On the line, |Σ̃′| grows polynomially (y ≤ 2 full sum; y ≤ 3–4 pieces).
      - The (e) crux is now only C₊(½ + iy). T20 (Neon) is asked for the per-order integrands.
- [ ] y = 3 for piece (I) (running), to test the linear trend.
- [ ] Optional: a full finite-difference two-implementation check of Σ̃′ total (lattice D_n at n = 1 ± δ). It was not
      done; the total currently has a single route.
- [x] 2026-11-21: EXP-065 stage C.
      - |C₊| on the CH07b line does not grow (rate −0.77 on [2, 4], y ≤ 5); G1 PASS.
      - The registered N caught an unconverged t₀ (my ladder design error); the post-registration rerun converged.
      - The blind ratio match (3 constructions) and T23's absolute first-order term were matched at a = ½ and along
        the line.
- [ ] Lemma U (e), open items:
      - an analytic all-y growth bound for C₊ (and Σ̃′);
      - the BIE referee (Neon T25) result, to be checked;
      - re-derive the full δκ tip term with f₀ ≠ 0 (twisted family) for the finite value.

## δκ status 2026-11-21 (after 77f10d0)
- [ ] DECISION PENDING (Sumit, via the Bridge): option (i) cannot give a physical number. The Tier-1/Tier-2 split is
      gauge-dependent: the twist-cut straddle makes ‖X‖ O(1), and the linear and quadratic q=0 pieces cancel there.
      This is argued, and verified on a pure-gauge toy. Options: (ii′) full SC / (iii) integer-n / (iv) write-up /
      (v) Neon theory brief for a gauge-invariant edge representation. Recommended: (v) + (iv).
- [ ] Unverified: Tier-1's L/w coefficient changes with cut placement on the strip (strip vs complement). Needs the
      strip machinery to show.
- [x] Z-factor checkpoint resolved (argued): for a smooth harmonic ΔG the local term contributes 0. The earlier free-entropy
      link was a formal error.

## δκ checkpoint 2026-11-21 (after 3c3d395): HOLD for Sumit
- [x] (v) T31 brief sent; T31 returned (UNVERIFIED). First pass and code read: EXP-073 (its σ numbers use a 2D stand-in
      bubble).
- [x] EXP-073(b): T31's free K1 test. INCONCLUSIVE as registered; consistent with CFH at the few-% level.
- [x] (iv) Write-up `WRITEUP_dkappa_settled.md` (Bridge-read fixes in b32f81b).
- [ ] DECISION (Sumit): how to settle σ-side well-posedness of det(I − K_σ) with the true 3D q-convolved bubble per slice.
      This is the open question for δκ.
- [ ] Optional, only if Sumit wants the free side sharpened: EXP-073(b) Richardson extrapolation with the exponent
      ladder {2a, 1, …}, as a new registration.
- [ ] Not on this box: W = 128 (~15–20 GB). Deferred: the BIE coincident-trace gate (det level).

## δκ status 2026-11-21 (after c49ae29)
- [x] T35 checked (EXP-075). Its ln Λ/w is an artefact of SC's continuation, so SC is WITHDRAWN as complete (argued,
      with cone numbers; 𝒞[c] = −1/32 ties to EXP-062).
- [ ] T36 (Neon): the correct n → 1 continuation of the σ-sector bubble, keeping the inner k-sum. Brief at
      neon_work/dkappa/BRIEF_T36_sector_continuation.md. Check it hard on return (P1–P4, F1–F2).
- [ ] WRITEUP_dkappa_settled.md §7 still describes SC as the route. Update it to "withdrawn (EXP-075)" when the write-up
      is next touched.

## δκ status 2026-11-21 (after dd370c9)
- [x] T36 checked (EXP-076). Its cut-gauge formula is falsified (pure-gauge toy 0.904 + iπ against 0); Neon conceded.
- [ ] Neon T40 (= our BRIEF_T37_admissible_continuation.md; renumbered by the Bridge because T37 exists elsewhere): an
      admissible (strictly sub-Carlson) n → 1 continuation. Check on return: G1, G2, P1 (computed), P2, P3, P4′
      (through the continuation), F1–F3. Standing must-pass: scripts/exp076_puregauge.py.

- [ ] EXP-081b (unregistered diagnostic): pole census for every production geometry: sign-change scan of F(s) = z^W det(I+MC) vs production poles for s <= s_cut (slice p=4 of W4P4 missed s=3.9476 > s_cut; check none is missed below s_cut).

- [ ] Dry runs that set a watchdog cap must run UNDER the watchdog and set the cap from its MEM+CMPRS peak, not from maxrss: either run long enough to see compressed memory level off, or declare measured peak × 1.5 (Bridge, 2026-11-21). Two kills from this slip (EXP-081 r=6; EXP-081b W2P12, 2026-11-21). Apply to the P = 16 night-run re-measure.
- [ ] KPS (arXiv:1105.4598) eq. (71)/(41): δF = −ζ(3)/(8π²) = −0.238 F_s read via ar5iv HTML only — check against the PDF before it enters any write-up (Bridge, 2026-11-22).

## 2026-11-22 (from the R3′ P = 2 grade)
- [ ] Latent overflow in production sigma3d.py:131 (`1/np.expm1(∓2πi n α)` is complex; inf+nan·i once 2π n s > 709.8). Harmless at
      production's n ≈ 1; it bites any n ≥ 709.8/(2π s_max) (W4P2: n ≥ 38). Do NOT patch production mid-referee; a real-arithmetic
      form (as in exp083_armb.kn) is the fix if production is ever evaluated at large n.
- [ ] Port tail grid: tmax = 48/n removes the large-n deviation (verified at 6 n). Any future large-n use of exp083_r3_qcont should
      scale the tail with n; the graded chain stays as run.
- [ ] Slope bound at W4P2 with the n = 1 floor (3.5e-8) gives 0.23 > 0.191. The n = 2 choice is argued, not verified.
- [ ] EXP-081c (post hoc) ρ = 1.86: the (2,4) lattice R is not resolution-stable under one doubling (6.44 vs 2.26–2.65). A refinement series has to be registered separately (amendment D) before the lattice route says anything about the size of δκ.
- [ ] exp081c_analyze R1 cap only forces failure at checkpoints >= the first unconverged node; if no checkpoint is that high it silently does nothing (effect here <= 1e-9 on R48). Fix before any reuse.

## Held for Sumit's scheduling (Bridge, 2026-11-22 13:00; no further runs today)
- [ ] EXP-081d refinement series (draft notes/EXP-081d_refinement_draft.md): k = 1.5, 2.5, 3. k = 3 is ~35 core-h (~9 h on 4 cores).
      Option (a) is the default: production's linear-solve σ̇, plus a C1 FD control at every k. σ-precision budget S₁ = 2.6e4·k³
      (direction-dependent).
- [ ] C2 W4P4 n = 2 residual +4.7e-10, in evaluating Q on the σ ≠ 0 strip. Candidates: Mx/tmax, and the CORRECTNESS of the Arb arm-(b)
      reference (the rerun only shows determinism). Excluded: s_cut, npt, npt0, Mt, aliasing, n·Δld1 precision, σ error.
- [ ] Cross-path tolerance guard (tools/tol_ref.py) and plant guard (tools/plant_guard.py) must be used by every 081d harness.
- [ ] GUARD (Bridge, 2026-11-22): memory estimates scale from a MEASURED full-run peak (nearest geometry, by Ny·N²), never from an
      array-count formula. Two misses today: the 081d draft's "< 0.3 GB at k = 3", and "k = 2.5 ≈ 1.5 GB", which was killed at 2.4–2.6 GB.
- [ ] 081d Stage 2 (Sumit via the Bridge, 2026-11-22): k = 3 as 2 node-split processes in parallel (~6.2 GB each, measured-scaled), ~24 h.
      Gate: Stage 1 ends with k = 1.5 and 2.5 both non-void. Before launch: a short k = 3 probe (no R) to measure the per-process
      peak, then ASK the Bridge for the start time. Caps: soft at the measured peak, hard backstop well above it, pressure-stop on.
      If the measured total > ~13 GB, go back to the Bridge before launching.
      Split: exp081d_route.py --nodes 0:24 (with t0/T_sad) and 24:48, then a final pass for the checks.
- [ ] GUARD: never edit a shell runner while any lane is executing it (zsh reads incrementally and re-entered run_081d_stage1.sh on 2026-11-22). New lanes go in a new file.
- [x] (2026-11-23, slip) The overnight Stage-1 event waiter (bdr3qhptw) could not fire. In zsh, `F="a b c"; cat $F` is ONE filename (no word-splitting), so the baseline and the loop count were both 0 for 11 h. Nothing was missed: no lane failed, and L2b completion was found by its own task notification. **Rule: before arming a waiter, run its condition against a file where it must already be true (a finished lane) and see it fire.** The replacement waiter (b86fo8pz7) was tested that way.
- [x] **DELIVERED 2026-11-23 (Bridge replied; correction 43fbd33). Was UNDELIVERED to the Bridge (not live at 12:55 on 2026-11-23); deliver on return:** "081d Stage 1 end (105e4fe). Stage 1 of 2, no verdict.
  - The k = 2.5 W5P10b10 and W10P10b10 gates all PASS, including C1 verdict_stored, with every plant firing. W10 is capped at s_max 3.948 by Step 0; that is the registered S0 cap, not a void. Peaks are 3.2 GB per process.
  - R(k) for k = 1, 1.5, 2, 2.5 is +2.26, +4.23, +6.44, +8.22, positive throughout, and partially verified.
  - PRIMARY is INCONCLUSIVE, as registered, because k = 3 is missing.
  - Descriptive (argued): the fits leaving out k = 3 predict R(3) of 9.2–9.9. The registered converging/gap boundary sits at R(3) = 9.58, so Stage 2 decides, and the gap is a live outcome. Bands untouched.
  - Asking you now: may I run the k = 3 memory probe (no R, short)? Then please give a start time for Stage 2 (2 node-split processes per width, ~24 h)."
- [ ] **081d Stage-2 launch test (Bridge, 2026-11-23):** peak_k3 = (k = 3 probe peak) × (k = 2.5 full-run peak 3.20 / k = 2.5 probe peak), applied even if the control reproduces ~2.9 GB, because the node probe cannot see the checks phase. Launch only if 2 × peak_k3 <= 13 GB; otherwise go back to the Bridge. Before launch, commit the expected wall time, a 3× check-in bound and a disk estimate, all measured. Disk is 11 GiB free with a 4 GB floor.
- [x] (2026-11-23, slip x2) report.md was left out of two commits (1c274a1, a65851e): a zsh glob no-match and then a nonexistent path aborted the `git add` line, and the commit went ahead anyway. **Rule: add report.md on its own line (`git add report.md && ...`), then check `git diff --cached --stat` includes it before committing.**
- [x] (2026-11-23, slip, caught by the Bridge) Stage 2 was first launched as a Claude-app background task (runner 46264 under zsh 46261 under app process 3453). An app restart or session close would have killed a 62 h run. Stopped it by verified PID at 15:03: census_k3 had finished (16 s, rerun) and Step 0 W6 was seconds in (logs kept as *_attempt0_killed*). Relaunched detached at ~15:04: `(nohup .venv/bin/python -c 'os.setsid(); os.execvp("zsh", ...)' ... &)`, giving runner PID 46956, **PPID 1**, its own session/pgid. macOS has no setsid binary. **Rule: any run over ~1 h is launched detached (PPID 1), and the PPID is checked before reporting the launch.**
- [ ] **Rule (Bridge, 2026-11-23, after the Stage-2 runner omitted CEN):** every registered gate row maps to a runner check. Before launch, list the mapping, one row per line (row -> runner line or "manual, at <time>").
- [x] **STOP route W12P12b12 before it starts** (mechanism armed: tools/guard_081d_w12.sh, PID 56538, PPID 1; tested on a planted log (fires, kills a dummy runner) and a negative log (does not fire)).** run_081d_stage2.sh goes on to it after C1 W6 (~31 h from 15:47, i.e. ~2026-11-24 23:00). It is a flagged geometry. Do NOT edit the running runner. Kill the W12 route by verified PID when it appears, or stop the runner after C1 W6 completes.
- [ ] EXP-081e draft (Bridge items 3(a)–(c)): root cause shown (filters loosened one at a time on p = 7, 10); pole lists identical at every Stage-1 geometry and W6P12b12 after any fix; planted near-double (split 1e-8–1e-7) must read as touch, not miss; test cases must include poles near the filter thresholds.
- [ ] **Tonight, when compute is allowed (Sumit's office use; Bridge 2026-11-23):**
  1. Write `exp085_run.py`, implementing registration 75f1513. Phases: same-lattice FFT check → c n-sweep + KA-IR → planted normalisation (7.045031843543933) → Σσ̇ per Stage-1 geometry (contour-varied precision) → test (i) at k = 1 → R_corr, ρ ± 2σ, reading; plus the must-fail and zero controls.
  2. Verified runner swap (idle runner 75214, cmdline checked): new order 084 → 085 → 081e. 081e body byte-identical; CUSPIS_081E unset for 084/085. Nothing runs beside a route.
  3. Optional after 081e: Σσ̇ at W6P12b12 and W12P12b12 (corrected k = 3 point).

## 084c READ headline: fixed wording (Bridge, 2026-11-24, after 085w2b)
- State the limitation in the headline: no k = 2.5, no n = 3, 4 (amendment 2).
- Level-1 line: "W = Wbox Level-1 residual unexplained but bounded at ≤ 1.1e-9 (in Q); the pole cutoff is EXCLUDED at integer n (tail weight 1/expm1(12π) = 4.2e-17)."
- Production s_cut change: scoped to the n = 1 derivative quantities (d, Q′(1)). Registered separately with its own KA before any route goes.

## 081e W12 (+ 085c GEOM at W6P12/W12P12): awaiting Sumit's word (2026-11-24)
- "Nothing new" is temporary, for Sumit's office hours. The W12 decision is his, later.
- **Revised cost:** route W12 ≈ 39 h (measured route scaling P^5.8, P6 → P10), P⁷ upper bracket ≈ 49 h; ~7.3 GB.
- **Gates agreed with the Bridge:**
  - W8P8 done, and the 084c READ sent to the Bridge;
  - memory green with ≥ 50% free at launch;
  - nothing else of mine running;
  - GEOM points first (≤ 1 h each, CUSPIS_081E=1, missing-ref handling in exp085c GEOM), W12 second;
  - one job at a time, nice 12, inform-only watchdog (NOT run_081e.sh's --stop-on-pressure-warn);
  - timing watch at the 49 h bracket;
  - PAUSE if free memory < 30% (tell the Bridge).
- **The free-memory pause guard must be REBUILT and tested first.** The first draft had a zsh subshell bug (a counter inside `$(...)`) and was removed untested.
- The W6 rerun stays on HOLD.

## Predictions to GRADE when EXP-087 recomputes / k = 3 land (Fable side session; filed before the runs; UNVERIFIED inputs, used only as predictions)
- Δt0 (code − true) at rad 1e-5: W8P8 −0.0201, W10P10 −0.1218 (smoothness hint: up to −0.135), W12P12 −0.0575. Zero at W6P6, W4P8, W5P10, W6P12 (bitwise by construction: no clusters).
  - GRADED 2026-11-25 22:49: W10P10 measured fixed − unfixed = +0.121780 (the prediction −0.1218 matches to 2e-5; the "up to −0.135" smoothness hint is NOT borne out). W8P8 measured +0.020684 (prediction −0.0201: off by 2.7%). There is no independent truth at W10P10 (report.md, EXP-087 recompute). W12P12 is pending.
- Inferred corrected R: 2.2552, 4.2334, 6.5838, 9.0901; R − Y_A slope +0.195 (stored −0.356), ρ_s +0.049. Any A re-read needs a NEW registration. EXP-086 is immune: its n = 2 overshoot is still unexplained.
- k = 3: ORIGINAL sealed R(t0+L)(3) = −1.55 [−2.0, −1.1] (6156a51, expected to fail); REVISED (ca63760): current code −0.07 [−0.60, +0.40]; corrected +0.33 [0.25, 0.42]; E(W12P12) 1.890 ± 0.02; X_Λ 244.958 ± 0.02. Grade BOTH.

## OPEN ITEM (Bridge, 2026-11-25): the A-vs-bulk choice now sits at n = 1
- 2026-11-26: EXP-090 k ≤ 2.5 gives A "supported" (finite-k) and bulk "overshoot". EXP-089 (ii) gives f = +0.212, "A not wrong" (Fable seal PASS). Both are partially verified and neither is a derivation. The Fable brief a457622/a0b6042 asks for the k → ∞ form of Δ_bb; grade its S-a, S-b and S-c seals when they arrive (S-c is gradeable with zero compute from G_W6P12/G_W12P12 plus norm(3)).
- Fable's Q2 ("c(x) is the same at every n") follows (non-author read, EXP-088 (f)). It MOVES the question of which counterterm is right, box c_A versus bulk c, to the n = 1 criterion.
- Fable §2c argues A because "the n = 1 box stays massless" (zero-row-sum self-energy). That is ARGUED, not shown, and it carries the whole A-vs-bulk choice for n → 1 AND n = 2 (EXP-086b's 0.982 rests on it).
- Needs its own argument or test. Do not let it disappear under "Q2 follows".

## W12P12 t0 (EXP-087/090 k = 3 input): was PAUSED 20:09:43 – 20:54:25 for Sumit's office work (2682 s; 0 re-pauses); RESUMED on Sumit's word via the Bridge
- [ ] KA OFF done before the pause: −486.137451254695 against the stored −486.137451254695, diff −4.5e-13, PASS (10622 s). The ON step was ~50 min in when paused.
- [ ] PID 31961 SIGSTOPped by tools/pause_keeper.sh (keeper PID 11269, f21baa9). The keeper re-pauses 31961 if any guard resumes it (freepct_guard 31492, or the watchdog 31955 after its own red or disk pause). Every re-pause logs a RE-PAUSE line in exp081d_results/run_087w12.txt.
- [x] RESUMED 2026-11-26 20:54:25 (keeper exited 20:54:17, no signal; 31961 verified, then SIGCONT; RESUME-OFFICE line in run_087w12.txt). Steps used:
  1. touch scripts/exp081d_results/run_087w12.office_release;
  2. wait until keeper 11269 is gone (≤ 10 s; it logs "release file seen");
  3. verify 31961 (kill -0, argv exp087_t0.py 12 12 -486.137451254695), then kill -CONT 31961;
  4. log a RESUME-OFFICE line in run_087w12.txt and tell the Bridge.
- [ ] When ON prints: report the ON time minus 2682 s.
- Note: the printed ON time "(…s)" and the watchdog's wall time will include the pause. Report the time minus the pause.

## EXP-095 (registered 83566e3, SEALED-READ) — running since 2026-11-26 17:26
- [ ] W2P10 route on the Air (~23 h), then W4P10 (~30 h), serial. Report the measured peak to the Bridge after the first hour.
- [ ] GEOM W2P10 / W4P10 on the Mac mini (run_095_geom.sh).
- [ ] At landing: commit ONLY the sha256 of the 4 outputs to exp081d_results/exp095_sealed_sha256.txt. Do NOT open them, do NOT run exp095_p1.py (it is not written yet; write and commit it without running).
- [ ] Next week: path S (Fable seal, if Sumit OKs) or path D (descriptive). Any accidental view of a P = 10 value is declared at once.
- [ ] EXP-095: W4P10 runs ALONGSIDE in ~/GitHub/fleet-air/corner_function_095b (since 18:27, Bridge OK). When W2P10 ends, the serial runner's duplicate W4P10 is SIGSTOPped by the pause guard. Then ask the Bridge: leave it paused, or end it by PID. Sealed sha so far: G_W2P10, G_W4P10 (bf15796).
- [ ] EXP-095 duplicate end (Bridge-approved procedure). When the 0 GB pause guard fires on runner 27427:
  - verify the watchdog (parent 27427, argv 'exp081d_route.py 4 10 10', kill -0); SIGTERM it, then SIGCONT it;
  - verify the route python (parent = that watchdog); SIGCONT it;
  - check for the STOP rc 98 line in air_run_095.txt; then move the duplicate's W4P10 files to exp081d_results/quarantine_dup_W4P10/ and list them with sha;
  - no pkill; 27427 untouched. The seal covers the Mac-mini G files plus the main-folder W2P10 and 095b W4P10 checkpoints only.
