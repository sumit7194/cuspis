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

## L3 (2026-11-24): bound how far the one variable can move the result BEFORE registering a prediction about it
- **Failure:** 085w2b changed s_cut 3 → 6 in route (ii) at n = 2 and predicted that Level-1 dev would drop. The result was bitwise identical. At integer n the pole tails above s_cut enter with weight e^(−2πns) ≈ 4e-17 (n = 2, s = 3), so the change could not act. The registered "FAIL" was uninformative about the change.
- **Same class as** "a check that cannot fail" and "show the ansatz contains the answer": a variable that cannot reach the result tests nothing.
- **Rule:** before registering a one-variable test, write the variable's largest possible effect on the measured quantity (an order-of-magnitude bound from the code's weights). If the bound is below the precision or below the effect to be explained, the test is not run as a test of that mechanism.

## L4 (2026-11-24): a model-shape row must be able to tell apart the shapes the mechanism itself predicts
- **Failure:** 085c's "1/a² row" (a k² coefficient over 4 k) was registered after the c_A/c map was anticipated to vary like 1 − α/P. That predicts 1/k curvature, which a k² fit reads as c₂ > 0. The row "failed" for what is post-hoc likely an O(a) effect. The row's premise ("R has no k² content") was also unchecked; raw R has c₂ = −0.20.
- **Rule:** before registering a shape test, (i) list the shapes the mechanism and the finite-size corrections predict (here k², 1/k, constant), and confirm the test separates them with the available points and dof; (ii) run the same test on the UNCORRECTED data to check its premise; (iii) ask "what else lands here?".

## L5 (2026-11-24): a cost projection from one scaling step must carry an explicit upper bracket
- **Failure:** 084c amendment 2 projected W4P8 at 5.1–5.8 h from P^4.1–4.3, an exponent fitted to ONE P step (P 4 → 6). W4P8 overran 7.8 h (≥ P^4.7). The dense-algebra asymptote N³·Ny ∝ P⁷ was argued only after the fact.
- **Rule:** any projection that rests on a single step states the asymptotic bound of the algorithm as its upper bracket (here P⁷, from N = Lx·Lt ∝ P², dense N³, ×Ny ∝ P). Schedules are planned against the bracket, not the point estimate.
