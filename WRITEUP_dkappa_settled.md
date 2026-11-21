# δκ in the large-N O(N) model: what is settled, what is not (draft for a Bridge read, 2026-11-21)

*Cuspis, Opus 5.5. Every claim carries a grade:*
- **verified**: checked by at least two routes or two readers, with numbers;
- **partially verified**: one route, or a measured range only;
- **argued**: a derivation with no independent check;
- **unverified**.

*Details and failed runs are in `report.md` under the experiment numbers given.*

---

## 0. The question and where it stands

**The question.**
- In the D = 3 O(N) model at large N, the strip entanglement entropy has a universal term −κ L/w.
- At O(N⁰), κ = Nκ_free + δκ + O(1/N). The sign of
  δ(κ/C_T)/(κ/C_T)_free = [δκ/κ_free + 40/(9π²)]/N
  decides whether the interacting κ/C_T lies above or below the free value.
  - Here C_T = N C_T,free(1 − 40/(9π²N)), from Petkou [Pet95], eq. (30).

**What is settled.**
1. **δκ is finite at this order** (partially verified; see §1). The first-order tip term carries no log(w/ε). Lemma U
   (e) holds for all y; the other gaps are graded in §1.
2. The tip coefficient C₊ at real twist.
3. Its first-order term.
4. The complex-twist BIE instrument.
5. The continuation and counting, checked against the free κ.
6. A structural obstruction: the cheap "Tier 1" route to δκ is gauge-dependent.

**What is not settled.** The number δκ itself, and parts of Lemma U (gaps a–d).

---

## 1. Lemma U (no log(w/ε) at O(N⁰))

**Statement.** The first-order (in n − 1) tip contribution to the strip coefficient contains no log(w/ε). Hence δκ is a
finite pure number at O(N⁰).

**Structure.**
- dS_tip/dn|₁ = (d/dn)S_{f₀}(n)|₁ + S_{h₁}(1).
- f₀ ∝ C₊(α)·Σ̃₁(iα, α)·(1 − e^{−2αL})/(2α), and h₁ ∝ C₊(α)·Σ̃′(iα)·(…), with L = ln(w/ε).
- A log arises only if f₀ or h₁ grows like e^{2π|y|} along α = ½ + iy. A planted L·sin²(πα) shows that exactly
  (EXP-057).
- f₀ ≠ 0: an earlier claim Σ̃₁(iα, α) ≡ 0 (Neon T7, claim 3) is **false**. This is verified by two routes (EXP-061),
  and Neon T20 concurs.

| gap | content | grade | where |
|---|---|---|---|
| (a) | the α → 1 end mirrors α → 0 | argued | EXP-053 |
| (b) | C₊ = −α/8 + O(α²) | argued; consistent with the T23 closed form and the BIE trend | EXP-057, EXP-066 |
| (c) | no off-axis zeros of the σ kernel | partially verified (8 cases) | EXP-056 |
| (d) | regulator dependence is local | argued | EXP-061 |
| continuation family | internal φ twisted, σ untwisted | argued | EXP-061 |
| **(e)** | **\|C₊(½ + iy)\| ≤ C(1 + \|y\|)²(1 + ln(1 + \|y\|))³ = o(e^{2π\|y\|}) for all y** | **verified** | EXP-067/068/070 |

**(e): the proof chain.** Neon T26 + T27 + T30. Every step was line-checked by two readers (the Bridge and Cuspis),
with numerical spot checks.

| step | content | checked in |
|---|---|---|
| T26 Steps 1–4 | positivity (Bochner); a rank-2 u-derivative of Rᵀ; Cauchy–Schwarz in the M inner product, giving \|C₊\| ≤ B(y) = (1/(8π²(¼ + y²)))∫du(−ln det(1 − λ²RᵀR)) | EXP-067 |
| T26 Step 5 | the Parseval/contour-shift bound on Tr B_u | the Bridge, plus EXP-070 (a)–(c) |
| T27 | κ_max(u; y) < 1 for all u > 0 and all real y (Loewner monotonicity plus a multiplier bound) | EXP-068 |
| T30 | the quantitative gap 1 − κ_max ≥ 1/(30000L²e^{2π\|y\|}cosh²πy) | the Bridge, plus the EXP-070 addendum |

- Corrections made along the way, all recorded:
  - my EXP-067 B(4) = 6.78·10⁻² was a non-Hermitian-slogdet artefact; T27's 6.871·10⁻² supersedes it;
  - my T30 "nit" was itself wrong (the Bridge's correction); T30's 0.96 stands.
- **The remaining factors of f₀ and h₁:**
  - the n = 1 on-shell factor is a polynomial in a: [1 + 4a² − 24a(1 − a)]/(12π²) (verified at real a by two routes;
    ~y² on the line);
  - Σ̃′ is polynomial to y = 3 (partially verified; no all-y bound).
- **Lemma U overall:** (e) is verified; (c) is partially verified; (a), (b), (d) and the continuation family are argued.
  **The no-log conclusion is therefore partially verified as a whole.** C₊'s growth is verified for all y. Σ̃′'s growth
  (the h₁ factor) is measured only to y = 3 (§8 item 3). The argued gaps (a), (b), (d) and the choice of continuation
  family are the other weak links.

## 2. C₊, the near-tip coefficient: four routes at real twist (verified)

C₊ = (1/(8π²a(1 − a)(2a + 1)))∫s^{2a+1}b u ds, from the CH05 Painlevé system (u-ODE, h, b) [CH05 route; report
"C₊ at complex α"]. It is settled at real twist by four routes:
1. the CH05 Painlevé route (this repo);
2. Neon T23 (first-principles legs);
3. the Bridge's re-implementation. The resummation ratio blind-matches the other two to 5–6 digits: 1.12449 / 1.16274 /
   1.17592 at a = 0.2 / 0.3 / 0.4 (Bridge seal V28);
4. Neon T25, a direct Galerkin BIE (EXP-066):
   - shape to ≤ 4·10⁻⁵;
   - absolute cross-channel coefficient e(w) to ≤ 2.4·10⁻⁴ for w ≤ 0.3.
   - It is the first finite-mass absolute test of the σ machinery's normalisation and sign.

The reflection sign is fixed independently by the CFT cross channel (EXP-064; the planted sign flip fires).

## 3. The first-order term is T23's closed form, not Born (verified)

C₊^lin(a) = −(sin πa/(4π³))·(Γ(a + ½)/Γ(a + 1))²·Γ(3a + ½)Γ(3/2 − a)/Γ(2a + 2).
- At a = ½ it equals (4/π)× the Born value. The CH05 linear term matches it to 2·10⁻⁷ and **excludes Born by 27%**.
- On the line a = ½ + iy it matches to ≤ 4·10⁻¹³ for y ≤ 5 (EXP-065 rerun, clause T).
- Its decay on the line (rate −0.45 on [2, 4]) agrees with T23's Stirling prediction of rate 0 on the measured range,
  against Born's π.

## 4. C₊ on the continuation line (partially verified numerically; analytic bound verified)

- EXP-065: |C₊(½ + iy)| = 5.997, 9.201, 7.077, 3.664, 1.527, 1.393 (×10⁻³) at y = 0…5. The local rate on [2, 4] is −0.77,
  against the borderline 2π. The planted 2π control fires.
- **The registered nuisance clause failed**, because the t₀ = 18 production rung was unconverged at y ≥ 3. This was my
  design error and is recorded.
  - The post-registration rerun on a converged t₀ ladder passes the gate.
  - The rtol rung is still short at y ≥ 3.5; this does not move the rate.
- The all-y analytic bound (§1 (e)) supersedes the measured-range caveat for the growth question.

## 5. The complex-twist BIE (EXP-069, verified on the line)

- Neon's T25 BIE, copied with marked changes, run at a = ½ + iy, passes two independent anchors:
  - **V1:** the Fredholm-determinant cross coefficient, to ≤ 1.2·10⁻³ for y ≤ 1 and 1.4% at y = 2;
  - **V2:** the CH05 resummation shape, to 0.07%.
- The planted 2% normalisation error fires at 7σ.
- y = 2 is the hard point (κ_max → 1). The continuation weight π/cosh²(πy) suppresses it.

## 6. The continuation and counting, checked against the free κ (EXP-071, verified)

- **KF0:** the line integral 𝒞[g] = ∫₀^∞ds(π/cosh²πs)g(½ + is) equals (d/dn)Σ_{q=1}^{n−1}g(q/n)|₁ to 2.5·10⁻¹⁴ and
  8.5·10⁻¹².
- **KF1:** −½𝒞[w_S] reproduces κ/C_T = 4.173987 (spread 6·10⁻⁶), inside the EXP-040 two-implementation bracket. So
  **κ_free = 0.0396481 per real scalar.**
- **Must-fail:** counting factor 1 gives 1.998×, so it fires.
- **Open, stated plainly:** [CHL09] Table 1 prints 0.0794 for the complex scalar; our three routes give 0.07930. Our
  secondary clause failed narrowly (miss 5.2·10⁻⁵). This is unresolved and does not affect δκ.

## 7. The SC formula (WITHDRAWN as complete, EXP-075), the gauge obstruction, and T31/T35

> **Update (EXP-075, c49ae29): the SC formula below is withdrawn as a complete formula.**
> - Its σ-sector object F₁(β) = ½ log det(2G₁∘G^{(β)}) has a q-dependent O(1) local part, 2S·a^{(β)}.
> - The honest replica bubbles all share the local part 2S² + 4S·a_n, with a_n = O(n − 1).
> - So SC carries a cubic UV log ∝ 𝒞[a³] that the honest theory lacks. On a single edge, 𝒞[c] = −1/32 (= EXP-062) but
>   𝒞[c³] = −4.0·10⁻⁵ ≠ 0. (Argued, with numbers.)
> - This is the origin of Neon T35's ln(Λw)/w. It does **not** indicate a UV log in δκ, and is consistent with Lemma U.
> - What survives:
>   - the exact sector decomposition;
>   - the 𝒞 identity (verified);
>   - T(α)'s gauge invariance;
>   - T31's free TGTG ↔ CFH isospectrality, verified for λ₁ at ≤ 0.4% (EXP-074);
>   - the BIE (EXP-069).
> - The correct continuation, which keeps the inner φ-sector sum, is the subject of Neon brief T36 (unverified until
>   checked).

**The SC formula (argued; withdrawn, see above).**
S⁽⁰⁾_univ = 𝒞[F₁(β)] + ½𝒞[T(α)], with
- F₁(β) = ½[log det(2G₁∘G^{(β)}) − log det B₁];
- T(α) = Tr(B₁⁻¹·2(G^{(α)}∘G^{(−α)} − G₁∘G₁)).

It uses only n = 1 objects: flat G₁, B₁ = 2G₁∘G₁, and free twisted strip propagators. It was derived by sector
decomposition plus Abel–Plana (report, "δκ step 1"). The saddle term is argued to be local.

**The gauge finding (argued, with a toy check).**
- The twist cut's placement is a gauge choice, G^{(β)} → U G^{(β)} U⁻¹. F₁ and T are invariant under it; the flat
  objects are not.
- So the expansion in ΔG = G^{(β)} − G₁ (the planned "Tier 1", i.e. the linear terms) is gauge-dependent:
  - across the cut ΔG ≈ (e^{2πiβ} − 1)G₁, so ‖X_β‖ = O(1) with no small parameter on the line (|c| ∈ (1, 2]);
  - in T(α), the linear and quadratic pieces cancel exactly at the cut.
- **Toy check (`scripts/exp072_gauge_toy.py`).** Pure gauge on a 1D lattice, where the exact answer is 0:
  - Tr X = 1.85 and ‖X‖ = 3.2 at φ = π + 0.5i, while log det(1 + X) = 10⁻¹⁵;
  - Q/L = −1.000000 at every φ;
  - the must-fail φ = 0 gives all zeros.
  - Grade: the algebra is verified on the toy; that the same holds on the strip is argued.
- **Consequence.** Option (i) (Tier 1 + a size estimate) was **not registered**.
  - T(α) can still be computed as one gauge-invariant trace. It has no Z-factor ambiguity (argued), but it costs as
    much as the old Tier 2.
  - F₁ needs a full Fredholm log det, or a gauge-invariant reorganisation. That reorganisation is the Neon T31 brief,
    in progress, and its output will be unverified until checked.

## 8. Open items, stated plainly

1. **The number δκ.** It is not computed. SC is withdrawn (EXP-075). Routes:
   - a corrected sector continuation (Neon T36, pending);
   - (iii) integer-n honest sums at n = 2, 3;
   - Route B (expansion around the n-cone, as in Lemma U).
2. **Lemma U gaps (a), (b), (d) and the continuation family:** argued only. Gap (c): 8 cases.
3. **Σ̃′:** no all-y bound (polynomial to y = 3).
4. **The SC formula:** withdrawn (EXP-075). Its Abel–Plana drop fails for the UV-local part. The registered n = 2, 3
   honest-sum gate would have caught it.
5. **The Tier-1 cut dependence on the strip** (e.g. strip vs complement cut): unverified. It would need the strip
   machinery.
6. **CHL09 0.0794 vs our 0.07930:** unresolved.

## 9. Withdrawn or corrected claims (kept as controls)

- "Σ̃₁(iα, α) ≡ 0" (T7 claim 3): false (EXP-061).
- "Born series diverges" (my EXP-060 corollary): withdrawn.
- Route A's angle-rescaling derivation: invalid for the strip; replaced by SC.
- EXP-067's B(4) = 6.78·10⁻²: a float artefact.
- My T30 "nit": wrong.
- The δκ Z-factor checkpoint (e4ffec0): a formal error, replaced by the gauge finding (77f10d0).
- The plane-wave "cut reduction" for Tier 1: superseded (it is in the cut gauge).
- The SC formula as a complete expression for S⁽⁰⁾: withdrawn (EXP-075). Its n = 1 σ-sector object mis-continues the
  inner φ-sector sum.
- My T35 "same-ray straddle" worry: resolved by T35's commutator identity (EXP-075). The remainder is cross-ray.

References: [Pet95] hep-th/9506116; [MZJ03] hep-th/0306133; [CHL09] and the CH05/CH07b sources as listed in
`references.md`.
