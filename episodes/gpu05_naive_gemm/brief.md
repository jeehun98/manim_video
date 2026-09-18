# GPU 05 — Naive GEMM: 같은 값을 몇 번 다시 읽을까?

174초 · 1080×1920 · 30fps · 음성 미포함 마스터.

## 장면 구성

- 0–30초: 메모리 역할 복습, 4×4 행렬의 한 행과 한 열을 곱하고 합산.
- 30–78초: Thread별 출력 매핑, Register 중간 합 누적, 결과 저장.
- 78–114초: A의 행과 B의 열에서 반복되는 입력 요청, 계산과 메모리 비용의 구분.
- 114–138초: 입력 재사용 기회와 Naive GEMM의 특징.
- 138–174초: Block 공용 Shared Memory, 2×2 조각 적재와 동기화, 재사용과 Tiling 연결.

## 파일 및 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu05`

최종 영상: exports/gpu05.mp4. 공통 DataCell, MemoryBox, DataArrow를 gpu_series에서 재사용합니다. MatrixCells는 이번 행렬 표현의 재사용 구성요소입니다. CAPTIONS와 DURATION이 문구와 전환 시간을 정의하며 장면별 동작은 개별 메서드로 나눴습니다.

## 자막과 TTS

29개 구간이 0초부터 174초까지 이어집니다. narration.md와 captions.srt는 실제 화면 자막과 같습니다. tts_script.txt는 같은 내용을 한글 발음으로 바꿨습니다. Naive GEMM은 나이브 젬, Tiling은 타일링, A·B·C는 에이·비·씨로 읽습니다. 음성은 합성하지 않았으므로 실제 발화 길이나 음성의 침묵 구간은 검증 대상이 아닙니다.

## 수학과 기술적 범위

C=AB의 교육용 단순 구현을 보여줍니다. 일반 GEMM의 알파·베타 항이나 라이브러리 구현 전체를 다루지는 않습니다. Thread 하나가 출력 하나를 맡는 매핑은 이 단순 Kernel의 예이며 실제 고성능 GEMM의 보편적 매핑이라고 주장하지 않습니다.

A 첫 행 [1,2,3,4], B 첫 열 [2,1,0,2]의 내적은 2+2+0+8=12입니다. 모든 출력값은 코드에서 입력으로부터 계산합니다. Register 중간 합은 0→2→4→4→12입니다.

같은 A 원소는 C의 같은 행에, 같은 B 원소는 C의 같은 열에 재사용됩니다. 화살표는 논리적 읽기이며 각각을 별도 DRAM 트랜잭션으로 세지 않습니다. 캐시, Warp의 요청 병합 등으로 실제 이동 비용이 달라질 수 있습니다. Shared Memory 사용이 모든 경우에 빠르다는 뜻은 아닙니다.

마지막 2×2 조각은 출력 2×2 영역의 부분 합 계산을 위한 첫 K 구간입니다. 전체 4×4 곱을 완료하려면 나머지 K 구간도 이어서 처리해야 하며 화면에 표시했습니다. 조각을 적재한 뒤 필요한 동기화를 맞추는 개념까지 보여줍니다. 정확한 인덱스·장벽·경계 처리 구현은 다음 단계의 범위입니다.

[NVIDIA CUDA Best Practices — Shared Memory in Matrix Multiplication](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#shared-memory-in-matrix-multiplication-c-ab)
