# GPU 연산과 최적화 05 — 행렬곱 뒤의 연산은 왜 합칠 수 있을까?

- 핵심 메시지: GEMM을 실행하는 Thread/Warp는 출력의 일부를 accumulator/register 상태로 가지고 있다. Bias와 ReLU처럼 현재 값과 단순히 대응하는 보조 입력만으로 계산 가능한 원소별 연산은, 그 값을 놓지 않고 같은 흐름에서 연속 처리할 수 있다. Global Memory materialization 제거는 이 dependency 특성의 결과다.
- 중심 인과: `출력 일부를 아직 가지고 있음 → 다음 연산도 현재 값만 필요함 → 값을 놓지 않고 계속 계산 → 중간 materialization 제거`. Memory Traffic 감소를 출발점이 아니라 결과로 설명한다.
- 길이: 112초, 1080×1920, 30fps 세로형 무음. 내레이션 글자 밀도에 따라 구간을 7–11초로 재배분했다. 각 화면에는 별도 mux 없이도 내용을 이해할 수 있는 2줄 설명 자막을 포함하며, SRT와 TTS도 별도 제공한다. 실제 TTS 음성 파일이 없어 파형 기준 싱크는 미검증이다.
- 장면: `Y = ReLU(XW + b)` → 출력 원소 하나 확대 → FMA 누적 → Thread/Warp가 여러 accumulator fragment를 보유 → 값이 아직 live임을 정지 화면으로 강조 → Bias의 원소별 dependency → ReLU의 원소별 dependency → 한 값의 연속 생명주기 → 분리 실행을 비교 대상으로 짧게 표시 → 최종 STORE만 남는 fused 흐름 → GEMM epilogue → materialization 제거 → 재사용 가능한 Fusion 조건 질문.
- Thread 정확성: `출력 원소 하나 = Thread 하나 = register 하나`라고 고정하지 않는다. 실제 GEMM은 GPU 세대, Tensor Core 사용, 데이터형과 타일링에 따라 한 Thread가 여러 accumulator fragment를 보유하거나 Warp 단위로 결과를 다룰 수 있다. 화면의 `cᵢⱼ`는 dependency를 설명하기 위한 확대 예시이며, 문구는 “실행 중인 Thread/Warp가 출력의 일부를 가지고 있다”로 유지한다.
- Elementwise 조건: ReLU는 현재 값 하나로 계산 가능하다. Bias add는 현재 값과 해당 열에 대응하는 `bⱼ`가 필요하지만 다른 출력 원소는 필요하지 않는다. 따라서 둘 다 현재 출력 fragment를 소비하는 흐름에 넣기 쉽다.
- Fusion 한계: 여러 출력 사이의 관계가 필요한 연산도 fusion이 불가능하다고 단정하지 않는다. 필요한 동기화, 데이터 이동, tile 범위와 구현에 따라 조건이 복잡해진다고만 말한다.
- 비교 장면: 분리 실행은 중간 `STORE → Global Memory → LOAD`를 반복하고, fused 실행은 `cᵢⱼ → +bⱼ → ReLU → final STORE`로 이어진다. 캐시나 기존 framework/compiler fusion에 따라 실제 물리적 트래픽은 달라질 수 있으므로 절대적인 속도나 바이트 수를 주장하지 않는다.
- 1화와의 연결: FMA는 출력값이 만들어지는 누적 과정에서 자연스럽게 재등장하지만, 이번 편의 중심은 명령 결합 비교가 아니라 intermediate value의 생명주기와 elementwise dependency다.
- 화면·자막·대본에는 숫자와 영어 원표기를, 한글 발음은 `tts_script.txt`에만 둔다.
- 참고: NVIDIA CUTLASS의 GEMM epilogue 및 NVIDIA CUDA Programming Guide의 accumulator/register/global memory 설명을 기준으로 한다.
