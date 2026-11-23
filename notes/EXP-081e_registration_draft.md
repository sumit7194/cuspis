# EXP-081e: k = 3 refinement point with the QEP reciprocal-pairing fix (DRAFT for the Bridge; not registered)

*Status: draft, 2026-11-23. Nothing here is registered until the Bridge's GO, and no production code is changed before that.
Pre-work: report.md entries bb09540 (item a), ddb277a (item c), d2702e5/8b4e9e7 (the 081d void). [model: Opus 5.5]*

## 0. Why this exists
- 081d ended with PRIMARY INCONCLUSIVE: k = 3 was VOID because census row CEN flagged W12P12b12.
- 081d's registered output is R(k) = +2.255, +4.233, +6.442, +8.219 for k = 1, 1.5, 2, 2.5 (partially verified).
- 081e asks the same question with the k = 3 point that 081d could not supply. It is a new experiment, not an amendment of 081d.

## 1. Defects being fixed (shown in pre-work)
**D1.** In `Slice._poles` (sigma3d.py L60), the reciprocal-pairing tolerance `min|ev·z − 1| < 1e-6` rejects 4 real poles at W12P12b12 (p = 7: s 2.4778963 / 2.4794482; p = 10: s 2.9124682 / 2.9126315).
- Their reciprocal mismatches are 3.4e-6 to 4.7e-6.
- The Im filter is not involved: loosening it changes nothing at any of 9 geometries.

## 2. The change (ONE variable)
`1e-6` → **τ = 1e-4** in the reciprocal filter. Nothing else changes.
- Why 1e-4:
  - The largest mismatch of any real candidate with s ≤ 3 over all 9 geometries is 4.7e-6, so τ sits more than 20× above everything observed.
  - At 1e-4, no candidate is newly admitted beyond the 4 missing poles.
- **Margin rule (new runtime check, logged per slice):** record the largest mismatch admitted and the smallest rejected.
  - If any real candidate has a mismatch in [τ/20, τ], the slice is flagged (near-threshold), and k is unverified until a finer check.
  - Must-fire: a planted candidate at mismatch 2τ must be rejected, and at τ/2 must be admitted and flagged.

## 3. Invariance gate (item b): nothing already measured may move
Before any R is read, with the fix in place:
1. The pole lists (count and positions to 1e-12) at all 8 previously used geometries must be IDENTICAL to production's old lists: W3P6b6, W6P6b6, W2P8b8, W4P8b8, W8P8b8, W5P10b10, W10P10b10, W6P12b12.
   - Preview (pre-work a): identical at all 8.
   - If any list changes, every R that used it is reopened, and 081e stops for a ruling.
2. Bitwise check: one g node (hardest, s = 5.972) at k = 2.5 W10P10b10 and at k = 3 W6P12b12, recomputed with the fix, must equal the stored values exactly (k = 2.5: 081d checkpoint; W6: the HELD route checkpoint).
3. Must-fire: the same comparison at W12P12b12 p = 7 must show the pole list CHANGES (the 4 poles appear).
- If 1 and 2 pass, the Stage-1 R(k) values and the HELD W6P12b12 route are valid under 081e's code, and are reused without rerunning.
- The HELD W6 route then enters 081e as its W6 arm. Its R has not been read.

## 4. Census gate, with its limit stated (item c)
- **CEN′:** the census at W12P12b12 under the fix must give no resolved MISS at s ≤ 3.
- A TOUCH is **unverified**, not a pass: item c showed the census is blind to splits below 1e-7.
- **TCH (new):** every TOUCH slice (W12 p = 14–24) gets a finer independent check:
  - a local sign scan of F(s) at step 1e-10 over ±1e-6 around the touch, F evaluated in mpmath at 40 digits;
  - it must find the production pair (or, for a merged single, a pair whose split is < the production contour radius, so one contour covers both).
- Must-fire for TCH, planted with a synthetic F placed OFF both scan grids:
  - split 1e-8 with production lacking it → FAIL;
  - split 1e-8 with production having it → PASS;
  - controls as in item c.
- Fail: k = 3 void (as in 081d).

## 5. Production run
Route W12P12b12 with the fix, serial, then C1 W12. W6 comes from the HELD route if gate 3.2 passes; otherwise it is rerun with the fix.
- Memory: measured 7.32 GB per process. Serial only.
- Wall time: ~29 h, argued from measured ratios (3x check-in bound: 90 h). Detached (PPID 1).
- All other gates as registered in 081d (Step 0 already PASS at both k = 3 geometries; planted ε_k, B2b, N1‴c, t0, residue, R1 cap, C1 verdict_stored).

## 6. Reading (unchanged from 081d; registered before R(3) is read)
- PRIMARY via `decide_r`: r = [R(3) − R(1.5)] / [R(2) − R(1)], with the same bands (converging ≤ 0.75; log-like or slow power 0.87–1.15; power-divergent ≥ 1.33; gaps INCONCLUSIVE; ±2σ_r rule; T0/T1 agreement).
- Stage-1 R(k) are reused per gate 3.
- Known before reading, stated so nobody mistakes it for blinding: 081d's descriptive extrapolation predicts R(3) of 9.2–9.9 (argued). That spans the upper gap and power-divergent.

## 7. Gate → runner mapping (rule of 2026-11-23; filled in before launch)
| row | runner check |
|---|---|
| D1 invariance (3.1) | `exp081e_invariance.py` → exit 1 stops the runner |
| bitwise (3.2) | `exp081e_bitwise.py` → exit 1 stops the runner, or W6 rerun queued |
| must-fire (3.3) | inside `exp081e_invariance.py`; no fire → exit 1 |
| margin (2) | logged by the patched `_poles`; any flag → STOP before the route |
| CEN′ | `exp081d_census.py 12:12:12` result parsed → MISS stops the runner |
| TCH | `exp081e_touch.py` → FAIL stops the runner |
| route, C1, Step 0 | as in 081d (`run_081d_stage2.sh` pattern) |

## 8. Open for the Bridge
- τ = 1e-4 against a conditioning-scaled tolerance. I chose the single constant (one variable), because the margin rule catches near-threshold cases.
- Should the W6 HELD route be reused (gate 3.2) or rerun?
- The Hawking-Page lesson (Bridge, §9.4): the filter tests in §2 and §3 include the threshold-adjacent cases W12 p = 9 (5.8e-7) and W10 p = 8 (1.5e-7).
