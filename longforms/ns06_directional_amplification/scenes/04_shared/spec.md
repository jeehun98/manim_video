# Scene 04 — 신경망에도, 변화율이 방향에 작용한다
## 목적과 핵심 주장
신경망에도, 변화율이 방향에 작용한다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
같은 강도라도, 회전축 방향이 다르면
## TTS 원문과 확정 길이
이제 하나의 신경망 입력을 고정하고, 그 주변에서 아주 작은 변화를 주겠습니다.

변화의 크기가 같아도, 어느 방향으로 움직였는지에 따라 출력의 반응은 달라질 수 있습니다.

이 작은 반응을 계산할 때도 야코비안이 등장합니다.

신경망의 야코비안에 작은 입력 변화 벡터를 곱하면, 출력의 변화를 국소적으로 근사할 수 있습니다.

유체에서는 공간의 변화율이 보티시티에 작용했습니다. 신경망에서는 입력에 대한 변화율이 입력의 작은 변화에 작용합니다.

공통점은 행렬이 방향 벡터에 작용한다는 구조입니다. 유체의 시간 발전과 신경망의 입력 반응은 서로 다른 현상입니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 40초. 원래 화면 기준은 40초.
## 화면 구성과 시간대별 애니메이션
유체 관/NN 입력 원 → 작은 입력 원과 출력 타원 → 두 Jacobian×Vector 색상 대응 → 결과 해석 구별
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
신경망에도, 변화율이 방향에 작용한다, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
원은, 어느 방향에서 가장 늘어날까?
## 수학 조건·과장 방지
미분 가능한 f의 기준입력에서 δy=Jf(x)δx+o(||δx||). 원-타원은 magnified local linear model, 실제 비선형 신경망의 큰 입력 영역을 정확히 타원으로 변환한다고 하지 않는다. Juω는 미분 항, Jfδx는 국소 출력 변화 근사.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

