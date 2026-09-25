# FlashAttention 시리즈 5편 제작 기준

- 새로운 알고리즘 원리를 추가하지 않고 1~4편의 `materialization`, `HBM IO`, `tiling`, `m,ℓ,O state`, exact output을 한 화면에 합친다.
- Standard와 Flash 경로는 동일한 Q/K/V와 동일한 Attention 수학에서 시작한다.
- 왼쪽은 `QKᵀ→S→softmax→P→PV`의 materialized 실행 구조와 S/P의 HBM write/read를 보여준다.
- 오른쪽은 Q/K/V tile을 on-chip working set으로 가져와 local score를 만들고 `m,ℓ,O`를 갱신한 뒤 local intermediate를 버린다.
- FlashAttention을 근사 Attention, 계산 생략, FLOP 감소 알고리즘으로 표현하지 않는다. 핵심은 HBM traffic을 줄이는 IO-aware exact algorithm이다.
- `O_standard=O_flash`는 4편의 scalar 예시 `5.741`을 재사용해 시리즈 내부의 연속성을 유지한다.
- 실제 구현과 backward pass에서 연산량의 세부 차이는 있을 수 있으므로 `identical FLOP count`가 아니라 `same Attention math`, `FLOPs보다 Memory IO가 핵심`으로 표현한다.
- 마지막 문장은 `같은 답을 계산해도, 계산하는 방법은 같지 않습니다.`로 고정한다.

