# Fable side-session handover, 2026-11-25 (branch fable/2026-11-25-t0L-largek) [model: Fable 5.2]
**Everything here is UNVERIFIED until the office sister checks it.** Stopped early: usage limit reached. Scripts and outputs are in this folder.

## 1. Main finding: a defect in t0 (`sigma3d.inner_beta0`) for cut width W >= 8  (verified by evaluation on a tiny box; one implementation)
- For W >= 7 the high-mass y-slices carry near-degenerate pole DOUBLETS of the same slice. Smallest gap in s (`intra_gaps_output.txt`):
  W6 1.0e-4, W7 1.8e-5, W8 3.0e-6, W9 5.1e-7, W10 8.5e-8, W12 1.8e-8. Narrow strips up to W = 6 have none below 1e-4.
- `inner_beta0` two-tag branch (partner slice q = p or Ny-p, i.e. k = 2p, -2p, 0) integrates on a contour of radius rad = 1e-5 around
  EACH entry. If the doublet gap g is in (1e-7, 1e-5), each contour encloses both members and both have entries: the doublet is counted TWICE.
- If g < 1e-7 (= 1e-2*rad) the two members merge into one entry and the single-tag branch uses only the nearest residue: one member is DROPPED
  for every other q. (Argued from the code; NOT tested: needs W >= 10.)
- **Test (production path: Strip3D + exp081c_numerics.install + inner_beta0(dn=True)), box W8 P3 Wb8 Ny16, N = 84** (`rad_test_W8P3_output.txt`):
  t0 = -35.787540656 (rad 1e-5, default); -35.769863760 (rad 1e-6); -35.769860344 (rad 3e-7). Shift -0.017677, only in k = 0, +-2, +-4.
- **Prediction from the code logic alone** (`artifact.py`, no t0 run): -0.017677 (slices u = 6, 7, 8). Matches the measured shift to 1e-7.
- Affected stored values: t0 of W8P8 (k = 2), W10P10 (k = 2.5), W12P12 (k = 3); via S_W2 this lowers R(2), R(2.5), R(3) (dR = +7 * dt0, dt0 < 0).
  Also inner_beta0(n = 2) in route (ii): weight e^(-4 pi s), consistent with 084c's degraded W8P8 precision (dev_a ~ 2e-6) (hypothesis).
- NOT done (limit): `artifact.py 8 8 8 32`, `10 10 10 40`, `12 12 12 48` to get dt0 at the production geometries (minutes each, < 1 GB).

## 2. Where the "accelerating" t0 + L comes from
- E(W,P) := 1/2 t0 - 2 Ny Sum Lambda d (S units); R(t0+L) = -(E_narrow - E_wide) * norm.
- Narrow series is smooth: E_n = 0.118 P - 0.312 + 0.316 ln P fits P = 4, 6, 8, 10 to 3e-4.
- Wide series (W = P), with my own points at P = 3, 5: every smooth form fitted without P = 10 over-predicts E_w(10) by 0.016-0.044, and
  E_w(8) is ~0.012 low against the log form from P = 4, 5, 6. Sign and onset (none at P <= 6) match the defect above. Size not yet computed.
- Analysis (argued): E = Sum B^-1(x,y) K'(x,y), K' = 1/2 d_n B^(0) - 2 G d. The k^2 pieces cancel identically. K'(x,x) is small, positive, smooth
  (9e-4 next to a branch point). E = T_rho + T_grad, T_rho = Ny Sum rho K'(x,x), rho = B_0^-1 1 (the same zero mode as Sum sigdot = 2 Ny Sum rho d).
  T_rho is 61% of E at k = 1 (`trho.py` reproduces the engine to 6 digits in 1 s). Power counting finds no 1/a or 1/a^2 W-dependent term:
  expected R(t0+L) -> constant. So I do not think T54's accounting misses a term here; the acceleration looks numerical.
- Rejected on the way: cross-slice near-coincident poles (`pole_pairs_output.txt`, none below 2e-4); "K'(x,x) = -G d" (false, measured).

## 3. SEALED PREDICTION for l = 3 (W1 = 6, W2 = 12, P = 12), written 2026-11-25 before the office run lands
- Exposure: I read t0(W12) = -486.137451 and T_sad(W12) = 504.570481 in report.md. I opened no k = 3 result file.
- **Production value (as the current code computes it): R(t0 + L)(3) = -1.55, 68% band [-2.0, -1.1], outer band [-2.5, -0.7].**
  Sub-predictions (S units): E(W6P12) = 1.892 +- 0.008; E(W12P12) = 1.78 +- 0.03.
- **If t0(W12P12) is recomputed with a contour radius below its smallest unmerged doublet gap: t0 moves UP (less negative), and R(t0+L)(3) moves up.**
  Same for W8P8 and W10P10: predicted sign dt0 < 0 in the stored values; size order 0.02 (W8P8) and 0.08-0.13 (W10P10), from the E_w anomaly.
- Fails if: R(t0+L)(3) > -0.7 or < -2.5; or t0(W8P8) does not change (beyond 1e-5) when rad goes 1e-5 -> 1e-6.

## 4. For the office sister to check
1. Re-run `rad_test.py 8 3 8 16 1e-5 1e-6 3e-7` (1.5 min). 2. Run `artifact.py` at W8P8, W10P10, W12P12. 3. t0 at W8P8 with rad = 1e-6 (KA: rad 1e-5
must reproduce -209.300110). 4. Mechanism B on a W = 10 tiny box (rad sweep down to 3e-8). 5. Then recompute R(2), R(2.5) and re-read 085/085c slopes.
