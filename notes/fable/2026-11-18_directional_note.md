# Directional note for cuspis — Fable side-session, 2026-11-18

Untracked scratch. Nothing here is a registered EXP. Cuspis decides what, if anything, goes into `report.md`.
Files: `notes/fable/dim_spread.py`, `dim_spread_L120_output.txt`, `dim_spread_L120.json`, `dim_spread.wd.log`.

## 1. One small experiment: the spread of κ_d/C_T as a function of dimension

**Why.** "Every computed theory" is three independent theories (free scalar, free Dirac, Einstein gravity), plus
their mixtures and a ±1% perturbation (ECG). All three exist for continuous d, and at d = 2 they must agree: the
strip becomes an interval and (d−2)·κ_d/C_T is fixed by the Virasoro anomaly. The record has never looked at d
(only "log-convexity in d", parked). So the cheapest question is whether d = 3 is special or just near d = 2.

**Method.** Free fields: Casini–Huerta dimensional reduction, κ_d = Ω_{d−3}/((d−2)(2π)^{d−2}) · ∫t^{d−3}c(t)dt, with
the 2d entropic c-functions measured on infinite 1d lattices (harmonic chain; staggered-mass hopping chain) at
L = 120 and 240, Richardson in 1/L². Einstein: the Ryu–Takayanagi strip closed form in d. C_T: Osborn–Petkou
free values and the holographic closed form. 5 s, 53 MB.

**Controls, written in the script header before the scan was read (tolerance 0.5%).**

| control | got | reference | |
|---|---|---|---|
| κ₃ real scalar | 0.039644 | 4.179·3/(32π²) = 0.039696 | −0.13% PASS |
| κ₃ Dirac | 0.072227 | 3.8005·3/(16π²) = 0.072201 | +0.04% PASS |
| Einstein κ₃/C_T | 3.70923 | π²Γ(¾)⁴/6 = 3.70923 | PASS |
| thermal Dirac/Einstein, d = 3 | 0.99956 | 12πζ(3)/(4π⁵/27) = 0.99957 | PASS |

Nuisance sweep: L = 120 only, L = 240 only, Richardson; two small-t tail models for the scalar. The d = 3 values
move by ≤ 0.01%, the crossing dimensions below by ≤ 0.003.

**Result.** κ_d/C_T divided by the Einstein value, and the same for the thermal entropy coefficient c_S/C_T:

| d | scalar/Einstein | Dirac/Einstein | scalar/Dirac | thermal S/E | thermal D/E |
|---|---|---|---|---|---|
| 2.02 | (unreliable) | 0.989 | (unreliable) | 1.00 | 1.00 |
| 2.50 | 0.817 | 0.894 | 0.914 | 1.073 | 0.925 |
| 2.75 | 0.933 | 0.935 | 0.999 | 1.179 | 0.947 |
| **3.00** | **1.125** | **1.025** | **1.098** | 1.333 | 0.9996 |
| 3.25 | 1.409 | 1.171 | 1.204 | 1.542 | 1.082 |
| 3.50 | 1.818 | 1.384 | 1.314 | 1.820 | 1.199 |
| 4.00 | 3.254 | 2.109 | 1.543 | 2.667 | 1.556 |
| 5.00 | 12.96 | 6.42 | 2.02 | 6.74 | 3.16 |
| 6.00 | 64.3 | 25.6 | 2.51 | 20.3 | 7.85 |

- Each pairwise ratio is 1 at d = 2, dips **below** 1, and comes back through 1 just below d = 3:
  **scalar/Dirac at d = 2.751, scalar/Einstein at 2.849, Dirac/Einstein at 2.943.**
- At d = 3 the log-ratios (+0.118, +0.025, +0.093) are slope × distance past the crossing
  (slopes 0.83, 0.46, 0.37 per unit d).
- The thermal Dirac/Einstein ratio crosses 1 at d = 3.0016. That is EXP-010's 4·10⁻⁴ coincidence.
- d = 4 with these moments: κ₄ scalar 0.005535, Weyl 0.010762; free 𝒩 = 4 SYM 0.0873 N² against the
  Ryu–Takayanagi 0.05104 N², ratio 0.584. The d = 3 analogue (equal-C_T free mix → Einstein) is 0.930.
- Below d ≈ 2.4 the scalar rows depend on how the 1/log small-t tail is modelled; do not read them. The Dirac
  rows are fine down to 2.02 (c_D → 1/3 analytically).

**Reading (mine; argued, not verified).** For this trio the d = 3 "collapse" is a crossing, not a law:
the curves are tied at d = 2, reverse their order completely between small d−2 (Einstein > Dirac > scalar) and
large d (scalar > Dirac > Einstein), and the three forced crossings fall at 2.75–2.94. The same sentence covers
three facts the record logs separately: the κ band, the Dirac–Einstein c_S coincidence, and no collapse under F₀
(C_T/F relative to Einstein is 1, then 2.42 and 1.41 at d = 3, then 3 and 18/11 at d = 4: monotone, no
crossing — integer anchors only, formulas from memory).

**What it does not do.** It does not say why the crossings sit within 0.25 of d = 3; that is a number. It says
nothing about CFTs outside the trio's hull. It was not predicted: I expected a monotone "shadow of d = 2" and
got a sign change.

**Grade.** Partially verified: one implementation, known answers at d = 3 reproduced, nuisance sweep done.
Not done: a second implementation, a source check of the d = 4 values, a prior-art sweep (M1).

**Disclosures.**
- Run 1 was killed by the pressure-yellow guard at 7 s (peak 2.2 + 0.5 GB, from 2²⁴-point FFT arrays I had not
  budgeted). Pressure was back to normal within seconds. I capped the grids and reran at 53 MB. The rerun
  overwrote run 1's watchdog log.
- Before running I recalled the d = 4 free values as 0.0049 and 0.0097 (Ryu–Takayanagi 2006's estimates, from
  memory). The computed values are 12% higher and match what I recall of the later Casini–Huerta review
  (0.0055; 0.0215 per 4-component Dirac). Both recollections are unverified.

## 2. Ranked directions

**D1. Dimensional continuation (explain; outcome A-partial or E).**
- First step: prior-art sweep on "strip/corner coefficient over C_T across dimensions", then register and redo
  the scan with a second implementation (the Painlevé c-functions, or the published κ_d tables and [AM26]'s
  all-d Dirac formula).
- Control it must pass: d = 3 (done here), and d = 4 against source.
- Extension worth one registration: the EMI curve κ_d/C_T in d, normalised through the second-order shape
  response. If it threads the crossings, "near EMI" and "near a crossing" are the same statement.
- Cheapest test that could cut it down: the Rényi version. (κ_n/h_n)_scalar/(κ_n/h_n)_Dirac is 1 at d = 2 and
  1.137–1.150 at d = 3 for n = 2, 3, 4. Register "crosses 1 in (2.4, 2.9)" against "monotone". If monotone, the
  crossing is an n = 1 feature and only "pinned at d = 2" survives.
- Odds: survives replication 90%; new after a sweep ~50%; accepted as the account of the collapse among computed
  theories ~40%.

**D2. The Mellin-pole formulation, with an exact proposer–verifier (this is the reframing for Sumit's idea).**
- K(d) = ∫t^{d−3}c(t)dt is the Mellin transform of the entropic c-function. Its pole at d = 2 has the universal
  residue c/3; d = 3 is one unit from the pole. Some moments are exact sum rules already (EXP-011's 1/8).
- Engine: integer-relation or symbolic-regression proposer over {π, ζ, Γ}, verifier = 30-digit Painlevé
  quadrature. Data are unlimited and the verifier is exact, which is what the method needs.
- Control: it must recover the known exact moments before any new one is believed.
- Odds of a closed form that fixes a crossing dimension: ~10%. Cheap to try; modest value.

**D3. A ceiling on κ/C_T — I would demote it.**
- In the continued trio the free scalar is the *smallest* κ_d/C_T for d < 2.75. The thermal and F-type envelopes
  do not flip. So "κ/C_T ≤ free scalar" has weaker standing than its sibling conjectures.
- The one structure I can name that is two-sided and not an entropic inequality on a(θ): monotonicity of
  Petz/sandwiched Rényi divergences gives I(A:B) ≤ D_α(ρ_AB‖ρ_A⊗ρ_B) for α > 1, hence κ ≤ κ̃_α. It only helps if
  κ̃_α is tied to C_T, which I cannot argue. Free-fermion strips would be the known-answer ground.
- Odds of a real ceiling from this: 2–3%.

## 3. Sumit's question: can a discovery engine work here?

Not on "κ/C_T across theories", for three concrete reasons:
1. **Data.** Three independent points. Any formula fits three points.
2. **Selection.** All three are mean-field (free or classical gravity) and all three are d-families pinned at
   d = 2. A regression would learn the selection.
3. **Target.** A ceiling is a statement about theories nobody has computed. Regression interpolates data; it
   cannot see a bound from points that all lie under it.

What makes the family's methods usable:
- Swap the theory axis for one where data are free and exact: d (section 1 needed no learning at all) or the
  Mellin moments (D2).
- Use networks or tensor networks as an *instrument* for a new theory point, with the free scalar as the
  known-answer control. That is data generation, not discovery, and it is compute-heavy.
- A proposer–verifier over inequalities returns the prior: any tight conjecture it finds is saturated by the
  free scalar by construction, and the verifier (finitely many curves) is not theorem-or-nothing.

## 4. What I think the framing gets wrong

1. "Theories that share nothing" — they share a continuation to d = 2, where agreement is a theorem.
2. The null is not the constraint range (2.28, ∞). It is the same three theories at other d: ×3.3 at d = 4,
   −18% at d = 2.5.
3. The band says nothing yet about interacting CFTs. The one out-of-hull number in the record is Rényi-2 Ising,
   which needs h₂ to normalise.
4. The recent arc firms up a floor. A floor cannot explain a band whose top is open.

## 5. Addendum after Cuspis's reply (same day): the two ends, and what is structural about d = 3

Checked on the same lattice table (`dim_spread_L120.json`); one implementation.

- **Large-t end.** c(t) → N_p·(t/4)·K₁(2t), N_p = number of particle species (real scalar 1, Dirac 2).
  Measured ratio to that form: 1.004 at t = 3.3, 1.0001 at t = 6.9, for both fields; c_D/c_S = 2.0000 from t ≈ 4.
  (Universal one-particle term of 2d massive entanglement: Cardy, Castro-Alvaredo, Doyon — from memory, verify.)
- **Consequence.** At large d the free-field order is set by C_T per particle species: scalar/Dirac → (d−1)/2.
  Measured: 1.543, 2.020, 2.510 at d = 4, 5, 6.
- **What is structural at d = 3.** scalar/Dirac = (d−1)/2 × 2M_S/M_D. The first factor is exactly 1 at d = 3
  (equal C_T per particle species in 2+1 dimensions). The second runs from 2 at d = 2 to 1 at large d and is
  1.098 at d = 3. So the scalar–Dirac gap at d = 3 is 2∫c_S/∫c_D − 1.
- **One-particle value.** With the one-particle form alone, M = (1/16)Γ(d/2−1)Γ(d/2); at d = 3 every free field
  gives κ/C_T = π²/3 = 3.2899. Scalar = (π²/3)·1.270, Dirac = (π²/3)·1.155, Einstein = (π²/3)·1.127 (no particle
  reading for Einstein).
- **Small-d end.** The scalar is lowest because c_S approaches 1/3 like 1/(2 ln t), which makes its Mellin
  transform non-analytic at d = 2. Dirac/Einstein has measured slope ≈ −0.55 at d = 2; not derived.
- **Open.** Nothing structural found for the two crossings against Einstein. Cuspis's toy-pair test (same
  pinning, different c(t) shapes) is the check for whether their location is generic.

## 6. Is the floor's π²/3 the one-particle π²/3? (Cuspis's question, same day)

**Read: shared normalisation plus a power-of-two coincidence. Argued, not proved.**
1. Floor: π²/3 = 8σ/C_T, the 8 from −log cos(ε/2) = ε²/8 (C3's saturating function) and the σ theorem.
2. One-particle: π²/3 = 8σ/C_T because κ_1p = N_p/32 and σ = N_p/256; the ratio had to be a power of two.
3. 𝔞_min has κ = 0, so it is not a one-particle corner function.
4. The better floor is 16φ*σ; 2.894/(π²/3) = 2φ* = 0.879. It does not tend to 8σ.

**A test that came out void.** Hypothesis: κ_{n,1p} = 8σ_n at n = 2, 3, with σ_n = h_n/(π(n−1)) (from memory).
Required amplitudes written first: n = 2 scalar 0.540, Dirac 0.637; n = 3 scalar 0.436, Dirac 0.545.
Control n = 1: 1.0002, 1.0001 at t = 7 (pass).

| | t = 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| scalar n = 2 | 0.364 | 0.323 | 0.293 | 0.270 | 0.251 |
| Dirac n = 2 | 0.392 | 0.344 | 0.310 | 0.285 | 0.265 |
| scalar n = 3 | 0.271 | 0.237 | 0.213 | 0.195 | 0.180 |
| Dirac n = 3 | 0.311 | 0.270 | 0.242 | 0.221 | 0.204 |

The ratio c_n/[N_p(t/4)K₁(2t)] does not converge: the Rényi c-functions have a different large-t form, so there
is no amplitude to compare. The registration assumed one. Void, not a fail.

**What survives (free fields only).** c(t) ≥ c_1p(t) at every t measured, so κ/C_T ≥ π²/3 for both free fields.
Band = (π²/3) × (1.155 to 1.270); the excess sits at t ≲ 1, limited by c(0) = 1/3 per field and monotonicity.

**By-product.** One-particle κ₄ (real scalar) = 1/(64π) = 0.00497 — the "0.0049" misremembered in section 1.
