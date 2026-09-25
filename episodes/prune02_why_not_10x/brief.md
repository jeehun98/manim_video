# Pruning & Sparsity 02 제작 기준

- 이 편의 유일한 학습 목표는 `0의 개수만으로 실제 속도가 결정되지 않는다`는 점이다.
- Dense GEMM을 그대로 쓰면 0도 계산한다. Sparse kernel로 곱셈을 건너뛸 수 있지만 index metadata, gather 성격의 memory access, thread별 작업량 불균형이 이득을 잠식할 수 있다.
- `Values + Positions` 장면은 CSR·CSC 등 특정 포맷을 가르치는 장면이 아니라 sparse representation의 공통 직관을 단순화한 것이다.
- 불규칙한 sparsity가 항상 느리다고 단정하지 않는다. 효율적인 sparse format, kernel, 충분한 sparsity와 하드웨어 지원에 따라 실제 이득은 달라진다.
- 마지막에는 같은 50% sparsity를 random 배치와 row-wise 배치로 비교해 Structured Pruning 편으로 연결한다.
- 영상은 대본 길이에 맞춘 82초, 1080×1920, 30fps 무음 마스터다.
