# GPU 연산과 최적화 06 — 여러 값이 필요한 연산도 합칠 수 있을까?

- 핵심 메시지: Reduction은 여러 원소를 필요로 하지만 모든 중간 원소를 하나의 Tensor로 Global Memory에 materialize해야 하는 것은 아니다. 각 원소가 만들어지는 즉시 필요한 정보만 partial state에 반영하고, 병렬로 만든 partial result들을 다시 merge할 수 있다.
- 전편과의 대비: Epilogue Fusion은 `하나의 live value → 다음 원소별 연산`으로 전달한다. Reduction Fusion은 `여러 live values → 작은 partial states → merged result`로 축약하면서 전달한다.
- 중심 인과: `ReLU 결과가 생성됨 → 중간 배열이 아니라 합이 필요함 → 각 결과를 partial sum에 반영 → 병렬 partial sums를 merge → 전체 intermediate Tensor materialization 회피`.
- 길이: 90초, 1080×1920, 30fps 세로형 무음. 80초 TTS 실측 길이와 구간별 발화량을 기준으로 각 장면을 6–10초로 배분하고 약 10초의 화면 전환·읽기 여유를 둔다. 각 화면에 2줄 설명 자막을 포함하며 SRT와 TTS도 별도 제공한다.
- 장면: 전편의 원소별 chain 회수 → `Σ ReLU(xᵢ)`의 다중 입력 dependency → 분리 Kernel과 중간 Tensor → “배열인가 합인가?” → 결과가 생길 때 partial state 갱신 → Thread 그룹별 partial sum → merge tree → intermediate Tensor 제거 → Epilogue/Reduction Fusion 비교 → SUM/MAX/MIN과 Softmax 질문.
- GPU 정확성: 실제 reduction은 Warp shuffle, Shared Memory, Block 간 단계, cooperative groups, atomic, 다중 Kernel 등 다양한 방식으로 구현될 수 있다. 화면은 “병렬 그룹이 partial result를 만들고 다시 merge한다”는 공통 구조만 표현한다.
- 수학 조건: 합은 부분 결과를 다시 합쳐 전체 결과를 만들 수 있다. MAX/MIN도 비슷한 merge state를 가진다. 모든 Reduction 또는 후속 연산이 같은 방식으로 쉽게 fusion된다고 단정하지 않는다.
- 부동소수점 주의: 부동소수점 덧셈은 실수 덧셈처럼 결합법칙이 엄밀히 성립하지 않으므로 reduction tree와 순서가 달라지면 반올림 결과가 달라질 수 있다. 마지막 화면에 작은 주의 자막으로 표시한다.
- Materialization 표현: 분리 실행은 ReLU 결과 Tensor를 STORE하고 Reduction Kernel이 LOAD하는 개념도다. 실제 compiler/framework가 이미 fusion할 수 있고 캐시 및 구현에 따라 물리적 트래픽은 달라질 수 있으므로 절대적인 속도 향상을 주장하지 않는다.
- 화면·자막·대본에는 숫자와 영어 원표기를, 한국어 발음 표기는 `tts_script.txt`에만 둔다.
