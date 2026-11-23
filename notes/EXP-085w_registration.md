# EXP-085w (side job, registered before running): why does test (i) fire at W4P4? [model: Opus 5.5]

*2026-11-23, after EXP-085 closed INCONCLUSIVE (3e8e610), at the Bridge's request. Side job beside part 8: measured < 0.5 GB, nice 12, one at a time.*

## Why it matters
- W4P4 now carries three anomalies:
  - the C2 exactness residual, 4.4–5.4e-10;
  - 084c Level 1, 5.4e-10;
  - 085 test (i), 5.8e-9 / 3.4e-9 against ≈ 7e-12.
- W4P4 is a k = 1 geometry in the 084c core set.
- Every W₂ = 4k geometry has the cut filling the box (W = Wbox = P): W4P4, W6P6, W8P8, W10P10.
- A pipeline defect there would reach 084c, and 081e's routes, which stay on HOLD until this is explained or bounded.

## Geometry fact (answers the Bridge's W = P question; from `Geom` / `build`)
- Lx = 2P + Wbox, Lt = 2P, Ny = 4P, Wbox = P. W is the cut width inside the box.
- W2P4 and W4P4 sit on the identical 12 × 8 × 16 lattice and differ ONLY in cut width (2 vs 4).
- "W = P" means the cut fills the box. It is not a square aspect ratio; both cuts are centred and mirror-symmetric.

## Primary hypothesis H1 (stated before any computation): s_cut truncation
- d^B (production `coincident_dn_c`) sums pole residues for s_j ≤ s_cut = 3 only.
- d^C = C_line[(1/Ny)Σ_p diag(G_p(β) − G0_p)] integrates the full line to s = 6. Its weight π/cosh²(πs) ≈ 8e-8 at s = 3, so it includes every pole.
- The residue weight is |_kdn(is)| ≈ 2πs·e^(−2πs) ≈ 1.2e-7 at s = 3. A slice pole just above s_cut therefore gives d^C − d^B of order 1e-9 to 1e-8: the observed order.
- `Slice._poles` stores ALL poles in (0, 1) in z, including s_j > s_cut, so the tail is computed exactly:
  - d^B_tail = (1/Ny) Σ_p Σ_{s_j > s_cut} (same residue formula as `coincident_dn_c`).

## Measurements (W2P4, W4P4; then W3P6, W6P6 if memory allows)
- **KA:** the recomputed (i-G) and (i-B) reproduce D.json bitwise: W2P4 iG = 1.543869199421358e-13; W4P4 iG = 5.7846216892053215e-09.
- **H1 test:** max|(d^C − d^B) − d^B_tail| ≤ 10 × (s_dB + s_dC), and the same for (i-B) with Ġ^A. Run at each geometry.
- **H1 must-fail:** with the tail's sign flipped, (d^C − d^B) + d^B_tail must FAIL at W4P4. This is graded only if |tail| > 20× tol there; otherwise reported as "H1 has no teeth at W4P4".
- **Plant (c), Bridge:** add 5e-9 to d^B at one site (the site of W4P4's max mismatch, mapped to W2P4's lattice) at W2P4. (i-G) must FAIL there.
- **Descriptive, Bridge (a)/(b):**
  - the x-locations (x, t) of the top-5 |d^C − d^B| entries;
  - the per-slice p share of the mismatch;
  - per p: poles with 3 < s < 4, the minimum pole gap, and the minimum |s_j − s_cut|;
  - cond(B₁[0]) at each geometry.

## Reading
| outcome | condition | meaning |
|---|---|---|
| **H1 explains** | H1 test PASS at W2P4 and W4P4, and the must-fail fires | the (i) mismatch is the registered s_cut = 3 truncation, which test (i) compared against an untruncated d^C: a test-design defect, not a pipeline defect. The production impact is bounded by |tail|/|d| (argued bound in R units, reported) |
| **H1 fails** | H1 test FAIL at W4P4 | the cause is not the tail. Report the (a)/(b) localisation; W4P4 stays unexplained, bounded only by size |
| no teeth | the tail at W4P4 is below 20× tol | H1 can't explain a 5.8e-9 mismatch; same as H1 fails |

## Conditional step 2 (only if H1 explains; registered now, run on the Bridge's go)
- **Does the same truncation explain C2 / 084c Level 1 at W4P4?** One variable: s_cut 3.0 → 6.0 in route (ii) (Gap and strip_sigma), at W4P4 n = 2, ≈ 18 min.
- **Prediction:** Level 1 dev drops ≤ tol (3.1e-10). If not, the C2 / Level-1 residual has a different cause.

## Pre-run note (Bridge, 2026-11-23; nothing run or read: the first launch was stopped in the pressure gate, so no output exists)
1. **Tail definition:** tail := poles with 3 < s_j ≤ 6, matching d^C's integration range (C_line to s = 6). The s > 6 remainder is reported separately as a size and is expected to be negligible. The H1 test and must-fail use the (3, 6] tail; "teeth" means |tail(3,6]| > 20× tol.
2. **Family prediction (stated now):** W2P4 (same lattice, W < Wbox) has |tail(3,6]| ≤ its tolG, consistent with its passing test (i). If W2P4's tail is > tolG while (i) passed there, H1 is wrong, or incomplete, as the cause, whatever happens at W4P4.
3. **Step 2 conditional go (Bridge):** step 2 (s_cut 3 → 6 in route (ii), W4P4 n = 2) runs without waiting for the Bridge if and only if, at W4P4, the H1 test PASSES, the must-fail FIRES and |tail| > 20× tol. It also needs the family prediction to hold at W2P4. Otherwise: stop and report.
4. **If H1 holds:**
   - The 084c READ headline states s_cut = 3, and per geometry the computed tail against the Level-1 tolerance margin.
   - Before any route gets a go, a registered change moves production d to s_cut ≥ 6 (or a tail-corrected sum), with a KA that d is unchanged where the tail ≤ tol.
