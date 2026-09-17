# GPU 02 — Warp란 무엇인가

164초 · 세로 FHD · 30fps · 무음 마스터. GPU 01의 색과 데이터 셀을 이어 사용합니다.

## 구성

0–37초: Thread / Block / Grid 복습, 32개 Thread를 담은 Warp 0과 Warp 1.
37–84초: 같은 +1 명령을 각자의 데이터에 실행하는 SIMT. Thread 관점과 실행 관점 비교.
84–140초: 조건에 따른 실행 경로, 활성 마스크와 Branch Divergence, 공통 명령으로 복귀.
140–164초: 동일 Thread 수라도 실행 경로가 다를 수 있다는 결론.

## 설명 범위

NVIDIA CUDA의 Warp는 32개 Thread로 구성됩니다. 64개 Thread를 갖는 1차원 Block을 예로 들며 T0–T31과 T32–T63은 해당 Block의 로컬 선형 Thread 번호입니다. 두 Warp에 각각 32개 표식을 실제로 표시합니다. 이후 계산 장면은 Warp 0의 8개 Thread만 확대합니다.

Warp 명령은 해당 명령의 활성 Thread들에 적용된다고 설명합니다. 항상 32개가 동기화되어 움직인다거나 한 클록 안에 모두 끝난다고 설명하지 않습니다. 최신 GPU의 Independent Thread Scheduling을 고려해 초안의 절대적인 동시 실행 표현을 완화했습니다.

분기 장면은 경로별 활성 마스크를 설명하는 개념도입니다. 실제 명령 순서·소요 사이클·컴파일 결과를 재현한 그림이 아닙니다. 짧은 조건문은 predication으로 구현될 수도 있습니다. 여기서 사용한 A 다음 B 순서는 설명을 위한 선택이며, 모든 조건문이 같은 비용으로 직렬화되거나 분기가 항상 2배 느려진다는 뜻이 아닙니다. Warp가 다르면 실행 경로도 별도로 진행할 수 있습니다.

## 계산 예시

입력: [-2, 3, 0, 4, -1, 2, -3, 1]
조건: x > 0이면 y = x + 1, 그 외에는 y = x − 1.
A의 활성 Thread: T1, T3, T5, T7. B: T0, T2, T4, T6.
출력: [-3, 4, -1, 5, -2, 3, -4, 2]. 0은 B 경로로 갑니다.

## 근거

[NVIDIA CUDA Programming Guide — SIMT와 독립 Thread 스케줄링](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html)

## 파일과 실행

20_softmax_attention_finale과 같은 구성: scene.py, narration.md, tts_script.txt, captions.srt, brief.md.
타이밍과 대본의 기준은 scene.py의 CAPTIONS 및 DURATION입니다. narration.md, tts_script.txt, captions.srt 모두 실제 영상 자막 원문을 그대로 사용합니다. TTS 텍스트는 줄바꿈만 공백으로 바꾸며 발음 치환·의역·추가 설명은 넣지 않습니다. 영상과 화면 전환 시각은 변경하지 않았고 합성 음성은 생성하지 않습니다.

`python scripts/render.py gpu02`

결과: exports/gpu02.mp4
