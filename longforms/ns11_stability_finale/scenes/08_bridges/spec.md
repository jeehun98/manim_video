# Scene 08 — 서로 다른 분야에서 같은 질문이 반복된다
## 목적과 핵심 주장
서로 다른 분야에서 같은 질문이 반복된다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
안정성은 하나의 성질이 아니다
## TTS 원문과 확정 길이
나비에 스토크스는 유체의 움직임을 기술하는 방정식입니다.

신경망은 입력을 변환하고, 데이터를 통해 파라미터를 학습하는 시스템입니다.

둘은 서로 다른 목적과 구조를 가지고 있습니다.

하지만 그 안에서 마주치는 수학적 질문에는 공통점이 있었습니다.

전체를 하나의 값으로 요약할 때 무엇을 놓치는가.

어떤 방향에서 변화가 가장 크게 증폭되는가.

어떤 모드가 전체 계산을 제한하는가.

그리고 현재의 상태와 실제 동역학은 어떤 관계를 갖는가.

서로 다른 현상을 같은 것으로 취급하지 않더라도, 이러한 공통 구조를 통해 새로운 관점을 얻을 수 있습니다.

- TTS: 사용자 측정 34초
- 화면: 34초. 원래 화면 기준은 42초.
## 화면 구성과 시간대별 애니메이션
두 영역에서 다섯 개 질문을 선으로 연결
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
서로 다른 분야에서 같은 질문이 반복된다, 속도장, 전체와 국소, 변형률과 Jacobian, 작은 격자와 곡률, 실현 경로, 과도 증폭, 다섯 질문과 분야 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
마지막으로 남길 질문
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

