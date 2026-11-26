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

## Amendment 1 (2026-11-26 ~09:30; before ANY P-1/P-2 run; Bridge confirmed)
**A. EXP-094 (P-2) input path.**
- As registered, `exp084c_run.py 2 6 2` / `4 6 2` cannot run: its `honest(n=2)` reads EXP-084's `exp084/Q_W{W}P{P}b{P}.json`, which do not exist at W2P6/W4P6. This is a registration slip (report 907bf3f).
- Q₂ is now the QA value of **EXP-084's phase-1 code, verbatim** (`exp084_run.py` lines 64–75; wrapper `exp094_honest.py` for (W, P) ∈ {(2, 6), (4, 6)}, writing `exp084/Q_W{W}P6b6.json` in the same format). This is exactly the number 084c's `honest` field would have read.
- σ₂ = `exp083_honest.Geom(W, 6, Wbox=6, c=2).saddle(2)` (EXP-088 (a)'s path).
- **Controls replacing "084c Level 1":**
  - (i) the wrapper, run on (2, 4) and (4, 4), reproduces the stored Q_W2P4b4 / Q_W4P4b4 QA bitwise;
  - (ii) EXP-084's two-path agreement |QA − QB| ≤ 1e-9 relative at W2P6/W4P6 (path B = reversed-order logdet with a looser saddle);
  - (iii) the registered P = 4 KAs (R₂ 0.6826; ΔR₂^A, ΔR₂^bulk bitwise against exp086b_result.json), unchanged;
  - (iv) σ₂ from `saddle(2)` reproduces the stored 084c W2P4 σ₂ sum to 1e-6 (the honest-saddle KA).
- The 084c route-(ii) runs at P = 6 become an optional continuation cross-check. They are not part of the reading. Bands and f₂ are unchanged.

**B2. EXP-093 (P-1) platform.**
- The W2P8 route runs on Sumit's MacBook Air (`ssh air`, Apple M1, macOS 27.2.1, Python 3.14.10; numpy 2.4.3 / scipy 1.17.1 / mpmath 1.3.0, the same versions as here; this Mac is an M4 on Python 3.14.5).
- Only the import closure of `exp081d_route.py` goes over: exp081d_route.py, exp081c_numerics.py, sigma3d.py, tools/{plant_guard, winding, watchdog}.py, tools/{freepct_guard, pgate}.sh. The sha256 manifest is compared on both sides. **No checkpoints go over.**
- **IDENTITY (before W2P8):** a fresh W2P6 route on the Air, pulled back and compared HERE with the stored W2P6 checkpoint (EXP-089).
  - **PASS iff** t0, tsad, all 48 g nodes and the n1c arms agree to ≤ 1e-10 relative, AND `row(6)` from the Air checkpoint reproduces exp089_wall.json's P = 6 row to 1e-4 (the registered KA).
  - Between 1e-10 and 1e-4: report, and the Bridge decides.
- **Operations:** nice 10; caffeinate -i; no-kill watchdog; freepct_guard v3 with LOW = 25 / HIGH = 35 (PID-scoped, pause-only); no caps. Pull-back goes to `exp081d_results/air_pull/`, validated before use.
