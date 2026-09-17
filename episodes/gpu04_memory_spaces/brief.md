# GPU 04 — 데이터를 어디에 두고, 얼마나 다시 쓸까?

174초 · 1080×1920 · 30fps · 음성 미포함 마스터.

## 장면 구성

- 0–14초: 이전 편의 주소 패턴에서 저장 위치로 연결.
- 14–31초: 큰 입력과 출력, Global Memory를 반복해서 읽는 모습.
- 31–67초: Thread별 Register, 입력 3을 읽어 4와 8로 계산하고 개인 범위 강조.
- 67–115초: Block 공용 Shared Memory, 적재와 동기화, 여러 Thread의 재사용.
- 115–138초: Shared Memory와 Register 용량 제한, 동시 유지 작업 수와의 관계.
- 138–174초: 크기·사용 범위·재사용 기준과 전체 데이터 이동 요약.

## 파일과 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu04`

결과: exports/gpu04.mp4. 공유 DataCell, ThreadMarker, MemoryBox, DataArrow는 gpu_series에서 재사용합니다. 장면 구성은 MemoryDiagram, 장면별 동작 메서드, CAPTIONS 타임라인으로 분리했습니다.

## 대본과 타이밍

CAPTIONS가 화면 전환과 문구의 단일 기준입니다. narration.md와 captions.srt는 같은 문구를 그대로 사용합니다. tts_script.txt만 영어 및 숫자를 한글 발음으로 바꿉니다. 29개 구간이 0초부터 174초까지 연속되며 wait는 없습니다. 음성을 합성하지 않았으므로 실제 음성의 무대사 구간이나 발화 속도를 검증한 것은 아닙니다.

## 기술적 표현 범위

메모리의 논리적 사용 범위와 데이터 재사용을 표현하는 개념도입니다. 화면 거리와 화살표 횟수는 지연 시간이나 DRAM 트랜잭션 수를 뜻하지 않습니다. Global Memory 반복 읽기의 비용은 캐시 등에도 영향을 받습니다. Shared Memory 적재는 Thread의 작업이며 공유 전에 필요한 동기화를 보여줍니다. 모든 데이터가 Shared Memory를 반드시 거치는 것은 아닙니다.

Register는 컴파일러가 배치하는 Thread별 계산 자원입니다. Warp 통신 명령 등의 예외는 이번 입문 범위에서 다루지 않습니다. 자원 그림의 8개와 4개 표식은 실제 하드웨어 정원이나 성능 비율이 아닙니다. Register 사용량 증가가 동시 상주 Thread 수를 제한할 수 있음을 보여주며, 사용량과 속도의 단순 비례를 주장하지 않습니다. Shared Memory에도 Block별 및 하드웨어 자원 한계가 있습니다.

[NVIDIA CUDA Programming Guide — Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

[NVIDIA — Using Shared Memory in CUDA](https://developer.nvidia.com/blog/using-shared-memory-cuda-cc/)
