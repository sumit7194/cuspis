# EXP-088 REGISTRATION (2026-11-25 ~20:20; nothing computed for (a), (c), (d), (e)): checks of Fable's n = 2 answer (a3a385f) and grading of its seal (bcdb69f) [model: Opus 5.5]

*Fable's claims are UNVERIFIED inputs used only as predictions or hypotheses. Seal bcdb69f is an ancestor of answer a3a385f (checked).*

## (a) Grading of the sealed predictions (needs σ₂ at P = 10: honest n = 2 saddles at W5P10 and W10P10)
- **Quantity:** S₂(2.5) = R₂(2.5) + ΔR₂^A(2.5), with R₂(2.5) = 4.3170 (084, stored), ΔR₂^A = Ny·[Σc_Aσ₂(W5) − Σc_Aσ₂(W10)]·norm(2.5) (n = 2 prefactor 1), c_A from `exp085c/G_W{5,10}P10.json`, σ₂ from the HONEST saddle (`exp083_honest.Geom(W, 10, Wbox=10, c=2).saddle(2)`).
  - KA first: the same honest-saddle code at W4P8 must reproduce the stored 084c σ₂ sum (−1.021015) to 1e-6.
- **PRIMARY (seal's 68% band): PASS iff S₂(2.5) ∈ [0.162, 0.202].** SECONDARY (outer band): inside [0.14, 0.23]. Fable's own risk values, 0.27 / 0.35, are reported if hit.
- **Second prediction:** the local bulk overshoot ratio on ℓ = 2 → 2.5, −[ΔR₂^bulk(2.5) − ΔR₂^bulk(2)] / [R₂(2.5) − R₂(2)]. PASS iff 1.27 ± 0.03 (hi c) and 1.39 ± 0.03 (lo c).
- Cost is unmeasured at P = 10 (n·N = 1200 dense per sector). It runs only on a free slot, under the no-kill watchdog.

## (b) Re-run of `notes/fable_n2/sig2_profile.py` — DONE: output identical to Fable's (reproduction, not independent)
- D(ℓ) = 0.06086, 0.07504, 0.08649 independently matches my EXP-086b sums.
- The r²σ₂ "plateau" at W4P8 is −0.033, −0.0375, −0.034, −0.028 over r ≈ 0.7–3, then decays: under a decade of r with ±15% scatter. The 1/r² form is ARGUED, not established.

## (c) Finite-difference test of Q1 (first-order form complete) — tiny boxes; can fail
- Leading-order free energy per N: f_n(J) = ½[Σ_p log det H_(n,p)(σ_n) − n·Ny·Σ_x J(x)σ_n(x)], with σ_n the honest saddle for coupling J.
- Shift J → J + ε h(x) for h ∈ {c_A (box), a uniform h, a random h}. Prediction (Q1 / envelope): [f_n(+ε) − f_n(−ε)]/(2ε) = −½·n·Ny·Σ h σ_n.
  - For n = 1 the left side is 0, since σ₁ = 0.
- **PASS** iff it agrees to 1e-6 relative at ε ∈ {1e-3, 1e-4}, for n = 2 on ≥ 2 tiny geometries (one with W = Wbox), and the second difference scales as ε² (no O(ε) curvature term).
- **FAIL** means a missing first-order term, against Q1.

## (d) σ̇ profile at n → 1 (Fable §3c "contact term, no 1/r² tail")
- Compute σ̇ = 2B₀⁻¹d (production path) at W4P8 and W8P8. Report r²σ̇ by shell, next to Fable's r²σ₂ shells.
- **Fable's claim FAILS** if r²σ̇ shows a plateau comparable to σ₂'s (within a factor 3 of |a₂| = 0.035, scaled by the σ̇/σ₂ magnitude ratio) over r ∈ [1, 3].
- The stored-number part, "the W-difference of Σc_Aσ̇ / (c(1 − 2/P)) is flat to 6%", is re-derived from the G files (zero compute).

## (e) Is the stored n = 2 saddle the dominant one?
- **Argument (mine, standard convexity):** log det(H_n + diag σ) is strictly concave in σ on {H_n + σ ≻ 0} (Hessian −G∘G, a Schur product of positive-definite matrices). So the gap equation has at most ONE stationary point in the domain where the φ-integral converges; by the sheet symmetry it is replica-symmetric.
- **The check that can fail:** λ_min(H_(2,p) + diag σ₂) > 0 for every sector p, at all six stored geometries (W2P4 … W8P8). If any λ_min ≤ 0, the stored saddle lies outside the convergent domain and the argument fails.

## (f) Non-author read of Q2 ("c(x) is the same at every n") — DONE (reading)
- **It follows, and it is not circular.** By §1, R_n + ΔR_n[c] is the honest R_n of ONE model with coupling J(x) + c(x)/N. A model's couplings are fixed before any Rényi index is chosen, so c cannot depend on n.
- **What it assumes, and what it moves:** c is chosen by an n = 1 criterion (criticality of the unreplicated box). Given that, using c_A at n = 2 adds no assumption.
- **What it does not show:** that A (rather than bulk) is the right n = 1 criterion. That question moves to §2c (argued: "the n = 1 box stays massless"), not to n = 2.
- So EXP-086b's c_A-at-n = 2 caveat reduces to the A-vs-bulk choice at n = 1. It is not an extra n = 2 assumption.
