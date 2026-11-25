# Brief for Cuspis-personal (Fable): which O(N⁰) critical-coupling counterterm, box A or bulk, at n = 1? (2026-11-26 ~01:00) [model: Opus 5.5]

*Self-contained. Requested by the Bridge for Sumit's Fable window (03:20–05:30). It is a consultation for thinking; compute at most minutes.
All numbers are the office session's runs, graded as stated. Your output is UNVERIFIED until the office checks it.*

## House rules
- **Branch only.** Work in your own worktree `../corner_function-fable` on a new branch. Never commit to main.
- Tag every claim UNVERIFIED and grade it: derived / argued / guessed. Say which steps are standard (with exact references) and which are yours.
- **Seal before measuring.** Commit the prediction(s) of §4 before you run or open anything that could inform them, and state your exposure.
- **Compute:** minutes at most per run, one core, under 1 GB. Report each run's wall time and peak memory (footprint). There are no caps and no kill logic: if something grows, stop it yourself and say so.
- Results go to the Bridge.

## 1. Setup (exact conventions; unchanged from `notes/fable_brief_n2_tension.md`)
- **Lattice:** large-N O(N) vector model on a cubic lattice, a = 1.
  - (x, t) open (Dirichlet), Lx = 3P, Lt = 2P; y periodic, Ny = 4P, handled as Fourier sectors.
  - H_p = diag(4 + m_p²) − A + diag σ, with m_p² = 2 − 2cos(2πp/Ny), and G = H⁻¹.
- **Cut and replicas:** cut C = W consecutive x-sites, centred, at t_c = P − 1. There are n sheets.
- **Coupling:** 1/g(x) = G₁^box(x, x) site by site, so the leading-order box is massless at every site (σ₁ ≡ 0).
- **Estimator:** S = ½Q′(1). R(k) = −(S(W₁) − S(W₂))·norm(k), with W₁ = 2k, W₂ = 4k, P = 4k and norm = 1/(Ny(1/W₁ − 1/W₂)κ).
  - R estimates the O(N⁰) strip coefficient δκ of the 3D WF point. The box is a regulator, and the aspect ratio scales with k.
- **O(N⁰) counterterm (T54/T55; coefficient and sign reproduced by an independent derivation, partially verified: T55's identity is algebraic):** R_corr = R − Y with Y = R[½Σ_x c(x)σ̇(x)], σ̇ = ∂_nσ_n|₁, c(x) = N·δ(1/g(x)).
  - **Bulk:** c = −4C_BZ ∈ [−0.12458, −0.11411]. This bracket is consistent with Hasenbusch's MC β_c(N) (arXiv:2112.03783, checked verbatim), which gives c∞ ≈ −0.1165 to −0.121 (partially verified).
  - **Box A:** c_A(x) = −4Σ B₁⁻¹(x,y)G₁(x,y)G₁(z,x)[G₁(y,z) − G₁(x,z)] (box propagators). This is site-by-site criticality of the box at O(N⁰) (zero-row-sum self-energy), and your own §2c argument for it was "the n = 1 box stays massless".

## 2. What is established (graded)
- **A t0 defect is fixed** (EXP-087; your lead). The inner_beta0 doublet double-count/drop for W ≥ 8 is verified at W8P8 against an independent route (9.2e-7). At W10P10 it is partially verified (KA bitwise; no truth referee).
- **EXP-090 (registered, k ≤ 2.5; confirmation, not blind), corrected R:**

| k | 1 | 1.5 | 2 | 2.5 |
|---|---|---|---|---|
| R | 2.2552 | 4.2334 | 6.5877 | 9.0902 |
| Y_A = R[½Σc_Aσ̇] | 1.9817 | 3.8641 | 6.1049 | 8.5280 |
| R − Y_A | 0.2735 | 0.3693 | 0.4828 | 0.5622 |
| Δ_bb := R[½Σ(c_A − c)σ̇], hi c | −2.4920 | −2.9765 | −3.4507 | −3.7567 |
| Δ_bb, lo c | −2.9026 | −3.6044 | −4.3277 | −4.8842 |

  - g_raw = 4.572 (2-dof slope).
  - **A: ρ_s = +0.043 ± 0.002, "supported" (A flattens).**
  - **Bulk: ρ_s = −0.144 (hi) / −0.249 (lo), "overshoot".**
  - The 085c 1/a² row on Y still fails: Y is curved. A post-hoc fit prefers c₀ + c₁k + c₃/k with c₁ = 5.28 over k² (×3 in rms, 1 dof).
  - Local slopes per unit k: R 3.96, 4.71, 5.01; Y_A 3.77, 4.48, 4.85; Δ_bb(hi) −0.97, −0.95, −0.61 (decelerating).
- **c_A/c map** (interior / wall / next to the cut ends) depends only on P:

| P | interior | wall | next to cut ends |
|---|---|---|---|
| 4 | 0.567 | 0.182 | ~interior |
| 6 | 0.684 | 0.192 | ~interior |
| 8 | 0.751 | 0.197 | ~interior |
| 10 | 0.795 | 0.200 | ~interior |

  - (1 − interior)·P = 1.73, 1.90, 1.99, 2.05, so c_A → c like ~2/P in the interior. The wall value stays at ~0.2c.
- **σ̇ profile** (EXP-088 D; per y-slice).
  - Σσ̇ = −2.697 at W4P8 and −3.069 at W8P8.
  - Shell means of r²σ̇ at W8P8, r from 0 to 9: −0.108, −0.096, −0.077, −0.066, −0.046, −0.025, −0.007. It decays and shows no flat stretch (partially verified: one implementation, EXP-088 D).
  - The W-difference of Σc_Aσ̇ / (c(1 − 2/P)) = 0.307, 0.308, 0.316, 0.326 (k = 1 … 2.5). This is the stored-number check you made before, reproduced.
- **n = 2 (EXP-086/086b; honest exact family, no continuation):** with bulk c the counterterm overshoots R₂'s growth by a ratio of 1.37–1.50. With c_A the ratio is 0.982.
  - The Q2 read: c is n-independent (a coupling), so the whole question is the n = 1 criterion (argued).

## 3. The question (please derive)
The target is δκ of the infinite-volume, bulk-critical WF theory. The box with Dirichlet walls is only a regulator, and it scales with k. Since c_A → c pointwise in the interior as P → ∞, one might expect A and bulk to give the same continuum δκ. Over k = 1–2.5 they do not: their slope difference IS the slope of Δ_bb, about −1 per unit k, decelerating.

1. **Scheme or physics?** Is "box at bulk-critical coupling" (bulk c) or "box massless site by site at O(N⁰)" (c_A) the prescription whose R(k → ∞) is the bulk δκ? Or do both converge to it, differing only at finite P?
   - With bulk c, the Dirichlet box acquires an O(1/N) finite-size mass profile. Is that physical content of the boxed CFT that the W-difference must keep, or a regulator artifact that must be subtracted?
   - Give the argument, not the number. If it turns on the boundary condition (ordinary transition) or on how 1/g is defined in a finite volume, say exactly how.
2. **Asymptotics of Δ_bb(k)** at fixed aspect ratio (P = 4k, W₁ = 2k, W₂ = 4k), from the pieces above:
   - the interior shift c_A − c ≈ −2c/P (plus its subleading form);
   - the wall layer (c_A ≈ 0.2c over O(1) sites);
   - σ̇'s spatial profile and fall-off;
   - norm ∝ 1/(Ny·κ·(1/W₁ − 1/W₂)).

   Does Δ_bb → const, grow ∝ k, or grow ∝ log k? Separate the interior and wall contributions. If it saturates, A and bulk share an asymptotic slope: A's flatness at k ≤ 2.5 is a finite-P transient, and bulk's overshoot is the continuum answer (or the reverse). If it grows ∝ k, the two schemes differ by a 1/a-type term, and only one can be right.
3. **Consistency with n = 2:** your answer to (1) must also explain EXP-086b. There, c_A removes 98% of R₂'s ℓ = 1 → 2 growth, and bulk overshoots it by 37–50%.

## 4. Seals requested (commit BEFORE any computation; state your exposure)
- **(S-a)** The functional form of Δ_bb(k) for k → ∞ with its leading coefficient (sign and size), and your verdict on Q1. Grade both.
- **(S-b)** A zero-compute check on the k ≤ 2.5 values in §2. These are in this brief, so it is NOT blind: label it a consistency check, not a test.
- **(S-c, optional; the Bridge decides whether it is allowed, since it uses k = 3 geometry data):** predict Δ_bb(3) and the interior c_A/c at P = 12.
  - Both come from stored GEOM files (`exp081d_results/exp085c/G_W6P12.json`, `G_W12P12.json`), which NO session has read for these quantities.
  - The office grades it with zero compute. This is not an R(3) prediction; your R(3) seals S-1 to S-3 are already on file and stay as they are.
- If you want a minutes-scale calculation (for example the c_A interior ratio on tiny boxes beyond P = 10, or a lower-dimensional analogue of the wall layer), state what would make it fail before running it, and keep it under 1 GB.
