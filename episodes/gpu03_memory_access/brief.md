# GPU 03 — 같은 계산인데 왜 메모리 접근에 따라 속도가 달라질까?

175초 · 1080×1920 · 30fps · 무음 마스터.

## 장면 구성

- 0–37초: 실제 32개 Thread 표식과 연속 주소, 적은 요청 영역, Coalesced Memory Access.
- 37–61초: 같은 Thread와 연산을 유지하며 주소 간격을 32개 원소로 변경.
- 61–90초: 같은 128바이트를 요청할 때 32바이트 영역 4개와 32개가 필요한 예시 비교.
- 90–123초: 행 우선 저장된 행렬의 행 방향과 열 방향 접근.
- 123–175초: Warp 전체 요청 관점, 데이터 저장 순서와 Thread 배치, 결론.

## 표현과 기술적 범위

32개 Thread 모두 활성 상태이며 각각 4바이트 원소 하나를 읽는 예시입니다. 배열 시작은 32바이트 경계에 정렬된 것으로 가정합니다. 연속 접근은 x0–x31, 간격 32 접근은 x0, x32, x64, …, x992입니다. 주소는 원소 인덱스이며 바이트 주소는 이 인덱스의 4배입니다. 두 경우 연산은 읽은 값에 1을 더하는 동일한 규칙이며 읽는 데이터 위치는 다릅니다.

최신 NVIDIA CUDA의 기본적인 32바이트 요청 영역 모델에서 연속 접근은 4개 영역, 간격 32 접근은 32개 영역을 덮습니다. 큰 연속 박스는 전체 128바이트 주소 범위를 묶어 보여주는 개념도이며, 단일 트랜잭션을 의미하지 않습니다. 안쪽 박스가 각 요청 영역입니다. 계산은 scene.py의 sector_ids()로 주소에서 직접 유도합니다.

이 그림은 캐시 아래의 실제 DRAM 명령 수, 지연 시간, 측정된 속도 또는 고정된 속도 비율을 보여주지 않습니다. 정렬·접근 크기·캐시·하드웨어·재사용 등에 따라 실제 비용이 달라집니다. 판독 요청을 그림으로 설명하며 쓰기 최적화의 모든 세부 사항을 다루지는 않습니다.

32개의 요청은 가독성을 위해 네 줄로 접습니다. 분산 장면의 빈 주소 간격은 축약했으며 화면상의 거리 자체는 바이트 수에 비례하지 않습니다.

행렬은 행 우선 저장된 32×32 행렬의 왼쪽 위 4×4 부분만 표시합니다. 같은 행의 접근 x0,x1,x2,x3과 같은 열의 접근 x0,x32,x64,x96을 비교합니다. 첫 행과 첫 열이 같은 값이라는 설명은 하지 않습니다. 전체 행렬을 모두 읽더라도 Warp마다 묶이는 원소가 달라질 수 있음을 설명합니다.

## 대본과 TTS

scene.py의 CAPTIONS와 DURATION이 화면 전환 및 문구의 기준입니다. narration.md와 captions.srt는 자막 원문을 그대로 사용합니다. tts_script.txt만 같은 내용을 한글 발음으로 변환하며 설명을 추가하거나 의역하지 않습니다.

발음: GPU→지피유, Warp→워프, Thread→스레드, Kernel→커널, Coalesced Memory Access→코얼레스트 메모리 액세스. 인덱스는 영어 숫자 발음: x₀→엑스제로, x₁→엑스원, x₂→엑스투, x₃₂→엑스서티투, x₆₄→엑스식스티포, x₉₆→엑스나인티식스.

## 근거

[NVIDIA CUDA Best Practices — Coalesced Access](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#coalesced-access-to-global-memory): 정렬된 4바이트 원소를 인접 Thread들이 읽을 때 32바이트 트랜잭션 네 개가 필요함을 설명합니다.

[NVIDIA CUDA Programming Guide — Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html): 한 Warp의 요청 주소 분포 및 전송량 대비 사용량 관점의 설명.

## 파일과 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu03`

결과: `exports/gpu03.mp4`. 음성 합성 및 별도 검증 스크립트는 생성하지 않습니다.
