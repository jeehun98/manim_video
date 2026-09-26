# GPU 연산과 최적화 01 — 곱셈과 덧셈을 적었는데, GPU는 FMA를 실행한다

- 목표: CUDA source의 `a*b+c`가 항상 별도 MUL·ADD 명령으로 실행되지는 않는다는 발견을 전달한다.
- 길이: 73초. 1080×1920, 30fps 세로 영상. 영상은 무음이며 대본·SRT·TTS는 별도다.
- 0–20초: CUDA 코드 → 자연스러운 `MUL → ADD` 예상 → compiler를 통해 `FMA`로 바뀌는 첫 반전.
- 20–38초: FMA의 세 입력과 단일 결과, 분리 연산의 두 번 반올림과 FMA의 한 번 반올림을 비교한다. 동일한 실수식이어도 부동소수점 결과가 다를 수 있다.
- 38–59초: source로 돌아와 FMA의 출처를 묻고, `CUDA Source → Compiler → PTX → Machine Code → GPU`를 한 번만 보여준다. compiler 내부에서 가능한 contraction에 초점을 둔다.
- 59–73초: 다른 최적화 이름을 소개하고 `Source Code ≠ Executed Instructions`와 다음 편 질문으로 마친다. 마지막 7초는 시리즈로 넘어가는 문이다.
- 기술 조건: `float`의 `a*b+c`는 컴파일 옵션과 표현식 조건이 허용되면 contraction될 수 있다. NVCC의 `--fmad` 기본값은 `true`지만, 모든 커널이 반드시 FMA가 된다고 단정하지 않는다. FMA는 곱셈 중간 결과를 별도로 반올림하지 않고 최종 결과만 반올림한다. 속도 향상은 이 영상에서 보장하지 않는다.
- 화면·자막·대본의 영어와 숫자는 원문 표기. 발음 표기는 `tts_script.txt`에만 둔다.
- 참고: [NVIDIA CUDA Programming Guide — FMA](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/mathematical-functions.html), [NVIDIA nvcc — `--fmad`](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/).
