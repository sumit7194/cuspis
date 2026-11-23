# EXP-085 (DRAFT for the Bridge; not registered): is R's 1/a growth the missing O(N⁰) critical-coupling counterterm (Neon T54)?

*Draft 2026-11-23. Paper only so far: NO numerics before registration, and all numerics run in the gap after C1 W6, alone, next to 084
(route rule). T54 is outside input, UNVERIFIED except where the Bridge marked it; every T54 formula used here is re-derived below or labelled.
[model: Opus 5.5]*

## A. Derivation (mine, on paper; grades per line)
1. **(exact, from the code definitions)** T_sad = (B) = Σ_z T(z)·σ̇(z), with T(z) = Tr B₁⁻¹·∂B/∂σ(z) = ∂ log det B/∂σ(z): the O(N⁰) tadpole. Since δB[σ̇] = 4G∘δG and δG = −G σ̇ G, this is identical to `saddle_term_c` with σ̇ = 2B₁⁻¹d.
2. **(argued)** Effective action Γ = N[½ Tr log(−∂² + σ) − Σσ/(2g)] + ½ Tr log B[σ] + ….
   - Criticality at O(N⁰) (σ stays 0) needs 1/g_c = ΣG(x,x) + (1/N)·∂_σ log det B|uniform.
   - Production fixes g = g_c(∞) and σ₁ = 0, so the O(N⁰) term −½·δ(1/g_c)·Σσ̇ is absent.
3. **(argued; matches T54 §2)** Split T₀ = −2B̃₁(0)·I_UV + T₀ˢᵘᵇ, with T₀ˢᵘᵇ = −Σ_k G(k)²·[Σ_ex(k) − Σ_ex(0)] and Σ_ex(k) = 4Σ_q B₁⁻¹(q)·G(k+q).
   - The −2B̃₁(0)·I_UV·Σσ̇ = −4I_UV·Σd piece cancels against (A)'s OPE term (the linearised gap equation).
4. **(argued)** T₀ˢᵘᵇ is the tadpole of the MASS-SUBTRACTED self-energy.
   - IR-finite: Σ^ren ~ k² log k, so G²Σ^ren ~ log k/k² is integrable in D = 3.
   - UV pure linear: ∫₀^Λ dk·log(k/Λ) = −Λ, so c/a with no log.
5. **(checked on paper, standard one-loop formula)** In dim-reg, ∫d^Dk/(k⁴(k+q)²) ∝ Γ(D/2−2)·Γ(D/2−1)·Γ(3−D/2)/Γ(D−3), which is 0 at D = 3 (1/Γ(0)). The subtracted piece G(q)·∫k⁻⁴ is scaleless, so it is 0 too. Hence T₀ˢᵘᵇ = 0 in dim-reg, and only the lattice c/a survives.
6. **(argued; Bridge condition 2a)** Finite box versus infinite BZ:
   - The production box is Dirichlet in x and t, periodic in y. T(z) is not uniform: there are wall layers, plus O(1/L) corrections.
   - So T₀ˢᵘᵇ,box = c/a + c′/L + …, and c′/L·ΔΣσ̇ ~ (W/L²) is a k-independent finite piece of R. It shifts the INTERCEPT, not the 1/a SLOPE.
   - The wall layers multiply σ̇'s tail at the walls (distance ~P from the cut edges), which is further suppressed.

## B. Prediction (the constant c computed independently; NOT fitted)
- **c = T₀ˢᵘᵇ,∞ in lattice units**, from Brillouin-zone sums on periodic n³ grids:
  - lattice G(k) = 1/Σᵢ(2 − 2cos kᵢ);
  - B₁(q) = 2Σ_k G(k)G(k+q) and Σ_k G(k)²G(k+q) as FFT convolutions;
  - zero mode excluded (box IR).
- n-sweep: n ∈ {32, 48, 64, 96, 128}, drift reported. "Converged" means |c(128) − c(96)| ≤ 1% of |c|; otherwise c is reported as unconverged and (ii) is INCONCLUSIVE.
- **Predicted corrected series:** R_corr(k) = R(k) − ½·c·ΔΣσ̇_norm(k), where ΔΣσ̇_norm(k) = [Σσ̇(W₁) − Σσ̇(W₂)] put through 081d's R normalisation (÷ Ny ÷ (1/W₁ − 1/W₂) ÷ κ, with S = ½Q′(1)), and the sign fixed by A.1/A.2.

## C. Measurements (in the gap, alone)
1. **σ̇ and Σσ̇** per Stage-1 geometry, k ∈ {1, 1.5, 2, 2.5}, both widths: install, B₁, d, solve. The production code path is unchanged.
2. **Test (i), residual R(x) = d(x) + δG[σ̇](x,x)** at k = 1 (W2P4b4, W4P4b4).
   - It is zero by the construction of σ̇ in the y-zero mode. What it tests is d (from `coincident_dn_c`) against t0's ∂ₙ (from `inner_beta0(dn = True)`), as a per-site comparison of the two coincident-point derivatives.
   - The precision of d is measured FIRST, by contour-radius variation (rad ×2, ×½).
3. The BZ constant c (B), with its n-sweep.

## D. Reading (pre-stated)
| row | condition | meaning |
|---|---|---|
| (i)-consistent | max\|R(x)\| ≤ 10× the measured d precision | (A) and (B) are discretised consistently |
| (i)-mismatch | otherwise | a discretisation mismatch (T54 candidate 2/3); (ii) is still run but read as INCONCLUSIVE |
| **T54 supported** | (i)-consistent AND c converged AND the R_corr slope satisfies \|g_corr\| ≤ 0.1·g_raw (g_raw = 4.02) | the 1/a growth is the missing counterterm (partially verified: one mechanism, one implementation) |
| **T54 partial** | 0.1·g_raw < \|g_corr\| < 0.5·g_raw | the counterterm contributes but is not the sole cause |
| **T54 refuted as sole cause** | \|g_corr\| ≥ 0.5·g_raw | look elsewhere |
| INCONCLUSIVE | (i)-mismatch, or c unconverged | — |

- Corrected values, descriptive only: R_corr intercept and level. A value "consistent with" the C_T-anchored −0.45 means R_corr(k) within ±0.3 of −0.45 at k = 2 and 2.5. This is descriptive and not a δκ claim.

## E. Controls
| row | check | expected |
|---|---|---|
| KA-dimreg | A.5 on paper | done (1/Γ(0)) |
| KA-scaling | c (lattice units) constant over the n-sweep: in physical units c/a scales like 1/a | drift ≤ 1% between n = 96 and 128 |
| KA-IR | the T₀ˢᵘᵇ sum with the subtraction REMOVED (full T₀) must grow with n (IR divergence ∝ B̃₁(0) ~ n) | must FIRE (grows) |
| MUST-FAIL | R_corr with −c (wrong sign) | must NOT flatten the slope (\|g\| ≥ g_raw) |
| MUST-FAIL-2 | R_corr with 0·c | reproduces g_raw (trivial identity check) |
| 084 cross-check | T54 predicts the 084 exact-n pair also grows (the honest saddle is also at g_c(∞)); premise: Σσₙ in the box carries the same O(n−1)·W/L_IR structure | 084 outcome (i) counts against T54 (argued; pre-stated in 3e045ef) |

## F. Open
- The sign of ½·c·Σσ̇ in S follows A.1/A.2 (S = ½Q′(1) contains +½T₀ˢᵘᵇΣσ̇, and the counterterm removes it). This must be cross-checked numerically by MUST-FAIL (if the sign is wrong, the "−c" run would flatten instead).
- Cost: (C.1) needs an install + B₁ per geometry. Measured route peaks: ~2–3 GB at k = 2.5, alone. (B) FFT grids at n = 128 are ~2M complex points per array: small, but they still run only in the gap.
