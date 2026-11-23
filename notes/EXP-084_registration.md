# EXP-084 REGISTRATION: where does R's 1/a growth live? The exact integer-n width pair

*Registered 2026-11-23 (Bridge review of draft eaa88f0, with its additions). GO at the measured memory (0.062 GB at k = 1.5), with each larger k
measured progressively; any geometry whose peak would not keep pressure green beside the 081e route queues after 081e.
The draft (`EXP-084_registration_draft.md`) is kept. [model: Opus 5.5]*

## A. Question and premises
As in the draft (§A, §B), kept verbatim:
- the estimator is exonerated by the k-stable free κ;
- the exact-n width-pair coefficient is argued UV-finite in the continuum (local conical terms cancel in the pair; the edge–edge σₙ cross term has only integrable singularities);
- **caveat:** σₙ ≠ σ₁, and the MFS conical behaviour near d = 3 means n-dependent growth could be physics.

## B. Measurement
- Geometries as in Stage 1: (W₁, W₂) = (2k, 4k), P = box = 4k, c = 2, for k ∈ {1, 1.5, 2, 2.5}.
- Exact Q_n = `exp083_honest.Geom(W, P, Wbox = P, c = 2).Q(n, saddle = True)` for n = 2, 3 (arm b). Arm a (σ = 0) is reported only.
- **S_n = ½·Q_n/(n − 1)**, the analogue of 081d's S = ½Q′(1).
- **R_n(k) = −[S_n(W₁) − S_n(W₂)] / Ny / (1/W₁ − 1/W₂) / κ(k)**, with κ(k) the registered Stage-1 free values (0.017660, 0.018206, 0.017743, 0.017468).
- **Reference column (Bridge):** the continued R(k) from Q′(1) at the same four k (registered Stage-1 values) goes through the SAME ratio.

## C. Ratio and bands (corrected: the 081d bands do NOT transfer to the shifted ratio)
**r = [R(2.5) − R(1.5)] / [R(2) − R(1)].** For R ∝ k^p this is r(p) = (2.5^p − 1.5^p)/(2^p − 1), and ln(5/3)/ln 2 at p = 0.

The bands are the 081d **p-bands**, mapped through r(p) (`exp081d_results/e084_ratio_map.txt`):

| reading | p | r |
|---|---|---|
| converging | ≤ −0.71 | ≤ 0.587 |
| log-like or slow power | \|p\| ≤ 0.35 | 0.659–0.822 |
| power-divergent | ≥ 0.70 | ≥ 0.914 |

- Gaps are INCONCLUSIVE. A reading needs the whole r ± 2σ_r in one band.
- Linear growth (p = 1) gives r = 1.000.
- **Reference (computed now, from registered numbers only):** continued r = 0.952, p_eff = 0.83, so power-divergent.
- Note: with the 081d numbers, linear growth would wrongly read "log-like". Caught on paper before registration.

## D. Precision (Bridge: measured on the PARTS, before any ratio is formed)
- Each Q_n(W, P) is computed by two numerically different paths:
  - A: the default;
  - B: the slice sum in reversed order, with the saddle Newton stopped at a tolerance of 1e-11 instead of 1e-13.
- σ(Q_n) = |A − B|, propagated linearly to σ(R_n(k)), then to σ_r and σ_r23 = (σ_r2² + σ_r3²)^½.
- The σ table is written to disk BEFORE the script forms any R_n or ratio (script phase order: Q values → σ table → R → ratios → reading).

## E. Reading (all outcomes pre-stated). g = least-squares slope of R vs k over the four k; g_cont = 4.02.

| outcome | condition | pre-stated meaning |
|---|---|---|
| **(i) continuation** | n = 2 and n = 3 both read converging or log-like | the 1/a defect is in the n → 1 continuation (the t0/T_sad construction) |
| **(ii-a) σ-sector, n-independent** | both power-divergent, \|r₂ − r₃\| < max(0.15, 3σ_r23), and g_n ≥ 0.5·g_cont for both n | the growth is upstream (Π = 2G∘G on the replica lattice) and of the same order as the continued slope; the continuation would be exonerated (argued, conditional on this outcome) |
| **mixed (both loci contribute)** | both power-divergent, \|r₂ − r₃\| < max(0.15, 3σ_r23), but g_n < 0.5·g_cont for some n | a σ-sector growth exists but is too small to account for the continued slope; the continuation also contributes |
| **(ii-b) n-dependent** | both power-divergent and \|r₂ − r₃\| ≥ max(0.15, 3σ_r23) | genuine conical O(N⁰) physics cannot be excluded; no defect localised |
| **INCONCLUSIVE** | anything else (gaps, mixed readings across n, non-monotone) | — |

- No δκ physics reading under any outcome.

## F. Controls
| row | check | expected |
|---|---|---|
| KA | float64 W2P2 (Wbox 4) arm-b Q(2), Q(3) against the 400-digit Arb values | **dry run: 4.0e-13 / 3.7e-13. PASS** (rerun inside the script) |
| SAD | saddle Newton converges at every geometry and n | it raises otherwise, and the geometry is void |
| PLANTS (reading function, synthetic series) | const + 4k (both n) → (ii-a); const + 0.5·ln k → (i); const + 1/k → (i); 4k at n = 2 with 4·k^1.5 at n = 3 → (ii-b) (r₁ = 1.000 vs r₂ = 1.157, Δ = 0.157 > 0.15); 0.5·k (both n) → mixed (g = 0.5 < 2.01); k^0.5 → INCONCLUSIVE (r = 0.862, in the gap) | all six must give their label, or the script exits 1 before reading the data |
| MEM | peaks measured per geometry, k ascending; the hard cap per job is 0.8 GB | a geometry over the cap queues after 081e |
