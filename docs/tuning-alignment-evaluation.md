# Tuning correction on Catalog recordings: score-alignment pilot

This is a research pilot on naturally recorded piano audio; no artificial tuning
shifts were introduced. The original 20 selected segments came from 19 video
IDs. Each model output was aligned independently to the same MusicXML score for
its recording; the historical automatically transcribed MIDI was **not** used as
the evaluation reference.

Of the 20 segments, 16 had completed alignments for all four conditions and
used score files whose hashes matched the frozen experiment input. Three had at
least one held alignment, and one had a score-version hash mismatch. These are
not a random sample; a model may be more likely to have its alignment held when
its transcription is poor. Consequently, the completed-only comparison may be
biased. Current service score revisions were not independently verified.

A same-pitch alignment link to a distinct score note counts as a matched score
note; at most one prediction counts per score note. Unmatched score notes and
unmatched or duplicate predictions are proxy FN and FP. Score coverage is
matched score notes divided by score notes. Macro values below are the mean of
segment-level scores; counts are summed. A score-linked note is not an
independently verified audio label: missed alignments, omitted or repeated
notes, different performances, and unnotated ornaments can all affect these
numbers. The score-based matching procedure can itself behave differently for
different predictions. Offset and velocity accuracy were not assessed.

| Model and tuning | Macro score coverage | Macro F1 | Proxy FN | Proxy FP |
|:-----------------|---------------------:|---------:|---------:|---------:|
| TransKun, tuning OFF | 88.77% | 90.95% | 1,916 | 692 |
| Sori-Ensemble, tuning OFF | 93.34% | 94.48% | 1,129 | 777 |
| TransKun, tuning ON | 95.60% | 96.11% | 774 | 625 |
| Sori-Ensemble, tuning ON | 95.57% | 95.89% | 787 | 748 |

Tuning ON uses the same SORI Current-derived tuning estimate for both models;
therefore this is not an independently estimated tuning baseline for TransKun.
The correction gate can leave individual recordings unchanged. Within this
selected aligned subset, the OFF comparison has higher Ensemble coverage; the
ON coverage values are similar. These results do not establish superiority on
a representative population or prove acoustic false-positive/false-negative
counts.

As an exploratory example, the audio-only tuning estimator reported about
+44 cents for one Bach WTC No.19 Fugue segment. Against 1,190 score notes,
coverage was 26.22% for TransKun OFF, 74.20% for Ensemble OFF, 98.07% for
TransKun ON, and 98.32% for Ensemble ON. The tuning estimate is not an
independent calibration, and the score links have not been adjudicated by
listening. This is a selected example, not a population average.

The selected segments, predictions, score hashes, alignment holds, and per-case
results are recorded in the associated internal experiment artifacts. A
separate 18-recording full-performance comparison uses another cohort; do not pool the two sets without establishing common
sources and evaluation conditions.
