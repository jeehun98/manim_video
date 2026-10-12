# Scene 01 — 처음의 두 메커니즘으로 돌아가다
## 목적과 핵심 주장
처음의 두 메커니즘으로 돌아가다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
8막 마지막의 증폭과 안정화 질문
## TTS 원문과 확정 길이
처음에 우리는 나비에 스토크스 방정식 안에서 서로 다른 두 경향을 발견했습니다.

유체의 흐름은 소용돌이를 늘어나게 만들고, 특정 조건에서 회전의 강도를 증폭시킬 수 있었습니다.

반대편에서는 점성이 급격한 속도 차이와 보티시티의 변화를 확산시켰습니다.

하나는 국소적인 회전을 강화할 수 있고, 다른 하나는 그것을 완화하는 효과를 가집니다.

그렇다면 점성이 존재한다는 사실만으로, 소용돌이의 끝없는 증폭을 막을 수 있을까요?

- TTS: 사용자 측정 27초
- 화면: 27초. 원래 화면 기준은 30초.
## 화면 구성과 시간대별 애니메이션
늘어나는 관과 확산 단면 → 같은 실제 흐름에서 두 효과
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
처음의 두 메커니즘으로 돌아가다, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
점성이 존재해도 왜 문제가 어려웠을까?
## 수학 조건·과장 방지
늘어남은 점성 제외한 부피 보존 변형 예시. 확산은 2D Gaussian 보티시티의 단면 ω(x,0,t)=σ0²/σ² exp(−x²/2σ²), σ²=σ0²+2νt. 분리 비교는 전체 NS 해가 아니며 점성이 모든 위치의 ω를 매순간 감소시키는 것은 아님.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html
- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450
- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385

