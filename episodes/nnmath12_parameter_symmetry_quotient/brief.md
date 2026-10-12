# 신경망의 수학 12 — 서로 다른 파라미터가 어떻게 같은 신경망이 될까?

## 학습 목표

- 은닉 뉴런과 그 뉴런의 incoming weight, outgoing weight, bias를 함께 순열하면 네트워크 함수가 보존됨을 확인한다.
- `θ_A≠θ_B`이면서 `f_{θ_A}=f_{θ_B}`일 수 있다는 Parameter Space와 Function Space의 차이를 이해한다.
- 동일 함수가 같은 데이터에서 동일 출력과 동일 예측 기반 loss를 만들고, 대칭적으로 복제된 minimum으로 나타날 수 있음을 연결한다.
- permutation으로 연결된 점들의 equivalence class를 한 점으로 보는 quotient space의 필요성을 현상에서부터 도출한다.

## 중심 흐름

`뉴런과 연결의 permutation → Different Parameters → Same Function → Same Loss → Symmetric Minima → Equivalence → Equivalence Class → Quotient Space`

## 수학적 정확성

- 은닉 뉴런 `h₁,h₂`의 위치만 바꾸는 것이 아니다. 각 뉴런의 모든 incoming weight, outgoing weight, bias를 하나의 묶음으로 함께 교환한다.
- 화면의 `y=v₁h₁+v₂h₂`는 스칼라 출력의 두 은닉 유닛 예시다. 교환 후에는 두 항의 순서만 달라진다.
- `f_{θ_A}=f_{θ_B}`이면 같은 데이터와 같은 target에 prediction-based loss를 적용할 때 `L(θ_A)=L(θ_B)`다.
- 서로 구별되는 `n`개 은닉 뉴런은 최대 `n!`개의 순열 표현을 만든다. 동일한 뉴런이 있으면 서로 다른 parameter vector 수는 더 작을 수 있다.
- 모든 minimum이 대칭 복제본이라는 뜻이 아니다. loss landscape의 일부 서로 먼 minimum이 같은 함수의 symmetry copy일 수 있다는 주장이다.
- 이 영상의 quotient는 `Parameter Space / Permutation Symmetry`다. ReLU network의 scaling symmetry 등 다른 중복 표현까지 모두 제거한다고 주장하지 않는다.
- 슬래시 `/`는 수치 나눗셈이 아니라 equivalence relation 아래 같은 점들을 식별한다는 뜻이다.

## 연출 기준

- `h₁,h₂`는 실제로 자리를 바꾸고 연결선은 updater로 따라간다. 교환 중 입력–출력 그래프는 고정한다.
- parameter/function space 투영을 첫 번째 대표 장면으로 삼는다.
- `same function → same predictions → same loss → symmetric minima`를 독립 장면으로 보여준다.
- `2!,3!,4!`은 숫자만 키우지 않고 같은 함수의 parameter point가 2·6·24개로 복제되는 모습으로 표현한다.
- quotient라는 이름은 equivalence class를 먼저 만든 뒤 제시한다. 타원으로 묶인 점 무리가 한 점으로 수축한다.
- 마지막에는 `Different Parameters → Same Function → Equivalence → Equivalence Class → Quotient Space`를 세로 흐름으로 정리한다.
- 122초, 1080×1920, 30fps, 무음 마스터. TTS 실측 전 타이밍은 대본 분량 기반 임시값이다.
