# GPU 08 — Register Pressure와 Occupancy

174초 · 1080×1920 · 30fps · 음성 미포함 마스터.

## 구성

- 0–30초: Thread별 중간 합과 Register Pressure.
- 30–60초: 유한한 SM Register 총량, 16/64 Registers per Thread 비교.
- 60–84초: Occupancy 정의, 32/64=50%, 64/64=100%, 상주와 명령 실행 구분.
- 84–108초: 준비된 Warp를 실행하는 Latency Hiding과 작업 부족.
- 108–126초: 높은 Occupancy가 항상 최고 성능은 아닌 이유와 재사용 이득.
- 126–144초: 과도한 Register 제한, Spill, 추가 메모리 읽기/쓰기.
- 144–174초: Tile·Thread당 일·Register·Occupancy의 연결, 측정과 균형.

## 파일 및 실행

scene.py · narration.md · tts_script.txt · captions.srt · brief.md

`python scripts/render.py gpu08`

최종 영상: exports/gpu08.mp4. 공통 DataCell, MemoryBox, DataArrow를 사용하고 WarpSlots는 상주 Warp 비율을 표시합니다. 장면별 메서드와 CAPTIONS/DURATION으로 타이밍을 분리했습니다. narration.md와 captions.srt는 실제 자막 원문이며 tts_script.txt만 한글 발음으로 변환합니다. Occupancy는 오큐펀시, Register Pressure는 레지스터 프레셔, Spill은 스필로 표기합니다.

29개 연속 구간이며 wait 호출은 없습니다. 음성을 합성하지 않았으므로 실제 발화 길이 또는 무음 구간을 검증한 것은 아닙니다.

## 수치 예제와 해석

가정: SM당 65,536개의 32-bit Register, 최대 상주 Warp 64개, Block당 Thread 256개(8 Warps). 다른 자원 제한과 할당 반올림은 생략합니다. 이 수치는 모든 GPU의 공통 규격을 주장하는 것이 아닙니다.

- 16 Registers/Thread: Block당 4,096개. 8 Blocks/64 Warps는 총 32,768개를 사용해 Warp 상한에 도달.
- 64 Registers/Thread: Block당 16,384개. 4 Blocks/32 Warps가 총 65,536개를 사용해 Register 상한에 도달.

사용량은 4배지만 이 예의 상주 Warp 수 감소는 64→32입니다. 첫 경우에 Register 외의 Warp 상한이 먼저 작동하기 때문입니다. 실제 상주 수는 Shared Memory, Thread/Block 상한, Register 할당 단위와 GPU에 따라 달라집니다. 가용 자원에 따른 이론적 수용 예시와 실제 실행 중 측정한 achieved occupancy는 구분해야 합니다.

Occupancy는 상주(active) Warp 수/하드웨어 최대 상주 Warp 수입니다. 상주 Warp들이 모두 같은 순간 명령을 발행한다는 뜻이 아닙니다. 스케줄 장면의 Warp 세 개는 개념적 확대이며 실제 scheduler 개수, 처리율, 정확한 실행 순서 또는 latency를 재현하지 않습니다. 낮은 Occupancy에서도 instruction-level parallelism 등으로 지연을 숨길 수 있으며 높은 Occupancy만으로 성능을 보장하지 않습니다.

Spill 그림은 필요한 값 일부가 메모리에 저장되고 다시 읽히는 개념도입니다. 일반적인 Local Memory는 Thread 전용 주소 공간이며 device memory 및 캐시를 이용합니다. Shared Memory spilling 등 컴파일러 옵션/구현 예외도 있어 항상 DRAM에 직접 접근한다고 단정하지 않습니다. 그림의 값 네 개/보관 여유 두 개는 실제 하드웨어 Register 한계가 아닙니다. Spill 비용과 최적 설정은 실제 실행 시간과 함께 확인해야 합니다.

[NVIDIA CUDA Best Practices — Occupancy](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#occupancy)

[NVIDIA CUDA Best Practices — Register Pressure](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#register-pressure)

[NVIDIA Blackwell Tuning Guide](https://docs.nvidia.com/cuda/archive/13.0.3/blackwell-tuning-guide/index.html)
