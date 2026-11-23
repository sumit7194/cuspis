# EXP-084b REGISTRATION: does the exact-n 1/a² coefficient vanish as n → 1?

*Registered 2026-11-23 (Bridge accepted the four design points plus three notes), after EXP-084 ("mixed"; 6b70078). It follows the Bridge's proposal with my four design points. Runs after EXP-085,
before the 081e routes, ALONE under the no-kill watchdog; n = 5 only in a slot cleared with the other sessions. [model: Opus 5.5]*

## A. Question
- EXP-084 (descriptive) shows the exact integer-n width pair growing like k² (1/a²): R_n/k² ≈ 0.69 (n = 2), ≈ 0.40 (n = 3). The continued R from Q′(1) grows like k (1/a).
- If c(n), the 1/a² coefficient, extrapolates to **0** at n → 1, the honest family and the continuation agree on the leading divergence. The residual 1/a (T54's target) is then the whole n = 1 story.
- If c(1) ≠ 0, the continuation misses a 1/a² piece that the honest family carries. That would point at the continuation itself (non-uniqueness of the n → 1 extension), not at a counterterm.

## B. Measurement
- Exact Q_n (arm b, honest saddle; `exp083_honest.Geom.Q(n, saddle = True)`; machinery unchanged from 084) for **n = 2, 3, 4**, plus **5 if its slot is cleared**, at the four Stage-1 k (width pairs (2k, 4k), P = box = 4k).
- n = 2, 3 are REUSED from EXP-084's stored Q files. No recomputation; the values are bitwise the registered ones.
- S_n = ½Q_n/(n − 1) and R_n(k) exactly as in 084 (stored κ).
- **Per n, the fixed k-fit R_n(k) = c(n)·k² + d(n)·k + e(n)** (4 points, 3 parameters, 1 dof). This separates the 1/a² coefficient c from the 1/a coefficient d.
- **Reference:** the continued R(k) (stored R_T0) through the same 3-parameter fit gives (c_cont, d_cont).

## C. Extrapolation to n = 1 (inference; robustness required)
- Fits of c(n) as polynomials in (n − 1) of order m = 1 … min(#n − 1, 2); the same for d(n).
- Leave-one-n-out at each m where #n − 1 > m.
- c(1) = the value of the highest admissible order. **σ_c = the max spread across orders and leave-one-out fits.**
- **Order-drift test:** |c(1)_m − c(1)_m′| over admissible orders must be ≤ σ_c. Otherwise INCONCLUSIVE, because the extrapolant moves with a non-physical choice.

## D. Reading (pre-stated)
| outcome | condition | meaning |
|---|---|---|
| **c(1) consistent with 0** | \|c(1)\| ≤ 2σ_c, drift OK | the exact-n family and the continuation agree on 1/a²; the 1/a remainder (T54) is the n = 1 question |
| **c(1) non-zero** | \|c(1)\| > 2σ_c, drift OK | the continued Q′(1) lacks a 1/a² piece that the honest family carries; a continuation (non-uniqueness) issue, not a counterterm |
| INCONCLUSIVE | the drift test fails, or #n < 3 | — |

- Also reported, descriptive only: d(1) against d_cont, and c_cont itself (expected ≈ 0 if the continuation is a 1/a series; the stored R/k² falls 2.26 → 1.31).

## E. Controls (all through the same fit and extrapolation code)
| row | planted c(n) on the actual n set | expected |
|---|---|---|
| P-lin | α(n − 1), α = 0.69 | consistent with 0 |
| P-quad | α(n − 1)² | consistent with 0 |
| P-const | α | non-zero |
| P-noise | α(n − 1) + N(0, 1e-3) noise, seed **20261123** (declared now, before any run) | consistent with 0, with σ_c > 0 (the σ machinery has teeth) |
| KA | n = 2, 3 Q values read from 084's files equal the 084 result.json R_n to 1e-12 | PASS |
| MEM | n = 4 peak measured at each k, ascending, alone. n = 5 only in a cleared slot (est. ~8 GB, argued from n² scaling of the measured 3.03 GB at n = 3) | — |

## F. Cost (argued)
- n = 4: ≈ 5.4 GB peak at k = 2.5; minutes per geometry.
- n = 5: ≈ 8.4 GB.
- n = 6 is excluded (≈ 12 GB) unless `logdetB` is made leaner first; that would be a code change requiring bitwise reproduction of the stored n = 2, 3.

## G. Additions at registration (Bridge's three notes)
1. **c and d are correlated over k ∈ [1, 2.5].** σ(c(n)) and σ(d(n)) come from the FULL covariance of the 3-parameter k-fit, as follows.
   - With σ_R(k) from the 084 σ table: cov = s²·(XᵀWX)⁻¹ with W = 1/σ_R², where s² = max(1, χ²/dof).
   - The c–d correlation coefficient is registered and reported per n.
   - Propagation to n = 1: σ_c(1) = max(spread across orders and leave-one-out, linear propagation of the per-n covariances through the highest-order fit).
   - **Plant P-cd:** a synthetic R(k) = c·k² + 0·k + e on the real k-set, with the real σ_R, must return d within 2σ_d of 0 and c within 2σ_c of the planted value.
2. **n = 5:** before it starts, the runner pauses and the session messages the Bridge (Sumit's condition: a swap-heavy hour is announced). It runs alone under no-kill. n = 6 is dropped unless leaner code reproduces the stored n = 2, 3 bitwise.
3. **Pre-stated:** with 3–4 n values, **INCONCLUSIVE is the likely outcome if the order drift is large.** That would be a limit of the n coverage, not a failure of the design.
