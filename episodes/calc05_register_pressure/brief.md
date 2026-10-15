# 계산의 두 얼굴 05 — GPU의 병렬성을 높였는데 왜 느려질까?

부제: Register Pressure와 Occupancy. 중심 반전: Register Spilling.

## 학습 목표

스레드의 자원 사용이 활성 Warp 수를 제한할 수 있음을 이해한다. Occupancy를 실행 장치 활용률과 구별하고, 레지스터 사용 제한이 활성 Warp 증가와 spill 접근 증가를 동시에 가져올 수 있음을 발견한다. GEMM의 재사용과 자원 예산까지 포함한 전체 실행 시간을 비교한다.

## 제작 기준

- 사용자 콘티에 구간 시간이 없어 초기 편집 예산 145초로 구성한다. 실제 TTS 미제공이며 문장 경계는 추정이다.
- 1080×1920·30fps, 미리보기 360×640. 무음 영상, SRT·발음 원고 별도.
- 9개 장면 종료: 14,26,48,63,81,105,122,136,145초.
- 복습·요약 및 다음 편 예고 없이 질문→자원 제약→지연 숨기기→Spilling 반전→GEMM→전체 비용의 결론으로 완결한다.

## 기술 조건과 과장 방지

1. Warp는 32스레드. 활성 Warp는 SM에 상주하는 Warp이며 모든 상주 Warp가 동시에 명령을 실행하는 뜻이 아니다. 총 요청 스레드 수·상주 스레드 수·실행 명령 수를 구분한다.
2. 교육용 SM은 65,536개의 32-bit registers, 최대 2,048 threads=64 warps, block=256 threads=8 warps로 가정한다. 다른 자원과 할당 단위를 생략한다. 활성 블록 수는 floor(65536/(256×R)), 최대 8. R=32/64/128이면 블록 8/4/2, 스레드 2048/1024/512, warps 64/32/16, Occupancy 100/50/25%다. 특정 실제 GPU의 스펙이 아니다.
3. Register File 위쪽 칸은 블록당 할당 예산이다. 아래 8개 블록은 작업 목록이며 밝은 블록만 상주, 나머지는 대기 작업이다. 회색 블록이 SM 자원을 점유한 상주 작업으로 보이지 않도록 제목을 표시한다. 스레드가 서로의 레지스터 변수에 임의 접근한다는 뜻이 아니다.
4. Latency Hiding 모형은 6개 추상적인 발행 슬롯이다. W0 load 이후 W0가 기다리는 동안 W1/W2의 준비된 명령을 발행하거나 준비된 명령이 없어서 대기한다. 실제 SM의 scheduler 개수·동시 발행 폭·수치 지연을 모사하거나 성능 배수를 제시하지 않는다. resident만으로 eligible한 Warp가 되는 것은 아니다.
5. Occupancy는 활성 Warp/최대 활성 Warp. 실행 장치 utilization과 다르다. 충분한 ILP로 낮은 occupancy에서도 높은 처리량이 가능하며 높은 occupancy가 성능 보장은 아니다.
6. Register Spilling 장면의 a–e는 한 스레드가 유지하는 중간값의 개념 모형이다. 레지스터 제한 시 일부 값을 Local 주소 공간에 저장하고 재사용 때 load할 수 있다. 컴파일러는 재계산·명령 스케줄 변경 등을 선택할 수도 있어 제한이 항상 spill을 만드는 것은 아니다.
7. Local Memory는 디바이스 메모리 주소 공간의 스레드별 영역이며 레지스터 같은 온칩 저장소가 아니다. 캐시를 통해 접근하므로 모든 access가 DRAM miss인 것은 아니다. 영상은 일반적인 Local spilling 경로 예시이며, 새로운 컴파일러의 선택적인 Shared spilling 등의 모든 전략을 설명하지 않는다.
8. 활성 Warp 증가의 이익이 spill 비용보다 클 수도 있다. A와 B의 승자를 정하거나 spill이면 반드시 느리다고 주장하지 않는다. 실제 compiled register count·local access·runtime은 실측해야 한다.
9. GEMM 장면은 register-backed accumulator tile의 개념 비교다. 실제 block tile·thread tile·warp mapping·dtype·MMA 명령에 따라 자원이 달라진다. 모든 Tile 증가가 모든 스레드의 register 사용을 증가시키거나 모든 최신 GPU의 accumulator가 반드시 같은 register 경로를 쓰는 것은 아니다.
10. 같은 문제를 풀 때 재사용 증가와 중간값 수명 증가가 함께 생길 수 있다. Tile 크기·매핑 변경의 trade-off이며 4칸/16칸 그림을 실제 레지스터 수치와 동일시하지 않는다. 산술 연산 횟수를 일부러 늘리는 장면이 아니다.

## 장면

| 시간 | 주장 |
|---|---|
| 0–14 | 병렬성을 높였는데 메모리 접근도 늘 수 있다 |
| 14–26 | 스레드는 중간값을 유지할 레지스터 자원이 필요 |
| 26–48 | 32/64/128 registers/thread의 같은 SM 자원 배분 |
| 48–63 | 준비된 다른 Warp로 지연 숨기기 |
| 63–81 | Occupancy와 utilization 구별, ILP |
| 81–105 | 레지스터 제한→Spill Store/Reload→Local/cache 경로 |
| 105–122 | 활성 Warp 증가 이득과 추가 이동 비용 비교 |
| 122–136 | GEMM 누산 Tile의 재사용과 register pressure |
| 136–145 | 경쟁하는 자원 사이의 전체 실행 시간 최소화 |

## 출처

- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html): occupancy, register pressure, ILP, local memory, register 제한의 trade-off.
- [CUTLASS Efficient GEMM](https://docs.nvidia.com/cutlass/latest/media/docs/cpp/efficient_gemm.html): accumulator의 register 자원과 tiling/occupancy 관계.
- [NVIDIA CUTLASS Linear Algebra](https://developer.nvidia.com/blog/cutlass-linear-algebra-cuda/): register/shared 자원이 GEMM 병렬 배치를 제한하는 사례.

## 검증

교육용 register 예산·블록·스레드·Warp·Occupancy를 검산한다. 준비/대기 슬롯과 Local spilling 표현을 검토한다. 미리보기 및 최종 주요 프레임의 겹침·자막·범위를 확인하고 누적 시간 gate와 출력 프레임 수·길이·오디오를 검사한다. TTS 싱크와 GPU 커널 성능은 별도다.

### 2026-10-15 제작 검증 결과

- Manim 0.21.0, FFmpeg, Malgun Gothic 확인。미리보기와 최종 렌더 완료.
- 최종 1080×1920·30fps 설정·4,350프레임·145.000초, 무음. 목표 145초와 1프레임 이내 차이.
- 미리보기 12/24/35/46/61/79/103/134초 및 최종 103/120/143초 확인. 모든 누적 시간 gate 통과.
- 32/64/128 registers/thread의 8/4/2블록, 2048/1024/512threads, 64/32/16warps, 100/50/25% Occupancy 검산.
- 실제 음원 발화 싱크와 GPU 커널 성능 실측은 미실시다.
