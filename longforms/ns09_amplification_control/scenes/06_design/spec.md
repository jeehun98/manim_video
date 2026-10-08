# Scene 06 — Normalization과 Residual Connection은 무엇을 바꿀까?
## 목적과 핵심 주장
Normalization과 Residual Connection은 무엇을 바꿀까?를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
증폭을 막는 것과 결과를 제한하는 것은 다르다
## TTS 원문과 확정 길이
신경망에는 그래디언트를 잘라내는 방법 외에도 여러 설계가 존재합니다.

노멀라이제이션은 활성값의 분포나 크기를 조절하는 데 사용됩니다.

레지듀얼 커넥션은 입력을 변환 결과에 더하는 경로를 만듭니다.

이런 구조는 깊은 신경망의 학습을 돕지만, 모든 방향의 증폭을 무조건 억제하는 장치는 아닙니다.

예를 들어 레지듀얼 블록의 변화율은 항등행렬과 변환의 야코비안의 합으로 나타납니다.

따라서 잔차 경로가 존재한다는 사실만으로 전체 야코비안의 크기가 반드시 작아지는 것은 아닙니다.

- TTS: 사용자 측정 32초
- 화면: 32초. 원래 화면 기준은 42초.
## 화면 구성과 시간대별 애니메이션
표준화의 값 분포 → skip와 F 경로 → Iδ와 JFδ 벡터 합
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
Normalization과 Residual Connection은 무엇을 바꿀까?, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
두 시스템의 안정화는 정말 같은 것일까?
## 수학 조건·과장 방지
표준화 예시 [10,12,14]→[-√1.5,0,√1.5], mean/std division, ε=0, 비제로분산, affine γ=1 β=0. 실제 norm 종류와 ε/learned scale은 별도. residual y=x+F(x), J=I+JF. JF=.8I→gain1.8, JF=−.8I→gain.2; 잔차 합의 방향에 따라다름. 모든 방향 축소 보장 없음.
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html
- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html
- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450
- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385

