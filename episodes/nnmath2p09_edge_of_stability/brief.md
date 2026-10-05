# 신경망의 수학 2부 09 제작 기준

## 제목과 목표

**Edge of Stability — 신경망은 왜 불안정해지기 직전까지 학습할까?**

단순히 Learning Rate가 크다는 이야기가 아니라, `eta`가 고정되어 있어도 학습 중 모델이 더 높은 local curvature의 영역으로 이동해 `eta lambda_max`가 안정성 경계에 접근할 수 있다는 점을 설명한다. 최종 메시지는 `좋은 학습 = 매 step의 단조로운 Loss 감소`가 아니라는 것이다.

## 정확성 기준

- `eta lambda < 2`는 1차원 quadratic 방향에 대한 단순 Gradient Descent의 안정성 조건으로 제시한다.
- `lambda_max`는 local Hessian의 가장 큰 eigenvalue, 즉 sharpness로 설명한다.
- Edge of Stability는 모든 optimizer와 모든 학습 설정의 보편 법칙이 아니라 특정 신경망 Gradient Descent 설정에서 관찰될 수 있는 현상으로 표현한다.
- 경계 근처의 진동과 실제 발산을 구분하며 `Edge ≠ unlimited instability`를 명시한다.
- Loss가 일부 step에서 증가할 수 있어도 장기 추세가 감소할 수 있음을 보여준다.
- Spectral Bias 편의 방향별 eigenvalue와 이번 편의 `lambda_max`를 연결하되 두 현상을 동일시하지 않는다.

## 핵심 수식

- `L(theta) = 1/2 lambda theta^2`
- `gradient L(theta) = lambda theta`
- `theta_(t+1) = (1 - eta lambda) theta_t`
- `eta lambda < 2`
- `eta lambda_max ≈ 2`

## 시각 구성

- 동일한 Learning Rate를 넓은 골짜기와 좁은 골짜기에 적용해 curvature의 역할을 먼저 이해시킨다.
- update 식을 직접 정리하고 `eta lambda = 0.5`, `1.5`, `2`의 위치 sequence를 비교해 경계 2가 나오는 이유를 보여준다.
- `eta=0.01`을 고정한 채 `lambda_max: 20 → 100 → 190`, `eta lambda_max: 0.2 → 1 → 1.9`가 되는 숫자 예시를 독립 장면으로 유지한다.
- `lambda_max` 곡선이 `2/eta` 경계로 상승한 뒤 근처에서 진동하는 그래프를 후반부의 중심 시각으로 사용한다.
- Learning Rate 게이지는 고정하고 curvature 게이지만 증가시켜 `eta lambda_max`가 2에 접근하는 장면을 영상의 핵심 애니메이션으로 만든다.
- 부드러운 Loss 감소 그래프에 X를 표시한 뒤 oscillation이 있으나 장기 추세는 감소하는 그래프로 전환한다.
- Stable / Edge / Divergence의 세 영역을 명확히 분리한다.
- 마지막에는 Spectral Bias의 eigenvalue spectrum 중 `lambda_max`만 확대해 안정성 경계로 연결한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1–3 | 00:00–00:43 | step size와 넓은/좁은 골짜기, curvature 직관 |
| 4–5 | 00:43–01:10 | quadratic gradient와 update multiplier 유도 |
| 6–9 | 01:10–01:57 | eta lambda 0.5 / 1.5 / 2 비교와 안정성 경계 |
| 10–11 | 01:57–02:22 | 고정 지형에서 이동하는 신경망 parameter로 전환 |
| 12 | 02:22–02:40 | eta=0.01 고정 숫자 예시 |
| 13–14 | 02:40–03:04 | fixed eta, changing lambda max와 2/eta 접근 |
| 15–17 | 03:04–03:39 | 경계 부근의 curvature/Loss 진동과 학습 지속 |
| 18–19 | 03:39–04:00 | local geometry 변화와 divergence 구분 |
| 20–21 | 04:00–04:16 | eigenvalue spectrum 연결과 결론 |

총 256초. 상세 설명을 위해 기존 132초 버전보다 curvature 직관, update 유도, 숫자 예시를 확장한다. 1080×1920, 30fps, 무음 마스터.

## 썸네일 기준

- 핵심 게이지 장면에서 `eta = constant`, `lambda_max ↑`, `eta lambda_max → 2`가 동시에 보이는 프레임을 추출한다.
