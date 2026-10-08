# Scene 07 — 안정성은 하나의 성질이 아니다
## 목적과 핵심 주장
안정성은 하나의 성질이 아니다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
다섯 번째 구별: 장기적 안정성과 순간적인 증폭
## TTS 원문과 확정 길이
이제 처음의 질문으로 돌아가 보겠습니다.

시스템이 안정적이라는 것은 정확히 무엇을 의미할까요?

전체 에너지가 제한되어 있다는 뜻일까요?

가장 극단적인 부분의 크기가 제한되어 있다는 뜻일까요?

어떤 방향에서도 변화가 크게 증폭되지 않는다는 뜻일까요?

아니면 충분히 긴 시간이 지난 뒤 모든 변화가 사라진다는 뜻일까요?

이 질문들은 서로 다른 수학적 조건을 나타냅니다.

그리고 한 조건이 성립한다고 해서 다른 조건까지 자동으로 성립하는 것은 아닙니다.

따라서 복잡한 시스템의 안정성을 이해하려면, 먼저 무엇을 측정하고 무엇을 보장하려는지 명확하게 구분해야 합니다.

- TTS: 사용자 측정 34초
- 화면: 34초. 원래 화면 기준은 42초.
## 화면 구성과 시간대별 애니메이션
STABILITY를 다섯 가지 질문으로 분해
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
안정성은 하나의 성질이 아니다, 속도장, 전체와 국소, 변형률과 Jacobian, 작은 격자와 곡률, 실현 경로, 과도 증폭, 다섯 질문과 분야 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
서로 다른 분야에서 같은 질문이 반복된다
## 수학 조건·과장 방지
서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- Trefethen et al. (1993), Hydrodynamic Stability Without Eigenvalues: https://people.maths.ox.ac.uk/trefethen/ttrd.pdf
- Dettmers et al. (2022), LLM.int8(): https://arxiv.org/abs/2208.07339
- MIT, Forward and Backward Euler Methods: https://web.mit.edu/10.001/Web/Course_Notes/Differential_Equations_Notes/node3.html
- Stanford, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf
- Gunasekar et al. (2018), Optimization Geometry and Implicit Bias: https://proceedings.mlr.press/v80/gunasekar18a.html
- Kerg et al. (2019), Non-normal Recurrent Neural Network: https://arxiv.org/abs/1905.12080
- 수학 조건의 상세 설명: 기존 1~10막 spec.md 및 sources.md. 이번 막은 이미 소개한 질문을 회수하며 새로운 특이점이나 학습 성능 주장을 추가하지 않는다.

