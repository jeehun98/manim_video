# 신경망의 수학 2부 05 제작 기준

## 제목과 목표

**Feature가 진짜인지 직접 지워보면 알 수 있을까? — Causal Intervention**

4화의 Identifiability 질문에서 이어서, 해석 가능한 상관관계와 reconstruction보다 내부 표현을 직접 조작하는 실험이 더 강한 인과적 증거를 준다는 점을 보여준다. feature direction의 제거와 추가를 필요성·충분성 질문으로 나누고, ablation의 음성 결과가 redundancy 때문에 모호할 수 있으며 과도한 개입은 activation distribution 밖으로 나갈 수 있고 superposition은 다른 정보까지 함께 바꿀 수 있음을 설명한다. 결론은 intervention을 최종 증명이 아니라 더 강한 검증 단계로 위치시키고 다음 편의 circuits로 연결한다.

## `gpuops12_dropout_rng`에서 적용한 시각 문법

- 설명 카드만 교체하지 않고 activation/feature 토큰이 고정된 경로를 실제로 이동하도록 한다.
- 두 관점을 좌우의 동일한 크기 패널로 배치한다: wolf/snow, remove/add, necessity/sufficiency, controlled/too large.
- 경로와 보드는 먼저 고정하고 토큰만 움직여 무엇이 조작되고 무엇이 유지되는지 분리한다.
- 비교 장면의 거리와 이동 시간은 효과 크기나 실제 계산 시간을 뜻하지 않는다.
- 이동 중 객체는 비균일 스케일이나 서로 다른 도형 사이의 Transform을 사용하지 않고 완성된 형태를 유지한다.

## 정확성 기준

- `vᵀh`가 특정 입력에서 크다는 관찰은 feature의 인과적 사용을 곧바로 뜻하지 않는다.
- 제거는 개념적으로 `h' = h − proj_v(h)`, 추가는 `h' = h + αv`로 표현한다. 실제 모델에서는 레이어, 정규화, 위치, 개입 크기와 구현이 결과에 영향을 준다.
- 제거 후 행동 감소는 필요성에 관한 증거, 추가 후 행동 증가는 충분성에 관한 증거와 연결되지만 각각을 수학적으로 완전히 증명한다고 말하지 않는다.
- ablation 뒤 변화가 없다고 해당 구성요소가 사용되지 않았다고 결론 내리지 않는다. 중복·우회 경로가 효과를 가릴 수 있다.
- 큰 개입의 효과는 정상 activation distribution을 벗어난 교란일 수 있다. dose, matched baseline, control intervention이 중요하다.
- superposition된 방향을 제거하면 의도한 의미 외의 정보도 함께 바뀔 수 있다.
- 예시 확률 `0.94→0.21`, `0.31→0.78`은 개념 설명용 수치이며 특정 실험 결과를 인용하지 않는다.

## 썸네일 기준

- 00:42–00:49의 필요성/충분성 비교 장면을 사용한다.
- 좌측 `REMOVE v`, 우측 `ADD v`, 하단 `correlation < intervention evidence`가 한 프레임에 보이게 한다.
- 최종 렌더 뒤 00:45.5 프레임을 `exports/nnmath2p05_thumbnail.png`로 추출한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:07 | 관찰에서 개입으로 전환 |
| 2 | 00:07–00:14 | 늑대와 feature의 관찰적 상관 |
| 3 | 00:14–00:21 | wolf/snow 두 메커니즘 비교 |
| 4 | 00:21–00:28 | projection 제거 개입 |
| 5 | 00:28–00:35 | 제거 뒤 행동 감소 |
| 6 | 00:35–00:42 | feature 추가 뒤 행동 증가 |
| 7 | 00:42–00:49 | 필요성과 충분성 병렬 비교 |
| 8 | 00:49–00:56 | 개입 수준: neuron/head/direction/activation |
| 9 | 00:56–01:03 | observe와 manipulate의 질문 차이 |
| 10 | 01:03–01:10 | redundancy 우회 경로 |
| 11 | 01:10–01:17 | no effect와 not used 구분 |
| 12 | 01:17–01:24 | off-distribution intervention |
| 13 | 01:24–01:31 | 통제된 변화와 과도한 변화 비교 |
| 14 | 01:31–01:38 | superposition으로 인한 동시 손상 |
| 15 | 01:38–01:45 | intervention의 증거 수준 정리 |
| 16 | 01:45–01:52 | feature에서 circuit으로 연결 |

총 112초. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다.
