# Scene 03 — 같은 강도라도, 회전축 방향이 다르면
## 목적과 핵심 주장
같은 강도라도, 회전축 방향이 다르면를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
주변의 변화율을 한 장에 기록하다
## TTS 원문과 확정 길이
이번에는 주변 흐름의 늘어남과 압축 효과를 고정하겠습니다.

길이가 같은 보티시티 벡터를, 늘어나는 방향과 압축되는 방향에 각각 놓아보겠습니다.

늘어나는 방향과 정렬되면 강해지고, 압축되는 방향과 정렬되면 약해지는 효과를 받습니다.

비스듬한 방향에서는 길이뿐 아니라 방향도 달라질 수 있습니다.

회전의 크기만큼, 회전축이 주변 변형의 어느 방향을 가리키는지도 중요합니다. 여기서는 점성의 영향을 잠시 제외했습니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 34초. 원래 화면 기준은 34초.
## 화면 구성과 시간대별 애니메이션
고정 S의 x-z 단면 → 같은 길이 ω 방향0/90/45도 → 짧은 시간 뒤 변화 → signed 증감 지표
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
같은 강도라도, 회전축 방향이 다르면, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
신경망에도, 변화율이 방향에 작용한다
## 수학 조건·과장 방지
고정하는 것은 S=diag(-.5,-.5,1)이고 독립적으로 omega 방향을 비교한다. 하나의 고정된 전체 Ju에서 omega를 독립적으로 바꿀 수 있다고 주장하지 않는다. 1/2 D|ω|²/Dt=ωᵀSω (ν=0,curl f=0). A=(Ju−Juᵀ)/2, Aω=0; 자체 vorticity를 국소 강체회전 성분이 기울인다고 하지 않는다. 짧은 뒤 exp(.3S)omega 설명용 비교.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

