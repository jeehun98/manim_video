# 신경망의 수학 2부 02 제작 기준

## 제목과 목표

**2차원 공간에 5개의 특징을 저장할 수 있을까? — Superposition**

독립적인 좌표축은 두 개뿐인 평면에 다섯 개의 feature direction을 둘 수 있다는 모순에서 출발한다. 직교성을 포기하면 더 많은 특징을 같은 representation에 배치할 수 있지만 interference가 생기며, feature activation이 sparse할수록 실제 충돌 빈도가 낮아져 이 선택이 유리할 수 있다는 논리를 시각적으로 발견하게 한다.

## 정확성 기준

- `5 features in R²`는 다섯 개의 독립 자유도나 임의의 다섯 실수를 무손실 복원한다는 뜻이 아니다. 두 좌표에 다섯 개의 **비직교 feature direction**을 배치한다는 뜻이다.
- representation은 `h = Σ xᵢ fᵢ`로 보여준다. `fᵢᵀfⱼ ≠ 0`이면 한 feature를 읽을 때 다른 feature가 섞이는 cross-term이 생긴다.
- sparsity는 간섭을 없애는 보장이 아니라, 동시에 활성화되는 feature 수와 충돌 가능성을 낮춰 기대 비용을 줄일 수 있는 조건이다.
- superposition을 모든 실제 신경망이 반드시 사용하는 보편 법칙으로 단정하지 않는다. 제한된 차원에서 capacity와 interference 사이를 절충하는 표현 전략으로 설명한다.
- neuron은 representation의 좌표이고 feature는 그 공간의 방향이라는 구분을 유지한다. `one neuron = one feature`를 전제로 하지 않는다.
- 1화와의 연결은 대비로만 쓴다. Neural Collapse는 특정 조건의 학습 후반에 class representation이 규칙적인 중심으로 모이는 현상이고, superposition은 제한된 차원에 여러 feature direction을 겹쳐 쓰는 현상이다.

## 화면 원칙

- 2개의 좌표축은 희미한 회색, 5개의 feature direction은 시리즈 색상으로 선명하게 구분한다.
- dense 입력에서는 여러 벡터와 cross-term을 동시에 켜 복잡하게, sparse 입력에서는 1~2개만 밝게 켜 충돌 감소를 즉시 비교한다.
- 영어 용어 `Feature`, `Interference`, `Sparse`, `Superposition`은 화면에 그대로 쓰고 한국어 설명은 내레이션과 자막에 둔다.
- 세로 프레임에서 제목, 본문, 하단 자막이 겹치지 않도록 본 시각화는 대략 y=−3.7~4.4 안에 둔다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:06 | R²의 두 독립 축 제시 |
| 2 | 00:06–00:12 | 두 feature의 직교 표현 |
| 3 | 00:12–00:18 | 세 번째 직교 방향의 불가능성 |
| 4 | 00:18–00:24 | 차원 확장과 고정된 차원 대비 |
| 5 | 00:24–00:31 | R²에 다섯 비직교 방향 배치 |
| 6 | 00:31–00:38 | 선형 중첩과 interference의 수학 |
| 7 | 00:38–00:45 | 독립성 대 capacity 절충 |
| 8 | 00:45–00:52 | dense activation의 높은 충돌 |
| 9 | 00:52–01:00 | sparse activation에서 충돌 감소 |
| 10 | 01:00–01:07 | 입력마다 다른 방향이 켜지는 공유 |
| 11 | 01:07–01:14 | dense / sparse 비교 |
| 12 | 01:14–01:21 | Superposition 명명 |
| 13 | 01:21–01:28 | neuron coordinate와 feature direction 구분 |
| 14 | 01:28–01:35 | capacity–interference trade-off |
| 15 | 01:35–01:42 | 1화 대비와 polysemanticity 질문 |

총 102초. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다.

