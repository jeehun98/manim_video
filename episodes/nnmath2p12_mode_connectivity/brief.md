# 제작 기준 — Mode Connectivity

## 핵심 질문

`Parameter space에서 멀리 떨어진 두 minimum은 정말 서로 다른 basin에 고립되어 있는가?`

## 시각적 중심

- 동일한 A와 B가 2D 단면에서는 장벽으로 막혀 보이지만, 숨겨진 축을 열면 우회 경로가 드러나는 첫 번째 반전을 핵심으로 삼는다.
- `straight path` 대 `curved low-loss path`를 동일한 색상과 배치로 반복 비교한다.
- 후반의 permutation symmetry는 좌표 정렬 문제가 직선 barrier에 영향을 줄 수 있다는 명확한 두 번째 반전으로 사용한다.
- 최종 이미지는 단순한 우회로보다 `고립된 웅덩이가 아니라 같은 거대한 low-loss 협곡의 서로 먼 두 지점`이라는 관점으로 회수한다.

## 정확성 제약

- 차원을 하나 늘리면 항상 길이 생긴다고 주장하지 않는다. 2D→3D는 낮은 차원 단면이 전체 공간을 대변하지 않는다는 시각적 비유다.
- Mode Connectivity의 곡선 경로는 보통 주어진 두 solution 사이에서 추가로 찾은 경로이며, 임의의 곡선이 낮은 Loss를 갖는다는 뜻이 아니다.
- Straight interpolation의 barrier는 disconnected의 충분한 증거가 아니지만, 모든 두 해가 항상 연결된다고 단정하지 않는다.
- Permutation alignment 후 linear mode connectivity는 `일부 설정에서`, `barrier가 줄어들 수 있다`로 조건부 표현한다.
- Low-loss `manifold`라고 수학적으로 단정하지 않고 `region`, `structure`, `협곡`이라는 시각적 비유를 사용한다.

## 근거

- Garipov et al., *Loss Surfaces, Mode Connectivity, and Fast Ensembling of DNNs*, NeurIPS 2018.
- Draxler et al., *Essentially No Barriers in Neural Network Energy Landscape*, ICML 2018.
- Entezari et al., *The Role of Permutation Invariance in Linear Mode Connectivity of Neural Networks*, ICLR 2022.
- Ainsworth et al., *Git Re-Basin: Merging Models modulo Permutation Symmetries*, ICLR 2023.
