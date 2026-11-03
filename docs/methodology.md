# 평가 방법론

소리(Sori) Audio-to-MIDI 벤치마크의 평가 방법론을 설명합니다.

## 개요

Audio-to-MIDI (Automatic Music Transcription) 시스템의 성능을 공정하게 비교하기 위해 표준화된 평가 프로토콜을 따릅니다.

## 데이터셋

### MAESTRO v3

- **출처**: Google Magenta
- **규모**: 약 200시간의 피아노 연주
- **특징**:
  - 국제 피아노 대회 녹음
  - 고품질 MIDI-오디오 정렬
  - 클래식 피아노 레퍼토리
- **분할**: 공식 train/validation/test 분할 사용
- **평가 대상**: Test set (약 20시간)

### MAPS

- **출처**: MUSIC ANALYSIS, PERCEPTION AND SYNTHESIS 프로젝트
- **규모**: 약 18시간
- **특징**:
  - 다양한 피아노 음색 (9개 피아노)
  - 실제 녹음 + 합성 오디오
  - 녹음 환경 다양성
- **평가 대상**: 전체 데이터셋

## 평가 메트릭

[mir_eval](https://craffel.github.io/mir_eval/) 라이브러리를 사용하여 표준 메트릭을 계산합니다.

### Note-level Metrics

노트 단위로 Ground Truth와 예측을 비교합니다.

| 메트릭 | 설명 | Tolerance |
|--------|------|-----------|
| Note F1 | Pitch + onset-only F1 | onset ±50ms; offset 미사용 |
| Note+Off F1 | Pitch + onset + offset F1 | onset ±50ms, offset max(20%, 50ms) |
| Note Precision | 예측 노트 중 정확한 비율 | 동일 |
| Note Recall | 실제 노트 중 검출된 비율 | 동일 |

### Onset/Offset Metrics

| 메트릭 | 설명 | Tolerance |
|--------|------|-----------|
| Onset F1 | 노트 시작 시점 정확도 | ±50ms |
| Offset F1 | 노트 종료 시점 정확도 | 20% of note duration or 50ms |

### Velocity Metrics

| 메트릭 | 설명 | 범위 |
|--------|------|------|
| Velocity MAE | 벨로시티 평균 절대 오차 | 0-127 |

## 평가 환경

### 하드웨어

- **GPU**: NVIDIA RTX 3090 24GB
- **CPU**: AMD Ryzen 9 5900X
- **RAM**: 64GB DDR4

### 소프트웨어

- **Python**: 3.11
- **PyTorch**: 2.0
- **mir_eval**: 0.7

### 추론 시간 측정

- GPU 워밍업 후 측정 (10 iterations)
- 배치 크기 1로 고정
- 전처리 시간 포함
- 1초 오디오 기준 ms 단위

## 알고리즘별 설정

### Sori Engine

- 최신 공개 버전 사용
- 기본 설정 적용

### Basic Pitch (Spotify)

- [basic-pitch](https://github.com/spotify/basic-pitch) v0.3.0
- 기본 설정 적용

### Onsets and Frames (Google Magenta)

- [magenta/models/onsets_frames_transcription](https://github.com/magenta/magenta)
- 공식 체크포인트 사용
- MAESTRO-trained model

### MT3 (Google)

- [magenta/mt3](https://github.com/magenta/mt3)
- Piano-only mode
- 공식 체크포인트 사용

## 재현성

모든 실험 코드와 설정은 요청 시 공개 가능합니다.
문의: tech@sori.ai

## 결과별 재현 정보

이 저장소에는 모델 추론이나 채점 실행기가 포함되어 있지 않습니다. 위 환경은 기존 기록이며 모든 후속 결과의 실행 환경을 뜻하지 않습니다. 새 결과는 고정 checkpoint, 데이터 분모, 집계, 채점 설정과 원결과 해시를 결과별 보고서에 기록합니다. 과거 행의 미기록 설정을 새 결과와 동일하다고 가정하지 않습니다. `tested_date: null`은 평가 날짜가 원자료에 없다는 뜻이며 게시 날짜로 대체하지 않습니다.
