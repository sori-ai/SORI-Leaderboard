# 메트릭 정의

소리(Sori) 벤치마크에서 사용하는 평가 메트릭을 상세히 설명합니다.

## 요약 테이블

| 메트릭 | 설명 | 범위 | 높을수록 좋음? |
|--------|------|------|---------------|
| `note_f1` | 노트 검출 F1 스코어 | 0-1 | O |
| `note_precision` | 노트 정밀도 | 0-1 | O |
| `note_recall` | 노트 재현율 | 0-1 | O |
| `onset_f1` | 노트 시작점 F1 | 0-1 | O |
| `offset_f1` | 노트 종료점 F1 | 0-1 | O |
| `velocity_mae` | 벨로시티 평균 절대 오차 | 0-127 | X |
| `inference_time_ms` | 추론 시간 (ms/s) | 0-inf | X |

---

## Note F1 Score

**가장 중요한 지표**로, 전체적인 노트 검출 성능을 나타냅니다.

### 정의

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

### 매칭 기준

노트가 "정확하게 검출됨"으로 판정되려면:

1. **Pitch**: 정확히 일치
2. **Onset**: Ground Truth 대비 ±50ms 이내
3. **Offset**: Ground Truth 대비 20% 또는 50ms 중 큰 값 이내

### 해석

| 점수 | 해석 |
|------|------|
| 0.95+ | 전문가 수준, 거의 완벽 |
| 0.90-0.95 | 우수, 대부분의 노트 정확 |
| 0.85-0.90 | 양호, 일부 오류 존재 |
| 0.80-0.85 | 보통, 개선 필요 |
| <0.80 | 미흡 |

---

## Note Precision

**예측된 노트 중 정확한 비율**

```
Precision = True Positives / (True Positives + False Positives)
```

- 높은 Precision: 예측한 노트가 대부분 실제로 존재
- 낮은 Precision: 존재하지 않는 노트를 많이 예측 (False Positives 많음)

### 사용 시나리오

악보 자동 생성 시 Precision이 중요합니다. 틀린 음표가 악보에 포함되면 연주자에게 혼란을 줍니다.

---

## Note Recall

**실제 노트 중 검출된 비율**

```
Recall = True Positives / (True Positives + False Negatives)
```

- 높은 Recall: 실제 노트를 대부분 찾아냄
- 낮은 Recall: 많은 노트를 놓침 (False Negatives 많음)

### 사용 시나리오

피아노 튜터 앱에서는 Recall이 특히 중요합니다. 학생이 친 노트를 놓치면 정확한 피드백을 줄 수 없습니다.

---

## Onset F1

**노트 시작 시점의 정확도**

Pitch 일치 + Onset ±50ms 조건만으로 매칭합니다 (Offset 무시).

### 중요성

- 리듬감 평가에 핵심
- 음악적 타이밍의 정확성 측정
- 빠른 패시지에서 특히 중요

---

## Offset F1

**노트 종료 시점의 정확도**

Pitch 일치 + Onset 매칭 + Offset 조건으로 매칭합니다.

### Offset Tolerance

```
tolerance = max(note_duration * 0.2, 50ms)
```

### 중요성

- 레가토/스타카토 구분
- 페달 사용 시 노트 연장 감지
- 음악적 표현의 정확성

---

## Velocity MAE

**벨로시티(세기) 예측 오차**

```
MAE = mean(|predicted_velocity - ground_truth_velocity|)
```

### MIDI Velocity

- 범위: 0-127
- 0: 무음
- 64: 보통 세기 (mezzo-forte)
- 127: 최대 세기 (fortissimo)

### 해석

| MAE | 해석 |
|-----|------|
| <5 | 매우 정확, 다이나믹 재현 우수 |
| 5-10 | 양호, 대부분의 다이나믹 포착 |
| 10-15 | 보통, 세밀한 차이 놓침 |
| >15 | 미흡, 다이나믹 표현 부정확 |

---

## Inference Time

**1초 오디오를 처리하는 데 걸리는 시간 (밀리초)**

### 측정 조건

- GPU: NVIDIA RTX 3090
- Batch size: 1
- 워밍업 후 평균

### 실시간 처리 기준

```
실시간 배율 = 1000ms / inference_time_ms
```

| 시간 | 실시간 배율 | 해석 |
|------|-------------|------|
| 32ms | 31x | 모바일에서도 실시간 가능 |
| 100ms | 10x | 데스크톱에서 실시간 가능 |
| 500ms | 2x | 실시간 어려움 |
| >1000ms | <1x | 오프라인 처리만 가능 |

---

## 참고 자료

- [mir_eval Documentation](https://craffel.github.io/mir_eval/)
- [MIREX Evaluation](https://www.music-ir.org/mirex/wiki/MIREX_HOME)
- Hawthorne, C. et al. "Onsets and Frames: Dual-Objective Piano Transcription" (ISMIR 2018)
