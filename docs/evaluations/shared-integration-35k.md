# Sori Shared Integration 35k — MAESTRO v3 test

Published 2026-11-03. Original evaluation: 2026-10-24.

This is the current shared-integration **research reference**, not a new product release or a claim of improvement in every metric. The frozen 35k candidate is evaluated with its preserved 15k reference publication path. The result is not the standalone native head's score.

| Metric | F1 (%) | Precision (%) | Recall (%) |
|---|---:|---:|---:|
| Note (onset only) | 96.816661 | 98.468134 | 95.275539 |
| Note + Velocity | 87.021734 | N/A | N/A |
| Note + Offsets | 85.534142 | N/A | N/A |
| Note + Offsets + Velocity | 76.973485 | N/A | N/A |

The four F1 values are arithmetic means over **177 complete tracks**, not scores pooled across tracks or the 137-crop development set. Missing precision/recall fields were not present in the original six-metric record and are not inferred from F1. The original evaluation contains 740,399 reference notes and 710,459 predicted notes; onset matching yields 697,611 TP, 12,848 FP and 42,788 FN. These totals do not replace the macro averages above.

## Protocol

- Official MAESTRO v3 test split, all 177 tracks; batch size 1 per track, continuous autoregressive history with 400-frame processing chunks.
- Frame-to-time conversion: 0.02 seconds; relative pitch maps to MIDI pitch by adding 21.
- Onset tolerance: 50 ms. Pitch tolerance: 50 cents.
- Note F1 ignores offsets. Offset metrics additionally use `max(0.2 × reference duration, 0.05 seconds)`.
- Velocity uses the original mir_eval-compatible ordered matching, per-track normalization `(v - min(v)) / max(1, max(v) - min(v))` and least-squares calibration of predicted velocity, with absolute normalized error below 0.1. This is **not raw MIDI velocity MAE**.
- Frozen predictions, original decoder/publication and metric outputs are reused. No new inference, re-scoring, threshold search or test-based checkpoint selection was performed for this update.

## Verification and provenance

All 177 saved prediction files were checked against their original SHA-256 values. The six stored per-track metric series each contain 177 entries and reproduce the original aggregate. The public [verification record](../../data/evaluations/shared-integration-35k.json) includes per-track prediction/metadata hashes and the available stored metrics; it contains no private host paths or model weights.

- Candidate checkpoint SHA-256: `424826a13ea40117b625ba926f53720552096a789d4eaace4ef99fe52d35b842`
- Reference checkpoint SHA-256: `b14a34920c8fe35543ccabfb573441b9e06a19246171018786c8574f90108205`
- Evaluation source commit: `e1be176f2231953c8a30148768acaaed4049011b`
- Scorer SHA-256: `deeedc64f7e6b1935753a69e69da94ae4b54b28356793048a5534aa8adf04b27`
- Saved prediction manifest SHA-256: `7593009a852e1ce57784f6e15faf7155b24777962844cc4eea8293d58392d46c`

The historical leaderboard does not ship its original inference/scoring runner or fully specify velocity calibration, aggregation, pedal handling and timing corrections for every row. The new row therefore documents its own verified contract; exact protocol equivalence with every historical or literature result is **not established**. The repository's generation scripts format results rather than execute a separate benchmark.

## Parameters and latency

CPU reconstruction counts 1,061,629 registered parameters in the candidate graph and another 1,061,629 in its independently held reference graph (2,123,258 registered parameters in total). The candidate native submodule has 836,399 parameters. Registered graph totals are not a certified count of only the modules consumed by the evaluated publication path; the headline parameter field remains unavailable rather than substituting the native submodule count.

The frontend uses 16 kHz audio, a 2,048-sample centered FFT and a 320-sample hop. Its nominal right-context support is 64 ms from the FFT plus two frames (40 ms), or **104 ms**. This is not a measured complete note-emission delay, application latency or device real-time factor. Full-path delay is consequently marked **Not measured**, and this model is omitted from the latency plot.
