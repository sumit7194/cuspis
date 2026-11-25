# EXP-087 (DRAFT for the Bridge; nothing recomputed): fix of `sigma3d.inner_beta0` for near-degenerate intra-slice pole doublets [model: Opus 5.5]

*Lead from the Fable side session (branch fable/2026-11-25-t0L-largek, 6156a51; UNVERIFIED there). Verified here on 2026-11-25 by reading the code
and by tiny-box measurements (scratchpad `fable_check/`; results below). Production-bug status: **verified on tiny boxes; not yet measured at a
production geometry**.*

## A. The defect (verified by code reading and measurement)
- `inner_beta0` builds contour locations for each slice pair (p, q = k − p). Locations within 1e-2·rad merge; each merged location gets ONE
  contour of radius rad = 1e-5 (two-tag branch) or ONE nearest residue (single-tag branch).
- Mechanism A (1e-2·rad ≤ g < rad): a doublet (s₁, s₂) of the same slice, gap g. When q ∈ {p, Ny − p} each member has its own two-tag entry, and each
  radius-rad contour encloses BOTH members, so **the doublet is counted twice**.
- Mechanism B (g < 1e-2·rad): the members merge into one entry, so the single-tag branch uses only the `argmin`-nearest residue and **the other
  member is dropped**.
- Doublets with g < 1e-4 occur for W ≥ 7 (W8: 3.0e-6 … ; W10: down to 8.5e-8; W12: down to 1.8e-8); none for W ≤ 6.

## B. Evidence (this session; tiny boxes, production path)
| check | result |
|---|---|
| (a) W8P3 Ny16, rad 1e-5 / 1e-6 / 3e-7 | t0 −35.787540656 / −35.769863760 / −35.769860344; shift −0.017677 (k = 0, ±2, ±4 only): reproduced exactly |
| control W6P3 Ny16 (no doublets < 1e-4) | rad 1e-5 → 1e-6 moves t0 by 2.4e-7 only (against 1.8e-2 at W8) |
| artifact.py (code-logic prediction) at W8P3 | −0.017677 (mechanism A only), matching the measured shift |
| (d) W10P3 Ny16 (one B doublet, gap 8.4e-8), rad 1e-5 → 3e-8 | measured shift −0.101434; predicted −0.101513 (A −0.085992 + B −0.015521): agreement 8e-5; A alone would miss by 0.0155, so **B is confirmed** |
| radius floor | rad 1e-8 differs from 3e-8 by a further 1.8e-3 (convergence check of 5e-8 / 2e-8 pending): very small contours are NOT numerically safe |
| (b) predictions at production geometries (code logic) | Δt0 = code − true: W8P8 −0.0201 (A); W10P10 −0.1218 (A −0.0857, B −0.0360); W12P12 −0.0575 (A −0.194, B +0.136) |

## C. Fix (registered design; one variable: the contour bookkeeping for intra-slice clusters)
- **Cluster** the in-cut poles of each slice by single linkage at gap < rad (rad = 1e-5 unchanged). Singletons keep the current code path
  **bit for bit**.
- For a cluster with ≥ 2 members:
  - **two-tag branch:** ONE contour around the cluster centre with radius 0.5·span + rad (encloses every member once; no tiny radii);
  - **single-tag branch:** the SUM of all members' residues (not the nearest one).
- Merge tolerance for a/b tags of the same pole stays 1e-2·rad (QEP pole accuracy ~1e-9, per the EXP-081b comment).

## D. KAs and plants (each can fail)
1. **Bitwise invariance where there are no clusters:** W2P4, W3P6, W4P4, W4P8, W5P10, W6P6 (and tiny W6P3): t0 with the fix == stored/production bitwise.
2. **Known answers on tiny boxes:** W8P3: fixed t0 == −35.769860 (rad-sweep converged) to 1e-5. W10P3: fixed t0 == the converged rad-sweep value (3e-8 → −35.824148 if the pending convergence check confirms it) to 1e-4.
3. **Code-logic agreement:** the fixed − unfixed difference equals artifact.py's predicted −Δt0 to 1e-4 relative at W8P3, W10P3 (tiny), then at W8P8.
4. **Must-fail plant:** with the fix disabled by a flag, W8P8 reproduces the stored −209.300109928361 bitwise (the Bridge's KA), and W8P3 reproduces −35.787540656.
5. Behind an env flag, default OFF until the KAs pass; production values are recomputed only after that.

## E. Recompute and cost (after the KAs; one core each, sequential; fleet ≤ 8)
- t0 only (install + t0; the other components are unaffected: T_sad and 𝒞 do not use inner_beta0):
  - W8P8 ~20 min, 0.73 GB;
  - W10P10 ~1.6 h, ~3.2 GB;
  - W12P12 ~2.8 h, ~5–6.5 GB (after the running route ends).
- R(2), R(2.5), R(3) are then zero-compute (stored components + corrected t0).
  - Predicted (inference): +0.142, +0.871, ~+0.41.
- Downstream to re-read (each a NEW registration, no silent edits): 081d's R(k) and g_raw; 085/085c slope readings; the ingredient check.
- **EXP-086 is immune** (honest exact-n family; no inner_beta0). The honest R₂ and its overshoot stand, and that tension must be stated in every re-read.
