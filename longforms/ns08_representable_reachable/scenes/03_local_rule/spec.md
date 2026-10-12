# Scene 03 — 학습은 모든 답을 비교하지 않는다
## 목적과 핵심 주장
학습은 모든 답을 비교하지 않는다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
신경망 안에 좋은 답이 존재한다면?
## TTS 원문과 확정 길이
신경망의 학습은 가능한 모든 파라미터를 하나씩 비교하는 방식으로 이루어지지 않습니다.

일반적인 그래디언트 디센트는 현재 위치에서 손실이 가장 빠르게 증가하는 방향을 계산합니다.

그리고 그 반대 방향으로 조금씩 이동합니다.

다음 위치에서도 같은 계산을 반복합니다.

즉 학습은 최종적으로 어디에 좋은 해가 존재하는지 미리 알고 움직이지 않습니다.

매 순간 현재 위치에서 얻은 정보에 따라 다음 위치를 결정하는 것입니다.

- TTS: 사용자 측정 26초
- 화면: 26초. 원래 화면 기준은 34초.
## 화면 구성과 시간대별 애니메이션
정확한 비볼록 toy loss의 −gradient 화살표 → GD 경로
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
학습은 모든 답을 비교하지 않는다, 속도장 조건, 파라미터 공간, 손실 지형, 초기점과 학습 경로, 훈련점과 새로운 입력, 해 집합, 암묵적 편향, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
같은 모델에서도 출발점이 달라지면
## 수학 조건·과장 방지
L(x,y)=.25(x²−1)²+.12x+.5y²−L_min; gradient=(x³−x+.12,y). 유클리드 파라미터 거리에서 gradient는 최급 증가 방향. GD η=.12, 실제 수치 반복. 벡터장 방향은 gradient flow와 공유하지만 이산 GD 경로를 표시.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- Gunasekar et al., Characterizing Implicit Bias in Terms of Optimization Geometry (2018): https://proceedings.mlr.press/v80/gunasekar18a.html
- Min et al., Initialization and Implicit Bias of Overparametrized Linear Networks (2021): https://proceedings.mlr.press/v139/min21c.html
- Stanford CS231n, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf

