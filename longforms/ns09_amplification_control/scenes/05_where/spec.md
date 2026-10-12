# Scene 05 — 증폭을 막는 것과 결과를 제한하는 것은 다르다
## 목적과 핵심 주장
증폭을 막는 것과 결과를 제한하는 것은 다르다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
큰 그래디언트를 잘라내면 해결될까?
## TTS 원문과 확정 길이
두 가지 상황을 비교해 보겠습니다.

첫 번째에서는 작은 변화가 여러 층을 통과하면서 계속 증폭됩니다.

하지만 마지막에 그래디언트의 크기를 잘라냅니다.

두 번째에서는 애초에 각 변환이 변화를 과도하게 증폭하지 않도록 설계합니다.

두 경우 모두 최종적으로 큰 업데이트를 피할 수 있을지 모릅니다.

하지만 작동하는 위치는 다릅니다.

하나는 이미 커진 결과를 제한하고, 다른 하나는 내부의 변화가 전달되는 구조를 조절하려는 것입니다.

- TTS: 사용자 측정 27초
- 화면: 27초. 원래 화면 기준은 36초.
## 화면 구성과 시간대별 애니메이션
결과 제한 1/2/4/8/3 vs 구조 제어1/1.2/1.1/1.3/1.2
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
증폭을 막는 것과 결과를 제한하는 것은 다르다, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
Normalization과 Residual Connection은 무엇을 바꿀까?
## 수학 조건·과장 방지
A는 같은 방향 전달 모형에서1→2→4→8 후 clipping3. B는 [1,1.2,1.1,1.3,1.2], 단계 gain=다음/이전인 실제 선형 예시. 작은 개별 gain도 누적증폭될 수 있으며 이 모형을 전체 학습 안정성 보장으로 주장하지 않는다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html
- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450
- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385

