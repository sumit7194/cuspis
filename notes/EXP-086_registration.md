# EXP-086 REGISTRATION (2026-11-24; nothing computed): the T54 counterterm at INTEGER n = 2 (no continuation) [model: Opus 5.5]

*Sumit's GO via the Bridge ("do the free things now"). Neon T59 test (a), corrected for the structure 084/084b found. It uses stored data only: zero compute.
**Exposure declared:** while checking the file format I saw W2P4's Σσ₂ = −0.706 (an input, not the result). Nothing else of σ₂ was read, and no ΔR₂ was computed.*

## Why it matters
- 085/085c: every T54 prescription overshoots R's continued 1/a slope by ~30%.
- Two branches remain: (ii) a continuation leak in Q′(1) (T59), or a genuine second contribution / c's value.
- At integer n there is no continuation. If the counterterm cancels honest R₂'s O(1/a) part at n = 2, the n → 1 overshoot implicates the continuation. If it does not, the overshoot is not continuation-specific.

## Inputs (all stored; premises named)
- **Honest R₂(k)** for k ∈ {1, 1.5, 2}: `exp084/result.json` Rn["2"] (084, registered; KA'd in 084b).
- **R₂'s linear coefficient d(2) and k² coefficient c(2):** 084b's registered per-n 3-parameter fit, `exp084b/result.json` fits["2"] (4 k).
  - **Premise P-cd:** c and d are −0.998 correlated (084b's known degeneracy). d(2) is treated with the systematic below.
- **σ₂:** `exp084c/c84_W{W}P{P}_n2.json` "sigma", i.e. route (ii)'s continued-saddle gap solution AT n = 2, for k ∈ {1, 1.5, 2}.
  - The W8P8 file is pending until part 8 ends.
  - **Premise P-σ:** equals the honest saddle σ₂ at the precision implied by 084c Level 1 (Q agreement ≤ 1.1e-9; argued).
- **c:** bulk, at BOTH amendment-5 bracket ends (`exp085/E.json` "ends": −0.11410550636913405 and −0.12457826330924628). The same-band rule applies at both ends.
- κ, Ny, norm(k): the stored 084 normalisation (same function as 084/085).

## Counterterm at integer n (derived; it reduces to 085's formula as n → 1)
- ΔF_n − nΔF₁ = −(n/2)·Ny·c·Σ_xt σ_n (σ₁ = 0). With Q = 2(F_n − nF₁) at O(N⁰): ΔQ_n = −n·Ny·c·Σσ_n.
- With R_n = −(½/(n − 1))·[Q_n(W₁) − Q_n(W₂)]·norm(k):
  **ΔR_n(k) = (n / (2(n − 1)))·Ny·c·[Σσ_n(W₁) − Σσ_n(W₂)]·norm(k).** At n = 2: ΔR₂ = Ny·c·ΔΣσ₂·norm.

## k² treatment (pre-stated)
- Honest R₂ is k²-dominated (084b: c(2) = 0.61). The counterterm is expected ∝ k (Ny ∝ k, ΔΣσ₂ = O(1), norm ≈ const), so it cannot touch a k² term.
- So the k² part of R₂ is **set aside**: it is 084/084b's finding and not addressed here.
- **Only the LINEAR coefficient is compared.**
  - g_ct := least-squares slope of ΔR₂(k) over k ∈ {1, 1.5, 2} (3 points, 1 dof; σ from the fit residual).
  - d_corr := d(2) + g_ct.
- **Reading quantity:** η := d_corr / |g_ct|, the corrected linear coefficient in units of the counterterm's own slope. This is robust to d(2) being small.
- **Systematic on d(2):** σ_d,sys := |d(2)[3-parameter fit, 084b] − d(2)[2-parameter fit c·k² + d·k (no constant), same 4 k]|. σ_η combines σ_d,sys, d(2)'s statistical σ and σ(g_ct).

## Reading (signed bands on the whole η ± 2σ_η interval; same at both c ends)
| reading | condition | meaning |
|---|---|---|
| **cancels at n = 2** | −0.1 ≤ η ≤ 0.1 | integer-n T54 is consistent. The n → 1 overshoot implicates the CONTINUATION (branch ii) |
| **overshoot at n = 2** | η < −0.1 | the overshoot persists without continuation, so it is NOT a continuation leak |
| **under at n = 2** | η > 0.1 | the counterterm is smaller than R₂'s linear part at integer n |
| INCONCLUSIVE | straddles a band edge, the two c ends differ, or a control fails | — |

## Controls
| row | check | expected |
|---|---|---|
| planted normalisation | ΔΣσ₂ = 1, c = 1, k = 2, n = 2 gives ΔR = Ny·norm(2), with norm(2) recomputed independently from the stored κ | 1e-12 relative |
| n → 1 reduction | the formula at n = 1 + 1e-6 with Σσ_n := (n − 1)·Sigma3D/Ny (stored 085 C) reproduces 085's ½c·ΔSigma3D·norm | ≤ 1e-5 relative |
| zero | counterterm × 0 gives d_corr = d(2) | bitwise |
| must-fail sign | −ΔR₂ | lands in a band different from the registered one (stated); fires iff it differs |
| KA inputs | Rn["2"] read here equals 084 result.json; fits["2"] equals 084b result.json | bitwise |

## Running
- Zero compute (reads stored JSON). It runs once `c84_W8P8_n2.json` exists, after part 8's W8P8. Nothing is run before this registration is committed.

## Pre-read note (Bridge, 2026-11-24; nothing read)
- The 3 k points mix parity: k = 1.5 has W₁ = 3 off-centre by ½ site, and parity zig-zags R's local slope by ~10%.
- So beside η the run also reports, **DESCRIPTIVELY**, the parity-matched k = 1 → 2 slopes of honest R₂ and of the counterterm ΔR₂, at both c ends.
- INCONCLUSIVE is the expected likely outcome (the d(2)/c(2) degeneracy); that is acceptable.
