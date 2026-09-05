# The general entropic constraints on the corner function do not localise κ/C_T

> ## ✅ INDEPENDENTLY VERIFIED — `../quantum`, commit `dbd443a`, 2026-09-05
>
> **All three load-bearing checks PASS. The result stands.** Verified by the sibling repo that owns
> the corner-coefficient machinery, working from this file rather than from the author's summary.
>
>     C3 reduction     RE-DERIVED from scratch, not read. a_L = eps^2/(pi^2-eps^2) gives exactly
>                      (pi^2+3eps^2) sin eps >= eps(pi^2-eps^2). Checked on 4e5 points: sign(CHL)
>                      = sign(f) everywhere, equality only at endpoints, f/eps^3 -> 4 - pi^2/6 to
>                      six digits, cubic bound alone reaches 2.1703 -- so the SECOND SUBINTERVAL
>                      IS GENUINELY NEEDED
>     admissibility    sigma = pi^2/24 and kappa = pi^5/48 confirmed. C4 Hankel determinants
>                      positive at four angles, and a DELIBERATELY CORRUPTED moment sequence goes
>                      negative -- so the C4 test is not vacuous
>     convexity        verified structurally AND the truncated family verified independently
>                      rather than on the lemma: min CHL >= 0 at u = 0, 0.5, 2, 5, 20, 50;
>                      kappa/C_T reaches 8.4e64 at u = 50
>
> **TWO DOCUMENTATION ERRORS FOUND, NEITHER LOAD-BEARING.** Both are annotated in place below:
> Lemma 2(i)'s claim that `a_min ∈ 𝒞` (it has κ = 0, C6 needs κ > 0), and the blanket
> "C1, C2, C4, C6 hold for every ρ ≥ 0" (**false for C6**). *The proof uses neither.*
>
> **THE MECHANISM, SHARPENED BY THE VERIFIER AND BETTER THAN THE ORIGINAL STATEMENT.** Not merely
> "positivity is blind to tails" —
>
> > **C6 constrains only the θ → 0 LIMIT, so it says nothing about WHERE the asymptotic regime
> > begins.** Pushing the cutoff u → ∞ holds the tail amplitude fixed while the mass goes to zero;
> > for `a_u` the κ/θ behaviour is only visible for θ ≲ 1/u. **That is a genuine looseness in an
> > asymptotic condition, not a trick.**
>
> **WHAT REMAINS UNCHECKED, AND IT IS THE LOAD-BEARING PART.** Whether C1–C6 is the *complete* set
> of known constraints is a **literature claim, not a mathematical one**, and was not swept. *The
> theorem is exactly as strong as that completeness.*
>
> ### But it is narrower than it looks — `../quantum` `e484518`
>
> **NOT a sweep. An enumeration from domain knowledge at a May 2026 cutoff, labelled as such**, of
> the families a general constraint on a(θ) could come from:
>
>     vacuum purity                  -> C1          SSA              -> C2
>     SSA + Lorentz                  -> C3          smooth limit     -> C5
>     reflection positivity, any order -> C4, and covered by the Corollary
>     sharp limit                    -> C6
>
> **And the ones that are NOT in C1–C6 turn out not to be statements about a(θ) at all:** the
> entropic c-theorem constrains RG flow *between* CFTs rather than a(θ) within one; ANEC and
> conformal-collider bounds constrain ratios of central charges with no known corner statement; the
> numerical bootstrap bounds `C_T` itself, not `a(θ)/C_T`; holographic positivity is theory-specific.
>
> **TWO PLACES A MISSING CONSTRAINT COULD PLAUSIBLY HIDE. A sweep should start here.**
>
> **1. A bound relating the thin-strip / cusp coefficient to C_T.** *As θ → 0 the wedge becomes a
> strip and κ is tied to the strip entanglement coefficient; a general inequality bounding that by
> C_T would bound κ directly.* **No rigorous one is known to the verifier; what exists in that area is
> conjectural.** *Most direct route — and a **negative** result there would substantially **strengthen**
> the theorem rather than weaken it.*
>
> **2. An inequality linking the Rényi tower across n — and this is the structurally interesting one.**
> `a_n` is computable at **integer n, where C4 is a THEOREM rather than a conjecture.** Anything
> connecting `κ_n` to `κ_1` would import real information into n = 1 —
>
> > **and crucially it would NOT be a consequence of ρ ≥ 0 at n = 1, so it is the one route that
> > survives the Corollary by construction.**
>
> *The verifier's own words: "if a bound on κ exists at all, my guess is it lives here" — **labelled a
> guess**, and the enumeration above labelled domain knowledge rather than a search.*
>
> **AND ONE REFRAME WORTH MORE THAN IT LOOKS:** C4 being conjectural at n = 1 is **CONSERVATIVE, not
> threatening.** *If C4 failed, 𝒞 would be LARGER and the supremum no less infinite.* "A conjectural
> constraint" reads like a weakness; here it is the opposite.

*Standalone statement of the result of this workspace. Self-contained; the lab notebook is `report.md`
(entries EXP-001 to EXP-013), the verified bibliography is `references.md`, the checking scripts are
under `scripts/`. Written 2026-09-05 and consolidated the same day after EXP-011; §10 is the handover.*

## 0. Statement and scope

**Statement.** Let a(θ) be the universal corner coefficient of the entanglement entropy of a
(2+1)-dimensional conformal field theory, σ = π²C_T/24 its smooth-limit coefficient, and κ its
sharp-limit coefficient (definitions in §1). Let 𝒞 be the set of functions satisfying every general
constraint known to hold for a(θ) in a unitary CFT (the six conditions C1–C6 of §2). Then for every
angle θ ∈ (0, π), sup_{a∈𝒞} a(θ)/C_T = ∞, and κ/C_T takes every value in (0, ∞) on 𝒞. In particular
the observed band κ/C_T ∈ [3.672, 4.179] spanned by all theories computed to date is not a
consequence of C1–C6, and no inequality that is itself a consequence of reflection positivity can
ever bound κ.

**Scope, stated once and meant throughout.** "Admissible" means *satisfies C1–C6*. It does not mean
"is the corner function of a unitary 3d CFT": one of the two endpoint functions in the proof is the
corner function of a z = 2 Lifshitz theory, which is not Lorentz invariant, and no CFT with a large
κ/C_T is claimed to exist. The valid conclusion is the narrower and stronger one: **the constraint
set does not localise κ, so the physical band is not explained by the constraints.** This answers,
in the negative, a question posed in [BWK16] §IX (quoted in §8). Why the constraints are blind to κ — and why
the d = 2 analogue is not — is explained in §6, with the explanation's proved and unproved parts separated.

**Mechanism in one sentence.** In the spectral representation implied by reflection positivity,
σ is the total mass of a positive measure and κ is the coefficient of its exponential tail; every
constraint except one is a positivity condition, positivity is blind to tails, and the one remaining
inequality rewards tails. A bound would need a growth condition at the tail end; the only known
sources of such conditions are an inverted-channel expansion whose lowest state is universal (the
Cardy/crossing mechanism) and locality/anomalies fixing local coefficients; §6 shows why neither
reaches κ in d = 3, and states carefully what is proved and what is a classification.

**Update after Phase 2 (EXP-013).** §6's own falsifier fired: a third bridge exists. The rectangle of
twist lines has a self-dual crossing in which κ_n is the vacuum energy of both channels and the four
corners carry a_n(π/2); it yields κ_n ≥ (2π/3) a_n(π/2) and, with a(π/2) ≥ 𝔞_min(π/2), κ/C_T ≥ 2.39
[LMW26, assuming their bound persists at n → 1]. It is one-sided: the pure-Casimir solution
𝒟 = e^{ε₀(y+1/y)} satisfies every constraint used and has a(π/2)/κ = 0. So the theorem below stands,
and the rigorous range becomes κ/C_T ∈ [2.39, ∞) against the observed [3.67, 4.18].

## 1. Setting and notation

For a region with a sharp corner of opening angle θ in the ground state of a 3d CFT,
S = B·(perimeter/δ) − a(θ) log(perimeter/δ) + O(1) [CH07, HT07]. a(θ) is universal. Its two limits:

    a(θ → π) = σ (π−θ)² + σ′ (π−θ)⁴ + …,      σ = π²C_T/24  (theorem, [FLP16]; conjectured [BMW15])
    a(θ → 0) = κ/θ + …                          (sharp limit, [CH07])

with C_T the stress-tensor two-point normalisation in the convention of [BMW15] (C_T = 3/(32π²)
per real scalar, 3/(16π²) per Dirac fermion). We write ε ≡ π − θ throughout.

Measured values of κ/C_T (all verified against their sources in `report.md` EXP-001):
real scalar 4.179 [CH07, CHL09]; Dirac fermion 3.8005 [CHL09]; Einstein holography
π²Γ(3/4)⁴/6 = 3.709 [HT07, BM15]; every quadratic/f(R) holographic model identical to Einstein
[BM15]; Einsteinian cubic gravity between 3.672 and 3.747 over its allowed coupling range [BCV21].
With σ/C_T fixed by theorem and the shape fixed by (σ, κ) to ≈1% [BMW15b, HHCWM16, BCV21], the
"collapse" of a(θ)/C_T across theories is, to that precision, the statement that κ/C_T lies in a 13%
band. The question is why. This document shows the question cannot be answered by the constraints
in §2.

Two auxiliary functions are used:

    𝔞_min(θ) = (π²C_T/3) log[1/sin(θ/2)]          [BWK16, eq. II.2]
    a_L(θ)   = (θ−π)²/(θ(2π−θ)) = ε²/(π²−ε²)       [Lifshitz shape; BWK16 §VII, BCV21 eq. 260]

## 2. The constraint set 𝒞

For a function a on (0, 2π):

- **C1** reflection a(2π−θ) = a(θ) (purity of the vacuum) [CH07].
- **C2** a ≥ 0, a′ ≤ 0, a″ ≥ 0 on (0, π) (strong subadditivity) [HT07, eq. 3.1].
- **C3** a″(θ) + a′(θ)/sin θ ≥ 0 (strong subadditivity with Lorentz invariance) [CHL09; BWK16 eq. II.1].
  We write CHL[a] for the left-hand side.
- **C4** det{∂_θ^{j+k+2} a(θ)}_{j,k=0}^{M−1} ≥ 0 for all M ≥ 1 and all θ (reflection positivity /
  conditional positivity of the entropy correlation matrices) [CH12]; derived for integer Rényi
  index, conjectural at n = 1, assumed at n = 1 in [BWK16].
- **C5** a is analytic at θ = π with only even powers of ε, and a = σε² + O(ε⁴) with σ = π²C_T/24.
- **C6** a ~ κ/θ as θ → 0 for some κ > 0.

Every bound on a(θ) at n = 1 in the literature ([HT07], [CHL09], [BWK16], [HHCWM16]) is derived from
a subset of C1–C5. No other general constraint is known (prior-art sweep, `report.md` EXP-001 R2).

## 3. Spectral form of the constraints

If a is analytic, C4 says that at each θ the sequence ∂_θ^{k+2} a(θ), k ≥ 0, is a Hamburger moment
sequence. By Bernstein–Widder (exponential convexity), a″ is then a Laplace transform of a positive
measure; symmetrising with C1,

    a″(θ) = ∫₀^∞ dρ(s) cosh(sε),   ρ ≥ 0,      a(θ) = ∫₀^∞ dρ(s) [cosh(sε) − 1]/s²,          (3.1)

using a(π) = a′(π) = 0. Consequences:

- the smooth-limit coefficients are moments: σ^{(p−1)} = M_{2p−2}/(2p)!, M_k ≡ ∫ s^k dρ; in particular
  **C5 is the mass condition M₀ = 2σ = π²C_T/12**;
- **C6 is a tail condition**: a ~ κ/θ ⟺ ρ(s) ~ 2κ s² e^{−πs} as s → ∞ (this reproduces the
  smooth–sharp asymptotics σ^{(p)} → 2κ/π^{2p+3} of [BWK16]);
- ~~C1, C2, C4, C6 hold for every ρ ≥ 0;~~ **FALSE FOR C6** — see the verification note at the top
  of this file. C1, C2 and C4 hold for every ρ ≥ 0; **C6 does not.** It requires the tail
  ρ ~ 2κ s²e^{−πs}, which the families used here have and a generic positive measure does not.
  *Counterexample (verified independently): ρ = 1 on [0.1, 1] gives a(θ→0) = 6.0966, finite, so
  κ = 0.* **The proof never uses the blanket statement, so nothing downstream changes.**
- **C3 is the single linear inequality**

      CHL[a](ε) = ∫₀^∞ dρ(s) K(s, ε) ≥ 0,     K(s, ε) ≡ cosh(sε) − sinh(sε)/(s sin ε).            (3.2)

Three closed-form densities (all σ-normalised, units of C_T): ρ_min(s) = (π²/3) s/sinh(πs) for 𝔞_min
(derived from −log cos(ε/2) = Σ_p (2^{2p}−1)|B_{2p}|(ε/2)^{2p}/(p(2p)!) and
(2^{2p}−1)ζ(2p)/2^{2p} = Σ_{m odd} m^{−2p}); ρ_L ∝ s² e^{−πs} for a_L (its Laplace transform is exactly
1/θ + 1/(2π−θ) − 2/π = (2/π)(π−θ)²/(θ(2π−θ))); and ρ_EMI ∝ s²/sinh²(πs/2) for the extensive-mutual-
information shape 1 + (π−θ)cot θ [BMW15 eq. 14] (not a CFT, [ABC21]).

## 4. Two lemmas and the theorem

**Lemma 1 (the kernel has exactly one sign change).** For fixed ε ∈ (0, π), K(s,ε) ≥ 0 ⟺
tanh(sε)/s ≤ sin ε. The map s ↦ tanh(sε)/s is strictly decreasing on (0, ∞), from ε to 0, because its
derivative has the sign of sε sech²(sε) − tanh(sε) = (y − sinh y cosh y)/cosh² y < 0 for y = sε > 0.
Since sin ε < ε, there is exactly one s*(ε) > 0 with K < 0 on (0, s*) and K > 0 on (s*, ∞). ∎

*Reading:* C3 penalises spectral weight at small s and rewards weight at large s.

**Lemma 2 (two admissible functions).** *[Verification note: **2(i) as stated is wrong** — `a_min`
has κ = 0 while **C6 requires κ > 0**, so it is not in 𝒞 except "in the limiting sense" the text
concedes. **It is not needed:** the theorem runs over λ ∈ (0,1] and states its conclusion on the
OPEN interval, and `a_λ` is in 𝒞 directly because ρ_λ ≥ 0 and κ_λ = λκ_L > 0. Cosmetic.]*
(i) 𝔞_min ∈ 𝒞 with κ = 0. C3 holds with equality [BWK16, App. A.1]; C1, C2, C5 are explicit; C4 holds
because ρ_min > 0; C6 holds in the limiting sense (logarithmic divergence, κ = 0).
(ii) â_L ≡ (π⁴C_T/24) a_L ∈ 𝒞 with κ/C_T = π⁵/48 = 6.375. C1, C2, C5, C6 are explicit from
â_L = (π²C_T/24) π²ε²/(π²−ε²); C4 holds because ρ_L > 0; C3: with ∂_ε a_L = 2π²ε/(π²−ε²)² and
∂_ε² a_L = 2π²(π²+3ε²)/(π²−ε²)³, and ∂_θ = −∂_ε, sin θ = sin ε, the inequality CHL[a_L] ≥ 0 is
equivalent to

      f(ε) ≡ (π² + 3ε²) sin ε − ε (π² − ε²) ≥ 0   on [0, π].                                      (4.1)

Proof of (4.1). Both sides of the inequality vanish at ε = 0 and ε = π. For ε ∈ [0, 2.17]: using
sin x ≥ x − x³/6 (x ≥ 0), f/ε ≥ (π²+3ε²)(1 − ε²/6) − (π² − ε²) = ε²[(4 − π²/6) − ε²/2] ≥ 0 since
4 − π²/6 = 2.355 ≥ ε²/2 for ε² ≤ 4.71. For ε = π − t with t ∈ [0, 0.97]: sin ε = sin t ≥ t(1 − t²/6)
≥ 0.843 t, so f ≥ (π² + 3(2.17)²)(0.843 t) − t(π−t)(2π−t) ≥ 20.2 t − 19.74 t ≥ 0, using
(π−t)(2π−t) ≤ 2π² = 19.74. ∎ (Checked numerically on 2·10⁵ points: min f = 2·10⁻¹⁸ at the endpoints.)
[BWK16] §VII state the same admissibility of the Lifshitz corner function.

**Theorem (no localisation of κ).**
(a) *Convexity.* C2, C3, C4, C6 are positivity or linear conditions and C5 is affine, so
𝒞 ∩ {σ fixed} is convex and κ is linear along segments. Hence a_λ ≡ (1−λ)𝔞_min + λ â_L ∈ 𝒞 for
λ ∈ [0, 1], with κ_λ/C_T = 6.375 λ: **every κ/C_T ∈ (0, 6.375] is admissible.** The band
[3.672, 4.179] is strictly inside.
(b) *Unboundedness.* For u ≥ 0 let ρ_u(s) ≡ 2κ s² e^{−πs} Θ(s − u), whose transform is

      a_u(θ) = κ [ e^{−uθ}/θ + e^{−u(2π−θ)}/(2π−θ) − 2e^{−uπ}/π ].                                (4.2)

Its sharp coefficient is κ for every u (the e^{−uθ}/θ term), while its mass is
2σ_u = 2κ e^{−πu}(u²/π + 2u/π² + 2/π³) → 0 as u → ∞. C1, C2, C4, C6 hold because ρ_u ≥ 0. For C3,
fix ε and let s*(ε) be as in Lemma 1. Either u ≥ s*(ε), and then CHL[a_u](ε) = ∫_u^∞ ρ_L K ≥ 0
because K ≥ 0 on [u, ∞); or u < s*(ε), and then
CHL[a_u](ε) = CHL[a_L](ε) − ∫₀^u ρ_L K ≥ CHL[a_L](ε) ≥ 0 because K ≤ 0 on [0, u] and CHL[a_L] ≥ 0 by
Lemma 2(ii). Rescaling a_u by 2σ/(2σ_u) to satisfy C5 gives an admissible function with
κ/C_T = (π²/24)(κ/σ_u) → ∞. ∎
(c) *Pointwise.* For any fixed θ ∈ (0, π), the rescaled a_u(θ)/C_T ∝ e^{πu} e^{−uθ}/θ → ∞, so no
upper bound on a(θ)/C_T at any angle follows from C1–C6; likewise σ′/σ = M₂/(12 M₀) ~ u²/12 → ∞, so
none follows for the expansion coefficients either.

Numerical check of (b) (`scripts/exp003_spectral.py`, output frozen in `scripts/exp003_output.txt`):
the family with (1−λ)𝔞_min added passes C1–C6 at 40 angles for κ/C_T = 0.004, 3, 10, 100, 10⁴, 10⁶;
the moment positivity of the real coefficient sequences (Einstein, 6 exact coefficients [BWK16 eq.
V.6]; complex scalar, 8; Dirac, 7 [HHCWM16 Tables 3–4]) passes and a deliberately corrupted sequence
fails, so the C4 test is not vacuous. The numerics are a check, not part of the proof.

**Corollary.** Any inequality that is a consequence of ρ ≥ 0 — every reflection-positivity-type
inequality for a(θ) at n = 1, of any order — cannot bound κ or a(θ) from above. A bound must be a
constraint that some positive ρ violates, i.e. it must carry information not contained in the
entropic inequalities of the corner function.

## 5. What a bound would have to use

| structure | what it gives | can it bound κ? |
|---|---|---|
| Strong subadditivity, all configurations | log-coefficient inequalities arise only when area terms cancel (overlapping sectors); the smallest angle always sits on the lower-bound side (convexity, C3) | no (lower bounds only) |
| Reflection positivity, any order | C4, i.e. ρ ≥ 0 | no (Corollary) |
| Rényi tower a_n, n ≥ 2 | each a_n satisfies its own C1–C4 with h_n for C_T [BWK16 eq. II.8]; no inequality links κ_n across n | no |
| Strip / mutual-information reading | κ_n = short-distance coefficient of I_n of two half-planes = −E_Cas(n)/(n−1) of the twist line and its reversal; reflection positivity of the slab gives E_Cas ≤ 0 | κ_n ≥ 0 only |
| Modular theory (Bisognano–Wichmann, relative entropy, QNEC) | second-order shape variations (the σ theorem) | no (κ is all orders; it sits at the boundary of convergence of the ε-expansion) |
| Stress-tensor 2-/3-point data (C_T, t₄) | see `report.md` EXP-002: two theories with equal t₄ differ in κ/C_T by 11.5% | no |
| An inverted-channel positive expansion with a universal lowest state | would fix κ from universal data (the Cardy/crossing mechanism) | absent for the two-ball function in d ≥ 3; the strip's inverted channel lands on a non-universal Casimir energy, §6 |
| A *self-dual* crossing with κ as the vacuum energy of both channels (the rectangle of twist lines) [LMW26] | κ_n ≥ (2π/3)a_n(π/2); κ/C_T ≥ 2.39 at n → 1 | lower bound only: 𝒟 = e^{ε₀(y+1/y)} is admissible with a(π/2)/κ = 0 (EXP-013) |

The named obstruction: **κ is a non-perturbative fusion datum of the twist defect, and no entropic
inequality or finite-order correlator bound reaches it.**

## 6. Why the analogous d = 2 problem is bounded and the d = 3 problem is not

*Status of this section.* First written as a causal explanation; then attacked with pre-registered
falsifiers (`report.md` EXP-009). The topological fact survived; the causal claim survived only in the
narrower form stated here. The naive version — "no limit-exchanging symmetry exists in d ≥ 3" — is
false and is not claimed.

*The Cardy mechanism, stated so it can fail.* Modular invariance Z(β) = Z(4π²/β) fixes the high-energy
density of states in terms of the vacuum. Two ingredients: (i) a positive expansion, and (ii) a second
positive expansion with inversely related parameter **whose lowest state is universal** (the vacuum,
with an anomaly-fixed Casimir energy in 2d; the identity operator in an OPE channel). Ingredient (ii)
is what turns a tail into a mass; positivity alone cannot (§4, and [TWZ21], [CV21] for the analogous
statement in EFT positivity: linear positivity gives one-sided bounds, full crossing gives two-sided).
For two intervals in a 2d CFT, F_n(x) = F_n(1−x) [CCT09: "It is also invariant under x → 1−x", and
"by symmetry x → 1−x also for x close to 1, corresponding to close intervals"], because the complement
of two intervals on the circle is two intervals; the crossed channel's lowest state is the identity,
so the short-distance coefficient is fixed by c.

*What d ≥ 3 has and lacks.* Two limit-exchanging structures do exist in d ≥ 3, and one contains κ:
- Two parallel twist lines (the strip): quantising along the lines gives an open channel
  Q = Tr e^{−ℓH(w)}, positive in e^{−ℓ}, whose ground-state energy is E₀(w) = −(n−1)κ_n/w. So κ_n is
  a mass — the Casimir energy of two twist points on the plane — in the other channel.
- The torus: exchanging cycles gives c_S = d·c_vac exactly [Sha16].
Neither fixes κ, because the mass at the other end is itself non-universal: in odd d there is no
conformal anomaly, and Casimir energies of flat and defect geometries are non-local numbers. *But
"non-universal" is not "useless" (correction, EXP-013):* when the geometry is self-dual — a rectangle
of twist lines, whose x ↔ y symmetry is a modular relation — the same non-universal κ_n sits at the
bottom of both channels while the corners bring a_n(π/2) into the equation, and OS positivity then
yields the inequality κ_n ≥ (2π/3)a_n(π/2) [LMW26]. In d = 2 the same crossing is an equality (corner
c/16, strip πc/24: Cardy). In d = 3 it is one-sided; see the update in §0 and EXP-013. The
d = 3 values c_S/C_T = 60.4 (real scalar), 48.3 (N = ∞ Wilson–Fisher, from c̃/N = 4/5 [Sac93]), 12πζ(3) = 45.32
(Dirac), 4π⁵/27 = 45.34 (Einstein) show the spread that remains despite the exact torus relation. (The
Dirac–Einstein agreement at 4.4·10⁻⁴ is the n → 0 endpoint of a known 0.2% agreement of σ_n/C_T on
0 ≤ n ≤ 1 [BMW15b]; assessed as chance in `report.md` EXP-010.)
For the two-ball Rényi function itself, the only positive channel with a universal lowest state is
radial quantisation about the common centre (identity at the far end, η → 0), and no conformal map
sends the touching end (η → 1) onto it: two disjoint disks are conformally a disk plus the exterior of
a concentric disk [NN15, AM26], their complement is the annulus between them, and purity only reverses
the orientation of the same two circles. In d = 2 the four endpoints of two intervals re-pair; in
d ≥ 3 a ball's entangling surface is connected and the complement of two balls in S^d is a shell, for
every d ≥ 3.

*What is proved and what is not.* Proved: (N1) positivity plus mass-dominated constraints cannot bound
a singular-end coefficient (§4); (N2) in d = 2 the x ↔ 1−x symmetry supplies the missing growth
condition through a universal crossed vacuum; (N3) the two-ball function in d ≥ 3 has no channel
relation onto a universal lowest state, and the strip's inverted channel lands on a non-universal
Casimir energy. The classification first offered here — that no *third* bridge could supply a growth condition at the
tail end — was falsified by [LMW26] (EXP-013): a self-dual crossing with a non-universal but shared
vacuum energy supplies one. What survives, now with an explicit witness: every known bridge is
one-sided at the tail. The analyticity route (Lorentzian cusps, [CGT26]) likewise yields a
positivity, not an upper bound.

*A solvable instance, read to the bottom.* For the free massless Dirac field the two-sphere Rényi
mutual information is known exactly for all n and d [AM26]; there the short-distance (strip)
coefficient is derived by "approximating the sum over the angular momentum as an integral, because
the divergence will come from the terms with large ℓ" (their eq. 4.18) and equals the 2d c-function
integral κ_d (their eq. 4.17, the Casini–Huerta formula in d = 3). Any finite set of low modes
contributes at most O(log): κ is literally the tail of the tower, with a universal polynomial density
and a mode function fixed by 2d dynamics. At n = 2 the mode function can be read to the bottom
([BMW15b] App. B, single sector a = ¼): κ₂^f = (2/π)∫₀^∞ y² u²_{1/4}(y) dy while
∫₀^∞ y u²_{1/4}(y) dy = 1/8 is the UV central charge — **κ₂ and the universal datum are the second
and first moments of the same positive Painlevé profile**, and no positivity fixes the one from the
other. The published κ₂ = 0.0472338(1) is this integral evaluated ([BMW15b] Table 3, App. B), so no
independent test of the tail identity exists or is needed. [AM26] also note that dropping the ℓ = 0
mode turns the d = 4 Dirac tower into the Rarita–Schwinger one: same κ₄, different lowest primary,
different log coefficient — Theorem (b)'s truncation realised by a pair of free fields. Details in
`report.md` EXP-008 and EXP-011.

*Consequences checked outside the construction.* The generalised Cardy relation on tori [Sha16] is the
"inverted channel ⇒ tail equals mass" prediction, exact; the non-universality of c_S/C_T is the
"non-universal mass" prediction; the even-d log coefficient of the two-sphere mutual information being
the anomaly [AM26 §4.3.2] and the absence of any universal subleading term in odd d is the "locality
fixes only local coefficients" prediction. Forward-looking and falsifiable: the free-scalar
extremality conjectures (κ/C_T ≤ 4.18; C_T/F₀ ≤ its scalar value [BFGLM26]) cannot be proved from
entropic inequalities or finite-order positivity.

*Status of novelty.* The one-sided/two-sided dichotomy is prior art in EFT positivity [TWZ21, CV21];
the torus relation is [Sha16]; the d = 2 symmetry is [CCT09]. The application to entanglement
coefficients, the open-channel reading of κ_n, the "universal lowest state" refinement, and the
complement-topology reason for its absence in the two-ball function were not found in the literature
reached here and are offered as new, with the caveats above.

## 7. Integer Rényi index: data and the same obstruction

For integer n the twist operator τ_n(∂A) is a genuine codimension-2 defect of CFT^n and C4 is not
conjectural. Free-field values (exact h_n from [BMW15b] Table 1; κ_n from [BMW15b] Table 3, quoted
there with an uncertainty of 1 in the last digit, reproduced in [BW22] Table 2; not computed here):

| n | h_n (complex scalar) | κ_n (cs) | κ_n/h_n | h_n (Dirac) | κ_n (f) | κ_n/h_n | spread |
|---|---|---|---|---|---|---|---|
| 2 | 1/(24π) = 0.013263 | 0.0455996(1) | 3.438 | 1/64 = 0.015625 | 0.0472338(1) | 3.023 | 13% |
| 3 | 1/(27√3) = 0.021383 | 0.037339(1) | 1.746 | 5/(108√3) = 0.026729 | 0.040662(1) | 1.521 | 14% |
| 4 | (3π+8)/(192π) = 0.028888 | 0.033798(1) | 1.170 | (1+6√2)/256 = 0.037052 | 0.0376674(1) | 1.017 | 14% |

The spread is no narrower at integer n than at n = 1. Fusion-channel positivity at integer n is
exact and reads: Q(d) = Z_n(A∪B)/(Z_n(A)Z_n(B)) is completely monotone in the separation d. For two
half-planes Q = e^{(n−1)κ_n ℓ/w}, which is completely monotone for every κ_n ≥ 0 (e^{c/w} =
Σ_k c^k/(k! w^k), each 1/w^k a Laplace transform of a positive density), so this gives κ_n ≥ 0 and
nothing else — the mechanism of §4 again.

*The sharp-end constant (Phase 2, EXP-012).* With a(θ) = κ/θ + a₀ + O(θ), the constant a₀ is the
sharp-end analogue of σ′: a second non-universal number, fixed by nothing in C1–C6 (it is an integral
of the non-tail part of ρ), and in the cusp language the derivative at n = 1 of the dimension of the
operator that creates the twist pair at the tip [CHK24 eq 2.12; inference for twist defects]. Measured
here: Einstein a₀ = 0 to four digits (exact curve); real scalar, n = 1: a₀ = −0.33 C_T (−0.38 … −0.27,
`scripts/exp004_eehp_result_Mcut13.1.json`, validated to ≤ 5·10⁻⁵ against [HHCWM16] from 20° to 170°);
real scalar, n = 2: −0.24 ± 0.03 C_T. The (σ, κ) trial function's own constant is
ã₀ = (3π/2)(3πσ − κ)/(π² − 6), which changes sign inside the physical band (κ/σ straddles 3π); the
residual's sign at each end of the interval is set by one number — σ′ − σ̃′ at π, a₀ − ã₀ at 0 — and
for the free scalar at n = 1 the two ends disagree, giving a node at 27 ± 3° with the exact function
above the trial function below it by ≤ 0.1%.

At n = 2 for the Dirac fermion the obstruction is explicit (§6, `report.md` EXP-011): κ₂ is the second
moment of the positive profile y u²_{1/4}(y) whose first moment, 1/8, is the UV central charge. The
same two numbers cannot be related by positivity, and the construction contains nothing else.

## 8. Relation to prior work

[BWK16] §II.1: "It is natural to ask whether the remaining infinite set of inequalities, Eq. (II.5),
will yield stronger bounds, or even an upper bound. […] With regards to the upper bounds, the answer
is simple: those inequalities all yield lower bounds." App. A.2: "We now show that all the
reflection positivity inequalities Eq. (II.5), labelled by an integer M ≥ 1, lead to lower bounds,
and never to an upper bound." §IX (Discussion): **"It is further natural to ask whether an upper
bound exists for a(θ), and its expansion coefficients. The holographic correspondence could be
helpful in answering this question."** The question is about a(θ) itself and its expansion
coefficients, in general. §4(c) answers it for the full constraint set C1–C6 (not only reflection
positivity): no upper bound on a(θ)/C_T at any angle, nor on any σ^{(p)}/C_T, follows from the general
constraints. The holographic route suggested there gave, in [Miao15] and [BCV21], that the Einstein
curve is not even a lower bound.

*Cusp literature, 2024–26 (EXP-013).* In d = 3 the corner function is the cusp anomalous dimension of
the replica twist line, Γ^{(n)} = (1−n)a_n(θ) [LMW26 eq 35; CGT26; Cha26]. [CHK24] prove Γ < 0,
Γ′ > 0, Γ″ < 0 and Γ″(π) = −C_D/6 for general line defects (C2 and σ_n ∝ C_D in that language);
[DKPW24] give the wedge/Casimir relation F = Vol(ℍ^p)ℰ/θ^p (the strip–corner identity); [KRS25] prove
the leading fusion coefficient non-negative and derive one-point-density growth *from* it; [LMW26]
bootstrap the rectangle and obtain the first lower bound on κ in terms of a(π/2). None bounds a
Casimir energy from above.

[CH12] introduced conditional positivity / infinite divisibility for the entropies and wrote, for the
holographic corner function, "if we could write g(θ) as a Laplace transform…"; the representation
(3.1) is that structure. [BWK16] §IV found the smooth–sharp asymptotics σ^{(p)} → 2κ/π^{2p+3}, which
is the tail statement in coefficient language. The mass-versus-tail reading, the explicit admissible
functions with arbitrary κ, the pointwise unboundedness of a(θ)/C_T, and the consequence for the
collapse are, as far as I could find, not in the literature.

## 9. How to check

- Lemma 1: differentiate tanh(sε)/s. Lemma 2(ii): substitute a_L = ε²/(π²−ε²) into CHL and clear
  denominators; (4.1) follows. The two-subinterval proof uses only sin x ≥ x − x³/6.
- Theorem (b): the Laplace transform of s²e^{−πs}Θ(s−u) against (cosh sε − 1)/s² is (4.2) by direct
  integration; the mass is the incomplete gamma function Γ(3, πu)/π³ up to the factor 2κ.
- `scripts/exp003_spectral.py` (numpy/scipy): evaluates C1–C6 on the family at 40 angles and the
  moment positivity of the published coefficient sequences; `scripts/exp003_output.txt` is its frozen
  output. A control that must fail (corrupted sequence) is included.
- The verbatim [BWK16] sentences are at ar5iv lines 290–295, 818–819 and 690–692 of arXiv:1511.04077;
  the [CCT09] sentences at lines 178–180 and 889–891 of arXiv:0905.2069.

- EXP-010 arithmetic: 12πζ(3) = 45.3165, 4π⁵/27 = 45.3362; π⁴/(81ζ(3)) = 1.00044; the n → 0 limits
  ζ(3)/π² and π²/81 are [BMW15b] Tables 2 and 4. EXP-011: the n = 2 sector is a = ¼ in [BMW15b]
  (B.2); swap the order of integration in (B.1)+(B.3); ω_a(0) = −2a² from Σk² = n(n²−1)/12.

## 10. Status and handover

**Settled.** (1) The prior-art sweep with two corrections to the task statement (EXP-001). (2) The
reframe: to ≈1% the collapse is the statement κ/C_T ∈ [3.672, 4.179]; the ≈1% shape residual is a
separate, open fact. (3) The t₄ obstruction: equal-t₄ theories differ in κ/C_T by up to 11.5%
(EXP-002). (4) The theorem of §4: no general entropic constraint bounds κ/C_T or a(θ)/C_T above;
analytic, with a falsifiable numerical companion. (5) What a bound must use (§5) and why d = 2 has
it and d = 3 does not, narrowed after attack (§6, EXP-007/009). (6) The solvable instance read to the
bottom (§6, EXP-008/011): κ₂ and the UV datum are different moments of one positive function.
(7) The Dirac–Einstein c_S/C_T near-coincidence is chance on a known loose pattern (EXP-010).
(8) Phase 2: the sign of the (σ, κ) trial-function residual is not universal but is set by one number
at each end — σ′ − σ̃′ at the smooth end (positive for every n = 1 theory, negative for both free fields
at n ≥ 2) and a₀ − ã₀ at the sharp end; a₀ measured for the free scalar (−0.33 C_T at n = 1, −0.24 C_T
at n = 2) and Einstein (0), with the predicted node for the n = 1 scalar found at 27 ± 3° (EXP-012). (9) Phase 2: the third bridge exists — the rectangle
crossing of [LMW26] — gives κ ≥ (2π/3)a(π/2), hence κ/C_T ≥ 2.39, and is provably one-sided (EXP-013).

**Open, in order of value.** (a) The shape residual, now reduced to two numbers per theory: why σ′
sits ≈2% below the (σ, κ) line at n = 1 and above it at n ≥ 2, and what sets the sharp-end constant
a₀ (0 for Einstein, −0.33 C_T for the free scalar at n = 1; a defect-creation dimension if the cusp
structure carries over; unmeasured for the Dirac fermion, whose solver branch is parked, EXP-012). (b) An *upper* bound on
κ: every known bridge, including the rectangle crossing, is one-sided; closing the problem needs a
constraint that excludes pure-Casimir solutions 𝒟 = e^{ε₀(y+1/y)} — dynamical input beyond OS
positivity and self-dual crossing (EXP-013). (c) The ECG t₄ sign
discrepancy between [BCV21] and [BCR18] (does not affect any conclusion here).

**For whoever picks this up.** Start from this file, then `report.md` in order; every number carries
its source key, and `references.md` says for each key what was actually read (abstract, table, full
text). Nothing here is a fit: the theorem is analytic, the two admissible functions are explicit, and
the numerics are controls that can fail. The parked instrument (`scripts/exp004_*`, a validated
double-precision and arbitrary-precision solver for the Casini–Huerta–Leitao ODE system) exists only
because no four-digit free-field a(θ) below 45° is published; resume it only if the shape residual
becomes the target, and re-run its known-answer controls first. The sibling repository's corner
numbers violate a rigorous lower bound at 120° and are recorded in `TODO.md` for the bridge, not
fixed. If you want to attack the theorem, the place to push is not the inequalities (they are all
positivity) but the scope line of §0: exhibit a *unitary CFT* constraint that some positive spectral
density violates. If you want to attack the explanation in §6, the falsifier is named there: a third
bridge that supplies a growth condition at the tail end.

## References (keys resolve in `references.md`)

[ABC21] Agón, Bueno, Casini, JHEP 08 (2021) 084 · [AM26] Abate, Martinek, arXiv:2608.23692 ·
[BCV21] Bueno, Camps, Vilar López, JHEP 04 (2021) 145 · [BM15] Bueno, Myers, JHEP 08 (2015) 068 ·
[BMW15] Bueno, Myers, Witczak-Krempa, PRL 115, 021602 (2015) · [BMW15b] id., JHEP 09 (2015) 091 ·
[BW22] Berthiere, Witczak-Krempa, PRL 128, 240502 (2022) · [BWK16] Bueno, Witczak-Krempa, PRB 93,
045131 (2016) · [Cardy13] Cardy, J. Phys. A 46 (2013) 285402 · [CCT09] Calabrese, Cardy, Tonni,
J. Stat. Mech. (2009) P11001 · [CH07] Casini, Huerta, NPB 764 (2007) 183 · [CH12] Casini, Huerta,
JHEP 11 (2012) 087 · [CHL09] Casini, Huerta, Leitao, NPB 814 (2009) 594 · [FLP16] Faulkner, Leigh,
Parrikar, JHEP 04 (2016) 088 · [HHCWM16] Helmes et al., PRB 94, 125142 (2016) · [HT07] Hirata,
Takayanagi, JHEP 0702:042 (2007) · [Miao15] Miao, JHEP 10 (2015) 038 · [NN15] Nakaguchi, Nishioka,
JHEP 04 (2015) 072 · [BCR18] Bueno, Cano, Ruipérez, JHEP 03 (2018) 150 · [BCGKM26] Bianchi, Cavaglià, Gutiérrez, Kousvos, Meineri,
arXiv:2609.04035 · [CGT26] Cuomo, Giombi, Tizzano, arXiv:2608.03704 · [Cha26] Chandra, arXiv:2608.28531 ·
[CHK24] Cuomo, He, Komargodski, JHEP 11 (2024) 061 · [DKPW24] Diatlyk, Khanchandani, Popov, Wang, arXiv:2404.05815 ·
[KRS25] Kravchuk, Radcliffe, Sinha, J. Phys. A 58 (2025) 465402 · [LMW26] Lanzetta, Moult, Wang, arXiv:2609.04041 · [BFGLM26] Bueno, Fernández García, Gentile,
Lasso Andino, Moreno, arXiv:2604.01436 · [CV21] Caron-Huot, Van Duong, JHEP 05 (2021) 280 · [Sac93] Sachdev, Phys.
Lett. B 309 (1993) 285 · [Sha16] Shaghoulian, PRD 93, 126005 (2016) · [TWZ21] Tolley, Wang, Zhou, JHEP 05 (2021) 255.
