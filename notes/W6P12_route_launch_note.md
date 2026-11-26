# Launch note: the W6P12 route rerun (EXP-081e / EXP-090 k = 3 input), 2026-11-26 ~23:25 [model: Opus 5.5]
*Sumit YES via the Bridge. Launch only after the Bridge's OK on this note. k = 3 stays SEALED until the route lands and the Bridge says read.*

## What runs
- **Command:** `exp081d_route.py 6 12 12 --tag-suffix _081e`. This is the registered rerun (run_081e.sh line 42).
  - Same env as the W12 route: CUSPIS_081E=1, CUSPIS_087 unset, 1 BLAS thread.
  - New checkpoint `sigma_W6_P12_box12_c2_cp12_sc3.0_dd0_081e_ckpt.json`. The HELD 2-key file stays untouched.
- **Runner:** `scripts/run_w6p12.sh`, with log `exp081d_results/run_w6p12.txt`.
- **Code since the W12 route started (24 Nov 21:26):** only sigma3d.py changed (6a2bd8c, EXP-087, behind CUSPIS_087, default OFF).
  - The W12 resume already ran with it OFF, and the K2 control there reproduced the stored t0 to 9e-16 relative.
  - W6P12 has no clusters, so ON and OFF are bitwise identical by construction (EXP-087 D1).
  - exp081d_route.py, exp081c_numerics.py and plant_guard.py are unchanged since 963c8f5.

## Memory prediction (TRUE units: MEM = phys_footprint)
- Same lattice as W12P12b12 (Lx = 36, Lt = 24, Ny = 48). At P = 10, the full runs W5 and W10 peaked within 2 % of each other.
- At t ≈ 1500 s, the killed W6P12 run showed 3.52 GB and the W12 route 3.47 GB: within 1.5 %.
- W12 route phase maxima (true): install 2.25; t0 3.69; first g node 5.05; g nodes 4.57-4.75; planted 4.65; B2b 4.72;
  N1'''c unrefined 5.295 (the peak); Woodbury 3.05.
- **Prediction: peak 5.3 GB central, ≤ 5.5 GB upper** (the upper allows for the kernel peak running above the 10 s samples:
  +0.09 GB seen on the Mac).
- **Hold: 5.5 × 1.25 = 6.9 GB TRUE, COL=3**, pause-only, no auto-resume.
  - Decoy-tested on a stand-in of this exact tree: MEM 5.40 / TREE 8.40 does not fire; MEM 7.00 fires.
  - It pauses only the watchdog and the route. The freepct guard, the backup and a same-argv decoy outside the root are untouched.
- The Mac mini has 16 GB.

## Gates (2026-11-24 list)
- ≥ 50 % free at launch; no other job of mine; fleet cores ≤ ncpu − 2; nice 12.
- Inform-only watchdog (the fixed TREE = MEM, a5ff03a), with pgate (pressure normal ≥ 300 s).
- freepct_guard v3: PAUSE below 30 % free for 60 s, resume at ≥ 40 % for 120 s, PID-scoped.

## Checkpoint plan (power cut)
- **The route checkpoints after every item** (install stats, t0, tsad, each of the 48 g nodes, each check), with an atomic tmp + os.replace.
  - A cut loses at most the item in progress.
  - Worst case: install + t0, ~2.8 h at W12, before the first t0 write.
  - After that, ≤ one g node (~35-48 min) or one check (≤ ~1.4 h, the N1'''c block).
- **Backup:** `tools/ckpt_backup.sh` every 30 min copies the checkpoint to `exp081d_results/ckpt_backup/`.
  - It keeps a copy only if the sha matches, the JSON parses and the key count does not fall.
  - Tested on dummy files: it keeps the last good copy on a fall and on broken JSON.
- **Resume after a cut:**
  1. Inventory, then verify the checkpoint: it parses, all values are finite, and its key count is ≥ the backup's. Otherwise use the backup.
  2. Pin its sha and tell the Bridge.
  3. On its OK, run `RESUME=1 SHA=<sha> TAG=e_route_W6_081e_r2 zsh run_w6p12.sh`. The route skips every key already present, and the logs get new names.
  - The Mac does not relaunch anything by itself.

## Time estimate
- W12 route compute ≈ 134.8 ks = 37.4 h: install 0.8 ks; t0 9.3 ks; 48 g nodes × ~2.3 ks; checks 12.8 ks.
- At P = 10, the narrower strip was 3 % faster (W5 47.6 ks against W10 49.1 ks).
- **W6P12 ≈ 36 h (range 35-40 h, longer if the Mac mini gets busier).** From a ~23:30 launch that is ~28 Nov 11:30 (10:30-15:30).

## Blinding
- Report-only views while it runs: rc lines, verdict words, key and node counts, memory and time columns.
- No .out tails: they print t0, tsad and S.
- At landing: the stale-file guard (mtime ≥ start, t0, tsad, 48 nodes, n1c, summary) and the sha only. The k = 3 read waits for the Bridge.
