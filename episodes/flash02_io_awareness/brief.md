# FlashAttention 시리즈 2편 제작 기준

- 핵심은 `같은 Attention · 다른 memory access`다. Attention의 수학식이 아니라 실행 중 데이터 이동을 비교한다.
- HBM은 `크지만 느리다`로 단순화하기보다, 큰 중간값의 반복적인 read/write에 비용이 든다고 표현한다.
- on-chip memory는 논문의 SRAM 관점을 시각화한 표현이다. 실제 GPU의 세부 메모리 종류를 이 편에서 확장하지 않는다.
- 표준 경로는 materialized `S`, `P`가 kernel 경계에서 HBM에 쓰이고 다음 계산을 위해 다시 읽히는 흐름이다.
- FlashAttention 경로는 Q/K/V block을 on-chip으로 가져와 local score와 compact state를 갱신하고, 전체 `S`, `P`를 HBM에 materialize하지 않는다는 수준까지만 말한다.
- 2편에서는 online softmax의 running max, running sum, rescaling 공식을 설명하지 않는다.
- `state update`는 정확한 Attention을 유지하는 계산이 존재함을 예고할 뿐, tile별 softmax를 독립적으로 계산한다는 뜻이 아니다.
- 마지막 질문은 `Softmax 분모에는 전체 score가 필요해 보이는데 어떻게 tile 순회가 가능한가?`이며 3편으로 이어진다.

