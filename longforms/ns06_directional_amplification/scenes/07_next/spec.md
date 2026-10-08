# Scene 07 — 진짜 공통점은, 방향에 따른 작용
## 목적과 핵심 주장
진짜 공통점은, 방향에 따른 작용를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
다음 층에서도 같은 방향으로 늘어날까?
## TTS 원문과 확정 길이
이제 소용돌이와 신경망을 나란히 보겠습니다.

유체의 변화율은 보티시티의 시간 변화에 관여하고, 신경망의 변화율은 작은 입력 변화에 대한 출력 반응을 알려줍니다.

유체의 순간적인 강도 증감은 변형률과의 정렬로, 신경망의 최대 국소 확대는 야코비안의 특잇값으로 살펴봅니다.

두 현상을 같은 것으로 만드는 것이 아니라, 변화율이 모든 방향에 똑같이 작용하지 않는다는 구조를 공유하는 것입니다.

이제 입력 공간에서 파라미터 공간으로 질문을 옮겨보겠습니다. 손실 지형에도 가파른 방향과 평평한 방향이 함께 있을 수 있습니다.

그렇다면 단 하나의 가파른 방향이 전체 학습을 제한할 수도 있을까요? 다음 막에서는 이 방향성을 헤시안으로 살펴보겠습니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 42초. 원래 화면 기준은 42초.
## 화면 구성과 시간대별 애니메이션
소용돌이/원타원 나란히 → Local derivative×Direction → S 정렬/σ 구별 → 우측만 손실 등고선 → 7막 Hessian 질문
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
진짜 공통점은, 방향에 따른 작용, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
7막: Hessian과 가파른 방향
## 수학 조건·과장 방지
입력 Jacobian과 파라미터 손실 Hessian은 서로 다른 미분 대상. 다음 막 contour L=.5(4θ1²+.25θ2²) 예시, stiffness 방향x. 유체 자체vorticity의 antisymmetric part Aω=0. 결과 동일성/신경망 유체 PDE 동일성 주장하지 않는다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

