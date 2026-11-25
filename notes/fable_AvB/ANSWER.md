# Answer to notes/fable_brief_A_vs_bulk.md (main a0b6042) and its wall-test addendum — Fable side-session, 2026-11-26 [model: Fable 5.2]
**Everything here is UNVERIFIED until the office checks it.** Seals: `SEALS_Sa_Sc.md`, commit c615773 (an ancestor of this commit; made before any computation and before the addendum).
Runs: `sb_check.py` (0.0 s wall, 29 MB peak; stored k <= 2.5 files, read-only) and `post_addendum_arith.txt` (arithmetic on brief + addendum numbers). No P = 12 file opened.

Notation: Delta_bb = Y_A - Y_bulk; G_b = -Delta_bb; raw g_b = G_b/norm; Sx = Sum_x sigdot per y-slice; D1 = Sx(W1) - Sx(W2); u(x) = 1 - c_A(x)/c;
h_i = (1 - w_i) P with w_i the sigdot-weighted c_A/c of strip i; rho_A = R - Y_A.

## Short answers
1. **Both converge to the bulk answer when the walls recede (W/P -> 0); at fixed aspect ratio they differ by a constant.** That constant is a box effect, not bulk physics.
   A is the consistent prescription; the bulk-c mass profile is an artifact. **But A is not converged either:** the wall test puts A's own error at about 0.2 of the A-bulk gap.
2. **Delta_bb -> const** (hi c): about -4.7 +- 0.6. A k-linear term appears only if the bulk number is not the true lattice c_inf. No log k expected; k <= 2.5 alone cannot exclude one.
3. **n = 2 fits the same picture** for the choice of c. It does NOT support carrying the wall-test fraction over as a universal correction.
4. **Consequence (argued, post-addendum):** the aspect-ratio error is now the dominant uncertainty on delta-kappa: about 0.5-0.8 in R units at k <= 2.5, larger than R - Y_A itself.

## 1. Scheme or physics?
**1a. Leading-order analogue.** — grade: DERIVED (standard: stationarity of the large-N action in sigma). At N = infinity, S = N x (entropy of free fields in the potential sigma_1(x)).
(Stated for general geometries in Whitsitt et al., arXiv:1610.06568, "Entanglement entropy of the large N Wilson-Fisher conformal field theory"; I checked title, id and abstract, not the full text.)
- Uniform bulk-critical 1/g in a Dirichlet box: sigma_1(x) != 0, a geometry-induced mass profile. The leading ratio to the free box is 1 only as W/P -> 0.
- 1/g(x) = G1_box(x,x): sigma_1 = 0, the free massless box. The leading ratio is exactly 1 at ANY aspect ratio.
- So at order N the site-by-site tuning exists precisely to remove the box-induced mass profile, and it makes the box estimate exact.
**1b. Next order.** — grade: ARGUED. The tuning that keeps the n = 1 box massless at O(1/N) is c_A (zero-row-sum self-energy). Bulk c keeps the tuning at order N and drops it at
order 1: a hybrid. Its O(1/N) mass profile is the same kind of object as the leading sigma_1(x) that the construction removes, so it is a regulator artifact to subtract, not content to keep.
- It does not turn on the ordinary transition as such. It turns on how 1/g is defined in the finite volume: "the massless Dirichlet box, order by order" (A) versus
  "massless box at leading order plus the bulk shift" (bulk c). A uniform bulk-critical 1/g at BOTH orders would be a third, also legitimate, regulator with its own honest R.
**1c. What A does not give.** — grade: ARGUED before the addendum (in the seal), now MEASURED by the office. At O(N^0) the entropy is not a free-field entropy, so dividing by the box
kappa no longer removes the wall effects exactly. A has an aspect-ratio error of its own. See §4.
**1d. Practical.** — grade: DERIVED arithmetic. An error dc in the bulk number shifts R_corr by 45 dc k. The 9% bracket is +-0.47 k. A needs no external number.

## 2. Asymptotics of Delta_bb(k)
**Structure** (exact rewriting): raw g_b = -(c/2) Ny [(1 - w1) Sx1 - (1 - w2) Sx2] = -2c [h1 Sx1 - h2 Sx2] = -2c [hbar D1 + (h1 - h2) Sxbar].
- **Interior.** Centre u*P = 1.666, 1.858, 1.968, 2.034 (P = 4..10) = 2.30 - 2.64/P for P = 6, 8, 10 (both step slopes equal 2.64). It saturates. — grade: stored arithmetic, 3 points.
  So c_A(centre) -> -0.1142 (quadratic in 1/P); cubic gives -0.1153, linear -0.1104. **c_Ainf = -0.1145 +- 0.003, on the hi end of the bracket.**
- **Weights and sums.** h1 = 1.747, 1.945, 2.050, 2.113 -> ~2.37; h2 = 1.814, 2.030, 2.151, 2.224 -> ~2.51 (1/P continuation). Sx1 -> ~-3.4, Sx2 -> ~-3.8, D1 -> 0.395
  (D1(3) = 0.3794 already graded by the office against my 0.3790).
- **Limit.** g_inf = 0.228 x [2.44 x 0.395 + (-0.147)(-3.58)] = 0.220 (uniform shift) + 0.120 (the two strips' ends sit at different c_A) = 0.34. In R units G_inf ~ 4.8.
  Sealed: 4.7 +- 0.6. — grade: ARGUED (each factor continued in 1/P).
- **Wall layer.** With sigma_2 as proxy weight (sigdot per site is not stored): share of Sum u*sigma_2 from d <= 2 is 11%, 3.2%, 1.4% at P = 4, 6, 8; from d <= 1: 2.6%, 0.85%, 0.39%.
  It dies like P^-2.5 or faster. No wall log. My pre-stated 5% line was crossed at P = 4 only (there d <= 2 is half the box). — grade: evaluated on a proxy.
- **Near-wall profile** (new, descriptive): u*d = 0.80, 1.12, 1.30, 1.43, 1.53 for d = 1..5, the same at P = 6, 8, 10: about 0.80 + 0.45 ln d. Not a pure 1/d law.
  If that log reached d ~ P the interior u*P would grow like ln P and Delta_bb would get a log k. The centre data say it does not (per-ln P increments 0.47, 0.38, 0.30, falling).
- **So: Delta_bb(hi) = -G_inf + beta/k, no k-linear term if c_hi = c_Ainf (L = 0.0 +- 0.11), no log expected.**
**S-b (consistency check, NOT blind).** Fits to raw g_b, k = 1..2.5: g_inf - beta/k rms 3.0e-3; a + b ln k rms 1.5e-3; a + b k rms 5.8e-3; g_inf - beta/k + gamma/k^2 rms 3.7e-4 (g_inf 0.353).
- **Honest reading: among two-parameter forms the log fits better than 1/k.** The three-parameter saturating form fits best but has one degree of freedom. k <= 2.5 cannot exclude a log.
- S-c separates them: at k = 3 the log form gives raw 0.2817, the saturating forms 0.269-0.276; my seal is 0.2735 +- 0.0030. If the office measures >= 0.279, saturation is in doubt.
- Lo minus hi: Delta_bb(lo) - Delta_bb(hi) = -0.4106, -0.6279, -0.8770, -1.1275 is exactly -8 dc D1 norm k (an identity; it cannot fail). Lo c carries a k-linear artifact if c_Ainf is the hi end.

## 3. Consistency with n = 2
- c(x) is a coupling, the same at every n (derived in my previous answer; the office's finite-difference test agreed). — So the n = 2 result is the same statement as n -> 1.
- n = 2 bulk "overshoot" ratio falls 1.44, 1.32, 1.21 (l = 1..2.5): the n = 2 gap G_b = 1.009, 1.406, 1.825, 2.157 is building toward its own constant, as at n -> 1. — grade: stored arithmetic.

## 4. What the wall test adds (post-addendum; nothing here is blind to it)
- My sealed f = 0.0 +- 0.3: measured **+0.212**. PASS, but not zero: when the walls move from P = 4 to 6 at fixed strips, rho_A drops 0.2735 -> 0.0472 while the gap closes 2.4920 -> 1.4256.
- **Reading (argued): A is the better prescription and is still off, by roughly 0.2 of the gap, in the direction of bulk.** For strips (2, 4) the wall-free value is
  -0.41 (A error ~ 1/P), -0.26 (A error = f x gap), -0.13 (A error ~ 1/P^2). All three are NEGATIVE while rho_A(4) = +0.27. One P step cannot choose between them.
- The two prescriptions do converge at fixed strips, faster than 1/P: G_b ~ P^-1.4 (or 5.7/P + 17/P^2). My unsealed sketch for P = 6 was 1.7; measured 1.43.
- **A coincidence I must report, and its counterexample.** On the scaling family, rho_A - 0.212 G_b = -0.255, -0.262, -0.250, -0.235 (k = 1..2.5, hi c): flat to 0.014, and the
  flattening mix is 0.228, next to the wall test's 0.212. That would read "A's upward drift is 0.2 x the growing gap, and the wall-free value is about -0.25".
  **But at n = 2 the same construction fails:** S_2 - 0.212 G_b = -0.096, -0.163, -0.231, -0.296, and the flattening mix there is 0.038. So "flat in k" does not pick the wall
  fraction in general. I do NOT propose 0.212 as a correction factor. Grade: post-hoc observation, unverified, one supporting and one contradicting instance.
- **What follows without any fitting:** rho_A at aspect (1/2, 1) carries a wall error of order 0.2 x G_b ~ 0.5-0.8 for k <= 2.5. That is larger than rho_A (0.27-0.56). So neither the
  size nor the SIGN of the wall-free O(N^0) coefficient is fixed by the A series alone. ρ_s = +0.043 "A flattens" stays true; it is a statement about the boxed family.

## 5. Predictions made here, after the addendum and before any further run (grade: sealed by this commit; not blind to the addendum)
- **P-1 (second wall step, strips (2, 4), P = 8; needs one fresh W2P8 route, W4P8 is stored):** G_b(8) = 0.97 +- 0.06; rho_A(8) = -0.05 +- 0.04; f(6 -> 8) = 0.21 +- 0.08.
  If f(6 -> 8) is near 0, A's error dies fast and the wall-free value is near +0.05. If it is >= 0.4, A's error is larger than read here. Three P points also allow a 1/P + 1/P^2 fit.
- **P-2 (wall test at n = 2, strips (2, 4), P = 4 -> 6; tiny boxes): f_2 = 0.05 +- 0.15.** Grade: GUESSED (from the n = 2 flattening mix 0.038). f_2 ~ 0.21 would instead say the
  fraction is a property of the box, the same at every n, and would support using it as a correction.
- Not made: any new R(3) prediction. S-1 to S-3 stay as filed.

## 6. For the office
1. Grade S-c from the stored P = 12 GEOM files (raw g_b(3), interior ratio, the two weighted ratios).
2. P-1 is the cheapest run that moves the main uncertainty. A scaling family at a second aspect ratio (P = 8k) would be the full answer; P-1 is its k = 1 point.
3. The near-wall profile u*d ~ 0.80 + 0.45 ln d: is the log real (a (ln d)/d finite-size law for c) or a crossover? c_A on a tiny box with P = 14-16 at n = 1 would show whether centre u*P keeps to 2.30 - 2.64/P.

## 7. REVISION after my own c_A run (commits 4edf674, 2499e4e; seal c615773 left as written) — this changes S-a
Runs (1 core, nice 12): `ca_centre.py` P = 4..14: 0.0, 0.0, 0.1, 0.6, 2.4, 5.7 s wall; peak 30, 42, 82, 169, 367, 751 MB. `h0.py` 0.1 s, 68 MB. `h0_positions.py` seconds.
**7a. Second implementation of c_A.** — grade: VERIFIED BY EVALUATION against the stored office values (two implementations): all sites at P = 4, 6 and the centre at P = 8, 10
agree to 1e-14; the planted break fails as required. New: centre c_A = -0.09440692 (P = 12, ratio 0.82737) and -0.09706750 (P = 14, ratio 0.85068).
**7b. My pre-registered reading was satisfied and I reject it.** Centre u*P = 2.0716, 2.0905 at P = 12, 14, below the 2.117 line that was to "support saturation". But that line
assumed c_inf = c_hi. Fitting c_A itself, the limit moves with every point added (-0.1142, -0.1151, -0.1157, cubic -0.1166) and a (ln P)/P form fits 10x better. u*P flattens
because c_A is heading PAST c_hi, not because it has converged to it. A check that named the failure and could not see it.
**7c. H-log, pre-registered before computing h0 (2499e4e).** The massless-box tuning is a profile of the relevant coupling, dimension y = 1 + y1/N, y1 = 32/(3 pi^2).
Scale covariance gives c_A - c_inf = (g1 + gL ln P)/P with gL = y1 h0, h0 = lim P (G_inf(0) - G1_box(x,x)), a leading-order lattice sum.
- h0(centre) = 0.0566, so gL = 0.0611. Free fits had given 0.074-0.077. Inside my pre-stated "supported" window [0.06, 0.09], near its edge.
- With gL FIXED at 0.0611 (no extra parameter) the fit c_inf + (g1 + gL ln P)/P + g2/P^2 has rms 6.5e-7 on P = 8..14, against 4.3e-6 without the log; 3.1e-6 against 1.8e-5 on P = 6..14.
- **c_Ainf = -0.1183 +- 0.001** (the three point sets give -0.11824, -0.11815, -0.11830; free-log fits -0.1188 to -0.1190). — grade: ARGUED (a fit with one theory-fixed coefficient).
  This is inside the bracket and inside the Hasenbusch window quoted in the brief (-0.1165 to -0.121). It is not the hi end.
**7d. What this does to S-a (my own scoring; the office should grade it).**
- Sealed "c_Ainf = -0.1145 +- 0.0025": **probably wrong** (now -0.1183).
- Sealed "hi c: L = 0.0 +- 0.11, Delta_bb(hi) -> const": **probably wrong.** c_hi is 3.6% short of c_Ainf, so G_b(hi) = G_b(c_inf) - 0.036 Y_bulk(hi): a k-linear piece of about -0.19 k in G_b.
- Sealed "no log k": **probably wrong against the exact bulk number.** Asymptotically raw g_b(c_inf) = a0 + aL ln k with aL = 2 y1 [hbar D1 + (h_wide - h_narrow)|Sx|] = 0.069
  (0.98 in R units: 0.70 from the uniform shift, 0.28 because the wide strip's ends sit at larger h0: 0.0591 against 0.0566). With c_inf = -0.1183 the stored k <= 2.5 values give
  G_b = 2.656, 3.228, 3.802, 4.208 and raw increments per ln k of 0.117, 0.121, 0.109: above the asymptotic 0.069 and starting to fall. Grade: ARGUED; coefficient not yet tested.
- This also explains the S-b fits: the log form beat 1/k because a log is there, partly masked at hi c by the -0.19 k piece.
**7e. Revised verdict on Q1.** — grade: ARGUED, partially supported by 7c.
- A and the exact bulk prescription do NOT differ by a constant. They differ by about -1.0 ln k (R units), from the anomalous dimension of the coupling that the box tuning uses.
- **Only A is a scaling family.** The leading-order profile G1_box(x,x) - G_inf = -h0/P is the right tuning when the coupling has dimension 1. At O(1/N) its dimension is
  1 + y1/N; the profile that keeps the box at the same scaled point is -h0/P^y, and the 1/N part of that is exactly the (ln P)/P piece that c_A contains and bulk c omits.
  With bulk c the scaled coupling drifts like ln P, so R_corr(bulk) has no k -> infinity limit at fixed aspect ratio: it keeps falling by ~1.0 per ln k.
- So bulk c is wrong for this box family even with the exact bulk number. It is not a second route to the same delta-kappa. A's remaining error is the constant aspect-ratio
  effect of §4 (wall test), which only W/P -> 0 removes. The uniform bulk-critical coupling at BOTH orders remains a different, legitimate regulator.
- n = 2: the same c(x), the same log. The falling bulk "overshoot" ratios (1.44, 1.32, 1.21) are a log against a quadratic-looking R_2, not convergence to 1 by a constant.
**7f. For the office.** (i) Grade S-a as probably failed in the three places above. (ii) Check H-log with one more box: centre c_A at P = 16-20 (my script needs 1.25 GB at
P = 16, over my limit); prediction from the fixed-gL fit on P = 8..14: c_A(16) = -0.09915, c_A(20) = -0.10220. (iii) If c_inf = -0.1183 holds, bulk-c readings should use it
(hi and lo ends are 3.6% and 5.3% off on either side). (iv) y1 = 32/(3 pi^2) is quoted from memory; please check it at a source before relying on 7c.
