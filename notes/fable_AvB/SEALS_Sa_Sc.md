# SEALS S-a and S-c for the brief notes/fable_brief_A_vs_bulk.md (main a0b6042) — 2026-11-26 03:40 IST [model: Fable 5.2]
UNVERIFIED by construction. Committed before any computation for this brief and before any addendum is read.

## Exposure (stated in full)
- NOT opened: `notes/fable_brief_A_vs_bulk_ADDENDUM_wall.md`; `G_W6P12.json`, `G_W12P12.json`; any k = 3 result file; kappa(3).
- KNOWN to me already, and it bears on S-c: the office's EXP-089 message (2026-11-25) quoted Sigma3D(W6P12) = -140.23314 and Sigma3D(W12P12) = -158.44252
  (D1(3) = 0.379362). So the BULK half of Delta_bb(3) is not blind: raw y_bulk(3) = (1/2)*48*|c_hi|*0.379362 = 1.03891.
  Blind parts of S-c: X_cA at P = 12 (the box half), the interior c_A/c at P = 12, and norm(3).
- Used for the seals: only numbers in this brief and my own k <= 2.5 tables (`notes/fable_n2/gb_n1_output.txt`, commit 7c846a1). No new run.

Notation: Delta_bb = Y_A - Y_bulk = R[(1/2) Sum (c_A - c) sigdot]; raw g_b := -Delta_bb / norm = y_bulk - y_A; Sx = Sum_x sigdot per y-slice;
D1 = Sx(W1) - Sx(W2); c_Ainf := lim_{P -> inf} of the interior c_A.

## S-a. Form of Delta_bb(k) for k -> infinity, and the verdict on Q1
**Form (argued):  Delta_bb(k) = -L k - G_inf + beta/k + o(1/k),  with  L = 8 D1_inf norm_inf (c_Ainf - c) ~ 45 (c_Ainf - c).**
- **No log k.** (argued from the sigdot profile: r^2 sigdot has no flat stretch; wall layer guessed below 1% of Delta_bb.)
- **The linear term is not a scheme difference; it is the error of the bulk number.** c_Ainf is the true lattice c_inf (A is the bulk formula in position space).
  Any bulk value c != c_Ainf gives -45 (c_Ainf - c) k. From the brief's interior ratios I get c_Ainf = -0.1145 +- 0.0025 (not blind).
  - hi end (c = -0.11411): L = 0.0 +- 0.11 per unit k. So **Delta_bb(hi) -> const = -G_inf, G_inf = 4.7 +- 0.6** (raw g_inf = 0.33 +- 0.04), beta ~ +2.4. Sign: negative.
  - lo end (c = -0.12458): L = +0.45 +- 0.11, i.e. Delta_bb(lo) keeps falling ~ -0.45 k. That is c_lo being off, nothing else.
- **Verdict on Q1 (argued):** A and bulk have the SAME asymptotic slope when the bulk number is exact. They differ by a constant, G_inf, at fixed aspect ratio.
  That constant is a box effect: it goes away when the walls recede at fixed strips (W/P -> 0), where both give the bulk delta-kappa. So: both converge; they differ at finite aspect ratio only.
  - The O(1/N) mass profile of the bulk-c box is an ARTIFACT, not content to keep. Reason: 1/g(x) = G1_box(x,x) was chosen to remove exactly that kind of profile at leading
    order (so the N = infinity box is the free massless box and the leading ratio is exactly the bulk one at ANY aspect ratio). Bulk c keeps that tuning at order N and drops it
    at order 1; A keeps it at both orders. A is the consistent prescription; bulk c is a hybrid.
  - What I do NOT claim: that A's constant equals the bulk delta-kappa at aspect ratio (1/2, 1). At O(N^0) the walls still distort the sigma propagator. Only W/P -> 0 settles that.
  - Practical point (derived arithmetic): bulk needs c_inf to 0.6% to hold R_corr(3) to +-0.1; the bracket is 9% wide (+-0.47 k). A needs no external number.
- **S-a fails if** Delta_bb(hi) stops decelerating (|Delta_bb(3) - Delta_bb(2.5)| >= 0.306, the last step), or if the interior (1 - c_A/c_hi) P keeps rising linearly in P.

## S-c. Predictions at k = 3 (P = 12)
- **Interior c_A/c (hi c) at P = 12: 0.826 +- 0.003.** Fails outside [0.820, 0.832]. (From (1 - ratio) P = 1.73, 1.90, 1.99, 2.05 -> 2.09.)
- **Raw g_b(3) = y_bulk - y_A = 0.2735 +- 0.0030 (hi c);** with it y_A(3) = (1/2)*48*|DA1| = 0.7654 +- 0.0030. This target does not need norm(3) (sealed prediction, unverified).
  Sub-predictions: sigdot-weighted c_A/c: W6P12 0.8206 +- 0.0010, W12P12 0.8109 +- 0.0010.
- **Delta_bb(3), hi c: -3.89 +- 0.08.** Fails outside [-4.05, -3.73]. **lo c: -5.24 +- 0.11** (raw 0.3689).
  These use my GUESS norm(3) = 14.22 +- 0.20 (kappa(3) unknown to me). If norm(3) is outside that, grade the raw g_b instead.
