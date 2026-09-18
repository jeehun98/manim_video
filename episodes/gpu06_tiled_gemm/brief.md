# GPU 06 — Tiled GEMM: 한 번 가져와, 함께 다시 쓰기

174초 · 1080×1920 · 30fps · 음성 미포함 마스터.

## 장면 구성

- 0–30초: Naive GEMM 복습, 입력 Tile과 Block의 출력 Tile 연결.
- 30–60초: Thread별 분담 적재, 공유 전 동기화, A와 B의 재사용.
- 60–96초: Register 부분 합, 덮어쓰기 전 동기화, 다음 K 구간 적재와 누적.
- 96–114초: 출력 저장, 전체 C 완성, 변하지 않은 수학.
- 114–132초: Naive와 Tiled의 논리적 입력 읽기 비교, 재사용의 의미.
- 132–150초: Tile 크기와 Shared/Register/Thread 구성의 균형.
- 150–174초: Warp 실행, coalesced 적재, Shared와 Register의 역할, 결론.

## 파일 및 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu06`

최종 영상: exports/gpu06.mp4. 공통 DataCell, MemoryBox, DataArrow는 gpu_series에서 재사용합니다. MatrixCells와 장면별 메서드로 분리했습니다. CAPTIONS와 DURATION이 화면 및 대본 타이밍을 정의합니다. 29개 연속 구간이며 wait 호출이 없습니다. 실제 합성 음성은 없으므로 발화 속도나 음성의 침묵은 검증하지 않습니다.

## 수학 및 모델

GPU05와 같은 4×4 A와 B를 사용합니다. Block 0은 C 왼쪽 위 2×2를 맡고 Thread 4개가 각각 출력 하나를 계산하는 교육용 예제입니다. 이 Thread 수를 전체 Warp 크기라고 설명하지 않습니다. 후반의 Warp 장면은 별도로 32개 lane을 보여줍니다.

K=0,1: A[0:2,0:2], B[0:2,0:2] → Register [4,5,5,4].
K=2,3: A[0:2,2:4], B[2:4,0:2] → [8,3,6,0] 추가.
최종 C 출력 Tile은 [12,8;11,4]입니다. 부분 합과 전체 출력은 A와 B에서 계산합니다. Shared 값을 교체해도 Register 누적 합은 보존합니다.

단일 Shared 버퍼를 재사용하는 설명입니다. 적재 후 공유 읽기 전, 현재 읽기가 모두 끝난 후 다음 적재 전 동기화를 모두 보여줍니다. 고급 비동기 적재나 파이프라이닝 구현은 다루지 않습니다.

한 출력 Tile의 논리적 입력 원소 읽기는 Naive 4출력×4항×2입력=32, Tiled 2구간×(A 4원소+B 4원소)=16입니다. 출력 저장은 비교에서 제외했습니다. 이는 DRAM 트랜잭션 수나 2배 속도 보장이 아니며 캐시와 요청 병합 등이 실제 이동 비용에 영향을 줍니다. Block 간 중복 입력도 있을 수 있습니다.

Tile 크기, Thread당 출력 개수, Shared 용량과 Register 사용량은 설계에 따라 함께 달라집니다. 더 큰 Tile이 항상 빠르다고 주장하지 않습니다. Tiling을 한다고 자동으로 coalesced 적재가 되는 것도 아니므로 주소 배치를 고려하는 별도 장면을 두었습니다.

[NVIDIA CUDA Programming Guide — Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

[NVIDIA CUDA Best Practices — Shared Memory in Matrix Multiplication](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#shared-memory-in-matrix-multiplication-c-ab)
