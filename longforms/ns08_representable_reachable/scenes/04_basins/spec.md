# Scene 04 — 같은 모델에서도 출발점이 달라지면
## 목적과 핵심 주장
같은 모델에서도 출발점이 달라지면를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
학습은 모든 답을 비교하지 않는다
## TTS 원문과 확정 길이
이번에는 같은 손실 지형 위에서 서로 다른 초기점들을 선택해 보겠습니다.

모든 점에 동일한 학습 규칙을 적용합니다.

하지만 처음 위치가 다르면 각 지점에서 계산되는 그래디언트도 달라집니다.

그래서 서로 다른 경로를 따라 이동하고, 다른 해에 도착할 수 있습니다.

어떤 경로는 낮은 손실의 영역에 도착하지만, 다른 경로는 상대적으로 높은 손실의 국소 최솟값에 머무를 수도 있습니다.

좋은 해가 존재한다는 사실과 실제 학습이 그 해에 도달한다는 사실은 다릅니다.

- TTS: 사용자 측정 29초
- 화면: 29초. 원래 화면 기준은 36초.
## 화면 구성과 시간대별 애니메이션
같은 toy loss와 규칙, 서로 다른 두 초기값 → 두 국소 최소
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
같은 모델에서도 출발점이 달라지면, 속도장 조건, 파라미터 공간, 손실 지형, 초기점과 학습 경로, 훈련점과 새로운 입력, 해 집합, 암묵적 편향, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
더 흥미로운 경우: 둘 다 좋은 해에 도착했다면?
## 수학 조건·과장 방지
같은 L, η=.12, 시작(-1.7,.9)/(1.7,.9), 50스텝. 국소 최소는 cubic x³−x+.12=0의 바깥 두근. 실제 대형신경망 실패 일반 설명으로 단정하지 않는다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- Gunasekar et al., Characterizing Implicit Bias in Terms of Optimization Geometry (2018): https://proceedings.mlr.press/v80/gunasekar18a.html
- Min et al., Initialization and Implicit Bias of Overparametrized Linear Networks (2021): https://proceedings.mlr.press/v139/min21c.html
- Stanford CS231n, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf

