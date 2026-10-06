# 신경망의 수학 13 — 신경망 학습을 동역학계로 보면 보이는 것

## 학습 목표

- Gradient Descent를 목적지를 알고 찾아가는 탐색이 아니라, 현재 상태가 다음 상태를 정하는 이산 동역학계로 본다.
- 한 점의 `-∇L(θ)`를 Parameter Space 전체의 vector field로 확장한다.
- initial condition, trajectory, basin of attraction, saddle, stable/unstable direction, attractor를 하나의 흐름으로 연결한다.
- 작은 step의 Gradient Descent와 연속시간 Gradient Flow `θ̇=-∇L(θ)`의 관계를 구별한다.
- 실제 SGD의 mini-batch noise와 연속적인 Gradient Flow 사이의 차이를 짧게 확인한다.

## 중심 흐름

`Loss Surface → Gradient at One Point → Vector Field → Initial Condition → Trajectory → Gradient Flow → Basin → Saddle → Stable/Unstable Direction → Attractor → Training as Dynamics`

## 수학적 정확성

- Gradient는 loss가 가장 빠르게 증가하는 국소 방향이다. Gradient Descent는 그 반대 방향으로 유한한 step을 이동한다.
- 영상의 부드러운 trajectory는 이후 구조를 설명하기 위한 Gradient Flow 근사다. 실제 Gradient Descent와 동일하다고 주장하지 않는다.
- 두 basin 장면은 `L(x,y)=(x²-a²)²+βy²`의 개념도다. 좌우에 두 local minimum이 있고 원점은 basin 경계 위의 saddle이다.
- Saddle 예시는 `L(x,y)=x²-y²`다. Gradient Flow는 `ẋ=-2x`, `ẏ=2y`이므로 x축이 stable direction, y축이 unstable direction이다.
- stable manifold는 엄밀한 일반 정의 대신, 이 예시에서 saddle로 수렴하는 특별한 초기조건의 집합으로 소개한다.
- 모든 local minimum이 무조건 attractor라고 단정하지 않는다. 주변에서 안정적인 local minimum이 Gradient Flow의 attractor처럼 동작할 수 있다고 표현한다.
- learning rate는 단순한 속도 조절값이 아니라 이산 dynamics의 안정성을 바꾼다.
- SGD는 deterministic vector field를 정확히 따르는 흐름이 아니라 mini-batch gradient noise가 섞인 경로로 표현한다.

## 연출 기준

- 처음의 3D loss surface는 실제 3D 카메라 대신 세로 프레임에 맞춘 등각 투영 mesh로 표현한다. 이후 같은 지형을 contour로 바꿔 관점 전환을 강조한다.
- vector field의 화살표는 방향 비교가 목적이므로 길이를 정규화한다.
- trajectory는 미리 계산한 경로를 사용하고 매 프레임 객체를 재생성하지 않는다.
- 여러 초기점은 동시에 움직이고, 이동 후에도 path를 남겨 공간 전체의 흐름을 읽게 한다.
- Scene 7~10은 같은 basin/saddle 문법을 유지한다. 색은 왼쪽 basin `WEIGHT`, 오른쪽 basin `SPARSE`, saddle `PRUNE`로 고정한다.
- Scene 13과 Scene 15는 보충 장면으로 짧게 처리한다.
- 마지막에는 `Initial Condition + Vector Field → Trajectory`와 `Training = Dynamics in Parameter Space`를 회수한다.
- 147초, 1080×1920, 30fps, 무음 마스터. 실측 TTS 구간 종료 시점에 맞춰 17개 화면을 전환한다.
