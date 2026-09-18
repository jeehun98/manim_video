# GPU 09 — Shared Memory Bank Conflict

174초 · 1080×1920 · 30fps · 음성 미포함 마스터.

## 구성

- 0–24초: Shared Memory Bank 구조, 32 Banks와 Warp의 32 Threads.
- 24–48초: 연속 원소와 간격 32 원소 요청의 Bank 매핑 비교.
- 48–72초: 서로 다른 주소의 Bank Conflict, 분할 처리, 같은 데이터 양.
- 72–120초: 행/열 접근, 전치의 문제, 32×33 Padding과 Bank 매핑 변경.
- 120–138초: 정확히 같은 주소 읽기와 Broadcast.
- 138–174초: Global 트랜잭션과 Shared Bank 비교, 적용 범위와 접근 패턴 설계.

## 파일 및 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu09`

최종 영상: exports/gpu09.mp4. 공통 DataCell, MemoryBox, DataArrow를 재사용하고 BankArray와 AccessTable로 구조를 나눴습니다. CAPTIONS/DURATION이 전환 시각을 정의하며 narration.md와 captions.srt는 실제 자막 원문입니다. tts_script.txt만 영어·숫자·수식을 한글 발음으로 변환합니다.

29개 연속 구간, wait 호출 없음. 실제 음성을 합성하지 않아 발화 길이나 음성의 무대사 구간은 검증 대상이 아닙니다.

## 모델과 범위

32-bank, 연속 32-bit word가 연속 Bank에 매핑되는 구조입니다. Warp의 모든 Thread가 같은 scalar load에서 정렬된 4-byte 원소 하나씩 읽고, 시작 원소는 Bank 0입니다. bank = word_index mod 32이며 화면 원소 번호는 byte 주소가 아닙니다.

- stride 1: 주소 0…31 → Bank 0…31.
- stride 32: 주소 0,32,…,992 → 같은 Bank 0의 서로 다른 32개 word. 이 읽기 모델에서 32-way conflict.
- stride 33: 주소 0,33,…,1023 → Bank 0…31. 해당 열 접근에서 conflict 제거.

처리 단계는 요청 분할의 개념도이며 실제 cycle 수, Kernel 속도 배수 또는 측정 결과가 아닙니다. 두 패턴 모두 32×4=128 bytes를 읽습니다. Bank와 Thread는 각각 32개로 표시하며 자세한 주소 표와 화살표는 대표 Thread 4개를 확대합니다.

행 우선 32×32 배열에 각 행 끝 한 칸을 추가해 32×33으로 바꿉니다. 첫 4행·첫 4개 값만 보여주고 중간 28열은 생략합니다. PAD는 계산에 사용하지 않습니다. 값은 유지하고 첫 열의 원소 번호를 0,32,64,96에서 0,33,66,99로 바꿉니다. Bank 수 자체는 32개로 유지됩니다.

정확히 같은 word의 읽기는 Broadcast가 가능하므로 서로 다른 word의 Bank Conflict와 구분합니다. 같은 주소에 대한 경쟁 쓰기가 올바르다는 뜻은 아닙니다. 벡터 명령, 다른 원소 크기나 Bank 모드, 분할된 하드웨어 요청에는 별도 분석이 필요합니다. Padding을 모든 접근의 보편적 해결책으로 주장하지 않습니다.

[NVIDIA CUDA Best Practices — Shared Memory and Memory Banks](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#shared-memory-and-memory-banks)

[NVIDIA CUDA Programming Guide — Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

[NVIDIA Nsight Compute — Profiling Guide](https://docs.nvidia.com/nsight-compute/ProfilingGuide/)
