# GPU 연산과 최적화 04 — GPU는 코드를 어떤 순서로 실행할까?

- 핵심 메시지: CUDA 코드는 Thread 관점에서 쓰지만, NVIDIA GPU의 SM은 32개 Thread를 Warp로 묶어 명령을 발행한다. 한 Warp가 데이터 의존성이나 메모리를 기다릴 때 다른 준비된 Warp의 명령을 진행해 지연을 숨길 수 있다.
- 1화 FMA를 실제 실행 단위와 연결하고, 3화의 “더 넓은 명령을 볼 수 있다”를 컴파일 시점 Instruction Scheduling으로 회수한다.
- 길이: 108초, 1080×1920, 30fps 세로형 무음. SRT와 TTS는 별도. TTS 발음 대본의 공백·문장부호를 제외한 627글자를 구간별로 세어 6·8·9·9·10·9·9·10·9·9·11·9초로 배분했다. 실제 TTS 음성 파일이 없어 파형 기준 싱크는 미검증이다.
- 장면: Thread별 kernel → 32 Thread Warp → 공통 FMA 명령과 각 lane의 데이터 → Warp 0 LOAD 후 대기 → Warp 1/2/3 선택 → 시간축의 빈 공간 채우기 → 컴파일러 명령 배치와 실행 시 Warp 선택을 구분 → Warp 수가 적으면 대기가 드러남 → 다음 화의 Global Memory 질문.
- SIMT 정확성: Warp는 32개 Thread로 구성되지만 분기 등으로 모든 lane이 항상 활성이라는 뜻은 아니다. 화면의 FMA 예시는 모든 lane이 같은 경로에 있는 경우다. Volta 이후 Independent Thread Scheduling도 있으므로 Thread가 모든 순간 엄격한 lockstep이라는 문구는 피한다.
- Warp Scheduler는 각 SM에서 준비된 Warp의 다음 명령을 선택한다. 이는 컴파일러가 만든 명령 순서와 다른 층위다. 한 Warp의 메모리 latency는 남아 있고 충분한 다른 준비된 Warp가 있을 때 그 시간을 다른 작업으로 덮을 수 있다. 모든 명령/warp를 마음대로 재배열한다고 표현하지 않는다.
- 영상의 시간축은 개념도이며 실제 사이클 수나 GPU별 발행 폭을 주장하지 않는다. FMA 역시 1화처럼 조건이 허용될 때 가능한 contraction이다.
- 화면·자막·대본에는 숫자와 영어 원표기를, 한글 발음은 `tts_script.txt`에만 둔다.
- 참고: [NVIDIA CUDA Programming Guide — Warps, SIMT, Warp Scheduler](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html), [NVIDIA CUDA Programming Guide — Warps and SIMT](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html), [NVIDIA CUDA Best Practices Guide — Latency Hiding](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-best-practices-guide/).
