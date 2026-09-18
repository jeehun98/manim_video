# GPU 07 — Tile 크기: 왜 16×16, 32×32일까?

174초 · 1080×1920 · 30fps · 음성 미포함 마스터.

## 장면 구성

- 0–18초: Tiling 복습과 크기 선택의 질문.
- 18–48초: 출력 하나당 Thread 하나일 때 16×16=256 Threads=8 Warps, 32×32=1024 Threads=32 Warps. Block당 Thread 상한.
- 48–78초: A/B 입력 재사용과 정사각 입력 Tile의 Shared Memory 용량 비교.
- 78–114초: Thread별 중간 합과 Register, SM의 상주 작업 수, 작은/큰 Tile의 장단점.
- 114–150초: 숫자는 후보일 뿐, Matrix→Block Tile→Warp Tile→Thread Tile 계층과 출력/Thread 수 구분.
- 150–174초: 문제·자료형·GPU 자원·실행 시간 측정을 통한 선택.

## 파일 및 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu07`

최종 영상: exports/gpu07.mp4. 공통 DataCell, MemoryBox, DataArrow를 재사용합니다. TileGrid는 행렬 격자와 영역 선택을 표현합니다. 객체 전환 때 이전 도형을 명시적으로 정리해 잔상을 방지합니다.

CAPTIONS와 DURATION이 29개 화면 구간을 정의합니다. narration.md와 captions.srt는 실제 자막과 정확히 일치하며 tts_script.txt는 같은 내용을 영어·숫자·수식의 한글 발음으로 바꿉니다. wait 호출은 없습니다. 실제 음성은 합성하지 않았으므로 발화 길이나 음성 침묵 구간은 검증 대상이 아닙니다.

## 비교 조건과 기술적 범위

처음의 Thread 수는 한 Block이 출력 T×T를 맡고 Thread 하나가 출력 하나를 맡는 단순 매핑에만 해당합니다. 16²=256, 256/32=8; 32²=1024, 1024/32=32입니다. NVIDIA 문서에 기재된 현재 compute capability의 Block당 Thread 상한은 1024입니다. 커널별 자원/설정 제한까지 만족해야 하며 상한이 권장값을 뜻하지 않습니다.

Shared 용량 비교는 A와 B 각각 T×T, 합산 구간 길이도 T, 4-byte 원소, 단일 버퍼, 패딩 제외 조건입니다. 2×16²×4=2048 B=2 KiB, 2×32²×4=8192 B=8 KiB. 일반적인 M×N 출력 Tile의 입력 버퍼는 M×K와 K×N이므로, 출력 Tile만 커진다고 항상 정확히 네 배인 것은 아닙니다.

Thread당 여러 출력에는 여러 누적 합이 필요하지만 실제 Register 수는 피연산자, 주소, 컴파일러와 구현에도 달려 있습니다. SM 상주 Block이 4개에서 2개로 바뀌는 도형은 개념도이며 실제 장치 용량이나 측정값이 아닙니다. 높은 occupancy가 항상 높은 속도인 것은 아닙니다.

후반의 계층은 교육용 SIMT 소유 영역 예시입니다. 128×128 Block Tile → 8개의 32×64 Warp Tile → Warp마다 32개 Thread의 8×8 Thread Tile. 8×32=256 Threads, 256×64=16384 outputs입니다. Warp Tile의 4×8 격자에서 한 칸은 Thread 하나의 8×8 출력 영역입니다. 모든 출력에 별도 Thread를 만들지 않습니다. 이것은 보편적인 최적 구성, 실제 Register 물리 배치, Tensor Core fragment 배치에 대한 주장이 아닙니다.

16과 32가 자주 쓰이는 이유를 모든 구현에 대해 단정하지 않으며 Warp/작업 배치/자원 제한과 관계있는 후보로 설명합니다. 최적값은 행렬 크기, 모양, 자료형, GPU 및 구현에 따라 측정해야 합니다.

[NVIDIA Compute Capabilities](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html)

[NVIDIA Advanced Kernel Programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html)

[NVIDIA CUTLASS — Efficient GEMM](https://docs.nvidia.com/cutlass/latest/media/docs/cpp/efficient_gemm.html)
