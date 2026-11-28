> **[Normaliser mark, 2026-11-28, EXP-100 (5bd59ac)] Normaliser: convention A (same-geometry κ_lat), IR-unconverged; superseded by EXP-100.** Any R here is about 2.2–2.3 × R_D = δκ/κ_free. Register: `notes/NORMALISER_AUDIT_EXP100.md`. The text below is unchanged.

# Addendum to `notes/fable_brief_A_vs_bulk.md`: the EXP-089 (ii) wall-test result (2026-11-26 01:17) [model: Opus 5.5]
**Read this ONLY after your S-a and S-c seals are committed.** Your seal commit must be an ancestor of any commit that cites this file.

The wall test holds the strips fixed at (W₁, W₂) = (2, 4) and moves the walls from P = 4 to P′ = 6 (your pre-declared fallback). The office graded it with all controls passing, against your sealed bands from 7c846a1. The KA at P = 4 reproduces the stored values to 1e-4. The fresh P′ = 6 routes have rc 0 and their internal gates PASS.

| | P = 4 | P′ = 6 |
|---|---|---|
| R | 2.2552 | 2.5561 |
| Y_A | 1.9817 | 2.5089 |
| Y_bulk | 4.4737 | 3.9345 |
| ρ_A = R − Y_A | 0.2735 | 0.0472 |
| G_b = Y_bulk − Y_A | 2.4920 | 1.4256 |
| ρ_bulk = R − Y_bulk (descriptive) | −2.2185 | −1.3784 |

- G_b(4) − G_b(6) = +1.066, which is ≥ 0.5, so the test is not INCONCLUSIVE.
- **f = +0.212**, inside your PRIMARY [−0.3, +0.3] and OUTER [−0.5, +0.5] bands. Registered reading: **"A not wrong"; your seal PASSES.**
- Under your kept premise (the prescription that moves less is closer to P → ∞), ρ_A moves by −0.226 and ρ_bulk by +0.840.
- **Caveats (graded):**
  - The premise is yours, and it is ARGUED.
  - ρ_A is not P-converged: f > 0 means A also drifts, by about 21% of the bulk–A gap.
  - Fixed strips are not the scaling sequence.
  - The test has one P step only.
  - Grade: partially verified (registered and graded, one implementation).
