# 신경망의 수학 14 — 왜 Hessian에는 0에 가까운 고유값이 많을까?

## 학습 목표

- 같은 minimum 주변에서도 방향마다 Loss의 곡률이 크게 다를 수 있음을 이해한다.
- Hessian 고유방향 `vᵢ`와 고유값 `λᵢ`를 각각 특별한 방향과 그 방향의 국소 곡률로 읽는다.
- near-zero eigenvalue가 많아질 수 있는 이유를 overparameterization, parameter symmetry, data-null direction, inactive unit으로 나누어 본다.
- 정확한 symmetry가 만드는 exact flat direction과 Loss가 천천히 변하는 approximately flat direction을 구별한다.
- 고차원 minimum을 `few stiff directions + many flat directions`인 넓은 골짜기로 해석한다.

## 중심 흐름

`Round Bowl → Anisotropic Bowl → Hessian Eigen-directions → Spectrum near 0 → Overparameterization → Scaling Symmetry → Data-null Direction → Inactive Unit → Exact vs Approximate Flatness → High-dimensional Valley`

## 수학적 정확성

- `L(x,y)=x²+y²`의 Hessian은 `2I`, `L(x,y)=10x²+0.01y²`의 Hessian은 `diag(20, 0.02)`다.
- `Hvᵢ=λᵢvᵢ`에서 `vᵢ`는 Hessian의 고유방향, `λᵢ`는 해당 좌표계에서의 국소 2차 곡률이다.
- `λᵢ≈0`은 국소 2차항이 작다는 뜻이다. 유한 거리 전체에서 Loss가 일정하거나 함수가 정확히 같다는 뜻은 아니다.
- ReLU scaling symmetry `w→cw`, `v→v/c`, `c>0`는 bias 없는 한 뉴런 예시로 제한한다.
- exact continuous symmetry를 따라 함수와 Loss가 일정하면 그 접선 방향은 정지점에서 Hessian의 zero mode가 될 수 있다.
- `Jv≈0`이면 현재 데이터에서 출력 변화가 작다. Gauss–Newton 계열 성분이 `JᵀGJ` 꼴일 때 이 방향의 곡률도 작아진다. 전체 Hessian이 언제나 정확히 `JᵀGJ`와 같다고 주장하지 않는다.
- 모든 모델과 데이터셋에서 대부분의 고유값이 반드시 0 근처라는 보편 법칙으로 말하지 않는다.
- Hessian eigenvalue와 flatness는 parameterization과 좌표 재척도화에 영향을 받는다. 이번 편은 고정된 parameterization 안의 국소 구조를 설명한다.

## 연출 기준

- 둥근 contour가 찌그러진 contour로 변하면서 방향별 곡률 차이를 첫 반전으로 만든다.
- `L(x,y)=10x²+0.01y²`는 x 방향의 좁은 단면과 y 방향의 넓은 단면을 동시에 보여준다.
- `L(x,y,z)=x²+y²`가 z 방향으로 일정한 trough가 되는 모습을 등각 투영 mesh로 표현한다.
- spectrum은 near-zero 막대 다수와 큰 양의 eigenvalue 소수로 표현하되 `conceptual` 표시를 둔다.
- scaling symmetry는 `(w,v)` 점이 `wv=constant` 곡선을 따라 움직이는 장면과 고정된 함수 출력 패널을 함께 보여준다.
- data-null direction은 데이터가 비추는 관측 방향과 보이지 않는 회색 방향을 분리한다.
- inactive ReLU는 모든 training sample에서 pre-activation이 음수여서 출력이 0인 제한된 예시로 표현한다.
- 마지막에는 점 하나를 길게 늘어난 valley로 변환하고 핵심 문장을 회수한다.
- 141초, 1080×1920, 30fps, 무음 마스터. 실측 TTS 구간 종료 시점에 맞춰 16개 화면을 전환한다.
