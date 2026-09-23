# Report

*Rule IX: every experiment gets an entry. If it is not here, it did not happen.*

Required fields per entry:

    ## EXP-NNN  <short title>
    **Goal**            what problem is this solving
    **Hypothesis**      why should this approach work
    **Method**          the mathematics, with notation defined before use (M2)
    **Implementation**  files and lines changed
    **Results**         table: method, instance, metric, delta
    **Analysis**        why it worked or did not; what it reveals
    **Grade**           verified / partially verified / unverified
    **Next steps**      what to try based on this

---

## EXP-001  Prior-art sweep, verification of TASK.md, and measurement of the disagreement

**Date** 2026-09-04. **Status** complete; no derivation started (per instruction).

**Goal** (1) Establish what is known about the near-universality of a(θ)/C_T, with verified
citations; (2) decide outcome F (already explained?); (3) verify every factual claim in TASK.md;
(4) measure the size, sign and angle-dependence of the inter-theory deviations, with error bars.

**Hypothesis** None to test; this is the M1 gate. The working expectation going in was TASK.md's:
a collapse across five theory classes, a nearly-saturated bound, no explanation. Two of those
three survive unchanged; the third ("five theory classes") does not.

**Method** Citation verification against the arXiv API and full texts (ar5iv/arXiv HTML) for every
paper used; see `references.md` (30 entries, 17 read in full). Numerical: my own evaluation of the
Einstein-gravity corner function from [HT07] eqs (5.1)-(5.5) and of the SSA bound [BWK16] eq (II.2),
both validated against independent published spot values before use; the ECG family from
[BCV21] eq (293); free-field values taken from [CHL09] Table 1 and [HHCWM16] Tables 1-4 (never
inferred). Notation (M2): θ ∈ (0,π) the opening angle; a(θ) the coefficient of −log(H/δ) per
corner in the von Neumann entropy; a_n(θ) the Rényi analogue; σ, σ', σ'', σ^{(p)} the coefficients
of (θ−π)^2, (θ−π)^4, (θ−π)^6, (θ−π)^{2p+2} in the smooth-limit expansion; κ the coefficient of 1/θ
as θ→0; C_T the stress-tensor two-point normalisation in the Osborn-Petkou convention used by
[BMW15], for which C_T = 3/(32π²) per real scalar and 3/(16π²) per two-component Dirac fermion;
t_4 the parity-even stress-tensor three-point parameter, −4 ≤ t_4 ≤ 4.

**Implementation**
- `scripts/exp001_measure.py`: holographic curve (via the substitution z = g₀t that removes the
  width-g₀ peak; g₀ → 0 is the smooth limit, g₀ → ∞ the sharp one), the bound, the free-field
  tables, the `../quantum` comparison. Controls: σ/C_T → π²/24 (rel. err. 1e-5 at θ = π−10⁻³),
  κ/C_T → π²Γ(3/4)⁴/6 (rel. err. 3e-7), a_E(π/2)/C_T = 1.2220 and a_E(3π/4)/C_T = 0.2642 vs
  [BWK16] Table 1 (1.222, 0.264), and the [CHL09]-normalised s_H(π/2) = 0.02321, s_H(3π/4) =
  0.005019, κ_H = 0.0705 vs their 0.02321, 0.005019, 0.0704. All passed before any number below
  was read off.
- `scripts/exp001_coefficients.py`: order-by-order decomposition, O(N) normalisation, Rényi-2 data.
- `scripts/exp001_ecg.py`: ECG curve at all angles; controls σ_ECG/σ_E = 1−3μ and
  κ_ECG/κ_E = 1−123μ/20 reproduced to 6 digits at both ends of the allowed μ range; the
  σ-κ trial function and its slope.
- Outputs frozen in `scripts/exp001_output.txt`. Verified bibliography in `references.md`.

**Results**

*R1. What is known (chronology, all verified).* Free scalar a(θ) as the solution of nonlinear ODEs,
values at π/4, π/2, 3π/4, and κ ≈ 0.039 per real scalar [CH07]. Holographic (Einstein) f(Ω) in
closed parametric form, convexity/monotonicity from SSA, κ_E ∝ Γ(3/4)⁴ [HT07]. Dirac fermion
[CHL09], whose Table 1 and text already record the near-collapse *before normalisation by C_T*:
"maximal relative difference between the scalar and Dirac case of 9%", holographic-vs-Dirac
"only 2.5%", both maximal at θ → 0, and the theorem-level statement that the σ's of the complex
scalar and the Dirac fermion coincide (both 1/128). [BMW15] added the C_T normalisation, the
numbers 13% (scalar) / 2.5% (fermion) for the maximal deviation from holography, the O(N)
points at π/2, the conjecture σ/C_T = π²/24, and the observation that the deviation ratio is
monotonically decreasing in θ. [BM15] showed that R², f(R) and generalised-Lovelock corrections in
AdS₄ multiply a(θ) and C_T by the *same* constant, so a(θ)/C_T is *identically* the Einstein
function for that family. [Miao15] proved σ/C_T = π²/24 for general perturbative higher-curvature
duals and showed κ/C_T is not universal and that the Einstein curve is not a lower bound. [FLP16]
proved σ = π²C_T/24 for all 3d CFTs (second-order shape dependence of S_EE is non-locally ∝ C_T);
[BMMS16] gave the defect-CFT (displacement-operator) form of the same statement. [EH15] proved
σ_scalar = 1/256, σ_fermion = 1/128 exactly and that σ_n/C_T is *not* universal for n ≠ 1.
[BWK16] derived a(θ) ≥ 𝔞_min(θ) = (π²C_T/3) log[1/sin(θ/2)] from the SSA-plus-Lorentz inequality
a'' ≥ −a'/sinθ of [CHL09]; showed σ' is not a function of C_T and t_4 alone; gave the exact
Einstein σ^{(p)}/C_T through p = 5; and observed σ^{(p)} → 2κ/π^{2p+3} (radius of convergence π).
[HHCWM16] gave lattice and field-theory values at seven angles for boson and fermion, α = 1..4, the
exact σ' for free fields, an improved ansatz, and "near collapse" across α. [WWS17]: at N = ∞ the
Wilson-Fisher corner function is *exactly* N times the free-scalar one (the geometry-induced
mass does not affect the n → 1 limit in the infinite plane), so the WF/free-scalar agreement is
trivial at leading order in 1/N. [BCV21]: cubic curvature terms are the first that change the
*shape*; for Einsteinian cubic gravity across the full t_4-allowed coupling range the curve stays
within about 1% of Einstein and lies *below* it for t_4 > 0; the σ-κ trial function reproduces
every known curve to ≤ 1.2%. [LSZM24], [NCRCLM26]: precise QMC corner coefficients for O(3) and
Ising, but for the *second Rényi* entropy.

*R2. Outcome F: NOT resolved in the literature.* Every source treats the near-universality as an
observation. [BWK16]: "Little is known about a(θ) beyond [the θ→π] limit." [BCV21] (2021) still
calls it "the observation/conjecture of [BMW15]". Searches through September 2026 (terms:
corner entanglement universality explanation, modular Hamiltonian, bootstrap, strip coefficient
bound, Chern-Simons matter corners, fuzzy sphere corners) found no paper claiming a mechanism.
Grade: **verified** to the extent a negative literature result can be.

*R3. TASK.md claims, checked.*
| claim in TASK.md | verdict |
|---|---|
| a(π/2) ≥ (π² ln2/6) C_T is a proven bound | **verified** [BWK16] eq (II.4); general form 𝔞_min(θ) = (π²C_T/3) log[1/sin(θ/2)]; it is the equality case of a'' ≥ −a'/sinθ, and it is *not* the corner function of any CFT (diverges only logarithmically) |
| "all known theories nearly saturate it" | **partially verified**: true only near π/2 and above. Excess over the bound at π/2: Einstein 7.2%, ECG 6.9–7.5%, fermion 7.5%, scalar 9.2%, WF 14 ± 9%. At 26.6° the bound is 4.84 against true values 7.5–8.2 (36–41% below). At π the bound is saturated by construction. |
| "a family of higher-curvature holographic models" collapses | **wrong as evidence**: for the [BM15] family the ratio is *identically* Einstein's (both a and C_T rescale by the same factor); this is not an independent theory landing on the curve. The only family with a different shape is cubic gravity [BCV21], where the allowed range gives ±0.9% at 26.6°, ±0.3% at π/2. |
| free scalar, free fermion, holography agree "nearly" | **verified and quantified** (R4): scalar +12.7% at θ→0 falling to +0.4% at 135°; fermion +2.5% → +0.05%. |
| Wilson-Fisher O(N), N = 1,2,3, collapse | **partially verified only**: one angle (π/2), error ±8–10%, values quoted as 1.36(14), 1.3(1), 1.3(1) by [BMW15]/[BWK16]. The underlying a₁(π/2) for Ising is not printed in the cited source [KHSM13] (whose in-text order-26 value 0.0140 would give 1.56); the ratio is therefore taken on the authority of [BMW15]. See R6 for why this data carries no information about the collapse. |
| θ→π limit a ≃ σ(π−θ)², σ = π²C_T/24 | **verified** (theorem, [FLP16]; holographic proof [Miao15]) |
| θ→0 limit a ≃ κ/θ | **verified**; κ = 0.0397 (real scalar), 0.0722 (Dirac) [CHL09] Table 1; κ_E/C_T = π²Γ(3/4)⁴/6 = 3.7092 |
| "exact values for the free scalar and free fermion where they exist" | exact closed forms exist only for σ (1/256, 1/128) [EH15] and σ' ((20+3π²)/(9216π²) per complex scalar, (16+3π²)/(9216π²) per Dirac) [HHCWM16]; a(π/2) etc. are 4-digit numerics from the ODE system; κ is an integral of the 2d entropic c-function [CH07] |
| Tier-2 constraints (positivity, monotonicity, convexity, reflection) | **established with sources**: reflection a(2π−θ) = a(θ) (purity, [CH07]); a ≥ 0, a' ≤ 0, a'' ≥ 0 on [0,π] (SSA, [HT07] eq 3.1); a'' ≥ −a'/sinθ (SSA + Lorentz, [CHL09], as quoted in [BWK16] eq II.1); det{∂^{j+k+2}a_n} ≥ 0 (reflection positivity, [CH12], derived for integer n and assumed for n = 1); σ^{(p)} ≥ 0 for p ≤ 4 and σ'/C_T ≥ π²/576 [BWK16] |
| Tier 3: `../quantum` supplies a(60°), a(90°), a(120°) | **unusable as a referee at the required precision**: vs the exact real-scalar values, a(90°) is 1.9% (s=1) / 1.3% (s=6) low; a(60°) = 0.02423 is ≈8% low (expected ≈0.0264 from the scalar/holographic ratio); a(120°) = 0.003896 is **below the rigorous bound** 𝔞_min(120°) = 0.004495 by 13%. Why the check fired: the bound is a theorem for any CFT with finite C_T and the lattice is a real scalar, so the extraction (`qsim/corner_angles.py`: hexagons R ≤ 14, triangles l ≤ 28, N = 160, m = 0.01, 3- and 4-parameter fits) is what is wrong, not the bound. Not modified (read-only); flagged in TODO. |

*R4. The disagreement, measured.* a(θ)/C_T at the angles where free-field values exist. Free-field
column shows the [HHCWM16] field-theory ansatz value with, in brackets, the spread to their lattice
value (the only available error estimate; ≈1.3% at 26.6°, ≤0.6% elsewhere). Einstein, ECG and the
bound are exact (≤1e-8). Deviations are relative to Einstein.

| θ | Einstein | bound | ECG t₄=+4 | ECG t₄=−4 | Dirac fermion | real scalar |
|---|---|---|---|---|---|---|
| 26.57° | 7.575 | 4.839 | 7.510 (−0.86%) | 7.642 (+0.87%) | 7.685 [±0.7%] (+1.5%) | 8.212 [±1.3%] (+8.4%) |
| 45° | 4.037 | 3.160 | 4.009 (−0.69%) | 4.065 (+0.69%) | 4.085 [±0.1%] (+1.2%) | 4.264 [±0.1%] (+5.6%) |
| 63.43° | 2.445 | 2.115 | 2.433 (−0.50%) | 2.458 (+0.51%) | 2.475 [±0.4%] (+1.2%) | 2.537 [±0.2%] (+3.8%) |
| 90° | 1.2220 | 1.1402 | 1.2185 (−0.29%) | 1.2255 (+0.29%) | 1.2259 (exact 4-digit) (+0.32%) | 1.2454 (exact 4-digit) (+1.9%) |
| 116.57° | 0.5483 | 0.5321 | 0.5476 (−0.14%) | 0.5491 (+0.14%) | 0.5491 [series = ansatz; lattice +1.6%] (+0.15%) | 0.5527 [0%] (+0.8%) |
| 135° | 0.2642 | 0.2605 | 0.2640 (−0.07%) | 0.2644 (+0.07%) | 0.2643 (exact) (+0.05%) | 0.2653 (exact) (+0.4%) |
| 153.43° | 0.0896 | 0.0892 | 0.0896 | 0.0897 | 0.0897 [series = ansatz; lattice +17%, unreliable] (+0.1%) | 0.0900 [±0.6%] (+0.4%) |
| θ→0 (κ/C_T) | 3.709 | log only | 3.672 (−1.0%) | 3.747 (+1.0%) | 3.8005 (+2.5%) | 4.179 (+12.7%) |

Sign: every known theory lies above Einstein except ECG with t₄ > 0. Ordering at every angle:
scalar > fermion > ECG(t₄=−4) > Einstein = all [BM15] models > ECG(t₄=+4). Note t₄ does *not*
order the deviation: the free scalar (t₄ = +4) is highest and ECG at t₄ = +4 is lowest.

*R5. Order-by-order decomposition* (σ^{(p)}/C_T relative to Einstein; free-field coefficients from
[HHCWM16] Tables 3–4, Einstein from [BWK16] eq V.6):

| p | 0 | 1 | 2 | 3 | 4 | 5 | κ |
|---|---|---|---|---|---|---|---|
| complex scalar | 0 (theorem) | +10.2% | +15.3% | +16.4% | +15.5% | +14.4% | +12.7% |
| Dirac | 0 | +1.35% | +3.8% | +4.6% | +4.1% | +3.3% | +2.5% |
| ECG t₄=±4 | 0 | ∓1.65% | ∓1.9% | | | | ∓1.0% |

The deviation is not concentrated in one coefficient; from p = 1 on it is a roughly constant
percentage, i.e. the non-universal part of a(θ) has, to first approximation, the *same shape* as
the universal part's tail, which is what σ^{(p)} → 2κ/π^{2p+3} says (ratio σ^{(p)}π^{2p+3}/2κ is
within 2% of 1 for p ≥ 2 in all three theories).

*R6. Reduction to one number, and what the interacting data can see.* The two-parameter (σ, κ)
trial function of [BMW15b] (eq 261 of [BCV21]) reproduces the exact Einstein curve to ≤0.9%, the
exact free-field values to ≤0.6% (45°–135°), and per [BCV21] the ECG curves to ≤1.2%. With σ/C_T
fixed by theorem, the entire known family of a(θ)/C_T is therefore a *one-parameter family in
κ/C_T* up to ≈1% shape residuals, and the measured collapse is the statement

    κ/C_T ∈ [3.672, 4.179]   for every theory computed to date (a 13% band),

with Einstein at 3.709, the [BM15] family degenerate with it, ECG spanning ±1% around it, the
fermion at +2.5%, the scalar at +12.7%. The trial-function slope d(a/C_T)/d(κ/C_T) is 1.18 at
26.6°, 0.43 at 45°, **0.048 at 90°**, 0.008 at 120°. A π/2 measurement with the O(N) error bar
(±0.1 on a/C_T) therefore constrains κ/C_T to ±2.1, four times the *entire* band. The θ = π/2
value is pinned between the bound (1.140) and ≈1.25 by σ alone; **the existing interacting-CFT
data (all n = 1 data are at π/2) carry no information about the quantity in which the residual
non-universality lives.** "Wilson-Fisher lands on the curve" is a ±8% statement at the one angle
where all theories are within 2% of each other by construction.

*R7. Rényi n = 2 (side result, outside the n = 1 collapse).* a₂(π/2)/C_T: Ising 0.556 ± 0.028
[NCRCLM26], free real scalar 0.676 (exact 0.02567/4 per corner), O(3) 0.743 ± 0.028 [LSZM24]; the
O(3) honeycomb/square ratio [2s(π/3)+2s(2π/3)]/[4s(π/2)] = 1.17(5) vs 1.3231 for free bosons
[LSZM24]. A 30% spread; consistent with [EH15]'s non-universality of σ_n/C_T for n ≠ 1, and in
tension with the 2013–14 NLCE values 0.62(6)/0.61(6) that [BMW15] tabulated, which [SSSDSM16]
attribute to unusual corrections to scaling in Rényi extractions. The precise modern QMC numbers
are not von Neumann numbers and must not be used to test the n = 1 collapse.

**Analysis**
1. Not solved in the literature; outcome F does not apply. But the problem as posed in TASK.md is
   inflated: of five "theory classes" one is degenerate with Einstein by construction ([BM15]),
   one is trivially free at N = ∞ ([WWS17]) and unmeasured at the relevant angles for finite N,
   leaving three genuinely independent curves (scalar, fermion, Einstein) plus the ±1% ECG band.
2. The quantitative content of the collapse is: (i) σ/C_T universal (theorem); (ii) the shape is
   fixed by (σ, κ) to ≈1% (empirical, five curves, no explanation); (iii) κ/C_T confined to a 13%
   band with Einstein near its bottom (empirical, no explanation, and no bound: [BWK16]'s bound
   gives only κ > 0, and ECG shows κ/C_T < κ_E/C_T^E is allowed). κ is the thin-strip coefficient,
   for free fields (1/π)∫c(t)dt over the 2d entropic c-function [CH07]; so (iii) is a statement
   about strip entanglement per unit C_T, not intrinsically about corners.
3. Any explanation "of type (C_T, t_4)" is refuted by the data in R4/R5: the sign of the deviation
   at fixed t_4 = +4 differs between the free scalar (+12.7%) and ECG (−1.0%). [BWK16] showed the
   weaker linear-ansatz version for σ'. This is an outcome-E-type fact already available: the
   deviations cannot be a function of the stress-tensor 2- and 3-point data alone.
4. Tier 3 of TASK.md cannot do its job with the sibling's numbers (R3, last row). The referee
   values at the required 0.1–1% level are the [CHL09]/[HHCWM16] tables, which are inference-free
   evaluations of the exact free-field expressions, not lattice fits.

**Grade** R1, R2, R4 (Einstein, ECG, bound, CHL values): verified. R4 free-field values at 26.6°–
63.4° and 116.6°–153.4°: partially verified (published field-theory/lattice pairs, ≤1.3% spread, no
independent recomputation here). R3 O(N) row: partially verified (ratios quoted by two papers; the
underlying Ising a₁ not visible in the cited source). R6: verified for the five computed curves;
the "one-parameter family" reading is a description of known data, not a theorem. R7: verified as
quoted; interpretation flagged as Rényi-only.

**Next steps** (none started; awaiting the user's answers to the questions in the session report)
- If the reframed target is accepted: the object to explain/bound is κ/C_T, with ≈1% shape
  residuals as the second-order question. A two-sided bound on κ/C_T would make the collapse a
  corollary (outcome C); the first thing to establish is whether κ has any known bound at all.
- Independent recomputation of the free-field a(θ) from the [CH07]/[CHL09] ODE system at
  arbitrary angles (this repo, own code) to replace the ±1.3% small-angle uncertainty with 4-digit
  values; this is the one computation the reasoning route cannot substitute for, because small
  angles are where the signal lives and no published 4-digit value exists below 45°.
- Interacting theories: the only informative measurement would be a von Neumann (n = 1) corner
  coefficient at θ ≤ π/3 in an O(N) model, or equivalently a strip coefficient κ/C_T for an
  interacting CFT; none exists.

## EXP-002  Obstruction: the residual deviations are not a function of stress-tensor 2- and 3-point data

**Date** 2026-09-04. **Status** complete. Promoted from a remark in EXP-001 at the user's request.

**Goal** Test the class of explanations in which a(θ)/C_T, or its deviation from the Einstein
curve, is determined by the stress-tensor two- and three-point data of the CFT. In a parity-even
3d CFT that data is exactly the pair (C_T, t₄) [BCR18 Sec. 7; BWK16 App. C]; since C_T scales out
of a(θ)/C_T, the class is "a(θ)/C_T = F(θ; t₄) for some function F", with no assumption on F
(linearity was already excluded for σ' by [BWK16] Sec. VI).

**Hypothesis** If the class is viable, two theories with equal t₄ must have equal a(θ)/C_T at
every angle, in particular equal κ/C_T, σ'/C_T, σ''/C_T. Free fields sit at the endpoints t₄ = ±4
of the allowed range and Einsteinian cubic gravity (ECG) spans that range continuously, so the
endpoints can be compared between two theories with different dynamics.

**Method** Inputs and their sources.
- t₄ of free fields: for n_s real scalars and n_f/2 Dirac fermions t₄ = 4(n_s − n_f)/(n_s + n_f)
  [BCR18 footnote 23]; hence real scalar t₄ = +4, Dirac fermion t₄ = −4. Confirmed independently by
  [BWK16] Sec. VI ("the complex scalar has a positive t₄ = 4 … the fermion has a negative t₄ = −4").
  Einstein gravity t₄ = 0 [BWK16 Sec. VI; BCR18 Sec. 7].
- t₄ of ECG: t₄ = −1260 μ f∞² / (1 − 3μ f∞²) [BCR18 eq. 129], from the twist-operator expansion
  h_q/C_T = (π³/24)(q−1) − (π³/11520)(420 + t₄)(q−1)² [BCR18 eq. 128, after Chu–Miao]; the same
  procedure reproduces the standard Gauss–Bonnet t₂ with the correct sign (BCR18 App. A). Restated
  unchanged in [Cano19] eq. 7.129 and in the ECG dictionary table C_T t₄ = −3780 μ f∞ L²/(π³G).
  The allowed range −4 ≤ t₄ ≤ 4 maps to f∞ ∈ [312/313, 318/317], i.e. μ ∈ [−0.00322, +0.00312],
  with t₄ = −4 at μ = +100489/32157432 = +0.0031249 [BCR18 eqs. 130–132].
- ECG corner data: σ = (1−3μ)σ_E, σ' = (1−33μ/4)σ'_E, σ'' = (1−2673μ/296)σ''_E,
  κ = (1−123μ/20)κ_E, C_T = (1−3μ)C_T^E [BCV21 eqs. 226, 295–297], same action and same μ as
  BCR18 (BCV21 eq. 118 is BCR18 eq. 3 up to the overall Euclidean sign). Full curves from my
  integration of BCV21 eq. 293 (`scripts/exp001_ecg.py`), controls passed to 6 digits.
- Free-field and Einstein numbers: EXP-001 R4–R5.

**A sign inconsistency in the sources, and how it is handled.** BCV21's Fig. 1 caption assigns
μ ≃ +0.00312 to t₄ = +4 and μ ≃ −0.00322 to t₄ = −4, and concludes "ECG theories with t₄ ≥ 0
lie below the Einstein gravity one". BCR18 eq. 129, which BCV21 cite as the source of the range,
gives the opposite: μ > 0 ⇔ t₄ < 0, and BCR18 say explicitly that t₄ = +4 "would imply a negative
value of μ". The two papers use the same action and the same C_T(μ), so this is not a convention
difference. I adopt BCR18 (the derivation, validated on Gauss–Bonnet) and flag BCV21's caption as
the inconsistent statement. **The obstruction below holds under either assignment**; only the
sizes of the two pairwise conflicts change, and both are given.

**Results** (units of C_T; deviations relative to Einstein; free-field and Einstein values exact
or 4-digit, ECG exact at first order in μ)

| theory | t₄ | κ/C_T | σ'/C_T | σ''/C_T | a(45°)/C_T | a(90°)/C_T |
|---|---|---|---|---|---|---|
| real scalar | +4 | 4.179 (+12.7%) | 0.028709 (+10.2%) | 2.814e-3 (+15.3%) | 4.264 (+5.6%) | 1.2454 (+1.9%) |
| ECG, μ = −0.00322 | +4 (BCR18) | 3.747 (+1.0%) | 0.026478 (+1.7%) | 2.488e-3 (+1.9%) | 4.065 (+0.7%) | 1.2255 (+0.3%) |
| Einstein, all [BM15] models | 0 | 3.709 (0) | 0.026042 (0) | 2.441e-3 (0) | 4.037 (0) | 1.2220 (0) |
| ECG, μ = +0.00312 | −4 (BCR18) | 3.672 (−1.0%) | 0.025611 (−1.7%) | 2.394e-3 (−1.9%) | 4.009 (−0.7%) | 1.2185 (−0.3%) |
| Dirac fermion | −4 | 3.8005 (+2.5%) | 0.026394 (+1.35%) | 2.533e-3 (+3.8%) | 4.085 (+1.2%) | 1.2259 (+0.3%) |

*Predicted by any F(θ; t₄):* scalar ≡ ECG(t₄=+4) and fermion ≡ ECG(t₄=−4) at every angle;
Einstein = F(θ; 0). If F is monotone in t₄ the five rows must be ordered by t₄.

*Measured:* neither identity holds, and the rows are not ordered by t₄.
1. Same t₄ = +4, different curves: κ/C_T 4.179 vs 3.747 (11.5% apart), σ'/C_T 8.4% apart,
   σ''/C_T 13.1% apart, a(45°) 4.9% apart. Uncertainties on both sides < 0.1%.
2. Same t₄ = −4, different curves: κ/C_T 3.8005 vs 3.672 (3.5% apart), σ'/C_T 3.1% apart,
   σ''/C_T 5.8% apart, a(45°) 1.9% apart.
3. Not monotone: the two t₄ = −4 theories straddle the t₄ = 0 theory (fermion +2.5%, ECG −1.0%),
   and the fermion (t₄ = −4) lies *above* the t₄ = +4 ECG curve (+2.5% vs +1.0%).
4. Under the alternative assignment (BCV21 caption): conflict 1 becomes 4.179 vs 3.672 (13.8%),
   conflict 2 becomes 3.8005 vs 3.747 (1.4% in κ, 0.3% in σ'), and the straddle disappears.
   Conflict 1 alone is two orders of magnitude above the uncertainties, so the obstruction is
   independent of which sign is right.

**Analysis** Any account of the residual non-universality that is a functional of ⟨TT⟩ and ⟨TTT⟩
alone cannot reproduce the measured deviations: it is forced to give the free scalar and one
holographic theory the same curve, and they differ by 11.5% in the sharp-limit ratio. This closes
the most natural "one more stress-tensor datum" extension of the σ theorem, including linear
(BWK16) and arbitrary nonlinear dependence, and including conformal-collider-type arguments that
only see energy-flux data. What survives: four-point stress-tensor data (BWK16's conjecture for σ'),
non-stress-tensor spectral data, or the twist-defect fusion data that control κ directly (EXP-003).
Two further readings of the table: within each family the deviation *does* increase with t₄
(scalar > fermion; ECG(+4) > ECG(−4)), but the scale differs by an order of magnitude between free
fields and holography, so t₄ is at most a within-family ordering parameter; and the free scalar
is the outlier in every column, consistent with its known anomalous Rényi stationarity [LLPS15].

**Grade** verified for the numbers and for the obstruction; the pairing of ECG curves with t₄
signs is *partially verified* (BCR18 derivation adopted over BCV21 caption; the inconsistency is
recorded above and in TODO).

**Next steps** None required for this entry.

## EXP-003  Outcome E: the general entropic constraints on a(θ) do not localise κ/C_T

**Scope, stated first.** "Admissible" below means *satisfies the listed inequalities C1–C6*. It does
not mean "is the corner function of a unitary 3d CFT": the Lifshitz endpoint used in the proof is the
corner function of a z = 2 Lifshitz theory and is not Lorentz invariant. Nothing here claims that a
CFT with κ/C_T = 10⁶ exists. The claim is narrower and stronger: **the constraint set does not
localise κ, so the physical band κ/C_T ∈ [3.672, 4.179] is not a consequence of the constraints.**

**Date** 2026-09-04; rewritten 2026-09-05 (argument spelled out, unboundedness made analytic).
**Status** complete.

**Provenance (M1 on this result).** The representation of the corner function as a Laplace
transform of a positive measure is the "infinite divisibility / conditional positivity" structure
of [CH12], who write (Sec. 5.2) "if we could write g(θ) as a Laplace transform…" for the holographic
case and verify the determinant inequalities for free fields to 6×6. [BWK16] proved in their App. A
that every reflection-positivity inequality "leads to lower bounds, and never to an upper bound", and
posed in their Sec. IX (Discussion), verbatim: "It is further natural to ask whether an upper bound exists for
a(θ), and its expansion coefficients. The holographic correspondence could be helpful in answering this
question." (ar5iv lines 690–692 of arXiv:1511.04077; the question is about a(θ) in general, not a narrower
object). That question is what this entry answers, in the negative and for the full
constraint set (not only reflection positivity). The mass-versus-tail reading, the explicit admissible
functions with arbitrary κ, and the consequence for the collapse are not in the literature I found
(searches on 2026-09-05: "corner function" with "moment problem", "completely monotone",
"infinitely divisible", "Laplace transform"; nothing relevant).

**Notation (M2).** θ ∈ (0, π), ε ≡ π − θ; a(θ) the corner function; σ = π²C_T/24 (theorem, [FLP16]);
κ ≡ lim_{θ→0} θa(θ); 𝔞_min(θ) ≡ (π²C_T/3) log[1/sin(θ/2)] [BWK16 eq. II.2]; a_L(θ) ≡ (θ−π)²/(θ(2π−θ))
[BWK16 Sec. VII; BCV21 eq. 260]; CHL[a] ≡ a'' + a'/sinθ.

**The constraint set 𝒞.** C1 reflection a(2π−θ) = a(θ) [CH07]; C2 a ≥ 0, a' ≤ 0, a'' ≥ 0 on (0,π)
[HT07]; C3 CHL[a] ≥ 0 [CHL09, as BWK16 eq. II.1]; C4 det{∂_θ^{j+k+2}a}_{j,k<M} ≥ 0 for all M, θ
[CH12; proven for integer Rényi index, conjectural at n = 1]; C5 a = σε² + O(ε⁴), σ = π²C_T/24, a
analytic at π with even powers; C6 a ~ κ/θ, κ > 0. Every published bound on a(θ) at n = 1 uses a
subset of these (EXP-001 R2).

**Spectral form.** For analytic a, C4 says the derivative sequence of a'' at every θ is a Hamburger
moment sequence, hence (Bernstein–Widder) a''(θ) = ∫₀^∞ dρ(s) cosh(sε) with ρ ≥ 0 after symmetrising
with C1, and a = ∫ dρ (cosh sε − 1)/s². Then: C1, C2, C4, C6 hold for every ρ ≥ 0 (C6 with κ read
off the tail: ρ ~ 2κ s² e^{−πs}); C5 is the total-mass condition M₀ ≡ ∫dρ = 2σ; C3 is the single
linear inequality CHL[a](ε) = ∫dρ(s) K(s,ε) ≥ 0 with kernel

    K(s, ε) = cosh(sε) − sinh(sε)/(s sin ε).

**Lemma 1 (the kernel has one sign change).** For fixed ε ∈ (0,π), K(s,ε) ≥ 0 ⟺ tanh(sε)/s ≤ sin ε.
The function s ↦ tanh(sε)/s decreases strictly from ε (s→0⁺) to 0, because its derivative has the
sign of sε sech²(sε) − tanh(sε) = (y − sinh y cosh y)/cosh²y < 0 (y = sε > 0). Since sin ε < ε,
there is exactly one s*(ε) > 0 with K < 0 on (0, s*) and K > 0 on (s*, ∞). So C3 penalises spectral
weight at small s and rewards weight at large s; it is the only constraint that is not automatic.

**Lemma 2 (two admissible functions).** (i) 𝔞_min ∈ 𝒞, κ = 0: C3 with equality [BWK16 App. A.1];
ρ_min(s) = (π²C_T/3) s/sinh(πs) > 0 (derived from −log cos(ε/2) = Σ_p (2^{2p}−1)|B_{2p}|(ε/2)^{2p}/(p(2p)!)
and (2^{2p}−1)ζ(2p)/2^{2p} = Σ_{m odd} m^{−2p}, giving M_{2p−2} = ∫s^{2p−2}·s/sinh(πs)). (ii) â_L ≡
(π⁴C_T/24) a_L ∈ 𝒞 with κ/C_T = π⁵/48 = 6.375: ρ_L ∝ s²e^{−πs} > 0 (the Laplace transform of s²e^{−πs}
is exactly 1/θ + 1/(2π−θ) − 2/π ∝ a_L); C3 reduces, with a_L = ε²/(π²−ε²), ∂_ε a_L = 2π²ε/(π²−ε²)²,
∂_ε²a_L = 2π²(π²+3ε²)/(π²−ε²)³, to f(ε) ≡ (π²+3ε²) sin ε − ε(π²−ε²) ≥ 0 on [0,π]. Proof: with
sin x ≥ x − x³/6 (x ≥ 0), f/ε ≥ ε²[(4 − π²/6) − ε²/2] ≥ 0 for ε ≤ 2.17; for ε = π − t, t ∈ [0, 0.97],
f ≥ (π² + 3·2.17²)(0.843 t) − t(π−t)(2π−t) ≥ (20.2 − 19.74) t ≥ 0. ∎ (Consistent with [BWK16] Sec. VII.)

**Theorem (no localisation).** (a) 𝒞 ∩ {σ fixed} is convex (C2–C4 and C6 are positivity/linear
conditions, C5 is affine), and κ is linear on segments. Hence a_λ = (1−λ)𝔞_min + λ â_L ∈ 𝒞 realises
every κ/C_T ∈ (0, 6.375]. (b) κ is unbounded above: let ρ_u ≡ 2κ s² e^{−πs} Θ(s−u), u ≥ 0, with
a_u = κ[e^{−uθ}/θ + e^{−u(2π−θ)}/(2π−θ) − 2e^{−uπ}/π] (closed form of its Laplace transform); its
sharp coefficient is κ for every u, while its mass 2σ_u = 2κ e^{−πu}(u²/π + 2u/π² + 2/π³) → 0. For
C3: at each ε, either u ≥ s*(ε), and then CHL[a_u](ε) = ∫_u^∞ ρ_L K ≥ 0 because K ≥ 0 on [u,∞) by
Lemma 1; or u < s*(ε), and then CHL[a_u](ε) = CHL[a_L](ε) − ∫₀^u ρ_L K ≥ CHL[a_L](ε) ≥ 0 because K ≤ 0
on [0,u] and CHL[a_L] ≥ 0 by Lemma 2(ii). C1, C2, C4, C6 hold since ρ_u ≥ 0. Rescaling to the
universal σ (C5) gives κ/C_T = (π²/24)·κ/σ_u → ∞ as u → ∞. ∎
Numerical check of the same family (`scripts/exp003_spectral.py`, `scripts/exp003_output.txt`):
κ/C_T = 0.004, 3, 10, 100, 10⁴, 10⁶ all pass C1–C6 at 40 angles; the moment positivity of the real
Einstein/scalar/Dirac coefficient sequences passes and a corrupted sequence fails.

**Mechanism.** In the spectral variable, σ is the mass of a positive measure and κ is its e^{−πs} tail.
C1, C2, C4, C6 are consequences of positivity; C5 fixes the mass; C3 is one inequality that is
indifferent to (in fact rewards) weight at large s. A tail functional of positive measures with fixed
mass is unbounded above and can vanish. **Corollary:** no inequality that is itself a consequence of
ρ ≥ 0 — any reflection-positivity-type inequality for a(θ) at n = 1, of any order — can bound κ. A
bound must be a constraint that some positive ρ violates, i.e. it must carry information beyond the
entropic inequalities of the corner function. This is why the problem is open, not merely that it is.

**Assumptions.** C4 at n = 1 is conjectural [CH12]; it is used only to organise the constraints and to
certify C4 for the constructions (which hold by ρ ≥ 0 regardless). Dropping C4 enlarges 𝒞, so the
theorem stands without it. Completeness of C1–C6 is the literature statement of EXP-001 R2.

**Grade** verified (analytic throughout; Lemma 2(ii)'s elementary inequality proved by standard
bounds; the numerical family is a check, not part of the proof).

## EXP-004  Direct numerical solution of the Casini–Huerta–Leitao system for the free-field corner functions at finite angle

**Date** 2026-09-04 (in progress; this entry is updated as results land). **Status** solver built and
validated on four exact controls; large-angle Rényi-2 values obtained; arbitrary-precision production
runs for the full angle range under way.

**Goal** Replace the ±1.3% published free-field values below 45° [HHCWM16] with 4-digit values at
arbitrary angles, for the real scalar (Rényi-2 as control, then von Neumann) and the Dirac fermion.
This is the computation the user authorised after the analytic route stalled (EXP-003): the residual
non-universality lives at small angles, where no published value is better than ≈1%.

**Why reasoning alone was insufficient** Every published free-field a(θ) below 45° is a Taylor
series about θ = π truncated at order 14–16 (radius of convergence π, so 8% short at 26.6°) plus
lattice points at the ≈1% level. The exact expressions of [CH07]/[CHL09] were never integrated
at finite angle; the authors expanded them in series ("an economic way to numerically integrate
the equations is to expand … in Taylor series around x = π", [CHL09] Sec. 4). Nothing analytic
reaches the sharp-angle regime.

**Method (M2).** x ≡ θ; δ ≡ π − x; M ≡ 2d mass on the unit sphere; a ≡ twist parameter; the 2d
Green-function trace on the cut sphere is tr G_S(x, M, a) = 8π a(1−a) F(x, M, a) with
F = ∫_x^π H_a(y, M) dy, and H solves the six-variable nonlinear ODE system with five algebraic
constraints of [CHL09] App. B eqs (73)–(83), boundary values (84)–(89) at x = π. Observables:
- Rényi-2, real scalar [CH07 eq. 40]: s₂(x) = 2 ∫_{1/2}^∞ dM M√(M²−¼) F(x, M, ½).
- Entanglement entropy, complex scalar [CHL09 eq. 61]: s_S(x) = ∫₀^∞ dt 2/cosh²(πt) ∫ dM M√(M²−¼)
  tr G_S(x, M, ½−it); real scalar = ½ of this.
- Dirac fermion [CHL09 eqs. 59–60]: s_D(x) = ∫₀^∞ dt /(2 sinh²πt) ∫_{−∞}^{∞} dm m tr G_D|odd, with
  tr G_D|odd = 2m tr G_S − 16π a(1−a) m (4β₁X₁cos(x/2) − bB₁sin²x)/(M(4β₁² − b²sin²x)), a = −it,
  M² = ¼ + m².
Mass variable p = √(M²−¼), so M√(M²−¼) dM = p² dp; Gauss–Legendre grids in p and t.
x = π is a regular singular point. The solution is started from a power series in δ whose
coefficients are found by least squares on the coefficient equations (leading orders derived by
hand: β₁¹β₂¹ = [a(a−1)+M²(1+b₀c₀)]/(4M²), β₁¹c₀ = b₀β₂¹, u¹ = Mc₀β₁¹, H¹ = 1/(16πa(1−a)) +
M(β₁¹X₂⁰ + β₂¹X₁⁰)); the local expansion has a genuine two-fold sign ambiguity in β¹, and only one
branch gives an H¹(M) that decays in M (the other does not, so its mass integral cannot exist).
Parities in δ, checked numerically: H, u, β₁, β₂, B₁₂ odd; X₁, X₂, b, c, B₁, B₂ even.

**Precision analysis (the finding that shaped the implementation).** The physical solution near
x = π has H ≈ e^{−2πM} relative to the O(1) variables and then grows like e^{2M(π−x)} as the
corner sharpens; any absolute error ε in the O(1) variables (b, c, X, u) seeds that same growing
mode, so the relative garbage in F is ε·e^{2πM}. Double precision therefore resolves the signal only
for M ≲ 4, while the mass integrand at small angles decays only slowly: measured rates
dlnF/dM ≈ 5.5, 3.9, 2.2, 1.6, 1.2, 0.83 per unit M at θ = 135°, 90°, 45°, 26.6°, 15°, 5°. Hence
double precision gives 4 digits only for θ ≳ 60°, and sharp angles need masses up to ≈15 with
≈25 + 3M decimal digits and a series start accurate to e^{−2πM}·10⁻¹⁰ in absolute terms
(N ≈ 1.6M + 8 terms from δ₀ = 0.01/M). Implemented in mpmath with a 32nd-order
Gragg–Bulirsch–Stoer integrator, parallel over (M, t) nodes.

**Implementation** `scripts/exp004_ch_solver.py` (double precision: series start by
Levenberg–Marquardt, DOP853 integration, algebraic constraints solved at every step with a
deterministic root branch), `scripts/exp004_mp.py` (arbitrary precision: parity-reduced
Gauss–Newton series start warm-started from the double solution, Bulirsch–Stoer with adaptive
macro-step, complex a), `scripts/exp004_prod.py` (parallel driver, per-node JSON checkpoints,
modes renyi2 / ee / dirac), `scripts/exp004_run.py` and `scripts/exp004_controls.py` (double
runs), logs and node files under `scripts/`.

**Controls (all passed before any new number was read off).**
| control | source of the known value | result |
|---|---|---|
| σ₂ (real scalar) = 1/(48π²) = 2.110857993e-3 | [BMW15] App. B, [HHCWM16] Table 3 | 2.110857993e-3 (ratio 1.0000000) |
| σ₂′ = (5+π²)/(960π⁴) | [HHCWM16] Table 3 (exact) | ratio 1.000000 |
| σ₂″, σ₂‴ | [HHCWM16] Table 3 (high precision) | ratios 1.000000, 1.000000 |
| s₂(90°) real scalar | 0.0064 [CH07 via KHSM13]; 0.0130/2 [HHCWM16] | 0.006487 (double, M ≤ 4, two grids agree to 2e-4) |
| s₂ at 116.6°, 135°, 153.4° | [HHCWM16] Table 1 α=2 /2: 0.00286, 0.001365, 0.0004615 | 0.0028591, 0.0013665, 0.00046127 (ratios 0.9997, 1.0011, 0.9995; their values are 3-digit) |
| mp vs double at M = 1 | internal | all six angles agree to the printed 8 digits |
| complex a (EE path) | imaginary part must cancel [CHL09] | Im F ≈ 1e-27 at a = ½ − 0.3i and ½ − i |
The first four are the smooth-limit coefficients from the series start alone, i.e. they validate the
boundary values, the local expansion and the branch choice to 7 digits; the angle values validate
the ODE integration and the mass quadrature.

**Results so far (double precision, M ≤ 4, real scalar Rényi-2, 48-node grid).**
θ = 90°: 6.4879e-3; 100°: 4.8632e-3; 110°: 3.5659e-3; 120°: 2.5291e-3; 130°: 1.7072e-3;
135°: 1.36649e-3; 140°: 1.06848e-3; 150°: 5.9099e-4; 160°: 2.5959e-4; 170°: 6.4448e-5
(uncertainty ≈ 2e-4 relative at 90°, ≤ 1e-5 beyond 130°). Values below 90° from this run are
contaminated by the large-mass loss of precision and are superseded by the mp run.

**Grade** solver and controls: verified. Angle values ≥ 90° (Rényi-2): verified to the stated
precision. Everything below 90° and all von Neumann / Dirac values: pending (mp production).

**Status update 2026-09-05 — runs parked at the user's request.** Rényi-2 real scalar completed after
the series-start fix (leading order built in mp, continuation in N; the double-precision warm start
was the cause of the failure above M ≈ 5.4 and had also biased earlier nodes at M ≈ 3 by 0.2–0.5%):
48 mass nodes to M = 15, 1.2 core-hours, σ₂ and σ₂′ from the nodes reproduce the exact values to
9 digits, the smooth limit at 170° to 7e-6, and the seven [HHCWM16] angles to ratios 1.0000, 1.0004,
1.0002, 0.9981 (their value is 3-digit), 0.9997, 1.0011, 0.9995. The sharpest angles (5°, 10°) are
still contaminated by the M ≈ 15 nodes (one node has F(5°) < 0), so "4 digits at any angle" was
overclaimed there. The von Neumann and Dirac runs were not executed (EE nodes for M ≲ 1 exist as
checkpoints). Honest justification, answering the user's challenge: this computation sharpens the
≈1% shape residual beyond (σ, κ) and supplies exact reference values; it does not address why the
band κ/C_T ∈ [3.67, 4.18] is narrow, which is the question. Parked, not killed: the instrument is
validated and can resume in minutes if the residual becomes the target.

**Next steps (if resumed)** von Neumann scalar (controls: σ = 1/256, σ′ = (20+3π²)/(18432π²), s(π/2) = 0.01183, s(3π/4) =
0.002520, κ = 0.0397); then the Dirac fermion (controls: σ = 1/128, σ′ = (16+3π²)/(9216π²),
s(π/2) = 0.02329, s(3π/4) = 0.005022, κ = 0.0722).


## EXP-005  What a bound on κ/C_T would have to use, and why nothing available does

**Date** 2026-09-05. **Status** complete as an audit; negative.

**Goal** Given EXP-003, list every general structure that could in principle constrain κ, and decide
for each whether it can exclude positive spectral measures (the criterion of EXP-003's Corollary).

**Method** For each candidate: what it constrains, whether that constraint is implied by ρ ≥ 0, and
what it would need to become a bound. Sources for each named structure are the ones already
verified in `references.md`.

| structure | what it gives for the corner function | bounds κ? | what would be needed |
|---|---|---|---|
| Strong subadditivity, all configurations | Inequalities among log coefficients arise only when the area terms cancel, i.e. overlapping sectors with shared boundary pieces (HT07; CHL09 with boosts). In every such configuration the *smallest* angle sits on the "≥" side (a(α−β) ≥ a(α)+a(γ−β)−a(γ)), so SSA gives lower bounds on a at small angles — convexity, C3 — never upper bounds. | No (lower bounds only; C2–C3 are already in 𝒞). | An SSA configuration putting a small-angle corner on the "≤" side with cancelling area terms; none exists for sectors (intersections are narrower than their factors). *partially verified*: standard configurations classified, no exhaustive proof. |
| Reflection positivity of the corner function, any order | C4 = ρ ≥ 0. | No (Corollary of EXP-003). | Nothing: it is a positivity condition, blind to the tail. |
| The Rényi tower a_n(θ), n ≥ 2 | Each a_n satisfies its own C1–C4 with h_n in place of C_T [BWK16 eq. II.8]; a_n at integer n is a genuine twist-line two-point function. | No: there is no inequality linking κ_n across n (Rényi mutual information is not monotone in n), and n → 1 is exactly where C4 becomes conjectural. | A proven n-monotonicity or an n-analyticity bound for the *sharp* coefficient; none known. |
| The strip / mutual-information reading of κ | κ is the short-distance coefficient I(A,B) ≈ κℓ/w of two half-planes [CH07; NN15; BW22]; equivalently κ_n = −E_Cas(n)/(n−1), the Casimir energy per unit length of a twist-n line and its orientation reversal (fusion datum, [DKPW24] define the fusion product). Reflection positivity of the slab partition function gives E_Cas ≤ 0, i.e. κ_n ≥ 0. | Lower bound 0 only. | An *upper* bound on the Casimir energy of the reflection-symmetric defect pair, which requires the slab spectrum and overlaps — dynamical data of the twist defect at n → 1. Not available in general; [DKPW24] compute examples. |
| A crossing relation for the two-defect system | The two-twist-line partition function has a short-distance (fusion, κ) and a long-distance (bulk OPE, Δ_min and OPE data) expansion; for 2d CFT the analogous 4-point function is bootstrappable and bounds follow. | Not yet: no positivity-controlled crossing equation is available for the n → 1 limit in d = 3 (positivity of the fusion expansion at n = 1 is again the [CH12] conjecture, which EXP-003 shows is insufficient on its own; the bulk-channel data would have to be added). | The n → 1 defect crossing equation with a positive fusion expansion *and* bulk spectral input. This is the one route that could produce a two-sided bound in terms of CFT data. Unverified, named as the target. |
| Modular theory (Bisognano–Wichmann, relative entropy, first law, QNEC) | Constrain state dependence and *second* null variations of S (QNEC: S''_null ≤ 0 in vacuum, which is the FLP entanglement density ∝ −C_T, i.e. the σ theorem). | No: second order only; κ is the resummation of all orders of the shape expansion (radius of convergence π, κ at its boundary). | An all-orders shape inequality; none exists. |
| Stress-tensor n-point positivity (ANEC, conformal collider) | Bounds 3-point data (t₄ ∈ [−4, 4]); higher-point positivity could in principle bound σ^{(p)} order by order. | No: EXP-002 shows κ is not a function of (C_T, t₄); and no finite set of moments M_{2p} bounds the tail of a positive measure (moment indeterminacy). | Simultaneous control of all orders, which is the crossing relation above in another guise. |
| Free-scalar extremality (κ/C_T ≤ 4.179) | Parallels the conjectured extremality of the free scalar for C_T/F₀ in d = 3 [BFGLM26]; consistent with all known values (EXP-001 R4). | Conjecture only. | An F-theorem-like monotonicity for the strip coefficient; the only known one is holographic (strip c-function, Myers–Singh 2012, not verified here), and it relates κ across an RG flow, not κ to C_T within a CFT. |

**Provenance.** [BWK16] Sec. IX raise the upper-bound question and suggest holography as the tool; the
holographic answer ([Miao15], [BCV21]) was that the Einstein curve is not even a lower bound. No
source treats the question structurally.

**Analysis** Every available general principle either is a positivity condition on the corner
function (and therefore cannot see the tail, by EXP-003), or acts at finite order in the shape
expansion (and therefore cannot see a quantity that sits at the boundary of that expansion's
convergence). The obstruction has a name: **κ is a non-perturbative fusion datum of the twist
defect (the Casimir energy of the reflection-symmetric pair as n → 1), and no entropic inequality or
finite-order correlator bound reaches it.** The only structure that could, a crossing equation for the
two-defect partition function with positive expansions at n = 1, does not exist in usable form. This
is outcome E for the class {entropic inequalities of a(θ)} ∪ {stress-tensor 2- and 3-point data} ∪
{finite-order shape perturbation theory}: no argument in that class can produce the band
κ/C_T ∈ [3.672, 4.179], and the reason is structural, not a failure of ingenuity.

**Grade** verified for the rows marked with sources and for the mechanism; the SSA row is partially
verified (no exhaustive classification); the crossing-relation row is a named target, unverified.

**Next steps** If the user wants to pursue a bound: the twist-defect crossing route at integer
n ≥ 2 first (where positivity is not conjectural), asking whether κ_n/h_n is bounded there; a bound
at n = 2 would be a new result even without the n → 1 continuation. This is analytic/bootstrap
work, not a corner-function computation.


## EXP-006  The integer-n route: formulation, data, and where it inherits the obstruction

**Date** 2026-09-05. **Status** formulated; one structural finding; negative as a bound.

**Goal** Follow EXP-005's one live route at n = 2, where positivity of the twist-line correlators is
not conjectural: ask whether κ_n/h_n is bounded by the structure of the two-twist-line partition
function.

**Setup (M2).** For integer n the twist operator τ_n(∂A) is a codimension-2 conformal defect of CFT^n;
S_n(A) = (1/(1−n)) log[Z_n(A)/Z₁^n]; the Rényi mutual information I_n(A,B) = (1/(n−1)) log[Z_n(A∪B)/(Z_n(A)Z_n(B))]
is the connected two-defect partition function. For two half-planes at separation w, I_n = κ_n ℓ/w
[CH07; BMW15b Sec. 3.2]; κ_n is the sharp-corner coefficient of a_n(θ) and, equivalently, minus the
Casimir energy per unit length of τ_n and its orientation reversal divided by (n−1). h_n is the
conformal weight of τ_n (energy density in the hyperbolic thermal ensemble, [HMS14]).

**Data at integer n (free fields; h_n exact from [BMW15b] Table 1; κ_n are source values from [BMW15b] Table 3, quoted there as 0.0455996(1), 0.0472338(1), etc., i.e. with an uncertainty of 1 in the last digit, reproduced in [BW22] Table 2; none computed here):**

| n | h_n (complex scalar) | κ_n (cs) | κ_n/h_n (cs) | h_n (Dirac) | κ_n (f) | κ_n/h_n (f) | spread |
|---|---|---|---|---|---|---|---|
| 2 | 1/(24π) = 0.013263 | 0.0455996 | 3.438 | 1/64 = 0.015625 | 0.0472338 | 3.023 | 13% |
| 3 | 1/(27√3) = 0.021383 | 0.037339 | 1.746 | 5/(108√3) = 0.026729 | 0.040662 | 1.521 | 14% |
| 4 | (3π+8)/(192π) = 0.028888 | 0.033798 | 1.170 | (1+6√2)/256 = 0.037052 | 0.0376674 | 1.017 | 14% |
| 1 | (C_T-normalised) | 0.0794 | κ/C_T = 4.179 | | 0.0722 | 3.800 | 10% |

The free-field spread of κ_n/h_n is ≈14% at every integer n, no narrower than at n = 1. No
holographic κ_n exists for n ≥ 2 (the strip Rényi entropy is not known holographically), so at
integer n the "band" is two points.

**Fusion-channel positivity is complete monotonicity in the separation, and is tail-blind.** Quantise
with Euclidean time along the direction joining two parallel twist lines; the reflection through the
mid-plane maps one line to the other (for n = 2, τ₂ is its own orientation reversal). Reflection
positivity then gives, for the family of separations, Σ c_i c_j Z(d_i + d_j) ≥ 0, i.e. (Widder)
Q(d) ≡ Z_n(A∪B)/(Z_n(A)Z_n(B)) = ∫ dμ(E) e^{−E d} with μ ≥ 0: Q is completely monotone in d. For two
half-planes Q = e^{(n−1)κ_n ℓ/w}, which is completely monotone for *every* κ_n ≥ 0 (e^{c/w} =
Σ_k c^k/(k! w^k) and each 1/w^k is a Laplace transform of a positive density). So the fusion channel
gives κ_n ≥ 0 and nothing else, by the same mass-versus-tail mechanism as EXP-003: the short-distance
coefficient is the large-E tail of μ, the long-distance behaviour is its small-E part, and positivity
of μ relates neither to the other.

**No crossing symmetry in d = 3 (the structural finding).** In d = 2 the two-interval Rényi entropy
obeys F_n(x) = F_n(1−x) because the complement of two intervals on the Riemann sphere is again two
intervals with cross-ratio 1−x; this exchanges the fusion limit (x → 1) with the OPE limit (x → 0) and
is what lets positivity bound the short-distance coefficient by low-lying data (the mechanism of the
Cardy formula: crossing turns a tail into a mass). In d = 3 the complement of two disjoint disks is a
region with two holes, conformally an annulus, not two disks; purity only reverses the orientation of
the same two circles. The two-disk Rényi partition function Q(η), η ∈ (0,1), therefore has two positive
expansions — the fusion expansion at η → 1 (complete monotonicity) and the bulk OPE expansion at
η → 0, Q = Σ_O C_O² G_O(η) with C_O the one-point coefficients of the twist defect — but **no symmetry
exchanging their limits.** Both expansions describe the same limits from the same side. Without such a
symmetry, positivity in each channel is tail-blind in the sense of EXP-003, and the short-distance
coefficient is fixed only by the high-Δ growth of Σ C_O², which unitarity alone does not bound.
(Consistently, [ACHM25] find the long-distance series of the d = 4 scalar mutual information is only
asymptotic at n = 1, and [AM26] give the exact two-sphere Rényi mutual information of the free
Dirac field in d = 3 for all n, which would be the test function for any sum rule.)

**What the integer-n route would need.** A bound on κ_n/h_n requires a bound on the growth of the
defect one-point coefficients C_O² of τ_n at large Δ in terms of low-lying data — a defect-bootstrap
statement (crossing of the defect two-point function of bulk operators, or of the bulk-to-defect
OPE), not an entropic inequality. That input exists for line defects in principle (defect bootstrap)
but has not been developed for twist lines of CFT^n and is beyond this session.

**Analysis** The obstruction of EXP-003/005 persists at integer n: the only non-conjectural positivity
available (reflection positivity of the two-defect correlator) is complete monotonicity in the
separation, which cannot see the tail, and d = 3 lacks the crossing symmetry that makes the analogous
d = 2 problem bootstrappable. The named input that could reach κ_n is the high-Δ growth of the twist
defect's one-point coefficients.

**Grade** the data table and the complete-monotonicity statement: verified; the absence of a crossing
symmetry for two disks: verified (elementary geometry of complements); "unitarity alone does not bound
the growth of C_O²": partially verified (no such bound is known to me; not proved impossible).

**Next steps** If continued: (i) extract the twist-line one-point coefficient growth from the exact
Dirac two-sphere Rényi mutual information [AM26] at n = 2 and check what "Cardy-like" growth
reproduces κ₂ = 0.0472338; (ii) ask whether the defect bootstrap for τ₂ constrains that growth.


## EXP-007  Complement topology: why the d = 2 tail-to-mass bridge has no d ≥ 3 analogue

**Date** 2026-09-05. **Status** complete; standalone version in `RESULT.md` §6.

**Goal** State the mechanism by which positivity bounds a short-distance coefficient in d = 2 (the
two-interval Rényi entropy), identify precisely what it needs, and show what fails for two balls in
d ≥ 3.

**The mechanism (Cardy).** A positive spectral sum plus a symmetry exchanging its two asymptotic
regimes turns a tail into a mass: modular invariance Z(β) = Z(4π²/β) fixes the high-energy density
of states from the vacuum. For two intervals in a 2d CFT the scaling function obeys F_n(x) = F_n(1−x)
[CCT09 verbatim: "It is also invariant under x → 1−x (even if not manifest in this form)", and "by
symmetry x → 1−x also for x close to 1, corresponding to close intervals"] because the complement of
two intervals on the circle is two intervals with cross-ratio 1−x; the far regime (lightest
operators) and the touching regime (short-distance coefficient) are exchanged.

**What it needs.** (i) a positive expansion of the function in one channel; (ii) a symmetry mapping
the regime where the sought coefficient dominates onto the regime controlled by low-lying data.

**What fails in d = 3.** Two disjoint disks are conformally a disk and the exterior of a concentric
disk [NN15; AM26 eq. 2.16 use exactly this map]; their complement is the annulus between them, a
connected region with two boundary circles, not two disks. Purity only reverses the orientation of the
same two circles. Hence the two-disk Rényi partition function Q(η) has two positive expansions (fusion
at η → 1: complete monotonicity in the separation; bulk OPE at η → 0 [Cardy13]) but no symmetry
exchanging their limits. Each channel's positivity is then tail-blind in the sense of EXP-003, and the
short-distance coefficient is fixed only by the large-Δ growth of the twist defect's one-point
coefficients.

**Generalisation.** In d = 2 an interval's entangling surface is two points and four points can be
re-paired; in d ≥ 3 a ball's entangling surface is a connected sphere and the complement of two balls
in S^d is a shell bounded by both, which cannot be re-paired. So the absence of crossing holds for
two-ball Rényi mutual information in every d ≥ 3, and the tail-blindness applies to every
short-distance coefficient of that function (the strip coefficient κ_d of [AM26] eq. 4.16 in any d).

**Provenance.** Ingredients standard ([CCT09]; [NN15], [AM26]). The assembled statement not found
(searches 2026-09-05 for higher-dimensional mutual information with "crossing"/"complement"; results
are the long-distance-expansion papers [Cardy13] and successors, none of which use or discuss a
crossing symmetry). Offered as new with that caveat.

**Grade** the geometry: verified (elementary); the claim that this is *the* reason bounds are absent
in d ≥ 3: an explanation consistent with everything checked, not a theorem — labelled as such.

## EXP-008  The Abate–Martinek route: what the exactly solvable instance shows

**Date** 2026-09-05. **Status** complete as a reading; negative as a bound.

**Goal** Follow EXP-006's next step: in the one exactly solvable case — the two-sphere Rényi mutual
information of the free massless Dirac field in d = 3 for all n [AM26] — read off how the short-distance
coefficient κ is encoded in the "OPE-channel" data, and ask whether the construction contains a bound.

**What [AM26] do (verified from their §2–4).** They map two spheres to the concentric configuration
(disk of radius a, exterior of radius b; cross-ratio η = 4ab/(a+b)², their eq. 2.16 — the same
disk-plus-exterior geometry as EXP-007), reduce on the angular sphere to a tower of two-dimensional
Dirac fields in AdS₂ with masses μ_ℓ and degeneracies λ(ℓ) (polynomial in ℓ, eq. 4.27), and compute
each mode's Rényi mutual information exactly through Painlevé VI tau functions (eqs. 3.19–3.27). The
full answer is the sum over ℓ (eq. 4.3). In §4.3.1 they extract the area term: "we will approximate
the sum over the angular momentum as an integral, because the divergence will come from the terms
with large ℓ" (eq. 4.18), each large-ℓ mode reduces to the flat-space two-interval problem for a
massive 2d Dirac field (eqs. 4.19–4.21), and the result is
I = 2^{[d/2]+1}/((d−2)(d−3)!) (a/ε)^{d−2} ∫₀^∞ dt t^{d−3} c_flat(t) (eq. 4.24), i.e. exactly the
strip coefficient κ_d = [(d−2)2^{d−3}π^{(d−2)/2}Γ((d−2)/2)]^{−1} ∫ t^{d−3} c_flat(t) dt (eq. 4.17),
which for d = 3 is the Casini–Huerta formula κ = (1/π)∫c(t)dt [CH07 eq. 44]. For n = 2 the same
integral with the Rényi-2 c-function is how [BMW15b] Table 3 obtained κ₂ = 0.0472338(1) (Dirac);
[AM26] do not re-quote that number.

**What this establishes.** In the solvable instance the picture of EXP-003/006/007 is literal: the
long-distance (OPE) regime is the ℓ = 0 sector and the first few modes (their §4.2 and App. B give the
long-distance coefficients mode by mode); the short-distance coefficient κ is the *tail* of the mode
sum, Σ_ℓ λ(ℓ) I(η; μ_ℓ) with λ(ℓ) ~ ℓ^{d−3}, and its value is set by the 2d dynamics of every mode
(the c-function of a massive Dirac fermion), not by any positivity property of the sum. The
"density of contributions" at large ℓ is polynomial and universal (it is the angular degeneracy); the
non-universal content of κ is the integral of the mode function. There is no crossing relation in
their construction (consistent with EXP-007), and the sum over ℓ converges "much slower" in the
short-distance regime, "strongly depending on the value of ε" (their §4.3.2), which is the same
tail-sensitivity in yet another guise.

**What it cannot give.** A bound on κ/h_n would need the mode function's integral to be bounded in
terms of low-ℓ data; in the free theory the mode function is the same 2d c-function for every ℓ (only
the mass changes), so the integral is fixed by the 2d theory and unrelated to h_n except through the
common free-field normalisation. For interacting CFTs the tower does not decouple, and the analogue of
the mode sum is the bulk-channel expansion of the two-defect correlator organised by spin, whose
large-Δ density is the defect one-point-coefficient growth named in EXP-006. The solvable instance
therefore confirms the diagnosis and supplies a test function for any future sum rule; it does not
supply the sum rule.

**Grade** the reading of [AM26]: verified against their text (equations quoted by number). The
interpretation as "κ = tail of the mode sum": verified (it is their derivation). "No bound is
contained in the construction": verified for the free case by inspection; the interacting statement
is the EXP-006 obstruction restated.

**Next steps** None within reach of this session. The open input remains a growth bound on the twist
defect's one-point coefficients at large Δ; the free-field mode sum gives the target growth
(polynomial density times a fixed mode function) that any such bound would have to reproduce.

## EXP-009  Attack on the complement-topology claim: pre-registered falsifiers, outcome "true in a narrower form"

**Date** 2026-09-05. **Status** complete. No computation; reasoning and three metadata lookups.

**The target (EXP-007, RESULT.md §6 as first written).** (T) The complement of two balls in S^d is a
shell for d ≥ 3. (C) This is *why* no bound on κ exists: the Cardy mechanism needs a symmetry
exchanging the two asymptotic regimes of a positive expansion; d = 2 has it (x ↔ 1−x, from the
re-pairing of four endpoints); d ≥ 3 has no such symmetry, so a tail can never become a mass.

**Pre-registered falsifiers (written before looking).**
- Strong (withdraw C): a model-independent two-sided bound or exact determination of a non-local
  short-distance coefficient in a d ≥ 3 CFT — κ, σ′, F, c_S/C_T, or a defect Casimir coefficient —
  derived without any relation between two positive expansions with inversely related parameters.
- Weak (force a narrowing): any d ≥ 3 configuration containing κ that possesses a limit-exchanging
  structure; C as stated says none exists.
- Unfalsifiable: if "limit-exchanging structure" cannot be defined so that a proposed mechanism can be
  tested against it without already knowing the answer.

**Step 1 — where tail-from-mass bounds come from anywhere.** Modular bootstrap (β ↔ 4π²/β); four-point
crossing (u ↔ v; the lightcone bootstrap's large-spin data come from the crossed identity);
open–closed duality of the annulus (t ↔ 1/t; Cardy's boundary-state conditions); Froissart (unitarity
plus analyticity in the crossed channel); EFT positivity, where linear positivity gives one-sided
bounds and crossing gives two-sided ones — [TWZ21] verbatim: "In contradistinction to the linear
positivity for scalars, these inequalities [from full crossing symmetry] can be applied to put upper
and lower bounds on Wilson coefficients"; [CV21] find all coefficients bounded both ways from
causality and unitarity. Positivity alone: Källén–Lehmann bounds the mass side (Z ≤ 1); the
c-theorem's sum rule gives one-sided c_UV ≥ c_IR; Nachtmann/Hölder give convexity in spin, no upper
bound. Anomaly matching fixes local coefficients without any channel relation. Pattern: positivity →
one-sided; two-sided → a second positive expansion with inversely related parameter whose lowest state
is universal; locality → local coefficients only.

**Step 2 — the weak falsifier fired.** Two limit-exchanging structures exist in d ≥ 3:
(i) *Two parallel twist lines (the strip geometry).* Quantising across the lines gives the closed channel
Q(w) = ∫dμ(E) e^{−Ew} (complete monotonicity, EXP-006). Quantising *along* the lines gives an open
channel: Q = Tr_{H(w)} e^{−ℓ H_open(w)} = Σ_k e^{−ℓ E_k(w)}, positive in e^{−ℓ}, where H(w) is the
Hilbert space of CFT^n on the transverse plane with two twist-point insertions at distance w. For
infinite lines only the ground state survives, Q = e^{−ℓE₀(w)}, so E₀(w) = −(n−1)κ_n/w: **κ_n is the
ground-state energy coefficient of the open channel.** The tail of one channel is the mass of the
other. The naive claim "no exchange exists for κ" is false.
(ii) *The torus.* The Euclidean partition function on T² × R^{d−2} is symmetric under exchanging the
two cycles, so the high-temperature entropy density coefficient equals d times the Casimir energy
coefficient of the theory with one compact spatial cycle: c_S = d·c_vac [Sha16, "generalized Cardy
formula"]. Free scalar in d = 3: c_vac = ζ(3)/(2π), c_S = 3ζ(3)/(2π): exact, as it must be (same
Euclidean path integral).
*Why neither yields a bound:* the mass at the other end is itself non-local. E₀(w) is the Casimir
energy of two twist points on a plane; c_vac is the Casimir energy on a circle; in odd d no anomaly
fixes such quantities (there is no conformal anomaly), and in even d anomalies fix Casimir energies only
of curved geometries, not of flat tori or defect configurations. Contrast d = 2, where the crossed
vacuum is universal twice over: the identity operator in the OPE channel, and the Casimir energy
−πc/(6L) fixed by the anomaly in the thermal channel. Numerical corroboration: c_S/C_T in d = 3 is
60.43 (real scalar: s = 3ζ(3)T²/(2π), C_T = 3/(32π²)), 12πζ(3) = 45.3165 (Dirac: s = (3/2)·3ζ(3)T²/(2π),
C_T = 3/(16π²)), 4π⁵/27 = 45.3362 (Einstein: s = 4π²L²T²/(9G), C_T = 3L²/(π³G)) — a 33% spread across
theories despite the exact cycle-exchange relation, because c_vac is non-universal. (The Dirac and
Einstein values agree to 4.4·10⁻⁴ — corrected from 3·10⁻⁴; resolved as chance in EXP-010.)

**Step 3 — the strong falsifier did not fire.** No model-independent two-sided bound on κ, σ′, F,
c_S/C_T or a defect Casimir coefficient in d ≥ 3 exists in the literature reached in this workspace or
in the attempts above. And the moment-problem statement of EXP-003 generalises: for Q(q) = ∫q^Δ dν(Δ)
with ν ≥ 0, any constraint of the form ∫φ dν ≤ B with φ = o(tail growth) leaves the singular-end
coefficient free; a bound requires a growth condition at the singular end itself. Known sources of
such growth conditions: (a) an inverted channel with a universal lowest state (absent for κ: the
two-ball function's only channel with a universal lowest state is radial quantisation about the
common centre, whose universal end is the far limit, and complement topology forbids any conformal map
of the touching end onto it; the strip's open channel exists but its lowest state is non-universal);
(b) locality/anomalies, which fix local coefficients only (σ ∝ C_T; the even-d log term of the
two-sphere mutual information equals the anomaly, [AM26] §4.3.2) — κ is not local (EXP-002);
(c) a finite local Hilbert-space dimension, giving cutoff-dependent bounds (κ ≤ 2β_∞δ from S ≥ 0,
cf. [BW22]); (d) an a priori analyticity-plus-growth bound of Froissart type — in QFT these come from
unitarity plus crossing, or from locality with a cutoff, so (d) reduces to (a) or (c) in every case
known to me. This is "I found no third bridge", not "none can exist".

**Step 4 — what is now a theorem, and what is not.**
(N1) *Theorem (moment problem).* Positivity of the expansion plus any set of constraints dominated by
the mass (finite-order local data, low-lying spectral data, normalisations) cannot bound a
singular-end coefficient from above; a bound requires a growth condition at the singular end.
(N2) *Theorem (d = 2).* The x ↔ 1−x symmetry supplies that growth condition because the crossed
channel's lowest state is the identity with a universal contribution; the symmetry exists because
the four endpoints of two intervals re-pair into two intervals.
(N3) *Theorem (d ≥ 3 geometry).* The two-ball Rényi function has exactly one positive channel with a
universal lowest state (radial quantisation; identity at the far end) and no conformal map sends the
touching end to the far end (complement of two balls is a shell). The strip has an inverted channel,
but its lowest state is the non-universal Casimir energy E₀(w) ∝ κ_n.
(N4) *Fact (odd d).* Casimir energies of flat and defect geometries are non-local in odd d, so inverted
channels there relate non-universal quantities to each other (torus: c_S = d c_vac; strip: κ_n = E₀).
(C, narrowed) The only known bridges from a singular-end coefficient to universal data are (a) an
inverted channel with a universal lowest state and (b) locality/anomaly; for κ, (a) is absent by
N3, (b) is excluded by EXP-002; no third bridge is known. This is a classification of known
mechanisms and is falsifiable by exhibiting a third; it is not a theorem that none exists.

**Step 5 — consequences checked against things not used to build the claim.**
- Torus: the generalised Cardy relation c_S = d·c_vac holds exactly in every CFT [Sha16] — predicted
  by "inverted channel ⇒ tail = mass"; and c_S/C_T is nonetheless non-universal (33% spread above) —
  predicted by "the mass is non-universal in odd d". Both checked.
- Even versus odd d: the refined mechanism says short-distance coefficients fixed without a channel
  relation must be local; the two-sphere mutual information's log coefficient is the anomaly in even d
  [AM26 §4.3.2] and no such universal subleading term exists in odd d, where the subleading term is
  F [AM26 eq. 4.4] — consistent.
- Forward-looking, falsifiable: no proof of the free-scalar extremality conjectures (κ/C_T ≤ 4.18;
  C_T/F₀ ≤ scalar value, [BFGLM26]) can come from entropic inequalities or finite-order positivity; a
  proof would have to supply a growth condition at a singular end. Consistent with [BFGLM26]'s d = 5
  finding that F(A) is unbounded in both signs for general regions.

**Outcome.** *True in a narrower form.* (T) stands. (C) as first stated is wrong: limit-exchanging
structures do exist in d ≥ 3 (strip along/across; torus cycles) and one of them contains κ. The
surviving statement is N1–N4 plus the narrowed classification: what d ≥ 3 lacks for κ is not an
exchange but an exchange *onto a universal lowest state*, and in odd d the missing universality is the
absence of anomaly-fixed Casimir energies. The general principle "positivity gives one-sided bounds,
crossing gives two-sided ones" is prior art in the EFT-positivity literature [TWZ21, CV21]; the
generalised Cardy relation is [Sha16]; the application to entanglement coefficients, the
open-channel reading of κ_n, and the "universal lowest state" refinement are not in the literature
reached here.

**Grade** N1–N3: verified (N1 is EXP-003's mechanism; N2 elementary with [CCT09]; N3 elementary
geometry plus the along/across quantisation). N4: verified as stated (no anomaly in odd d; torus
and defect Casimir energies non-local). The narrowed (C): a classification, partially verified —
its falsifier is a third bridge. Numbers in Step 2: computed here from standard free-field and
Einstein-gravity formulas; not independently sourced.

## EXP-010  The parked coincidence c_S/C_T (Dirac) ≈ c_S/C_T (Einstein): chance, and here is the base rate

**Date** 2026-09-05. **Status** complete; arithmetic and three lookups, no computation.

**Pre-registration (before looking).** Null: chance. "Chance" withdrawn only if (a) the base rate against
the actual Dirac–Einstein spread in this family comes out below ~1% *and* (b) a further independent
quantity shows the same pair within 1e-3 while the scalar does not. "Relation" only if it predicts a
number not used to find it. "Less non-universal than the theorem allows" requires a third,
structurally different theory within ~1% of the value.

**Correction of my own numbers first.** 12πζ(3) = 45.3165 and 4π⁵/27 = 45.3362, not 45.320 and 45.332
as written in EXP-009 and TODO (both now corrected). The agreement is 4.4·10⁻⁴, not 3·10⁻⁴. The
underlying inputs are standard and were re-derived here: real scalar s = 3ζ(3)T²/(2π), C_T = 3/(32π²);
Dirac s = (3/2)·3ζ(3)T²/(2π), C_T = 3/(16π²); Einstein s = 4π²L²T²/(9G) (planar AdS₄ black brane,
T = 3r_h/(4πL²)), C_T = 3L²/(π³G) [BMW15]. Since 4π⁵/27 = 12π·(π²/9)², the physical coincidence is
exactly the arithmetic near-identity **ζ(3) ≈ π⁴/81** (81ζ(3)/π⁴ = 0.99956).

**It is not new and not isolated in the sense that matters: it is the n → 0 end of a known curve.**
The Rényi corner coefficient σ_n of a disk-type twist is set by the thermal free energy on H² at
temperature T₀/n; as n → 0 that is the flat-space high-temperature limit, i.e. c_S. [BMW15b] Tables 2
and 4 give lim_{n→0} n²σ_n/C_T = ζ(3)/π² (Dirac) and π²/81 (Einstein): the same two numbers, the same
ratio π⁴/(81ζ(3)). [BMW15b] already recorded (Sec. 5, verified text) that σ_n/C_T for the free Dirac
fermion and Einstein gravity agree to "no more than 2.6% for n ≥ 1 and 0.2% in the range 0 ≤ n ≤ 1".
So the c_S coincidence is the endpoint of a curve whose 0 ≤ n ≤ 1 branch was already known to agree to
0.2%. The two are one observation, not two.

**Base rate, three ways.**
1. Conditional on the known 0.2% envelope on 0 ≤ n ≤ 1 with a forced zero at n = 1 (the σ theorem): a
   smooth deviation of typical size ≲ 2·10⁻³ on that branch lands within 4.4·10⁻⁴ at the endpoint with
   probability of order 4.4·10⁻⁴/2·10⁻³ ≈ 20%.
2. Unconditionally, against the Dirac/Einstein log-ratios of the quantities in hand — κ/C_T +2.4%,
   σ′ +1.3%, σ″ +3.7%, σ‴ +4.5%, a(π/2) +0.3%, a(45°) +1.2%, σ_∞ +2.6%, h₂ +0.95% (Dirac π²/12 = 0.8225
   vs Einstein π·σ₂^{hol}/C_T = π³(5√13−1)/648 = 0.8148, from [BMW15b] Table 4), F/C_T −34%, c_S −0.044% —
   a spread of a few per cent gives ≈1% per quantity for a 4.4·10⁻⁴ hit, and ≈5–10% for at least one
   among the eight or so comparable quantities.
3. Arithmetically: the chance that ζ(3) lies within 4.4·10⁻⁴ of *some* π^k/n with small k and n ≤ 100 is
   of order 10–20% (the spacing of π⁴/n near 1.2 is ≈0.015, so that family alone gives ≈6%).
None reaches the pre-registered 1%.

**Criterion (b) fails.** The one out-of-sample quantity I had not looked at, h₂/C_T, differs by 0.95%
between the pair; σ_∞ by 2.6%; F/C_T by 34%; t₄ maximally (−4 vs 0). The pair's typical proximity is
1%, not 10⁻³. The only sub-percent agreements are the forced ones near n = 1 (σ theorem) and the n < 1
branch already noted by [BMW15b].

**Hypothesis "less non-universal than allowed" fails.** Third theories: real scalar 16πζ(3) = 60.43;
N = ∞ O(N) Wilson–Fisher (4/5)·16πζ(3) = 48.34 (c̃/N = 4/5 [Sac93], with C_T = N C_T^{free} at leading
order [WWS17]); N = ∞ Gross–Neveu equals N free Dirac fermions exactly, c̃/N = 3/2 [PSN99], hence not
an independent point. The value 45.3 is shared only by the free Dirac fermion and Einstein gravity;
bosonic theories sit 7–33% higher. The obstruction theorem is untouched: c_S/C_T spans a 33% band.

**Hypothesis "a relation" fails as an exact statement and is not pursued as an approximate one.** Any
relation making the two functions equal would have to hold on n > 1 as well, where they differ by up
to 2.6% with a definite sign (Dirac above Einstein for every n > 1, Einstein above at n → 0). No
relation is proposed; constructing one to hit 45.32 would be the post-hoc fitting the contract
forbids.

**Verdict.** Chance, superposed on a known, loose and still unexplained pattern: the hyperbolic thermal
free energy of the free Dirac fermion and of Einstein gravity, normalised by C_T, agree exactly at
T = T₀ (theorem), to ≤ 0.2% for T ≥ T₀ (n ≤ 1), and to ≤ 2.6% for T < T₀ (n > 1) [BMW15b]; the c_S
endpoint at 4.4·10⁻⁴ is within that envelope. The residue worth explaining, if any, is the 0.2%
branch, and it belongs to [BMW15b]'s observation, not to this session. What would distinguish
"crossing plus coincidence" from anything structural: the sign of the deviation on n ∈ (0, 1) —
both closed forms are known (Einstein: (π²/24) n x_n(1−x_n²)/(n−1) with x_n = (1+√(1+3n²))/(3n),
reproducing Table 4; Dirac: [BMW15b] eq. 3.10 sums) — a sign change inside (0, 1) would make the
small endpoint difference a crossing artefact; but even a uniform sign would not turn a 0.2%
agreement into a relation without a prediction on n > 1, where none exists.

**Grade** numbers: verified (re-derived; cross-checked against [BMW15b] Tables 2 and 4, which reproduce
the same ratio). Base rates: estimates, stated as such. Verdict: the null, with the pre-registered
criteria applied as written.

## EXP-011  The Abate–Martinek route at n = 2: κ₂ is the tail, the bridge is absent, and it is confirmation

**Date** 2026-09-05. **Status** complete; reading and arithmetic only, no computation.

**Pre-registration.** Three outcomes named before reading: (A) a sum rule relating a growth rate to κ₂
that predicts something not used to build it; (B) confirmation that κ₂ is exactly the tail with
nothing in the construction bounding it; (C) the step is not session-sized. Also pre-registered: a
growth rate fitted to reproduce 0.0472338 is not a result, and (B) if obtained is not news.

**Fact 1 — the n = 2 tail formula, and what 0.0472338 is.** [AM26] §4.3.1 write the area term only at
n → 1 (eqs. 4.18–4.24, mutual information I and the entropic c-function). The Rényi version is the
same derivation with I → I_n, c̃ → c̃_n; in d = 3 it is exactly [BMW15b] eq. (3.20),
κ_n^f = (1/π)∫₀^∞ c_n^f(t) dt, and their Appendix B states that Table 3 was obtained by "numerically
solv[ing] eqs. (B.4) and (B.6) … and then us[ing] the results to evaluate eq. (3.22)". So
κ₂ = 0.0472338(1) *is* the tail integral evaluated numerically. Comparing "the growth read off the
solvable case" with it compares a formula with its own evaluation: an identity, not a test. No
independent 3d determination of κ₂^f (lattice or corner-function extraction) was found to test
against, and none is needed, because the tail identity is a derivation, not a conjecture.

**Fact 2 — what "the growth" is in the solvable case, and why it cannot bound anything.** In d = 3
the degeneracy is λ(ℓ) = 1 and μ_ℓ = ℓ + ½ ([AM26] eqs. 2.9–2.10). The area term (their 4.18) keeps
only the top power of λ and only ℓ ~ ℓ_* ~ a/ε → ∞ (their 4.25); any finite set of low modes
contributes at most O(log(a/ε)) (their 4.28: each mode gives ⅓ log(a/ε) + 𝓘(μ_ℓ)). Translated to
defect language with a/ε = 1/(2√(1−η)) (their 4.4): the bulk-channel coefficient density of the
two-defect Rényi-2 function must grow so that its partial sums scale as Λ^{1/2}; the exponent is
kinematic (the dimension of the entangling circle) and the amplitude is κ₂ by definition. The only
relation between "growth rate" and κ₂ available in the construction is this Tauberian identity, which
predicts nothing that was not used to state it. Outcome (A) is empty.

**Fact 3 — the sharpest form of the obstruction, read off at n = 2 (new here, arithmetic).** From
[BMW15b] (B.2)–(B.3) at n = 2 the fermionic sum has the single sector k = ½, a = k/n = ¼, so
c₂^f(t) = −2ω_{1/4}(t) = 2∫_t^∞ y u²_{1/4}(y) dy, and swapping the order of integration,

    κ₂^f = (1/π)∫₀^∞ c₂^f dt = (2/π) ∫₀^∞ y² u²_{1/4}(y) dy,       ∫₀^∞ y u²_{1/4}(y) dy = 1/8.

The second equation is the UV central charge: c₂^f(0) = (c/6)(1 + 1/n) = ¼ for c = 1, equivalently
ω_a(0) = −2a² (check: (1/(1−n)) Σ_k (−2k²/n²) with Σ_{k=−(n−1)/2}^{(n−1)/2} k² = n(n²−1)/12 gives
(n+1)/(6n); at n = 2, ¼). So in the solvable instance κ₂ and the universal UV datum are the **second
and first moments of the same positive profile y u²_{1/4}(y)**, a Painlevé transcendental with fixed
short- and long-distance asymptotics ((B.7): −½ log t at t → 0, (2/π) sin(π/4) K_{1/2}(t) at t → ∞).
Positivity, a fixed first moment, and a fixed decay rate do not fix a second moment; only the full
connection problem does. This is EXP-003's mass-versus-tail dichotomy realised inside the one
exactly solvable case, one step further down (in the 2d mode function itself). Grade: derivation
verified against the quoted equations; the number 0.0472338 not recomputed.

**Fact 4 — a physical pair with equal tail and different head ([AM26]'s own remark, d = 4).** "If the
sum begins at ℓ = 1 instead, (4.2) gives the RMI for the Rarita–Schwinger field in d = 4" (their §4.1).
The area term depends only on the top power of λ(ℓ) at ℓ → ∞ (their 4.18), so Dirac and
Rarita–Schwinger in d = 4 have the same κ₄, while the removed ℓ = 0 mode carries the leading
long-distance term (η^{2μ₀+1} = η³, the Δ = 3/2 fermion) and shifts the log coefficient (their 4.8,
ΔS = ⅙ log(a/ε) + 𝓘(1)). That is the truncation of RESULT.md Theorem (b) — cut the bottom of the
tower, keep the tail — realised by two free fields rather than by a constructed density. Caveats: it
is d = 4 not d = 3, and the entanglement entropy of the spin-3/2 gauge field carries the usual
edge-mode subtleties, which [AM26] address only by matching their ref. [41]; the pair is an
illustration, not part of the theorem.

**Outcome (B), stated as such.** κ₂ is exactly the tail; the construction contains no bound; and this
is confirmation of EXP-003/006/008, not news. The step tightens the obstruction from "no bridge
found" to: *in the one solvable instance the bridge is absent too, and the reason is visible — the
universal datum and κ₂ are different moments of one positive function.*

**What is not session-sized, and what it would need (outcome (C) for the remainder).**
(i) A closed form for ∫y²u²_{1/4}: a Painlevé connection-type integral; integrable-systems question,
no bearing on the bound. (ii) An independent 3d κ₂^f to test the identity: unnecessary, see Fact 1.
(iii) The actual open input, unchanged: a growth condition on the bulk-channel density of the
two-defect function that does not come from the tail itself. It would have to come from a second
positive expansion with a universal lowest state (absent for two balls in d ≥ 3, RESULT.md §6) or
from an analyticity-plus-growth argument of a type not yet available for defect fusion. Search terms
for a next person: defect fusion, Casimir energy of parallel conformal defects, cusp/fusion
anomalous dimensions; not surveyed here and no specific paper is cited.

**Not done, by decision.** The only sum-rule-shaped structure the solvable case offers is
cross-dimensional: κ_d ∝ ∫t^{d−3}c_n(t)dt are Mellin moments of one positive function ([AM26] 4.17,
[CH07]), so log-convexity in d must hold for free fields. It is a free-field statement about
dimensional reduction, not about the bound; the Casini–Huerta table of κ_d needed to check it did
not survive the text conversion of arXiv:0905.2562; left unchecked and listed in TODO.

**Grade** Facts 1–2: verified against the quoted equations. Fact 3: derivation verified; arithmetic
checked in two ways. Fact 4: verified as [AM26]'s statement; physical status of the RS entropy not
examined. Outcome (B): the null, as pre-registered.

## EXP-012  Target A, the cheap sub-question: is the sign of the trial-function residual universal?

**Date** 2026-09-05. **Status** complete from published tables plus the two validated exp001 modules;
one pre-registered prediction handed to the instrument (running, see end).

**Pre-registration.** r(θ) ≡ ã(θ) − a(θ), with ã the two-parameter (σ, κ) function of [BMW15b]
eqs (6.2)–(6.7) (= [HHCWM16] eq 21, = [BCV21] eq 261). Outcomes named before looking: (i) one sign
for all theories, all n, all θ; (ii) the sign is set by a single datum and flips with it; (iii) no
pattern. Inputs: exact smooth-limit coefficients σ_n^{(p)} for the complex scalar (8) and Dirac (7)
at n = 1–4 [HHCWM16] Tables 3–4 ("all shown digits are significant"); κ_n from [CHL09] Table 1 (n = 1)
and [BMW15b] Table 3; Einstein and ECG curves from `exp001_measure.py` / `exp001_ecg.py` (controls:
σ/C_T = π²/24, κ/C_T = π²Γ(3/4)⁴/6, σ_ECG/σ_E = 1−3μ, κ_ECG/κ_E = 1−123μ/20, all pass).
Script: `scripts/exp012_sign.py`. Its controls reproduce four entries of [HHCWM16] Tables 1–2.

**Where the free-field values come from, and how exact they are.** The Taylor series about θ = π has
radius π, so at θ ≥ 90° the truncated series (M = 7, 8 terms) is exact to < 10⁻⁴ relative; at 63.4°
to 7·10⁻⁴; below that [HHCWM16] eq (22) (series plus the geometric tail with σ^{(p)} → 2κ/π^{2p+3})
is used. Because the coefficients approach the asymptote from above ([HHCWM16] Fig. 3; measured excess
r of the last coefficient 0.0–0.8%), eq (22) is a lower bound with one-sided error ≤ r × tail: 0.01% at
45°, 0.03–0.05% at 26.6°. [CHL09]'s exact values at 90°, 135° agree with the series to all digits.

**Result A — the sign near θ = π is decided by one number.** ã has σ̃ = σ exactly and
σ̃′ = λ¹/π⁴ + λ²/45, a fixed linear function of (σ, κ); r ≈ (σ̃′ − σ′)ε⁴. Measured (σ̃′ − σ′)/σ′:

| | n = 1 | n = 2 | n = 3 | n = 4 |
|---|---|---|---|---|
| complex scalar | +1.53% | −1.08% | −1.39% | −1.42% |
| Dirac | +2.24% | −0.79% | −1.43% | −1.65% |
| Einstein | +1.65% | — | — | — |
| ECG μ = +0.00312 / −0.00322 | + / + (numerically, from the exact curves) | — | — | — |

**Result B — the interior sign follows it, with no node where tables can see.** (ã − a)/a in %:

| | 26.6° | 45° | 63.4° | 90° | 116.6° | 135° | 153.4° |
|---|---|---|---|---|---|---|---|
| Einstein | +0.92 | +0.79 | +0.57 | +0.31 | +0.14 | +0.07 | +0.02 |
| ECG μ=+0.00312 | +1.22 | +1.09 | +0.81 | +0.45 | +0.21 | +0.10 | +0.03 |
| ECG μ=−0.00322 | +0.62 | +0.49 | +0.33 | +0.17 | +0.07 | +0.03 | +0.01 |
| scalar n=1 | +0.01(3) | +0.16 | +0.22 | +0.19 | +0.12 | +0.06 | +0.02 |
| Dirac n=1 | +0.54 | +0.58 | +0.50 | +0.33 | +0.17 | +0.09 | +0.03 |
| scalar n=2 | −0.83(5) | −0.67 | −0.47 | −0.25 | −0.11 | −0.05 | −0.02 |
| scalar n=3 | −0.94(5) | −0.78 | −0.56 | −0.31 | −0.14 | −0.07 | −0.02 |
| scalar n=4 | −0.95(5) | −0.80 | −0.58 | −0.32 | −0.15 | −0.07 | −0.02 |
| Dirac n=2 | −0.21 | −0.22 | −0.19 | −0.12 | −0.06 | −0.03 | −0.01 |
| Dirac n=3 | −0.39 | −0.40 | −0.34 | −0.22 | −0.12 | −0.06 | −0.02 |
| Dirac n=4 | −0.45 | −0.46 | −0.40 | −0.26 | −0.14 | −0.07 | −0.02 |

[BCV21] Fig. 2 (1 − a/ã, curves ordered top to bottom by decreasing μ, "better for negative μ") is
reproduced in sign and ordering. [BMW15b] reported only |difference| ≤ 0.33% for the n = 2 scalar.

**Result C — the sign near θ = 0 is decided by a second number, and it is a defect datum.** With
a = κ/θ + a₀ + O(θ): ã₀ = −¾λ¹ = (3π/2)(3πσ − κ)/(π² − 6), so r(0⁺) = ã₀ − a₀. For Einstein the
exact curve gives a₀ = 0 to four digits (a − κ/θ = −0.9424 θ at θ = 0.02, 0.01, 0.005, 0.0025), so
r(0⁺) = +0.203 C_T > 0 and the Einstein residual is single-signed. ã₀ in units of C_T: Einstein
+0.203, ECG +0.248 / +0.158, Dirac n=1 +0.092, scalar n=1 −0.370, scalar n=2 −0.373, Dirac n=2
−0.023 (sign of 3π − κ/σ; the physical band κ/σ ∈ [8.9, 11.0] straddles 3π = 9.42). For the free
fields a₀ is not in any table. Structure from the cusp literature (EXP-013): a_n(θ) = Γ^{(n)}(θ)/(1−n)
with Γ the cusp anomalous dimension of the twist line, whose fusion expansion is
Γ = C/θ + Δ_tip + … with Δ_tip the dimension of the operator creating the defect pair at the tip
[CHK24 eq 2.12]. If that operator is unitary, Δ_tip^{(n)} ≥ 0 for n > 1, so a₀^{(n)} ≤ 0 and
a₀^{EE} = −∂_nΔ_tip|_{n=1} ≤ 0 (my inference from their general structure; not verified for twist
defects). Consequences: Dirac n = 1 has r(0⁺) = 0.092 C_T − a₀ ≥ 0.092 C_T > 0 — single-signed at all
angles, as the data show; the scalar at n = 1 has r(0⁺) = −0.370 C_T − a₀, negative iff
a₀ > −0.370 C_T (= −0.0035 in real-scalar units) — a node below 26.6°, consistent with the +0.01(3)%
measured there and undecidable from tables.

**Verdict.** Outcome (ii): the sign is *not* universal, but it is not patternless. It is uniform across
all five n = 1 theories at every angle where data exist (trial above exact), uniformly opposite for
both free fields at n = 2, 3, 4, single-signed in θ in every decidable case, and set at each end of
the interval by one number: σ′ − σ̃′ at the smooth end, a₀ − ã₀ at the sharp end.

**What this constrains before any mechanism is built.** (1) A mechanism must make the second spectral
moment ⟨s²⟩ = 12σ′/σ fall *below* the two-basis interpolation at n = 1 for free fields, Einstein and
ECG alike, and *above* it at n ≥ 2. (2) It must be a statement about one number per end, not about the
whole curve: fixing σ′ (respectively a₀) in addition to (σ, κ) would remove the residual to the level
of the next coefficient, which is what [HHCWM16] eq (22) does. (3) δ ≡ σ′/σ̃′ − 1 is not a function
of κ/σ alone (Einstein 9.02 → −1.6%; Dirac n = 2 9.50 → +0.8%; Dirac n = 1 9.24 → −2.2%), so the
n-dependence is genuine and the n = 1 (entanglement) point is on the opposite side from all n ≥ 2.
(4) The trial function's accuracy is not mysterious once stated this way: all theories have
κ/σ within 15% of the EMI value 3π and σ′/σ within 5% of the EMI value 1/15; the residual is the
≈2% by which the true σ′ misses the line through the EMI and Lifshitz points.

**Pre-registered for the instrument (scalar EE production launched 2026-09-05, 672 nodes, M ≤ 15,
n_t = 14, t_max = 3.2, reusing 97 validated nodes; Tier-1 continuity control EE(t → 0) vs Rényi-2
passed: deviation ∝ t², 0.03% at t = 0.022, no branch jump).** (P1) a₀ ≤ 0 for the real scalar.
(P2) If a₀ > −0.0035, the n = 1 scalar residual changes sign below 26.6° with the exact function
above ã at small angles; with a₀ = 0 the leading estimate is r/a ≈ −8.8% × θ(rad), which the Einstein
case suggests is reduced ≈2.7× by O(θ) terms, i.e. ≈ −1% by 15–20°. (P3) The run must first
reproduce [HHCWM16] Table 1 (α = 1) at 63.4°–153.4° to the series precision and [CHL09] at 90°, 135°;
its first disagreement with a table is evidence about the solver, not about the table. Failure of P1
would falsify the tip-unitarity inference; failure of P3 stops everything downstream.

**Grade** Results A, B: verified (published exact coefficients; validated modules). Result C: Einstein
verified; the Δ_tip identification and a₀ ≤ 0: unverified inference, labelled. Verdict: as stated.

## EXP-013  Target B: the missing growth condition exists in the literature, it is one-sided, and here is why

**Date** 2026-09-05. **Status** complete as a reading plus one explicit construction; no computation.

**Pre-registration.** RESULT.md §6 named its falsifier: "a third bridge that supplies a growth
condition at the tail end." Outcomes: (i) found in the literature; (ii) constructed here; (iii) proven
impossible; (iv) not session-sized. Sweep rule from PHASE2 applied: the queries contained neither κ
nor C_T — they asked for cusps, defect fusion, Casimir energies, Regge/causality for defects, cross-n
inequalities, energy-flux positivity with twist defects.

**Finding 1 — the object.** In d = 3 the entangling corner is a cusp on the replica twist *line*
defect of CFT^n/Z_n, and the corner function is its cusp anomalous dimension:
Γ^{(n)}_twist(θ) = (1 − n) a_n(θ) [LMW26 eq 35; the same identification is stated in the
introductions of CGT26 and Cha26]. The 2024–26 "cusp" papers are therefore about this object, not a
different one. The sibling's filing in PHASE2 ("cusped line defects, not entangling-surface corners")
checked the noun against the wrong object: cusped line defects *include* the twist line, and one of
those papers derives corner bounds explicitly. Correction recorded in TODO for the bridge.

**Finding 2 — the third bridge, as published.** [LMW26] bootstrap a rectangle of line defects
(L_x × L_y): ⟨𝔇(L_x, L_y)⟩ = ⟨staple| e^{−L_y Ĥ(L_x)} |staple⟩ = 𝒟(y)/A^{2Γ}, y = L_x/L_y,
Γ ≡ Γ^{aā}(π/2) (their eq 12); the x ↔ y symmetry is a modular relation 𝒟(y) = 𝒟(1/y) (13); and
𝒜(y) ≡ y^{−2Γ} e^{−ε₀ y} 𝒟(y) = ∫₀^∞ S(ε) e^{−yε} dε with S ≥ 0 by OS positivity (14–15), where
ε₀ = ε^{aā} is the Casimir energy of the defect and its conjugate, V(L) = −ε^{aā}/L. An analytic
"magic" functional gives Γ^{aā}(π/2)/ε^{aā} ≥ −3/(2π) (their eq 1), optimal for these constraints and
saturated by every 2d BCFT (𝒟 = y^{2Γ}η^{8Γ}(iy), Γ = −c/16, ε₀ = πc/24). For twist defects, with
ε^{(n)} = (n−1)κ_n (the same normalisation as RESULT.md §6's open-channel reading E₀ = −(n−1)κ_n/w):

    κ_n ≥ (2π/3) a_n(π/2)    (their eq 38),    κ_n/σ_n ≥ π³/6 = 5.17   (eq 39, using a_n(π/2) ≥ σ_n π²/4),
    κ_EE ≥ (π⁵/144) C_T = 2.125 C_T   (eq 40, "assuming the magic bound persists in the n → 1 limit").

Their eq 37 uses the weaker input a(π/2) ≥ σπ²/4; with the theorem a(π/2) ≥ 𝔞_min(π/2) = 4σ log 2
[BWK16 + FLP16] the same step gives **κ/C_T ≥ (π³ log 2/9) = 2.387** and κ/σ ≥ 5.81 (my combination,
same n → 1 assumption). Data: (2π/3) a(π/2)/κ = 0.62 (scalar), 0.68 (Dirac), 0.69 (Einstein),
0.69/0.69 (ECG), 0.60–0.66 at n = 2–4 — satisfied everywhere with 30–40% to spare; the rigorous window
is now κ/C_T ∈ [2.39, ∞) against the observed [3.67, 4.18].

**Finding 3 — what this corrects in RESULT.md §6, and what it confirms.** §6 required the inverted
channel's lowest state to be *universal*, and dismissed the strip channel because its vacuum energy
is the non-universal κ. That requirement was too strong. It suffices that the tail coefficient itself
be the vacuum energy of a *self-dual* crossing: the rectangle puts κ_n at the bottom of both channels
and its four right-angle corners bring a_n(π/2) into the same equation, so the non-universal mass
gets traded against another value of the same function. In d = 2 this is exactly the Cardy mechanism
(corners c/16 by Cardy–Peschel, strip energy πc/24 — the bound is an equality); in d = 3 it is an
inequality. The falsifier fired, in the narrowed form "a third bridge exists and is one-sided."
The new inequality is not a consequence of C1–C6: 𝔞_min (κ = 0, a(π/2) = 1.14 C_T) violates it, so
the [BWK16] lower-bound curve is not the corner function of any theory satisfying [LMW26]'s
assumptions.

**Finding 4 — the bridge is one-sided, by an explicit admissible solution (new here).** Within the
constraints that produce the magic bound (S ≥ 0 and 𝒟(y) = 𝒟(1/y)), take

    𝒟(y) = exp[ε₀ (y + 1/y)],   Γ = 0:   𝒜(y) = e^{ε₀/y} = Σ_k ε₀^k/(k! y^k) = ∫₀^∞ S(ε) e^{−yε} dε,
    S(ε) = δ(ε) + Σ_{k≥1} ε₀^k ε^{k−1}/(k!(k−1)!) ≥ 0.

It is modular invariant, OS-positive, has any ε₀ > 0 and a vanishing corner dimension, i.e.
a(π/2)/κ = 0 at κ > 0. Hence these constraints cannot bound κ above at fixed a(π/2), only below — the
same pure-Casimir, tail-only object as RESULT.md §7's Q = e^{(n−1)κℓ/w} and the truncated family of
Theorem (b), now inside the rectangle bootstrap. Whether further cutting-and-gluing relations (other
polygons, the cuboid of [LMW26]'s end matter) exclude it is open; nothing published does.

**Finding 5 — the rest of the 2024–26 structure, mapped onto Phase 1.**
- [DKPW24] eq (2.10), F = Vol(ℍ^p) ℰ/θ^p as θ → 0: the strip/corner identity in general-defect form;
  prior art for §6's "κ_n is a Casimir energy in the other channel". ℰ is stated to be new data.
- [KRS25]: a₀ ≥ 0 (Thm 3.1), inequalities between a₀ of different fusions (Thm 3.2), and the density of
  bulk one-point coefficients log ρ(Δ, J) ~ √(8πa₀Δ)[1 − ½j² − …] for line defects in d = 3 (eq 11):
  the growth of the one-point coefficients is *fixed by* the Casimir coefficient, not bounding it — the
  Tauberian direction of EXP-006/011, now general. [BCGKM26] §6 do the same for the density of cusp
  operators from a two-cusp crossing (cusp-operator channel vs fusion channel).
- [CHK24]: Γ < 0, Γ′ > 0, Γ″ < 0 by reflection positivity of displacement two-point functions on
  opposite edges (= C2 in cusp language), Γ″(π) = −C_D/6 (= σ_n ∝ C_D of [BMMS16]), and the Casimir
  energy of a defect with its reversal is attractive (= κ_n ≥ 0, RESULT §5).
- [CGT26]: Lorentzian cusps; Rindler positivity gives Γ^L ≥ 0 — the analyticity route yields a
  positivity, not an upper bound, as §6 anticipated. [Cha26]: complete monotonicity of Γ in a
  reflection-symmetric variable, stated as a conjecture from examples; possibly the cusp-side form of
  C4 (proved for twist defects at integer n by [CH12]); not checked.
- No paper bounds a Casimir energy from above in terms of other data; none was found that connects the
  n → 1 twist bound to entanglement beyond [LMW26]'s eq 40.

**Verdict.** Outcome (i)+(iii) together: the growth condition Phase 1 asked for exists (the rectangle
crossing, [LMW26]), it bounds the tail from *below*, κ ≥ (2π/3)a(π/2), and it provably cannot bound it
from above within the constraints used, by the solution of Finding 4. The theorem of RESULT.md §4
stands unchanged and is strengthened in scope: C1–C6 together with the rectangle crossing localise
κ/C_T only to [2.39, ∞). The upper edge of the observed band, 4.18 at the free scalar, is explained by
no known constraint. Closing the problem would require a constraint that excludes pure-Casimir
solutions, i.e. dynamical input beyond OS positivity and the self-dual crossing.

**Grade** Finding 1: verified (three independent statements in the sources). Finding 2: verified
against [LMW26]'s equations as extracted; the numerical sharpening is my arithmetic on their step.
Finding 3: reasoning, checked on the d = 2 case. Finding 4: verified (a two-line computation, the
Laplace transform of 1/y^k). Finding 5: verified as the sources' statements; proofs not read.

### EXP-012 addendum (2026-09-05) — the Dirac known-answer control FAILED; diagnosis; one-variable fix under test

**The control.** Before any Dirac EE production, the Rényi-2 Dirac mode (`dirac2`: a = ±½, no
t-integration, 48 mass nodes, M ≤ 15) was run against exact targets: σ₂^f = 1/(64π),
σ₂′^f = (35π−8)/(30720π²) [HHCWM16 Table 4], and the seven α = 2 fermion angles of [HHCWM16] Table 2
(0.0955, 0.0503, 0.0302, 0.01496, 0.006669, 0.003204, 0.001085). Result: **fail, decisively.** The
assembled s₂(θ) is negative, −0.84 × the exact value from 45° to 117° (e.g. −0.01263 vs +0.01496 at
90°), and structurally wrong near π (s(160°) ≈ s(170°) ≈ +2·10⁻⁴ instead of scaling as ε²). The run
and its 48 nodes are kept (`scripts/exp004_nodes/dirac2_*`, `exp004_dirac2_result_*.json`) as the
control for any fix. The Dirac EE production was not launched.

**Why the check fired (asked before acting).** The references are solid — closed forms and a table
whose other entries the scalar mode reproduces — so the routine is wrong, not the check. Node-level:
at the lowest mass (M = 0.5001, m = 0.0096) the regularised vertex term is ≈ −5.4·10³ against a scalar
piece of 0.03, and the per-node subtraction Ψ_π = +5396.6; Ψ_π scales as m^{−2.00} between the first
two nodes. The first four mass nodes alone contribute −0.030 to s₂(90°), overwhelming the true +0.015.
Cause, from the solver's own leading-order relations at a = ½: the denominator of the vertex term,
4β₁² − b² sin²x → ε²(4(β₁¹)² − b₀²) = ε² m²/M², vanishes like m² *identically* (verified numerically:
D/m² → 4.00); the numerator as transcribed from [CHL09] eq (59), 4β₁X₁cos(x/2) − bB₁sin²x →
ε²(2β₁¹X₁⁰ − b₀B₁⁰), does not: 2β₁¹X₁⁰ = −0.1061 and b₀B₁⁰ = +0.0530 at m = 0.0096, so the two terms
*add*. A straight line has no vertex term, so the ratio must be finite at every m; with these boundary
values that requires the second term's coefficient to be −2 rather than +1 in the solver's conventions
— and indeed 2β₁¹X₁⁰/(b₀B₁⁰) = −2.0011, −2.0303, −2.1851, −2.6641 at m = 0.0096, 0.0505, 0.1235,
0.2272, i.e. −2 − 11.85 m² + O(m⁴): an exact cancellation at m → 0 with a smooth O(m²) remainder. The
scalar sector cannot see this: H¹ = 1/(16πa(1−a)) + M(β₁¹X₂⁰ + β₂¹X₁⁰) does not contain B₁, and at
a = ½ the system is 1 ↔ 2 symmetric, so no index swap is diagnosable either. Whether the −2 is a typo
in eq (59), a convention difference in B₁, or my transcription, is not established.

**The fix under test, one variable.** New mode `dirac2r`, identical to `dirac2` except that the
coefficient of b B₁ sin²x in the numerator (and correspondingly in Ψ_π) is −2 instead of +1. Chosen
by the regularity requirement, *not* by the target numbers. Launched 2026-09-05 at two workers.
Pass criterion, fixed in advance: the assembled s₂(θ) agrees with the exact series at θ ≥ 63.4° to
≤ 10⁻³, with eq (22)/Table 2 at 45° and 26.6° to ≤ 2·10⁻³, and s(170°)/(σ₂ε² + σ₂′ε⁴ + σ₂″ε⁶) = 1 to
10⁻⁴. Anything else: the Dirac branch stays parked with this record.

### EXP-012 addendum 2 (2026-09-05) — the one-variable fix removes the singularity and still fails; Dirac branch parked

**Result of `dirac2r`** (48 nodes, 0 failures) against the pre-registered criterion: **FAIL.** The
small-mass singularity is gone — the assembled s₂(θ) is finite, positive for θ ≥ 20°, and scales as
ε² near π — but it is 2.00–2.03 × the exact value at 153°–170°, 1.58 × at 90°, 0.84 × at 45°,
0.33 × at 26.6°, and negative below 20°. Both failed runs are kept (`dirac2_*`, `dirac2r_*` nodes and
result files).

**What the failure localises.** The computed function is A − V with A = 2 s₂^{cs}(θ) the validated
scalar-like piece (2m tr G_S integrated) and V the vertex term. The exact vertex term is therefore
V_true = 2 s₂^{cs} − s₂^f, positive at every angle, with smooth-limit coefficient
2σ₂^{cs} − σ₂^f = 2/(24π²) − 1/(64π) = 0.003469. The computed V: −0.49 × V_true at 170°, −0.43 × at
153°, −0.31 × at 135°, +0.21 × at 90°, +0.73 × at 63°, +1.21 × at 45°, +1.79 × at 26.6°. A sign change
near 75° and the wrong sign near π cannot be produced by any constant rescaling or sign flip of the
term, and the per-node subtraction of Ψ_π cannot produce it either (a constant offset would not scale
as ε²). So the vertex term as implemented has an *angle-dependent* error — a cos(x/2) ↔ sin(x/2),
sin²x ↔ sin²(x/2), or tan(x/2)-structure mismatch between [CHL09] eq (59)/App. B and the solver's
variables — in addition to the m → 0 normalisation that the −2 repaired.

**Parked, with the check a next person needs.** The vertex term's smooth-limit coefficients are exact
and independent targets: V → (2σ₂^{cs} − σ₂^f)ε² + (2σ₂′^{cs} − σ₂′^f)ε⁴ + …, i.e. 0.003469 ε² +
[2(5+π²)/(480π⁴) − (35π−8)/(30720π²)] ε⁴. Like H¹ for the scalar, these are computable from the
series start at each mass (no ODE integration) followed by the mass quadrature, so any candidate
transcription of eq (59) can be tested in seconds against two exact numbers before a 48-node run.
Neither the old nor the −2 transcription passes that test (the old one is singular; the new one gives
−0.0017 for +0.003469). The Dirac EE production stays unlaunched; its prediction ("no node, trial above
exact at all angles, a₀ ≤ 0") stays pre-registered and untested.

**Grade** verified: both control outcomes, the decomposition A − V (A is the validated scalar
integral), the exact V targets. The diagnosis of *which* angular structure is wrong: not established.

### EXP-012 addendum 3 (2026-09-05) — dry run of the analysis on the Rényi-2 result: truncation measured, and a first sharp-end constant

Run before the EE result exists, so that the analysis script meets known numbers first
(`scripts/exp012_ee_analyze.py` on `exp004_renyi2_result_n24_24_p15.0_t1.json`, real scalar, n = 2).

**Truncation, measured rather than estimated.** Against [HHCWM16] eq (22) (complex/2): −8.0% at 5°,
−0.51% at 10°, then +3.7·10⁻⁴, +5.3·10⁻⁴, +3.1·10⁻⁴, +2.2·10⁻⁴, +0.8·10⁻⁴ at 15°, 20°, 26.6°, 30°, 40°
(positive and within eq (22)'s own one-sided error r × tail ≈ 4.6·10⁻⁴ at 26.6°), and ≤ 4·10⁻⁴ from
45° to 153° against the exact series; smooth limit exact to 10⁻¹². So the M ≤ 15 mass cutoff
contaminates 5° and 10° and nothing above: the earlier note "≈4·10⁻⁴ relative at 5°" (TODO,
from an extrapolated decay rate) was wrong by two orders of magnitude and is withdrawn. Protocol
consequence: the sharp-end fits use windows starting at 15°.

**Residual sign at n = 2 from the instrument** (trial − s)/s: −0.13% at 10°, −0.80% at 15°, −0.86% at
26.6°, −0.68% at 45°, −0.25% at 90°, −0.05% at 135°, −0.002% at 170° — negative at every angle from
10° to 170°, as EXP-012 Result B found from tables; the +8% at 5° is the truncation artifact above,
not a node.

**A new number: the Rényi-2 real-scalar sharp-end constant.** With κ₂ fixed at 0.0455996/2 and
s − κ₂/θ fitted to a₀ + a₁θ + a₂θ² (+ a₃θ³): a₀ = −0.00236 (15–45°, degree 2), −0.00228 (15–45°,
degree 3); windows reaching down to 10° or 5° drift to −0.004 … −0.06 and are excluded for the
reason above. So **a₀^{(n=2)} = −0.0023 ± 0.0003** (drift, not a statistical error), i.e. −0.24 C_T.
Checks: negative, as the tip-unitarity inference requires (Δ_tip^{(2)} = (1−n)a₀ = +0.0023 ≥ 0);
above the trial function's ã₀ = −0.00354, so r(0⁺) = ã₀ − a₀ = −0.0012 < 0, consistent with the
single-signed negative residual at n = 2. Grade: instrument verified to ≤ 5·10⁻⁴ on the window used;
the fit is model-dependent at the ±0.0003 level quoted; the interpretation as a defect-creation
dimension is the unverified inference of Result C.

### EXP-012 addendum 4 (2026-09-05) — scalar EE production: validated from 50° up; the small-angle end is not yet measured

**Run.** 672 nodes (48 masses ≤ 15 × 14 Gauss–Legendre t-nodes on [0, 3.2]), no failures,
`exp004_ee_result_n24_24_p15.0_t14.json`, analysed with `exp012_ee_analyze.py` in the pre-registered
order.

**P3 (contact with published values): PASS from 63.4° to 170°, and the instrument is better than the
references there.** Against the exact series [HHCWM16 Table 3, α = 1, /2]: −9.8·10⁻⁷ uniformly from
100° to 170° (a constant 10⁻⁶ offset, the same as σ from H1: 0.999 999 0 × 1/256 and σ′ from H3:
0.999 999 3 × exact — the t-quadrature's residual), +1.0·10⁻⁵ at 90° (CHL09's 0.01183: +2.9·10⁻⁴,
i.e. CHL09's last digit), +5.9·10⁻⁵ at 80°, +2.0·10⁻⁴ at 70°, and at 63.4° the value sits 7·10⁻⁴
*above* the truncated series, which is exactly that series' own one-sided truncation error at that
angle (re-assembly with M ≤ 11 gives +7.3·10⁻⁴ at 63.4° and −2.5·10⁻⁵ at 50°).

**Residual sign at n = 1 from the instrument** (trial − s)/s: +0.23% (70°), +0.21% (80°), +0.193%
(90°), +0.115% (116.6°), +0.062% (135°), +0.023% (153.4°), +0.003% (170°) — positive throughout,
matching EXP-012 Result B's table values (+0.19, +0.12, +0.06, +0.02) to the last digit.

**Below 50°: the run is garbage, and the cause is localised, not yet fixed.** The assembled s(θ)
blows up to −0.76 at 45° and −2.8·10⁹ at 5°. Node by node, |F(5°)| is physical (10⁻³·⁹ and falling
with M) for every node with t = 0.02 up to M = 7 and for every real-a (Rényi-2) node up to M = 15,
but for complex a it is 100× too large already at (M = 7.1, t = 0.11), spreads to all t by M ≈ 12,
and reaches 10⁷–10⁸ at M ≈ 15, with random signs. The onset mass rises with t (≈7 at t = 0.1, ≈11 at
t = 2.7). No branch flag accompanies the onset (branch −1, 0 flips at M = 7.1, t = 0.11). A mass
cutoff cannot rescue small angles: with M ≤ 8 the 5° value is still 5× too large, because the
garbage begins below the mass where the physical contribution at 5° is exhausted (the Rényi-2 run
needed M > 15 there). Diagnosis in one sentence: the complex-a integration loses the physical
solution against the growing mode e^{2M(π−x)} at small x for M ≳ 7 with the precision rule
dps = 25 + 3M that suffices at real a; the one-variable test (the same node at higher dps) is
next. Until it passes, **P1 and P2 are undecided**; the pre-registered predictions stand.

**What is measured.** For θ ≥ 50° the free-scalar corner function at n = 1 is now known to ≤ 10⁻⁵
(≥ 70°) and ≤ 10⁻³ (50°–63°) independently of [HHCWM16]'s series, and agrees with it. That is a
confirmation of published numbers, not news; the news this run was built for lives below 45°.

### EXP-012 addendum 5 (2026-09-05) — the small-angle failure is precision, proved on one node; re-run designed

**One-variable test** (`scripts/exp012_precision_test.py`, node M = 7.1317, t = 0.1145, the first
garbage node). With the production rule dps = 25 + 3M = 46 the node reproduces its stored values to
every digit (F(5°) = 9.134·10⁻³, F(90°) = 1.136·10⁻¹², H1 = 1.934·10⁻¹⁹). With dps = 70 and dps = 100
it gives identical values (F(5°) = 1.3171·10⁻⁴, F(26.6°) = 7.248·10⁻⁷, F(90°) = 1.755·10⁻¹³,
H1 = 2.833·10⁻¹⁹), and F(5°) matches the 1.36·10⁻⁴ expected from the t = 0.02 neighbour times the
smooth (¼ + t²) factor. Tightening every tolerance by 10⁸ at dps = 70 changes nothing. So the cause
is the digits rule alone: it suffices at real a (the Rényi-2 run was correct to M = 15) and not at
complex a, where even F(90°) and H1 were wrong by 6× and 1.5× at M = 7 — invisible in the assembled
90° value only because that mass contributes 10⁻¹² there.

**Re-run design (mode `eehp`, same solver, one change: the digits rule).** dps = 25 + s·M with the
slope s calibrated at M = 11.24, t = 0.50 (dps 59 = rule, 80, 100, 120; running). Grid: the same 48
masses to M = 15; t-nodes reduced to 10 Gauss–Legendre points on [0, 2.2], dropping the four largest
of the old grid: the weight 2/cosh²(πt) has ∫_{2.2}^∞ / ∫_0^∞ = 2·10⁻⁶, angle-independent, so the cut
costs nothing at the 10⁻³ level the sign question needs while removing the slowest 30% of nodes.
Smoke test passed on two production-grid nodes (files written, reusable). Cost estimate after
calibration; the M ≥ 7 nodes dominate.

**What stays fixed.** The predictions P1–P3 and the fit protocol (windows from 15°, κ fixed, drift
reported) are unchanged; the old run's nodes are kept; the new run's first job is again P3 — now with
the 15°–45° values of eq (22) as the referee, which the old run could not reach.

### EXP-012 addendum 6 (2026-09-05) — the measurement: P1 and P2 confirmed, the node found, a₀ measured

**Run** `eehp`: 480 nodes (48 masses × 10 t-nodes on [0, 2.2]), dps = 50 + 5M, no failures. Two
instrument facts first, because they set the error bars. (i) The higher digits cured every node up
to M ≈ 13.1 (smooth in t, consistent with the calibrated nodes, branch = +1 nodes included), but the
top five masses M ≥ 14 are garbage even at 120–125 digits — a *different* failure, not precision; they
are excluded by assembling with M ≤ 13.1 (`exp004_eehp_result_Mcut13.1.json`, 420 nodes). The cost of
that cutoff, measured by moving it: −5.5·10⁻⁴ at 15°, −9·10⁻⁵ at 20°, −7·10⁻⁶ at 26.6°, −4·10⁻⁹ at 45°
per 0.5 unit of M; against eq (22) the deficit is −1.6·10⁻³ at 15° and −1.0·10⁻⁴ at 20°. (ii) Reducing
the t-grid from 14 nodes on [0, 3.2] to 10 on [0, 2.2] — a second variable changed in the same run,
against Rule VI — costs a uniform normalisation of −1.874·10⁻⁴ (σ from H1 = 0.999 813 × 1/256; the same
−1.87·10⁻⁴ against the exact series at every angle from 100° to 170°). It is known exactly and is
divided out below; it would have been avoided by keeping the old grid.

**P3 — contact with published values: PASS.** After the known normalisation, the instrument agrees
with the exact series to ≤ 5·10⁻⁵ from 70° to 170° and with eq (22) to ≤ 5·10⁻⁵ from 26.6° to 60°
(26.6°: −1.9·10⁻⁵, 30°: −5·10⁻⁵, 40°: −1.2·10⁻⁴ raw = +6·10⁻⁵ corrected, 45°: −1.4·10⁻⁴ raw); CHL09's
0.01183 and 0.002520 to their last digit. 20° carries the 1·10⁻⁴ cutoff deficit, 15° the 1.6·10⁻³ one;
10° and 5° remain truncation-dominated (−1.5%, −13%) and are not used. This is the first independent
four-digit determination of the free-scalar entanglement corner function between 20° and 60°.

**P2 — the sign below 26.6°: node found.** Residual (ã − a)/a after both corrections: +0.213% (60°),
+0.181% (50°), +0.155% (45°), +0.121% (40°), +0.031% (30°), −0.007% (26.6°), −0.069% (20°),
−0.107% (15°, using the eq (22) deficit; between −0.09% and −0.18% depending on how much of eq (22)'s
own one-sided error is real). The residual changes sign at **27 ± 3°** (the uncertainty is the
normalisation's possible angle dependence, ±5·10⁻⁵) and the exact function lies *above* the trial
function below it, by ≤ 0.1% down to 15°. This is exactly the case EXP-012 Result C left undecided
(+0.01(3)% at 26.6° from tables): the node sits at the last angle the tables could reach.

**P1 — the sharp-end constant: a₀ ≤ 0 confirmed, and measured.** With κ fixed at 0.0397 and windows
from 20°: a₀ = −0.00321, −0.00300 (20–50°, degrees 2, 3), −0.00330, −0.00301 (20–60°), −0.00340,
−0.00302 (26–60°), −0.00316, −0.00300 (20–45°), −0.00331, −0.00292 (26–50°); over all windows,
degrees and κ = 0.0397 ± 0.00005 the range is [−0.00362, −0.00259], median −0.00317. So

    a₀^{EE}(real scalar) = −0.0032 (−0.0036 … −0.0026) = −0.33 C_T (−0.38 … −0.27),

against the trial function's ã₀ = −0.00351 (−0.370 C_T). The difference a₀ − ã₀ = +0.0003
(−0.0001 … +0.0009) is what makes the node exist and makes it shallow; the negative residuals at
15°–20° confirm its sign independently of the fit.

**The a₀ table so far** (units of C_T; ã₀ = (3π/2)(3πσ − κ)/(π²−6)):

| theory | a₀ | ã₀ | r(0⁺) = ã₀ − a₀ | node |
|---|---|---|---|---|
| Einstein, n = 1 | 0.000 (exact curve) | +0.203 | +0.203 | none |
| real scalar, n = 1 | −0.33 (−0.38 … −0.27) | −0.370 | −0.04 (−0.10 … +0.01) | at 27 ± 3° |
| real scalar, n = 2 | −0.24 ± 0.03 | −0.373 | −0.13 | none (negative throughout) |
| Dirac, n = 1 | unmeasured (branch parked) | +0.092 | ≥ +0.09 if a₀ ≤ 0 | none predicted |

If a₀ = −∂_nΔ_tip|_{n=1} (the CHK24 structure, unverified for twist defects), the free scalar's
tip operator has ∂_nΔ_tip = +0.0032 at n = 1 and Δ_tip = +0.0023 at n = 2; Einstein's vanishes at
leading order in 1/N. Both scalar numbers are positive, as unitarity requires.

**Grade** P3: verified. Node and sign below 27°: verified at the level of the stated corrections.
a₀: measured; the quoted range is a systematic drift, not a statistical error; the κ value is CHL09's
to three digits. Δ_tip interpretation: inference, labelled. Instrument lessons recorded above.

## EXP-014  Independence audit of the cuspis ↔ vestigium edge (answering the bridge's A4)

**Date** 2026-09-22. **Status** complete; reading and file comparison only, no compute. Asked by the
bridge, which is auditing the family's founding claim that the repos are kept ignorant of each other.
Read-only rule observed: `../quantum` was read, never written.

**Q1 RECEPTION — content crossed, but no match was ever counted as evidence.** The only sibling
content load-bearing in my work is `../quantum`'s lattice corner values (a(60°) = 0.024232,
a(90°) = 0.011604 / 0.011673, a(120°) = 0.0038955), read directly from their `qsim/*.json` in EXP-001
and quoted as comments in `scripts/exp001_measure.py:100`. They entered as a *referee*, and the
comparison **failed**: a(120°) sat 13.3% below a rigorous lower bound. I then retired them as Tier-3
referee in favour of [CHL09] Table 1 and [HHCWM16] Tables 1–2. By the audit's own definition (an edge
requires content received *and* a match counted as evidence) this is not an echo edge — the only
number I ever compared to theirs disagreed, and the disagreement is what I reported.

**Q2 CODE — the coupling is real, it is file-level, and it runs cuspis → vestigium.** I imported
nothing from any sibling: no code, no data, one comment line quoting three of their numbers. The
transfer is in the other direction and is larger than the audit's question assumes.
`../quantum/corner_function/` is a **copy of this workspace** — `RESULT.md`, `TODO.md`, `report.md`,
`references.md`, my `scripts/` including the solver, my result JSONs and 145 of my node files —
imported 2026-09-05 via thebridge-d1 and documented in their `PROVENANCE.md`. Checked by hash:
`exp004_mp.py`, `exp004_ch_solver.py`, `exp001_measure.py` are **byte-identical** to mine.
*Mitigation, verified:* their two check scripts (`scripts_check/check_kappa.py`,
`check_truncated_hankel.py`) import numpy and scipy only — not my modules — and re-derive the algebra.
Their verification of the analytic theorem is therefore genuine independent code, not a re-run of mine.

**Q2b — the echo channel that does exist, and it is the reverse of the one flagged.** I handed them
the [BWK16] bound: prefactor exactly 1/32 and the three targets 0.0216610, 0.0108304, 0.0044950.
Their `qsim/CORNER_BOUND_FINDINGS.md` opens "The bound is real and I verified it independently",
then their repaired extraction was accepted when it came into consistency with those numbers.
**My number became their acceptance criterion.** Had the bound been wrong, the corrected lattice value
would have been tuned to a wrong target and the agreement manufactured. Their own retraction
("consistent with the bound, not satisfying it", my `TODO.md`) shows the over-claim was caught, but
the structure stands and it means: *their post-repair a(120°) is not independent of this repo, and
must never be used to corroborate anything here.*

**Q2c — shared validation target, the failure mode the bridge named.** Partially yes, and it is
ordinary. Both repos take σ = π²C_T/24 [FLP16] and C_T = 3/(32π²) as ground truth and both cite
[CHL09]. If either is wrong, both of us are wrong in the same direction. This is shared dependence on
the published literature rather than on each other; it is not an artifact of the bridge, but it does
mean agreement between us on any quantity resting on those two inputs is one measurement, not two.

**Q2d — why the coupling does not reach the result that needs a referee.** Their corner data exists
only at 60°, 90°, 120°. My unrefereed region is 20°–45°. They hold no value below 60°, so they can
neither corroborate nor contaminate the node at 27 ± 3° or a₀ = −0.33 C_T. **Corollary that matters
for the outside reviewer's recommendation:** because `../quantum` holds a byte-identical copy of my
solver, an independent re-implementation cannot be sourced from there. Any future run of that copy
reproducing my magnitudes is an echo by construction, and would satisfy the recommendation only in
appearance.

**Q3 REFUSED / DECLARED-NULL.** (i) Never wrote to any sibling; the a(120°) finding was placed in my
own `TODO.md` marked "for the bridge, not for this session to fix. Not modified (read-only)".
(ii) Declined to message the sibling session directly when the user ruled cross-repo traffic goes
through the bridge. (iii) Retired `../quantum` as Tier-3 referee rather than use numbers I had just
shown to violate a bound. (iv) EXP-010: declined to build a mechanism for the c_S coincidence and
reported the null. (v) Phase 2: declined to apply the relayed instruction "check the object, not the
noun" as written, because followed literally it excludes [LMW26], the paper that answers Target B;
the bridge has filed that postscript.

**Q4 UNLOGGED CHANNELS — the largest single finding, and the census structurally cannot see it.**
Sibling content entered my primary documents as **direct commits made outside my sessions**, never as
a message to me:

| commit | what it carried into which file |
|---|---|
| 071bbc6, ed29f8b, 8a7747e | `../quantum`'s a(120°) resolution, its retraction, and forward guidance → `TODO.md` |
| 5131089 | `../quantum`'s verification → `RESULT.md`, as the banner that is the load-bearing "INDEPENDENTLY VERIFIED" claim in this repo |
| ee2453a | `../quantum`'s enumeration of constraint families → `RESULT.md` §0 |
| 67e7016 | `../quantum`'s widened prior-art sweep → `PHASE2.md`; **later withdrawn** (bea84c1, 2026-09-21) |

I learned of every one of these by reading git diffs at the start of a later session, not by being
told. Two further unlogged paths: the user relayed a sibling verification in chat ("Both lemmas
verified independently here — including that the cubic bound only reaches ε ≤ 2.170"), and `PHASE2.md`
was authored outside my sessions with sibling content quoted inside it. And the workspace copy into
`../quantum` was logged on their side only; I discovered it during this audit.

**Assessment of the flagged edge.** cuspis ↔ vestigium is coupled, in three distinct ways (a
file-level copy of my workspace including the instrument; my bound serving as their post-repair
acceptance criterion; a shared literature ground truth), and none of the three was visible in a
bridge census. The coupling does **not** touch this repo's two headline results: the theorem was
re-derived there with independent code, and the sub-45° measurement has no counterpart there at all.
The honest label for the banner in `RESULT.md` is *independent re-derivation of my stated steps with
independent code* — which is what it already says — and not *independent confirmation of the result*,
since the constraint set, the two test functions and the lemma structure were all supplied by me, and
their own note concedes that whether C1–C6 is complete "was not swept".

**Grade** file-level findings (the copy, the hashes, the check scripts' imports, the commit list):
verified by direct inspection. The bound-as-acceptance-criterion reading: verified from their own
document's wording and sequence. "No echo reached my results": verified for the sub-45° region (no
overlapping data exists), reasoned for the theorem.

### EXP-014 addendum (2026-09-22) — the date boundary, and two corrections to the audit's picture

**The date, which was the question.** `../quantum`'s vendored snapshot corresponds to my **ee2453a,
the last commit of 2026-09-04**. Phase 2 begins at ee459b5 and every commit in it is dated
**2026-09-05**. EXP-012 in its entirety — the pre-registration, the sign analysis, the `eehp` run,
the node at 27 ± 3°, a₀ = −0.33 C_T — postdates the snapshot. Confirmed by inspecting their tree
today: their vendored `report.md` ends at EXP-011, and `EXP-012`, `EXP-013`, `eehp`, `a₀` and the node
value return zero hits across all four vendored prose files. **They hold none of the n = 1 sub-45°
magnitudes.** Their `scripts/` is already removed; seven files remain.

**Correction 1 — their detector's "zero" is wrong, and a detector that under-reports is worse than
none.** The 2026-09-04 tree *did* contain angle-indexed numeric tables below 45°:
`scripts/exp004_renyi2_result_n24_24_p15.0_t1.json` carries an explicit `deg` key with seven entries
below 45° (5, 10, 15, 20, 26.565, 30, 40), alongside 145 per-node files. These are **Rényi-2 (n = 2)**
values, not the n = 1 entanglement values under audit — but they are sub-45° tables from the same
instrument, and a₀(n = 2) = −0.0023 was derived from that very file in addendum 3. Consequence for
scoping their check: **the n = 1 arm is clean on values; an n = 2 arm would not be.**

**Correction 2 — the bound reached them on or before 2026-09-04, not 2026-09-21.** The audit logs the
[BWK16] transfer as 2026-09-21. But their resolution of it is already recorded in *this* repo in
commits 071bbc6, ed29f8b and 8a7747e, all dated **2026-09-04**, and their own `dbd443a` is the same
day. A seventeen-day error on the strongest reception edge in the audit is worth fixing in the ledger.

**Residual exposure, which does not dissolve with the date.** The solver predates the snapshot and was
vendored: `exp004_ch_solver.py` and `exp004_mp.py` were byte-identical to mine when I hashed them
earlier today. Removing `scripts/` from their working tree does not remove it from their history, and
their repository is public — the implementation is recoverable by `git show` from any commit between
the vendoring and the removal. So *values* are sealed and *implementation* is not, which is precisely
the axis their proposed check runs on.

**My position on the check.** No veto. The values under check postdate the snapshot and are absent
from their tree; they disclosed unprompted, which is what makes the exercise worth anything; and the
CHECK-not-REPLICATION label with declared prior exposure is the correct one — I accept it in their
voice. Four conditions, all of which I would want stated in their pre-registration: (1) the fresh
implementation is written from the published [CHL09] equations without consulting the vendored solver
in their history, and they say so explicitly; (2) the detector is fixed, or its "zero" is withdrawn
and replaced by the count above; (3) the n = 2 arm is either excluded or declared contaminated;
(4) conventions and the agreement criterion are frozen before any of my sub-45° numbers cross. Until
then the values stay sealed on my side — they were withheld even from this session's own transcript
when I inspected the file.

**On the A4 verdict and its replacement.** Independent data, entangled methodology is the right axis
and this pair fits it: their lattice data and my ODE-system data have never touched. What is entangled
is the methodology — a shared literature ground truth (σ = π²C_T/24 [FLP16], C_T = 3/(32π²), [CHL09]),
a bound of mine that became their post-repair acceptance criterion, and now a vendored implementation.
Agreement between us is evidence about the data, and not about the method.

### EXP-014 addendum 2 (2026-09-22) — the "≈4·10⁻⁴ at 5°" note, and a citation made precise

**What the note was.** The 2026-09-04 `TODO.md` line "decide the M > 15 tail (measured decay 0.83/unit
M; ≈4·10⁻⁴ at 5°)" is **not a value of a(θ) at any Rényi index**. It is a *relative truncation-error
estimate* for cutting the mass integral at M = 15. The decay rate behind it came from
`scripts/exp004_mdecay.py`, which calls the solver at **a = ½ only** (`cs.integrate(M, 0.5, …)`),
i.e. the Rényi-2 point, and prints per-mass integrands F(θ; M), not the corner function. So it was
measured on n = 2 data and proposed for application to n = 1. It carries no information about the
magnitude of a₁(5°). It was also wrong by a factor of about 200 — addendum 3 measured the actual
Rényi-2 truncation at 5° as −8% — and was withdrawn there. For the scope of `../quantum`'s check: it
falls under the n = 2 exclusion and leaks no n = 1 magnitude. The same applies to
`scripts/exp004_mdecay.log`, present in the 09-04 tree: per-mass a = ½ integrands, n = 2 arm.

**Citation, corrected on the bridge's report.** Every real-scalar known-answer value in this repo —
σ = 1/256, s(π/2) = 0.01183, s(3π/4) = 0.002520, κ = 0.0397 — is the [CHL09] Table 1 **complex-scalar**
entry halved (1/128, 0.02366, 0.005040, 0.0794). The values were right and the halving was stated in
some places ("0.02366/2" in EXP-001) but not all; the live `TODO.md` lines now say it explicitly.
These four are the controls `../quantum` transcribed verbatim, so the halving arithmetic was
re-checked: all four exact. The Dirac controls (σ = 1/128, 0.02329, 0.005022, 0.0722) are the [CHL09]
Dirac column unmodified.

## EXP-015  Where the sharp-end constant can come from: a structural answer, a correction to EXP-012, and a caveat on my own number

**Date** 2026-09-23. **Status** complete; reasoning, three source reads, and one millisecond fit on
stored numbers (`scripts/exp015_a0_models.py`, output frozen in `scripts/exp015_output.txt`).

**Goal.** First picked item of the deferred list: an independent route to a₀ that does not pass
through the ODE solver, together with the question of whether a₀ is a tip-operator dimension.

**Pre-registration (before the reads and the fit).** Outcomes: (i) an independent computation of
a₀ reproducing −0.33 C_T; (ii) a structural statement fixing whether a₀ can be nonzero, by theory;
(iii) a correction to EXP-012's mechanism; (iv) not session-sized. The fit was declared a
*model-dependence check* on my own published number, not a new measurement.

**Result 1 — the local physics of the thin wedge cannot produce a θ⁰ term (my argument).** At
distance r from the tip the wedge is a strip of width w = rθ with slope w′ = θ. Any local description
— the rectangle decomposition of [CH07] §3, or the fusion effective theory of [KRS25] — gives an
entropy density (1/w) f(w′, w w″, …), and scale invariance plus w″ = 0 reduce the log coefficient to
f(θ)/θ. Parity (mirror image of the wedge sends w′ → −w′) makes f even. So **every local contribution
is odd in θ: κ/θ, θ, θ³, …** The leading [CH07] term κ/θ is the first of these. [KRS25]'s small-angle
cusp expansion, −a₀/α − 3a₂,₂α + …, has no α⁰ term, as this requires.

**Result 2 — the tip cannot produce it either, for twist defects.** [CHK24] eq (2.12) (read):
Γ_ab = C/θ + Δ_c1 + α θ^{Δ_irr − 1} + …, where Δ_c1 is "the scaling dimension of the end-point
operator" of the fused defect c, and α θ^{Δ_irr−1} comes from "the least irrelevant operator on c".
A twist line and its orientation reversal fuse to the **trivial** defect, whose endpoint is the
identity: **Δ_c1 = 0**. The only remaining source of a θ⁰ term is an operator on the fused line with
dimension 1 — marginal on a line — which [CHK24] §3.3 already name, for N = 4 Wilson lines, as a
contributor to the θ⁰ term. On the trivial line these are bulk operators; with a trivial endpoint
their one-point functions vanish, so they enter at second order as θ^{2Δ−2}, which is θ⁰ exactly
at Δ = 1.

**Result 3 — classification, and one sharp prediction.** The lowest operator in the fusion channel of
a twist pair is the replica bilinear.

| theory | lowest pair-fusion operator | Δ | small-θ non-local term | a₀ |
|---|---|---|---|---|
| free real scalar | φᵢφⱼ, φᵢ² | 2Δ_φ = 1 | θ⁰, possibly with logs | ≠ 0 allowed ✓ (measured) |
| free Dirac | ψ̄ᵢψⱼ | 2Δ_ψ = 2 | θ² | **= 0 exactly (prediction)** |
| Einstein, leading N | T_μν (no light operators) | 3 | θ⁴ | = 0 ✓ (exact curve) |
| O(N) Wilson–Fisher | φᵢᵃφⱼᵃ | 1 + η | θ^{2η}: non-analytic | no true constant; a slowly drifting effective one |

Einstein checked against data that existed before this argument (not pre-registered, but it could
have failed): a − κ/θ = −0.9424 θ at θ = 0.02, 0.01, 0.005, 0.0025 to four digits, so the θ⁰ term is
zero and an O(1) θ² term is excluded (|c₂| ≲ 0.005 C_T against c₁ = 0.94 C_T), exactly the
odd-series-plus-θ⁴ structure predicted. **Pre-registered for the Dirac instrument (parked):
a₀^{Dirac} = 0 exactly, so the residual at θ → 0 equals ã₀ = +0.092 C_T and there is no node.**

**Result 4 — correction to EXP-012 Result C.** There I inferred a₀ = −∂ₙΔ_tip|₁ with Δ_tip the
dimension of a "defect-creation operator at the tip", and derived a₀ ≤ 0 from unitarity (P1). For
twist defects that dimension is zero identically (Result 2). **The mechanism was wrong; P1 passed, but
its pass is not evidence for the mechanism, and unitarity does not fix the sign of a₀.** The finite
part of a second-order term after its divergence is removed has no fixed sign. The TODO route "compute
∂ₙΔ_tip, target +0.0032" was aimed at a quantity that vanishes, and is replaced below.

**Result 5 — caveat on my own number.** The free scalar's dimension-one operators close under the
operator product (φᵢφⱼ × φᵢφⱼ ⊃ φᵢ² + φⱼ²). A marginal line coupling with nonzero three-point
coefficient runs logarithmically, so its θ⁰ sector can carry log θ. Fit on the stored n = 1 values,
κ fixed, windows from 20°:

| model | a₀ / C_T across four windows | rms |
|---|---|---|
| a₀ + a₁θ + a₂θ² + a₃θ³ | −0.315 … −0.322 | 0.5–1.9·10⁻⁶ |
| b log θ + a₀ + a₁θ + a₂θ² | −0.48 … −0.57 (b = −0.07 … −0.12) | 0.03–1.8·10⁻⁶ |
| b / log θ + a₀ + a₁θ | — | 40–180·10⁻⁶, rejected |

Both surviving models fit at the instrument's accuracy, and a log coefficient that drifts by 70% with
the window is not a detection. **So a₀ is model-dependent at the factor-1.5 level; if b ≠ 0 it is not
even a well-defined number, since it shifts with the unit of θ.** The range published in EXP-012
(−0.38 … −0.27) covered windows and polynomial degree but not the functional form the theory itself
allows. Robust across every model tried: the sign of the θ⁰ sector (negative), and the node at
27 ± 3°, which is read directly from the corrected residuals at 15°–30° rather than from any fit.

**Verdict.** Outcome (ii) plus (iii). No independent number for a₀, and that is the honest limit.
What this entry gives is an independent account of *whether* a₀ is nonzero: it explains why the
free scalar has a θ⁰ sector and Einstein does not, from the operator content of the twist-pair
fusion, and it predicts a₀ = 0 exactly for the Dirac fermion.

**Next steps.** The independent route to the *magnitude* is now concrete: the coefficient of the
marginal bilinears in the fusion of two parallel free-scalar twist lines at n → 1, together with the
one-loop beta function of the φ² line coupling in d = 3. Those give b, and whether the log is there
at all. Prior art to check first: free-scalar twist one-point functions ([HMS14], "Twist operators in
higher dimensions"; not re-read this session) and the φ² line defect's RG flow in the free theory.

**Grade.** Result 1: derivation, verified against [CH07] §3 and consistent with [KRS25]'s expansion
(abstract-level extract). Result 2: [CHK24] eq (2.12) and §3.3 as extracted, applied by me to twist
defects. Result 3: classification from standard operator dimensions; Einstein row checked on existing
data; Dirac row a prediction. Result 4: verified (it follows from Result 2). Result 5: verified; the
script and its output are in `scripts/`. Prior art: the θ⁰ mechanism for general cusps is [CHK24]'s;
its application to twist defects, the parity argument, and the classification were not found in the
sources checked ([CH07], [CHL09], [CHK24], [LMW26], one query without corner vocabulary).

## EXP-016  The shape residual: the sharp-end half is a Lifshitz artifact, the ≈1% accuracy is not a consequence of the constraints

**Date** 2026-09-23. **Status** complete; closed forms and published tables only
(`scripts/exp016_shape.py`, output frozen in `scripts/exp016_output.txt`; runtime seconds).

**Goal.** Second picked item: why the (σ, κ) trial function reproduces every computed curve to ≈1%,
and why its residual has the sign it has.

**Pre-registration (before running).** P-A: ECG, holographic with no light operators and not used in
EXP-015, has a₀ = 0. P-B: imposing a₀ = 0 on the trial function reduces its error at small angles
(26.6°, 45°) for every theory without a dimension-1 fusion operator (Einstein, ECG at both ends of
the allowed coupling, Dirac n = 1–4). P-C: imposing a₀ = 0 does not help the free scalar.

**Result 1 — where the trial function's constant comes from (derived).** Of the two basis shapes, the
extensive-mutual-information shape has no θ⁰ term (1 + (π−θ)cot θ = π/θ − πθ/3 + θ²/3 + …), while the
Lifshitz shape carries −¾ ((θ−π)²/(θ(2π−θ)) = π/(2θ) − ¾ + θ/(8π) + …). So the trial function's
constant is ã₀ = −¾λ¹, inherited entirely from its Lifshitz component, with λ¹ ∝ κ − 3πσ. For a theory
without a dimension-1 fusion operator the true a₀ is zero (EXP-015), so **the sharp-end residual equals
ã₀ exactly and its sign is sign(3π − κ/σ)**. The Lifshitz shape is the corner function of a
non-Lorentz-invariant theory, and its constant is the part of the trial function no such CFT can have.

**Result 2 — P-A passes.** ECG, exact first-order curve [BCV21 eq 293]: a − κ/θ is exactly linear in θ
at θ = 0.02, 0.01, 0.005, with intercept 0.00000 at all four couplings μ = +0.00312, +0.001, −0.001,
−0.00322. Out of sample for EXP-015, and it could have failed.

**Result 3 — P-B passes at 26.6°, partly at 45°; P-C passes.** a₀ = 0 is imposed by adding a third
shape with κ = 0, solving for all three weights, and repeating with two different third shapes,
cos²(θ/2) and ((π−θ)/π)², so the outcome is not one arbitrary choice. With a₀ set to ã₀ the three-shape
function reduces to the trial function exactly (control: 9·10⁻¹⁶). At 26.6°, 14 of 14 cases improve (7
theories × 2 shapes). At 45°, 11 of 14; the three misses are holographic. **Dirac n = 1–4 improve 3 to
15-fold at every angle with both shapes** (n = 1 at 26.6°: 0.54% → 0.12% / 0.04%). Einstein and ECG
improve at 26.6° and over-correct at wider angles. **The free scalar gets 10 to 100 times worse** (n = 1
at 26.6°: 0.01% → 2.5% / 2.2%; n = 2: 0.83% → 3.7% / 3.1%), as it must when the imposed constant is wrong.

**Result 4 — a scan that failed its known-answer control.** Scanning the imposed a₀ for the best fit over
five angles returns +0.09 … +0.13 C_T for Einstein and ECG, whose true a₀ is exactly zero. The control
fails, so the scan does not measure a₀ — it absorbs the smooth-end mismatch. Consequence: the Dirac scan
values (−0.012 … +0.026 C_T) are **not** evidence for the Dirac prediction a₀ = 0 beyond ±0.1 C_T. That
prediction still needs the Dirac instrument. (The scalar scan returns −0.39, between the instrument's
two model values; it is not used.)

**Result 5 — the smooth end: an empirical regularity, not derived.** sign(σ̃′ − σ′) = sign(3π − κ/σ)
holds for all nine entries without a dimension-1 operator (Einstein, four ECG couplings, Dirac n = 1–4)
and for the scalar at n ≥ 2; the one exception is the scalar at n = 1. But the zero crossing is not at
a fixed κ/σ: along the ECG family it extrapolates to κ/σ ≈ 9.19, along the Dirac n-family to ≈ 9.43. The
Dirac crossing lands within 0.006 of 3π; given a crossing somewhere in that interval, the chance of
landing that close is about 5%, so it is not claimed. **So the n = 1 versus n ≥ 2 split for the Dirac
fermion is an x-dependence (κ_n/σ_n crosses ≈3π between n = 1 and 2), not an n-dependence** — a
restatement that makes it less mysterious, without deriving the smooth-end sign.

**Result 6 — "little freedom" does not follow from the constraints.** [BMW15b] §6.2 explain the trial
function's accuracy by convexity: with both ends fixed, "little freedom remains at intermediate angles".
Counterexample: a_λ = (1−λ)𝔞_min + λâ_L with λ = 0.5818 lies in 𝒞 (RESULT.md Theorem (a)) and has
exactly Einstein's σ and κ (checked: 0.411234, 3.7094). It departs from Einstein by +9.6% at 26.6°, +7.9%
at 45°, +3.4% at 90° and +0.8% at 135°. That is ten times the trial function's error. **The ≈1% accuracy is
an empirical property of the theories computed, not a consequence of any known constraint.**

**Result 7 — a reframing that unifies the two halves (not an explanation).** The trial function is the
EMI shape plus a Lifshitz admixture proportional to κ − 3πσ. Its accuracy says that every computed n = 1
theory lies close to the EMI point: within 8% in x = κ/σ (EMI: 3π) and 5% in y = σ′/σ (EMI: 1/15). The
EMI value κ/C_T = π³/8 = 3.876 sits inside the observed band [3.672, 4.179]. So the κ band and the
shape residual are one observation — **physical corner functions are close to the EMI corner function**
— and, by the theorem and Result 6, neither follows from C1–C6. The EMI model is not a CFT [ABC21].

**Verdict.** The sharp-end half of the residual has a mechanism, derived and confirmed out of sample:
the Lifshitz component's spurious constant. The smooth-end sign is an empirical regularity. The size of
the residual is not explained by the constraints, and is the same open fact as the κ band.

**Grade.** Results 1, 2, 3, 6: verified (algebra; exact curves; published tables; an admissible function
from a proved theorem). Result 4: the failed control, verified. Result 5: verified as a regularity,
not derived. Result 7: a reframing, labelled as such.

## EXP-017  The upper bound on κ: the rectangle bootstrap is closed under Casimir dressing, at every corner dimension

**Date** 2026-09-23. **Status** complete; a two-line proof and a sub-minute check
(`scripts/exp017_dressing.py`, output in `scripts/exp017_output.txt`).

**Goal.** Third picked item: can the other cutting-and-gluing relations exclude the pure-Casimir
solution that makes [LMW26]'s bound one-sided (EXP-013 Finding 4)?

**Pre-registration.** Outcomes: (i) a known constraint excludes it; (ii) closure — shown impossible
within the constraints in hand; (iii) not session-sized.

**Result 1 — closure under Casimir dressing (theorem).** Let 𝒟(y) = 𝒟(1/y) and let
𝒜(y) = y^{−2Γ} e^{−ε₀y} 𝒟(y) be completely monotone — the two conditions of [LMW26] eqs (13)–(15).
Then for every E ≥ 0, 𝒟_E(y) = 𝒟(y) e^{E(y+1/y)} satisfies both, with the **same** corner dimension Γ
and Casimir energy ε₀ + E. *Proof.* Symmetry is manifest. 𝒜_E = 𝒜 · e^{E/y}. The factor e^{E/y} is
completely monotone, being the Laplace transform of δ(ε) + Σ_k E^k ε^{k−1}/(k!(k−1)!) ≥ 0, and a product
of completely monotone functions is completely monotone, since the spectral densities convolve. ∎
EXP-013's witness was the case 𝒟 = 1, Γ = 0. **This theorem covers every Γ.** In particular it covers
the nonzero corner dimension a twist defect is forced to have by the lower bound a_n(π/2) ≥ 𝔞_min-type
bound: at any fixed a_n(π/2), κ_n is unbounded above within the rectangle bootstrap.

**Check** on the 2d-BCFT extremal solution (𝒟 = y^{2Γ}η(iy)^{8Γ}, c = 1), dressed with E = 0, 1, 5:
modular symmetry to 2·10⁻¹²¹; (−1)^k𝒜^{(k)} ≥ 0 for k ≤ 6 at y = 0.5, 1, 2, 10, 30; control 𝒜·(1+y)
must fail and does, at every E. Two failures of the check itself were kept rather than repaired quietly.
With points only up to y = 2 the control did not fire at E = 5, because (1+y)e^{E/y} mimics a completely
monotone function for y ≪ E. Once large y was added, the positive check failed at E = 0 at 20 digits,
because the undressed 𝒜 is 1 + O(10⁻⁸⁰) there. The check was wrong both times, not the mathematics.

**Result 2 — the same obstruction in two languages.** Dressing multiplies 𝒜 by a factor that tends to 1
in one channel (y → ∞) and dominates in the other (y → 0): a pure contact attraction between the two
defects, invisible at finite aspect ratio. In the corner function's spectral representation, the tail
truncation of RESULT.md Theorem (b) adds κ with vanishing mass, invisible at finite angle. Both add
weight only at the singular end, and both leave everything else unchanged.

**Result 3 — the constraints in hand are all dressing-invariant.** The rectangle bootstrap (Result 1);
concavity and monotonicity of Γ(θ) [CHK24], which are C2 in corner language and preserved by the tail
truncation (EXP-003); [LMW26]'s mixed-cusp inequality, which for twist defects (a = b) reduces to those.
Not checked: [LMW26]'s cuboid equations (not read), and multi-rectangle or polygon relations beyond
their paper. **So an upper bound on κ requires a constraint that is not invariant under
𝒟 → 𝒟e^{E(y+1/y)}** — one in which the Casimir energy enters other than as a multiplicative
e^{ε·(geometry)} factor. The Cardy mechanism is of that kind (the vacuum energy is fixed by the anomaly,
so dressing would change a universal number); RESULT.md §6 explains why it is absent in odd d.

**Verdict.** Outcome (ii) for the constraints in hand. "No bridge found" becomes a single test that any
proposed upper bound on κ must pass: it must fail to be invariant under Casimir dressing,
equivalently under adding a pure singular-end tail.

**Grade.** Result 1: proved; numerical check with a working control. Result 2: a precise analogy.
Result 3: verified for the constraints read; the cuboid is not covered and not claimed.

## EXP-019  The Dirac control failed because it ran at the wrong twist parameter

**Date** 2026-09-23. **Status** diagnosis complete; corrected known-answer control running (mode
`dirac2q`, 48 nodes); pass criterion below, fixed before the run.

**Why both earlier Dirac controls failed (EXP-012 addenda 1–2).** [CHL09] eq (6) sums fermion sectors
over k = −(n−1)/2 … (n−1)/2 with boundary phase e^{2πik/n}; eq (12) writes that phase as e^{2πia}, so
a = k/n; eq (13) restricts to a ∈ (0, ½), and the text of §3 repeats "recall that a ∈ (0,1/2)" at the
point where eq (59) is derived. For n = 2 the fermion has a = ±¼. My driver used **a = ½** for the
Dirac Rényi-2 mode — the free scalar's n = 2 value (bosons sum k = 0 … n−1, so k = 1 gives a = ½),
carried across to the fermion. At a = ½ the formula is outside its stated range: the denominator
4β₁² − b² sin²x vanishes like m² identically, which is exactly the m → 0 singularity diagnosed in
EXP-012 addendum 1. So:

- the transcription of eq (59) was probably right all along;
- the "−2" patch of addendum 1 was chosen to cure a symptom of evaluating at an excluded point, and is
  withdrawn (its failure in addendum 2 was the correct outcome);
- the decomposition "A = 2 s₂^{cs}" used in addendum 2 was also wrong: the 2m tr G_S piece of eq (59)
  at the fermion's a = ¼ is not the scalar Rényi-2 function, which lives at a = ½.

**Why the check fired, asked before acting.** The check was right both times; the routine had the
wrong input. The cue that should have been caught earlier: EXP-011 already used a = k/n = ¼ for the
n = 2 fermion sector, in this same notebook.

**Tier 1 (seconds), at a = ¼.** The regularised vertex term is finite as m → 0: Ψ_π = 7.32, 7.02,
3.78 at m = 0.0096, 0.0505, 0.2272, against 5.4·10³ at the lowest mass at a = ½. The degeneracy is gone.

**Pass criterion for `dirac2q`, fixed before the run** (identical to addendum 1's, except that 63.4° is
refereed by eq (22) rather than by the truncated series — EXP-016 showed the series is 0.16% low there
for the fermion): s₂(θ) within 10⁻³ of the exact series at θ ≥ 90°; within 2·10⁻³ of [HHCWM16] eq (22)
and Table 2 (α = 2) at 26.6°, 45°, 63.4°; s(170°)/(σ₂ε² + σ₂′ε⁴ + σ₂″ε⁶) = 1 to 10⁻⁴, with
σ₂ = 1/(64π), σ₂′ = (35π−8)/(30720π²) exact. If it passes, the Dirac entanglement run (mode `dirac`,
a = −it) is licensed; its prediction, a₀ = 0 exactly (EXP-015), stays pre-registered.

## EXP-018  The M ≥ 14 failure is the series start stalling at the size of the signal

**Date** 2026-09-23. **Status** complete (`scripts/exp018_m14.py`, output `scripts/exp018_m14.out`).

**One-node diagnosis, one variable per variant.** Node M = 14.019, t = 0.0287 from the high-precision
run, whose stored F(5°) = −1.6·10⁻⁵ is wrong in sign; its good neighbours give ≈ +1.0·10⁻⁵ by
interpolation (M = 13.58: 1.12·10⁻⁵; M = 14.38: 0.90·10⁻⁵). Production values: dps = 50 + 5M = 120,
N = 1.6M + 8 = 30, δ₀ = 0.01/M.

| variant | F(5°) | F(15°) | series-start residual | time |
|---|---|---|---|---|
| baseline | −1.5995·10⁻⁵ (reproduces the stored node exactly) | −3.9·10⁻¹⁰ | 2.5·10⁻³⁷ | 802 s |
| δ₀ / 2.5 | −2.1·10⁻⁵ (different wrong value) | −1.6·10⁻⁸ | 2.5·10⁻³⁷ | 800 s |
| N = 40 | **+1.0043·10⁻⁵** | **8.1341·10⁻⁸** | 5.9·10⁻⁵⁵ | 1794 s |
| dps = 170 | **+1.0043·10⁻⁵** | **8.1341·10⁻⁸** | 5.1·10⁻¹⁷⁰ | 627 s |

Two independent changes agree in every printed digit, and both converge the series start far below
the signal e^{−2πM} ≈ 10⁻³⁸. The failing runs leave a starting residual larger than the signal. Values
near θ = π and H1 were fine throughout; the error only surfaces after amplification toward small
angles. **Cause: at dps 120 the series-start solve loses about 80 digits to conditioning at M = 14 and
stalls at the size of the signal.** My TODO entry calling this "not a precision failure" was wrong:
it is precision in the starting solve, not in the integrator. It was also invisible because the
residual was never stored — the fix the TODO itself had named.

**Changes.** The solver now returns the starting residual and every node records it, together with
its ratio to e^{−2πM}; a node is trustworthy only if that ratio is far below 1. The high-precision
digits rule becomes dps = 30 + 9M (165 at M = 15), which is also faster than the old rule where the old
rule fails; it now applies to the Dirac entanglement mode as well, which runs at complex a.
The scalar entanglement masses M ≥ 14 can be re-run under this rule (50 nodes) to remove the
15°–20° cutoff deficit of EXP-012 addendum 6; not yet done.

### EXP-019 addendum (2026-09-23) — `dirac2q` FAILED as run; two assembly errors of mine found in the stored nodes; a precision bug of mine caught by Tier 1

**Outcome as pre-registered: FAIL.** s₂(θ) was 6·10³ times too small near π, scaled as ε⁴ (zero ε²
coefficient), and blew up below 45°.

**Diagnosis from the stored nodes, no rerun.** The node files store the scalar part F and the
regularised Ψ separately, so the assembled function splits into A (the 2 tr G_S part) and V (the
vertex part as coded). Two errors, both mine:
1. The code divides the vertex term by 2M(…) where [CHL09] eq (59) prints M(…): the vertex term was
   halved relative to the source.
2. The assembly omitted the 1/(1−n) of the Rényi entropy, which is −1 at n = 2.
With the source's factor, −(A − 2V) reproduces the exact Dirac Rényi-2 function to 3·10⁻⁶ at 135°–170°,
4·10⁻⁵ at 90° and 6·10⁻⁴ at 63.4°. **This correction was identified on the same data it is checked
against**, so it is confirmed only by the prospective rerun below, whose small angles played no part
in finding it, and by the Dirac entanglement run's own known answers.

**Small-angle garbage: the same class as EXP-018.** At a = ¼ the per-mass values are smooth to M ≈ 6
and wrong from M ≈ 6.5 at the default 25 + 3M digits. The scalar at a = ½ stayed clean to M ≈ 14.7,
because a = ½ is the symmetric, well-conditioned point. (The validated a = ½ run has one bad node,
M = 14.87; recorded here, not previously noticed.)

**A bug of mine, caught by Tier 1.** In the EXP-018 edit I appended a comment mid-line and commented
out the statement that installs the high-precision digits rule. Every high-precision mode would have
run silently at the old precision; nothing ran in those modes in between. Tier 1 of the new mode
reported 46 digits at M = 7.13 where 94 were intended. Fixed; the two cached nodes written at the
wrong precision were moved to `scripts/exp004_nodes_rejected/`, not deleted. After the fix: 94 digits,
starting residual 6·10⁻⁷⁴ of the signal, F(5°) = 9.9·10⁻⁵ on the smooth trend.

**Prospective control running:** mode `dirac2v` = a = ¼, the source's vertex factor, the 1/(1−n) sign,
30 + 9M digits, residual stored. Same criterion as fixed before `dirac2q`. The out-of-sample part is
26.6° and 45° against [HHCWM16] Table 2.

### EXP-019 addendum 2 (2026-09-23) — `dirac2v` FAILED as run, on one node; the cause was a solver bug of mine from EXP-004

**Outcome as pre-registered: FAIL.** From 100° to 170° the new run agrees with the exact Dirac Rényi-2
function to ≈ 3·10⁻⁶, and at 90° to 5·10⁻⁵. These are fresh nodes at new precision, but at the angles
used to identify the EXP-019 corrections, so they count as reproduction, not out-of-sample.
Everything below 80° was swamped by one node, M = 13.58, whose starting residual was 7·10⁻¹⁵ against a
signal of e^{−2πM} ≈ 10⁻³⁷, and whose F(5°) was about −10¹⁰. The residual guard added in EXP-018 flagged it
during the run. That assembly is kept as
`scripts/exp004_nodes_rejected/exp004_dirac2v_result_first_assembly_with_bad_node.json`.

**What it was not.** Larger N made it worse (N = 40: residual 2·10⁻⁹). Replaying only the starting
solve showed erratic stage failures: at the production mass it converged; 10⁻⁴ below, the last stage
jumped to 2·10⁻¹⁴ and stayed; 10⁻⁴ above, one stage jumped to 9·10⁻¹⁵ and the next recovered. The
solver contains no randomness.

**What it was.** Every jump landed near 10⁻¹⁴, at double-precision round-off. In `series_start_mp`,
each continuation stage passes its coefficients to the next through `complex(cc[k])`, so **every
stage restarted from double precision**. Newton's method usually recovers from there within a few
iterations. But the line search accepts its last trial point even when that point is worse than the
current one, so one failed step leaves the solve stuck at the double-precision floor. The conversion
was written for the double-precision warm start and silently reused for the high-precision
continuation.

**Fix, one change.** Carried coefficients stay in multiple precision. The deterministic failing case
now converges at every stage, to ≈ 10⁻¹⁵⁰ (a residual 10¹¹³ below the signal), in half the time.
Regression: a validated scalar Rényi-2 node (M = 3.13) is unchanged at all 25 angles. The line
search's acceptance of a worse point is left as found and recorded here; it is harmless once the
start is accurate, and changing it would be a second variable. The bad node was quarantined, not
deleted, and is being recomputed through the driver; the control will be re-judged on the same
criterion. Recomputing a node that failed its own pre-declared convergence test is not a change to
the evaluation.

### EXP-019 addendum 3 (2026-09-23) — the Dirac known-answer control PASSES; the Dirac entanglement prediction frozen numerically

**`dirac2v`, with the recomputed node** (residual 1.6·10⁻¹¹³ of the signal): **PASS** on the criterion
fixed before `dirac2q`. Worst deviation from the exact series at 90°–160° is 3.9·10⁻⁵, at 90°; 100°–170°
agree to ≈ 3·10⁻⁶. The out-of-sample angles, which played no part in identifying the corrections, agree
with [HHCWM16] eq (22) and Table 2 to 5.0·10⁻⁶ (26.6°) and 1.2·10⁻⁶ (45°), four hundred times inside
the criterion. Below 20° the M ≤ 15 mass cutoff shows, as for the scalar: −4·10⁻⁴ at 15°, −0.6% at 10°,
−7.8% at 5°. The Dirac instrument is validated at n = 2.

**Frozen before the entanglement run (mode `dirac`, a = −it, eq (60)).**
- Known-answer controls, all out of sample for the n = 2 validation (complex twist, t-integral,
  branch path): σ = 1/128; σ′ = (16 + 3π²)/(9216π²); s(π/2) = 0.02329 and s(3π/4) = 0.005022 [CHL09];
  [HHCWM16] Table 2 α = 1, series and eq (22), at the seven angles. They must hold to ≤ 10⁻³ at
  θ ≥ 63.4° and ≤ 2·10⁻³ at 26.6° and 45° before the fit below is looked at.
- **The prediction (EXP-015): a₀^{Dirac} = 0 exactly.** Protocol: κ fixed at [CHL09]'s 0.0722, fit
  s − κ/θ = a₀ + a₁θ + a₂θ² + a₃θ³ on the windows 20–50°, 20–60°, 26–60°, 20–70°, from 20° up because of
  the mass cutoff. **Confirmed if every window gives |a₀| < 0.05 C_T; refuted if every window gives
  |a₀| > 0.1 C_T; inconclusive otherwise.** C_T = 3/(16π²). For scale: the trial function's ã₀ is
  +0.092 C_T and the free scalar's measured a₀ is ≈ −0.3 C_T. A log θ term is not expected (no
  dimension-1 fusion operator); the log model is fitted and reported, not used for the verdict.
- Also predicted: no node; the trial function lies above the exact function at every angle.

## EXP-020  The Dirac entanglement run: the pre-registered prediction a₀ = 0 is confirmed

**Date** 2026-09-23. **Status** complete. Mode `dirac` (a = −it, [CHL09] eq (60)), 672 nodes
(48 masses ≤ 15 × 14 t-nodes on [0, 3.2]), digits 30 + 9M, the EXP-019 fixes, residual guard on.
Result `scripts/exp004_dirac_result_n24_24_p15.0_t14.json`; analysis `scripts/exp020_analyze.py`,
applied exactly as frozen in EXP-019 addendum 3 before the run.

**Failed nodes, measured before the verdict was looked at.** Sixteen nodes failed, all at large t
(≥ 2.7) for M ≥ 11.9. The starting solve raised "matrix is numerically singular", probably near a
branch transition, where the leading coefficient vanishes. The assembly skips failed nodes, so their
effect was measured (`scripts/exp020_failed_nodes.py`) with two independent fill-ins, extrapolation in t
and interpolation in M, which agree to ≈ 10%. **Their total contribution is ≤ 4·10⁻⁷ of s(θ) at every
angle, and ≤ 2·10⁻⁷ from 20° up**: immaterial to every criterion below. The singular-start cases
remain open as an instrument item.

**(1) Known answers: PASS** (criterion ≤ 10⁻³ at 63.4°–160°, ≤ 2·10⁻³ at 26.6° and 45°). Against the
exact series and eq (22) of [HHCWM16]: worst 3.9·10⁻⁵ at 63.4°–160° (90°); 3.6·10⁻⁵ at 26.6° and 5·10⁻⁶
at 45°; ≤ 4·10⁻⁶ from 100° to 170°; 2·10⁻⁶ at 20°. [CHL09]: 0.02329 at 90° (+9·10⁻⁵, their last digit)
and 0.005022 at 135° (−6·10⁻⁶). The mass cutoff shows below 20°: −7·10⁻⁴ (15°), −1% (10°), −11% (5°).
This is the first independent four-digit determination of the free-Dirac corner function between 20°
and 60°, and it agrees with [HHCWM16]'s eq (22) there to ≤ 4·10⁻⁵.

**(2) Residual sign: as predicted.** (ã − a)/a is positive at every angle from 15° to 170° (+0.48% at
15°–20°, maximum +0.58% at 40°, +0.005% at 170°). No node.

**(3) a₀: CONFIRMED on the frozen rule.** κ fixed at [CHL09]'s 0.0722, model a₀ + a₁θ + a₂θ² + a₃θ³:

| window | 20–50° | 20–60° | 26–60° | 20–70° |
|---|---|---|---|---|
| a₀ / C_T | +0.001 | +0.002 | +0.005 | +0.002 |

All four satisfy |a₀| < 0.05 C_T; the rule was confirm-if-all-below-0.05, refute-if-all-above-0.1. The
reported-only models agree in direction: quadratic −0.002 … −0.005; with a log term −0.017 … −0.058
and a log coefficient drifting −0.007 … −0.028, which is not a detection. **Sensitivity beyond the
frozen rule:** moving κ across its published rounding (0.07215–0.07225) moves a₀ by ±0.02 C_T, and
fitting κ freely returns 0.07215 with a₀ = +0.019, the same degeneracy. So **a₀^{Dirac} = 0.00 ± 0.02
C_T**, the uncertainty set by κ's third digit rather than by the instrument. For comparison: the
trial function's ã₀ = +0.092 C_T, and the free scalar's a₀ ≈ −0.3 C_T.

**What this establishes.** EXP-015 derived that a θ⁰ term needs a dimension-1 operator in the
twist-pair fusion channel; the free scalar has one (Δ = 2Δ_φ = 1), the Dirac fermion does not
(Δ = 2Δ_ψ = 2). The Dirac prediction was frozen numerically before this run, could have failed, and did
not. Together with Einstein (a₀ = 0, exact curve), ECG (a₀ = 0, four couplings, EXP-016) and the free
scalar (a₀ ≈ −0.3 C_T, nonzero), the sharp-end constant now behaves as the operator content says in
all four theories where it has been measured. The mechanism of EXP-012 Result C, now withdrawn, would
have allowed any a₀ ≤ 0 here.

**Grade** known answers: verified. Failed-node immateriality: measured. a₀ = 0.00 ± 0.02 C_T: measured,
κ-limited, with a verdict fixed in advance. Below 45° the instrument's values are refereed by [HHCWM16]
eq (22), whose one-sided error for the fermion is ≈ 0 (the last coefficient already sits at its
asymptote), so here the sub-45° values have two independent methods behind them.

## EXP-021  Literature sweep for the backlog, and a prior-art correction to EXP-015

**Date** 2026-09-23. **Status** complete. Six parallel research streams, restricted to reading, covered:
interacting-CFT corner data; holography and extremality; the defect and cusp bootstrap; free-field twist
lines; Rényi-index constraints; strip and mutual-information coefficients. The ranked backlog they
informed is `BACKLOG.md`.

**Correction to EXP-015.** [LMW26b] eq. (28), posted 3 September 2026, gives the small-angle expansion
Γ = C/θ + Δ_c𝟙 + a₂θ + αθ^p + … with p = 2(Δ_irr − 1) when fusion is dominated by the identity defect
(verified on the paper's HTML). That is the structure EXP-015 derived on 23 September: a θ⁰ term from
an operator with Δ = 1 entering as θ^{2Δ−2}. EXP-015 read only the companion paper [LMW26] and claimed
the application "not found in the sources checked". Revised novelty claim: the exponent and the fusion
structure are [LMW26b]'s. What may still be new, pending a proper check against the whole paper: the
parity argument for the absence of local θ⁰ terms; the application to replica twist lines (twist pair
fuses to the identity, so a₀ ≠ 0 exactly when a dimension-1 operator is present); the classification of
the scalar, Dirac, Einstein and ECG cases; and the confirmation in EXP-020. Two extracts disagree on
whether [LMW26b] discuss the dimension-1 case explicitly; that must be read before any claim.

**Other findings that bear on existing entries.**
- EXP-017's closure of the rectangle bootstrap under Casimir dressing was listed by one stream as an open
  research task, which suggests it is not in the literature. Not yet a verified novelty claim.
- A stream's own algebra suggests [LMW26]'s cuboid bound is also closed under dressing; unchecked
  (BACKLOG #24).
- [LMW26b] eq. (37), a₂ ≥ a₀/12 for Δ_irr > 3/2, is the only upper-type inequality on a Casimir energy
  found, and it is relative to the O(θ) coefficient. A stream checked it is dressing-invariant. It is
  testable on this repository's data (BACKLOG #22).
- The only interacting κ is Ising at Rényi-2, 0.763(22) of free [KHSM19]; none at n = 1 for any
  interacting theory.

**Grade.** The [LMW26b] eq. (28) statement: verified by me on the source. Other stream findings:
verified by the streams on arXiv abstract pages or text as labelled in `references.md`; two entries lack
recorded titles and are flagged there.

## EXP-022  Testing the "eye" cusp inequalities on this workspace's curves (bridge C17 = CF-22) — pre-registration

**Date** 2026-09-24. **Status** pre-registered; results in the addendum below. Requested by the bridge as
the first step of the bounds chain; sole owner.

**Source, read on the paper ([LMW26b] = 2609.04302).** Conformal concavity: ℰ″(u) ≤ 0 with
ℰ(u) = √u·Γ(θ(u)) and u = tan²(θ/4) (eqs. 1–2). For twist lines Γ⁽ⁿ⁾ = (1−n)a_n (eq. 40), so for integer
n ≥ 2 the function F_n(u) = tan(θ/4)·a_n(θ) is positive, decreasing and convex (eq. 41). The paper says this
does not apply a priori at n → 1 and checks it there only graphically (its Fig. 2: free scalar, Dirac,
Einstein). Eq. (37): if Δ_irr > 3/2, a₂ ≥ a₀/12 with a₀ ≡ −C, from Γ = C/θ + Δ_c𝟙 + a₂θ + αθ^p (eq. 28).

**Sign convention, settled.** Eq. (3) gives ℰ(0) = C/4 with Γ ≈ C/θ, so for the twist line
C = (1−n)κ_n < 0 when n > 1, and a₀ ≡ −C > 0. The sentence "C_{aāc̄} ≥ 0" near eq. (34) contradicts
angular concavity (Γ″ ≤ 0 requires C ≤ 0) and is read as a slip.

**Eq. (37) re-derived here, independently.** With u ≈ θ²/16 and θ = 4 arctan √u,
ℰ(u) = C/4 + (C/12 + 4a₂)u + O(u²) when p > 1. The tangent-line form of concavity (their eq. 22) at u = 0,
ℰ(1) ≤ ℰ(0) + ℰ′(0), with ℰ(1) = Δ_aā = 0, gives C + 12a₂ ≥ 0, which is their eq. (36) and (37). The condition
Δ_irr > 3/2 (p > 1) is what keeps ℰ′(0) finite. **In corner-function language** (a_n = κ_n/θ + a₀ᶜ + a₁θ + …,
with a₂ = (1−n)a₁): **a₁ ≤ −κ_n/12 for n > 1**; at n = 1 this is the continuation of that statement. It applies
where the lightest fusion operator has Δ > 3/2: Dirac (Δ = 2), Einstein and ECG (stress tensor, Δ = 3). It
does **not** apply to the free scalar (Δ = 1).

**Frozen tests.**
- **T-A, known answers that must pass (theorems at integer n ≥ 2).** F_n positive, decreasing and convex in u
  for: this workspace's scalar n = 2 and Dirac n = 2 runs; and the published [HHCWM16] curves (series at
  θ ≥ 90°, eq. (22) below) for boson and fermion at n = 2, 3, 4. Eq. (37) for Dirac at n = 2:
  a₁⁽²⁾ ≤ −κ₂/12 with κ₂ = 0.0472338(1) [BMW15b]. **A failure stops the exercise:** it would mean my
  transcription or my data is wrong, not the theorem.
- **T-B, tests of the n → 1 continuation (not guaranteed).** Concavity for Einstein (exact curve), ECG (exact
  first-order curves at four couplings; a theory not in [LMW26b]'s Fig. 2), Dirac n = 1 and scalar n = 1.
  Eq. (37) at n = 1 for Einstein, ECG and Dirac: a₁ ≤ −κ/12.
- **T-C, secondary and low weight.** Eq. (35), α(Δ_irr − 3/2) ≤ 0 for 1 < Δ_irr < 5/2, applies to Dirac
  (Δ = 2, p = 2): the θ² coefficient of a_n must be ≥ 0 for n ≥ 2. Extracting it from numerics is inference;
  reported with its fit drift, not used as a verdict.

**Methods, fixed in advance.** Exact curves: F evaluated on a dense u-grid, second differences checked
against a relative tolerance of 10⁻⁷. Numerical runs: the discrete secant-slope test of [LMW26b] eq. (39),
on angles where the run is validated (θ ≥ 20° at n = 1, ≥ 15° at n = 2), with the noise level of the
second differences estimated from the run's stated accuracy. a₁ for exact curves: lim (a − κ/θ)/θ from
evaluations at θ = 0.01, 0.005, 0.0025, which is evaluation at points, not a fit. a₁ for numerical runs: fits
of s − κ/θ with a₀ = 0 imposed (Dirac, EXP-020) over the windows 20–50°, 20–60°, 26–60°, 20–70°, with drift
and κ-sensitivity reported; this is inference and graded as such. **Verdict per test:** pass if the
inequality holds by more than the stated uncertainty, fail if violated by more, inconclusive otherwise.

**What would be news.** The concavity checks on the free scalar, Dirac and Einstein at n = 1 repeat
[LMW26b]'s Fig. 2, so passing them is confirmation, not news. New: concavity for ECG; every eq. (37) test;
the margins by which each theory satisfies the inequalities.

### EXP-022 addendum — results: every pre-registered test passes; one check fired on an artifact; a correction to EXP-015

Script `scripts/exp022_eye.py`, output `scripts/exp022_output.txt` (runtime seconds).

**T-A, known answers (theorems at integer n ≥ 2): all pass.** F_n is positive, decreasing and convex for the
published [HHCWM16] curves, boson and fermion, at n = 2, 3, 4, and for this workspace's scalar and Dirac runs
at n = 2 (no secant-slope decrease at all, let alone beyond noise). Eq. (37) for Dirac at n = 2: a₁ lies
between 4.07 and 4.09 times −κ₂/12 across four windows and κ₂'s last digit, so it holds with a factor-4
margin.

**T-B, the n → 1 continuation.** Convexity holds for Einstein (exact), for ECG at all four couplings (exact;
a theory not in [LMW26b]'s Fig. 2), and for this workspace's Dirac and scalar runs at n = 1. Eq. (37) holds at
n = 1 in every applicable case:

| theory | a₁ | −κ/12 | a₁ / (−κ/12) |
|---|---|---|---|
| Einstein | −0.9424 C_T (exact, stable to 10⁻⁵) | −0.3091 C_T | 3.05 |
| ECG, μ from +0.00312 to −0.00322 | −0.908 … −0.977 C_T (exact) | −0.306 … −0.312 C_T | 2.97 … 3.13 |
| Dirac n = 1 | fits, a₀ = 0 imposed | κ = 0.0722 | 3.56 … 3.88 |
| Dirac n = 2 | fits | κ₂ = 0.0472338 | 4.07 … 4.09 |

The inequality is satisfied by a factor of 3 to 4 everywhere, far from saturation. It cannot come close to
constraining κ in any known theory. It is also dressing-invariant: Casimir dressing shifts C by 4δ and a₂ by
−δ/3, leaving C + 12a₂ unchanged. So it is not a route to an absolute bound (S5, CF-1).

**The check that fired, and why.** [HHCWM16]'s eq. (22) for the fermion at n = 1 fails convexity. Asked
before acting: the violation sits only at 3.4°–4.1° (u ≈ 2–3·10⁻⁴). Eq. (22)'s constructed small-angle tail
gives that curve a small **positive** constant, a₀ = +0.00011 (+0.006 C_T), while the boson curves carry
negative ones. A constant a₀ in a(θ) adds a₀√u to F, whose second derivative −a₀/(4u^{3/2}) dominates as
u → 0. So any positive constant must break convexity at small enough angle. This is an artifact of the
formula's tail, not physics: the measured Dirac a₀ is 0.00 ± 0.02 C_T (EXP-020), and this workspace's Dirac
curve passes. It matters to anyone who uses eq. (22) below a few degrees; the 20°–45° refereeing it provides
(S10, EXP-012) is unaffected.

**Correction to EXP-015 Result 4: the sign of a₀ is fixed after all.** The same mechanism, applied to the
cusp, gives a theorem. If Γ contains a constant α (the p = 0 case of [LMW26b] eq. (28)), then ℰ ⊃ α√u and
ℰ″ ⊃ −α/(4u^{3/2}) dominates as u → 0. Conformal concavity (ℰ″ ≤ 0, proven for integer n ≥ 2) then
forces α ≥ 0. For twist lines α = (1−n)a₀, so **a₀ ≤ 0 at every integer n ≥ 2**, and a₀ ≤ 0 at n = 1 if the
concavity continues. This is the Δ_irr → 1 end of [LMW26b] eq. (35), α(Δ_irr − 3/2) ≤ 0, which the paper
states for 1 < Δ_irr < 5/2. EXP-015 wrote that "unitarity does not fix the sign of a₀", having withdrawn
EXP-012's defect-creation argument. That was wrong: reflection positivity in the eye geometry fixes it. The
measured values, free scalar −0.24 C_T at n = 2 and ≈ −0.3 C_T at n = 1, and Dirac 0 (the boundary),
are consistent. P1 of EXP-012 therefore has a correct mechanism, though not the one originally given.

**T-C (low weight).** Eq. (35) with Δ = 2 predicts a non-negative θ² coefficient for the Dirac fermion at
n ≥ 2. Fits give +0.0050 at n = 2 and +0.003 … +0.008 at n = 1 (in units of a). Consistent; inference only.

**Observations, labelled as such.** (i) Eq. (22)'s own constant for the boson corresponds to
−0.305 C_T for the real scalar at n = 1. That is close to this workspace's no-log value of −0.32 C_T. It
cannot bear on the log question, because a geometric tail cannot produce a log θ term by construction.
(ii) In holography a₁/κ = −0.254 (Einstein) and −0.247 … −0.261 (ECG), close to −¼. For the Dirac fermion
it is about −0.30 to −0.32, and for the EMI shape −⅓. No explanation is offered.

**Verdict.** Confirmation for the concavity checks at n = 1 on the free fields and Einstein, which repeat
[LMW26b]'s Fig. 2. New: ECG concavity; every eq. (37) test, all passing by factors of 3 to 4; the
artifact in eq. (22); and the theorem a₀ ≤ 0 at integer n ≥ 2, which corrects EXP-015.

**Grade.** Tests: verified (exact curves, published curves, validated runs; controls passed). Eq. (37)
re-derivation and the a₀ ≤ 0 argument: derived here, the latter as an elementary consequence of [LMW26b]'s
proven concavity. Dirac a₁ values: fits, κ-limited, drift reported.

## EXP-023  The cuboid bootstrap is also closed under Casimir dressing — including for the pair energy κ (bridge: bounds chain; CF-24)

**Date** 2026-09-24. **Status** complete; algebra by hand, checked numerically at 40 digits with a working
control (`scripts/exp023_cuboid.py`, output `scripts/exp023_output.txt`, runtime under a second).

**Question.** Can [LMW26]'s cuboid ("wireframe") bootstrap bound anything from above, in particular the pair
Casimir energy, which is κ for twist lines? The rectangle cannot (EXP-017). A research agent's algebra (EXP-021)
suggested the cuboid is closed under a dressing of its four-body energy; that was unchecked.

**The constraints, read on the source** (2609.04041 End Matter, eqs. 41–46). ⟨D̂(L₁,L₂,L₃)⟩ = 𝒟(r₁,r₂)/V^{8Γ/3}
with r_i = L_i/L₃. (42): 𝒟(r₁,r₂) = 𝒟(r₂,r₁) = 𝒟(1/r₁, r₂/r₁), from invariance under swapping side lengths.
(43): 𝒜(r₁,r₂) = (√r₂/r₁)^{8Γ/3} e^{−(r₁/√r₂)ε₄(r₂)} 𝒟(r₁,r₂) = ∫ S(ε; r₂) e^{−(r₁/√r₂)ε} dε, so 𝒜 is completely
monotone in r₁ for each r₂. Here ε₄(r₂) = ε₄(1/r₂) is the four-body potential of two a, ā pairs on the diagonal
corners of a rectangle, eq. (44). The authors note there are "no obvious sign constraints on derivatives with
respect to r₂". Their bound (46) is Γ^{Y} ≥ −(3/8)ε₄(1).

**Result 1 — four-body dressing.** 𝒟 → 𝒟·exp[E(L₁/√(L₂L₃) + L₂/√(L₁L₃) + L₃/√(L₁L₂))], E ≥ 0. It is symmetric
under all permutations of the sides, so (42) holds, and scale invariant, so Γ is unchanged. It raises ε₄(r₂) by E
uniformly, preserving ε₄(r₂) = ε₄(1/r₂). The leftover factor in 𝒜 is exp[E(r₂ + r₂^{−1/2})/√r₁]. That is a
positive power series in r₁^{−1/2}, and each r₁^{−k/2} is completely monotone, so (43) holds. This confirms the
research agent's claim; my first hand-written leftover had √r₂ where r₂ belongs, which check (ii) caught.

**Result 2 — pair dressing, the part that matters for κ.** 𝒟 → 𝒟·exp[E′ Σ_{i≠j} L_i/L_j], E′ ≥ 0. This is exactly
the rectangle dressing e^{E′(y+1/y)} applied to each of the cuboid's three face orientations: a pure contact
attraction between adjacent parallel edges. It is permutation symmetric and scale invariant. Absorbing its
r₁-linear part shifts ε₄(r₂) by E′(√r₂ + 1/√r₂), which is symmetric under r₂ → 1/r₂. As r₂ → 0 that shift is
E′/√r₂, which is exactly the form in which the pair Casimir energy enters ε₄. With two a, ā pairs at short
separation L₂, E₄ ≈ −2ε^{aā}/L₂, so ε₄ ≈ 2ε^{aā}/√r₂. So this dressing raises the pair energy by E′/2. The leftover
factor, exp[E′((1+r₂)/r₁ + r₂ + 1/r₂)], is completely monotone in r₁.

**Checks.** At 200 random points: both symmetries (42) hold to 6·10⁻³⁹; both leftover formulas hold to 3·10⁻³⁹.
Complete monotonicity ((−1)^k∂^k ≥ 0, k ≤ 6, at r₁ = 0.3, 1, 3, 30) holds for both leftovers at E = 0.5 and 2 and
r₂ = 0.2, 1 and 5. The control (1 + r₁)×leftover, which is not completely monotone, fails at every point, as it must.

**Verdict.** With the constraints the paper states, the cuboid bounds neither its four-body energy nor the pair
Casimir energy κ from above. Its bound (46) can only ever be a lower bound on Γ^{Y}, or a lower bound on ε₄ given
Γ^{Y}. The rectangle (EXP-017) and the cuboid are both closed under the same move, a pure contact attraction
between parallel defects, and that move is invisible to every positivity constraint yet written. Next link of
the bounds chain: a constraint where the Casimir energy enters other than as e^{ε·(geometry)}, if one exists.

**Grade.** Proved (two-line arguments per dressing); numerical checks with a working control; one hand-algebra
slip found by the checks and corrected before any conclusion was drawn.
