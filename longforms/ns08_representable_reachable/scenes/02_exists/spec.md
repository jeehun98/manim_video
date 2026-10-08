# Scene 02 — 신경망 안에 좋은 답이 존재한다면?
## 목적과 핵심 주장
신경망 안에 좋은 답이 존재한다면?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
4막에서 남겨 두었던 질문
## TTS 원문과 확정 길이
하나의 신경망을 생각해 보겠습니다.

이 신경망의 파라미터를 바꾸면 서로 다른 함수를 만들 수 있습니다.

그중에는 주어진 데이터를 매우 정확하게 설명하는 파라미터도 존재할 수 있습니다.

파라미터 공간에서 이 해를 하나의 점으로 나타내 보겠습니다.

이 점에서는 손실이 매우 낮습니다.

즉 모델의 표현 능력만 보면 좋은 답이 존재하는 것입니다.

그렇다면 학습도 반드시 이 점에 도착할까요?

- TTS: 사용자 측정 25초
- 화면: 25초. 원래 화면 기준은 36초.
## 화면 구성과 시간대별 애니메이션
파라미터 공간의 여러 점 → 낮은 손실 후보 → 떨어진 초기점
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
신경망 안에 좋은 답이 존재한다면?, 속도장 조건, 파라미터 공간, 손실 지형, 초기점과 학습 경로, 훈련점과 새로운 입력, 해 집합, 암묵적 편향, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
학습은 모든 답을 비교하지 않는다
## 수학 조건·과장 방지
좋은 파라미터의 존재와 특정 초기화·알고리즘의 수렴 보장은 구별. 2D 그림은 설명용 모델.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- Gunasekar et al., Characterizing Implicit Bias in Terms of Optimization Geometry (2018): https://proceedings.mlr.press/v80/gunasekar18a.html
- Min et al., Initialization and Implicit Bias of Overparametrized Linear Networks (2021): https://proceedings.mlr.press/v139/min21c.html
- Stanford CS231n, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf

