# EXP-090 REGISTRATION (2026-11-25 ~23:30; nothing computed): re-reads with the corrected t0 (EXP-087) [model: Opus 5.5]

*Bridge request 2026-11-25 ~23:10: register BEFORE W12P12's corrected t0 lands. Every reading below is NEW. 081d, 081e, 085 and 085c keep their
registered readings as recorded. No silent edits.*

## 0. Header: carried items, stated in every headline this registration produces
- **Fable's k = 3 seals (UNVERIFIED inputs; graded, never used as inputs).** Grading rule: PASS iff the measured value lies inside the stated band. All seals are graded and reported, including the one Fable expects to fail.
  - **S-1, original seal** (6156a51, HANDOVER §3, current code): R(t0+L)(3) = **−1.55**. 68% band [−2.0, −1.1]; outer band [−2.5, −0.7]. Sub-seals E(W6P12) = 1.892 ± 0.008 and E(W12P12) = 1.78 ± 0.03. Fable expects this seal to FAIL.
  - **S-2, revised, current code** (ca63760, ADDENDUM §E): R(t0+L)(3) = **−0.07**. 68% band [−0.30, +0.15]; outer band [−0.60, +0.40]. Sub-seals E(W6P12) = 1.895 ± 0.006, E(W12P12) = 1.890 ± 0.02 and X_Λ(W12P12) = 244.958 ± 0.02.
  - **S-3, revised, corrected t0** (ca63760): R(t0+L)(3) = **+0.33**, band [0.25, 0.42]. Fable's fail rule is "outside [0.15, 0.50]"; both are reported, and the stated band [0.25, 0.42] is the PASS criterion. Sub-seal Δt0(W12P12) = +0.0575 ± 0.03.
  - **S-4 (ca63760):** corrected R(t0+L) at k = 2 and 2.5 lies within 0.03 of 0.428 and 0.371.
  - Definitions (Fable's, checked against stored numbers below): E(W,P) := ½t0 + X_Λ with X_Λ := −2Ny·ΣΛd (the `X_Lam` key of `exp081d_results/exp085c/G_W{W}P{P}.json`), and R(t0+L)(k) := −(E(W₁) − E(W₂))·norm(k).
- **OPEN ITEM (EXP-088 (f)): A versus bulk at n = 1.** Whether the box c_A or the bulk c is the correct n = 1 counterterm is ARGUED (Fable §2c, "the n = 1 box stays massless"), not shown. Every A reading below is conditional on it. No reading here decides it.
- **EXP-086 tension (immune).** The honest exact n = 2 family has no inner_beta0, so it is untouched by EXP-087. Its "overshoot at n = 2" (bulk c) stands unexplained. Every headline states it.

## 1. Exposure (not blind; stated so nobody mistakes it for blinding)
- **k ≤ 2.5 is arithmetic on landed numbers.**
  - Δt0(W8P8) = +0.020684 (EXP-087 referee) and Δt0(W10P10) = +0.121780 (EXP-087 recompute) are known. So are ΔR(2) = +0.1457 and ΔR(2.5) = +0.8715.
  - Fable's inferred series is in TODO.md: R 2.2552 / 4.2334 / 6.5838 / 9.0901; R − Y_A 0.2735 / 0.3693 / 0.4789 / 0.5621; slope of R − Y_A +0.195.
  - **The k ≤ 2.5 readings are therefore confirmations, not news.**
- **k = 3 (W₁ = 6, W₂ = 12, P = 12).**
  - Known to me: t0(W12) = −486.137451254695 and T_sad(W12) = +504.570481250655 (route), plus GEOM W6P12/W12P12 run facts (time, peak, T_sad agreement).
  - On disk but not knowingly read: G_W6P12/G_W12P12 X_cA, X_Lam and Sigma3D, so Y_A(3) and X_Λ(W12P12) are not known to me. The held W6P12 route's components (its R was never read) and the W12 route's 𝒞 (still running) are also unread.
  - Nothing at k = 3 is opened before this registration is committed.

## 2. Quantities (one variable changed: t0 on the wide strips)
- **Correction.** For each geometry, Δ(W,P) := t0_fixed − t0_stored, read from these files (no typed constants):
  - `exp081d_results/exp087_referee_W8P8.json` (on_1e-5 − off_1e-5);
  - `exp087_t0_W10P10.json` (on − off);
  - `exp087_t0_W12P12.json` (on − off).
  - Δ ≡ 0 for every geometry without clusters: W2P4, W4P4, W3P6, W6P6, W4P8, W5P10, W6P12. This is by construction and was checked bitwise in EXP-087 D1.
- **Corrected R.** R^c(k) = R(k) + ½[Δ(W₂) − Δ(W₁)]·norm(k), with norm(k) = 1/(Ny(1/W₁ − 1/W₂)κ(k)) and κ stored in `exp081d_results.json`. The same shift is applied to the stored component t0 (R_t0); T_sad and 𝒞 are unchanged (EXP-087 D′).
- **σ of the correction.**
  - σ_Δ(W8P8) = |truth − fixed| = 9.2e-7.
  - σ_Δ(W10P10) and σ_Δ(W12P12) = |fixed − artifact model|. This is a code-against-code PROXY: there is no truth referee at those sizes.
  - It is added in quadrature to the stored σ_R.
  - **Robustness rule:** every reading is recomputed with σ_Δ = 3% of |Δ| (W8P8's model gap fraction). If any band changes, that reading is INCONCLUSIVE (robustness).
- **g_raw^c** := the unweighted 2-dof polyfit slope of R^c over k ∈ {1, 1.5, 2, 2.5} (085c READ code, verbatim). The stored g_raw = 4.019821717340081 is reported beside it.

## 3. Readings
**(R1) Corrected series, descriptive.** Report R^c(k) for k = 1–2.5 (and k = 3 once §5 passes), g_raw^c, and local slopes. There is no band, because 081d registered no slope reading.

**(R2) A, PRIMARY of 085c, re-read with SIGNED bands (085c §D bands verbatim).**
- Inputs: R_corr^A = R^c − Y_A, with Y_A = R[½Σc_Aσ̇] unchanged (no t0 in it). g_A = the 085c `slope_and_sigma` result over k ∈ {1, 1.5, 2, 2.5}, and **ρ_s := g_A / g_raw^c** (registered denominator). The value divided by the stored g_raw is reported, labelled descriptive.
- Bands (the whole ρ_s ± 2σ interval must lie in one):

| reading | condition |
|---|---|
| overshoot | ρ_s < −0.1 |
| supported (A flattens) | −0.1 ≤ ρ_s ≤ 0.1 |
| partial | 0.1 < ρ_s < 0.5 |
| refuted as sole cause | ρ_s ≥ 0.5 |
| INCONCLUSIVE | the interval straddles a band edge |

- **Fixed caveat:** 085c's 1/a² row on Y still fails, since Y is unchanged. So this is a finite-k slope over k = 1–2.5, not a continuum statement, and its headline must say so.
- **Second row once k = 3 exists:** the same, over k ∈ {1, …, 3} (3 dof). Y_A(3) comes from G_W6P12/G_W12P12. If the two rows disagree in band, the reading is "k-range dependent".

**(R3) Bulk c, re-read (085's +c; amendment-5 rule: a reading only if BOTH bracket ends, c = −0.11411 and −0.12458 from `exp085/E.json`, give the same signed band).**
- Inputs: R_corr^bulk = R^c + ½c·ΔSigma3D·norm. ρ_s and the bands are as in (R2).
- 085's reason 1 (test (i) at W4P4) does not depend on t0. It is now bounded: EXP-085w found 99.8% of it is the s_cut tail, and 085c §G bounds |ΔR| ≤ 5.3e-4. It is carried as a named k = 1 caveat, not a void.

**(R4) 081e PRIMARY, k = 3.**
- (a) **081e as registered:** `decide_r` on the stored-t0 R. Reported first and labelled "carries the EXP-087 defect at W8P8 (denominator) and W12P12".
- (b) **EXP-090 corrected:** the same `decide_r`, the same bands (converging ≤ 0.75; log-like 0.87–1.15; power-divergent ≥ 1.33; gaps INCONCLUSIVE) and the same ±2σ_r and T0/T1 rules, applied to R^c with σ from §2.
- Only (b) is the physics reading. Known beforehand: 081d's descriptive extrapolation gave R(3) = 9.2–9.9 (stored t0).

**(R5) Ingredient split, re-read with the outcome map of the ingredient check, verbatim, (a)–(d).**
- Series: t0 + L corrected, 𝒞, Y_A. Thresholds: 0.1·g_raw^c on BOTH parity pairs (1 → 2, 1.5 → 2.5).
- The original check was post-hoc. This re-read applies the same map, now fixed in a registration. k = 3 enters as a descriptive pair 2 → 3 only.

**(R6) Fable seal grading (§0):** S-4 at k ≤ 2.5. S-1, S-2 and S-3 (plus the E and X_Λ sub-seals) at k = 3.

## 4. Controls (each can fail; exit 1 on FAIL)
- **K1, zero-correction reproduction.** With Δ ≡ 0 the script must reproduce:
  - 085c `result.json` RA1, ρ_A and σ_ρA, bitwise;
  - g_raw = 4.019821717340081, bitwise;
  - the ingredient table's slope(t0 + L) = −0.808 and pairs −0.475 / −1.039 to 5e-4 (they were printed at 3 decimals).
- **K2, source KA per geometry.** Each Δ file's OFF value must equal the stored t0 of that geometry (081d checkpoint S_W2.t0, or the W12 route's −486.137451254695) to 1e-10 relative. If it doesn't, that k's corrected values are VOID.
- **K3, placement plant (must fire).** A synthetic Δ = +1 placed on the NARROW strip W₁ = 4 must move R(2) by exactly −½·norm(2) (1e-12). Placed on W₂ = 8, it must move R(2) by +½·norm(2).
- **K4, two-route identity.** RA1 = RA2 per k to 1e-10, after correction (both routes carry the same t0 shift).
- **K5, must-fail sign.** 085c's control (R^c + Y_A) must land in a band different from (R2)'s.
- **K6, E/X_Λ definition check.** E built from stored k ≤ 2.5 files must reproduce Fable's stored R(t0+L) row (0.7615, 0.5381, 0.2865, −0.5005) to 1e-4 before any seal is graded.

## 5. Order and gates
1. Commit this file. Nothing is computed before the hash goes to the Bridge.
2. **k ≤ 2.5 part:** zero compute (seconds), run only on the Bridge's word after step 1. It yields (R1), (R2) first row, (R3), (R5) and S-4.
3. **k = 3 part, after all four gates:**
   - the W12 route ends (rc 0, with the stale-file guard PASS in run_k3);
   - C1 W12 passes (081e rows);
   - `exp087_t0_W12P12.json` exists with KA OFF PASS (K2);
   - 081e F.3 W6 reuse is as recorded.
   - It then yields (R2) second row, (R4), (R5) pair 2 → 3, and S-1/S-2/S-3. If any gate fails, the k = 3 readings are VOID, with the reason stated.
4. Results go to the Bridge only, and the grading goes to the Bridge, not to Fable.

## 6. Grades to be attached
- Corrected values at W10P10 and W12P12: **partially verified** (KA bitwise; code-logic agreement; no independent truth referee).
- Readings inherit that grade, plus the A-vs-bulk condition (§0).
