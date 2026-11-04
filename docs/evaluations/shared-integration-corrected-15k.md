# Sori Corrected 15k

The existing A15k checkpoint retains the original bounded PA, offset, dynamics, pitch, rescue and refiner corrections. Its standalone output does not use completed-parent-note interval merging. This checkpoint uses the single shared-backbone integration architecture with its trained correction branches. It does not automatically incorporate newer models developed independently for each task. This is a research comparison; selection across the remaining best-model candidates is ongoing.

All 177 MAESTRO v3 test tracks were verified against the fixed reference-event arrays. Existing scalar results were reused; missing ordered pairs and velocity metrics were completed on CPU without neural inference.

| Metric | F1 | Precision | Recall |
|:-------|---:|----------:|-------:|
| Note | 96.734854 | 98.532998 | 95.062281 |
| Note + Velocity | 86.988323 | N/A | N/A |
| Note + Offsets | 85.482125 | 87.055223 | 84.018594 |
| Note + Offsets + Velocity | 76.957538 | N/A | N/A |

Values are unweighted track-level means. Onset tolerance is 50ms, pitch tolerance 50 cents, and offset tolerance max(20% of reference duration, 50ms). Velocity uses per-track reference-range normalization, least-squares calibration and normalized error below 0.1. The reference contains 740,399 notes; predictions contain 707,940 notes, with onset TP 695,683, FP 12,257 and FN 44,716. Counts are not the macro averaging denominator. Exact protocol equivalence with other historical leaderboard rows is not established.

## Model size and delay

The original checkpoint has **1,051,293 active parameters**, verified with the existing operation-level trace and original-source binding; the registered graph contains 1,061,629 parameters.

The plot uses **344ms source-derived model lookahead**: 204ms raw acoustic support (64ms FFT + 2 CNN frames + 3 pitchwise frames + 2 adapter frames, at 20ms/frame), plus max(7 rescue-age frames, 2 pitch-neighborhood + 2 neutral-neighborhood frames) × 20ms. Rescue arrival is max(age, 2), not age + 2.

This is static dependency support, not measured device latency or a verified 344ms online publication schedule. The original evaluator collected whole-piece arrays and decoded on CPU; equivalence across arbitrary streaming chunks has not been established. Packet rounding, computation and queue time are separate. Finite lookahead is allowed by the model design; no future completed-parent-note interval join is used.

## Provenance

- Corrected checkpoint SHA-256: `b14a34920c8fe35543ccabfb573441b9e06a19246171018786c8574f90108205`.
- Original public source: `e849c844368fe73992fa652eba8db34e3da4f2c4`.
- Original training source: `68f70ed4c2a5f0ae25c03ab8de2f90822b950318`.
