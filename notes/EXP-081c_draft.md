# EXP-081c — DRAFT registration (not registered; sent to the Bridge for review 2026-11-22) [model: Opus 5.5]

Re-measures the EXP-081b lattice nuisance σ_W as a new experiment. **EXP-081b stays INCONCLUSIVE on the record,
unchanged.** Nothing in this draft is computed until the Bridge approves it.

## 0. Disclosure (what has been seen)
- The EXP-081b descriptive value, R∞ = 2.41 ± 0.29 with σ_W excluded, has been seen by Cuspis and the Bridge. Its σ-count
  is withdrawn and must not be quoted (report.md, 2026-11-22).
- All EXP-081b R(P), the failed σ_W (R48 = 32.7 from a truncated W = 8 calculation) and the N4 value 1.6·10⁻⁴.
- **Prerequisite diagnostics run since the Bridge's decision.** None computes a W = 8 g, S or R.
  - **N4 root cause** (`scripts/exp081c_n4diag.py`): β = 0 part X = t0 + T_sad of W4P4 and W4P6 against s_cut 2 … 3.5.
    The pole census is complete to 3.5. Values below.
  - **W = 8 G accuracy** (`scripts/exp081c_w8diag.py`): G-level only, at the 081b checkpoint nodes, against mixed-precision
    reference columns (residual 10⁻²⁹ … 10⁻³²).
  - **Resource dry run** (`scripts/exp081c_dryrun.py`): G-call counts with a dummy G, plus inverse timings.
  - **Free side only:** κ_lat for (4,8)@P8 box 8, (2,4)@P8 box 8 and (2,8)@P8 box 8.

## 1. What the diagnostics found (and why they shape the design)
- **EXP-081b's N1 reference was the weaker method at W = 8.** At the worst tail ingredients:

  | node | Woodbury | 081b `_G_direct` (H0 = inv(G0), a double inversion) | direct inverse of the **exact integer** H(α) |
  |---|---|---|---|
  | s = 0.94 | 4.8·10⁻⁶ | 1.6·10⁻⁵ | 2…4·10⁻⁹ |
  | s = 1.97 | 1.7·10⁻³ | 2.2·10⁻³ | 1·10⁻⁸ … 1.3·10⁻⁷ |

  - So "W8 failed N1" measured both methods' errors. The nuisance was never measured (the Bridge's point).
  - For W = 2 and 4, the N1‴ agreement of two different methods and the independent N2′ mpmath referee (W4P4) still
    stand.
  - Even the exact-H0 inverse is conditioning-limited (~10⁻⁷) at Im α ≈ 5. Hence one refinement step and an
    a-posteriori check (below).
- **N4 root cause: a mis-specified tolerance, not a numerics error.**
  - X(s_cut) converges geometrically. For W4P6 the increments are 1.3·10⁻³ (2 → 2.5), 9.1·10⁻⁵ (→ 2.75), 2.0·10⁻⁵ (→ 3),
    4.8·10⁻⁶ (→ 3.25) and 1.6·10⁻⁶ (→ 3.5); each 0.25 step shrinks by ≈ e^{−2π/4}.
  - The 081b test (2.5 vs 3) measured the contribution of the poles in (2.5, 3]. It did not measure the remainder beyond
    3. The 10⁻⁶ tolerance came from a single-pole e^{−2πs} estimate that omitted the N_y² slice-pair multiplicity and the
    ∂ₙ kernel 2πs·e^{−2πs}.
  - The actual remainder at s_cut = 3 is X(3.5) − X(3) = 6.5·10⁻⁶ for W4P6. That is ΔR ≈ 2·10⁻⁵, about 1·10⁻⁵
    relative.
- **Free side, resolution at fixed physical geometry:**
  - (4,8)@P8 box 8 is exactly the 2× refinement of (2,4)@P4 box 4: 24×16 vs 12×8, N_y 32 vs 16, widths doubled.
  - κ_lat = 0.017743 vs 0.017660: **+0.47%.** The free (2,4) pair is resolution-stable at the 0.5% level.
  - The large P-dependence of κ_lat (0.0177 → 0.0334 for P = 4 → 12) is a box (physical) effect.

## 2. Geometries
- **W8P8 box 8** (the nuisance target) and **W2P8 box 8** (new; separates resolution from box).
- Reused from 081b, unchanged: W4P8 box 8, W2P8 box 4, W4P8 box 4, W2P4 box 4, W4P4 box 4.
- Positive-control recomputations under the new numerics: W4P8 box 8 and W2P8 box 4 (§4).

## 3. New numerics (production path for all 081c σ computations)
- **G(α)** = direct inverse of the exact integer H(α) = H0 + twist. H0 is the 5-point stencil with 4 + m² on the
  diagonal, built from integers (not inv(G0)).
- **One step of iterative refinement:** G′ = G + G·r, with r = I − H(α)G. The residual is evaluated in double-double
  arithmetic, which is exact enough because H is a stencil plus 2W twist entries.
- **Residues:** R±_j by the contour of the refined direct G (radius from pole spacing, as in `_poles`), so that tails and G
  are consistent.
- **Poles:** QEP, gated by the 081b census at s ≤ s_cut for every 081c geometry.
- **β = 0 term (t0, confluent contours):** the same refined direct G. Merge tolerance 10⁻²·rad (the 081b fix).
- **Step 0, an implementation test before any σ:**
  - Refined G must match the 40-digit mixed-precision reference columns of `exp081c_w8diag.py` (6 columns, Im α up to
    4.96) to ≤ 10⁻¹².
  - Unrefined exact-H0 must reproduce the recorded 2·10⁻⁹ … 1.3·10⁻⁷.
  - This fails if the double-double residual is wrong.

## 4. Positive control on the production path (the Bridge's item 3), before W8P8 is read
- Recompute **W4P8 box 8** and **W2P8 box 4** with the new numerics, and compare with the EXP-081b checkpoints:
  - every 𝒞 node: impact |Δg|·π/cosh²(πs) ≤ 10⁻⁷;
  - |Δt0| ≤ 2·10⁻⁶ and |ΔT_sad| ≤ 2·10⁻⁶;
  - |ΔS| ≤ 10⁻⁶ per geometry. That bounds ΔR at ~4·10⁻⁶.
- **If either geometry fails, STOP.** The new numerics or the 081b values are wrong; diagnose before anything else. W8P8
  is not read.

## 5. Reliability rule for W8P8 (the Bridge's item 4)
- **N1‴c:** at the 081b checkpoint nodes (s ≈ 1, 2, 3, 4, 5), g from refined G (production) vs g from unrefined
  exact-H0 G.
  - Per-node impact ≤ 10⁻⁷ and cumulative ≤ 10⁻⁷, as in 081b (registered a206381/019439c), with the comparison pair
    changed.
  - This is conservative: it bounds the unrefined error, which exceeds the refined one.
  - **Must-fire:** the same check with the unrefined G replaced by 081b's Woodbury G must fire at W8P8 (G-level errors
    1.7·10⁻³ at s ≈ 2).
- **t0 check:** t0 refined vs unrefined, |Δt0| ≤ 2·10⁻⁶.
- **Residue check:** residues from the refined direct G vs the unrefined direct G, at every pole ≤ s_cut, relative
  ≤ 10⁻⁸.
- **W8P8 must pass N1‴c with s_max covering [0, 6], or the cumulative criterion.**
  - **If it fails: verdict "nuisance unmeasured → INCONCLUSIVE".** No further rescue inside 081c.

## 6. Verdict rule (the Bridge's item 2)
- σ_W = |R48(8, box 8) − R24(8, box 4)|, exactly as defined in 081b. It enters in quadrature, **whatever its value.**
- R∞ and the routes are taken from EXP-081b's impact-rule numbers, unchanged. 081c replaces only σ_W, plus N4 below.
- Sign rule as in 081b: decided only if the 2σ interval of R∞ + 0.4503 excludes 0. T0 = T1 here (all W2/W4 reliable to
  s = 6); if W8 needs T1 and it is undefined, INCONCLUSIVE.
- **Continuum readiness (reported separately from the sign):** ρ = |R48(P8, box 8) / R24(P4, box 4) − 1|. This is the
  σ-side resolution shift at fixed physical geometry; the free-side reference is 0.47%.
  - **ρ > 0.10 (≥ 20× the free shift): "the (2, 4) pair is not continuum-ready"**, whatever σ_W does to the error bar.
    The lattice route then needs a refinement series, not more P.
  - 0.10 is about the shift that alone moves R by its current route σ (0.29 at R ≈ 2.5).
- **Decomposition (descriptive, reported):** R48(8, b8) − R24(8, b4) = [R48(8, b8) − R24(8, b8)] (resolution at fixed
  box) + [R24(8, b8) − R24(8, b4)] (box width). This uses the new W2P8 box 8.

## 7. N4 in 081c (the Bridge's item 5)
- **N4c:** s_cut 3.0 vs 3.5 at P = 6 (W = 2 and 4), with the census complete to 3.5 (checked).
  - Pass if |ΔR| ≤ 0.1 × σ_route (0.029).
  - **If it fails, add 2|ΔR| to σ in quadrature** (geometric-tail bound; observed ratio per 0.25 step ≈ 0.25–0.33).
- Expected from the diagnostic: |ΔR| ≈ 2·10⁻⁵. This is stated before 081c computes it, so it is a prediction.

**Every control and its consequence (no blank rows):**

| control | pass | consequence if it fails |
|---|---|---|
| Step 0 (refinement vs reference) | ≤ 10⁻¹² | STOP; fix the implementation |
| Positive control (W4P8 b8, W2P8 b4) | §4 tolerances | STOP; W8 not read |
| N1‴c on W8P8 | impact / cumulative ≤ 10⁻⁷ | nuisance unmeasured → INCONCLUSIVE |
| N1‴c must-fire (Woodbury) | must fire | the check is void → INCONCLUSIVE |
| t0 / residue checks | as §5 | nuisance unmeasured → INCONCLUSIVE |
| Census at s ≤ s_cut (all 081c geometries) | match | that geometry's R flagged; INCONCLUSIVE if it is W8P8 or W2P8 b8 |
| N4c | ≤ 0.1 σ_route | add 2\|ΔR\| in quadrature |
| ρ | ≤ 0.10 | label "not continuum-ready" (sign verdict still per §6) |

## 8. Resources (the Bridge's item 6)
- **Dry run** (dummy G, nothing physical computed): W8P8 needs 11,328 G per β node and 35,604 for the β = 0 term. One
  N = 384 inverse takes 5.3 ms and a refinement step ~3 ms, single thread. That is **≈ 1.6 h** for 53 nodes plus t0.
  Peak 0.33 GB measured, **declared 0.5 GB** (× 1.5).
- Positive controls: W4P8 box 8 ≈ 1.6 h (same size); W2P8 box 4 ≈ 0.5 h. W2P8 box 8 (Woodbury, as in 081b) ≈ 15 min.
- **Total ≈ 4 h, one core, < 1 GB: fits the daytime guards.** Run in the day, one job at a time, nice 12, watchdog cap
  1.5 GB.

## 9. Merge with the P = 16 night run? No.
- (4,8)@P8 box 8 is the **2× refinement of (2,4)@P4 box 4**: the same physical geometry at half the lattice spacing.
- (2,4)@P16 box 4 is a **larger box at the same lattice resolution** (36×32, N_y 64, 1152 sites vs 384).
- They are different computations testing different things: resolution versus volume.
- **Recommendation: hold the P = 16 night run.**
  - R(P) is already flat for P = 8–12 (2.644, 2.665, 2.646; impact rule), so volume is not the limiting uncertainty.
  - If ρ > 0.10, the next lattice run is a refinement series, e.g. (8,16)@P16 box 16 = 4× refined (2,4)@P4. That is 1536
    sites and (64, 1536, 1536) complex arrays at 2.4 GB each: night-scale. It would be registered separately.

## 10. Physical-meaning check (answered here, before computing)
- **Priors, read at source:**
  - δC_T/C_T = −40/(9π²) = −0.4503 (Petkou hep-th/9506116 eq. 30; report.md 2026-11-21).
  - δF = −ζ(3)/(8π²) ≈ −0.0152 = −0.238 F_s, with F_s = (1/16)(2 ln 2 − 3ζ(3)/π²) ≈ 0.0638.
    - Source: Klebanov, Pufu, Safdi, *F-Theorem without Supersymmetry*, arXiv:1105.4598, eqs. (71), (67), (41). Read via
      the ar5iv HTML by a fetch agent, 2026-11-22; not checked against the PDF.
    - The Bridge's −0.24 is confirmed.
- No O(N⁰) κ is in print (Whitsitt–Witczak-Krempa–Sachdev 1610.06568: κ_WF = Nκ_free at leading order only; report.md
  sweep).
- So R ≈ +2.4 is not excluded by anything known. It is large (> 2 free scalars) and of opposite sign to both known
  O(N⁰) corrections. Treat it as **suspect until the resolution test**.
- **Lattice terms that survive a (2, 4) difference**, and how 081c sees each:
  1. **A λ/W² term**, s(W) = e − κ/W + λ/W² + …. A pair (W₁, W₂) returns κ − λ(1/W₁ + 1/W₂): (2,4) → κ − 0.75λ,
     (4,8) → κ − 0.375λ.
     - On the free side, K's +1.9% excess (0.0404 vs 0.0396) is of this kind if λ_f ≈ −0.025 κ_f (argued). That fits the
       +0.47% refinement shift being small.
     - **σ-side: ρ measures it directly.** A σ excess of order R ≈ 2.4 from λ_σ would show as ρ ~ 0.5, not 0.005.
  2. **Amplification by the β = 0 cancellation.** t0 + T_sad is ~6% of either term (e.g. W4P6: −105.2 + 112.0). A 1%
     lattice artefact in either becomes ~16% in S.
     - 081c reports t0, T_sad and 𝒞 separately for every geometry, and the decomposition of ρ by component. So a
       resolution shift can be traced to the saddle/β = 0 sector or to 𝒞[g].
  3. **Box-width effects** (edges at different wall distances): the decomposition in §6 separates these.
- None of these is resolved here. The design can now see each one.

## 11. Order of work (after approval)
1. Step 0.
2. Positive controls (W2P8 b4, then W4P8 b8).
3. W2P8 b8 (Woodbury, 081b numerics; reliable for W = 2).
4. W8P8 b8 under the new numerics.
5. N4c.
6. Analysis by `exp081c_analyze.py`. It is committed before step 4 is read, with planted-value tests of the verdict logic.

Each step is committed and pushed as it lands; failures are kept.
