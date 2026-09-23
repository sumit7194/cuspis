# Corner-function backlog — a shared map for all sessions

*From the `corner_function` (cuspis) workspace, 2026-09-23. Written to be read by other sessions and
people without opening anything else in this repository. Its purpose is that parallel sessions working
on this problem complement each other and do not contradict each other.*

**How to use it.** Items carry stable IDs **CF-1 … CF-25**. If your session made its own list, map your
items onto these IDs rather than renumbering; add genuinely new items under your own prefix (for
example QU-1 for `quantum`). Section 1 is the vocabulary every number should be stated in. Section 2 is
what is already settled, with its status. Section 3 lists traps that have already cost real time.
Section 5 ranks the items and Section 6 describes each one. Section 7 says which items check each other,
so that two sessions can aim at the same quantity by different methods on purpose, not by accident.

**Nothing here assigns work.** Section 7 also suggests fits by repository; the user and the bridge decide.

---

## 1. Shared conventions — state every number in these

| Quantity | Convention | Source |
|---|---|---|
| a(θ) | Coefficient of −log(perimeter/δ) in the entanglement entropy, **per corner** of opening angle θ. Some papers quote the sum over four corners of a square; divide by 4. | Casini–Huerta 2007 (hep-th/0606256) |
| C_T | Stress-tensor two-point normalisation: 3/(32π²) per free real scalar, 3/(16π²) per two-component Dirac fermion, 3L²/(π³G) for Einstein gravity in AdS₄. | Osborn–Petkou convention, as in Bueno–Myers–Witczak-Krempa 2015 |
| σ | a(θ) → σ(π−θ)² as θ → π. **σ = π²C_T/24 is a theorem.** | Faulkner–Leigh–Parrikar 2016 |
| κ | a(θ) → κ/θ as θ → 0. Equals the coefficient of −κL/w for a long thin strip. | Casini–Huerta 2007 |
| a₀ | The constant in a(θ) = κ/θ + a₀ + a₁θ + … | this workspace |
| Rényi twist parameter | Free fields reduce to sectors with boundary phase e^{2πia}, a = k/n. **Bosons: k = 0 … n−1. Fermions: k = −(n−1)/2 … (n−1)/2.** So at n = 2 the scalar has a = ½ and the Dirac fermion a = ±¼. | Casini–Huerta–Leitao 2009 (0811.1968) eqs. (6), (7), (12), (13) |
| Cusp language | Γ⁽ⁿ⁾(θ) = (1−n)·a_n(θ): the corner function is the cusp anomalous dimension of the replica twist line. | Lanzetta–Moult–Wang 2026 (2609.04041) eq. (35) |
| Real-scalar reference values | σ = 1/256, s(π/2) = 0.01183, s(3π/4) = 0.002520, κ = 0.0397 are the **complex-scalar** entries of CHL09 Table 1 **halved**. Dirac: σ = 1/128, s(π/2) = 0.02329, s(3π/4) = 0.005022, κ = 0.0722, unmodified. | 0811.1968 Table 1 |

**Measured κ/C_T:** free real scalar 4.179; free Dirac 3.8005; Einstein holography π²Γ(3/4)⁴/6 = 3.709;
all quadratic and f(R) bulk actions identical to Einstein; Einsteinian cubic gravity 3.672–3.747 over its
causality-allowed coupling range, at first order in the coupling. **The band is [3.672, 4.179].**

**Normalisation warning.** Ratios change order when divided by the sphere free energy F₀ instead of C_T.
The EMI model's κ/C_T = π³/8 ≈ 3.876 sits inside the band. Its κ/F₀ = 1/π sits *below* the Dirac fermion's
0.3297 (Bueno–Casini–Lasso Andino–Moreno 2023, 2307.05164). Always name the normaliser.

---

## 2. Settled — build on these, do not re-derive them

Status words: **proved**, **verified** (checked against sources or exact results), **measured** (this
workspace's numerics, with the stated caveat), **conjectured**.

| # | Statement | Status | What would reopen it |
|---|---|---|---|
| S1 | No constraint in the known general set (purity, strong subadditivity, strong subadditivity with Lorentz invariance, reflection positivity, the two limits) bounds κ/C_T above. Every κ/C_T in (0, ∞) is admissible, and a(θ)/C_T is unbounded above at every angle. | proved; independently re-derived by `quantum` with its own code | A general constraint missing from that set. The set's completeness is a literature claim, not a theorem. |
| S2 | The collapse, to ≈1%, is the statement κ/C_T ∈ [3.672, 4.179]; the ≈1% shape residual is a separate fact. | verified | — |
| S3 | Theories with equal t₄ differ in κ/C_T by up to 11.5%, so ⟨TT⟩ and ⟨TTT⟩ data cannot order the band. | verified | — |
| S4 | The only known "second channel" is Lanzetta–Moult–Wang's rectangle of twist lines. It gives κ_n ≥ (2π/3)·a_n(π/2), which together with a(π/2) ≥ (π²C_T/3)·log√2 (Bueno–Witczak-Krempa 2016) gives **κ/C_T ≥ 2.39 at n = 1, assuming their bound continues to n = 1.** | proved at integer n ≥ 2; continuation assumed | A proof at n = 1 (CF-9). |
| S5 | **The rectangle bootstrap can never bound κ above.** Multiplying any admissible solution by e^{E(y+1/y)}, E ≥ 0, keeps it admissible, with the same corner dimension and a larger Casimir energy. | proved (two-line proof, numerical check with a working control) | — |
| S6 | Local thin-wedge physics contributes only odd powers of θ. The twist line fuses with its reversal to the trivial defect, so the tip contributes nothing. Hence **a₀ ≠ 0 requires a dimension-1 operator in the twist-pair fusion channel.** The general exponent θ^{2(Δ−1)} for identity fusion is **prior art: Lanzetta–Moult–Wang, "Eye-opening bounds on cusps", 2609.04302, eq. (28)**. The application to twist lines is this workspace's. | derived; exponent is prior art | A dimension-1 operator where none is expected, or a θ⁰ term without one. |
| S7 | a₀ by theory: Einstein 0 (exact curve, four digits); ECG 0 (five digits, four couplings); **Dirac 0.00 ± 0.02 C_T** (pre-registered prediction, confirmed; the error comes from κ's third digit); free real scalar at n = 1 ≈ −0.3 C_T; free real scalar at n = 2 −0.24 ± 0.03 C_T. | measured | For the scalar, see S8. |
| S7a | **a₀ ≤ 0 is a theorem at integer n ≥ 2** (and at n = 1 if conformal concavity continues): a constant in Γ adds α√u to ℰ, whose second derivative −α/(4u^{3/2}) dominates as u → 0, so the proven concavity of 2609.04302 forces α = (1−n)a₀ ≥ 0. All measured values agree. This corrects this workspace's earlier claim that the sign is not fixed. | derived from a proven theorem (added 2026-09-24) | — |
| S7b | 2609.04302 eq. (37), in corner language **a₁ ≤ −κ_n/12** when the lightest fusion operator has Δ > 3/2, holds for Einstein (factor 3.05), ECG (2.97–3.13), Dirac n = 1 (3.6–3.9) and Dirac n = 2 (4.1). Conformal concavity holds for all these curves and for ECG, a theory the paper did not test. Far from saturated; dressing-invariant, so not a route to an absolute bound on κ. | verified (added 2026-09-24) | — |
| S8 | The free scalar's a₀ is **model-dependent by a factor of about 1.5.** −0.32 C_T without a log θ term and −0.48 … −0.57 C_T with one; the data from 20° to 70° cannot tell them apart. Its sign is robust. | measured, with caveat | CF-13 or CF-18. |
| S9 | The (σ, κ) trial function's constant comes entirely from its Lifshitz component, so for theories with no dimension-1 fusion operator the residual at θ → 0 equals that constant exactly. Imposing a₀ = 0 improves the Dirac fermion 3 to 15 times and makes the scalar 10 to 100 times worse. | derived and verified | — |
| S10 | The free scalar's residual changes sign at **27 ± 3°**. | measured | Below 45° the values are refereed only by one published formula (Helmes et al. 2016, eq. 22); see CF-12. |
| S11 | "Fixing σ and κ leaves little freedom" is **not** a consequence of the constraints. An admissible function with exactly Einstein's σ and κ differs from Einstein by 8% at 45°. The trial function's ≈1% accuracy is an empirical property of the theories computed. | verified | — |
| S12 | The Dirac and Einstein values of the thermal coefficient over C_T agree to 4·10⁻⁴. This is chance on a known looser pattern, not a relation. | verified | — |
| S13 | Free-Dirac corner function from 20° to 170°: this workspace's solver agrees with Helmes et al. 2016 to ≤ 4·10⁻⁵. The free scalar agrees to ≤ 5·10⁻⁵ from 26.6° to 170° after two stated corrections; at 20° a known mass-cutoff deficit of 10⁻⁴ remains. | verified | — |

---

## 3. Traps already paid for — please do not repeat them

1. **The fermion's twist parameter is not the scalar's.** At n = 2 the Dirac sectors have a = ±¼, not ½
   (Section 1). Eq. (59) of Casini–Huerta–Leitao is stated only for a ∈ (0, ½) and degenerates at ½. Two
   failed control runs here came from exactly this.
2. **Real-scalar reference values are halved complex-scalar values** (Section 1).
3. **High-mass nodes in the Casini–Huerta–Leitao ODE system need more precision than the signal suggests.**
   At complex twist parameter, or at any a ≠ ½, the starting series solve loses digits to conditioning. The
   rule that worked here is 30 + 9M digits. Carry the continuation coefficients in multiple precision: a
   double-precision hand-off between stages was a real bug. Store the starting residual and reject any node
   where it is not far below e^{−2πM}.
4. **Per-corner versus four-corner values.** Several QMC papers quote the square's total.
5. **The Einsteinian cubic gravity t₄ sign.** Bueno–Camps–Vilar López 2021's Fig. 1 caption and Bueno–Cano–
   Ruipérez 2018 eq. (129) pair the coupling with opposite signs of t₄. This workspace follows the 2018
   paper. No conclusion depends on it; state which you use.
6. **Old Rényi-2 tables.** 2013–14 linked-cluster values disagree with modern QMC at 2–4σ; cite the modern ones.
7. **Lower-bound inputs.** Lanzetta–Moult–Wang's a_n(π/2) ≥ (π²/4)σ_n rests on positivity that is only
   "suggested". Bueno–Witczak-Krempa's a(π/2) bound is rigorous at n = 1 only.
8. **Two citations lack recorded titles:** Van Bastelaere–Huang–Vanderstraeten 2609.20020 and Zhu–Wang–Cheng–Yan
   2605.00104. Verify before citing.
9. **Helmes et al.'s tail-completed formula (their eq. 22) is not reliable below a few degrees.** Its
   constructed tail gives the n = 1 fermion curve a small positive constant, which violates the proven
   convexity at 3–4°. Fine as a referee from 20° up; not below a few degrees.
10. **Prior art moves fast here.** Three relevant cusp-bootstrap papers appeared on 3 September 2026. Sweep
   again with your own framing's central term removed before claiming novelty.

---

## 4. Independence notes (read before calling anything a cross-check)

- **`quantum` holds a file-level copy of this workspace's solver**, byte-identical as of 2026-09-22, plus
  this workspace's notebook up to its entry EXP-011. Its `scripts/` has since been removed from the
  working tree but remains in its history. **A run of that copy cannot be an independent check of this
  workspace's numbers.**
- **`quantum`'s repaired a(120°) was accepted against a bound this workspace supplied.** It must not be
  used to corroborate anything here.
- **Shared literature ground truth.** Every route so far takes σ = π²C_T/24 and the Casini–Huerta–Leitao
  and Helmes et al. tables as given. Agreement on anything resting on those is one measurement, not two.
- **The sub-45° free-scalar magnitudes rest on this workspace's instrument alone at the 10⁻⁴ level**
  (S10). The Dirac ones have two methods behind them (S13).

---

## 5. The ranked backlog

**Scores are judgement.** Impact 1–5, where 5 bears directly on why the collapse happens. Complexity
1–5, where 5 means new theory or a new instrument over weeks or more. Chance is the probability of a
clean, reportable answer. **Ranking key: moonshot index = Impact × Complexity × (1 − Chance)**, so hard,
unlikely, high-impact work ranks first. **Kind:** A analytic, N numerical with an existing tool, I new
instrument, L literature or desk work.

| ID | Item | Impact | Complexity | Chance | Index | Kind |
|---|---|---|---|---|---|---|
| CF-1 | An absolute upper bound on κ/C_T | 5 | 5 | 3% | 24.3 | A |
| CF-2 | Why corner functions sit near the EMI shape (the κ band itself) | 5 | 5 | 5% | 23.8 | A |
| CF-3 | First von Neumann κ for an interacting CFT (Ising) | 5 | 5 | 8% | 23.0 | I |
| CF-4 | Corner entanglement on the fuzzy sphere (a two-cornered "lune") | 5 | 5 | 10% | 22.5 | I |
| CF-5 | The 1/N correction to κ/C_T for large-N O(N) | 4 | 5 | 10% | 18.0 | A |
| CF-6 | Test the non-analytic θ^{2η} small-angle term at Ising/O(N) | 4 | 5 | 10% | 18.0 | I |
| CF-7 | Numerical bootstrap of the n = 2 replica twist line in 3d Ising | 4 | 5 | 10% | 18.0 | I |
| CF-8 | A non-perturbative or top-down holographic corner function | 4 | 5 | 15% | 17.0 | A |
| CF-9 | Prove the rectangle bound, or conformal concavity, holds at n = 1 | 4 | 4 | 20% | 12.8 | A |
| CF-10 | What orders κ/C_T across theories (t₄ does not) | 3 | 4 | 10% | 10.8 | A |
| CF-11 | Prove reflection positivity of the corner function at n = 1 | 3 | 4 | 15% | 10.2 | A |
| CF-12 | A second instrument for free-field values below 45° | 3 | 4 | 35% | 7.8 | I |
| CF-13 | Independent analytic a₀ for the free scalar, including any log θ | 3 | 4 | 40% | 7.2 | A |
| CF-14 | Derive the smooth-end sign rule of the shape residual | 2 | 4 | 15% | 6.8 | A |
| CF-15 | A thermal handle on κ: the n → 0 limit of κ_n | 3 | 3 | 25% | 6.8 | N |
| CF-16 | Closed form of the Painlevé integral for the Dirac κ₂ | 1 | 4 | 20% | 3.2 | A |
| CF-17 | Is Ising's Rényi-2 corner function a constant multiple of the free one? | 3 | 2 | 60% | 2.4 | L then N |
| CF-18 | Scalar entanglement run at masses ≥ 14 and beyond, to reach 5°–10° | 2 | 2 | 70% | 1.2 | N |
| CF-19 | Cubic-gravity scan of κ/C_T over the t₄-allowed couplings | 2 | 1 | 95% | 0.1 | A |
| CF-20 | Fix the singular starting solve at large t in the Dirac run | 1 | 2 | 80% | 0.4 | N |
| CF-21 | Log-convexity in dimension of the free-field κ_d | 1 | 2 | 80% | 0.4 | A |
| CF-22 | Test the new cusp-paper inequalities on existing exact and numerical curves — **DONE 2026-09-24, see S7a, S7b** | 3 | 1 | 90% | 0.3 | N |
| CF-23 | κ/F₀ normalisation audit and the κ/F₀ ≤ 0.622 conjecture | 2 | 1 | 90% | 0.2 | L |
| CF-24 | Check the cuboid bootstrap's closure under Casimir dressing | 2 | 1 | 90% | 0.2 | A |
| CF-25 | The ECG t₄ sign discrepancy | 1 | 1 | 90% | 0.1 | L |

---

## 6. Item cards

Each card gives the goal, a first step, what counts as success or failure, and what must not be contradicted.

**CF-1 Upper bound on κ/C_T.** Every known positivity mechanism bounds κ from below: strong subadditivity,
reflection positivity, the rectangle and cuboid, conformal concavity, fusion-EFT positivity, Rindler
positivity. *First step:* for each new candidate constraint, test invariance under Casimir dressing (S5)
before anything else. *Success:* a constraint, true in every unitary CFT, that some dressed solution
violates. *Do not contradict:* S1 and S5. The only upper-type inequality found is 2609.04302 eq. (37),
which ties κ to the O(θ) coefficient, not to C_T. Sub-routes already shown to give lower bounds only:
twist-line crossing at integer n, and growth of one-point coefficients (Kravchuk–Radcliffe–Sinha 2406.04561,
whose density grows at a rate fixed *by* κ).

**CF-2 Why near EMI.** The deviation from the EMI shape is exactly the tripartite information
(Agón–Bueno–Casini 2109.09179). *First step:* compute the tripartite information in the strip and corner
limits for the free scalar and Dirac fermion, and holographically, and see whether a common reason makes it
small. *Do not contradict:* S11, and the normalisation warning.

**CF-3 First interacting κ at n = 1.** None exists for any interacting theory. The only interacting κ is
Ising at Rényi-2: 0.763(22) of the free value, from about 200 CPU-years of QMC on a thinly sliced torus
(Kulchytskyy–Hayward Sierens–Melko 2019, 1904.08955). QMC does not reach n = 1 directly. *Success:* any
controlled value. A value well outside 3.67–4.18 would break the collapse.

**CF-4 Fuzzy-sphere corners.** The fuzzy sphere gives ground-state (von Neumann) entanglement with no
replica limit; Ising's F = 0.0612(5) was obtained this way (Hu–Zhu–He 2024, 2401.17362). A lune between
two great half-circles has two corners and maps conformally to a wedge. Nobody has tried. *Obstacle:*
extracting a log coefficient from about 40 orbitals. *Known-answer control first:* a free or large-N
point, if one can be realised.

**CF-5 The 1/N correction.** At leading order κ and C_T are both N times the free values (Whitsitt–
Witczak-Krempa–Sachdev 2016, 1610.06568). The sign of the next order decides whether Wilson–Fisher sits
above or below the free scalar. *Control:* the known 1/N correction to C_T at θ → π.

**CF-6 The θ^{2η} term.** S6 with p = 2(Δ−1) predicts θ^{2η} ≈ θ^{0.07} at Ising, numerically close to a
logarithm. It needs sub-45° interacting data. The tensor-network and 3d classical transfer-matrix methods
of 2609.20020 reach 2·10⁻⁵ at 90° for Ising. *Control:* the free-scalar point. *Caveat:* replica twist
lines at O(3) points carry their own defect criticality (2605.00104), which may change the fusion content.

**CF-7 Twist-line bootstrap.** No bootstrap of a replica twist in an interacting 3d CFT exists. For the
free scalar, the n = 2 twist is a ℤ₂ monodromy (Bianchi et al. 2104.01220), which gives a known-answer
case. Would provide Rényi-2 cusp and Casimir data independent of Monte Carlo.

**CF-8 Non-perturbative holography.** Only perturbative cubic gravities move κ/C_T, and finite
higher-curvature couplings need a stringy tower to be causal. Top-down models are the only holographic
route to asking whether any strongly coupled theory leaves the band.

**CF-9 The n → 1 continuation.** Lanzetta–Moult–Wang's rectangle bound and their conformal concavity
(2609.04302: tan(θ/4)·a_n(θ) is convex) are theorems at integer n ≥ 2 and only checked numerically at n = 1.
A proof at n = 1 gives the first rigorous κ/C_T ≥ 2.39 for entanglement entropy.

**CF-10 The order of κ/C_T.** The order is scalar > Dirac > ECG(t₄ = −4) > Einstein > ECG(t₄ = +4). No
known quantity produces it (S3).

**CF-11 Reflection positivity at n = 1.** Conjectured by Casini–Huerta 2012. S1 does not depend on it; any
positive use of the corner function's spectral density would.

**CF-12 Second instrument below 45°.** Candidates are a free-scalar wedge with the 2609.20020 tensor-network
method, or an analytic expansion of the Casini–Huerta system. It must not use `quantum`'s copy of this
workspace's solver (Section 4). A lattice with only three clean angles, 60°, 90° and 120°, cannot reach
below 45°.

**CF-13 Analytic a₀ for the free scalar.** Half the inputs are published. The φ² coupling on the
entangling surface is marginally irrelevant, with its beta function in Metlitski–Fuertes–Sachdev 2009
(0904.4477) eq. (4.20) and a one-loop-exact form in Bianchi et al. 2021 (2104.01220) eq. (6.19). Missing is
the coefficient of the replica bilinears in the fusion of two parallel twist lines. Cardy 2013 (1304.7985)
gives the two-sphere analogue, which serves as a known-answer control. *Most direct route:* expand the
exact Casini–Huerta equations one order past κ/θ. *Success:* a number for a₀ and a yes or no on the log θ
term; this resolves S8.

**CF-14 Smooth-end sign.** The rule sign(σ̃′ − σ′) = sign(3π − κ/σ) holds everywhere except the n = 1 free
scalar, but its zero moves between theory families. Empirical, not derived.

**CF-15 Thermal handle.** As n → 0, σ_n is fixed by the thermal-entropy coefficient. Does n²κ_n tend to a
fixed multiple of it too? This would give κ a second channel at small n, not a bound at n = 1.

**CF-16 Painlevé closed form.** The Dirac κ₂ is the second moment of a Painlevé profile whose first moment is
fixed. An integrable-systems curiosity.

**CF-17 Ising Rényi-2 as a multiple of free.** The ratio to free is 0.763(22) at small angle (1904.08955)
and 0.78(4) at 90° (Ngai et al. 2512.00382). *First step:* pre-register the prediction at an angle nobody
has measured, then test it with CF-6's instrument or existing QMC codes.

**CF-18 Larger masses for the free scalar.** Rerun the 50 masses ≥ 14 with the fixed solver (Section 3,
trap 3), then extend to reach 5°–10°. The numerical side of CF-13's log question.

**CF-19 Cubic scan.** Only (9/5)β₁ + (18/5)β₂ moves κ/C_T among cubic couplings (Bueno–Camps–Vilar López
2021). Map it inside the t₄ bounds. Perturbative only.

**CF-20, CF-21.** Instrument housekeeping, and a parked free-field curiosity.

**CF-22 Test the new cusp inequalities.** 2609.04302 eq. (37) gives a₂ ≥ a₀/12, with a₀ ≡ −C the Casimir
coefficient, when the lightest fusion operator has Δ > 3/2. That covers Dirac, Einstein and ECG. Their
concavity says tan(θ/4)·a_n(θ) is convex for integer n ≥ 2. Exact Einstein and ECG curves exist, as do Dirac
and scalar curves at n = 1 and 2. A known-answer test that can fail; hours. *Watch the sign conventions:*
the paper mixes two for C.

**CF-23 κ/F₀.** Bueno–Casini–Lasso Andino–Moreno conjecture κ/F₀ ≤ 0.6223, the free-scalar value.
Tabulate κ/C_T and κ/F₀ side by side for every theory with known κ.

**CF-24 Cuboid under dressing.** An unchecked calculation suggests the Lanzetta–Moult–Wang cuboid bound is
also closed under a dressing that raises its four-body energy. Verify by hand.

**CF-25 ECG t₄ sign.** Bookkeeping (Section 3, trap 5).

---

## 7. Complementarity map — same quantity, different methods

Agreement between sessions counts as evidence only when the **methods** differ, not merely the code.

| Quantity | Independent routes | Why they are independent |
|---|---|---|
| Free-scalar a₀ and the log θ question | CF-13 analytic · CF-18 ODE numerics · CF-12 tensor-network wedge | Field-theory expansion, ODE system, lattice-type regularisation |
| Interacting κ at n = 1 | CF-3 QMC · CF-4 fuzzy sphere · CF-5 large-N analytic | Different regularisations and approximations entirely |
| Upper bound on κ | CF-1 · CF-9 · CF-24 · CF-22 | Each tests a different family of constraints against S5 |
| Shape near EMI | CF-2 tripartite information · CF-14 sign rule · CF-17 Ising shape · CF-23 normalisation | Analytic, empirical, numerical, desk |
| Interacting small-angle structure | CF-6 numerics · CF-7 bootstrap · CF-5 large N | Numerics, bootstrap bounds, analytic |

**Dependencies.** CF-22 and CF-24 are cheap first steps for CF-1. CF-18 supplies data for CF-13. CF-17's
desk study comes before its numerics. CF-6 and CF-17 can share one instrument. CF-23 should precede any
claim about CF-2.

**Suggested fits by repository, for the user and the bridge to decide.**
- **`corner_function`:** the items that use its solver or its derivations: CF-9, CF-13, CF-14, CF-15,
  CF-18, CF-20, CF-22, CF-24.
- **`quantum`:** lattice routes, within its geometric limit of 60°, 90° and 120°. Its own lattice numbers
  bear on CF-17 only if it builds interacting codes. Not an independent check of this workspace's solver.
- **`conjecture_machine`:** exact symbolic verification: CF-24, a symbolic check of S5, CF-16.
- **`TheBridge`:** cross-session items: CF-23, reconciling the sessions' backlogs, independence audits.
- **`SpaceTime` and `BlackHole`:** methods review of any new instrument (CF-3, CF-4, CF-6) against their
  catalogues of silent nulls and plateau failures.
- **Open to anyone:** CF-1, CF-2, CF-5, CF-7, CF-8, CF-10, CF-11.

**A light claiming rule.** Before starting an item, write it into your own repository's TODO with this
ID and your session's name, and tell the bridge. If two sessions want the same item, prefer different
methods from the table above to splitting one method.

---

## 8. References (verification level in brackets)

**Read here in full or at the cited equations:**
- Casini, Huerta, hep-th/0606256 (2007)
- Casini, Huerta, Leitao, 0811.1968 (2009)
- Bueno, Myers, Witczak-Krempa, 1507.06997 (2015)
- Bueno, Witczak-Krempa, 1511.04077 (2016)
- Helmes et al., 1606.03096 (2016)
- Bueno, Camps, Vilar López, 2012.14033 (2021)
- Lanzetta, Moult, Wang, 2609.04041 (2026)
- Lanzetta, Moult, Wang, 2609.04302 (2026), eqs. (28) and (37) read on the source
- Cuomo, He, Komargodski, 2406.10186 (2024)

**Checked on arXiv abstract pages or extracts by research agents on 2026-09-23:**
- Kulchytskyy, Hayward Sierens, Melko, 1904.08955
- Hu, Zhu, He, 2401.17362
- Bueno, Casini, Lasso Andino, Moreno, 2307.05164
- Agón, Bueno, Casini, 2109.09179
- Metlitski, Fuertes, Sachdev, 0904.4477
- Bianchi, Chalabi, Procházka, Robinson, Sisti, 2104.01220
- Whitsitt, Witczak-Krempa, Sachdev, 1610.06568
- Kravchuk, Radcliffe, Sinha, 2406.04561
- Cardy, 1304.7985
- Ngai et al., 2512.00382

**Titles not recorded; verify before citing:** Van Bastelaere, Huang, Vanderstraeten, 2609.20020; Zhu,
Wang, Cheng, Yan, 2605.00104.

*The workspace's own evidence for every row of Section 2 is in its `report.md` (entries EXP-001 to
EXP-021) and `RESULT.md`. A session that cannot read those can still rely on Section 2's status words.*
