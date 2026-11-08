# Long-note boundary postfilter evaluation

The existing 177-track Sori-Ensemble result predates the long-note boundary
postfilter. The new postfilter checks long Current-model onsets at inference
window boundaries against the preceding overlapping window and removes an
unsupported matching note only after decoding and merging. It does not use a
score. A true reattack can still be lost if both windows miss its onset.

The following onset-only experiments use one-to-one same-pitch matching within
50 ms. Only reference notes with velocity at least 32 count; unmatched
predictions that match lower-velocity reference notes are ignored. Macro F1 is
the mean of the per-recording or per-clip F1 values. FP and FN are totals.

| Population and system | Macro F1 before | Macro F1 after | FP before → after | FN before → after |
|:----------------------|----------------:|---------------:|------------------:|------------------:|
| Validation: 16 full recordings, Current | 99.04635% | 99.05983% | 472 → 459 | 1,608 → 1,608 |
| T2 test: 16 full recordings, Current | 98.85544% | 98.86188% | 468 → 462 | 1,738 → 1,738 |
| T2 test: 100 selected boundary-reattack clips, Sori-Ensemble | 99.27899% | 99.29023% | 31 → 30 | 76 → 76 |

The 100 clips were selected for a reference same-pitch reattack within 8 ms
of a boundary. Only their central four seconds were scored, excluding clip
edges. The baseline and postfilter both detected 148 of 151 targeted reattacks;
for pedal-down reattacks, both detected 91 of 92. These selected clips are not a
random sample or a 177-recording benchmark. Audio for Stock was resampled from
16 kHz. The test split has been used during earlier seam-rule development, so
these results are not independent held-out evidence.

In a separate 16-recording T2 test, 124 of 127 reference boundary reattacks
were detected before and after the change. No additional matched high-velocity
reference notes were lost. Full T2 reference construction is described in the
[177-recording evaluation](recent-offline-evaluation.md). The full
Sori-Ensemble benchmark with the new long-note postfilter has not been run.

The corresponding code change was merged in [sori PR #1422](https://github.com/sori-ai/sori/pull/1422).
These experimental measurements do not establish that a particular API service
is running that version.
