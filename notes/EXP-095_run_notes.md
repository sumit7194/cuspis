# EXP-095 run notes (sealed-read; memory and time columns only) [model: Opus 5.5]

## 2026-11-26 21:48: the W4P10 3 GB hold fired on a measurement error

- **What fired:** peak_hold.sh read the watchdog's TREE column, 3.066 GB ≥ 3 GB, and SIGSTOPped the real W4P10
  (corner_function_095b, PIDs 33459/33463). The Bridge ruled: keep it paused until W2P10 ends.
- **Why it fired (verified, `scripts/exp081d_results/exp095_memtest_footprint.txt`):**
  - The watchdog logs TREE = top MEM + top CMPRS.
  - On macOS, top's MEM is the kernel phys_footprint, and that already INCLUDES compressed memory.
  - So TREE counts compressed pages twice.
  - The controlled test: a 400 MB process kept MEM = phys_footprint = 405 MB while macOS compressed 295 MB of it.
  - At the hold, W4P10's true footprint was 1.896 GB (the MEM column). The kernel's high-water mark is
    phys_footprint_peak = 2.126 GB.
- **Scope of the bug:** every TREE number since the watchdog began (holds, declarations, report peaks) is overstated by the compressed
  part. On a roomy machine with little compression this is small; on the Air it is ~40-60 %. Hold thresholds set in TREE units fire early.
  Pause-only, so this was never unsafe, but the numbers are wrong.

## Declaration miss

- **Declared peak for W4P10: 1.52 GB.**
  - It came from W2P10's FIRST HOUR (install/t0 phase, TREE units).
  - I did not use the full same-lattice runs W5P10b10 / W10P10b10 that were already in the repo. At P = 10, box 10 the lattice
    (Lx = 30, Lt = 20, Ny = 40) does not depend on W.
- **Measured:**
  - W4P10 kernel peak 2.126 GB (true), +40 % over the declaration;
  - TREE 3.066 GB (overstated), 2.0x the declaration.
  - W2P10 kernel peak 1.953 GB, +28 %.
- The miss is real in true units (+28-40 %). The "2x" was mostly the accounting bug.

## Memory model (true footprint = MEM column / phys_footprint)

Same lattice for all W at P = 10, box 10. The phases come from the .out timestamps of the old Mac runs
route_W5P10b10 / route_W10P10b10 (EXP-081d, not blind). Max MEM per phase:

| phase | W5P10 (Mac) | W10P10 (Mac) |
|---|---|---|
| install | 0.97 | 1.01 |
| t0 | 1.48 | 1.52 |
| 48 g nodes | 2.12 (first quarter), then 1.99 | 2.16, then 1.98 |
| planted | 2.00 | 2.03 |
| B2b | 2.03 | 2.07 |
| N1'''c + Woodbury (end) | **2.16** | **2.21** |

- The Air runs sit in the same bands so far:
  - W2P10's MEM max is 1.90 GB, kernel peak 1.95 GB, in the g-node phase (4 nodes at 21:53).
  - W4P10 jumped from 1.45 to 1.90 GB at the t0 → g-node step, the same step every run shows; its kernel peak is 2.13 GB.
- The 10 s samples undershoot the kernel peak by 0.05 (W2P10) and 0.23 GB (W4P10).
- **PREDICTION (written 2026-11-26 ~22:10, before either run reaches its checks):**
  - the true peak of each run, W2P10 and W4P10, is 2.25 GB central and **≤ 2.45 GB** upper;
  - it is reached at the end (N1'''c / Woodbury) or at the first g node.
  - Falsified if either run's phys_footprint_peak exceeds 2.45 GB.
  - Grade: partially verified (an inference from same-lattice references, consistent so far with both Air runs).
- **Hold for the W4P10 resume:** predicted 2.45 × 1.25 = **3.06 GB TRUE (MEM column)**. The Air has room: true usage beside the routes is
  ~1.5 GB (WindowServer 0.54 GB, Quantum chunks not in the top 14).
- **W2P10 and its own hold:** its live hold (peak_hold 27442) reads TREE at 3 GB. TREE already touched 3.039 GB once at t = 13813 s,
  for one 10 s sample; the 30 s poll missed it. In the late phases TREE on the Mac reached 3.0-3.2 GB. So the W2P10 hold is LIKELY to fire
  falsely before W2P10 ends, while its true footprint is ~2.0-2.2 GB.
- **W2P10 ETA from node counts:** nodes 1/2/3/4 at the pulls of 19:53/20:53/21:23/21:53, so ~30-40 min per node. 44 nodes are left, plus
  the checks, so it ends ~28 Nov 00:00-04:00, not 16:30 on 27 Nov. It may be faster now that W4P10 is paused.
