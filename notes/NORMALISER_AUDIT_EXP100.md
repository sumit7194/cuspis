# Normaliser audit after EXP-100 (2026-11-28, the Bridge's ask) [model: Opus 5.5]

**Finding (EXP-100 part A, 5bd59ac).** Convention A (Lt = 2P, Ny = 4P, unequal gaps) gives κ_lat(P/2, P)/κ_free = 0.4454 / 0.4475 / 0.4325 at k = 1 / 2 / 3. So every R = δκ_lat/κ_lat that uses the same-geometry κ_lat is about 2.2–2.3 × R_D = δκ_lat/κ_free.

**Mark applied:** "Normaliser: convention A, IR-unconverged; superseded by EXP-100". Entries were annotated in place and their text left unchanged. Registrations are frozen and were not edited; they are listed here.

## What changes and what does not (descriptive; σ not propagated)

| k | κ_lat,A | R^c_T0 (EXP-090) | R_D = R^c_T0 · κ_lat,A/κ_free |
|---|---|---|---|
| 1 | 0.017660022 | 2.2552 | 1.0045 |
| 1.5 | 0.018206102 | 4.2334 | 1.9440 |
| 2 | 0.017743046 | 6.5877 | 2.9481 |
| 2.5 | 0.017467869 | 9.0902 | 4.0049 |
| 3 | 0.017147713 | 11.7582 | 5.0854 |

- κ_lat,A was recomputed with `exp081b_run.pair` (the exp098_3w `kappa` expression).
  - Against the stored values: bitwise at k = 1, 2; within 5e-8 of the printed 0.0171477 at k = 3.
  - It reproduces norm(2.5) = 14.311992.
- **Absolute values** (R(k), extrapolations such as "R(3) ≈ 9.2–9.9", counterterm sizes such as Y_A in R units) all scale by κ_lat,A/κ_free ≈ 0.43–0.45.
- **Ratio and shape statistics** (the 081d r and p, ρ_s, the wall fractions f, the width drift D/R) change only through the 6% k-spread of κ_lat,A.
  - Headline check: the 081d PRIMARY r = [R(3) − R(1.5)]/[R(2) − R(1)] goes 1.7368 (R^c) → 1.6163 (R_D). Both are in the power-divergent band (≥ 1.33).
  - Other ratio statistics are NOT re-derived here (unverified).
- **δκ_lat itself is IR-unconverged at convention A** (EXP-099: the σ slope drifts 9–11%). So R_D,A is not a continuum estimate either. Part B of EXP-100 tests the σ side's IR sensitivity at k = 1.

## Records that used the same-geometry normaliser

**report.md** (35 entries, each marked in place; found by a pattern search for R values and definitions, so an entry that states R only in words could be missed; grade **partially verified**):
- EXP-081, EXP-081a: EXP-081 rung geometry, not convention A. Same-geometry κ_lat; IR status never measured. Marked with that variant.
- EXP-081b registration and result (R(P) = 2.2552 … for P = 4…12).
- EXP-083 and EXP-083 R1 (R(4) → δQ′).
- EXP-081c post hoc.
- EXP-081d: §A, §B, §E, amendment 1, the Stage-1 end, the Stage-2 census, the RESULT (R(k) = 2.255, 4.233, 6.442, 8.219).
- Pre-R(3) note; 081e outcome table.
- EXP-084 registration and result.
- Neon T54 note; EXP-085 draft, amendments and B–E.
- t0-defect entry (ΔR(2), ΔR(2.5)).
- EXP-090 registration; k ≤ 2.5 result; k = 3 result (R^c_T0 series, (R2) ρ_s, (R4) power-divergent).
- EXP-091; EXP-087 W12P12 gate check.
- EXP-096 W8P8, step 2 and W12P12 (materiality in R units).
- DIGEST 2026-11-28; CORRECTION to the k = 3 checklist and digest.
- EXP-098 stage 0 result; EXP-099 result.

**Top-level documents:**
- `STATUS.md` line 5 (R(k) series): marked, with the R_D series added.
- `WRITEUP_dkappa_settled.md` (2026-11-21): checked. **No R value, and no same-geometry normaliser.** It states "the number δκ is not computed" and gives κ_free = 0.0396481. Not affected; not marked.
- `RESULT.md`, `README.md`, `DIGEST_EXP040-043.md`, `PHASE2.md`, `BACKLOG.md`, `SHARED_BACKLOG*.md`: checked. No δκ R values. Not affected.

**Briefs sent to other model sessions (marked):**
- `notes/fable_brief_A_vs_bulk.md` (R(k) table), `notes/fable_brief_A_vs_bulk_ADDENDUM_wall.md` (R at n = 1, 2), `notes/fable_brief_n2_tension.md` (R shifts): these went to Fable.
- `notes/T55_neon_prompt_draft.md` (R definition; Neon, relayed by the Bridge).
- Whether each was actually sent, and in which version, is the Bridge's record, not mine.

**Registrations (frozen; NOT edited; listed):**
- notes/EXP-081c_draft, 081d_refinement_draft, 081e (both), 084 (both), 084b (both), 085 (both), 085c (both), 087 (both), 090, 098, 099.
- All define R with the same-geometry κ_lat. EXP-100 supersedes the normaliser (its §0 / part D).

**Data and code:** the stored JSON outputs (exp090_*.json, exp081d results, exp098_stage0.json) carry R values computed with κ_lat. They are left as computed; this register is their mark.

## Outside the repo
- **The GitHub repository `cuspis` is PUBLIC.** Every pushed R value has therefore been publicly readable since its push.
- I find no preprint, Zenodo deposit, DOI or email in the repo or in my session record.
- I have sent nothing outside except git pushes and the Bridge's cross-session messages.
- I cannot see messages sent by other sessions or by Sumit.
