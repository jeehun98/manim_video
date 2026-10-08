# Scene 01 — 처음의 물로 돌아가다
## 목적과 핵심 주장
처음의 물로 돌아가다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
10막의 장기 안정성과 일시적 증폭
## TTS 원문과 확정 길이
처음에 우리는 물의 움직임을 수많은 속도 화살표로 표현했습니다.

그리고 이 화살표들이 시간에 따라 어떻게 변하는지 살펴봤습니다.

유체의 흐름은 새로운 구조를 만들고, 점성은 급격한 속도 차이를 완화했습니다.

삼차원에서는 소용돌이가 늘어나면서 회전의 강도가 증폭될 수도 있었습니다.

이렇게 시작한 질문은 결국, 매끄러운 유체가 언제까지 매끄럽게 유지될 수 있는가로 이어졌습니다.

그런데 이 문제를 따라가면서 우리는 유체역학을 넘어서는 몇 가지 수학적 구조를 발견했습니다.

- TTS: 사용자 측정 29초
- 화면: 29초. 원래 화면 기준은 34초.
## 화면 구성과 시간대별 애니메이션
속도장 → 점성 완화 → 보티시티 관 늘어남 → 전체 시야
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
처음의 물로 돌아가다, 속도장, 전체와 국소, 변형률과 Jacobian, 작은 격자와 곡률, 실현 경로, 과도 증폭, 다섯 질문과 분야 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
첫 번째 구별: 전체와 국소
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

