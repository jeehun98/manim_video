# Scene 01 — 4막에서 남겨 두었던 질문
## 목적과 핵심 주장
4막에서 남겨 두었던 질문를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
7막 마지막의 가능한 상태와 도달 경로 질문
## TTS 원문과 확정 길이
앞에서 우리는 속도가 끝없이 커지는 유체의 모습을 생각해 봤습니다.

빠른 흐름이 나타나는 영역을 좁히면, 전체 에너지는 유한하게 유지될 수 있었습니다.

하지만 그런 속도장을 그리는 것만으로는 나비에 스토크스의 해가 되지 않았습니다.

실제 유체는 이류와 압력, 점성, 그리고 외력의 조건을 함께 만족해야 했기 때문입니다.

즉 수학적으로 원하는 모양을 만드는 것과, 실제 운동 법칙이 그 모양을 허용하는 것은 서로 다른 문제였습니다.

이번에는 이 구별을 신경망에 적용해 보겠습니다.

- TTS: 사용자 측정 29초
- 화면: 29초. 원래 화면 기준은 34초.
## 화면 구성과 시간대별 애니메이션
集中 속도장 → PDE와 초기/외력 조건 검증 → 존재와 도달 질문
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
4막에서 남겨 두었던 질문, 속도장 조건, 파라미터 공간, 손실 지형, 초기점과 학습 경로, 훈련점과 새로운 입력, 해 집합, 암묵적 편향, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
신경망 안에 좋은 답이 존재한다면?
## 수학 조건·과장 방지
에너지 집중은 이전 설명용 모형. 그 모형이 NS 해라는 주장이나 폭주해 검증을 새로 하지 않는다. PDE/비압축성/초기·경계/외력 조건 검증과 학습 동역학은 다른 문제.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- Gunasekar et al., Characterizing Implicit Bias in Terms of Optimization Geometry (2018): https://proceedings.mlr.press/v80/gunasekar18a.html
- Min et al., Initialization and Implicit Bias of Overparametrized Linear Networks (2021): https://proceedings.mlr.press/v139/min21c.html
- Stanford CS231n, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf

