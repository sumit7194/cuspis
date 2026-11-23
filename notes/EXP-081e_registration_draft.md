# EXP-081e: the k = 3 refinement point with a structural pole selector (DRAFT v2 for the Bridge; not registered)

*Status: draft v2, 2026-11-23. Nothing here is registered until the Bridge's GO, and no production code is changed before that.
v1 (05e099c, blanket τ = 1e-4) was superseded by report c9c9660.
Pre-work: report bb09540 (item a), ddb277a (item c), c9c9660 (items 1–2), and the winding tests (`exp081d_results/e_winding_tests.txt`). [model: Opus 5.5]*

## 0. Why this exists
- 081d: PRIMARY INCONCLUSIVE, with k = 3 VOID (census row CEN flagged W12P12b12).
- 081d's registered output: R(k) = +2.255, +4.233, +6.442, +8.219 for k = 1, 1.5, 2, 2.5 (partially verified; zero TOUCH slices at every Stage-1 geometry).
- 081e is a new experiment that supplies the k = 3 point. It is not an amendment of 081d.

## 1. Defect (shown)
- In `Slice._poles` (sigma3d.py L60), the reciprocal filter `min|ev·z − 1| < 1e-6` (the partner's RELATIVE error) rejects 4 genuine poles at W12P12b12:
  - p = 7: s 2.4778963 and 2.4794482;
  - p = 10: s 2.9124682 and 2.9126315.
- Argument-principle count: 2 zeros at each pair.
- Partner mismatches scale as C·u/z. Genuine poles reach C = 3600, overlapping the range of rejected candidates (1.8e-3 to 1.2e4). No tolerance is principled.
- Inside the cut (s ≤ 3), the filter has never removed a spurious candidate at any of the 9 geometries.

## 2. The change (ONE variable: how candidates are selected)
- **Replace** the reciprocal filter, inside the cut, by **structural-zero deflation:**
  - Each slice's QEP has exactly n₀ = 2W − rank(A₀) structural zero eigenvalues.
  - Remove the n₀ eigenvalues of smallest modulus.
  - Keep the Im filter (unchanged; shown to change nothing) and 0 < z < 1, s ≤ s_cut.
- The merge rule (1e-7·z), the contour radii and the residues are unchanged.

**Gates in the patched `_poles`, logged per slice, every run:**

| gate | rule | must-fire plant |
|---|---|---|
| **ZC** (zero count) | #(\|ev\| < 1e-12) must equal n₀, with rank(A₀) from the SVD; print the singular-value gap σ_rank / σ_rank+1. Mismatch → STOP. | A₀ perturbed by a rank-1 term of size 1e-6·‖A₀‖ (the rank rises by 1, the count changes) must STOP |
| **GAP** | (smallest admissible z, = e^(−2π·s_cut) floor or the smallest kept z) / (largest structural \|ev\|) must be ≥ 1e3. Smaller → STOP. | a structural zero moved to \|ev\| = 1e-10 (gap below 1e3 at s_cut = 3) must STOP |

## 3. Arbiters, both independent of the eigensolver
**CEN′ (census, sign-change scan):** no resolved MISS at s ≤ 3, in either direction.
- MUST-REJECT plant: a resolved spurious real eigenvalue planted inside the cut (production list + 1 entry, F unchanged) must read "production has extra" (MISS).
- **Registered limit, not a pass:** the census is blind to splits below 1e-7 (item c). A spurious entry within 1e-7 of a genuine pole is not caught by CEN′. It is caught by WIND below.

**WIND (argument principle; Bridge suggestion):**
- Applies to every TOUCH slice, and to every production pole pair or merged entry with split < 1e-6.
- Zero count of F(s) = det(D + M·C(z)) inside each production residue contour, from the winding of arg F (`tools/winding.py`, adaptive steps |Δarg| < π/8).
- It must equal the number of production entries the contour stands for: 1 per entry, 2 for a merged pair. Raw winding must be within 0.05 of an integer.
- Cost: milliseconds per contour (measured).
- Plants, all measured PASS in pre-work:

  | plant | count |
  |---|---|
  | single | 1 |
  | exact double | 2 |
  | near-double at split 1e-8 | 2 |
  | tiny contour enclosing one of the pair | 1 |
  | near but not enclosing | 0 |
  | no pole | 0 |
  | triple | 3 |
  | known resolved real pair (W10 p = 19, split 8.9e-8) | 2 |
  | isolated real pole (W10 p = 8) | 1 |
  | offset contour (W10 p = 8) | 0 |

- Pre-work result on the 081d void geometry: at all 11 W12 TOUCH slices, every production contour encloses the right number of zeros (p = 14–16: 1 per entry; p = 17–24: 2 per merged entry). Those slices are verified.
- Assumption to test in the registered pre-check: production's α-plane contour (α = i·s) has the same radius as the s-plane circle used here.

## 4. Invariance (item b): nothing already measured may move
1. **Pole lists** (count and positions to 1e-12) at all 9 geometries must be IDENTICAL to the old production lists, EXCEPT exactly the 4 recovered W12 poles:
   - W3P6b6, W6P6b6, W2P8b8, W4P8b8, W8P8b8, W5P10b10, W10P10b10, W6P12b12, W12P12b12.
   - Any other change: every R that used that list is reopened, and STOP.
2. **Threshold-adjacent cases** must be in the list and unchanged: W12 p = 9 (old mismatch 5.8e-7) and W10P10b10 p = 8 (1.5e-7).
3. **Bitwise:** g at the hardest node (s = 5.972) at W10P10b10 and at W6P12b12, recomputed under the patch, must equal the stored values exactly (081d checkpoint; HELD route checkpoint).
   - Must-fire: the same comparison at W12P12b12 must show the list CHANGES (the 4 poles appear).
- If 1–3 pass, the Stage-1 R(k) and the HELD W6P12b12 route are valid under 081e's code and are reused. W6's R has not been read.

## 5. Production run
- Route W12P12b12 (patched), serial, then C1 W12. W6 comes from the HELD route if 4.3 passes; otherwise it is rerun.
- Memory: measured 7.32 GB per process.
- Wall time: ~29 h, argued from measured ratios; 3× check-in bound 90 h.
- Detached (PPID 1). The 081d gates carry over (Step 0 already PASS at both k = 3 geometries; planted ε_k, B2b, N1‴c, t0, residue, R1 cap, C1 verdict_stored).

## 6. Reading (unchanged from 081d; registered before R(3) is read)
- `decide_r`: r = [R(3) − R(1.5)] / [R(2) − R(1)], with the 081d bands, the ±2σ_r rule and T0/T1 agreement.
- Stated so nobody takes it for blinding: 081d's descriptive extrapolation puts R(3) at 9.2–9.9 (argued), between the upper gap and power-divergent.

## 7. Gate → runner mapping (one row per line; finalised before launch)
| row | runner check |
|---|---|
| ZC, GAP | inside patched `_poles` → raise → route exits non-zero → runner STOP |
| ZC / GAP must-fire | `exp081e_precheck.py` (plants) → exit 1 → STOP |
| invariance 4.1 / 4.2 | `exp081e_invariance.py` → exit 1 → STOP |
| bitwise 4.3 (+ must-fire) | `exp081e_bitwise.py` → exit 1 → STOP (or W6 rerun queued; decided at registration) |
| CEN′ + MUST-REJECT plant | `exp081e_census.py` → MISS or plant not firing → STOP |
| WIND + plants | `exp081e_wind.py` → any count mismatch or non-integer winding → STOP |
| route, C1 | as in 081d, detached, with the W12 guard removed only by the 081e runner |

## 8. Open for the Bridge
- Deflate exactly n₀ structural zeros (rank-based), or deflate by magnitude |ev| < 1e-12 with ZC as the cross-check? I propose rank-based, with magnitude as the gate.
- Should the reciprocal filter stay beyond the cut (s > 3, unused by production)? I propose leaving it untouched there, so nothing outside the change moves.
- W6 HELD reuse via 4.3: yes or no?
