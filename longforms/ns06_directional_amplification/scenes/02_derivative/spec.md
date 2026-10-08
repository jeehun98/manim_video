# Scene 02 — 주변의 변화율을 한 장에 기록하다
## 목적과 핵심 주장
주변의 변화율을 한 장에 기록하다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
소용돌이는 왜 축을 따라 늘어났을까?
## TTS 원문과 확정 길이
유체의 속도는 위치에 따라 달라집니다. 이동하는 방향에 따라, 만나는 속도의 변화도 다릅니다.

아주 작은 거리를 세 방향으로 움직이며, 속도가 어떻게 달라지는지 기록해 보겠습니다.

이 정보를 모은 행렬을 속도장의 야코비안이라고 합니다.

여기에 보티시티 벡터를 곱하면, 회전축 방향을 따라 속도장이 어떻게 변하는지 계산할 수 있습니다.

이 곱은 다음 순간의 보티시티 자체가 아니라, 보티시티의 시간 변화에 들어가는 하나의 항입니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 36초. 원래 화면 기준은 36초.
## 화면 구성과 시간대별 애니메이션
x/y/z 작은 변위 → 속도 차이 → Jacobian 카드 → ω 통과 → 시간 변화율 항
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
주변의 변화율을 한 장에 기록하다, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
같은 강도라도, 회전축 방향이 다르면
## 수학 조건·과장 방지
Jij=∂ui/∂xj convention. (ω·∇)u=Juω 정확한 항등식. 물질 미분Dω/Dt=Juω+νΔω+curl f. Juω의 단위는 ω/time이며 NN의 유한 확대비와 다르다. 프로브예시 J=[[-.5,-.5,0],[.5,-.5,0],[0,0,1]], omega=(0,0,1).
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

