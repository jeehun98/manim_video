# Quantization 시리즈 7편 제작 기준

- 이 편의 중심 인과관계는 `작은 datatype → 같은 전송량에 더 많은 값 → memory traffic 감소 가능`이다.
- 제목과 첫 장면은 bit 수를 사용하지만, 본론은 저장 공간보다 HBM과 compute 사이의 데이터 이동에 더 많은 시간을 배정한다.
- FP32는 값당 32 bits = 4 bytes, INT8은 값당 8 bits = 1 byte다. 부가 metadata를 제외한 동일 개수 원소의 원시 저장 공간은 정확히 1/4이다.
- 메인 예시는 동일한 16-byte 전송이다. 여기에 FP32는 4개, INT8은 16개 원소가 들어간다.
- `values per transfer ×4`는 동일 byte 전송량을 가정한 원소 수 비교이지, 실행 속도가 항상 4배라는 뜻이 아니다.
- 속도 효과는 memory-bound workload에서 특히 직접적이다. compute-bound 작업, 변환 비용, kernel 구현, 하드웨어 지원에 따라 실제 향상 폭은 달라진다.
- 이 편에서는 Tensor Core, SIMD, dot-product instruction, quantized GEMM의 구체적인 연산 구조를 설명하지 않는다.
- 다음 편은 낮은 precision이 산술 처리량을 높일 수 있는 이유로 연결한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
