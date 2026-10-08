# Scene 06 — 학습 규칙은 어떤 해를 선택하는가?
## 목적과 핵심 주장
학습 규칙은 어떤 해를 선택하는가?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
더 흥미로운 경우: 둘 다 좋은 해에 도착했다면?
## TTS 원문과 확정 길이
이제 질문이 다시 바뀝니다.

신경망이 어떤 함수를 표현할 수 있는가가 아니라, 학습 과정이 가능한 여러 해 중 어떤 해를 선택하는가입니다.

이 선택에는 초기값과 학습 알고리즘, 파라미터화 방식 등이 영향을 줄 수 있습니다.

특히 손실이 낮은 해가 여러 개 존재할 때, 학습 알고리즘이 특정 성질의 해를 선호하는 현상을 암묵적 편향, 임플리시트 바이어스라고 합니다.

명시적으로 그런 해를 선택하라고 지시하지 않아도, 학습 동역학 자체가 선택에 영향을 줄 수 있는 것입니다.

- TTS: 사용자 측정 28초
- 화면: 28초. 원래 화면 기준은 34초.
## 화면 구성과 시간대별 애니메이션
좋은 해 직선 → 초기값 변화 → GD/방향별 보정 선택 → 암묵적 편향
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
학습 규칙은 어떤 해를 선택하는가?, 속도장 조건, 파라미터 공간, 손실 지형, 초기점과 학습 경로, 훈련점과 새로운 입력, 해 집합, 암묵적 편향, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
이제 두 시스템을 다시 비교한다
## 수학 조건·과장 방지
동일 loss의 최소 집합 a+b=1. 유클리드 GD는 초기 nullspace성분 보존. zero init GD→(.5,.5) 최소 유클리드 노름. zero init 방향별 고정 보정 P=diag(4,1), η=.1의 θ←θ−ηPgradient→(.8,.2); 명시적 정규화 추가 아님. 특정 모델 결과이며 일반 신경망 보편 보장 아님.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- Gunasekar et al., Characterizing Implicit Bias in Terms of Optimization Geometry (2018): https://proceedings.mlr.press/v80/gunasekar18a.html
- Min et al., Initialization and Implicit Bias of Overparametrized Linear Networks (2021): https://proceedings.mlr.press/v139/min21c.html
- Stanford CS231n, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf

