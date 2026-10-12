# Scene 04 — 큰 그래디언트를 잘라내면 해결될까?
## 목적과 핵심 주장
큰 그래디언트를 잘라내면 해결될까?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
신경망에서도 변화는 증폭될 수 있다
## TTS 원문과 확정 길이
그렇다면 그래디언트가 너무 커지는 것을 막으려면 어떻게 해야 할까요?

한 가지 방법은 그래디언트의 크기에 상한을 두는 것입니다.

그래디언트의 길이가 정해진 기준을 넘으면, 방향은 유지한 채 길이만 줄입니다.

이를 그래디언트 클리핑이라고 합니다.

단순한 그래디언트 디센트에서는, 이 방법으로 한 번의 업데이트가 지나치게 커지는 것을 제한할 수 있습니다.

하지만 여기서 중요한 차이가 있습니다.

그래디언트의 크기를 제한했다고 해서, 그래디언트가 커지는 내부 원인 자체가 사라진 것은 아닙니다.

- TTS: 사용자 측정 28초
- 화면: 28초. 원래 화면 기준은 38초.
## 화면 구성과 시간대별 애니메이션
global gradient norm 임계3 · 길이10→3, 방향 유지 · SGD 보폭
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
큰 그래디언트를 잘라내면 해결될까?, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
증폭을 막는 것과 결과를 제한하는 것은 다르다
## 수학 조건·과장 방지
global L2 norm clipping c=3, g=(6,8), clipped=(1.8,2.4). g=0은 그대로0. plain SGD Δθ=−η clipped g, η=.1이므로 ||Δθ||≤.3. momentum/Adam/weight decay 적용 후 실제 업데이트의 같은 상한 보장은 아님. 내부 계산의 overflow 방지나 모든 Jacobian의 제약도 아님.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html
- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450
- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385

