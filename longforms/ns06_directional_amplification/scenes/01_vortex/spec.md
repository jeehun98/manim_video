# Scene 01 — 소용돌이는 왜 축을 따라 늘어났을까?
## 목적과 핵심 주장
소용돌이는 왜 축을 따라 늘어났을까?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
5막 마지막의 값의 크기와 방향별 증폭에 관한 질문
## TTS 원문과 확정 길이
앞에서 삼차원의 소용돌이는 회전축을 따라 늘어나면서, 회전의 강도가 커질 수 있다고 했습니다.

왜 하필 회전축을 따라 늘어나는 것이 중요할까요?

보티시티 벡터의 방향은 국소적인 회전축을, 길이는 회전의 강도를 나타냅니다.

이 축을 따라 주변의 속도가 달라지면, 소용돌이를 잡아 늘리는 효과가 생길 수 있습니다.

반대로 압축되면 회전이 약해질 수 있고, 변형에 의해 축의 방향도 기울어질 수 있습니다.

- TTS: 미확정. 사용자 허용에 따라 화면 제작 우선.
- 화면: 34초. 원래 화면 기준은 34초.
## 화면 구성과 시간대별 애니메이션
부피 보존 3D 관 → 보티시티 축 → 축 늘어남/압축/전단 비교
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
소용돌이는 왜 축을 따라 늘어났을까?, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
주변의 변화율을 한 장에 기록하다
## 수학 조건·과장 방지
점성과 외력의 컬에 의한 생성은 제외해 변형 효과만 분리한 개념도. F=diag(s⁻¹/²,s⁻¹/²,s), 이후 x←x+kz 전단은 detF=1. 보티시티는 Fω0로 변화하는 비점성 국소 변형 예시. 기울어짐이 순수 강체 회전 때문이라고 하지 않는다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html
- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/

