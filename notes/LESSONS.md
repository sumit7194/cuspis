# Lessons ledger (Cuspis; failure-driven, newest last) [model: Opus 5.5]

## L1 (2026-11-23): an end-to-end test must run EVERY phase on the stored files the real run reads
- **Failure:** EXP-085 B–E run 1 crashed in 5 s in phase B. The real `exp081d_results.json` stores `S_W1`/`S_W2` as dicts (the value under `S_T0`); the code subtracted the dicts.
  - The "synthetic end-to-end test" drove phase E only, with synthetic inputs, so phase B's read of the real file was never exercised.
- **Same class as** the EXP-085 planted-κ slip (planted value 7.045… derived from a typed κ rather than the stored one). In both, the test fed inputs other than the stored ones.
- **Rule:** an end-to-end test runs ALL phases (A–E, not only the phase under study). Synthetic data replaces only the expensive computed quantities. Every stored input (exp081d_results.json, A4.json, sigma files) is read from the real file, in its real shape, through the same code path.
- **Check:** before calling a test "end-to-end", list every file the real run opens. Each must be opened by the test too.

## L2 (2026-11-23): chain on the predecessor's SUCCESS, not its PID exiting
- **Failure:** part 8 waited only on part 7's PID. When part 7 crashed, part 8 went straight to its pressure gate; only the gate's 300-s wait kept 084c compute from starting ahead of the registered order.
- **Rule:** a chained runner starts only on a completion marker the predecessor produces solely on a clean exit (its own "rc 0" line AND its expected result file, fresh and of the right amendment). Anything else → STOP → HOLD, and the Bridge is told.
- **Check:** test the gate with planted predecessors (crash, controls-fail rc 1, stale result, wrong amendment, an "rc 10" prefix trap) plus the true case, before relying on it. Done for `run_queue8.sh` (all five blocked, true case passes).

## Related standing rules (recorded earlier in report.md)
- Never chain a registration commit with a data run.
- Test a waiter's condition on a true case first.
- Memory caps come from measured full peaks only, never from scaled guesses.
- Expected values in controls come from the exact stored inputs the code reads, never from typed or rounded constants.
