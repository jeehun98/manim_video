# 신경망의 수학 2부 07 제작 기준

## 제목과 목표

**신경망은 학습하면서 정말 새로운 Feature를 만들까? — Feature Learning vs Lazy Learning**

예측 성능의 향상을 곧바로 새로운 내부 Feature의 형성으로 해석할 수 없다는 점을 설명한다. 핵심 시각 언어는 `Feature Learning = 축과 point cloud가 움직임`, `Lazy Learning = 축과 cloud는 거의 고정되고 조합 계수가 움직임`으로 고정한다.

## 정확성 기준

- Lazy Learning을 모든 넓은 신경망의 보편적 행동으로 표현하지 않는다. 폭, parameterization, scaling, 초기화, 학습률 등 특정 regime에 의존한다고 명시한다.
- `θ = θ₀ + Δθ`에서 parameter norm 하나만으로 lazy 여부가 결정된다고 주장하지 않는다. 초기점 주변의 선형화가 학습 동안 유효하게 유지되는 상황이라고 표현한다.
- `φ(x)=∇θf(x;θ₀)`는 선형화 모델의 tangent feature다. 일반 hidden representation과 완전히 같은 객체라고 말하지 않는다.
- 특정 무한 폭 scaling limit에서 NTK가 학습 중 거의 고정된다고 제한한다.
- Feature Learning과 Lazy Learning은 엄격한 이분법이 아니라 두 극단 또는 regime으로 설명한다.
- 높은 예측 성능만으로 Feature Learning 발생 여부를 판정할 수 없다고 결론낸다.

## 시각 구성

- 00:15.4–00:48.5는 동일한 point cloud와 feature 축을 가진 좌우 보드를 유지한다.
- 왼쪽 Feature Learning에서는 vector가 형태를 유지한 채 회전하고 point cloud가 두 class를 분리하기 좋은 구조로 재배치된다.
- 오른쪽 Lazy Learning에서는 vector와 point cloud를 고정하고 coefficient만 `0.2, −0.1, 0.3`에서 `1.4, −0.8, 2.1`로 바꾼다.
- 양쪽에 같은 `Accuracy = 95%`를 표시해 성능만으로 내부 motion을 구분할 수 없음을 보여준다.
- 선형화 식 하나를 메인 수식으로 사용하고 `∇θf(x;θ₀)`와 `Δθ`를 각각 고정에 가까운 tangent feature와 learned combination으로 분리한다.
- NTK는 입력 두 개가 tangent feature vector로 바뀐 뒤 내적되는 객체 이동으로 설명한다.
- 마지막에는 완만한 파형과 작은 고주파 진동을 함께 보여주고 모델이 완만한 성분부터 따라가는 Spectral Bias 장면으로 연결한다.
- 모든 이동과 회전은 객체의 형태 및 종횡비를 유지한다. 장면 전환 시 stage 전체를 교체한다.

## 썸네일 기준

- 00:29 부근의 좌우 비교 장면을 사용한다.
- 왼쪽의 회전한 축과 분리된 point cloud, 오른쪽의 고정된 축과 섞인 point cloud가 동시에 보이게 한다.
- 최종 렌더 뒤 00:29 프레임을 `exports/nnmath2p07_thumbnail.png`로 추출한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:07.7 | Grokking 그래프에서 반대 질문으로 전환 |
| 2 | 00:07.7–00:15.4 | point cloud가 Feature 축에 맞춰 재배치되는 기본 직관 |
| 3 | 00:15.4–00:23.2 | 완전히 같은 초기 상태를 가진 두 모델 |
| 4 | 00:23.2–00:32 | 왼쪽의 Feature 축과 point cloud 변화 |
| 5 | 00:32–00:40.8 | 오른쪽의 고정 Feature와 coefficient 변화 |
| 6 | 00:40.8–00:48.5 | 동일 Accuracy, 서로 다른 내부 motion |
| 7 | 00:48.5–00:57.4 | 초기점 주변 궤적과 접평면 |
| 8 | 00:57.4–01:06.2 | 중심 선형화 식과 두 항의 역할 |
| 9 | 01:06.2–01:13.9 | 초기 gradient vector를 tangent feature로 해석 |
| 10 | 01:13.9–01:22.7 | 고정된 feature와 움직이는 Δθ slider |
| 11 | 01:22.7–01:30.5 | 두 tangent vector의 내적으로 NTK 정의 |
| 12 | 01:30.5–01:39.3 | width 증가와 K₀≈Kₜ |
| 13 | 01:39.3–01:47 | wide와 lazy의 단순 등치 반박 |
| 14 | 01:47–01:54.7 | 큰 출력 변화와 작은 representation 변화 |
| 15 | 01:54.7–02:02.5 | Feature/Jacobian/kernel의 before-after 비교 |
| 16 | 02:02.5–02:09.1 | 두 regime을 연속체로 표현 |
| 17 | 02:09.1–02:14.6 | Prediction Learning과 Feature Learning 분리 |
| 18 | 02:14.6–02:19 | Spectral Bias 파형 예고 |

총 139초. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다.
