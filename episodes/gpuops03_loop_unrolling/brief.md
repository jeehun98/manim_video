# GPU 연산과 최적화 03 — 반복문을 없애면 왜 빨라질까?

- 핵심 질문: 코드를 짧게 쓰는 것이 좋아 보이는데 컴파일러는 왜 더 긴 실행 코드로 펼칠까?
- 핵심 개념: Loop Unrolling은 반복 본문을 여러 번 복제해 일부 또는 모든 반복 제어를 줄이는 변환이다. 반복 횟수가 알려진 작은 CUDA 루프는 컴파일러가 자동으로 펼칠 수 있고 `#pragma unroll`로 제어할 수도 있다.
- 길이 84초, 1080×1920, 30fps 세로 무음. SRT와 TTS는 별도 파일.
- 0–15초: 네 번의 dot-product 누적 루프와 `k`, 조건, 분기라는 제어 흐름을 보여준다.
- 15–29초: 고정된 네 번 반복을 네 줄의 계산으로 펼친다. 소스는 짧지만 생성 코드는 길어질 수 있다.
- 29–51초: 분기/반복 제어가 줄어드는 것은 한 이점이다. 동시에 네 개의 독립적인 곱셈이 보이고 더 넓은 범위의 명령 스케줄링 기회가 생길 수 있다는 점에 집중한다. `sum` 누적에는 순서 의존성이 남으므로 네 FMA가 동시에 실행된다고 표현하지 않는다.
- 51–64초: 1화와 연결한다. 펼친 `sum += a[k]*b[k]`의 각 항목은 조건이 허용되면 FMA로 contraction될 수 있다.
- 64–84초: 코드 크기 증가와 레지스터 압박 가능성, 펼침 정도의 조절, 개념적인 비단조 성능 그래프를 보여준다. 그래프는 측정값이 아니라 개념도임을 화면에 적는다. `8×`는 처음의 4회 예시가 아닌 일반적인 긴 루프의 펼침 계수 비교다.
- 발화 시간 조정: TTS 표기의 공백·문장부호를 제외한 504글자를 구간별로 세고, 앞선 두 화의 발화 밀도에 맞춰 7·8·7·7·10·12·13·11·9초로 배분했다. 실제 TTS 음성 파일은 이 저장소에 없어 파형 기준 싱크는 아직 검증되지 않았다.
- 기술적 주의: 루프를 펼친다고 반드시 빨라지는 것은 아니다. 제어 명령 감소, 명령 수준/메모리 수준 병렬성, 레지스터 사용량, 명령 코드 크기와 실제 GPU에 따라 결과가 달라진다. FMA contraction도 조건부다.
- 화면·자막·대본에는 숫자와 영문 원문 표기를 유지하고 한글 발음은 `tts_script.txt`에만 둔다.
- 참고: [NVIDIA CUDA Programming Guide — `#pragma unroll`](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cpp-language-extensions.html), [NVIDIA Profiler Guide — ILP와 unrolling](https://docs.nvidia.com/cuda/profiler-users-guide/), [NVIDIA Developer Blog — code size](https://developer.nvidia.com/blog/new-compiler-features-cuda-8/).
