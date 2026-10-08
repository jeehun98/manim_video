# Scene 07 — 두 시스템의 안정화는 정말 같은 것일까?
## 목적과 핵심 주장
두 시스템의 안정화는 정말 같은 것일까?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
Normalization과 Residual Connection은 무엇을 바꿀까?
## TTS 원문과 확정 길이
이제 나비에 스토크스와 신경망을 다시 비교해 보겠습니다.

유체에서 점성은 공간적인 차이를 확산시키는 물리적 메커니즘입니다.

신경망에서 그래디언트 클리핑은 큰 업데이트를 제한하는 최적화 기법입니다.

노멀라이제이션은 활성값의 표현을 변화시키고, 레지듀얼 커넥션은 정보가 전달되는 경로를 바꿉니다.

이들은 서로 같은 수학적 연산이 아닙니다.

그럼에도 공통된 질문을 던질 수 있습니다.

어떤 과정에서 변화가 증폭될 수 있을 때, 그것을 제어하는 다른 메커니즘은 실제로 무엇을 제한하고 있을까요?

그리고 그 제한은 시스템 전체의 안정성을 보장하기에 충분할까요?

- TTS: 사용자 측정 35초
- 화면: 35초. 원래 화면 기준은 42초.
## 화면 구성과 시간대별 애니메이션
유체/역전파/순전파 비교 · 개입 대상과 위치 → 공통 질문
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
두 시스템의 안정화는 정말 같은 것일까?, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
정말 안정적인 시스템이라면 변화는 항상 작아질까?
## 수학 조건·과장 방지
점성은 물리적 공간 확산, clipping은 gradient 결과 제한, norm은 표현변환, residual은 전달경로. 동일 연산이 아님. 어떤 안정성 정의/조건인지 밝히지 않은 장치의 존재만으로 전체 보장을 내리지 않는다.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html
- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450
- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385

