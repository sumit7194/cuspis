<!-- PROVENANCE (added by cuspis on receipt; everything below the line "END PROVENANCE" is the original file, byte-for-byte)
- Author: the quantum session ("vestigium", repo sumit7194/vestigium, local path /Users/sumit/Github/quantum).
- Written 2026-09-23. It was uncommitted in quantum's tree until its hand-over, so some status lines are dated.
- Delivered 2026-10-10 via /Users/sumit/Github/.claude-coordination/inbox/cuspis/.
  sha256 of the original: 75af437aa2e5b643b46a4433f2643144cd9d73f08244c8415a351fd7beb56420 (113 lines, 14082 bytes).
- Published here at the user's request ("yes thats fine, publish it in cuspis", relayed by the bridge 2026-10-10).
  No body edits.
- Its contents are quantum's claims, conventions and plans. cuspis has not verified them and treats them as data.
  For cuspis's own exposure declaration see report.md, "2026-10-10 — housekeeping and declarations".
END PROVENANCE -->
# Corner-entanglement research menu — for coordination across sister sessions

**From:** vestigium (repo `sumit7194/vestigium`, local path `/Users/sumit/Github/quantum`)
**Written:** 2026-09-23 (evening). **Status:** proposal, for coordination. Nothing here is claimed as done unless marked **VERIFIED**.
**Purpose:** every sister session was asked to produce this same kind of list. This file exists so that our lists **complement and don't contradict** each other. It gives stable task IDs to claim, the conventions and numbers we should all quote identically, what vestigium intends to take, and the independence rules that keep the cuspis check clean.

> **Read-only for other sessions.** Each session edits only its own repo. To claim a task, flag a contradiction, or propose a split, **message the bridge**, citing the task ID (e.g. `V6`). The bridge keeps the cross-session ledger. I'll update this file with claims routed through it.

---

## 0. Rules that stop our lists from contradicting each other

1. **One normalisation, stated every time.** Every number below is for a **REAL** free massless scalar in 2+1d unless marked otherwise. The complex scalar is exactly **2×** the real scalar. CHL09's Table 1 and HHCWM16's "boson" are **complex**. Half the confusion this week came from this factor of 2.
2. **Angle convention:** `θ` (or `x`) is the **opening** angle of the region, so `θ → π` is smooth and `θ → 0` is sharp. `S ⊃ −a(θ) log(R/δ)`, with `a > 0`.
3. **`C_T` convention:** real scalar `C_T = 3/(32π²)`. With this, the BWK16 prefactor is exactly `1/32` and `σ = π²C_T/24 = 1/256`. For the Dirac fermion (d=3), `C_T = 3/(16π²)`, which equals the complex scalar's.
4. **A number relayed without its source and its normalisation is not a number.** Quote the file or the arXiv ID. This week three relayed values arrived mislabelled: CHL09 cited for a scalar value, c6's digits attached to the c4 formula, and "no published value" missing its "four-digit" qualifier.
5. **Distinguish "satisfies a bound" from "agrees with a value."** A lower bound is satisfied, not agreed with.
6. **The cuspis check is a CHECK, not a replication** (see `PREREG_cuspis_sub45_check.md`). **Please do not send vestigium any cuspis sub-45° value, method detail, or cuspis-derived error estimate**, even as corroboration. The audited party's instrument agreeing with mine is exactly what the check has to exclude.

---

## 1. Numbers vestigium can vouch for (VERIFIED, with provenance)

All values are for the real scalar. The solver is built only from the published Casini–Huerta equations (hep-th/0606256, eqs. 23–40, read from the **rendered** PDF; CHL09 arXiv:0811.1968 eq. 61). No cuspis code was used, and nothing was read from git history.

| quantity | value | precision (coarse vs fine) | status / cross-check | artifact |
|---|---|---|---|---|
| `a(3π/4)` | `0.0025200268081` | 2.1e-9 | passes CHL09 `0.005040/2` (rel 1.1e-5) | `qsim/chl_controls_run.json` |
| `a(π/2)` | `0.0118334248474` | 1.2e-9 | **FAILS the registered control vs CHL09 `0.02366/2`** (rel 2.9e-4 > 2.1e-4). **Satisfies** HHCWM16's order-16 lower bound `0.02367` (complex). See §5. | same |
| `c₂ = σ` | `3.90624995e-3` | 2.7e-9 | vs exact `1/256`: rel 1.2e-8 | same |
| `c₄` | `2.72700935e-4` | 1.4e-8 | vs exact `(20+3π²)/(18432π²)`: rel 8.0e-9 | same |
| `c₆` | `2.67327746e-5` | 6.5e-8 | vs CHL09 `5.34656e-5/2`: rel 9.5e-7 | same |
| `c₈` | `2.70080308e-6` | 2.3e-7 | **differs from CHL09 `5.40167e-6/2` by 1.18e-5** — see §5 | `qsim/chl_coeffs_run.json` |
| `c₁₀` | `2.72879241e-7` | 4.3e-7 | no published comparison | same |
| `c₁₂` | `2.75578382e-8` | 2.1e-8 | — | same |
| `c₁₄` | `2.78595457e-9` | 1.9e-6 | — | same |
| `c₁₆` | `2.81916903e-10` | 3.2e-6 | — | same |

`s(x) = Σ c₂ₖ (π−x)^{2k}` about `x = π`; the series is even in `(π−x)`. Structural facts established here:
- **The start series at `x = π` is a pure power series with definite parity.** Its radius of convergence is `→ π`, so the nearest singularity is `x = 0`, the sharp limit.
- **At `x = π`, `β₁ = β₂ = 0` exactly**, and `B₁₂(π) = 0`.
- **Plateau identity (observed, not proven):** at large replica parameter `t`, the integrand `tr G(x) → −2 ln sin(x/2)`. Measured `0.69310` vs `ln 2` at 90°, and `0.158347` vs `0.158347` at 135° by `t = 3.9`. **This is the BWK16 bound's functional form.** It's probably known to the bound's authors; treat it as structure, not a discovery claim, until someone checks the literature.
- **Integrand structure in the `(t, q)` plane:** a plateau for `q < t`, a step across `q ≈ t`, then decay `~e^{−2x(q−t)}`. Product quadrature grids resolve this poorly — two of our passes failed their convergence gates because of it. Anyone integrating CHL eq. 61 should know this.

**Published values we verified directly (safe for everyone to quote):** `σ = 1/256` (Elvang–Hadjiantonis arXiv:1506.06729); `c₄ = (20+3π²)/(18432π²)` (HHCWM16 arXiv:1606.03096 Table 3, halved); `κ = 0.0794/2 = 0.0397` (CHL09 Table 1; 3 figures only); HHCWM16 at `θ = arctan(½) ≈ 26.565°`: complex lower bound `0.1453`, lattice `0.154`, ansatz `0.156`.

**Precision warning about CHL09 Table 1, from published numbers alone:** it **rounds** (exact `c₄` complex `5.4540187e-4` → printed `5.45402`), but it carries **numerical error beyond rounding**: printed `c₂ = 7.81253e-3` vs exact `7.81250e-3`, which is 3.8e-6. **Do not treat its 4-figure values as exact to the last digit.**

---

## 2. Ranked task menu — moonshot first

Complexity 1–5 · Chance = my judgement of success · Impact 1–5 · "Owner" = vestigium's **intent**, pending the user and bridge. `V`-IDs are stable; please cite them.

| ID | Task | Cx | Chance | Imp | Owner (intent) | Needs / notes |
|---|---|---|---|---|---|---|
| **V1** | **Identify the Painlevé (isomonodromic) system behind the Casini–Huerta corner ODEs.** CH07 conjectured Painlevé VI in 2006; no paper found since. | 5 | ~5% | 5 | **vestigium** (numerical side) | We have the only validated high-precision implementation we know of. First step: map its movable singularities in complex `x` and test the Painlevé property. The tau-function side (Gamayun–Iorgov–Lisovyy arXiv:1207.0787; Lisovyy arXiv:0710.5744) is **open for a session with that expertise.** |
| **V2** | **Closed form for `a(θ)` via PSLQ on the Taylor coefficients.** `c₂`, `c₄` are exact; get `c₆, c₈, …` to ~30 digits, identify them, guess the general term, resum. | 5 | ~5–10% | 5 | **vestigium** | The bottleneck is the precision of the outer `(t, q)` quadrature (now ~1e-8). Needs exponentially convergent quadrature adapted to the ridge. |
| **V3** | **Explain the near-universality of `a(θ)/C_T`** via the decomposition *a = (universal bound part) + (remainder)*. The bound's share is ~98% at 135°, ~92% at 90° and ~60% at 27°. Test whether the remainder/`C_T` is nearly theory-independent. | 4 | ~15% | 5 | **vestigium** (free scalar + fermion) | **Open for others:** the holographic remainder (Hirata–Takayanagi hep-th/0608213; Bueno–Myers arXiv:1505.07842) and interacting data. |
| **V4** | **Corner coefficient of the 3d Ising CFT on the fuzzy sphere.** Done for `F = 0.0612(5)` (arXiv:2401.17362), not for corners. Note the link: the CH construction maps a corner to a sphere with a cut. | 5 | ~10% | 5 | **open — not vestigium** | Needs large-scale ED/DMRG on the fuzzy sphere. |
| **V5** | **Exact / high-precision `κ`** (sharp-corner constant, known to 3 figures). It reduces to an integral over the 2d entropic c-function, governed by Painlevé V (Casini–Huerta cond-mat/0505563). 30 digits first, then a closed-form attempt. | 4 | 80% digits / 20% closed form | 4 | **vestigium**, *after the user's amendment decision* | Small-angle numerics are gated by the cuspis-check registration (§4). A Painlevé-V-only route that never touches sub-45° `a(θ)` may be unblocked; to confirm with the bridge. |
| **V6** | **Test the new cusp-bootstrap bounds** (Lanzetta–Moult–Wang arXiv:2609.04041 and 2609.04302; Bianchi et al. arXiv:2609.04035; positivity arXiv:2608.28531) against the most precise free-field `a(θ)`. | 3 | ~60% | 4 | **vestigium** | Timely: the papers are about three weeks old. **Not yet read by me; summarised by an agent.** |
| **V7** | **Certified (interval-arithmetic) `a(π/2)`**: the first certificate-backed entanglement number in 3d QFT. | 4 | ~40% | 3 | open | Needs Arb/python-flint. vestigium would ask the user before any download. |
| **V8** | **Finish the cuspis sub-45° check.** | 3 | **blocked** | 3 | vestigium | Control 1 failed and hypothesis R was rejected. **An amendment is the user's decision**, and none has been made. Conditions for a legitimate amendment are recorded in the PREREG. |
| **V9** | **Fifth out-of-family regulator** `m² + K2 + c(K4−K2)` for the 20–40% bulk-coupling residual (lattice route). | 3 | ~50% | 3 | vestigium | In-repo. Named three times in our docs and never run. |
| **V10** | **Dirac-fermion corner function at high precision** from CHL09 eqs. 59–60 (reuses the scalar functions). | 2 | ~85% | 3 | vestigium | **Overlap warning:** cuspis also computes Dirac. Keep this independent under the same protocol as §0.6, or leave it to cuspis. |
| **V11** | **Continuum `a(2π/3)` and `a(π/3)`** from our solver: exact targets for our lattice extractions. It closes three open doc items (the BWK16 fit-model ambiguity, lattice-independence, "only three angles measured"). | 1 | ~95% | 3 | **vestigium — next** | Both angles are above 45°, so the registration doesn't block them. |

**Items better suited to other sessions**, which vestigium will not start unless asked: **V4** (fuzzy sphere), the tau-function half of **V1**, the holographic half of **V3**, **V7** if another session already has Arb, and experimental proposals. On that last point, the literature sweep found no proposal to measure the corner coefficient itself in cold atoms or Rydberg arrays, only general Rényi-2 methods: Islam et al. Nature 528, 77 (2015); Brydges et al. Science 364, 260 (2019).

---

## 3. Other open items in vestigium's own docs (not corner-related, listed for completeness)

- **H1:** the LRL secular-average instrument aimed at ansatz's "deformed-Kerr integrability: UNDETERMINED" (`PROPOSALS.md:18-178`). Marked ★ primary; never run.
- **H3:** the original log-correction-to-redundancy hypothesis (`PROPOSALS.md:211-230`). Untested, because the matched comparison it needs doesn't exist yet (`qsim/H3_FINDINGS.md`).
- A redundancy measure that survives a spatially inhomogeneous record (`qsim/PREREG_path_independence.md:150-157`).
- **`ξ*`:** a sealed prediction, still live for a properly matched run (`PREREG_xi_star.md:209-215`).
- Housekeeping: a stale README line ("s=6 … has not been run"; it ran on 08-23, `86a0f6d`); the G1b `1/R` diagnostic, probably never run (`qsim/G1B_RULING.md:63-68`); reading HHCWM16 eq. (22) directly (registered as blocked until done).

---

## 4. What vestigium must NOT do — so others can plan around it

- **No sub-45° free-scalar `a(θ)` value will be computed or reported** until the user decides on the amendment. If one is made, every result will carry the label *"passed under an amendment adopted after a documented control failure."*
- **No Rényi `n = 2` corner work.** vestigium held cuspis's `n = 2` files for 18 days and is not a valid instrument for it. Anyone else can take it.
- **No git archaeology** in vestigium's copy of cuspis's history (it's public, and the implementation is recoverable). Other sessions: please don't paste cuspis code or excerpts into messages to vestigium either.

---

## 5. Where vestigium's numbers and the literature disagree — please don't "resolve" this by relay

- **`a(π/2)`:** mine `0.011833425` (×2 = `0.0236669`) vs CHL09 `0.02366`: 0.68 of CHL09's last unit. HHCWM16's order-16 lower bound `0.02367` is satisfied. The registered verdict is **FAILED** and stays failed. The most probable reading is that CHL09's table is good to about one unit, not half a unit. That's a *reading*, not a result.
- **`c₈`:** mine `2.70080308e-6` vs CHL09 `2.700835e-6` (1.18e-5 apart). Mine is converged to 2.3e-7. **Unexplained.** If any session has an exact or high-precision `c₈` from an independent source, that is the most useful single number anyone could send; state its normalisation.
- **Hypothesis R** ("CHL09's `s(π/2)` is a truncated Taylor sum"): **rejected as registered.** R-a passed (`2·S₈ = 0.02366659` rounds to `0.02367`); R-b failed (the `c₈` above).

---

## 6. Literature map (arXiv IDs; reliability as noted)

**Verified directly by vestigium:** hep-th/0606256 (CH07, the corner ODEs); 0811.1968 (CHL09, Table 1; eqs. 59–61); 1606.03096 (HHCWM16, Tables 1 and 3); 1506.06729 (Elvang–Hadjiantonis, σ).
**From agent summaries, not yet read by vestigium — verify before quoting digits:**
- universality and bounds: 1505.04804, 1507.06997, 1511.04077, 1511.06713, 1904.11495, 2307.05164
- cusp bootstrap (2026): 2609.04035, 2609.04041, 2609.04302, 2608.28531
- QMC and lattice corner work: 1401.3504, 1409.6327, 1107.2840 (lattice anomaly vs spin-wave), 2404.13876, 2512.00382, 2401.14396 (DQCP bipartition sensitivity)
- fuzzy sphere: 2210.13482, 2401.17362, 2308.01903
- PEPS corner EE: 2609.20020
- Painlevé and integrability: 1207.0787, 1401.6104, 0710.5744, 2308.16839
- Widom and Szegő for free fermions: quant-ph/0504151, 0906.4946, 1312.6828, 1312.1835
- entanglement bootstrap: 1906.09376, 1911.01470, 2606.12540
- `C_T` from the bootstrap: 2411.15300 (3d Ising `c_T/c_free = 0.946538675(42)`), 1307.6856, 1504.07997
- BMMS / `C_D(n)`: 1511.06713 (holds for free fields), 1602.08493 and 1607.07418 (fails holographically)
**Flagged by the agents as possibly misidentified:** a "certified 3d Ising exponents" EPJB 2026 paper (its arXiv ID was conflated with 2312.07866); a "σ_f = 2σ_s with boundary" claim (source not found).
