# 신경망의 수학 2부 04 제작 기준

## 제목과 목표

**모델의 진짜 Feature를 찾았다는 걸 어떻게 알까? — Identifiability**

해석 가능한 feature direction을 찾고 activation을 잘 복원했다는 사실만으로 그것이 모델의 실제 feature라고 말할 수 있는지 묻는다. 같은 관측을 서로 다른 decomposition이 똑같이 잘 설명하는 예에서 출발해, 좋은 설명의 존재와 설명의 유일성, 실제 메커니즘의 확인은 서로 다른 주장임을 보여준다. Sparse Autoencoder는 정답을 읽는 장치가 아니라 sparsity라는 가정을 추가해 가능한 설명 중 하나를 선호하는 방법으로 최소한만 소개한다.

## 정확성 기준

- `Reconstruction error ≈ 0`은 관측된 activation을 설명한다는 증거일 뿐 decomposition의 유일성이나 인과적 실재를 보장하지 않는다.
- Identifiability는 관측 분포와 모델 가정 아래에서 숨은 구조를 유일하게 복원할 수 있는지의 문제로 설명한다. 실제 식별 가능성은 permutation, scale, sign 같은 허용 가능한 대칭까지 고려할 수 있지만 본편에서는 개념적 수준으로 제한한다.
- `(1,1)=(1,0)+(0,1)=√2·(1,1)/√2` 예시는 단일 관측 벡터가 여러 dictionary 설명을 허용한다는 직관용이다. 전체 데이터 분포와 추가 가정이 있으면 식별 조건은 달라질 수 있다.
- Sparse Autoencoder는 `h → z → ĥ`와 sparse `z`만 보여준다. sparsity는 관측에 더해진 inductive bias이며, 해석 가능성이나 ground-truth recovery를 자동 보장하지 않는다.
- 해석 가능한 상관관계, reconstruction, intervention evidence를 강도의 층위로 구분하되 intervention도 완전한 identifiability의 보장은 아니라고 명시한다.
- `모델이 실제로 사용하는 feature`는 조작했을 때 예측 가능한 행동 변화가 나타나는지 등의 인과적 검증이 더 강한 증거가 될 수 있다는 수준으로 표현한다.

## 썸네일 기준

- 00:28–00:35 장면을 썸네일 전용 정지 구간으로도 사용한다.
- 좌우에 서로 다른 두 decomposition, 중앙 물음표, 하단에 `좋은 복원 ≠ 유일한 설명`을 크게 배치한다.
- 렌더 후 00:31.5 프레임을 `exports/nnmath2p04_thumbnail.png`로 추출한다.
- 프레임 자체가 9:16 썸네일로 작동하도록 핵심 요소를 상단 제목과 하단 자막 사이에 집중한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:07 | 뉴런 축 사이 feature direction 회상 |
| 2 | 00:07–00:14 | 해석 가능한 feature를 찾았다는 첫 결론 |
| 3 | 00:14–00:21 | 첫 decomposition의 성공적 reconstruction |
| 4 | 00:21–00:28 | 전혀 다른 decomposition도 성공 |
| 5 | 00:28–00:35 | 좋은 복원과 유일한 설명의 차이, 썸네일 장면 |
| 6 | 00:35–00:42 | `(1,1)`의 두 가지 설명 |
| 7 | 00:42–00:49 | 관측 h에서 숨은 원인을 역추론하는 문제 |
| 8 | 00:49–00:56 | Identifiability 명명 |
| 9 | 00:56–01:03 | 동일 activation cloud 위 여러 좌표계 |
| 10 | 01:03–01:10 | sparse 설명 선호와 SAE 최소 소개 |
| 11 | 01:10–01:17 | Observation + Assumption → Explanation |
| 12 | 01:17–01:24 | 실제 sparsity 발견 / sparsity를 요구한 결과 대비 |
| 13 | 01:24–01:31 | 좋은 설명과 실제 메커니즘 구분 |
| 14 | 01:31–01:38 | 상관관계에서 intervention으로 |
| 15 | 01:38–01:45 | fit, uniqueness, mechanism의 서로 다른 주장 |
| 16 | 01:45–01:52 | 최종 Identifiability 질문 |

총 112초. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다.

