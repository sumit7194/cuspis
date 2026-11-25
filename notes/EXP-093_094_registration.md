# EXP-093 (P-1) and EXP-094 (P-2) REGISTRATION (2026-11-26 ~05:45; nothing computed): Fable's wall-test predictions from 8a9e4b8 §5 [model: Opus 5.5]

*Bridge go to register (2026-11-26). Fable's values are UNVERIFIED predictions. Both are **not blind to P = 4/6** (sealed after the EXP-089 addendum). They are **blind to P = 8 (P-1) and to n = 2 at P = 6 (P-2)**.*
**Grading, both:** PASS per item iff inside ±1σ as sealed; the ±2σ result is reported beside it.
**Order (Bridge):** on my one core, after the registered W12 chain (route → C1 → W12P12 t0): P-1 (~5–7 h), then P-2 (~3 h), one for one. Exception: P-1's G_b(8) part (GEOM-only, minutes) may run now, as one minute-scale job.

## EXP-093 (P-1): second wall step, strips (W₁, W₂) = (2, 4), walls P = 6 → 8
- **Quantities:** exactly those of EXP-089 (ii) (`exp089_wall.py` `row(P)`, unchanged), at P = 8.
  - R^(8) = −(S_T0(W2P8) − S_T0(W4P8))·norm₈, with norm₈ = 1/(Ny(1/2 − 1/4)κ₈) and κ₈ = `pair(free, 8, W1=2, W2=4, Wbox=8)`.
  - Y_A = −(X_cA(W2P8) − X_cA(W4P8))·norm₈; Y_bulk = −(c_hi/2)(Sigma3D(W2P8) − Sigma3D(W4P8))·norm₈.
  - ρ_A = R − Y_A; G_b = Y_bulk − Y_A.
  - **f(6 → 8) = −[ρ_A(8) − ρ_A(6)] / [G_b(6) − G_b(8)]**, with the P = 6 row from EXP-089 (`exp089_wall.json`).
- **Inputs:**
  - W4P8: the stored 081d route checkpoint (`sigma_W4_P8_box8_…_ckpt.json`, has n1c) and `G_W4P8.json`.
  - W2P8: a **fresh 081d route** (`exp081d_route.py 2 8 8`, CUSPIS_081E unset, the k ≤ 2 convention). The 081c W2P8 checkpoints in `exp081c_results/` have no n1c and are not used. The route must write a NEW file in `exp081d_results/`, where no W2P8 checkpoint exists today (checked). Plus a **fresh GEOM W2P8** (`exp085c_run.py GEOM 2 8`).
- **Predictions and bands:**

| item | sealed | PASS (±1σ) | ±2σ (reported) |
|---|---|---|---|
| G_b(8) | 0.97 ± 0.06 | [0.91, 1.03] | [0.85, 1.09] |
| ρ_A(8) | −0.05 ± 0.04 | [−0.09, −0.01] | [−0.13, +0.03] |
| f(6 → 8) | 0.21 ± 0.08 | [0.13, 0.29] | [0.05, 0.37] |

- **Fable's interpretive lines, reported, not graded:** f ≈ 0 means "A's error dies fast; wall-free value ≈ +0.05". f ≥ 0.4 means "A's error larger than read".
- **INCONCLUSIVE for f** if G_b(6) − G_b(8) < 0.2·G_b(6) = 0.285. This rule is mine: EXP-089's threshold of 0.5 was 0.2·G_b(4), and I scale it the same way. The sealed drop is 0.46.
- **Controls:**
  - `row(4)` and `row(6)` reproduce `exp089_wall.json` bitwise (the same code).
  - The fresh W2P8 route's internal gates pass (B2b, t0 refined vs unrefined, residue, census as in 081d) and rc = 0.
  - The W2P8 checkpoint is newer than the route's start (stale-file guard).
  - G_W2P8: `failed` is empty.
- **G_b(8) part now:** GEOM W2P8 plus κ₈, graded as its own item before the route runs. ρ_A(8) and f wait for the route.

## EXP-094 (P-2): wall test at n = 2, strips (2, 4), walls P = 4 → 6
- **Quantities (honest exact n = 2, no continuation):**
  - R₂^(P) = −½[Q₂(W2P) − Q₂(W4P)]·norm_P, with Q₂ = the `honest` value (arm b) of `exp084c_run.py W P 2` → `exp084c/c84_W{W}P{P}_n2.json`, and norm_P as in P-1 (κ_P from `pair`).
  - ΔR₂^A = Ny·[Σc_Aσ₂(W2) − Σc_Aσ₂(W4)]·norm_P (n = 2 prefactor 1), with σ₂ = the c84 `sigma` and c_A from `G_W{2,4}P{P}.json` (P = 6 files exist from EXP-089).
  - ΔR₂^bulk = Ny·c_hi·[Σσ₂(W2) − Σσ₂(W4)]·norm_P.
  - ρ₂A = R₂ + ΔR₂^A; G₂b = ΔR₂^A − ΔR₂^bulk.
  - **f₂ = −[ρ₂A(6) − ρ₂A(4)] / [G₂b(4) − G₂b(6)].**
- **Inputs:** P = 4 is stored (c84_W2P4_n2, c84_W4P4_n2; G_W2P4, G_W4P4). P = 6 needs **fresh** `exp084c_run.py 2 6 2` and `exp084c_run.py 4 6 2` (~1.5 h each from W3P6 5392 s / W6P6 6716 s; 0.22 GB).
- **Prediction (Fable: GUESSED):** f₂ = 0.05 ± 0.15. PASS iff in [−0.10, 0.20]; ±2σ [−0.25, 0.35]. Fable's line, reported: f₂ ≈ 0.21 would mean "the fraction is a property of the box, the same at every n".
- **INCONCLUSIVE** if G₂b(4) − G₂b(6) < 0.2·G₂b(4). Same scaling rule, mine.
- **Controls:**
  - KA at P = 4: R₂^(4) = 0.6826 (honest, 4 dp; |Δ| ≤ 1.5e-5 against 084's R₂(1) per 084c), ΔR₂^A(4) = −0.5644392004106492 and ΔR₂^bulk(4) = −1.5729028584150315, both bitwise against `exp086b_result.json`.
  - The fresh 084c P = 6 runs pass their Level 1 (|dev| ≤ tol), with rc 0.
  - Σσ₂ at P = 6 from c84 equals the honest saddle (`exp083_honest.Geom(W, 6, Wbox=6, c=2).saddle(2)`) to 1e-6. This is the same check as EXP-088 (a)'s KA.

## Footprint
- P-1: route ~0.4 GB (W2P6 took 0.29 GB), 4.8 h at P^5.8, P⁷ bracket 6.7 h; GEOM W2P8 minutes, < 1 GB expected.
- P-2: 0.22 GB, ~1.5 h each.
- All one core, nice 12, no-kill watchdog, pgate, free ≥ 50% at launch.
