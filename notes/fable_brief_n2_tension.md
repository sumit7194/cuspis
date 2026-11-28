> **[Normaliser mark, 2026-11-28, EXP-100 (5bd59ac)] Normaliser: convention A (same-geometry κ_lat), IR-unconverged; superseded by EXP-100.** Any R here is about 2.2–2.3 × R_D = δκ/κ_free. Register: `notes/NORMALISER_AUDIT_EXP100.md`. The text below is unchanged.

# Brief for Cuspis-personal (Fable): the n = 2 counterterm tension (2026-11-25, ~20:00) [model: Opus 5.5]

*Self-contained. Numbers are from the office session's runs, each graded. Please treat it as a consultation: derive, predict, and grade your claims.*

## Setup (exact conventions)
- **Lattice:** large-N O(N) vector model on a cubic lattice, a = 1.
  - (x, t) open (Dirichlet), Lx = 3P, Lt = 2P; y periodic, Ny = 4P, as Fourier sectors (m_p² = 2 − 2cos 2πp/Ny).
  - H_p = diag(4 + m_p²) − A + diag σ (diagonal 6, hopping −1); G = H⁻¹, δG = −GδσG.
- **Cut and replicas:** cut C = W consecutive x-sites centred in the middle third, at t_c = P − 1. n sheets; links across the cut are reconnected from sheet s to s + 1.
- **Coupling:** site-dependent, 1/g(x) = G₁^box(x, x). σ_n is the replica-symmetric gap solution with that 1/g(x) held fixed per site; σ₁ ≡ 0.
- **Bubble and entropy:** B_k = (2/Ny)Σ_p G_p∘G_(k−p). Q(n) = Σ_k log det B_(n,k)[σ_n] − n Σ_k log det B_(1,k); S = ½Q′(1).
- **R_n:** strip pair W₁ = 2ℓ, W₂ = 4ℓ, P = 4ℓ; norm(ℓ) = 1/(Ny(1/W₁ − 1/W₂)κ(ℓ)), with κ the free per-component analogue.
  - R_n(ℓ) = −(½/(n − 1))·[Q_n(W₁) − Q_n(W₂)]·norm(ℓ); continued R = R_(n→1).
- **O(N⁰) critical-coupling counterterm** (T54/T55: coefficient and sign confirmed by an independent derivation):
  - ΔF_n − nΔF₁ = −(N/2)·n·Ny·Σ_x δ(1/g(x))·σ_n(x), hence ΔR_n = (n/(2(n − 1)))·Ny·Δ_W[Σ_x c(x)σ_n(x)]·norm, with c(x) = N·δ(1/g(x)).
  - Bulk: c = −4C_BZ = −0.114 … −0.125 (also confirmed by Hasenbusch's MC β_c(N): c∞ = −0.1165 … −0.121).
  - Box prescription A: c_A(x) = −4Σ B₁⁻¹(x,y)G₁(x,y)G₁(z,x)[G₁(y,z) − G₁(x,z)] (box propagators). In the interior c_A/c ≈ 1 − 2/P.

## What is established
1. **A t0 defect (fixed):** `inner_beta0` double-counted / dropped near-degenerate same-slice pole doublets for W ≥ 7. Fixed and verified:
   - tiny boxes;
   - W8P8, where an independent radius-1e-6 route agrees with the fix to 9e-7.
   - Measured R(2) shift +0.146. Predicted (code logic, which under-counts ~3% at W8P8): R(2.5) +0.87, R(3) ~+0.4. W10P10 is recomputing now.
   - Your earlier inference: after the fix, under prescription A the n → 1 slope ratio is ≈ +0.05 (essentially flat). **Not yet re-read.**
2. **Honest exact n = 2 family** (no analytic continuation and no inner_beta0, so it is unaffected by the defect):
   - R₂(ℓ) = 0.6826, 1.5509, 2.7810, 4.3170 at ℓ = 1, 1.5, 2, 2.5. It is k²-dominated: 3-parameter fit c₂ = 0.612, d = 0.319, with c/d correlation −0.998.
   - The continuation equals the honest family at n = 2 to |ΔR| ≤ 1.5e-5 (EXP-084c).
3. **The n = 2 counterterm** (σ₂ from the stored n = 2 saddles), on the parity-matched pair ℓ = 1 → 2, where honest R₂ grows +2.098:
   - **bulk c:** the counterterm changes −2.88 / −3.14, so the ratio is **1.37–1.50**: it overshoots even R₂'s TOTAL growth (registered reading "overshoot at n = 2").
   - **box c_A (descriptive):** ΔR₂^A = −0.564, −1.416, −2.625 (ℓ = 1, 1.5, 2), so the ratio is **0.982**. The σ₂-weighted c_A/c is 0.54 (P = 4), 0.66 (P = 6), 0.73 (P = 8).
   - **CAVEAT:** using c_A at n = 2 is an assumption, which is question (2) below.

## Questions (please derive; state which steps are standard, with references, and which are yours; grade each claim)
1. **At integer n,** is the first-order form ΔF_n = −(N/2)·n·Ny·Σ δ(1/g)σ_n complete at O(N⁰)? Or do terms enter at n = 2, where σ_n is O(1) and not small, that the n → 1 derivation never sees: O(σ_n²), the response ∂σ_n/∂(1/g), or a counterterm-induced change of the saddle?
2. **Prescription at n = 2:** is the box δ_A(x) (site-by-site criticality on the same box) the correct O(N⁰) counterterm for the integer-n Rényi as well as for n → 1? Or does an integer-n quantity need a different subtraction (e.g. the full box tadpole)? Give the argument, not the number.
3. **The k² growth:** honest R₂ grows ∝ ℓ² (a 1/a² term) while the continued R (n → 1) is linear. With c_A the counterterm removes ~98% of R₂'s ℓ = 1 → 2 growth, k² included. Is R₂'s ℓ² growth ENTIRELY the coupling-mismatch term (so that R₂ + ΔR₂^A → const), or does an integer-n Rényi carry a genuine 1/a² piece (conical/contact terms at the cut) that the counterterm should NOT remove? **Predict R₂ + ΔR₂^A at ℓ = 2.5 (P = 10):** we can compute it from stored data once σ₂ exists there.
4. **Consistency:** if the answers are (1) complete, (2) δ_A and (3) entirely mismatch, then the n → 1 and n = 2 pictures agree and T54-with-box-prescription is the whole story. If not, which branch carries the leftover, and with what sign?
