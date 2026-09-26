# GPU 연산과 최적화 02 — GPU가 계산하기도 전에 끝난 계산

- 학습 목표: `out[i] = x[i] + (2.0f * 3.0f);`의 상수 곱셈이 GPU 실행 전에 `6.0f`로 접힐 수 있음을 발견한다. 중심 질문은 “GPU에서 사라진 계산은 누가 대신 했을까?”다.
- 핵심 대비: 1화 FMA는 실행할 연산의 형태가 바뀐 예, 2화 Constant Folding은 컴파일 시점에 확정 가능한 부분을 미리 계산해 해당 런타임 연산이 사라진 예다.
- 90초, 세로 1080×1920, 30fps, 무음. SRT와 TTS는 별도 자료다.
- 0–19초: CUDA 코드와 자연스러운 `2 × 3 → 6` 런타임 예상, 곱셈이 GPU 경로에서 사라지는 반전.
- 19–38초: `x[i] + (2.0f * 3.0f)` → `x[i] + 6.0f` 변환과 1화 FMA 비교.
- 38–59초: “누가 계산했나?” 질문, `kernel.cu → nvcc / Compiler → optimized code`에서 컴파일 도구가 호스트 CPU에서 실행된다는 설명.
- 59–68초: 위쪽 `COMPILE TIME / CPU`에서 `2 × 3 → 6`, 아래쪽 `RUNTIME / GPU`에서 `out[i] = x[i] + 6.0f`를 보여준다. CPU가 `x[i]` 데이터까지 계산한다고 표현하지 않는다.
- 68–78초: `2.0f * 3.0f`는 양쪽 값이 알려짐, `x[i] * 3.0f`는 `x[i]`가 런타임 입력이라는 경계 조건을 비교한다.
- 78–90초: 커널을 여러 번 실행해도 동일한 상수 곱셈을 반복할 필요가 없다는 점과 “미리 할 수 있는 일은 미리 한다”로 마친다.
- 정확성: `nvcc`를 사용하는 일반적인 오프라인 빌드 경로를 예로 든다. 컴파일러는 호스트 CPU에서 돌아가는 프로그램으로 상수식을 평가해 코드에 반영할 수 있다. 모든 연산이 CPU로 이동한다는 뜻은 아니다. JIT 등 다른 컴파일 경로의 세부 단계는 이 편의 범위 밖이다. `6.0f`는 `2.0f * 3.0f`의 정확한 float 결과다.
- 화면·자막·대본은 숫자와 영문 원문 표기. 발음 표기는 `tts_script.txt`에만 둔다.
- 기술 참고: [NVIDIA CUDA Programming Guide — nvcc](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/nvcc.html), [NVIDIA nvcc documentation](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/).
