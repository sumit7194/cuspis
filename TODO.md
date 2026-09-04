# TODO — living list

*Open questions, unverified claims, and deferred work. Consolidated 2026-09-05 after EXP-011: nothing
settled is listed here. Settled items live in `report.md` (EXP-001 … EXP-011) and `RESULT.md` §10.*

## Open — actionable, unowned

- [ ] **The shape residual.** Why does the (σ, κ) trial function reproduce every computed curve to ≈1%
      ([BMW15b], [HHCWM16], [BCV21] all report it; none explains it)? Is the residual universal in
      sign (it overshoots every known curve: +0.9% Einstein at 26.6°, +0.2–0.6% free fields; BCV Fig. 2
      says smaller for μ < 0)? This is the half of the original problem the κ-band reframe leaves open.
- [ ] **The input any bound on κ needs** (RESULT.md §5–6, EXP-011): a growth condition on the
      bulk-channel density of the two-defect function that does not come from the tail itself.
      Named falsifier of the §6 classification: a third bridge (neither an inverted channel with a
      universal lowest state nor locality/anomaly). Entry points not surveyed here: defect fusion,
      Casimir energy of parallel conformal defects (no specific paper cited; verify before citing).
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
  controls first (σ = 1/256, s(π/2) = 0.01183, s(3π/4) = 0.002520, κ = 0.0397 for the scalar;
  σ = 1/128, s(π/2) = 0.02329, κ = 0.0722 for Dirac), then check smoothness of F in t at fixed M
  (branch flips), then decide the M > 15 tail (measured decay 0.83/unit M; ≈4·10⁻⁴ at 5°). Justified
  only if the shape residual becomes the target.
- Closed form of κ₂^f = (2/π)∫₀^∞ y² u²_{1/4}(y) dy (EXP-011): a Painlevé connection-type integral;
  integrable-systems curiosity; no bearing on the bound.
- Cross-dimensional log-convexity of the free-field κ_d (Mellin moments of one c-function, [AM26]
  eq. 4.17): free-field only; the [CH09] table needed to check it did not survive text conversion.
  Unchecked.

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
  value ≈0.0264; a(90°) passes and is 1.9% (s=1) / 1.3% (s=6) below the exact 0.011830 [CHL09].
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
