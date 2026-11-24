# T59 (Neon) answer: Cuspis verification (2026-11-24) [model: Opus 5.5]
*Input: the Bridge's condensation `~/Github/neon_work/cuspis/T59_answer.md` (Neon output; UNVERIFIED data).*

## (a) The outside check of c's value: **NOT VERIFIED; the citation is wrong**
- **arXiv:2211.03590 is a different paper.** Fetched abstract page: C. Bonati, N. Francini, "Non-compact lattice Higgs model with Abelian discrete gauge groups: phase diagram and gauge symmetry enlargement", Phys. Rev. B 107, 035106 (2023), submitted 7 Nov 2022.
  - It is not an O(N) spin-model paper and gives no simple-cubic O(50) J_c. Neon's "Bonati, Pelissetto & Vicari, J_c = 0.2502(3)" has **no verified source**.
  - Two web searches found no such paper. The number must not be used.
- **hep-lat/9305005 exists:** J. Adler, C. Holm, W. Janke, "High-Temperature Series Analyses of the Classical Heisenberg and XY Model", Physica A 201 (1993) 581, submitted 4 May 1993.
  - Its abstract defines K ≡ J/k_B T but states no K_c. The PDF text was not readable, so **K_c = 0.6929 is NOT verified from the source**.
- **Normalisation (argued, mine):** the σ-model here is the Lagrange-multiplier form of the constraint φ_x² = N/g. With unit spins s = φ√(g/N), the action becomes −(N/g)Σ_⟨xy⟩ s_x·s_y. So the standard unit-spin coupling β = N/g, and J ≡ β/N ↔ our 1/g, with J_c(N → ∞) = W/6 = 0.252731.
  - IF a verified β_c(N) for the simple-cubic N-vector model exists, then c_eff(N) = N·(β_c/N − W/6) is the right comparison, up to O(1/N).
  - Possible verified lead, not checked: the Butera–Comi simple-cubic N-vector high-temperature series (hep-lat/9805025, hep-lat/9903010) quote β_c(N).

## (b) Is Neon's n = 2 test meaningful? Does tonight's 084c READ answer (ii)?
- 084c tests P2: the continuation equals the honest family AT INTEGER n (n = 2, Level 2).
  - "agree" means the continuation is right at the integers.
  - It does NOT exclude a leak in the n → 1 DERIVATIVE: two functions can agree at every integer n ≥ 2 and differ at n → 1 (uniqueness needs growth conditions; Carlson).
  - So 084c answers (ii) only partly: it can EXCLUDE a gross continuation error at integers, but it cannot certify Q′(1).
- Neon's (a), the exact integer-n counterterm, is computable **from stored data with zero new compute**:
  - ΔR_n = (½·n/(n − 1))·Ny·c·[Σσ_n(W₁) − Σσ_n(W₂)]·norm(k) (it reduces to 085's formula as n → 1);
  - σ₂ is stored in the 084c files (`c84_W*P*_n2.json`, the "sigma" field); honest R₂ is stored by 084.
  - **But its reading is confounded:** 084 found the exact integer-n R₂ grows like k² (R₂/k² ≈ 0.69), unlike the linear continued R. A counterterm ∝ Ny·Σσ₂ ∝ k cannot remove a k² growth. So "does the overshoot vanish at n = 2" is not well posed without a pre-stated treatment of R₂'s k² term.
  - Worth doing only as a registered descriptive, with that treatment stated.

## (c) Parity / centring at half-integer ℓ (stored data)
- **Geometry:** at k = 1.5 and 2.5 the narrow strip W₁ = 2k is ODD (3, 5) in an even box (6, 10), so it sits **off-centre by ½ site**. At k = 1 and 2 it is centred. That is an O(a) effect.
- **Raw R local slopes:** 3.956 → 4.417 → 3.554. They zig-zag, lower on intervals ending at half-integer k.
  - Integer pair (1 → 2): 4.187. Half-integer pair (1.5 → 2.5): 3.985.
- **The counterterms do NOT zig-zag:**
  - box A Y: 3.765 → 4.482 → 4.846;
  - bulk Y (hi end): 4.734 → 5.430 → 5.458;
  - bulk Y (lo end): 5.168 → 5.928 → 5.959.
  - So the parity effect lives in R (t0/C), not in the counterterm.
- **The overshoot is robust to parity:** on parity-matched pairs, R's slope (3.99–4.19) is below the bulk counterterm's (5.08–5.94) in every pair.
  - Integer pair: bulk 5.08 (hi) / 5.55 (lo) against R 4.19. Half pair: 5.44 / 5.94 against 3.99.
  - The ratio R / Y_bulk spans 0.73–0.82. So parity changes the estimate of the "0.77" by about ±5%; it does not remove it.
- The collinearity Neon notes (linear vs 1/ℓ, ρ ≈ −0.96) applies to the 085c post-hoc 1/k fit (c₁ = 5.28 is fragile). The raw local slopes of the bulk counterterm (≥ 5.4 on the last interval) need no fit.

## (d) Recommendation: the cheapest decisive first moves
1. **Free, tonight:** the 084c READ (Level 2 at n = 2). If it says "disagree", the continuation is implicated directly and branch (ii) becomes primary.
2. **Free (stored data, register first):** the integer-n counterterm test at n = 2 from stored σ₂ + R₂, with R₂'s k² handled as pre-stated (e.g. compare k-slopes of R₂ − ΔR₂ against R₂ on parity-matched pairs). Descriptive unless registered.
3. **For (i) finite-ℓ:** ℓ = 3 needs the PRODUCTION R(3). That is exactly 081e's held W12 route (k = 3; ~29 h, 7.3 GB, registered), not route (ii)'s 160–200 h. The matching counterterm at k = 3 is a 085c GEOM at W6P12/W12P12 (~2–3 GB, minutes–1 h; measure first). That gives a parity-matched ℓ = 1, 2, 3 for both R and Y.
   - This is the decisive test of (i), and it is already registered: 081e. It costs the route time once the Bridge lifts the HOLD.
4. Branch B (c's value): do NOT treat it as disfavoured on T59's basis (the citation fails). If wanted, verify β_c(N) from a real source first (e.g. Butera–Comi); reading only.

## Addendum (Bridge-approved reading): a VERIFIED simple-cubic β_c(N), from Butera & Comi
- **Source (body level, ar5iv HTML):** P. Butera, M. Comi, "Critical specific heats of the N-vector spin models on the sc and the bcc lattices" (hep-lat/9903010, Jan 1999), **Table III**, row "β^sc_c(N) HT Refs. [4], [43]". These are earlier HT determinations quoted there.
  - N = 0, 1, 2, 3, 4: **0.213493(3), 0.2216544(3), 0.45419(3), 0.69305(4), 0.93600(4)**. Table III has no sc entry for N ≥ 5.
- **Normalisation (verbatim, eq. 1):** H = −½Σ_⟨x,x′⟩ v(x)·v(x′) with unit-length spins.
  - Their companion paper (hep-lat/9805025, 1998, eqs. 18–19) gives β̃^sc_c(∞) = β_c/N = **0.2527310098..**, exactly W/6 (mpmath: 0.252731009858663).
  - This **verifies the mapping J = β/N ↔ 1/g at N = ∞** (my argued mapping holds).
- N = 6 (β_c = 1.42895) appears only in an agent's summary of hep-lat/9805025's table, not verbatim. **UNVERIFIED**; it is used below only as a labelled extra point.
- **c_eff(N) = β_c − N·W/6:** N = 1: −0.03108; N = 2: −0.05127; N = 3: −0.06514; N = 4: −0.07492 (N = 6, unverified: −0.08744).
  - Monotone, with shrinking steps (−0.020, −0.014, −0.010).
- **N → ∞ extrapolation (INFERENCE, not verification):**
  - c∞ = **−0.084** (pure c + a/N on N = 1–4; the crudest model, since N = 1 is far from large N; Bridge, reproduced);
  - −0.097 (c + a/N on N = 2–4); −0.107 (c + a/N + b/N² on N = 1–4); −0.116 (same, on N = 2–4); −0.118 / −0.121 (adding the unverified N = 6).
  - **Spread −0.084 to −0.121** across model choices.
- **Reading (corrected wording, Bridge):** the small-N data are **compatible with our bracket [−0.1246, −0.1141] and do not exclude the flattening value −0.088. Branch B is not decided by this.**
  - My first version said the data "argue against branch B". That leaned on the steeper fits and was too strong; withdrawn.
- Contrast with T59: Neon's O(50) number would have been decisive had it existed; its citation is wrong. The verified small-N route does NOT reach its conclusion.

## Addendum 2 (T59c, 2026-11-24): Hasenbusch MC, **verified verbatim**. Branch B (c ≈ −0.088) EXCLUDED
- **Source (verified):** M. Hasenbusch, "Three-dimensional O(N)-invariant φ⁴ models at criticality for N ≥ 4", arXiv:2112.03783 (v1 7 Dec 2021, v2 6 Apr 2022), DOI 10.1103/PhysRevB.105.054428.
  - Single author. The HTML full text (v2) was read verbatim.
- **Model, verbatim eq. (1):** H = −βΣ_⟨x,y⟩ φ_x·φ_y + Σ_x[φ_x² + λ(φ_x² − 1)²], on the simple cubic lattice. "In the limit λ→∞ the field is forced to unit length".
  - So λ = ∞ is the unit-spin N-vector model, with the same normalisation as Butera–Comi: their N = 4 values agree to 1.5e-4, not a factor of 2. Hence J = β/N ↔ 1/g holds (verified at N = ∞ via Butera–Comi's β̃_c(∞) = W/6).
- **β_c at λ = ∞, verbatim:**
  - Table 1: N = 4: 0.93585450(25).
  - Table 4, caption "Estimates of the inverse critical temperature βc for N=5, 6, 8, 10, and 12 for λ=∞, 10 and 5": 1.1813639(5), 1.4286859(9), 1.926761(3), 2.427525(4), 2.929802(11).
  - The paper notes its N = 4 value is consistent with Deng's 0.935856(2) (PRE 73, 056116, 2006). Butera–Comi's HT 0.93600(4) differs by 1.46e-4 (3.6× the HT quoted error); Hasenbusch says the HT estimates "essentially agree" but with "clearly larger" errors. That is plausible for HT extrapolation systematics.
- **c_eff(N) = β_c − N·W/6:** −0.075070, −0.082291, −0.087700, −0.095087, −0.099785, −0.102970 for N = 4, 5, 6, 8, 10, 12. **Monotone decreasing** (every step negative).
- **Extrapolation (inference):**

| model | N range | c∞ | ± (residual) |
|---|---|---|---|
| c + a/N | ≥ 4 | −0.11645 | 0.00074 |
| c + a/N | ≥ 6 | −0.11812 | 0.00029 |
| c + a/N | ≥ 8 | −0.11872 | 0.00009 |
| c + a/N + b/N² | ≥ 4 | −0.12096 | 0.00020 |
| c + a/N + b/N² | ≥ 5 | −0.12057 | 0.00024 |
| c + a/N + b/N² | ≥ 6 | −0.12018 | 0.00022 |

  - Model spread: **−0.1210 to −0.1165 (drift 0.0045)**, inside our bracket [−0.12458, −0.11411].
- **Exclusion of −0.0877 without extrapolation (argued):** c_eff(12) = −0.1030 is already beyond −0.0877, and c_eff(N) is monotone decreasing over N = 4–12. With the single premise that it stays monotone, c∞ ≤ −0.103. (N = 6 sitting at −0.0877 is a coincidence of the sequence, not its limit.)
- **Grade:**
  - **Branch B (c's value being the cause of the ~30% overshoot) is EXCLUDED.** The source is verified verbatim; the exclusion is argued (monotonicity), consistent with every extrapolation.
  - **Our c is independently confirmed** within the model drift: verified data, extrapolation by inference, agreement partially verified.
- **Supersedes addendum 1's "branch B not decided"**, which was based on N ≤ 4 only.
