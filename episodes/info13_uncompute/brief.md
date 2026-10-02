# 정보이론 13 — 삭제하지 말고 되감아라 — Reversible Computing

학습 목표: 입력을 보존하고 결과를 별도 레지스터에 저장한 뒤 역연산으로 작업 공간을 정리하는 compute–copy–uncompute를 이해한다. 핵심 이미지는 삭제 아이콘이 아니라, 작업 칸은 원래 0으로 돌아가고 결과 칸의 1은 남는 장면이다.

## 제작 기준

- 세로 1080×1920, 30fps, 기존 색상과 Malgun Gothic 유지. 무음 영상과 별도 TTS/SRT.
- 14구간, 약 74초. 발화 길이 기반 누적 시각에 맞추며 실음성 합성 뒤 조정 가능.
- AND에서 입력의 구분 손실 → 입력 보존 → 결과까지 되돌아가는 문제 → 중간값 누적 → 결과 보존 → 작업 계산만 되감기 → Toffoli → 같은 양자 회로 → 중첩에서 보조 큐빗 정리 → 측정·리셋과 실제 소비 구분.
- 입력 a,b는 청록, 작업 t는 분홍, 결과 r은 초록으로 고정한다. 1,1,0,0 → 1,1,1,0 → 1,1,1,1 → 1,1,0,1을 직접 애니메이션한다.
- 중간값을 물리적으로 삭제하거나 모든 레지스터를 강제로 0으로 바꾸는 장면을 쓰지 않는다. 결과 보존은 알려진 0 결과 칸에 XOR로 기록하는 가역 연산이다.

## 수학적 조건

모든 상태에 정의된 가역 게이트를 쓴다. Toffoli는 (a,b,t,r)→(a,b,t XOR (a AND b),r), CNOT는 r→r XOR t이다. 각 게이트는 자기 역이다. t=r=0인 입력에서는 최종 (a,b,0,a AND b). 입력이 남으므로 값 1인 작업 칸을 입력의 함수로 정확히 되돌릴 수 있다. 임의의 독립적인 미지 비트를 공짜로 초기화하는 방법이 아니다. (x,0)→(x,f(x))만을 가역성 증명의 전부로 삼지 않고 XOR 확장을 명시한다.

양자 파트는 동일한 Toffoli–CNOT–Toffoli 회로를 사용한다. 입력 (|00〉+|11〉)/√2, t=r=|0〉이면, 계산 및 결과 저장 뒤 (|0000〉+|1111〉)/√2, uncompute 뒤 (|0000〉+|1101〉)/√2가 된다. 순서는 a,b,t,r. t는 전체 상태에서 |0〉로 분리되고 a,b,r에는 상관관계가 남는다. 두 행은 혼합된 별개 시행이 아니라 하나의 중첩 상태의 두 항이다. CNOT의 기저값 저장은 임의의 미지 양자상태를 복제하는 것이 아니다.

역회로는 게이트 순서를 뒤집고 각 역게이트를 적용한다. 이상적 유니터리 게이트에 한정하며, 일반적인 측정 결과·리셋·잡음 과정의 역복원을 보장하지 않는다. 특정 알려진 상태나 특별한 측정 프로토콜까지 전부 불가능하다는 뜻이 아니다. 가역 계산은 논리적 정보 삭제를 피하는 구성이지, 실제 장치의 총 에너지 소비가 0이라는 주장이 아니다. 작업 공간, 결과 저장 공간, 추가 역연산의 비용을 표시한다. AND 한 번의 열이 무조건 kBT ln2라는 잘못된 수치 주장을 하지 않는다.

## 근거

- Bennett (1973), Logical Reversibility of Computation: https://www.cs.princeton.edu/courses/archive/fall06/cos576/papers/bennett73.html
- IBM Quantum Learning, Classical computations on quantum computers: https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-algorithmic-foundations/simulating-classical-computations
- IBM Quantum Learning, Limitations on quantum information: https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/limitations-on-quantum-information

## 검증

전체 16개 고전 상태에서 게이트 일대일 대응과 역복원을 확인한다. 양자 상태벡터와 보조 큐빗의 분리, U†U=I를 확인한다. 360×640 미리보기의 각 구간을 검토하고 1080×1920 최종본을 렌더한 뒤 전체 디코딩으로 검증한다. 결과는 render_report.json에 기록한다.
