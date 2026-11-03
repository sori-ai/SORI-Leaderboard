# Sori Native 35k

Evaluated 2026-11-03 on all 177 MAESTRO v3 test tracks. The frozen 35k candidate is evaluated through its own note decoder, with no 15k reference, completed-note merge, or online join. This is a research result, not a product release.

Results are unweighted track-level means. Verified original pre-merge native states and velocities were reused with the original decoder, GT, time shift and scorer; each native prediction was scored once. No neural inference was repeated. Previous merged results are not the values reported here.

| Metric | F1 | Precision | Recall |
|:-------|---:|----------:|-------:|
| Note | 96.745756 | 99.328412 | 94.389804 |
| Note + Velocity | 77.314041 | 79.402417 | 75.409278 |
| Note + Offsets | 80.580937 | 82.721258 | 78.628136 |
| Note + Offsets + Velocity | 65.210362 | 66.953850 | 63.619670 |

Onset tolerance is 50ms; pitch tolerance is 50 cents. Offset tolerance is `max(0.2 × reference duration, 0.05 seconds)`. Velocity uses per-track reference-range normalization, least-squares calibration and normalized error below 0.1. The 740,399 reference notes are preserved; onset counts are TP 689,599, FP 5,558 and FN 50,800 (not the macro averaging denominator).

Reference events were converted from five-state labels (20ms/frame, relative pitch +21). Exact original-MIDI pedal/timing equivalence and the historical mir_eval version are unverified; exact protocol equivalence with other historical rows is not established.

## Model size and delay

The executed native path contains **853,807 parameters across 132 tensors**. The training graph contains 1,061,629 parameters; the unused reference branch is excluded from the active count.

Model lookahead is **204ms**: centered FFT 64ms + temporal CNN 40ms + pitchwise temporal layers 60ms + future adapter 40ms. Finite lookahead is part of the real-time design. Input-call rounding adds up to 16ms separately; hardware processing and queue latency are not measured. The figure plots model lookahead, not measured end-to-end device latency.

The retained inference used 400-frame acoustic chunks. CPU finite-support checks and causal recurrent decoding support the bounded-context interpretation; this result is not a new 177-track live transport benchmark, and continuous-window boundary outputs are not claimed identical to the retained chunked outputs. No future completed reference-note interval is used to accept or retract a native note.

## Provenance

- Checkpoint SHA-256: `424826a13ea40117b625ba926f53720552096a789d4eaace4ef99fe52d35b842`.
- Original inference source: `e1be176f2231953c8a30148768acaaed4049011b`.
- Original scorer SHA-256: `deeedc64f7e6b1935753a69e69da94ae4b54b28356793048a5534aa8adf04b27`.
- 177 original pre-merge native outputs were verified. Native device-set results have not been measured; prior merged scores are not inherited.
