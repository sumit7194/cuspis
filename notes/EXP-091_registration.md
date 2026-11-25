# EXP-091 REGISTRATION (2026-11-26 ~03:50; nothing computed): grading Fable's seals S-c (and the gradeable clauses of S-a) [model: Opus 5.5]

*Seal: branch fable/2026-11-26-A-vs-bulk, c615773 (03:36:47), `notes/fable_AvB/SEALS_Sa_Sc.md`. It was committed before the addendum (960d2b8 is not an ancestor) and before any P = 12 GEOM file was opened. Fable's values are UNVERIFIED predictions, used only as predictions.*

## 0. Exposure (mine and Fable's)
- **Fable's (declared):** the BULK half of Δ_bb(3) is not blind. My EXP-089 message quoted Sigma3D(W6P12) = −140.23314 and Sigma3D(W12P12) = −158.44252 (D1(3) = 0.379362).
- **Blind:** X_cA at P = 12, the c_A map at P = 12 (interior ratio), and norm(3) (κ(3) not computed by anyone).
- **Mine:** I read Sigma3D from G_W6P12/G_W12P12 for EXP-089 (i). I have NOT read X_cA or cA from them. κ(3) has never been computed.

## 1. Definitions (Fable's notation; computed with 085c READ code verbatim where it exists)
- **Interior c_A/c (hi):** the 085c READ map. Mean of cA over sites with |x − Lx//2| ≤ 1 and |t − Lt//2| ≤ 1, divided by c_hi = −0.11410550636913405 (`exp085/E.json`, first end).
  - Computed from G_W12P12 AND G_W6P12. The map depends on P only, so they must agree to 1e-4 (C5). If they don't, both are graded and the seal must pass on both.
- **norm(3)** = 1/(Ny(1/W₁ − 1/W₂)κ(3)), with W₁ = 6, W₂ = 12, P = Ny/4 = 12, Wbox = 12. κ(3) comes from `exp081b_run.pair(free, 12, W1=6, W2=12, Wbox=12)`, the same call that gave norm(2.5) = 14.311992 (C2).
- **Raw quantities (no norm):**
  - y_A(3) = −(X_cA(W6P12) − X_cA(W12P12));
  - y_bulk(3) = −(c/2)(Sigma3D(W6P12) − Sigma3D(W12P12));
  - **raw g_b(3) = y_bulk − y_A** (hi c; lo c reported).
  - **Δ_bb(3) = −g_b(3)·norm(3).**
- **σ̇-weighted c_A/c** (per geometry) = X_cA / (½·c_hi·Sigma3D). Units are checked by C1b.

## 2. Grading rules (bands as sealed; Fable's own fail rules where stated)
| item | sealed | PASS iff |
|---|---|---|
| G1 interior c_A/c (hi), P = 12 | 0.826 ± 0.003 | ∈ [0.820, 0.832] (Fable's fail rule); also report whether it is inside ±0.003 |
| G2 Δ_bb(3), hi c | −3.89 ± 0.08 | **only if norm(3) ∈ [14.02, 14.42]** (Fable's guess 14.22 ± 0.20): ∈ [−4.05, −3.73] (Fable's fail rule) |
| G2′ raw g_b(3), hi c | 0.2735 ± 0.0030 | **graded IN PLACE of G2 if norm(3) ∉ [14.02, 14.42]; reported as secondary otherwise.** PASS iff ∈ [0.2675, 0.2795] |
| G3 y_A(3) | 0.7654 ± 0.0030 | ∈ [0.7594, 0.7714] |
| G4 σ̇-weighted c_A/c: W6P12, W12P12 | 0.8206 ± 0.0010; 0.8109 ± 0.0010 | each ∈ ±0.0020 |
| G5 Δ_bb(3) lo c; raw lo | −5.24 ± 0.11; 0.3689 | reported against ±2σ, labelled (no fail rule stated by Fable) |
| S-a clause 1 | Δ_bb(hi) decelerates | **S-a FAILS** if \|Δ_bb(3) − Δ_bb(2.5)\| ≥ 0.306 (Fable's clause; needs norm(3), any value) |
| S-a clause 2 | interior (1 − c_A/c_hi)·P stops rising linearly | **S-a FAILS** if the P = 10 → 12 increment of (1 − r)·P is ≥ 0.06, the P = 8 → 10 increment. (Operationalisation of "keeps rising linearly" is MINE; Fable's predicted value is 2.09.) |

- ±2σ for G2′, G3 and G4 is inferred from Fable's convention elsewhere in the same file (its fail rules for G1 and G2 are exactly ±2σ). This inference is labelled in the result.
- S-a's asymptotic claim (Δ_bb(hi) → −4.7 ± 0.6; no log k; the linear term ∝ (c_A∞ − c)) is NOT gradeable at k = 3. Only the two fail clauses are graded, and passing them does not verify S-a.

## 3. Controls (each can fail; run BEFORE any P = 12 X_cA/cA value is read; exit 1 = no grading)
- **C1a, map reproduction:** the interior ratio at P = 4, 6, 8, 10 reproduces the 085c READ output (0.5672, 0.6841, 0.7509, 0.7949) to 1e-4.
- **C1b, units:** Δ_bb(k) for k ≤ 2.5 from X_cA and Sigma3D reproduces the stored box-minus-bulk (hi) [−2.49199, −2.97652, −3.45065, −3.75667] to 1e-5.
- **C2, norm path:** the same `pair` call at P = 10 (W1 = 5, W2 = 10) reproduces `exp081d_results.json` κ(2.5) to 1e-12.
- **C3, non-blind part:** y_bulk(3) from the files equals Fable's 1.03891 to 1e-5 (it reproduces the exposure).
- **C4:** both P = 12 G files have `failed` empty/false.
- **C5:** the W6P12 and W12P12 interior ratios agree to 1e-4 (see §1).

## 4. Order
1. Commit this registration.
2. Commit the script.
3. Run it: controls, then grading.
4. Report to the Bridge only.

Cost: GEOM files exist, so the only compute is κ(3) (seconds to minutes, one core).

## Amendment 1 (2026-11-26 ~04:20; after run 1's C3 FAIL, before any grading; on the Bridge's word)
- **C3′ replaces C3.** Expected = ½·48·|c|·D1 on the inputs AS TYPED in Fable's seal: c = −0.11411 (seal line 19) and D1 = 0.379362 (line 7). That gives **1.0389359**.
  - Tolerance from their rounding: |c| ± 5e-6 and D1 ± 5e-7, so δy = 24·(0.379362·5e-6 + 0.11411·5e-7) = **4.69e-5**.
  - PASS iff |y_bulk(3)_file − 1.0389359| ≤ 4.69e-5. The file value 1.0388953 differs by 4.07e-5, so it PASSES, thinly. Fable's printed 1.03891 (diff 2.6e-5) is consistent too.
- **Correction to run 1's write-up (report 320e5fe):** I computed the "expected" value with the code's full-precision c_hi (−0.1141055), not Fable's typed −0.11411. So my claim that Fable's 1.03891 was a last-digit slip is WRONG and is withdrawn (Bridge's catch). Fable's number is right to its quoted precision.
- **Slip (logged):** a control clause with a tolerance (1e-5) below the precision of typed inputs. It is the same class as the EXP-085 typed-constant amendment and L6. A second slip in my first diagnosis: inputs not taken as typed.
- Nothing else changes: no band, and no other control.
