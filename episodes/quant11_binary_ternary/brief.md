# Quantization 시리즈 11편 제작 기준 — Part I Finale

- 이 편의 핵심 질문은 `1비트까지 줄이면 무엇을 잃고, 대신 어떤 구조가 남는가?`다.
- Binary/Ternary Network를 단순한 activation 압축으로 설명하지 않는다. Activation-only는 전달 신호를 단순화하지만, weight까지 binary일 때 dot product의 개별 곱셈을 부호 비교로 바꿀 수 있음을 구분한다.
- 일반 weight가 담는 정보를 `magnitude + direction`으로 보고, binary weight는 magnitude를 크게 버린 채 direction을, ternary weight는 direction과 selection을 남긴다는 의미를 중심에 둔다.
- 둘 다 binary인 예시에서 같은 부호는 `+1`, 다른 부호는 `−1`이며, 0/1 encoding에서는 XNOR가 같은 위치를 표시한다.
- 예시 `w=[+1,−1,+1,+1]`, `x=[+1,+1,+1,−1]`는 matches 2, mismatches 2이므로 dot product는 `2−2=0`이다.
- 일반적으로 길이 n의 bipolar binary vector에서 `dot=2·popcount(XNOR)−n`이지만, 이 수식은 화면 복잡도를 줄이기 위해 내레이션에서 생략한다.
- Ternary weight는 `+1: add`, `−1: subtract`, `0: ignore`의 세 명령으로 표현한다. 0 weight는 해당 연결의 합 기여를 제거하므로 weight sparsity를 만들 수 있다.
- XNOR/count로의 전환은 weight와 activation이 모두 binary이고 적절한 bit encoding과 kernel이 있을 때의 핵심 아이디어다. 실제 네트워크에는 scaling, normalization, accumulation 등이 남을 수 있다.
- Bit 연산과 sparsity가 실제 속도 향상으로 이어지는 정도는 하드웨어와 kernel 지원에 따라 달라진다는 caveat를 마지막 화면에 남긴다.
- 학습 방법, sign 미분, STE, 상세 packing/popcount 구현은 제외한다.
- 다음 편 예고 없이 `정밀한 magnitude를 잃고 direction/selection과 새로운 dot product 구조를 얻는다`는 문장으로 Quantization 1부를 마무리한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
