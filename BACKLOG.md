# Backlog — ranked for moonshots

*Internal working version. The version written for other sessions and people, with stable IDs CF-1 … CF-25, shared conventions and a complementarity map, is `SHARED_BACKLOG.md`.*

*Written 2026-09-23, after a six-stream literature sweep (up to September 2026). Every item planned in
this repository's documents and never done, plus new items suggested by that sweep, scored and
ranked. The notebook is `report.md`; the result is `RESULT.md`; the working list is `TODO.md`.*

## How the ranking works

Each item gets three judgement scores. **Impact** (1–5): how much the answer would change the
problem, where 5 means it would bear directly on why the collapse happens. **Complexity** (1–5): 5
means new theory or a new instrument, weeks or more. **Chance**: the probability of a clean, reportable
answer, with a positive answer counted separately where that matters. The ranking key is the
**moonshot index = Impact × Complexity × (1 − Chance)**, so hard, unlikely, high-impact work rises to
the top, as requested. Quick wins fall to the bottom; they are listed there because several of them
are cheap first steps toward the moonshots.

Source tags: **[doc]** was planned in this repository (file named); **[new]** comes from the sweep.

## The ranking

| # | Item | Impact | Complexity | Chance | Index | Source |
|---|---|---|---|---|---|---|
| 1 | An absolute upper bound on κ/C_T | 5 | 5 | 3% | 24.3 | [doc] TODO, RESULT §10(b) |
| 2 | Why physical corner functions sit near the EMI shape (the κ band itself) | 5 | 5 | 5% | 23.8 | [doc] TODO, RESULT §10(a) |
| 3 | First von Neumann κ for an interacting CFT (Ising) | 5 | 5 | 8% | 23.0 | [new] |
| 4 | Corner entanglement on the fuzzy sphere (a "lune") | 5 | 5 | 10% | 22.5 | [new] |
| 5 | The 1/N correction to κ/C_T for large-N O(N) | 4 | 5 | 10% | 18.0 | [new] |
| 6 | Test the non-analytic θ^{2η} small-angle term at Ising/O(N) | 4 | 5 | 10% | 18.0 | [new] |
| 7 | Numerical bootstrap of the n = 2 replica twist line in 3d Ising | 4 | 5 | 10% | 18.0 | [new] |
| 8 | A non-perturbative or top-down holographic corner function | 4 | 5 | 15% | 17.0 | [new] |
| 9 | Prove the rectangle bound, or conformal concavity, survives n → 1 | 4 | 4 | 20% | 12.8 | [doc] TODO; [new] |
| 10 | What orders κ/C_T across theories (t₄ does not) | 3 | 4 | 10% | 10.8 | [doc] TODO |
| 11 | Prove reflection positivity (C4) at n = 1 for the corner function | 3 | 4 | 15% | 10.2 | [doc] TODO caveats |
| 12 | A second instrument for the free-field sub-45° values | 3 | 4 | 35% | 7.8 | [doc] TODO |
| 13 | An independent analytic a₀ for the free scalar, including any log θ | 3 | 4 | 40% | 7.2 | [doc] TODO |
| 14 | Derive the smooth-end sign rule of the shape residual | 2 | 4 | 15% | 6.8 | [doc] TODO |
| 15 | A thermal handle on κ: the n → 0 limit of κ_n | 3 | 3 | 25% | 6.8 | [new] |
| 16 | Closed form of the Painlevé integral for κ₂ (Dirac) | 1 | 4 | 20% | 3.2 | [doc] TODO parked |
| 17 | Is Ising's Rényi-2 corner function a constant multiple of the free one? | 3 | 2 | 60% | 2.4 | [new] |
| 18 | Scalar entanglement run at M ≥ 14 and beyond, to reach 5°–10° | 2 | 2 | 70% | 1.2 | [doc] TODO |
| 19 | Cubic-gravity scan of κ/C_T over the t₄-allowed couplings | 2 | 1 | 95% | 0.1 | [new] |
| 20 | Fix the singular starting solve at large t | 1 | 2 | 80% | 0.4 | [doc] TODO |
| 21 | Log-convexity in d of the free-field κ_d | 1 | 2 | 80% | 0.4 | [doc] TODO parked |
| 22 | Test the new cusp-paper inequalities on this repository's data — **done, EXP-022** | 3 | 1 | 90% | 0.3 | [new] |
| 23 | κ/F₀ normalisation audit, and the κ/F₀ ≤ 0.622 conjecture | 2 | 1 | 90% | 0.2 | [new] |
| 24 | Check the cuboid bootstrap's closure under Casimir dressing — **done, EXP-023: closed, also for κ** | 2 | 1 | 90% | 0.2 | [new] |
| 25 | The ECG t₄ sign discrepancy | 1 | 1 | 90% | 0.1 | [doc] TODO |

Merged, not listed separately: the twist-defect crossing at integer n (report EXP-005) and the
one-point-growth route (EXP-006/008) are sub-routes of #1, since both are now known to give lower
bounds only. "Attack Phase 1's scope line" (PHASE2.md) is #1 from the other side: its lower half is
done by [LMW26]'s rectangle bound, which already excludes the 𝔞_min function.

## The items

**1. An absolute upper bound on κ/C_T.** The problem's closing move. Every positivity mechanism
known — strong subadditivity, reflection positivity, the rectangle and the cuboid, conformal concavity,
fusion-EFT positivity, Rindler positivity — bounds κ from below. The rectangle is closed under Casimir
dressing (EXP-017, apparently new: the sweep found it listed as an open task elsewhere). A research
agent's algebra suggests the cuboid is closed too (#24 checks it). What would be needed is a constraint
in which κ enters other than as a multiplicative factor. The only upper-type inequality found is
[LMW26b] eq. (37), which relates κ to the O(θ) coefficient, not to C_T.

**2. Why corner functions sit near the EMI shape.** This is the original question, reduced. The
trial function is the EMI shape plus a small Lifshitz admixture (EXP-016). The deviation from EMI is
(~~exactly the tripartite information [ABC21b]~~: corrected 2026-09-24, EXP-026; [ABC21b] contains no corner identity; only EMI ⇔ I₃ ≡ 0 [ABC21] is sourced), so the concrete question is why tripartite information is
small in the strip and corner limits for free and holographic theories. Nobody has explained it.
Caution from the sweep: whether EMI lies inside the band depends on dividing by C_T; divided by F₀, it
falls below the Dirac fermion [BCLM23].

**3. First von Neumann κ for an interacting CFT.** No such number exists. The only interacting κ is
Ising at Rényi-2: κ₂/κ₂^free = 0.763(22), from about 200 CPU-years of QMC on a thinly sliced torus
[KHSM19]. A von Neumann value needs the n → 1 limit, which quantum Monte Carlo does not give directly.
If Ising's κ/C_T fell well outside 3.67–4.18, the collapse would be broken. Beyond this machine without
a new method; see #4.

**4. Corner entanglement on the fuzzy sphere.** The fuzzy-sphere regularisation already gives Ising's
F-function from ground-state entanglement [HZH24]. That is von Neumann entropy directly, with no replica
limit. A "lune" between two great half-circles has two corners and maps conformally to a wedge. Nobody
has tried it, and a 2026 review lists fuzzy-sphere entanglement structure as open. The obstacle: with
about 40 orbitals, extracting a log coefficient is hard. If it worked, it would give interacting a(θ)
at any angle, including κ.

**5. The 1/N correction to κ/C_T for large-N O(N).** At leading order, κ and C_T are both N times the
free values [WWS17]. The sign of the 1/N correction decides whether Wilson–Fisher lies above or below
the free scalar, a direct test of free-scalar extremality. It is not known. It needs the fluctuation
determinant of the Hubbard–Stratonovich field on the replica manifold near a sharp corner.

**6. The θ^{2η} small-angle term at Ising/O(N).** EXP-015's mechanism, with [LMW26b] eq. (28) fixing the
exponent at p = 2(Δ_irr − 1), predicts a non-analytic term θ^{2η} ≈ θ^{0.07} at Ising, numerically
almost a logarithm. It needs sub-45° interacting data. The 2026 tensor-network method [VBHV26] reaches
2·10⁻⁵ at 90° for Ising and could run wedges; its free-scalar point is the known-answer control. Note
that replica twist lines at O(3) points carry their own defect criticality [ZWCY26], which may modify
the fusion content.

**7. Numerical bootstrap of the n = 2 twist line in 3d Ising.** No bootstrap of a replica twist in an
interacting 3d CFT exists; for the free scalar the n = 2 twist reduces to a ℤ₂ monodromy. A
bootstrap would give Rényi-2 cusp and Casimir data independent of Monte Carlo, and could test #17.

**8. Non-perturbative holography.** Only perturbative cubic gravities move κ/C_T, and finite couplings
need a stringy tower to be causal. A top-down calculation (ABJM with corrections, or bulk fields
backreacting) is the only holographic route to asking whether any strongly coupled theory leaves the
band.

**9. Prove the n → 1 continuation.** [LMW26]'s κ_n ≥ (2π/3)a_n(π/2) and [LMW26b]'s conformal concavity
are theorems at integer n ≥ 2 and only assumed or checked numerically at n = 1. Proving either at n = 1
would give the first rigorous lower bound κ/C_T ≥ 2.39 for entanglement entropy.

**10. What orders κ/C_T.** The order across theories is scalar > Dirac > ECG(t₄ = −4) > Einstein >
ECG(t₄ = +4), and t₄ does not produce it (EXP-002). No candidate ordering quantity exists.

**11. C4 at n = 1.** Reflection positivity of the corner function's derivative matrices is a
conjecture at n = 1 [CH12]. EXP-003 does not depend on it; any positive use of the spectral density
would. [LMW26b]'s concavity is the nearest proven relative.

**12. A second instrument below 45°.** The magnitudes below 45° are refereed only by one published
formula (EXP-012, RESULT §0). Candidates: a free-scalar wedge with the tensor-network method of
[VBHV26], or the Casini–Huerta equations expanded analytically. Must not be sourced from the copy of
this solver held by `../quantum` (EXP-014).

**13. An independent analytic a₀ for the free scalar.** The sweep found half the inputs. The
entangling-surface φ² coupling is marginally irrelevant and its beta function is published [MFS09]
eq. (4.20); [BCPRS21] eq. (6.19) gives a one-loop-exact version. The missing half is the coefficient of
the replica bilinears in the fusion of two parallel twist lines. Cardy's two-sphere coefficient is a
ready known-answer control [Cardy13]. Most direct route: expand the exact Casini–Huerta system one order
past κ/θ. The free-field review ties the scalar's 1/log behaviour to the zero mode, with no such term for
the fermion, which parallels a₀ ≠ 0 versus a₀ = 0. Also settles whether EXP-015's log θ term is physical.

**14. The smooth-end sign rule.** sign(σ̃′ − σ′) = sign(3π − κ/σ) holds in every case except the n = 1
scalar, but its zero moves between theory families (EXP-016). Empirical; not derived.

**15. A thermal handle on κ.** As n → 0, σ_n is fixed by the thermal-entropy coefficient (EXP-010). If
n²κ_n also tends to a fixed multiple of it, κ gains a second-channel handle. The instrument can compute
free-field κ_n at small n. It would not by itself bound κ at n = 1.

**16. The Painlevé integral.** κ₂ for the Dirac fermion is a second moment of a Painlevé profile
(EXP-011). A closed form is an integrable-systems curiosity with no bearing on the bound.

**17. Ising Rényi-2 as a constant multiple.** Ising's Rényi-2 corner runs at 0.763(22) of free at small
angle [KHSM19] and 0.78(4) at 90° [NCRCLM26]. If the ratio is constant at all angles, the shape at n = 2
is exactly free. Pre-register the prediction at an unmeasured angle; a desk study first, then #6's
instrument.

**18. Scalar run at larger M.** With the fixed solver (EXP-018, EXP-019), rerun the 50 scalar nodes at
M ≥ 14, then extend M to reach 5°–10°. This is the numerical side of #13's log question.

**19. Cubic-gravity scan.** Map κ/C_T over the two cubic couplings that affect it, (9/5)β₁ + (18/5)β₂,
inside the t₄ bounds [BCV21]. Perturbative only.

**20–21.** Instrument housekeeping, and a parked free-field curiosity; see TODO.

**22. Test the new cusp inequalities.** [LMW26b] eq. (37) says a₂ ≥ a₀/12 (with a₀ ≡ −C, the Casimir
coefficient) when the lightest fusion operator has Δ_irr > 3/2, which covers Dirac, Einstein and ECG.
Their conformal concavity says tan(θ/4)·a_n(θ) is convex for integer n ≥ 2. This repository has exact
Einstein and ECG curves, and Dirac and scalar curves at n = 1 and 2. A known-answer test that can fail;
hours.

**23. κ/F₀.** [BCLM23] conjecture κ/F₀ ≤ 0.6223, the free-scalar value. Tabulate κ/C_T and κ/F₀
side by side for every known theory, and fix the normalisation before any "near EMI" claim.

**24. The cuboid under dressing.** A research agent's algebra says [LMW26]'s cuboid bound is also
closed under a dressing that raises its four-body energy. Check it by hand; if true, the TODO item
"test the cuboid against dressing" closes.

**25. ECG t₄ sign.** Bookkeeping; affects no conclusion.

## What the sweep changed

- **A prior-art correction to EXP-015.** [LMW26b] eq. (28), posted 3 September 2026, already gives the
  small-angle exponent p = 2(Δ_irr − 1) for defects that fuse to the identity. EXP-015 derived the same
  structure three weeks later without citing it; the correction is recorded in `report.md` EXP-021.
- **Probably new, pending a proper check:** the closure of the rectangle bootstrap under Casimir dressing
  (EXP-017), the parity argument, and the twist-defect classification with the Dirac confirmation
  (EXP-015, EXP-020).
- **New data:** Ising's Rényi-2 κ [KHSM19]; high-precision Ising corners by tensor networks [VBHV26];
  Ising's F-function on the fuzzy sphere [HZH24].
- **Negative but useful:** no holographic model beyond cubic gravity has a corner function; no
  interacting κ at n = 1; no explanation of near-EMI behaviour; no upper bound on any defect Casimir
  energy.

## References new to this file

Keys resolve in `references.md`. [LMW26b] Lanzetta, Moult, Wang, arXiv:2609.04302 · [KHSM19]
Kulchytskyy, Hayward Sierens, Melko, PRB 100, 045139 (2019), arXiv:1904.08955 · [VBHV26] Van Bastelaere,
Huang, Vanderstraeten, arXiv:2609.20020 · [HZH24] Hu, Zhu, He, arXiv:2401.17362 · [BCLM23] Bueno, Casini,
Lasso Andino, Moreno, arXiv:2307.05164 · [ABC21b] Agón, Bueno, Casini, arXiv:2109.09179 · [MFS09]
Metlitski, Fuertes, Sachdev, arXiv:0904.4477 · [BCPRS21] Bianchi, Chalabi, Procházka, Robinson, Sisti,
arXiv:2104.01220 · [ZWCY26] Zhu, Wang, Cheng, Yan, arXiv:2605.00104.
