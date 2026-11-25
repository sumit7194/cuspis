# Post-seal addendum, 2026-11-25 ~17:40 IST (branch fable/2026-11-25-t0L-largek) [model: Fable 5.2]
**Everything here is UNVERIFIED until the office sister checks it.** Written AFTER the sealed prediction in `HANDOVER.md` §3 (commit 6156a51),
which is left exactly as it was. Written BEFORE the k = 3 office run lands (~05:00 on 2026-11-26).

**Exposure since the seal.** I opened no k = 3 result file. I saw the subject lines of main commits 08e7ab9, 27aea6f, 50555f4 (office sister:
defect reproduced on tiny boxes, EXP-087 registered). They carry no k = 3 value of R or of X_Lam. Still known to me from before: t0(W12) = -486.137451.

## A. Short version
1. The dropped-residue case ("mechanism B") is now tested on a tiny W = 10 box and matches the code-logic prediction.
2. The code-logic prediction of the t0 error at production size is: W8P8 **-0.0201**, W10P10 **-0.1218**, W12P12 **-0.0575** (code minus true); zero for
   every narrow strip (W6P6, W4P8, W5P10, W6P12).
3. With these removed, R(t0+L) is smooth and slowing: **0.7615, 0.5381, 0.4283, 0.3709** (k = 1, 1.5, 2, 2.5). No acceleration is left.
4. **My sealed number (-1.55) is now expected to FAIL.** Reason in §D. Revised expectation for the current code at k = 3: **R(t0+L)(3) = -0.07**.

## B. Mechanism B, tested (tiny box W10 P3 Wb10 Ny16, N = 96; production path)  — grade: verified by evaluation on one tiny box, one implementation
Doublet gaps in this box: 8.4e-8, 1.1e-7, 2.1e-7, 6.4e-7, 3.2e-6, 2.5e-5. Files: `rad_test_W10P3_output.txt`, `rad_test_W10P3_big_rad_output.txt`,
`artifact_W10P3_output.txt`.

| rad | engine t0 | measured shift vs rad 3e-8 | predicted by `artifact.py` (A + B) |
|---|---|---|---|
| 1e-4 | -35.980809926 | -0.156661 | -0.156740 (A -0.201953, B +0.045213) |
| 3e-5 | -36.041290698 | -0.217142 | -0.216114 |
| 1e-5 | -35.925582712 | -0.101434 | -0.101513 (A -0.085992, B -0.015521) |
| 1e-6 | -35.861740507 | -0.037592 | -0.037670 |
| 1e-7 | -35.963990005 | (bad, see below) | -0.001337 |
| 3e-8 | -35.824148449 | reference | 0 |
| 1e-8 | -35.822319422 | +0.001829 | 0 |

- Agreement 8e-5 to 1e-3 over a shift that changes by a factor 6 and whose B part changes sign. The reference itself is only good to ~2e-3
  (rad 3e-8 and 1e-8 differ by 1.8e-3: precision loss at tiny radius).
- **rad = 1e-7 is NOT explained by A + B.** It is off by -0.14. Cause (argued, not isolated): a pole sits just outside a contour and the 32-point
  quadrature leaks. So there is a third failure mode, and **no single radius is safe for W >= 10**: too big double-counts, medium drops a member,
  small leaks or loses digits. The fix needs one contour per pole cluster (which is what EXP-087 drafts).
- What would have made this check fail: a predicted shift of the wrong sign or size at any of the four radii. The B sign flip between 1e-4 and 1e-5
  was not tuned; it comes out of the merge rule.

## C. Production sizes, default rad = 1e-5 (`artifact_production_output.txt`)  — grade: inference (code logic, tested only at N = 84 and 96)
| geometry | predicted t0_code - t0_true | parts |
|---|---|---|
| W6P6, W4P8, W5P10, W6P12 | 0 | no doublet below 1e-4 |
| W8P8 | -0.020126 | A only (slices u = 11..16) |
| W10P10 | -0.121770 | A -0.085737 (u = 9..17), B -0.036033 (u = 18, 19, 20) |
| W12P12 | -0.057468 | A -0.193760 (u = 8..13), B +0.136292 (u = 14, 15, 16) |

Premise I am keeping: `artifact.py` assumes each contour returns exactly the residues inside it (no quadrature leak). That held at rad 1e-5 on the
tiny W10 box (8e-5), and failed at rad 1e-7. If a production pole sits within ~1.1 rad outside a contour, these numbers are off.

## D. Corrected series (`corrected_series_output.txt`; stored values, minus half the predicted t0 error on the wide strip)  — grade: inference
| k | 1 | 1.5 | 2 | 2.5 |
|---|---|---|---|---|
| R(t0+L), stored | 0.7615 | 0.5381 | 0.2865 | -0.5005 |
| R(t0+L), corrected | 0.7615 | 0.5381 | 0.4283 | 0.3709 |
| R, stored | 2.2552 | 4.2334 | 6.4420 | 8.2187 |
| R, corrected | 2.2552 | 4.2334 | 6.5838 | 9.0901 |
| Y_A (unchanged) | 1.9817 | 3.8641 | 6.1049 | 8.5280 |
| R - Y_A, stored | 0.2735 | 0.3693 | 0.3371 | -0.3092 |
| R - Y_A, corrected | 0.2735 | 0.3693 | 0.4789 | 0.5621 |

- Increments of corrected R(t0+L): -0.223, -0.110, -0.057: halving each step. Local slopes of corrected R: 3.96, 4.70, 5.01, next to Y_A's
  3.77, 4.48, 4.85. Stored R had 3.96, 4.42, 3.55.
- Smoothness control on the wide series E_w (P = 3, 4, 5, 6, 8, 10): a·P + b + A·ln P fits the stored values to rms 7.4e-3 and the corrected values
  to rms 7.5e-4 (10x better). From P = 4, 5, 6 alone the form misses P = 8, 10 by -0.012, -0.067 (stored) and -0.002, -0.006 (corrected).
  This check could have failed: a wrong-size correction leaves a kink. A small one is left at P = 10 (-0.006), so the W10P10 number may be ~10% short.
- 2-dof slope of R - Y_A: stored -0.356 (rho_s -0.089), corrected **+0.195 (rho_s +0.049)**. To be re-read against 085/085c's registered
  thresholds by the office sister; I have not re-read them here.
- So for question (2): after the correction I see nothing in t0 + L that T54's accounting misses. t0 + L tends to a constant near 0.3, as the
  power counting in `HANDOVER.md` §2 said. What remains between bulk c and the box-consistent c_A is a finite-box term (hypothesis; not tested here).
  EXP-086's n = 2 reading does not use this routine at n = 1 in the same way; I have NOT checked whether it is touched.

## E. Why the sealed number is expected to miss, and the revised prediction
The seal continued the growing anomaly (-0.012 at P = 8, -0.06 at P = 10) to P = 12. That was the mistake: I had mechanism B only as an untested
argument and did not put a number on it. At W = 12 most doublets are closer than 1e-7, so they flip from "counted twice" (negative) to "one member
dropped" (positive here), and the two parts mostly cancel: -0.194 + 0.136 = -0.057. The error at W12P12 is SMALLER than at W10P10.

**Revised prediction, k = 3 (W1 = 6, W2 = 12, P = 12), registered here before the run lands:**
- Current code (rad 1e-5): **R(t0+L)(3) = -0.07; 68% band [-0.30, +0.15]; outer band [-0.60, +0.40].**
  S units: E(W6P12) = 1.895 +- 0.006; E(W12P12) = 1.890 +- 0.02; given t0(W12) = -486.137451 this means X_Lam(W12P12) = 244.958 +- 0.02.
- After a correct t0 (cluster contours): t0(W12P12) rises by +0.057 (+-0.03); **R(t0+L)(3) = +0.33, band [0.25, 0.42].**
  Likewise t0(W8P8) rises by +0.0201 and t0(W10P10) by +0.122 (the P = 10 kink suggests up to +0.135).
- Where the width comes from: the W12 error is a difference of two parts (+-10% each gives +-0.17 in R); the true E_w(12) is an extrapolation
  (geometric continuation of the increments gives -0.0236 for E_n - E_w; the six-point log fit gives -0.0256).
- **Fails if** R(t0+L)(3) from the current code is outside [-0.60, +0.40]; or the corrected value is outside [0.15, 0.50]; or corrected R(t0+L)
  at k = 2, 2.5 is not within 0.03 of 0.428, 0.371.
- Scoring: the sealed -1.55 stands as my registered prediction. If the run lands near -0.07 the seal FAILED and this addendum is the reason, kept on file.

## F. For the office sister
1. t0 with cluster contours at W8P8, W10P10, W12P12: expect +0.0201, +0.1218 (to +0.135), +0.0575 (+-0.03). Narrow strips must not move.
2. Check for a pole just outside any contour at production size (the rad = 1e-7 failure above); `artifact.py` cannot see it.
3. Recompute R(2), R(2.5), R(3) and re-read the 085/085c slopes. Expect R - Y_A = 0.479, 0.562 at k = 2, 2.5.
4. Whether inner_beta0 at n = 2 (route ii, EXP-086) is touched: not checked by me.
