# Scene 05 — 원은, 어느 방향에서 가장 늘어날까?
## 목적과 핵심 주장
원은, 어느 방향에서 가장 늘어날까?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
신경망에도, 변화율이 방향에 작용한다
## TTS 원문과 확정 길이
입력 주변의 작은 원 위에서는, 모든 변화가 중심에서 같은 거리만큼 떨어져 있습니다.

이 변화를 신경망에 통과시키면, 국소적인 선형 근사에서는 원이 타원으로 바뀔 수 있습니다.

야코비안은 고정하고, 입력 변화의 방향만 돌려보겠습니다.

어떤 방향에서는 출력이 크게 늘어나고, 다른 방향에서는 줄어듭니다.

가장 많이 늘어나는 방향의 확대 비율을, 야코비안의 가장 큰 특잇값이라고 합니다. 같은 입력 크기라도 방향에 따라 반응이 달라지는 것입니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 38초. 원래 화면 기준은 38초.
## 화면 구성과 시간대별 애니메이션
단위 방향 원 → diag(1.8,.5) 타원 → theta30/90/0도 → gain1.58/.5/1.8 → sigma_max
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
원은, 어느 방향에서 가장 늘어날까?, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
다음 층에서도 같은 방향으로 늘어날까?
## 수학 조건·과장 방지
J=diag(1.8,.5) 국소 예시. 실제 입력 반경ε의 그림을 확대해 ||v||=1 방향으로 표시. ratio=sqrt((1.8cosθ)²+(.5sinθ)²), θ30 gain≈1.578765. σmax=1.8, 최소=.5. 일반 네트워크의 보장값이 아니다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

