# EXP-083 — DRAFT: honest integer-n referee for the lattice σ continuation (sigma3d Strip3D, s_cut, saddle) [model: Opus 5.5]
Not registered and nothing computed. Drafted at the Bridge's request (2026-11-22), alongside EXP-081c and separate from its
chain.

## Answer from the code (the Bridge's question): partially, yes
- **Validated before.** The per-slice anchored-residue continuation was checked against honest integer-n data on 2D
  stand-ins only (EXP-079: P4′ n = 2..6 to 2·10⁻¹¹; P5 Q′(1) = −1.38687; a 2-slice q-convolution, clause C).
- **Never checked against honest integer-n data: the production `Strip3D` pipeline used in 081b.** That pipeline includes:
  - QEP slice poles, with the **s_cut = 3 threshold**, which is the lattice analogue of the near-¼ cut: poles with
    r < e^{−6π} = 6.5·10⁻⁹ are dropped;
  - stable-K residues;
  - the y-convolution over N_y slices;
  - **the saddle term T_sad**, never compared with an honest replica saddle. Its only test (S4) was a pure gauge, where
    it is 0 by construction.
- **Lattice vs continuum.** Each lattice slice has only 2W poles, at s ≲ 4, so there is no accumulation at r → 0. The N4
  diagnostic shows the β = 0 contributions of poles beyond s_cut shrinking geometrically (≈ e^{−2πΔs}), so the s_cut
  truncation itself looks benign (argued).
  - **But EXP-082 shows that matching integers and self-consistent convergence do not validate the n → 1 slope.** Only
    an honest-data referee does. 081b's controls (K free side, N2′ referee, N_y, census) test numerics and the free side.
    **None of them tests the σ continuation against honest data. This is a missing control for the +2.4.**

## Design
- **Geometries.**
  - The 081b strip family at small P: W = 2 and 4 in box 4.
  - P = 2 (Lx 8, Lt 4, N_y 8; 32 sites/sheet).
  - P = 4 (Lx 12, Lt 8, N_y 16; 96 sites/sheet). These are exactly 081b's W2P4 and W4P4, whose continuation values are
    on record (S_T0 0.988599 and 1.167472, impact rule).
- **Honest data.**
  - Q(n) = Σ_k [log det B_n^{(k)} − n log det B₁^{(k)}], with B_n^{(k)} = (2/N_y) Σ_p G_p⁽ⁿ⁾∘G_{k−p}⁽ⁿ⁾ on the n-sheet
    manifold (each slice's cut links glued cyclically; the EXP-082 gluing, de-duplicated).
  - n = 2..24 (P = 2) and n = 2..12 (P = 4).
  - (a) **No saddle.**
  - (b) **With the honest replica saddle:** σ_n(x, t), sheet-symmetric, solves (1/N_y)Σ_p G_p⁽ⁿ⁾[σ](x, x) =
    (1/N_y)Σ_p G_p⁽¹⁾(x, x) at every site, by Newton. Q(n) is then evaluated at σ_n.
  - Spot checks at 40 digits at two n (P = 2).
- **Referee Q′(1) from the honest data.**
  - Fixed-base fits with the census-checked slice poles as bases b_j = e^{−2πs_j}, plus confluent n·bⁿ terms for
    coincident poles across slices (the k-sector structure), plus A·n + B.
  - Drift reported over base sets and n-ranges; the last n held out.
  - Newton or Levin alone is not used (the EXP-077 lesson).
- **Comparisons.**
  1. Integer values: the continued sector sums Σ_Q log det B_n^{(Q/n)} (route_b's `inner(n, Q/n)` / `inner_beta0`) at
     n = 2, 3 vs honest, to ≤ 10⁻⁹. This checks numerics only.
  2. **Slope:** route_b Q′(1) = t0 + 𝒞 vs referee (a); t0 + T_sad + 𝒞 vs referee (b). The strip-pair combination
     δQ′ = Q′(W2) − Q′(W4), which is what enters R, is compared as well.
- **Tolerance (to be fixed at registration, after a Tier-1 feasibility probe of the fit drift that runs the honest side
  only, at P = 2, W = 2, no saddle):** |Q′_cont − Q′_ref| ≤ max(3 × drift, 10⁻⁶ |Q′|), for each geometry and for δQ′.
- **Must-pass / must-fire.**
  - Honest code: a wall-to-wall cut (pure gauge) gives Q(n) = 0 to ≤ 10⁻¹⁰.
  - The planted drop of confluent residues (dd = 1) must disagree with the referee.
  - s_cut lowered to 1.5 must disagree. If it does not, s_cut is shown irrelevant at this size, and that is reported.
- **Consequence.**
  - Disagreement beyond tolerance at P = 2 or P = 4, without saddle or with saddle: **the lattice continuation is not
    validated, and EXP-081b's R values (and 081c's σ_W) cannot carry a sign.** The +2.4 is suspended.
  - The with/without-saddle split locates the failure in T_sad or in t0 + 𝒞.
  - Agreement: the continuation is **validated on the production family at small P (partially verified)**.
- **Resources (estimate, to be measured).** P = 4, n ≤ 12: 1152-site slices, 9 unique slices, about a minute per n. The
  saddle Newton adds ~10×. Peak < 1 GB, daytime, one core.

## Order
1. Register.
2. Tier-1 feasibility of the honest-data fit at P = 2 (honest side only; fixes the tolerance).
3. P = 2 comparison, then P = 4.
4. Report.

Separate from 081c's chain. Run after it, or in parallel at nice 12 if the Bridge prefers.
