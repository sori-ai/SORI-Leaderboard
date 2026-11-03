# Recent offline evaluation

The August 2026 evaluation covers all 177 full recordings in the MAESTRO v3
test split (about 19.98 hours). It reports the mean of per-recording onset F1
values, using one-to-one same-pitch matching with a 50 ms onset tolerance.

| System | Original GT onset F1 (%) | T2-cleaned GT onset F1 (%) |
|:-------|-------------------------:|---------------------------:|
| TransKun 2.0.1 (Stock) | 98.38493 | 98.51155 |
| SORI Current | 98.37483 | 98.51924 |
| Sori-Ensemble (raw Current + Stock UNION) | 98.57212 | 98.69965 |

Sori-Ensemble retains Current notes and adds Stock notes unmatched within
50 ms. It uses two models and is an offline system. Under the T2 protocol,
2,404 identified erroneous notes are removed from the original key-release
reference MIDI; predictions are not filtered. Original-GT and T2 scores are
therefore separate evaluation conditions.

For T2, the UNION's macro precision and recall are 99.40293% and 98.02042%;
the Stock baseline's are 99.77593% and 97.31078%. The improvement comes with
a precision trade-off. This test set has been used in previous development
and analysis, so the results should not be treated as an untouched final test.
The historical leaderboard does not document its aggregation and reference
processing sufficiently to establish direct comparability.

These figures measure onset detection only. They do not establish offset,
velocity, pedal, latency, or device performance. The evaluation is not a claim
about a deployed API configuration.

## Decoder experiments (October 2026)

These experiments use the same Current checkpoint without retraining. They are
research results and do not establish the behavior of a deployed service.

| Evaluation and system | Macro onset F1 (%) | Note-micro onset F1 (%) |
|:----------------------|-------------------:|------------------------:|
| T2 test 177: Current baseline | 98.51937 | 98.21208 |
| T2 test 177: Current + weak onset-peak bonus | 98.55232 | 98.24979 |
| Validation 89: Current baseline | 98.10493 | 97.83799 |
| Validation 89: + weak onset-peak bonus | 98.13562 | 97.87332 |
| Validation 89: + weak onset-peak bonus and seam fix | 98.18129 | 97.90396 |

Both cohorts contain full recordings. The T2 test uses the cleaned key-release
reference described above; the validation reference extends notes with sustain.
The peak bonus improves onset recall while lowering precision: on T2, micro
precision changes from 99.46889% to 99.35387%, and recall from 96.98663% to
97.16998%. On validation 89, adding the seam fix to that bonus improves both
micro precision and recall, though the rule can merge a genuine reattack at a
segment boundary. The seam rule was motivated by T2 examples; these results are
not an independent final test of that rule. The T2 result for the peak bonus
alone is not a result for the peak bonus plus seam fix.

A different selective onset correction was also evaluated with UNION on the T2
test: Current macro onset F1 improved from 98.51937% to 98.52664%, while its
paired UNION changed from 98.69974% to 98.68819%. This correction is distinct
from the weak peak bonus above. The weak peak bonus was subsequently evaluated with the ensemble below. The
combined effect of that bonus and the seam fix on the ensemble has not yet been
established; Current's improvement cannot be substituted for a UNION result.

## Full-test note attribute evaluation

In November 2026, saved Current and Stock predictions were combined and scored
on all 177 full MAESTRO test recordings. Both systems below use the same Stock
predictions; the second uses the previously evaluated weak onset-peak bonus on
Current. The seam fix is not included. The numbers are song-level macro F1 (%).

| System | Reference note end | Note | Note + velocity | Note + offset | Note + offset + velocity |
|:-------|:-------------------|-----:|----------------:|--------------:|-------------------------:|
| Sori-Ensemble | Original key release | 98.57221 | 97.91850 | 42.96816 | 42.79684 |
| Sori-Ensemble | Sustain-extended | 98.57221 | 97.91850 | 93.41812 | 92.84823 |
| Sori-Ensemble + weak peak bonus | Original key release | 98.56710 | 97.90197 | 42.95592 | 42.78268 |
| Sori-Ensemble + weak peak bonus | Sustain-extended | 98.56710 | 97.90197 | 93.45286 | 92.86766 |

The sustain-extended reference retains the original notes and velocities and
extends their endpoints using sustain pedal events. Pitch and onset are matched
one-to-one within 50 ms; offset tolerance is max(50 ms, 20% of reference note
duration). Velocity scoring follows `mir_eval.transcription_velocity`: an
affine fit per recording and normalized velocity tolerance of 0.1. Scores are
means of per-recording F1, not pooled note-level F1. The matching and velocity
implementation was checked against `mir_eval` on a representative recording.

The baseline is reconstructed from saved MIDI predictions, with UNION combined
in memory; it was not serialized to MIDI and read back after combining. Its
original-GT onset F1 (98.57221%) differs slightly from the historical evaluation
above (98.57212%); these are separate evaluation runs. Weak peak improves the
sustain-extended offset scores but slightly lowers onset and velocity scores.
The reference processing for historical leaderboard rows is not fully known,
so direct comparison of the offset and velocity values is not established.
