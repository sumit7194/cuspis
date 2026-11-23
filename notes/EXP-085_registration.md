# EXP-085 REGISTRATION: is R's 1/a growth the missing O(N⁰) critical-coupling counterterm?

*Registered 2026-11-23 after the Bridge's review of the draft (`EXP-085_registration_draft.md`, kept), with its six points incorporated.
Queue: 084 → 085 → 081e, by a verified runner swap, in the gap after C1 W6, alone. No compute until Sumit's office use ends (Bridge, 2026-11-23).
The derivation is in the draft §A, with grades per line. [model: Opus 5.5]*

## 1. Sign, registered from the derivation (Bridge point 1); NOT settled by the run
1. Q(n) = log det B_n[σ_n] − n·log det B₁; S = ½Q′(1) (081d convention).
2. **(exact; production conventions: σ enters H as +diag σ, δG = −GσG)** d/dn log det B_n[σ_n]|₁ = (A) + Σ_z T(z)σ̇(z), with T(z) = ∂log det B/∂σ(z). So (B) enters Q′(1) with a PLUS sign.
3. **(argued)** T₀ = −2B̃₁(0)·I_UV + T₀ˢᵘᵇ. The first term's contribution −4I_UV·Σd cancels against (A)'s OPE term, leaving S ⊃ **+½·T₀ˢᵘᵇ·Σσ̇**.
4. **(argued)** The O(1/N) critical-coupling counterterm is the linear term that removes T₀ˢᵘᵇ from the O(N⁰) tadpole: in Q units, −T₀ˢᵘᵇ·Σσ. Hence **S_corr = S − ½·c·Σσ̇**, with c ≡ T₀ˢᵘᵇ,lat.
5. **Registered prediction:** R_corr uses **+½c** in the equation of §5. If instead −½c flattens the slope and +½c does not, that REFUTES this derivation; it is not a sign choice. The must-fail run (§7) stays a control.

## 2. Scope: SLOPE only (Bridge point 2)
- The −0.45 comparison is DROPPED. The box term c′/L·ΔΣσ̇ shifts R's intercept by an amount that is not computed, so absolute corrected values cannot be compared with −0.45.
- Absolute R_corr is reported descriptively, with that caveat in words. 085 reads only the 1/a slope.

## 3. Same lattice as production (Bridge point 3)
- c is computed for the SAME lattice action as production:
  - 3D nearest-neighbour Laplacian with diagonal 6 (Slice: 4 + m_p², with m_p² = 2 − 2cos k_y);
  - hopping −1 in x, t, y;
  - σ as +diag;
  - bubble B = 2·G∘G with y handled as Fourier sectors, which is identical to production's (2/Ny)·Σ_p G_p∘G_(k−p).
- Infinite BZ: G(k) = 1/Σᵢ(2 − 2cos kᵢ), B(q) = 2⟨G(k)G(k+q)⟩_k, with ⟨·⟩_k = (1/n³)Σ_k on a periodic n³ grid (zero mode excluded).
- **Check (must pass before c is used):** the FFT G on the periodic n³ grid equals the direct (pseudo-)inverse of the same stencil on the same periodic box at 5 separations to ≤ 1e-12 relative (n = 8, 12).
- **Code identity (shown by reading `Slice.__init__`):** production's per-slice H₀ is this stencil, with Dirichlet x, t and Fourier y. Its slice decomposition was validated against the direct 3D inverse in EXP-080 (`honest_slices` vs `honest_3d_replica`, regression a2).

## 4. c (prediction) and its precision
- c = T₀ˢᵘᵇ = −4·⟨B⁻¹(q)·⟨G(k)²·[G(k+q) − G(q)]⟩_k⟩_q, computed by FFT convolutions, n ∈ {32, 48, 64, 96, 128}.
- σ_c = |c(128) − c(96)|. "Converged" means σ_c ≤ 0.01·|c|; otherwise (ii) is INCONCLUSIVE.
- KA-IR: the unsubtracted T₀ must grow with n (∝ B̃₁(0) ~ n) and must FIRE.
- KA-dimreg: done on paper (1/Γ(0)).

## 5. Normalisation, as one equation (Bridge point 5)
**R_corr(k) = R(k) + ½·c·[Σσ̇(W₁) − Σσ̇(W₂)] / (Ny·(1/W₁ − 1/W₂)·κ(k))**
- with W₁ = 2k, W₂ = 4k, Ny = 16k, κ(k) the registered Stage-1 free values, and Σσ̇ = Σ_x σ̇(x) in lattice units (σ̇ = 2B₁[0]⁻¹·d, production path).
- **Planted test:** a synthetic ΔΣσ̇ = 1, c = 1 at k = 2 must give ΔR = ½ / (32·(1/4 − 1/8)·0.017743) = 7.045031843543933 (computed, python), through the same code path, to 1e-12.

## 6. Reading: bands on the whole ±2σ interval (Bridge point 4)
- g = least-squares slope of R_corr vs k over k ∈ {1, 1.5, 2, 2.5}: 4 points, 2 parameters, **2 dof**.
- σ_g = (σ_fit² + σ_prop²)^½, where σ_fit is the standard error from the 2-dof residuals, and σ_prop is propagated from σ(Σσ̇) (contour-radius variation) and σ_c.
- Ratio ρ = |g| / g_raw, with g_raw = 4.020 (the registered Stage-1 slope).

| reading | the whole interval ρ ± 2σ_ρ lies in |
|---|---|
| T54 supported | ρ ≤ 0.1 |
| T54 partial | 0.1 < ρ < 0.5 |
| T54 refuted as sole cause | ρ ≥ 0.5 |
| INCONCLUSIVE | straddles a band edge; or test (i) mismatch; or c unconverged |

- Test (i): max|R(x)| ≤ 10× the measured d precision gives (i)-consistent; otherwise mismatch, and (ii) is read INCONCLUSIVE.

## 7. Controls
| row | check | expected |
|---|---|---|
| MUST-FAIL sign | R_corr with −½c | ρ ≥ 1 (the slope does not flatten); if it flattens, §1.5 applies |
| zero | R_corr with c = 0 | reproduces g_raw exactly |
| planted normalisation | §5 | 7.045031843543933 to 1e-12 relative (an earlier draft value of 0.88062 was an arithmetic slip, caught before registration) |
| same-lattice | §3 FFT vs direct inverse | ≤ 1e-12 |
| KA-IR | unsubtracted T₀ grows with n | FIRES |
| 084 cross-check | T54 predicts 084 ≠ (i) | pre-stated (3e045ef) |

## 8. Later, optional (Bridge point 6)
Σσ̇ at W6P12b12 and W12P12b12 (W12 is ~7 GB alone) gives a corrected k = 3 point once 081e lands. It is queued AFTER 081e and is not part of this reading.

## Amendment 1 (pre-run, 2026-11-23; NOTHING of 085 has run). Found by the Bridge.
- §5's planted expected value 7.045031843543933 used κ(2) ROUNDED to 0.017743. The code reads κ_stored(2) = 0.017743046048925182 (`exp081d_results.json`), and through the same path ½/(32·0.125·κ_stored) = **7.04501355941485** (2.6e-6 relative difference). A correct implementation would have FAILED the 1e-12 tolerance.
- **Rule (same family as the wrong-path tolerance slip):** expected values are computed from the exact inputs the code reads. The planted expected value is therefore defined as ½/(Ny·(1/W₁ − 1/W₂)·κ_stored(2)), evaluated from the JSON at run time. It is not a typed constant.
- Likewise **g_raw = the least-squares slope of the stored R_T0(k)** (JSON), not the typed 4.020.
