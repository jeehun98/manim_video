# GPU 계층 구조 LEVEL 07 — Shared Memory

사용자 문장 종료 시각 160초 · 독립 씬 17개 · 가로/세로 30fps · 무음/전체 자막.
상단 관계도도 기록, 이웃 읽기, 동기화, Tile 재사용, Bank 접근에 맞춰 움직인다.

```powershell
python longforms/gpuh07_shared_memory/build.py --preview
python longforms/gpuh07_shared_memory/build.py --jobs 4
python longforms/gpuh07_shared_memory/verify.py
```

실제 CUDA 검증: neighborRead 1×128, 별도 GEMM N=4 / TILE=2, 32 Bank 중 4개 활성 Lane.
`cuda_validation.txt`와 `cuda_trace.json`에 실행 결과를 보관한다.
타일링의 32→16은 선택한 출력 4개의 소스 수준 입력 요청 원소 수이며 실측 DRAM 트래픽이 아니다.
도착 순서, 서비스 단계와 64 KiB 예산은 설명용이다.

기술 기준: [NVIDIA CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html), [Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html).
