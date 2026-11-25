# Answer to the n = 2 counterterm brief (office brief 91595d1) — Fable side-session, 2026-11-25 [model: Fable 5.2]
**Everything here is UNVERIFIED until the office sister checks it.** Each claim carries a grade.
Seal: `notes/fable_t0L/SEAL_n2_l2.5.md`, commit bcdb69f, pushed before anything below was worked out on data.
Scripts and outputs: `notes/fable_n2/` (`sig2_profile.py`, `raw_units.py`, read-only on stored office files; seconds each; no P = 10 saddle opened, none exists).

Notation. X = (sheet, y, x) with x = (x, t) a site of the 2D section; J(x) = 1/g(x) = G1_box(x,x); c(x) = N * delta(1/g(x));
sigma_n(x) the replica-symmetric saddle; B_n = 2 G_n o G_n; Sigma^(x,y) := B1^-1(x,y) G1(x,y) (the 1/N self-energy kernel, up to a constant factor);
Lambda(x) := Sum_y Sigma^(x,y) (its row sum, "local zero-momentum self-energy"); tau(z) := d(log det B1)/d sigma(z) (the full box tadpole);
D(l) := Sum_x sigma_2 (W1) - Sum_x sigma_2 (W2); DA(l) the same with weight c_A; S_n(l) := R_n + dR_n^A.

## Short answers
1. **Complete.** At O(N^0) and any integer n the counterterm is exactly -(1/2) n Ny Sum c sigma_n. No O(sigma^2), no response term, no saddle-shift term.
2. **The same c(x) at every n.** The counterterm is a property of the model's coupling, not of the Rényi index. The full box tadpole is the wrong choice.
   Box c_A versus bulk c is a separate question: both are legitimate families with the same asymptotic slope; A is the one that continues the N = infinity definition.
3. **No genuine 1/a^2 term.** R_2's l^2 growth is l times a tail integral of sigma_2 ~ -0.035/r^2 that has not converged at W <= 8. **Sealed: S_2(2.5) = 0.182 +- 0.020.**
4. **The two pictures agree** at the precision available. The leftover sits in S_n(l), is positive in both branches, and is 2-4% of the raw growth.

## 1. Is the first-order form complete at integer n?  — grade: DERIVED (exact identity; the argument is standard)
Z_n(J) = Int D sigma exp(-(N/2)[Tr log(H_n + sigma) - Sum_X J sigma]). The coupling enters ONLY through the term linear in sigma. So for J -> J + c/N, exactly,

  F_n(J + c/N) - F_n(J) = -log < exp( (1/2) Sum_X c(X) sigma(X) ) >_J .

Cumulants: <sigma> = sigma_n + O(1/N); connected <sigma sigma> = O(1/N) (the sigma propagator is (2/N) B_n^-1); higher cumulants are smaller. Hence

  dF_n = -(1/2) Sum_X c sigma_n + O(1/N) = -(1/2) n Ny Sum_x c(x) sigma_n(x) + O(1/N).

- **O(sigma_n^2):** cannot occur. The shift is linear in sigma at every order, because 1/g multiplies sigma only.
- **Response d sigma_n / d(1/g):** it is the second cumulant, O(1/N).
- **Counterterm-induced saddle shift:** delta sigma = O(1/N); by stationarity it changes N*S by O(1/N), and (1/2) log det B_n by O(1/N).
- None of this needs sigma_n small. It needs only (a) B_n[sigma_n] non-degenerate, (b) the replica-symmetric saddle is the dominant one at that n,
  (c) the fluctuation determinant runs over ALL sigma fluctuations on the n-sheeted lattice (replica-odd ones included).
- n dF_1 = 0 because sigma_1 = 0. So the brief's dR_n = (n/(2(n-1))) Ny Delta_W[Sum c sigma_n] norm is complete.
- Standard: this is first-order perturbation theory / the envelope theorem; I give no reference for it. The 1/N setting for entanglement in the O(N) model:
  Metlitski, Fuertes, Sachdev, "Entanglement Entropy in the O(N) model", arXiv:0904.4477 (title, authors, id checked on arXiv; journal ref seen only second-hand).
- **Caveat on (b), not checked by me:** Rényi entropies of large-N vector models can change saddle as a function of n. The abstract of 0904.4477 mentions a transition
  in n near d = 3, and a search turned up arXiv:1811.04109 ("On phase transitions in the Rényi entropies of 2+1-d large-N interacting vector models"; title only seen, NOT read).
  The office's continuation matching the honest n = 2 family to 1.5e-5 says the continued branch IS the n = 2 saddle that was found; it does not say that saddle dominates.
- **A check that can fail** (office, tiny box): shift 1/g(x) by eps*c_A(x), re-solve the n = 2 gap equation, and compare the change of the LEADING-order free energy
  with -(eps/2) n Ny Sum c_A sigma_2. It tests sign and prefactor without using T54/T55 (a proposed check, not run).

## 2. Which prescription at n = 2?
**2a. The profile c(x) cannot depend on n.** — grade: DERIVED. By §1, R_n + dR_n[c] IS the honest R_n of the lattice model with coupling J(x) + c(x)/N. One model, one c(x),
all n. So using c_A at n = 2 is not an extra assumption beyond having chosen A at n -> 1. An "integer-n subtraction" (e.g. a tadpole built from B_n) does not exist as an option:
everything specific to the n-sheeted lattice is already inside log det B_n[sigma_n], exactly.

**2b. The full box tadpole is wrong.** — grade: ARGUED (uses the office's identity, 1e-12 KA in exp085c_run.py). From the 085c definition (free index z),
c_A(z) = -4 term1(z) + 2 (B_0 Lambda)(z) = tau(z) + 2 (B_0 Lambda)(z).
- c = tau means "the sigma tadpole cancels, <sigma>_1 = 0 at O(1/N)". Then the n = 1 propagator keeps the unsubtracted self-energy, i.e. a local mass Lambda(x)/N.
  That is not critical: in the bulk the critical point has <sigma> = -Sigma(0)/N, not 0. And B_0 at zero momentum grows like P, so tau differs from c_A by a term that grows with the box.
- With tau, the n -> 1 saddle term would cancel exactly and leave t0 + C, whose t0 carries the k^2-sized mass piece. A does the reverse: it leaves
  Sum (Sigma^(x,y) - Lambda(x) delta_xy) dG(y,x), a kernel with ZERO ROW SUMS, which is why the k^2 pieces cancel identically (my HANDOVER §2).

**2c. Box c_A versus bulk c.** — grade: ARGUED; numbers below are stored office values.
- c_A - c is ~ -2c/P times a profile of x/P: a scale-covariant, dimension-1 deformation. Its effect on R is Ny * (1/P) * Delta_W[Sum h sigma_n] = O(l^0) times logs.
  So **A and bulk have the same asymptotic slope; they differ by a constant plus (at n = 2) a log l term.** The 1.37-1.50 "overshoot" of bulk c is this difference still building up.
- Evidence it is building, not a wrong coefficient: local overshoot ratio of bulk c is 1.438 (l 1 -> 1.5) then 1.324 (1.5 -> 2) [hi end; lo 1.570, 1.445]. It is falling.
- But it is slow: Y_bulk - Y_A = 1.009, 1.406, 1.825 (hi), still rising 0.4 per half step. Two parts (rough hand arithmetic): 12.9*D(l) = 0.79, 0.97, 1.12, which
  saturates when D does; and a part from c_A being closer to c at the narrow strip's ends (w1 - w2 = 0.016, 0.013, 0.012) times Ny*|Sum sigma_2|: 0.31, 0.45, 0.65.
  The second part is the log: |Sum sigma_2| grows like 0.44 ln W (§3).
- Why A is the right one of the two (argued, not proved): the N = infinity family is DEFINED by "the n = 1 box is the massless free box" (sigma_1 = 0). A is the same statement
  at O(1/N): the n = 1 self-energy has no local mass term (zero row sums) and the constraint holds. Bulk c instead leaves the n = 1 box with a mass profile of order 1/(N P^2).
  Normalising by the free kappa(l) of the same box only makes sense if the n = 1 box stays massless.
- **What I cannot show:** that S_2 under A has NO log l term. At n = 2 the area-law coefficient depends on the local coupling with a log (because sigma_2 has a 1/r^2 tail),
  and the two strips' ends sit at different c_A. So S_2(l) = const + lambda*log l is possible. Grade of "lambda = 0": UNVERIFIED. Data only bound it: S_2 moves 0.016, 0.021 per half step.

## 3. Is R_2's l^2 growth a genuine 1/a^2 term?
**3a. No W*Ny/a^2 term can exist.** — grade: ARGUED (locality). The cut is movable; away from its two end lines the n-sheeted lattice is locally the plain lattice, with the same
J(x) on every sheet. Local divergent terms sit on the end lines, are proportional to Ny, and do not depend on W. Nothing is "owed" to the cut area.
(R_n = const means the W-difference of Q is O(1); R ~ l means it is ~Ny; R ~ l^2 would need ~W*Ny, a cut tension.)

**3b. What the stored sigma_2 shows** (`sig2_profile_output.txt`). — grade: VERIFIED BY EVALUATION on stored profiles, P <= 8, one reading
- sigma_2 < 0 everywhere, peaked on the 8 sites at r = 0.707 from the two cut ends (-0.060 to -0.067 each; about half of Sum sigma_2).
- r^2 * sigma_2 is flat for r <~ 3: -0.031, -0.037, -0.034, -0.029 (W4P8 shells), then falls (-0.020, -0.012, -0.004). So **sigma_2 ~ a_2/r^2 with a_2 ~ -0.035**, cut off at r ~ W.
- Along the cut, away from the ends (W8P8, 2.5-3.5 sites in): -0.0025. That is tail level. No sigma_2 "on the cut".
- Sum sigma_2 per geometry: -0.706, -0.897, -1.021 (W = 2, 3, 4) and -0.767, -0.972, -1.108 (W = 4, 6, 8): slope -0.43 to -0.51 per ln W. The tail predicts 4 pi |a_2| = 0.44.
- D(l) = 0.0609, 0.0750, 0.0865: still growing. By region at l = 2: core (r < 1.2) +0.011, middle +0.029, far (r >= 3.2) +0.046; the far part was -0.002 at l = 1.
  The W-difference of two log tails needs both tails developed; at W1 = 2..4 the narrow strip has almost no tail.

**3c. So where the l^2 comes from.** — grade: ARGUED, consistent with 3b. Y_2 = Ny |c_eff| norm D(l) ~ l * D(l), and D(l) is still climbing toward D_inf.
In raw units (`raw_units_output.txt`): R_2/norm = 0.04822, 0.11295, 0.19737, 0.30163, second differences 0.0197, 0.0198; Y_A/norm = 0.03987, 0.10311, 0.18632,
second difference 0.0200. The same curvature, which is the 98%.
- Asymptotically R_2 must become linear, slope 25.7 * D_inf per unit l (hi c). D_inf is not known from these sizes (0.11 from an A - B/l fit; up to ~0.3 if the tails
  develop fully). **Prediction: R_2/l^2 (0.683, 0.689, 0.695, 0.691) falls at larger l.** Not testable at l <= 3.
- Contrast with n -> 1 (continuum linear response, DERIVED; profile itself NOT checked, sigdot is not stored): d(r) = b/r and B^-1 = 4|p| give sigdot(p) = 16 pi b, a constant:
  **sigdot is a contact term at the cut end, with no 1/r^2 tail** (a_sigma starts at order (n-1)^2). Consistent with the stored numbers: the W-difference of Sum c_A sigdot,
  divided by c(1 - 2/P), is 0.307, 0.308, 0.316, 0.326 (l = 1..2.5): flat to 6%. The n = 2 analogue grows 42% from l = 1 to 2.
  That is why the continued R is linear from the start and R_2 looks quadratic.

**3d. Sealed prediction and what I learned after sealing.**
- **Sealed (bcdb69f): S_2(2.5) = R_2 + dR_2^A = 0.182 +- 0.020; outer [0.14, 0.23].**
- Post-seal, raw units (seal not changed): three continuations give 0.172, 0.174, 0.176. Inside the sealed 68% band.
- **Main risk, found after sealing:** S is a 4% difference of two numbers near 4.2, so the answer depends on which variable is smooth. If DA (without the Ny factor) is the smooth one:
  0.27. If |DA| saturates like A - B/l - C/l^2: 0.35. Both break the outer band. My reason to reject them: honest R_2/norm is quadratic through l = 2.5 with third difference
  0.0001, and R_2 = Y_A + S exactly, so a kink in Y_A needs an equal and opposite kink in S. That is an argument, not a measurement. If the value lands at 0.27-0.35, then
  "c_A tracks R_2 including its curvature" fails at P = 10 and §2c's choice of A is in doubt.
- Second prediction (follows from the seal plus the trend of Y_bulk - Y_A): local bulk overshoot ratio on l = 2 -> 2.5: **1.27 +- 0.03 (hi end), 1.39 +- 0.03 (lo end)**; i.e. still falling.

## 4. Consistency of n -> 1 and n = 2
| l | 1 | 1.5 | 2 | 2.5 |
|---|---|---|---|---|
| n -> 1: R - Y_A (R(2) with the office's measured +0.146; R(2.5) with the predicted +0.87, not yet measured) | 0.274 | 0.369 | 0.483 | 0.56 |
| n = 2: R_2 + dR_2^A | 0.119 | 0.135 | 0.156 | sealed 0.182 |
- Both residuals are positive and drift up slowly: +0.19 per unit l at n -> 1 (4% of the raw slope 4.6), +0.037 at n = 2 (1.8% of R_2's growth). Same sign, same order.
- The fractions differ (4% vs 1.8%), so the drift is not one common rescaling of c_A. It reads as the finite-size behaviour of S_n(l) = "twist at fixed sigma with the
  mass-subtracted self-energy" + "non-linear terms". At n -> 1 those two parts are (0.76, 0.54, 0.43, 0.37) and (-0.49, -0.17, 0.05, 0.19): one falling, one rising, both slowing.
- **Verdict: (1) complete, (2) delta_A, the same at all n, (3) no 1/a^2 term. T54 with the box prescription is the whole story to within a positive residual of 2-4% of the growth.**
  If a leftover is real, it is in S_n(l), sign positive (A slightly under-subtracts), and at n = 2 it may be a log l (§2c). Grade of the verdict: PARTIALLY VERIFIED
  (items 1, 2a derived; 3b evaluated on stored data; 2c, 3a, 3c argued; the n -> 1 row rests on my unverified corrected values plus one office measurement).

## 5. For the office sister
1. sigma_2 at P = 10: S_2(2.5) against the seal; the local bulk ratio against 1.27 / 1.39.
2. Re-run `notes/fable_n2/sig2_profile.py` (seconds): r^2 sigma_2 plateau, tail-level sigma_2 along the cut, D(l) by region.
3. The finite-difference check in §1 on a tiny box.
4. sigdot profile at any stored geometry: is it contact-like (no 1/r^2 tail)? This is the one claim in §3c I could not look at.
5. Whether the n = 2 saddle that was found is the dominant one (§1 caveat b) — I have no evidence either way.

## 6. Kept on file: what I got wrong on the way
- From the brief's rounded weights (0.54, 0.66, 0.73) I first reconstructed bulk dR_2 as -1.04, -2.15, -3.60. Wrong (stored: -1.573, -2.822, -4.450): the weights are per strip, not per W-difference.
- I first expected Y_bulk - Y_A to saturate near 1.4 soon. The stored values (1.009, 1.406, 1.825) show no saturation by l = 2; the log part (§2c) was missing from my estimate.
- My sealed error bar (+-0.020) did not account for the sensitivity in §3d. It stands as sealed.
