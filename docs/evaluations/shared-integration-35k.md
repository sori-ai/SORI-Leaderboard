# Sori Shared Integration 35k

Added 2026-11-03; original evaluation 2026-10-24. Current shared-integration research reference, not a product release. The frozen 35k candidate uses its preserved 15k reference publication path.

## Evaluation

Official MAESTRO v3 test split, all 177 complete tracks. Results are unweighted track-level means, not pooled-note scores or development-set results.

- Note F1: **96.816661%** (precision 98.468134%, recall 95.275539%).
- Note + Velocity F1: **87.021734%**.
- Note + Offsets F1: **85.534142%**.
- Note + Offsets + Velocity F1: **76.973485%**.

All 177 original saved prediction SHA-256 values were verified, and six stored metric series reproduce the original aggregate. No new inference or scoring was performed. Unavailable precision/recall values are not inferred.

Onset tolerance is 50 ms; pitch tolerance is 50 cents. Offset tolerance is `max(0.2 × reference duration, 0.05 seconds)`. Velocity uses per-track reference-range normalization, least-squares predicted-velocity calibration and absolute normalized error below 0.1. Predictions retain the original continuous autoregressive decoder/publication path with 400-frame chunks.

Reference events come from saved five-state labels converted to notes (20 ms/frame, relative pitch + 21). Exact original-MIDI pedal/timing equivalence and the historical `mir_eval` package version are unverified. Exact protocol equivalence with historical leaderboard rows is therefore not established.

## Provenance and limits

- Candidate checkpoint SHA-256: `424826a13ea40117b625ba926f53720552096a789d4eaace4ef99fe52d35b842`.
- Reference checkpoint SHA-256: `b14a34920c8fe35543ccabfb573441b9e06a19246171018786c8574f90108205`.
- Evaluation source: `e1be176f2231953c8a30148768acaaed4049011b`.
- Scorer SHA-256: `deeedc64f7e6b1935753a69e69da94ae4b54b28356793048a5534aa8adf04b27`.
- Prediction manifest SHA-256: `7593009a852e1ce57784f6e15faf7155b24777962844cc4eea8293d58392d46c`.

Active-path parameter count and full-path latency are unverified. The two resident graphs total 2,123,258 parameters, but inference bypasses some modules. Nominal frontend support is 104 ms (centered FFT plus two future frames); this is not a complete note-emission delay and is not plotted as one.
