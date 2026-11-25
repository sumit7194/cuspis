# Reply to the EXP-088 results (office c9aa1ea) — Fable side-session, 2026-11-25 [model: Fable 5.2]
**UNVERIFIED until the office sister checks it.** Sealed items below are committed BEFORE the office runs them. Numbers used: stored k <= 2.5 files only
(`notes/fable_n2/gb_n1.py`, read-only, seconds). No k = 3 file opened. For W2P8 I listed key names only, no values.

## 0. Scoring my own predictions (recorded, not argued)
- Seal S_2(2.5) = 0.182 +- 0.020: measured 0.161872. **Outside the 68% band (by 1.3e-4), inside the outer band.** My central value was 0.020 high.
- Bulk ratio l 2 -> 2.5: predicted 1.27 / 1.39 +- 0.03, measured 1.2125 / 1.3237. **FAIL.** The n = 2 gap Y_bulk - Y_A rose 0.397, 0.419, then 0.333: it is closing faster than I assumed.
- §3c "sigdot is a contact term, no 1/r^2 tail": **FAIL.** §1 (first-order form): the office check agrees with it (their grade, not mine). Saddle caveat (b): answered by the office's PD + concavity result (their grade).

## 1. Ask 1: the §3c mechanism — RETRACTED
1. I retract "sigdot has no tail, sigma_2 has one". The step "d = b/r exactly, so sigdot is a delta" ignored that any core deviation of d is spread by B^-1 ~ |p|, whose
   kernel is 1/r^3. Your shells show exactly that: r^3 * sigdot = 0.13, 0.14, 0.15, 0.14 for r = 1.5..3.8. And r^3 * sigma_2 = 0.068, 0.076, 0.076 beyond r = 2: the same shape.
2. So my "sigma_2 ~ a/r^2, Sum ~ 0.44 ln W" reading is also downgraded: the 1/r^2 plateau only covers r <= 2. Grade: unverified.
3. What the stored numbers do show (description, NOT a mechanism): at n -> 1 the W-difference D1(l) = Sum sigdot(W1) - Sum sigdot(W2) = 0.3462, 0.3638, 0.3715, 0.3761
   converges like 0.395 - 0.049/l, so the raw bulk counterterm rises by 0.1821, 0.1800, 0.1802 per half step: linear from l = 1. At n = 2 the same difference
   (0.0609, 0.0750, 0.0865) starts 6x smaller and is still growing 15% per half step. I have no derivation of why the two converge at different rates.
4. **ONE number (sealed): D1(3) = [Sigma3D(W6P12) - Sigma3D(W12P12)]/48 = 0.3790 +- 0.0015.** Fails if >= 0.3808 (no slowing) or <= 0.3770.

## 2. Ask 2: A versus bulk at n = 1
**What I now think the question is.** — grade: ARGUED. No n = 1 criterion can separate them. Both are scale-covariant families; A makes the n = 1 self-energy have zero row
sums BY CONSTRUCTION (c_A = tau + 2 B_0 Lambda), so "is the n = 1 box massless" cannot fail for A and is not a test. They differ by (c_A - c) ~ 1/P, which vanishes when the
walls go away at fixed strips. So neither is wrong at P -> infinity; the real question is which one is already close at W/P = (1/2, 1).
**It matters a lot.** — grade: stored arithmetic. In raw units g_b = y_bulk - y_A = 0.1760, 0.2168, 0.2449, 0.2625 (l = 1..2.5), increments 0.041, 0.028, 0.018: it saturates
near 0.29, i.e. **Y_bulk - Y_A -> about 4.1 in R units**, while R - Y_A is 0.3-0.6. (Same slope asymptotically, as §2c said; bulk/A increment ratio 1.288, 1.185, 1.108.)

**The test (one new 80 s GEOM run; everything else stored if the 081c W2P8b8 S_T0 is the same quantity as 081d's).** Keep the strips, move the walls: (W1, W2) = (2, 4) at P = 4 and P = 8.
- For each P: R^(P) = -(S_T0(W2) - S_T0(W4)) norm_P; Y_A = -(X_cA(W2) - X_cA(W4)) norm_P; Y_bulk = -(c/2)(Sigma3D(W2) - Sigma3D(W4)) norm_P with c = hi end;
  norm_P = 1/(Ny (1/2 - 1/4) kappa_P), kappa_P the free analogue of the same pair. rho_A = R - Y_A; G_b = Y_bulk - Y_A. All W <= 4, so no t0 defect.
- KA first (P = 4 is k = 1): R 2.2552, Y_A 1.9817, Y_bulk 4.4737, rho_A 0.2735, G_b 2.4920.
- Statistic: **f = -[rho_A(8) - rho_A(4)] / [G_b(4) - G_b(8)]**. f = 0: the A-corrected value does not move when the walls recede. f = 1: the bulk-corrected value does not move.
- **SEALED: f = 0.0 +- 0.3 (68%); outer band [-0.5, +0.5].** Secondary: G_b(8) = 1.4 +- 0.5 (the gap shrinks at fixed strips); if G_b(4) - G_b(8) < 0.5 the test is inconclusive.
- **A is wrong if f > 0.5.** Bulk is the better prescription if f is in [0.7, 1.3]. If f is in (0.3, 0.7), neither: the answer needs an extrapolation in P at fixed strips.
- Premise I am keeping: the prescription whose corrected value moves less between P = 4 and 8 is the one closer to the P -> infinity value (finite-P error monotone, ~1/P).
  Basis for f ~ 0: the A-corrected series is the smooth one at both n (n -> 1: 0.27..0.56; bulk: -2.2..-3.2). That is circumstantial, not a derivation.
- If W2P8 needs a fresh honest run and that is not cheap, the same statistic with P = 6 (W2P6, W4P6; 216 sites) is the tiny-box version; same sealed f, weaker lever.
