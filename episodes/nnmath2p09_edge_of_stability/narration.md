# 신경망의 수학 2부 09 — Edge of Stability

## 00:00–00:16

Gradient Descent는 현재 위치의 기울기를 보고 Loss가 낮아지는 방향으로 이동합니다. Learning Rate가 작으면 조금씩, 적당히 크면 더 빠르게 최소점에 접근합니다. 하지만 너무 크게 움직이면 최소점을 반복해서 넘어가며 안정적으로 수렴하지 못할 수 있습니다.

## 00:16–00:31

그런데 안정성을 결정하는 것은 Learning Rate뿐만이 아닙니다. 같은 Learning Rate로 넓고 완만한 골짜기와 좁고 가파른 골짜기를 움직이면, 가파른 곳에서는 같은 한 걸음으로도 최소점을 크게 넘어갈 수 있습니다.

## 00:31–00:43

얼마나 크게 움직이는지와 함께 현재 Loss가 얼마나 심하게 휘어 있는지도 중요합니다. 완만한 곡선은 기울기가 천천히 바뀌고, 가파른 곡선은 같은 거리에서도 기울기가 빠르게 바뀝니다. 이것이 curvature입니다.

## 00:43–00:59

가장 단순한 quadratic Loss를 생각해보겠습니다. `L(theta)=1/2 lambda theta^2`이면 gradient는 `lambda theta`입니다. Gradient Descent의 다음 위치는 현재 theta에서 `eta lambda theta`를 뺀 값입니다.

## 00:59–01:10

정리하면 다음 위치는 현재 위치에 `1-eta lambda`를 곱한 값입니다. 이 multiplier의 크기와 부호가 다음 위치와 진동의 폭을 결정합니다.

## 01:10–01:20

`eta lambda=0.5`라면 위치는 매번 절반으로 줄어들며 같은 쪽에서 최소점에 접근합니다.

## 01:20–01:32

`eta lambda=1.5`라면 부호가 계속 바뀝니다. 최소점을 좌우로 넘어가지만 이동 폭은 절반씩 줄어들기 때문에 여전히 수렴합니다.

## 01:32–01:45

`eta lambda=2`이면 multiplier는 `-1`입니다. 현재 위치가 1이면 다음에는 -1, 다시 1, 다시 -1이 됩니다. 최소점을 계속 넘지만 더 이상 가까워지지 않습니다.

## 01:45–01:57

진동의 폭이 줄어들려면 `|1-eta lambda|<1`이어야 합니다. 따라서 고정된 1차원 quadratic에서 simple Gradient Descent의 안정 영역은 `0<eta lambda<2`입니다.

## 01:57–02:08

여기까지는 고정된 Loss 지형에서의 이야기입니다. 실제 신경망도 처음에 안전한 Learning Rate를 골랐다면 계속 안전할 것 같지만, parameter 자체가 학습 중 계속 이동합니다.

## 02:08–02:22

처음에는 넓고 완만한 영역에 있어도 학습하면서 더 좁고 높은 curvature를 가진 영역을 경험할 수 있습니다. Learning Rate는 그대로인데 Hessian의 최대 eigenvalue `lambda max`가 커질 수 있습니다.

## 02:22–02:40

예를 들어 `eta=0.01`로 고정하겠습니다. `lambda max`가 20, 100, 190으로 증가하면 `eta lambda max`는 0.2, 1.0, 1.9로 변하며 안정성 경계 2에 접근합니다.

## 02:40–02:51

Learning Rate를 키워서 경계에 간 것이 아닙니다. 한 번도 바뀌지 않은 eta에, 모델이 새 위치에서 경험하는 `lambda max`가 곱해진 것입니다.

## 02:51–03:04

실제 신경망 학습에서 가장 큰 Hessian eigenvalue를 추적하면 이 값이 증가해 simple Gradient Descent의 classical boundary인 `2/eta` 부근에 도달하는 현상이 관찰될 수 있습니다.

## 03:04–03:16

고정된 quadratic의 직관이라면 곧 학습이 무너질 것 같습니다. 하지만 신경망 학습은 바로 끝나지 않을 수 있고 curvature가 경계 부근에서 움직이면서도 학습이 계속됩니다.

## 03:16–03:28

Loss도 매 step 부드럽게 감소하지 않습니다. 일부 step에서는 증가하고 진동할 수 있지만 더 긴 시간에서 보면 학습은 계속 진행될 수 있습니다.

## 03:28–03:39

classical stability boundary 부근에서 curvature와 Loss가 진동해도 학습이 이어질 수 있는 이런 dynamics를 Edge of Stability라고 합니다.

## 03:39–03:50

모델이 처음부터 경계에 있었던 것은 아닙니다. parameter 이동이 local geometry를 바꾸고, 그 결과 같은 Learning Rate의 안정성도 위치에 따라 달라집니다.

## 03:50–04:00

불안정할수록 좋다는 뜻은 아닙니다. Learning Rate가 지나치게 크거나 안정 범위를 크게 벗어나면 실제로 발산합니다. 핵심은 고전적인 경계 부근에서도 학습이 이어질 수 있다는 점입니다.

## 04:00–04:09

앞에서는 eigenvalue가 방향별 학습 속도와 연결될 수 있음을 봤습니다. 이번에는 가장 큰 값 `lambda max`, 즉 가장 높은 curvature를 가진 방향과 안정성 문제에 주목했습니다.

## 04:09–04:16

좋은 학습이 항상 매 step Loss를 매끄럽게 낮추는 모습일 필요는 없습니다. Learning Rate가 그대로여도 curvature는 변할 수 있습니다. 안정성과 불안정성의 경계에서 이어지는 dynamics가 Edge of Stability입니다.
