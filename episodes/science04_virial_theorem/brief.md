# 과학의 한 장면 04 — Virial Theorem 제작 기준

- 질문: 저울에 올릴 수 없는 멀리 있는 은하단의 질량을 어떻게 잴까?
- 목표: 같은 크기에서 대표 속도가 빠를수록 M∝v², 같은 대표 속도에서 클수록 M∝R이라는 직관을 얻고 비리얼 평형 및 속도 분산과 연결한다.
- 길이: 83초, 1080×1920, 30fps, 무음. 01편의 대사 글자 수당 시간 기준으로 총길이를 정하고 10개 장면을 대사 길이 비율로 배분한다.
- 순서: 저울 없는 대상 → 분광 속도 → 속박과 탈출 → v 두 배/M 네 배 → R 두 배/M 두 배 → M∼Rv²/G → 비리얼 에너지 → 시선 속도 분산 → 질량 추정의 조건 → 두 직관 요약.
- 비교는 비슷한 밀도 구조와 정의의 크기, 대표 속도를 쓰는 안정된 계를 가정한다. 조건 없이 임의의 빠른 은하 하나에서 전체 질량을 확정하지 않는다.
- 전체 계의 평균 이동을 뺀 내부 속도다. v는 대표적 내부 RMS 속도이며 단일 은하의 속도가 아니다.
- 고립된 자기중력 뉴턴계에서 시간 평균 2〈K〉+〈U〉=0, U<0. 크기 변화의 시간 평균이 안정되고 표면 항·외압 등은 무시한다. 계수는 구조와 측정 정의에 따라 달라진다.
- U=−aGM²/R, K=(1/2)M〈v²〉로부터 M∼R〈v²〉/G. 이 장면은 차원 및 비례 관계를 설명하며 계수를 1로 확정하지 않는다.
- 관측의 σᵥ는 시선 방향 속도의 표준편차다. 통상 velocity dispersion을 속도 분산이라 부르지만 통계학적 분산은 σᵥ²다.
- M∼C R σᵥ²/G에는 투영, 운동 비등방성, 분포 구조에 따른 계수 C가 필요하다. 등방적 3D 운동에서 〈v²〉=3σ_los²이나 이 3까지 포함해 계수 C로 설명한다.
- 대표적이고 오염이 적은 회원 은하 표본, 거리 및 크기 측정이 필요하다. 크기 R은 무조건 겉보기 반지름과 동일하지 않는다.
- 이전 Bullet Cluster처럼 합병·충돌 중인 계는 평형 가정부터 확인해야 한다. 영상 내에서 이를 명시한다.
- 은하단 점 운동은 경계가 유지되는 설명용 운동으로 실제 N-body 시뮬레이션이 아니다. 비교 화살표는 대표 속도의 상대적 크기다.
- Scene 3만 같은 초기 위치와 속도에서 서로 다른 점질량 중력장을 velocity-Verlet로 적분해 탈출/속박을 비교한다. 이 탈출 그림 자체를 비리얼 정리의 증명으로 제시하지 않는다.
- 질량은 보라색 막대 길이로 표시한다. 질량 증가를 실제 공간 크기 증가로 혼동하지 않게 한다. 크기 비교는 경계 반지름으로 표시한다.
- Scene 5는 반지름이 두 배인 계의 궤도 위상 변화율을 절반으로 해 같은 이동속도를 유지한다.
- 수식은 Cambria/Pango 문자 조합으로 렌더한다. 별도 LaTeX 설치를 요구하지 않는다.
- 대본과 자막은 숫자·원래 영문 표기를 쓰고 발음 표기는 TTS 전용 파일에 둔다.

## 확인한 자료

- Jo Bovy, Dynamics and Astrophysics of Galaxies, virial theorem: https://galaxiesbook.org/chapters/I-04.-Equilibria-of-Collisionless-Stellar-Systems_2-The-virial-theorem.html
- C. L. Sarazin, X-ray Emission from Clusters of Galaxies, dynamical masses: https://ned.ipac.caltech.edu/level5/March02/Sarazin/Sarazin2_8.html
- D. Merritt, Internal Dynamics of Galaxy Clusters: https://ned.ipac.caltech.edu/level5/Sept03/Merritt/Merritt2.html

## 타이밍

`python scripts/retime_science04.py --duration 83` 후 미리보기와 최종 렌더. timing.json과 SRT를 함께 갱신한다.

- 화면의 `2K+U=0`에서 K와 U는 시간 평균값임을 바로 아래 문구로 명시한다. 평균 괄호의 폰트 누락을 피하며 시간 평균 조건을 유지한다.
