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
