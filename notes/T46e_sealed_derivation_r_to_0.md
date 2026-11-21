# Sealed derivation: the n → 1 contribution of λ → ¼ (r → 0) modes under the anchored-residue continuation
[model: Opus 5.5] Written blind to T46e (at the Bridge's request, 2026-11-22), before T46e returned. T46e is to be graded against this text, not the other way round.
Grades: every statement below is **argued** unless marked otherwise. The numerical checks in §6 are run after sealing and recorded separately.

## 1. Objects (notation as in the T46c/T46d code, restated)
- Each Woodbury cut mode has an eigenvalue λ ≥ ¼ of S = M₋^{½} M₊ M₋^{½}, where
  - M₊ = ½I + G_s and M₋ = ½I − G_a;
  - G_s, G_a are the symmetrised cut-projected Green's-function blocks.
- The mode's α-dependence is f(α) = 1/(λ − γ²) and h(α) = γ f, with γ(α) = (i/2)cot πα.
- With u = e^{2πiα}: γ = −(u + 1)/(2(u − 1)). Then

  f(u) = 4(u − 1)² / [(4λ − 1)(u − r)(u − 1/r)],   r = (2√λ − 1)/(2√λ + 1) ∈ [0, 1).

  The poles in α sit at ±i s with r = e^{−2πs}.
- **Fourier coefficients:** c₀ = A and c_{±m} = B r^{m} (m ≥ 1), with Br ≡ B·r finite as r → 0. At r = 0: A = 2 and Br = −1,
  i.e. f = 2 − u − 1/u = 4 sin²πα. h has antisymmetric coefficients ±C r^{m}.
- **Residue growth:** the residue of f at α = i s grows like 1/r. Near the pole, λ − γ² ≈ −2√λ γ′(is)(α − is), with
  γ′(is) = (iπ/2)/sinh²(πs) ∝ r. So the pole recedes to Im α → ∞ while its strength grows. This is the origin of every
  non-uniformity below.

## 2. Single-factor average at integer n, and its continuation
(1/n) Σ_{k=0}^{n−1} f(k/n) = Σ_j c_{jn} = A + 2B rⁿ/(1 − rⁿ) = A + 2 Br · r^{n−1}/(1 − rⁿ).   (E1)

- **Fixed r ∈ (0, 1):** the right side is entire in n, bounded on Re n ≥ 1 and of type 0 along i·ℝ. It is therefore the
  unique Carlson continuation of the integer data.
- Its n-derivative at n = 1 is exact and finite:

  ∂ₙ I_f |_{n=1} = 2 Br · ln r / (1 − r)².   (E2)

  The code's `dIf` already has this form.
- **E2 is continuous on (0, 1) and has only an integrable logarithmic singularity at r → 0.** No threshold is needed for
  any r > 0.
- **Exactly r = 0** (λ = ¼; f a trigonometric polynomial): the integer data of (E1) are {A + 2Br at n = 1, A for n ≥ 2}.
  - This sequence has no continuation of type < π. If h interpolated δ_{n,1}, then (n − 1)h(n) would vanish on all
    positive integers with type < π, so by Carlson h ≡ 0, a contradiction.
  - The r → 0 limit of the fixed-r continuation does not exist either: E2 diverges as 2Br·ln r.
  - **So r → 0 and n → 1 do not commute. A per-mode threshold that sends small r to the r = 0 branch replaces a valid
    type-0 term with a non-continuable Kronecker datum.**
  - The error it makes is Σ_{modes with r<ε} weight × 2Br ln r/(1 − r)² (plus the pair analogues below). That is O(ln ε)
    unless the weights vanish. This explains the T46d threshold sensitivity measured in the T46d grade (`t46d_e.txt`):
    T0 moves by +0.067 at z = 4 when the threshold moves 10⁻¹⁰ → 10⁻⁸.

## 3. Pair averages (the objects that enter B)
- For factors φ₁ (coefficients a_m) and φ₂(β − α) (coefficients b_m wᵐ u^{−m}, w = e^{2πiβ}):

  P_n(β) = (1/n) Σ_k φ₁(k/n) φ₂(β − k/n) = Σ_{m₁ ≡ m₂ (mod n)} a_{m₁} b_{m₂} w^{m₂}.

- For r₁, r₂ > 0 every term is geometric in r₁ⁿ and r₂ⁿ (including the confluent r₁ = r₂ and the n·aⁿ structures). The
  closed form, i.e. the anchored-residue continuation, is the type-0 Carlson continuation **at fixed r₁, r₂**.
- **The G₀ cross term is where the singular piece lives.** In the pair sum, factor 2's zeroth harmonic (the α-average Ḡ₂,
  including G₀) multiplies factor 1's harmonics m₁ ≡ 0 (mod n). That reproduces (E1) for mode 1 with weight
  (spatial f-part of mode 1) ∘ Ḡ₂.
  - So the ln r₁ singularity of (E2) enters T1 = Tr(B1⁻¹ ∂ₙB⁽⁰⁾) through the G₀∘dG and dG∘G₀ terms. The analogous
    pieces of the dG∘dG terms are geometric in r₁r₂ and r₁^{n−1} times f₂ evaluated at large |Im α|.
  - That last factor → 1/(λ₂ − ¼) as Im α → ∞, which is also unbounded for λ₂ → ¼. Products of two near-¼ modes can
    therefore carry 1/r-type tail terms that cancel only between the factor-1 and factor-2 tails taken **together, at the
    same r's**.
  - A per-mode threshold that treats one partner as r = 0 and the other as r > 0 breaks that cancellation. That is a
    second mechanism for threshold sensitivity, and for NaN when the threshold is small, as at 10⁻¹².

## 4. The prescription (answer to the Bridge's request)
**(P1) Limit order: n → 1 at fixed r for every mode. There is no r → 0 limit and no threshold.**
- Q(n) is defined for the actual operator, whose cut modes all have r > 0 unless the problem has an exact gauge
  degeneracy.
- Carlson uniqueness holds at fixed r (type 0), so the continuation, and hence Q′(1), is the fixed-r formula:
  - (E2) for single factors;
  - its pair analogues (the T46c/T46d closed forms, with the tail loops kept for every r > 0).
- r → 0 is a property of the spectrum (UV loop momenta, or links that decouple), not a limit to take per mode.

**(P2) Compute λ − ¼ without cancellation**, so r is accurate even when λ − ¼ is below the float64 resolution of λ:

  S − ¼I = M₋^{½} [ ½(G_s − G_a) − G_s G_a ] M₋^{−½},

  because M₊M₋ − ¼ = (½ + G_s)(½ − G_a) − ¼ = ½(G_s − G_a) − G_s G_a.
- G_s − G_a is the cross-cut block (G_tb + G_bt), formed directly from G's off-diagonal entries without subtraction.
- Then use r = (2√λ − 1)/(2√λ + 1) = (4λ − 1)/(2√λ + 1)², with 4λ − 1 = 4(λ − ¼) taken from the stable eigenvalues. The
  form (2√λ − 1)/(2√λ + 1) itself cancels catastrophically for λ → ¼ and must not be used.
- Modes whose stable λ − ¼ is still at round-off (or negative) must be reported. Their contribution's sensitivity to
  r ∈ [r_floor/10, 10·r_floor] must be shown negligible; otherwise the geometry's T0 is not resolved.
  - **This is an honest failure mode, not a threshold.**

**(P3) Exact r = 0 (gauge degeneracy).**
- If λ = ¼ exactly for a symmetry reason (closed cocycle / pure gauge), the integer data are n-independent in total.
- By continuity of the exact answer under a small symmetry-breaking perturbation, the ln r coefficients of (E2) and
  §3 must cancel in the sum over modes. The total ∂ₙ contribution is then 0, which is what the pure gauge requires.
- **Test:** perturb the closed cocycle so that its modes acquire small r > 0 (weaken one twisted link by 1 − δ). The
  fixed-r formula must give a Q′(1) that is continuous as δ → 0 and tends to 0. The threshold formula must jump.

## 5. Consequences and predictions (to grade T46e against)
1. A correct T46e treatment has **no threshold anywhere**. It keeps every pole tail for r > 0 and computes λ − ¼ in a
   cancellation-free way, or proves the near-¼ modes' contribution negligible by a sensitivity bound. It reports which
   modes are at round-off.
2. **T0 must be independent of any cutoff** placed below the round-off floor of r. The T46d threshold is not that kind
   of cutoff: 219 of 656 modes sit at 0 < r ≤ 10⁻⁸ in the T46d grade configuration.
3. The pure gauge must stay exactly 0 under P1–P3, **and its perturbed version must be continuous in δ.** A threshold
   formula fails the perturbed test.
4. **On the verified T40 stand-in** (P4′/P5 lattice, Q′(1) = −1.38687; EXP-078):
   - P1–P2 must reproduce −1.38687.
   - A variant with small-r modes (e.g. an added weakly-coupled cut link, or a heavy slice) must keep agreeing with the
     honest-integer Carlson interpolant.
   - The threshold formula must fail on that variant once r of some mode falls below its threshold.
5. **Expected size:** the UV tail of near-¼ modes (large loop momentum q) contributes a z-independent level shift to T0.
   T46d's −0.075 between Q_max 16 and 48 is an instance of this.
   - It cancels in κ only if it is z-independent. Any z-dependent remainder after P1–P2 is the real T0 slope question.

## 6. Numerical checks planned after sealing (recorded separately in report.md)
- **(a) Identity E1** at integer n for r ∈ {10⁻², 10⁻⁶, 10⁻¹², 10⁻²⁰}, against direct α-sums at 50 digits.
- **(b) T46d engine** with P1 + P2 (the scratch-modified solve_q: stable λ − ¼; tails kept for all r > 0) vs the
  threshold versions at the T46d-grade configuration. T0 must not depend on any cutoff below the floor.
- **(c) Perturbed pure gauge (P3):** continuity in δ.
