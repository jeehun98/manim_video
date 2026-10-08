# Scene 03 — 신경망에서도 변화는 증폭될 수 있다
## 목적과 핵심 주장
신경망에서도 변화는 증폭될 수 있다를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
점성이 존재해도 왜 문제가 어려웠을까?
## TTS 원문과 확정 길이
이제 신경망으로 돌아가 보겠습니다.

앞에서는 작은 입력 변화가 야코비안을 통과하면서 방향에 따라 다르게 증폭되는 모습을 살펴봤습니다.

그런데 신경망은 여러 층을 연속해서 통과합니다.

한 층에서 변형된 변화는 다음 층으로 전달되고, 그다음 층의 야코비안에 다시 영향을 받습니다.

역전파에서도 비슷한 문제가 나타납니다.

여러 층의 야코비안이 반복해서 작용하면서, 특정 조건에서는 그래디언트의 크기가 급격하게 증가할 수 있습니다.

이를 익스플로딩 그래디언트, 그래디언트 폭주라고 합니다.

- TTS: 사용자 측정 30초
- 화면: 30초. 원래 화면 기준은 40초.
## 화면 구성과 시간대별 애니메이션
3층 방향 증폭 → 전달 방향 반전 → transpose 역전파
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
신경망에서도 변화는 증폭될 수 있다, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
큰 그래디언트를 잘라내면 해결될까?
## 수학 조건·과장 방지
J_l=∂h(l+1)/∂h(l), δh(l+1)≈J_lδh(l), g_l=J_lᵀg(l+1). J=diag(2,.5) 3층의 정렬 e1 예시. 전방 활성값 자체와 작은 입력 변화, hidden gradient와 전체 파라미터 gradient는 구별. clipping 장면은 모은 파라미터 gradient를 사용.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html
- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450
- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385

