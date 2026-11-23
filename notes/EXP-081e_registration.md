# EXP-081e REGISTRATION: the k = 3 refinement point with pencil-confirmed pole admission

*Registered 2026-11-23 under the Bridge's acceptance of v3 plus additions 1–2 (one-to-one matching; bidirectional pencil gate).
Supersedes the drafts `notes/EXP-081e_registration_draft.md` v1/v2 (kept). Pre-work: report bb09540, ddb277a, c9c9660, 174b06d, c234c89.
The Bridge's GO covers: pre-checks, then W12 production (detached, 3x bound 90 h, soft caps). [model: Opus 5.5]*

## A. Question and status
- 081d: PRIMARY INCONCLUSIVE, k = 3 VOID (CEN flagged W12P12b12). Its registered output is R(k) at k ≤ 2.5 (partially verified).
- 081e supplies R(3) with a corrected in-cut pole selection. It is a new experiment, not an amendment.

## B. Defect (shown)
- The reciprocal filter `min|ev·z − 1| < 1e-6` (`Slice._poles`, sigma3d.py L60) rejected 4 genuine in-cut poles at W12P12b12:
  - p = 7: s 2.4778963 and 2.4794482;
  - p = 10: s 2.9124682 and 2.9126315.
- Confirmed by census sign changes, by the linear pencil, and by winding counts (2 per pair).
- Inside the cut, the filter rejected nothing else at any of 9 geometries.

## C. The change (ONE variable: in-cut admission)
**Objects:**
- QEP candidates: production's eigenvalues, unchanged.
- Pencil roots: generalized eigenvalues of F(z) = det(L₀ + zL₁), with L₀ = D₀ + M·C̃₀ and L₁ = D₁ + M·C̃₁ (the census F written as a linear pencil). Real roots in (0, 1), Im filter 1e-8 relative.
- "In-cut" means s ≤ s_cut = 3.

**Procedure per slice, in this order, before the existing merge:**
1. **Match the kept candidates** (those passing the existing filters) to pencil roots, one-to-one, by nearest distance in s, within a window w = 1e-7.
2. **Admission:** a filter-REJECTED in-cut real candidate is admitted iff an UNMATCHED pencil root lies within w; that root is then consumed (one-to-one). Otherwise it stays rejected.
3. **Merge** with the existing 1e-7·z rule. Each entry's multiplicity m = the number of candidates merged into it.
4. **Contours, residues:** unchanged.
- Beyond the cut (s > 3), nothing changes.
- Positions always come from the QEP, so lists at geometries where step 2 never fires are bitwise unchanged.

## D. Gates (all logged per in-cut slice, every run)

| row | rule | on failure |
|---|---|---|
| **PB** (bidirectional pencil) | after steps 1–2, every in-cut entry has its own pencil partner within w, AND every in-cut pencil root (s ≤ 3 − w) has a QEP entry. Roots within w of the cut edge are logged only. | STOP |
| **WIND** | for every in-cut entry, the argument-principle zero count of F inside the entry's production contour (radius rad = min(1e-6, 0.3·spacing)) equals its multiplicity m, and raw winding is within 0.05 of an integer | STOP |
| **CEN′** | census (sign-change scan, s ≤ 3): no resolved MISS in either direction. TOUCH is not a pass; it is covered by WIND. **Registered limit:** spurious entries within 1e-7 of a genuine pole are invisible to CEN′ (they are caught by PB / WIND) | k void |
| **GAP** | logged only: (smallest in-cut z) / (largest \|ev\| < 1e-12). Not a gate (see I.4) | — |
| 081d rows | Step 0 (PASS at both k = 3 geometries), planted ε_k, B2b, N1‴c, t0, residue, R1 cap, C1 verdict_stored | as in 081d |

## E. Plants, each checked on paper (expected outcome derived before running)

| # | plant | paper check | expected |
|---|---|---|---|
| P1 | MUST-REJECT, pencil-unconfirmed. A decoupled 1×1 QEP block (not in F) with roots z_p = e^(−2π·2.0) and (1 + 1e-3)/z_p, added to slice W10P10b10 p = 8. No genuine pole lies within 1e-3 of s = 2.0 there (poles at 0.953, 2.8585, 2.8602 and beyond). | Its candidate's reciprocal mismatch is 1e-3 ≥ 1e-6, so the filter rejects it. The pencil (from the unmodified slice) has no root within 1e-7 of s = 2.0, so it is not admitted. | rejected; list unchanged |
| P1b | MUST-STOP, spurious that passes the filter. The same block with an exact reciprocal partner (offset 0). | The filter keeps it. In step 1 no pencil root lies within w, so PB finds an entry without a partner. | **STOP (PB)** |
| P2 | MUST-REJECT, rider. A decoupled block with root at s_g + 1e-8, where s_g = 2.858532… is the kept genuine pole (W10 p = 8), partner mismatch 1e-3. | The filter rejects it. Step 1 already matched the genuine kept candidate (pencil offset ≤ 1e-9) to the pencil root at s_g. No unmatched root lies within w, so it is not admitted. If admission were (wrongly) allowed, the merge (Δz/z = 2π·1e-8 = 6.3e-8 < 1e-7) would give m = 2, while WIND at that contour gives 1, so it would STOP. | rejected |
| P3 | MUST-STOP, deleted genuine. Remove the genuine candidate at s = 2.858532 (W10 p = 8) from the QEP candidates. | The pencil root at 2.858532 has no QEP entry, so PB fires. | **STOP (PB)** |
| P4 | MUST-FIRE, admission. W12P12b12 unmodified. | The 4 rejected in-cut candidates each lie ≤ 1e-9 from a distinct unmatched pencil root (measured, c234c89), so all 4 are admitted. Entries: separate (splits 1.6e-3 and 1.6e-4 ≫ merge), m = 1 each. WIND at radius 0.3·spacing gives 1 each. | +4 entries; PB and WIND pass |
| P5 | MUST-FIRE, WIND radius. W12P12b12 p = 14, entries 1.1214539263 / 1.1214539822 (split 5.6e-8), production rad 1.7e-8 → count 1 each. Wrong radius 1e-7 > split. | The contour now encloses both zeros, so the count is 2 ≠ m = 1. | **STOP (WIND)** |
| P5b | α-plane equivalence. Evaluate F on production's own contour points α₀ + rad·e^(iθ) with s = −iα. | The map is an isometry (a rotation), so the counts are identical to the s-plane circle. | identical counts at all in-cut entries |
| P6 | MUST-FIRE, CEN′. Add a resolved spurious entry at s = 2.0 to the production list of W10 p = 8 (F unchanged). | The census's own list lacks 2.0 and production has it, so the counts differ. | **MISS** |
| P7 | Invariance must-fire. Old versus patched lists at W12P12b12. | The 4 poles appear. | lists DIFFER |

## F. Invariance (before any R is read)
1. Patched pole lists at W3P6b6, W6P6b6, W2P8b8, W4P8b8, W8P8b8, W5P10b10, W10P10b10 and W6P12b12 are **bitwise identical** to the unpatched ones. At W12P12b12 they are identical except exactly the 4 admitted poles (P7).
2. The threshold-adjacent cases are present and unchanged: W12 p = 9 (old mismatch 5.8e-7) and W10 p = 8 (1.5e-7).
3. Bitwise g at the hardest node (s = 5.972) recomputed with patched code: W10P10b10 against the 081d checkpoint, and W6P12b12 against the HELD route checkpoint.
- If 1–3 pass, the Stage-1 R(k) and the HELD W6P12b12 route are reused under 081e (Bridge: yes). Otherwise STOP for a ruling.

## G. Production
- Route W12P12b12 (patched), serial, detached (PPID 1), then C1 W12.
- Caps: soft 8 GB, hard 11 GB (measured peak 7.32 GB), pressure-stop on.
- Wall time: ~29 h, argued from measured ratios; check-in bound 90 h.
- The 081d W12 guard (`tools/guard_081d_w12.sh`) stays armed on the 081d runner. 081e uses its own runner and tags.

## H. Reading (unchanged from 081d; fixed before R(3) is read)
- PRIMARY via `decide_r`: r = [R(3) − R(1.5)] / [R(2) − R(1)], per tail.
- Bands: converging ≤ 0.75; log-like or slow power 0.87–1.15; power-divergent ≥ 1.33; gaps INCONCLUSIVE.
- ±2σ_r rule; T0/T1 agreement.
- Known beforehand, stated so nobody mistakes it for blinding: 081d's descriptive extrapolation puts R(3) at 9.2–9.9 (argued).

## I. Gate → runner mapping (one row per line)
| row | runner check |
|---|---|
| PB, WIND (production) | raised inside patched `_poles` → route exits non-zero → runner prints FAILED and stops (`set -e` semantics in the 081e runner) |
| P1–P7 plants | `exp081e_precheck.py`: each plant's observed outcome is compared with column E's expected outcome; any disagreement → exit 1 → runner stops before production |
| F.1 / F.2 invariance | `exp081e_invariance.py` → exit 1 → stop |
| F.3 bitwise | `exp081e_bitwise.py` → exit 1 → stop (W6 reuse forfeited, Bridge ruling needed) |
| CEN′ | `exp081d_census.py 12:12:12` (patched lists) → parsed; MISS → stop |
| route, C1, Step 0 rows | as in 081d; Step 0 already PASS (logs kept) |

**I.4 (why GAP is logged, not gated):** paper check of the v2 GAP plant (a structural zero at 1e-10):
- It is not in the set GAP measures (|ev| < 1e-12), so it cannot fire.
- Widening the set to "below the cut floor" fails on real data: genuine poles just beyond the cut (W12 p = 11, s = 3.039, z = 5.1e-9) sit against the smallest kept z of 7.3e-9.
- v3 does not rely on magnitude separation (the pencil votes), so GAP carries no decision.
