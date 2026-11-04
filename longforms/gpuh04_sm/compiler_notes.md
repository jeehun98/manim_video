# CUDA 결과와 영상의 개념도 구분

`compute.cu`를 CUDA 13.3, sm_86, -O3로 컴파일하고 RTX 3060에서 실행했다.
N=1003, blockSize=128, gridSize=8이며, 마지막 Block의 경계 검사까지 포함해 모든 결과가 `2*A[i]`와 일치했다. 컴파일러 보고값은 Thread당 10 Register, Shared Memory 0 bytes, Spill 0 bytes다.

실제 API가 보고하는 장치 최대치는 SM당 48 Warp이고, 이 kernel의 이론적 최대 상주율은 100%다. 이는 8개 Block을 실행했을 때 모든 SM이 100% 차 있다는 측정값이 아니다.

영상의 최대32Warp와 16/32=50%는 사용자 콘티가 정한 가상 SM의 설명용 수치다. 영상의 Warp 0 Load→대기→Warp 1·2 발행→Warp 0 재개는 데이터 지연이 발생하고 다른 Warp에는 발행 가능한 명령이 있다고 가정한 예시다. 실제 kernel이 이 순서나 이 지연으로 실행됐다는 주장이 아니다. 단순한 곱셈의 기계 명령 형태와 메모리 대기는 컴파일러·캐시 상태 등에 따라 달라질 수 있다.

## 참고

- [NVIDIA CUDA Best Practices — Occupancy](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy): 상주 Warp 비율, Register·Shared 자원 제한, 높은 Occupancy가 높은 성능을 보장하지 않는다는 설명.
- [NVIDIA CUDA Programming Guide — Hardware Multithreading](https://docs.nvidia.com/cuda/archive/11.1.1/cuda-c-programming-guide/index.html#hardware-multithreading): 상주 Warp 실행 상태와 스케줄링, 준비된 명령 발행.

2026-10-29 확인. 대본은 사용자가 확정한 문장과 종료 시각을 유지했다.
