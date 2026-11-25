# EXP-089 REGISTRATION (2026-11-25 ~21:10; nothing computed): grading Fable's sealed reply (7c846a1, committed and pushed 20:54) [model: Opus 5.5]

## (i) D1(3) seal
- **Quantity:** D1(3) = [Sigma3D(W6P12) − Sigma3D(W12P12)]/48, from the stored 085c GEOM outputs `exp085c/G_W6P12.json` and `G_W12P12.json`.
- **Premise named:** those GEOM runs used CUSPIS_081E=1 (the 081e production convention at k = 3). σ̇ comes from the d path, which EXP-087 does not affect.
- **PASS iff 0.3770 < D1(3) < 0.3808** (Fable: "fails if ≥ 0.3808 or ≤ 0.3770"; central 0.3790 ± 0.0015).

## (ii) Wall test (A vs bulk at n = 1): fixed strips (W1, W2) = (2, 4), walls moved P = 4 → P′
- **Premise check, answered:** the 081c W2P8 checkpoint has NO `n1c` arms, so 081d's S_T cannot be computed from it; it is NOT the same quantity. **So Fable's pre-declared fallback P′ = 6 is used** (fresh 081d routes W2P6b6 and W4P6b6, ~40 min each; plus 085c GEOM W2P6, W4P6). Its sealed f is unchanged.
- **Per P:**
  - R^(P) = −(S_T0(W2) − S_T0(W4))·norm_P, with norm_P = 1/(Ny·(1/2 − 1/4)·κ_P) and κ_P the free pair (exp081b_run.pair) at that P and box;
  - Y_A = −(X_cA(W2) − X_cA(W4))·norm_P;
  - Y_bulk = −(c/2)·(Sigma3D(W2) − Sigma3D(W4))·norm_P, c = hi end (−0.11410550636913405);
  - ρ_A = R − Y_A; G_b = Y_bulk − Y_A.
- **KA first (P = 4 = k = 1):** R 2.2552, Y_A 1.9817, Y_bulk 4.4737, ρ_A 0.2735, G_b 2.4920 (to 1e-4).
- **f = −[ρ_A(P′) − ρ_A(4)] / [G_b(4) − G_b(P′)].**
- **Grading (Fable's sealed bands, as stated):**
  - PRIMARY f ∈ [−0.3, +0.3]; OUTER [−0.5, +0.5].
  - **A wrong if f > 0.5.** Bulk better if f ∈ [0.7, 1.3]. (0.3, 0.7): neither (a P-extrapolation is needed).
  - **INCONCLUSIVE if G_b(4) − G_b(P′) < 0.5.**
  - Secondary: G_b(8) = 1.4 ± 0.5 was sealed for P′ = 8; at P′ = 6 it is reported, not graded.
- **Premise kept (Fable's):** the prescription whose corrected value moves less between P = 4 and P′ is the one closer to P → ∞.
- **Runs:** sequential, no-kill watchdog, the fleet limit respected (queued behind the W10P10 t0 job unless the Bridge or Sumit say otherwise). CUSPIS_081E unset (the k ≤ 2 convention). W ≤ 4, so no t0 defect.
