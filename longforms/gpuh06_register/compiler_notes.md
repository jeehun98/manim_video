# 실제 컴파일 결과와 개념 시각화

2026-10-31, CUDA13.3 / sm_86 / -O3 / RTX3060에서 `register_example.cu` 실행. 1536개 출력이 모두 입력 합과 일치했고 Thread2의 A[2]=3,B[2]=4,C[2]=7을 확인했다.

컴파일 로그는 Thread당12Register, Spill Store0bytes, Spill Load0bytes다. 런타임 함수 속성도12Register와Local0bytes를 보고했다. 이 수치는 소스의 a,b,sum 세 변수에 대한 세 슬롯 배치도가 아니며, 포인터·인덱스 등을 포함한 컴파일된 커널의 전체 요구량이다.

영상의 32/64Register는 이 vectorAdd의 실제 사용량이 아닌 별도 가상 예시다. 128Thread에서4096/8192개의32-bitRegister가 필요하다는 단순 곱셈을 보여준다. 가상SM예산32768Register/max32Warp로, 다른 제약과 할당단위를 무시하면8/4Block과32/16Warp를 표현한다. 실제 장치의 SM사양이나 정밀Occupancy계산 결과가 아니다. 성능 배수도 추정하지 않는다.

Spilling 장면은 컴파일러 동작의 개념도다. 이 실제vectorAdd에서 Spilling이 발생했다고 주장하지 않는다. `spill_store`/`spill_load`는 CUDA원문이나 실제SASS를 인용한 것이 아닌 설명용 의사표현으로 패널 제목에 표시했다. Local은Thread전용 논리주소공간이며 L1/L2캐시와DRAM계층의 경로를 그렸다. 캐시 적중 시 매번DRAM에 접근하지 않는 경로도 보여준다. RegisterPressure와Spilling을 동일시하지 않는다.

참고: [NVIDIA CUDA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html), Local Memory, Registers / Register Pressure, Occupancy 절. 실제 컴파일 로그는 cuda_compile.log, 검증 결과는 cuda_validation.txt 및 cuda_trace.json에 보존.


## v3 동작 경로

Load는L2캐시적중가정에서L2→L1→Register로표시한다. Global Store는Register→L2의요청경로로표시해L1캐시배정을단정하지않는다. 이요청을DRAM쓰기완료와동일시하지않는다. Local Spill은별도가정의경로이며실제vectorAdd의Spill0결과와분리한다. 경로는실측트레이스가아니다. 참고: https://docs.nvidia.com/cuda/parallel-thread-execution/ 의Cache Operators for Memory Store Instructions.
