# Recent offline evaluation

The August 2026 evaluation covers all 177 full recordings in the MAESTRO v3
test split (about 19.98 hours). It reports the mean of per-recording onset F1
values, using one-to-one same-pitch matching with a 50 ms onset tolerance.

| System | Original GT onset F1 (%) | T2-cleaned GT onset F1 (%) |
|:-------|-------------------------:|---------------------------:|
| TransKun 2.0.1 (Stock) | 98.38493 | 98.51155 |
| SORI Current | 98.37483 | 98.51924 |
| Raw Current + Stock UNION | 98.57212 | 98.69965 |

The raw UNION retains Current notes and adds Stock notes unmatched within
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
