# 신경망의 수학 13 — 신경망 학습을 동역학계로 보면 보이는 것

## 00:00–00:06

Gradient Descent는 흔히 Loss 지형을 내려가는 공으로 설명됩니다. 하지만 이 그림은 중요한 것 하나를 숨깁니다.

## 00:06–00:16

Parameter Space 전체를 보겠습니다. 현재 위치가 `θ`라면 gradient는 Loss가 가장 빠르게 증가하는 방향이고, Gradient Descent는 그 반대로 움직입니다.

## 00:16–00:26

공간의 모든 위치에서 `-∇L`을 그리면 Parameter Space 전체에 하나의 vector field가 만들어집니다.

## 00:26–00:32

서로 다른 위치에서 시작해봅시다. 각 점은 목적지를 알지 못한 채 현재 위치의 방향만 보고 움직입니다. 그 반복이 trajectory를 만듭니다.

## 00:32–00:44

Gradient Descent는 `θ₀, θ₁, θ₂`처럼 한 step씩 이동합니다. Step을 매우 작게 보면 부드러운 곡선, `θ̇=-∇L(θ)`인 Gradient Flow가 됩니다.

## 00:44–00:50

같은 minimum에 도착해도 경로는 다릅니다. Initial condition과 vector field가 함께 trajectory를 결정합니다.

## 00:50–00:57

Minimum이 두 개라면 공간이 갈라집니다. 같은 attractor로 흘러가는 초기조건의 영역이 basin of attraction입니다.

## 00:57–01:05

두 basin의 경계에는 단순한 벽만 있는 것이 아닙니다. 가운데에는 한 방향과 다른 방향의 행동이 전혀 다른 saddle point가 놓일 수 있습니다.

## 01:05–01:15

`L(x,y)=x²-y²`에서 원점은 x방향의 minimum이자 y방향의 maximum입니다. 흐름은 x축으로 들어오고 y축으로 멀어집니다.

## 01:15–01:23

끌려오는 쪽은 stable direction, 밀려나는 쪽은 unstable direction입니다. 정확히 x축 위의 시작점들은 stable manifold를 만듭니다.

## 01:23–01:32

주변의 시작점들이 한 상태로 흘러들어간다면 그 상태가 attractor입니다. 안정적인 local minimum은 attractor처럼 동작할 수 있습니다.

## 01:32–01:40

Gradient Descent는 최단 경로를 찾거나 목적지를 직접 알지 못합니다. 현재 gradient만 따르므로 trajectory는 휘어질 수 있습니다.

## 01:40–01:48

작은 step은 흐름을 잘 따르지만 너무 크면 minimum을 지나쳐 진동하거나 발산합니다. Learning rate는 dynamics 자체를 바꿉니다.

## 01:48–01:59

실제 신경망의 Parameter Space는 두 차원이 아니라 수백만, 수십억 차원일 수 있습니다. 지금 본 그림은 복잡한 dynamics의 작은 단면이지만 원리는 같습니다.

## 01:59–02:06

Mini-batch SGD에서는 gradient에 noise가 섞여, 실제 경로가 vector field 주변을 조금씩 흔들리며 이동합니다.

## 02:06–02:17

이 관점에서 초기값은 trajectory를 정하는 initial condition이 됩니다. Loss Landscape는 vector field를 만들고, basin과 saddle, attractor는 그 흐름의 장기적인 구조를 결정합니다.

## 02:17–02:27

신경망 학습은 단순히 공이 아래로 굴러가는 과정이 아닙니다. Parameter Space 전체에 만들어진 방향장 위에서 초기 상태가 하나의 경로를 만드는 동역학계입니다.
