# 신경망의 수학 2부 03 제작 기준

## 제목과 목표

**뉴런 하나는 하나의 의미를 담당할까? — Polysemanticity**

하나의 뉴런이 고양이, 바퀴, 곡선처럼 서로 다른 입력에 강하게 반응하는 관찰에서 시작한다. 이를 “뉴런 안에 여러 의미가 든다”로 끝내지 않고, 뉴런은 representation 공간의 좌표축이고 feature는 여러 뉴런에 걸친 방향일 수 있다는 관점 전환으로 이끈다. 마지막에는 섞인 activation을 sparse feature 방향으로 분해하는 다음 문제와 Sparse Autoencoder를 예고한다.

## 정확성 기준

- 높은 activation 몇 사례만으로 뉴런의 의미를 확정하지 않는다. activation ranking은 가상의 설명용 예시다.
- Polysemanticity는 한 뉴런이 여러 서로 다른 feature 또는 개념과 연관된 activation을 보이는 현상으로 설명한다. Monosemanticity는 한 뉴런이 하나의 명확한 feature와 대응하는 이상적 대비다.
- Superposition과 Polysemanticity를 동치로 쓰지 않는다. 차원보다 많은 feature가 비직교 방향으로 표현되면 각 neuron coordinate가 여러 feature의 성분을 받을 수 있어 polysemantic neuron이 **나타날 수 있다**고 표현한다.
- `neuron = coordinate axis`, `feature = direction`은 이 편의 기하학적 해석 틀이지 모든 feature가 항상 선형 방향 하나로 완전히 기술된다는 단정이 아니다.
- 좌표 회전 예시는 동일한 기하학적 점이 basis에 따라 다른 coordinate를 갖는다는 사실만 설명한다. 45도 회전 시 `(0.8, 0.3) → (0.78, −0.35)`를 사용한다.
- `h ≈ Σ zᵢvᵢ`와 sparse `z`는 다음 편의 feature dictionary / Sparse Autoencoder 문제를 여는 이상화된 모델이다.

## 화면 원칙

- Neuron 17은 세로형 activation meter와 분홍색 강조로 일관되게 표시한다.
- 입력은 저작권 이미지 대신 `CAT`, `WHEEL`, `ARC`의 추상 아이콘 카드로 표현한다.
- neuron-centric 관점은 상자와 1:1 화살표, feature-centric 관점은 좌표계 위의 다색 방향으로 대비한다.
- 좌표축은 회색과 낮은 불투명도, feature direction은 시리즈 색상과 높은 불투명도로 구분한다.
- `can emerge`, `may`, `can` 같은 조건 표현이 화면과 내레이션에서 유지되도록 한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:07 | Neuron 17과 고양이 반응 |
| 2 | 00:07–00:14 | One Neuron = One Feature 직관 |
| 3 | 00:14–00:21 | 바퀴·곡선에도 높은 반응 |
| 4 | 00:21–00:28 | 여러 의미 상자 해석과 Superposition 회상 |
| 5 | 00:28–00:35 | neuron coordinate와 feature direction 구분 |
| 6 | 00:35–00:42 | 여러 feature의 한 neuron 축 투영 |
| 7 | 00:42–00:49 | Neuron ≠ Feature 관점 전환 |
| 8 | 00:49–00:57 | basis 회전과 coordinate 변화 |
| 9 | 00:57–01:04 | Neuron 17의 재해석 |
| 10 | 01:04–01:11 | Polysemantic / Monosemantic 비교 |
| 11 | 01:11–01:18 | Superposition과 가능성 관계 |
| 12 | 01:18–01:25 | 뉴런별 라벨링의 한계 |
| 13 | 01:25–01:32 | 축이 아니라 feature를 찾는 해석 |
| 14 | 01:32–01:40 | activation의 sparse feature 분해 |
| 15 | 01:40–01:48 | Neuron View에서 Feature View로 전환, SAE 예고 |

총 108초. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다.

