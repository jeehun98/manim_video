# FlashAttention 시리즈 1편 제작 기준

- 논문: Tri Dao et al., *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*, arXiv:2205.14135 (2022).
- 1편은 해법보다 문제를 세운다. SRAM, tiling, online softmax의 작동 원리는 설명하지 않는다.
- `S = QKᵀ`, `P = softmax(S)`, `O = PV`에서 표준적인 materialized 구현이 연산 경계마다 `S`, `P`를 HBM에 쓰고 다시 읽는 데이터 흐름을 보여준다.
- `S`와 `P`는 각각 `N × N`이지만, 둘이 반드시 동시에 HBM에 상주한다고 말하지 않는다.
- FlashAttention은 근사 Attention이 아니라 정확한 Attention이며, 1편 결말의 `same output O`가 이 점을 예고한다.
- 마지막의 작은 tile은 2편의 시각적 단서일 뿐, 1편에서는 원리를 설명하지 않는다.
- 색 의미: `Q` 파랑, `K` 분홍, `V` 초록, `S` 금색, `P` 보라, `O` 코랄, HBM 짙은 파랑.
- 핵심 관점 전환은 `Attention의 수학 → Attention 실행 중 생기는 데이터`이다.

