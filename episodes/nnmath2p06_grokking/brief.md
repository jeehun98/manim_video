# 신경망의 수학 2부 06 제작 기준

## 제목과 목표

**훈련 정확도 100% 이후에도 모델은 무엇을 배우고 있을까? — Grokking**

훈련 정확도가 일찍 100%에 도달한 뒤 테스트 정확도는 오랫동안 낮게 유지되다가 훨씬 나중에 급격히 상승하는 delayed generalization을 소개한다. 현상을 단순히 “모델이 갑자기 이해했다”라고 의인화하지 않고, 정확도 포화와 optimization 종료가 다르며 같은 훈련 답을 만족하는 memorizing solution과 generalizing solution 사이에서 모델의 구현 방식이 계속 변할 수 있다는 관점으로 설명한다.

## 정확성 기준

- Grokking은 모든 모델을 오래 학습시키면 나타나는 보편 법칙이 아니다. 데이터, 모델, optimizer, regularization, training regime에 따라 양상이 달라지는 특정 현상으로 표현한다.
- 모듈러 덧셈은 대표적인 장난감 문제로만 사용한다. `5+4=2 (mod 7)`과 예시 train/test 조합은 개념 설명용이다.
- Train Accuracy 100%는 모든 train example의 argmax가 맞다는 뜻이지 cross-entropy loss가 0이거나 gradient가 0이라는 뜻이 아니다.
- `P(y)=0.6`과 `P(y)=0.999`는 둘 다 정확한 분류일 수 있지만 loss와 gradient는 다를 수 있다는 예시다.
- `memorization → generalization`은 두 개의 고정된 parameter 해 사이를 실제로 통과한다는 주장이 아니라 행동과 표현 방식이 달라질 수 있음을 설명하는 추상화다.
- Test accuracy의 급격한 변화가 내부 representation의 동일 시점 급변을 자동으로 뜻하지 않는다고 명시한다.
- 초기 연구에서 weight decay 등 regularization이 중요한 역할을 한 설정이 있었지만 이를 grokking의 단일 원인이나 필수 조건으로 일반화하지 않는다.

## 시각 구성

- 00:16–00:22.5에서 Train/Test 곡선의 시간차를 영상의 중심 현상으로 제시한다.
- 모듈러 연산은 숫자 토큰이 고정된 연산 경로를 통과하도록 표현한다.
- 01:06.5–01:17에서 같은 훈련점을 통과하는 복잡한 곡선과 규칙적인 선을 좌우 비교한다.
- 01:17–01:24에서 고정된 두 solution 카드 사이로 parameter 토큰을 이동시켜, 정답 이후에도 dynamics가 이어진다는 점을 보여준다.
- 모든 이동 객체는 원래 모양과 종횡비를 유지하며, 장면 전환 시 이전 장면의 객체가 남지 않도록 stage 그룹 안에서 관리한다.

## 썸네일 기준

- 01:06.5–01:17의 두 solution 비교 장면을 사용한다.
- 좌측 Memorization, 우측 Generalization, 하단 `Train Accuracy = 100% · both`를 한 화면에 둔다.
- 최종 렌더 뒤 01:15 프레임을 `exports/nnmath2p06_thumbnail.png`로 추출한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:10 | Train Accuracy 100%를 apparent finish로 제시 |
| 2 | 00:10–00:16 | 일반적인 과적합 직관 |
| 3 | 00:16–00:22.5 | delayed Test Accuracy 상승 |
| 4 | 00:22.5–00:29.5 | Grokking 명명과 제한된 정의 |
| 5 | 00:29.5–00:37 | 모듈러 연산 예시 |
| 6 | 00:37–00:44 | memorization과 unseen failure |
| 7 | 00:44–00:52 | 긴 plateau에서도 이어지는 optimization |
| 8 | 00:52–00:59.5 | 100% accuracy와 nonzero gradient 구분 |
| 9 | 00:59.5–01:06.5 | 같은 정답, 다른 confidence와 loss |
| 10 | 01:06.5–01:17 | 두 종류의 fitting solution 비교 |
| 11 | 01:17–01:24 | 같은 train fit 안에서 달라질 수 있는 dynamics |
| 12 | 01:24–01:32 | sudden behavior와 gradual internal change 구분 |
| 13 | 01:32–01:40 | optimization과 regularization의 해 선택 |
| 14 | 01:40–01:50.5 | representable과 reached yet 연결 |
| 15 | 01:50.5–01:57.5 | 비보편성 명시 |
| 16 | 01:57.5–02:06 | accuracy saturation과 learning completion 구분 |

총 126초. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다. 화면 구성과 개별 애니메이션 속도는 유지하고 TTS 문단 길이에 맞춰 장면 유지 시간과 전환 시점만 조정한다.
