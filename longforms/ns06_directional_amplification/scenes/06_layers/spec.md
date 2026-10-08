# Scene 06 — 다음 층에서도 같은 방향으로 늘어날까?
## 목적과 핵심 주장
다음 층에서도 같은 방향으로 늘어날까?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
원은, 어느 방향에서 가장 늘어날까?
## TTS 원문과 확정 길이
이제 작은 변화가 여러 층을 통과한다고 생각해 보겠습니다.

한 층에서 변한 방향과 크기는 다음 층으로 전달됩니다. 다음 층의 야코비안이 여기에 다시 작용합니다.

연속된 층에서 늘어나는 방향과 잘 맞으면, 작은 차이가 점점 커질 수 있습니다.

하지만 다음 층에서 압축되는 방향과 만난다면, 앞에서 커진 변화가 다시 작아질 수 있습니다.

각 층의 최대 확대 비율만큼, 층 사이에서 방향이 어떻게 연결되는지도 중요합니다. 이 층별 합성은 유체의 시간 발전과 구별해야 합니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 36초. 원래 화면 기준은 36초.
## 화면 구성과 시간대별 애니메이션
3층 선형 국소 모형 → 1/1.8/3.24/5.832 → 두번째 층 압축축 교체 → 1/1.8/.9/1.62
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
다음 층에서도 같은 방향으로 늘어날까?, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
진짜 공통점은, 방향에 따른 작용
## 수학 조건·과장 방지
연쇄법칙 Jtotal=JL…J1 (각 J는 해당 기준 hidden state에서 평가). aligned 3×diag(1.8,.5) e1gain5.832, middle=diag(.5,1.8) e1gain1.62. 각 σmax1.8이며 ∥product∥≤∏σmax, equality 보장하지 않는다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

