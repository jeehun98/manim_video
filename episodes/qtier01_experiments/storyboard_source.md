# 양자역학 실험 티어리스트 — Manim 영상화 콘티

총 167초 · 세로형 9:16 · 9개 실험 · S/A/B/C 티어

이번 영상의 핵심은 처음부터 실험 9개를 작은 아이콘으로 배치하고, 설명할 실험만 확대해 애니메이션으로 전환한 뒤 티어표에 배치하는 것이야.

일반적인 티어리스트처럼 이미지 하나를 옮기는 데 그치지 않고, 각 실험의 특징적인 물리 현상이 아이콘 내부에서 직접 움직이도록 만들면 좋아.

## 1. 전체 화면 디자인

QUANTUM EXPERIMENTS

1900 — 1992

S

EXPERIMENT CARDS

A

EXPERIMENT CARDS

B

EXPERIMENT CARDS

C

EXPERIMENT CARDS

ACTIVE EXPERIMENT

## 전자 이중슬릿

입자 하나씩 검출 → 간섭무늬 형성

열

빛

준위

자석

산란

파동

슬릿

얽힘

지우개

9 EXPERIMENTS · CHRONOLOGICAL ORDER

9:16 레이아웃 개념도. 실제 영상에서는 중앙 실험 애니메이션이 가장 큰 비중을 차지하고, 하단 아이콘은 진행 상태를 표시함.

### 화면 영역 비율

| 영역           | 세로 화면 내 위치 | 역할                |
| ------------ | ---------- | ----------------- |
| 상단 0\~30%    | 티어표        | 실험 평가 결과 누적       |
| 중앙 30\~81%   | 메인 실험 무대   | 실험 확대 및 물리 현상 시각화 |
| 하단 81\~94%   | 9개 아이콘     | 순서 표시 및 다음 실험 선택  |
| 최하단 94\~100% | 여백         | 플랫폼 UI와 겹침 방지     |

자막은 중앙 실험 무대의 아래쪽에 위치시키되, 물리 현상과 겹칠 때는 애니메이션 자체를 살짝 위로 이동시키는 방식이 적합해.

## 2. 아이콘 디자인

각 아이콘은 작은 크기에서도 구별되도록 서로 다른 실루엣을 가져야 해.

01

흑체복사

연속 스펙트럼

02

광전효과

빛과 전자

03

프랑크–헤르츠

에너지 준위

04

슈테른–게를라흐

빔 분리

05

콤프턴 산란

방향·파장 변화

06

전자 회절

회절무늬

07

전자 이중슬릿

두 개의 슬릿

08

벨 부등식

두 입자 상관관계

09

양자 지우개

경로 정보

실제 Manim에서는 이 아이콘을 단순한 PNG로 사용하는 것보다, `VGroup`으로 구성한 미니 벡터 도형을 권해. 그래야 하단의 작은 기호가 확대되면서 실제 실험 장치로 변형되는 연출이 가능해.

## 3. 공통 전환 애니메이션

모든 실험에 동일한 패턴을 적용하면 영상 전체의 완성도와 리듬이 좋아져.

선택

아이콘 강조

확대

중앙 무대로 이동

실험

물리 시뮬레이션

# A

평가

티어표에 고정

공통 모션: 선택 0.2초 → 확대 0.45초 → 실험 5\~11초 → 평가 0.65초

- 선택되지 않은 아이콘은 약 35% 밝기로 유지.
- 현재 선택된 아이콘만 푸른빛을 발산하고 1.15배 확대.
- 중앙 실험이 시작되면 주변 설명과 무관한 그래픽은 숨김.
- 등급을 말하는 순간 실험 도형을 작게 축소해 해당 티어로 이동.
- 티어표에 배치된 카드는 다시 움직이지 않으며 계속 누적.

## 4. 실험별 상세 콘티

### Scene 01 — 흑체복사 (0:05–0:24)

1900

흑체복사 · C 티어

[PPT - Chapter 03 Experimental Basis for Quantum Theory PowerPoint Presentation - ID:814839](https://images.openai.com/static-rsc-4/XSTKNv2AR5SMB3oRNYy7UyWkjzFRe-1XgndNReoZ1lE8lKCEN8kdkPyhQvjT78kBjVRXCHqVYmRQQsmrwbU8THXWNM4SUakE8hbbMK3LW3asMR1AhpXC7BeOeEwIih6bsN8Euk2qUTv0lYVL-4oZvRL4PV_NC6nTqgwGsO7ww90?purpose=inline)

[electromagnetic radiation - Is the light from the Sun the same as the light from a bulb? - Physics Stack Exchange](https://images.openai.com/static-rsc-4/i3KIG9BOU21w8esPcyUFnLxzFw1mbxchKBS5WPMSv3fQvo97J6ZcLDmyWfAFOoE5ZmJ1I8fqmWeMivYFCyzdObLSba4jGSQwXHd6hxweeZoMKsVFpzRJ1F7nR9fm1toSFsqem7YX_VZ_oEOzt9qrqL3Nm8RMnOO0nzXG6ACzIVk?purpose=inline)

[PPT - Quantum physics (quantum theory, quantum mechanics) PowerPoint Presentation - ID:1885690](https://images.openai.com/static-rsc-4/-OhmYe_e7NS2F1QpyRkbuJkAYl_1SUwbRuhxQYRrQsFZysqYIsVkVBpIyhBjDpXUYrLC9dcKQ-j6lBmu06CqsUc3s4wXxRU6bJPb4AtMKkcSgC1AYidxxpNUjXODP-RvTx5F4RmJPeNQuPV5gfeA4Kic7janbAhfLC8jA3ogNuU?purpose=inline)

핵심 시각화: 가열된 물체 → 온도에 따른 복사 스펙트럼 → 고전 이론과 실제 결과의 차이.

| 시간     | 나레이션 대응         | 화면 연출                                         |
| ------ | --------------- | --------------------------------------------- |
| 05–07초 | 1900년, 흑체복사     | 하단 첫 아이콘이 중앙으로 확대. 발광하는 원형 물체 등장              |
| 07–12초 | 뜨거운 물체에서 방출되는 빛 | 물체의 온도가 올라가고 빨강·주황·흰색으로 변화. 오른쪽에는 스펙트럼 그래프 생성 |
| 12–18초 | 플랑크의 가정         | 그래프에 실제 관측과 맞는 플랑크 곡선 표시. 고전 이론 곡선과 비교        |
| 18–24초 | C 티어            | 두 곡선의 차이 강조 후 물체와 그래프를 카드로 축소, C 칸에 배치        |

Manim 구현 지시

- `Axes`로 가로축 `Wavelength`, 세로축 `Spectral radiance` 설정.
- 실제 형태를 반영한 플랑크 분포의 봉우리를 부드러운 파란 곡선으로 그림.
- 고전 예측은 짧은 파장 쪽에서 과도하게 증가하는 점선으로 표현.
- 고전 곡선은 `CLASSICAL`, 플랑크 곡선은 `PLANCK`로 표시.
- 설명의 핵심은 곡선 두 개가 달랐고, 새로운 가정으로 관측값을 설명했다는 데 있음.

### Scene 02 — 광전효과 (0:24–0:41)

1905

광전효과 · A 티어

[Waves Revision Notes — OCR A-Level | MasteryMind](https://images.openai.com/static-rsc-4/rE5v-Bfq49qYBLOth1pGZYGuKId5c_H2Qow1oUeB3q3tOCbYWYeyqqcEU0E1RcenVT3nEv8tL5DFw8ZgY_bRByFS6MKb4ejmf4oA6w0efSTMMxe7IwiYMwYpIw9DMbJwiuQ1U0zftpnf8B38i4fm7zrsaxpBA3C5PjMvjf73tXg?purpose=inline)

[masterymind.co.uk](https://masterymind.co.uk/study-guides/physics-ocr-a-level-waves?utm_source=chatgpt.com)

핵심 시각화: 광자의 주파수를 바꾸었을 때 전자 방출 여부가 달라지는 모습.

| 시간     | 화면 연출                                        |
| ------ | -------------------------------------------- |
| 24–26초 | 두 번째 아이콘 확대. 금속판과 광원 등장                      |
| 26–31초 | 빨간색 광자를 매우 많이 비춤. 세기를 높여도 전자가 방출되지 않음        |
| 31–37초 | 광자를 파란색으로 변경. 개별 광자의 에너지가 증가하고 전자가 금속 밖으로 방출 |
| 37–41초 | 금속에서 튀어나온 전자들이 작은 카드 속으로 모이면서 A 티어로 이동       |

세부 효과

낮은 주파수

강한 빛 · 방출 없음

높은 주파수

전자 방출

단순히 빛의 색깔만 바뀌는 것이 아니라, 광자의 진동 간격과 금속에서 튀어나오는 전자가 연결되어야 직관적이야.

### Scene 03 — 프랑크–헤르츠 (0:41–0:57)

1914

프랑크–헤르츠 · B 티어

[P115: Frank-Hertz-Versuch](https://images.openai.com/static-rsc-4/pcjmYUPmIfX2y6UNU3qLLFhBm74_eSlbejy41F-dok0PX6PYio7MjVG85So6kQPqip4ngE5TAURomDealyOur6dIOFpQmO8bTZHa1k1-xoetC7UavhBipSw9n5lHBhw_eDLWMldXx31b3Fg-E7SaAp2aLJrK-MaHwP5H6wIYwQ8?purpose=inline)

[physikkursq3lichtundquanten.blogspot.com](https://physikkursq3lichtundquanten.blogspot.com/2021/01/p115-frank-hertz-versuch.html?utm_source=chatgpt.com)

핵심 시각화: 전압을 점점 증가시키면 특정 지점에서 전자가 원자에 에너지를 전달하고, 수집 전류가 급격히 감소하는 현상.

| 시간     | 화면 연출                                        |
| ------ | -------------------------------------------- |
| 41–44초 | 세 번째 아이콘 확대. 원자와 이동하는 전자 등장                  |
| 44–50초 | 전자가 가속되다가 원자와 충돌. 특정 에너지에 도달했을 때 전자가 에너지를 잃음 |
| 50–56초 | 충돌 장면 옆에 전류–전압 그래프가 나타나며 반복적인 전류 감소 지점을 강조   |
| 56–57초 | 원자와 전자 아이콘 축소 → B 티어                         |

Manim 구현 지시

- 전자: 작은 청색 점.
- 수은 원자: 중앙의 핵과 흐릿한 바깥 원으로 단순화.
- 전자의 에너지를 수치와 함께 증가시키고, 예시로 `4.9 eV`에서 비탄성 충돌.
- 충돌 이후 원자는 밝게 발광하고 전자의 운동 속도는 감소.
- 그래프의 첫 번째 전류 감소 지점에만 `4.9 V` 표시.

원자에 에너지가 전달되는 모습을 원자가 물리적으로 튕겨 나가는 것처럼 그리지 말고, 원자의 내부 에너지 상태가 바뀌는 효과로 표현해야 해.

### Scene 04 — 슈테른–게를라흐 (0:57–1:11)

1922

슈테른–게를라흐 · A 티어

[Stern Gerlach Experiment. This was originally written by the… | by Roopam Taneja | Medium](https://images.openai.com/static-rsc-4/-7fjdkumehn-E_bFdQyDceOpWMggKUuo4oqaApJ2ip5wKXFGynwxs1c0HcGotpc0K5P-hNevNxWgZY9DrIns1BQ4GHWGdJ7TNk8wZKmz9uBq3017NcTuewhKCq3HV_zYfSKwRQZazmPXOFcr9MzXPn6PcSRTNf4aYq4XhFdGz54?purpose=inline)

[medium.com](https://medium.com/%40roopam_t/stern-gerlach-experiment-895ccba2a0c4?utm_source=chatgpt.com)

핵심 시각화: 하나의 입자 빔이 자기장을 통과하면서 두 갈래로 분리.

| 시간     | 화면 연출                                     |
| ------ | ----------------------------------------- |
| 57–59초 | 자석 아이콘을 확대하며 N극과 S극 등장                    |
| 59–66초 | 왼쪽에서 은 원자 빔이 진입. 자기장 내부에서 빔이 위아래 두 갈래로 분리 |
| 66–70초 | 오른쪽 검출판에 두 개의 분리된 검출 분포 형성. 연속 분포 예측과 비교  |
| 70–71초 | 두 점을 카드로 축소 → A 티어                        |

특히 중요한 연출

연속적인 분포 예측 vs 두 개의 분리된 검출 분포

고전적인 예측과 실제 결과를 짧게 겹쳐 보여주는 편이 자석만 등장시키는 것보다 훨씬 설명력이 높아.

### Scene 05 — 콤프턴 산란 (1:11–1:26)

1923

콤프턴 산란 · B 티어

[Efek Compton: Pengertian, Persamaan, dan Panjang Gelombangnya](https://images.openai.com/static-rsc-4/Y-7Pf3YiLBGqAzdYf0j_nh1WqubvB8OAM0KOyPeMQY5orgM8Bn0EyDRsgePHi271bFNJNss0NvbdD4c39ZHpztnLqFmwd_0Ib1sEY2PHczBojPhjsVviZe2Ibs00gEmwdZHGJclWtfpk77bavP8mfx3EHOYSSaYMK3FcjxCxTzQ?purpose=inline)

[kompas.com](https://www.kompas.com/skola/read/2022/03/08/134805969/efek-compton-pengertian-persamaan-dan-panjang-gelombangnya?utm_source=chatgpt.com)

핵심 시각화: 광자가 전자와 충돌한 뒤 방향이 바뀌고 파장이 길어짐.

| 시간     | 화면 연출                                           |
| ------ | ----------------------------------------------- |
| 71–74초 | 파란 파형의 X선과 정지해 있는 전자 등장                         |
| 74–78초 | X선이 전자와 상호작용. 전자는 아래쪽으로 반동하고 산란된 광자는 다른 방향으로 이동 |
| 78–83초 | 입사 광자와 산란 광자의 파장 비교. 산란 후 파형이 길어졌음을 강조          |
| 83–86초 | 입사·산란 화살표를 하나의 아이콘으로 축소 → B 티어                  |

구체적인 물리 표현

- 입사 광자: 짧은 파장의 푸른 물결.
- 산란 광자: 간격이 더 넓은 청록색 물결.
- 반동 전자: 노란 입자.
- 충돌 전후 `λ' > λ` 표시.
- 배경에 운동량 보존을 암시하는 방향 화살표.

이 연출에서는 실제 광자가 공간에서 물결 모양의 궤도를 따라 날아간다는 뜻이 아니라, 파장 차이를 나타내는 도식임을 구별해 주는 것이 좋아.

### Scene 06 — 전자 회절 (1:26–1:43)

1927

전자 회절 · A 티어

[\[2.0\] The Bohr Atom & The New Quantum Mechanics](https://images.openai.com/static-rsc-4/ZYho9rxC38IXqzRzHYgSdmAcbRkMY1flBPYA-irx_E1f6U-Ytemqw1OXgPQbpfhtRnOQsBVqzJrWbcyZ9C9a5c_PER9fzsqCrWBHZUactsUdNlPteV3u-Npx4KGgZioKuhL6Klgjqmgk4zhpIgvA5_ZtyZxi0Pqk1jrAwiKtLkI?purpose=inline)

[vc.airvectors.net](https://vc.airvectors.net/tpqm_02.html?utm_source=chatgpt.com)

핵심 시각화: 전자빔 → 결정 격자 → 특정 각도에서 강한 산란 신호.

| 시간       | 화면 연출                                    |
| -------- | ---------------------------------------- |
| 86–89초   | 파동 아이콘 확대. 결정 격자 등장                      |
| 89–94초   | 왼쪽에서 전자 빔이 결정으로 입사. 원자 배열에서 여러 산란 파동이 퍼짐 |
| 94–97초   | 파동들이 특정 방향에서 보강간섭을 일으키는 모습 강조            |
| 97–102초  | 각도에 따른 산란 강도 그래프 생성. 뚜렷한 회절 피크를 표시       |
| 102–103초 | 격자와 회절 피크 축소 → A 티어                      |

Manim 구현 지시

- 결정 격자는 `Dot`의 규칙적인 배열.
- 각 원자에서 반원형 파동을 발생시키는 방식으로 산란 표현.
- 위상이 맞는 특정 방향의 파동을 밝게 강조.
- 검출기의 각도를 따라 이동하는 점과 산란 강도 그래프를 연동.

전자 회절에서 나타나는 결정 격자에 의한 회절과 다음에 등장하는 두 슬릿에 의한 간섭은 시각적으로 구분해야 해.

### Scene 07 — 전자 이중슬릿 (1:43–2:02)

1961

전자 이중슬릿 · S 티어

[File:Double-slit experiment results Tanamura four.jpg - Wikimedia Commons](https://images.openai.com/static-rsc-4/604CKFRXeBe2rfeewq0wqAia0k1d5sRHClwFVCxHh2IVOU6SUrSqWm6kzZxMpZdTQQIC75DR67e4rzhgObAWcb5KsTXlh5UaE3eLNG9difgO7sMeJiGBc03OvSz4IBcF7ozbSdtkFUuITFZSuRwR9b9RAwlOwWGVhGEOJyPCeb4?purpose=inline)

[commons.wikimedia.org](https://commons.wikimedia.org/wiki/File%3ADouble-slit_experiment_results_Tanamura_four.jpg?utm_source=chatgpt.com)

핵심 시각화: 전자가 하나씩 검출되어 점들이 쌓이지만, 그 분포는 간섭무늬를 형성한다.

| 시간       | 화면 연출                                                 |
| -------- | ----------------------------------------------------- |
| 103–106초 | 두 슬릿을 가진 장벽이 중앙에 등장                                   |
| 106–110초 | 전자들이 슬릿 방향으로 이동. 양쪽 슬릿에서 확률진폭을 나타내는 파동이 퍼짐            |
| 110–116초 | 오른쪽 검출판에 전자 검출 점이 하나씩 등장. 점들이 빠르게 누적되어 밝고 어두운 간섭무늬 형성 |
| 116–122초 | 개별 점과 최종 간섭무늬를 동시에 강조. 화면 상단의 S 티어가 붉게 밝아지고 카드가 이동    |

이 장면은 다른 실험보다 연출 밀도를 높이는 게 좋아.

하나씩 검출되는 전자 → 간섭 분포의 형성

검출 점의 위치는 단순히 규칙적으로 찍지 말고, 간섭 확률분포에서 표본추출하여 누적하는 형태가 좋아.

예를 들어 이상화된 두 슬릿 모델에서 검출 확률을 가우시안 포락선과 코사인 간섭항의 곱으로 설정하고, 그 분포에 따라 점을 생성할 수 있어.

### Scene 08 — 벨 부등식 검증 (2:02–2:26)

1972

벨 부등식 · S 티어

[Bell's Inequalities: Full Story](https://images.openai.com/static-rsc-4/JkcsBO-rHA8KsS1ZNsUsm9GPLlqNrcW-vm8JfadE2Famt0hohwDVlyAxEAbar3cBNE6UeF56NMpE-Pbdl5OWJwQvxKFRgVgSFWwQlwMI1nZYlwUok5TGTH68wwCOs1SNxkgBI88eePibPXo4d8835EHUrsd6e08YOnzcax8zHsc?purpose=inline)

[linkedin.com](https://www.linkedin.com/pulse/bells-inequalities-full-story-rui-manuel-de-almeida-pinheiro-jkhsf?utm_source=chatgpt.com)

핵심 시각화: 얽힌 입자쌍을 양쪽에서 독립적으로 측정하고, 측정 결과의 상관관계가 국소적 숨은변수 이론의 한계를 넘어서는 모습.

| 시간       | 화면 연출                                                       |
| -------- | ----------------------------------------------------------- |
| 122–125초 | 가운데 얽힌 광자쌍의 광원 등장. 두 광자가 좌우로 이동                             |
| 125–131초 | 화면 양쪽에 편광 측정기 등장. 입자가 미리 정해진 정보를 지녔다고 가정하는 작은 카드 표현         |
| 131–136초 | 측정기 방향을 여러 각도로 바꾸며 결과를 수집. 고전적 국소 숨은변수 모형의 상관관계 한계를 점선으로 표시 |
| 136–140초 | 양자역학의 예측을 나타내는 곡선과 실험 결과가 나타나고, 한계를 넘는 영역을 강조               |
| 140–146초 | `BELL INEQUALITY VIOLATED` 표시 후 S 티어에 카드 배치                 |

핵심 그래픽

이 부분은 복잡한 벨 부등식의 유도를 보여주지 않아도 돼. 대신 두 측정기가 다른 방향을 선택하고, 수많은 측정 결과의 통계적 상관관계를 비교한다는 과정이 반드시 보여야 해.

주의할 점은 두 입자 사이에 빛이나 신호가 즉시 전달되는 장면을 넣지 않는 것. 벨 부등식 위반은 초광속 통신을 의미하지 않아.

### Scene 09 — 양자 지우개 (2:26–2:47)

1992

양자 지우개 · C 티어

[File:Kim Quantum Eraser schematic.svg - Wikimedia Commons](https://images.openai.com/static-rsc-4/3f-xd0Flhig4cZgJoUGhfcevtN6wxo0ZsLt_pjaKFIImSfWopF3OPQsSUB8y-4AR6FXIzgGmmQEyN0nh8qQ7_gjhjSb_S4YpEesDo9HLz5srDcrJ5e69oj87HSI8dqmlC8muDEvsagVkCxyixIQulzyLR_LiXJhGZhl0vSepl6U?purpose=inline)

[commons.wikimedia.org](https://commons.wikimedia.org/wiki/File%3AKim_Quantum_Eraser_schematic.svg?utm_source=chatgpt.com)

핵심 시각화: 경로 정보를 구별할 수 있는 상태와 구별할 수 없는 상태에서 나타나는 간섭의 차이.

| 시간       | 화면 연출                                                            |
| -------- | ---------------------------------------------------------------- |
| 146–149초 | 마지막 아이콘 확대. 두 경로를 가진 간섭계 등장                                      |
| 149–153초 | 두 경로에 서로 구별되는 표식을 부여. 화면의 검출 확률분포에서 간섭이 사라짐                      |
| 153–159초 | 표식을 구별할 수 없는 측정 기저로 투영하고 결과를 분류. 각 조건부 데이터에서 간섭 패턴이 나타남          |
| 159–167초 | `PATH INFORMATION`과 `INTERFERENCE`의 관계를 잠깐 표시하고 C 티어에 마지막 카드를 배치 |

여기는 특히 간섭이 사라진 전체 데이터와, 분류 후 나타나는 조건부 간섭무늬를 구별해야 해.

전체 검출 결과 자체가 갑자기 간섭무늬로 변형되는 연출은 피하는 게 좋아. 1992년 실험의 구체적인 광학 구성에 맞추어 편광 표식과 편광 분석을 사용하는 편이 적절해.

## 5. Manim 제작 구조

이 영상은 실험별로 9개의 독립적인 Scene을 만들기보다는, 하나의 메인 Scene 안에서 실험 모듈을 교체하는 구조가 더 적합해.

특히 아이콘 확대 → 실험 시뮬레이션 → 티어표 배치가 하나의 객체가 변형되는 것처럼 보여야 하기 때문이야.

### 추천 프로젝트 구조

```
quantum_tierlist/
│
├── main.py
├── config.py
│
├── components/
│   ├── tier_board.py
│   ├── experiment_dock.py
│   ├── experiment_card.py
│   ├── timeline.py
│   └── transitions.py
│
├── experiments/
│   ├── blackbody.py
│   ├── photoelectric.py
│   ├── franck_hertz.py
│   ├── stern_gerlach.py
│   ├── compton.py
│   ├── electron_diffraction.py
│   ├── double_slit.py
│   ├── bell_test.py
│   └── quantum_eraser.py
│
└── assets/
```

### 실험별 시간 및 애니메이션 명세

| 실험       | 전체 시간 | 티어 | 메인 애니메이션       |
| -------- | ----- | -- | -------------- |
| 흑체복사     | 19초   | C  | 스펙트럼 곡선 비교     |
| 광전효과     | 17초   | A  | 광자 충돌과 전자 방출   |
| 프랑크–헤르츠  | 16초   | B  | 에너지 손실과 전류 감소  |
| 슈테른–게를라흐 | 14초   | A  | 입자 빔 분리        |
| 콤프턴 산란   | 15초   | B  | 광자의 파장 변화      |
| 전자 회절    | 17초   | A  | 결정에서의 회절       |
| 전자 이중슬릿  | 19초   | S  | 확률적인 점 누적      |
| 벨 부등식    | 24초   | S  | 상관관계 측정과 한계 위반 |
| 양자 지우개   | 21초   | C  | 경로 정보와 조건부 간섭  |

### 구현 시 중요한 기술적 선택

1\. 실제 객체의 확대와 시뮬레이션을 분리

`TransformFromCopy` 또는 `ReplacementTransform`을 이용해 아이콘을 확대하되, 복잡한 실험 그래픽은 별도의 `VGroup`으로 준비하는 것이 좋아.

확대 과정의 마지막에 아이콘의 형태를 실험 장치로 변환하면 자연스럽게 이어져.

2\. 모든 애니메이션의 시간은 나레이션 타임코드에 종속

실험 객체별로 `start_time`, `end_time`, `grade_time`을 정의하고, 전체 영상의 시간축에 따라 애니메이션을 실행하는 구조를 권해.

특히 각 실험을 티어표에 배치하는 순간은 사용자가 제공한 티어 발화 구간에 맞춰야 해.

3\. 메인 실험은 최대한 간결하게

복잡한 실제 실험 장치를 완벽히 재현하는 것이 목적은 아니야.

- 프랑크–헤르츠: 에너지 손실
- 슈테른–게를라흐: 두 갈래 분리
- 콤프턴 산란: 파장의 증가
- 전자 회절: 회절 피크
- 이중슬릿: 간섭 분포
- 벨 실험: 상관관계의 한계 위반

각각의 결정적인 현상 하나를 시각적으로 이해시키는 것이 우선이야.

## 6. 최종 티어표 완성 연출

마지막 C 티어 배치가 끝나면 중앙의 시뮬레이션 공간을 축소하고, 상단 티어표 전체를 화면 중앙으로 확대하는 것이 좋아.

### QUANTUM EXPERIMENT TIER LIST

1900 — 1992

## S

이중슬릿

벨 실험

## A

광전효과

슈테른–게를라흐

전자 회절

## B

프랑크–헤르츠

콤프턴 산란

## C

흑체복사

양자 지우개

어떤 실험이 가장 중요했을까요?

여기서 추가로 추천하는 연출은 하단 아이콘을 단순한 아이콘이 아니라 각각의 실험을 대표하는 작은 그래픽 카드로 구성하는 것이야.

예를 들어 흑체복사는 작은 스펙트럼 곡선, 슈테른–게를라흐는 두 갈래의 입자 빔, 전자 회절은 회절 피크, 이중슬릿은 간섭 줄무늬를 카드 내부에 넣는 거지.

이렇게 하면 영상이 진행되는 동안 하단에서는 아직 평가되지 않은 실험들의 특징을 미리 볼 수 있고, 상단에서는 평가가 끝난 실험들이 쌓이게 돼.

즉, 하단의 실험 목록이 하나씩 비워지고, 상단의 티어표가 채워지는 구조가 영상 전체의 시각적 흐름이 되는 거야.