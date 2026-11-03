# Sori-Ensemble offline evaluation

Sori-Ensemble combines SORI Current and TransKun 2.0.1 (Stock) predictions,
using the weak onset-peak bonus and the unfinished-note segment-boundary fix on
Current. It is an experimental offline two-model system.

The evaluation covers all 177 full recordings in the MAESTRO v3 test split.
It reports per-recording macro F1 (%):

| System | Note | Note + velocity | Note + offset | Note + offset + velocity |
|:-------|-----:|----------------:|--------------:|-------------------------:|
| Sori-Ensemble | 98.71075 | 98.04305 | 93.68190 | 93.09061 |

The T2 reference is built by removing 2,404 audited erroneous notes from the
original MIDI, then extending the remaining note durations using CC64 sustain
pedal events. Each excluded note was uniquely matched to an original MIDI note
using pitch, onset and velocity. Across all 177 tracks, retained note count,
onset, pitch and velocity were checked against the T2 key-release reference.

Notes are matched one-to-one by pitch and onset within 50 ms. The offset
tolerance is the greater of 50 ms and 20% of reference note duration. Velocity
scoring follows `mir_eval.transcription_velocity`, with a per-recording affine
fit and normalized tolerance of 0.1. Stock predictions are saved MIDI; the
ensemble is combined in memory. Machine-readable results: [T2 sustain evaluation](../data/benchmarks/t2-sustain-results.json).

The seam rule was motivated by examples from this test set, so this is not an
independent final test of that rule. It could merge a genuine reattack at a
segment boundary. The test set has also been used in previous research. The
historical leaderboard's reference processing and aggregation are not fully
documented, so direct comparison is not established. These experimental results
do not establish deployed API behavior.

Current inference used three RTX 3090 GPUs with the same checkpoint and decoder
source as the prior experiments. Test audio was verified against source SHA-256
for all 177 recordings. A representative recording without the seam fix
reproduced the earlier peak-bonus MIDI exactly for pitch, onset, offset and
velocity. The three seam outputs covered 177 distinct tracks, and their
transferred MIDI hashes were verified before scoring.
