# y1 = 32/(3π²) checked at source (2026-11-26) [model: Opus 5.5]
- **Source read at body level:** M. Moshe and J. Zinn-Justin, "Quantum field theory in the large N limit: a review", arXiv:hep-th/0306133v1 (13 Jun 2003). §3.2, "1/N-expansion and renormalization group: an alternative formulation", printed pp. 43–44. The journal reference was NOT checked here; cite the arXiv version.
- **Eq. (3.28):** X1 = 2N_d/b(d) = 4Γ(d−2)/[Γ(d/2)Γ(2−d/2)Γ²(d/2−1)] = 4 sin(πε/2)Γ(2−ε)/[πΓ(1−ε/2)Γ(2−ε/2)], with ε = 4 − d.
- **Eq. (3.33):** 1/ν = d − 2 + 2(3−ε)(2−ε)X1/(N(4−ε)) + O(1/N²).
- **Evaluated at d = 3 (ε = 1):** X1 = 8/π² (numerically 0.8105695), so **1/ν = 1 + 32/(3π²N)**, and y1 = 32/(3π²) = 1.0807593. Checked numerically from the printed formula.
- **Consistency:** Eq. (3.32) gives η = εX1/(N(4−ε)) = 8/(3π²N), equal to the printed η1 = 8/(3π²) in §3.3 (p. 44).
- **Fable's use (d79a113, §7c):** the "massless-box tuning" coupling of dimension y = 1/ν = 1 + y1/N, consistent with Eq. (3.26): d − 1/ν = d_{φ²}.
- **Grade:** the value is VERIFIED at source. Fable's identification of the box-tuning profile as this coupling is ARGUED (see report, EXP-092).
