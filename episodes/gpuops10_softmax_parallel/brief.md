# GPU 연산과 최적화 10 제작 기준

## 제목과 형식

**Softmax는 GPU에서 왜 까다로울까? — 두 번의 Reduction**

- 108초, 세로 1080×1920, 30fps, 무음
- 별도 TTS 원고와 SRT 제공. 화면 문구에는 수식·영문 원어를 유지한다.
- 직전 09화 ReLU의 원소별 독립성을 출발점으로 삼는다. 07화의 Fusion은 짧게 회수한다.

## 학습 목표

Softmax의 출력이 전체 입력에 의존한다는 점을 이해한다. 안정적인 계산에서는 최댓값과 지수값의 합을 각각 Reduction으로 구하며, 그 사이에 원소별 계산과 결과 공유가 있음을 시각화한다.

## 계산 및 표현의 경계

1. `pᵢ = exp(xᵢ−m) / Σⱼ exp(xⱼ−m)`, `m = maxⱼ xⱼ`. 유한하고 비어 있지 않은 벡터에서는 최댓값을 빼도 실수 연산상 같은 Softmax다. 부동소수점 결과가 비트 단위로 같다는 뜻은 아니다.
2. `[1,2,1000]`의 `exp(1000)`은 일반적인 float에서 overflow 위험을 설명하는 예다. 최대값을 빼면 가장 큰 지수의 인수는 0이다.
3. Reduction tree와 Thread 하나당 원소 하나는 교육용 도식이다. 실제 매핑과 reduction 방식은 크기·하드웨어·구현에 따라 달라진다.
4. 같은 실행 범위 안의 협력과 동기화를 도식화한다. 여러 block 사이에는 추가 단계가 필요할 수 있다. 모든 길이가 단일 Kernel에서 처리된다고 주장하지 않는다.
5. 별도 Kernel이면 중간 global-memory 왕복이 생길 수 있으며, Fusion은 이를 줄일 수 있다. Fusion이 두 Reduction 또는 동기화 자체를 제거하는 것은 아니다.

## 장면과 목표 시각

| 종료 | 장면 |
|---|---|
| 09초 | ReLU 대 Softmax 의존성 |
| 18초 | 네 Thread의 지수와 공통 분모 |
| 25초 | 직렬 합산의 한계 |
| 33초 | 병렬 합 Reduction tree |
| 43초 | 큰 지수와 최댓값 빼기 |
| 51초 | 첫 Reduction: max |
| 58초 | 최댓값 공유 후 원소별 exp |
| 67초 | 두 번째 Reduction: sum, 분모 공유 |
| 75초 | ReLU 대 Softmax 흐름 비교 |
| 83초 | Elementwise / Reduction / 대기 |
| 91초 | 분리된 Kernel의 중간 데이터 이동 |
| 99초 | 가능한 경우 Kernel Fusion |
| 108초 | 핵심 요약과 다음 편 질문 |

## TTS 싱크

문장별 발화량을 고려해 구간을 7~10초로 배정했다. 화면 전환은 구간 초반 약 1초 안에 끝나고 나머지 시간 동안 해당 핵심 시각화를 유지한다. 최종 TTS 음성의 실제 길이에 맞춘 소폭 조정은 가능하다.

## 참고 자료

- NVIDIA cuDNN Developer Guide, Softmax graph: https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-895/pdf/cuDNN-Developer-Guide.pdf
- NVIDIA CUDA C Programming Guide, synchronization and thread blocks: https://docs.nvidia.com/cuda/archive/11.4.0/pdf/CUDA_C_Programming_Guide.pdf
