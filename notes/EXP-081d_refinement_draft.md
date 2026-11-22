# EXP-081d — refinement series for the lattice σ-route (DRAFT, NOT registered, nothing run) [model: Opus 5.5]

Requested by the Bridge on 2026-11-22, after the 081c post-hoc reading (ρ = 1.86). This draft is for scheduling with Sumit.
Amendment D of 081c says a refinement series must be registered separately; this is that series.

## 0. What is known (data in hand; all descriptive and post hoc)
- **Refinement pair** (same physical geometry, lattice spacing halved): (2,4)@P4 box 4 gives R = 2.2552; (4,8)@P8 box 8 gives
  R = 6.4420. Free κ moves +0.47 %.
- **R is a near-cancellation.** By component (`scripts/exp081c_components.py`), R = R_t0 + R_Tsad + R_C:

  | pair | R | t0 | T_sad | 𝒞 |
  |---|---|---|---|---|
  | (2,4)@P4b4 | +2.255 | −36.15 | +38.89 | −0.49 |
  | (4,8)@P8b8 | +6.442 | −123.04 | +129.44 | +0.05 |
  | shift | **+4.19** | −86.90 | +90.54 | +0.54 |

  The shift is the residual of two pieces about 20 times larger than it, the β = 0 sector (t0) and the saddle (T_sad), with 𝒞
  contributing 13 %. Neither piece "carries" it alone. T_sad/|t0| goes 1.0759 → 1.0520.
- **The same cancellation, in the IR direction** ((2,4) box 4, P = 4…12): t0 and T_sad each grow roughly linearly in P (−36 → −86),
  while their sum converges (2.74, 3.14, 3.31, 3.37, 3.38) and R settles at ~2.65. **The cancellation is robust in P and degrades
  only in the width/resolution direction.**
- **Splitting the +4.19 refinement shift** (all pairs exist):
  - P 4 → 8 at (2,4) box 4: +0.39
  - box 4 → 8 at (2,4)@P8: +0.009
  - W pair (2,4) → (4,8) at fixed lattice P8 box 8: **+3.79**
- **Log vs power: not decidable from data in hand.**
  - There is one refinement doubling, so two points. A pure power R ∝ k^p gives p = log₂(6.442/2.255) = 1.51; a log R = c + B ln k
    gives B = 6.04. Both fit exactly.
  - The fixed-lattice W-series at P8 b8 (W = 2, 4, 8) has three widths, and every 3-parameter form (c + d/W + e/W², c + d/W + e ln W,
    …) fits it exactly.
  - Nothing else in hand varies the resolution.
  - The components' W-dependence at fixed lattice, R_t0(4,8)/R_t0(2,4) = 1.80, is closer to the ×2 a ln W term gives than to ×1
    (pure 1/W) or ×4 (∝ W). That is a hint, not a test.

## 1. Question
In the fixed physical geometry of the (2,4)@P4 box 4 pair, does R(k) at resolution k (lattice spacing a/k) **converge**
(R(2k) − R(k) → 0), **diverge logarithmically** (R(2k) − R(k) → const ≠ 0), or **diverge as a power** (increments grow)?

## 2. Design: five resolutions, k ∈ {1, 1.5, 2, 2.5, 3}
Geometry at k: (W1, W2) = (2k, 4k), P = 4k, box = 4k, N_y = 16k (c = 2), so N = 96k² sites per slice and 8k + 1 unique slices.

| k | (W1, W2) | P | box | N | N_y | status |
|---|---|---|---|---|---|---|
| 1 | (2, 4) | 4 | 4 | 96 | 16 | have (081b) |
| 1.5 | (3, 6) | 6 | 6 | 216 | 24 | new, cheap |
| 2 | (4, 8) | 8 | 8 | 384 | 32 | have (081b + 081c) |
| 2.5 | (5, 10) | 10 | 10 | 600 | 40 | new |
| 3 | (6, 12) | 12 | 12 | 864 | 48 | new, the expensive point |
| 4 | (8, 16) | 16 | 16 | 1536 | 64 | **not proposed** (§5) |

- **Why five points over a factor 3, not three over a factor 4:** with three points, the converging model R∞ + A k^−p has three
  parameters and fits any data exactly, so it cannot be distinguished from a log. Five points give two degrees of freedom.
- The half-integer k values are cheap and make two **doubling increments** possible:
  - Δ(1) = R(2) − R(1), which we have: +4.187.
  - Δ(1.5) = R(3) − R(1.5).

## 3. Pre-registered discriminator (to be fixed before any new number)
**Primary statistic:** r = Δ(1.5)/Δ(1).
- Pure log: r = 1.
- Convergence R∞ − A k^−p: r = 1.5^−p.
- Power divergence k^p: r = 1.5^p.

**Bands** (proposed; the Bridge and Sumit fix them):

| r | reading |
|---|---|
| r ≤ 0.6 | "converging" (p ≳ 1.26); a continuum value can be estimated |
| 0.8 ≤ r ≤ 1.25 | "log-like"; a UV log in the σ sector; the lattice route cannot give δκ without its subtraction |
| r ≥ 1.6 | "power-divergent" |
| otherwise | INCONCLUSIVE between the two neighbouring readings |

**Secondary statistic (descriptive):** fits over all five points of
- (a) R∞ + A k^−p,
- (b) c + B ln k,
- (c) c + B ln k + D/k.

Report the residuals and the leave-k=3-out prediction of each.

**Per-component series:** t0, T_sad, 𝒞, and the free κ, all reported per k. If the log sits in t0 + T_sad, that names the saddle /
β = 0 construction as the place to look.

## 4. Controls (each can fail, each has a pre-stated consequence)
1. **Known answer.** The pipeline must reproduce the stored k = 1 and k = 2 S values (≤ 10⁻⁹ in R) before k = 1.5, 2.5, 3 are read.
   Otherwise STOP.
2. **Numerics.** 081c numerics (exact integer H, adaptive refinement, R1 tiers) at every k. A Step-0-style 40-digit reference column
   at k = 3 at the largest |Im α| per checkpoint node, with tolerance 10⁻¹². Cost unmeasured: mpmath at N = 864, possibly hours. If
   it fails, k = 3's s_max is capped per R1.
3. **Residue tolerance = slip 13's rule.** Grade by downstream impact (≤ 10⁻⁷ on R), never a flat relative tolerance inside the
   comparison arm's own error.
4. **Planted must-fire** at k = 3, as in 081c A (ε on G at one node, predicted Δg within 10 %).
5. **Low-rank residue storage**, needed for memory (§5). Low-rank vs full-matrix residues at k = 1, 2 must match ≤ 10⁻¹² on S.
   Planted: rank truncated by one must fail.
6. **Census at every new k** (poles ≤ s_cut, 081b census code).
7. **𝒞 quadrature at the new k:** same 48 nodes. The reduced-node option in §5 has its own known-answer control at k = 1, 2.

## 5. Resources (estimates; **measure k = 1.5 first** and rescale before committing to k = 2.5 or 3)
**Measured at k = 2** (W8P8, 081c numerics):
- 25 ms per G at N = 384 (inverse plus adaptive refinement).
- 6018 G per 𝒞 node (354 per unique slice); t0 35,604 G (886 s); T_sad negligible.
- 52 poles ≤ 3 across 17 unique slices.

**Scaling assumed** (to be verified at k = 1.5): G cost ∝ N³; G calls ∝ unique slices (8k + 1); the W1 geometry ≈ 0.63 × the W2
cost (measured at P8).

| k | s per G | 𝒞 (48 nodes) | t0 | both widths | residue memory (full / low-rank) |
|---|---|---|---|---|---|
| 1.5 | ~5 ms (floor) | ~0.3 h | ~0.04 h | **~0.5 core-h** | 0.1 GB / — |
| 2.5 | ~95 ms | ~9 h | ~1.2 h | **~17 core-h** | ~1.1 GB / < 0.1 GB |
| 3 | ~285 ms | ~34 h | ~4 h | **~61 core-h** | ~2.1 GB / < 0.1 GB |
| 4 | ~1.6 s | ~250 h | ~31 h | ~450 core-h | ~9.8 GB / < 0.2 GB |

- The 𝒞 nodes are independent processes. On 4 cores, k = 3 takes ~15 h wall (two nights at 2 cores, or one long night at 4) and
  k = 2.5 takes ~4–5 h.
- **k = 4 is not night-scale on this machine** by this estimate (~450 core-hours). That is why k = 3 is the top point.
- **Optional saving (its own control):** 𝒞 contributes 13 % of the shift, and nodes at s > 3 carry weight ≲ 4π e^−6π. Fewer nodes
  on [3, 6] could save up to ~40 %, but only if the reduced quadrature reproduces the full 48-node 𝒞 at k = 1, 2 to ≤ 10⁻⁷ in R.
  It is not assumed.
- **Memory:** k ≥ 2.5 needs low-rank residues for parallel processes (control 5). Each process is then ~N² working set: < 0.3 GB at
  k = 3. Declared before launch with formula and measured × 1.5, per the box rules.

### 5a. Measured cost probe (2026-11-22 08:03; `scripts/exp081d_costprobe.py`, timing only, no physics value kept)
Run on a loaded box (load ~8 of 10 cores), so treat timings as ±30 %. Peak memory 0.52 GB.

**Single G, adaptive refinement, probe:** 1.8 / 11.4 / 33.4 / 66.7 / 167 ms at N = 96 / 216 / 384 / 600 / 864.
- The growth is milder than N³ (BLAS efficiency at larger N): N = 384 → 864 is ×5.0, not ×11.4.
- Production per-G is ×1.27 below the probe (k = 2: 25 vs 33 ms; k = 1.5: 9.2 vs 11.4 ms).

**k = 1.5 W2 geometry, measured:**
- Install: 26 s (2432 G, 38 poles ≤ 3 over 13 unique slices).
- One 𝒞 node: 36 s (3900 G, i.e. 300 G per slice).
- t0: 233 s (23,336 G).

**Re-estimated cost, both widths (×1.63 the W2 geometry).** Calls per slice interpolated (300 at k = 1.5, 354 at k = 2); production
per-G = probe / 1.27.

| k | 𝒞 (48 nodes) + t0, W2 geometry | both widths | wall |
|---|---|---|---|
| 1.5 | 0.48 h + 0.07 h | **~0.9 core-h** | — |
| 2.5 | ~5.9 h + 0.7 h | **~11 core-h** | — |
| 3 | ~19 h + 2.4 h | **~35 core-h** | **~9 h on 4 cores: one night** |
| 4 | per-G ~0.6 s, ~135 h + 16 h | **~250 core-h** | still not night-scale |

- The §5 first estimates were 0.5 / 17 / 61 / 450 core-h. The N³ assumption overestimated the large k and underestimated k = 1.5,
  where the per-G floor is ~9 ms, not 5.
- Residue memory is unchanged (full matrices ~2 GB at k = 3), so low-rank storage is still needed for parallel processes.

## 6. What a result would mean (pre-stated)
- **Converging:** R∞ from the fits, with fit-model drift as the systematic. The "+2.4" (k = 1, P-extrapolated) is then a k = 1
  number, and the continuum value is what 081d returns.
- **Log-like:** the σ-route as built carries an unsubtracted UV log. Its O(N⁰) "δκ" is regulator-dependent until the log is
  identified, either physically (an anomalous-dimension-type term, which would need theory) or as a construction mismatch between
  t0 and T_sad. The per-component series is where to look. No sign claim from the lattice route.
- **Power-divergent:** a construction error is near-certain, since a power divergence cannot survive in a physical O(N⁰)
  coefficient. Debug the t0 / T_sad cancellation before anything else.

## 7. Not in this design (stated limits)
- A larger physical box (base (2,4)@P8 box 4, on the plateau). Its k = 2 point is N = 1280, already 4× the cost of k = 3 here.
  The fixed-geometry series answers the UV question; the IR is shown converged separately (P-series).
- k = 4.
- **Half-integer k is not an exact scaling.** W1 = 3 and 5 are odd, so the narrow strip sits half a site off-centre in its box.
  The two placements are mirror images, so the choice is unambiguous. It is still an O(a) geometry difference, which a converging
  fit absorbs as a 1/k term but a two-point increment does not. Mitigation: report r also from the integer-k-only increment
  R(3) − R(2) against R(2) − R(1) (Δk = 1, model-dependent), and use fit (c) over all five points.
- Any change to the σ construction itself.
