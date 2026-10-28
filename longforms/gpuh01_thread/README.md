# GPU 계층 구조 LEVEL 01 — Thread

GPU의 스레드 하나는 무엇을 할까? 사용자 확정 원문과 33개 문장 종료 시각에 맞춘 **152초** 영상. 16개 교체 가능한 Manim 씬을 가로·세로로 각각 렌더한다. 음원은 제공되지 않아 무음이며 전체 내레이션 자막을 포함한다.

## 결과물

- 세로: `../../exports/gpuh01_thread_152s_shorts_final.mp4` — 1080×1920, 30fps.
- 가로: `../../exports/gpuh01_thread_152s_longform_final.mp4` — 1920×1080, 30fps.
- 미리보기: 같은 이름의 `_preview.mp4` — 360×640 / 640×360, 15fps.
- 최종본은 각 4560프레임. 영상 파일 옆에 동일 종료 시각의 SRT도 복사한다.

## 제작·재실행

프로젝트 루트에서 실행한다. Python 3.12, Manim 0.21.0, FFmpeg, Malgun Gothic·Consolas 사용.

```powershell
python longforms/gpuh01_thread/build.py --preview
python longforms/gpuh01_thread/build.py
python longforms/gpuh01_thread/build.py --resume
python longforms/gpuh01_thread/build.py --layout shorts --scene 07
python longforms/gpuh01_thread/build.py --concat-only
python longforms/gpuh01_thread/verify.py
```

`--scene`은 해당 씬만 렌더한다. 이후 `--concat-only`로 갱신한 씬을 결합한다. `--preview` 여부와 layout을 맞춰 사용한다. `create_project.py`는 최초 자료 생성용이며 편집한 대본을 덮어쓸 수 있으므로 재실행하지 않는다.

- `master_script.md`, `narration.md`: 사용자 원문과 종료 시각.
- `tts_script.txt`: 주요 화면 변화별 발음 원고. 읽지 않는 제목·시간 제외.
- `timing.json`, `captions.srt`: 사용자 문장별 구간 33개.
- `manifest.json`, `scenes.yaml`: 16개 독립 씬과 확정 구간.
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬별 제작 자료.
- `visuals.py`: 공통 도형·코드·가로/세로 배치·문장 시각 동작.
- `build.py`: 씬별 렌더→프레임 수 검증→concat→자막→최종 검증.
- `verify.py`: 문장·씬의 구간 연속성, 최종 프레임 수·길이·해상도·코덱·음원 유무·화면 경계 검사와 16개 시점의 검토용 프레임 시트 생성. 결과는 `qa_final.json`에 기록한다.

가로형은 구조와 코드를 나란히, 세로형은 구조 위·코드 아래로 재배치한다. 자막은 별도 하단 공간에 배치한다. Register File은 SM의 자원으로 표현하며 Thread의 개별 물리 메모리로 그리지 않는다. 화면 동작은 소스 수준의 개념도이며 GPU 명령 trace를 재현하지 않는다.

## 코드 가독성 수정 v2

사용자 피드백에 따라 `01`, `02` 같은 줄 번호를 제거했다. 코드 영역은 채운 배경·외곽 테두리·제목줄·분리선이 있는 고정 패널로 표시한다. 장면에 필요한 소스 부분만 발췌하고 글자를 확대하며 자료형·인덱스·중간값을 색으로 구분한다. 이어지는 식은 앞 줄을 함께 표시해 `+ threadIdx.x`만 떨어져 나오지 않도록 한다. 대본·자막·문장 종료 시각과 전체 152초는 유지한다.

기본 최종 경로에 수정본을 저장하고, 전달용 복사본은 `gpuh01_thread_152s_shorts_code_readable_v2.mp4` 및 `gpuh01_thread_152s_longform_code_readable_v2.mp4`로 제공한다.

## 구조 연결 수정 v3

[continuity.md](continuity.md)에 따라 같은 GPU·SM 0·Block·Thread의 실행 배치도를 계속 유지한다. 선택한 Thread의 번호·색을 배열 계산과 일치시키고, Register 설명에서는 같은 SM을 확대해 Block과 Thread 1을 남긴다. 저장 자원은 Thread 내부의 물리 메모리로 표현하지 않는다. 2D 설정은 다른 설정 예시임을 명시한다. 전달용은 `gpuh01_thread_152s_shorts_structure_connected_v3.mp4` 및 `gpuh01_thread_152s_longform_structure_connected_v3.mp4`다.

## CUDA 실행 검증

`vector_add.cu`는 전체 host 준비·오류 확인·결과 검증·해제를 포함한다. CUDA 13.3, NVIDIA GeForce RTX 3060, driver 610.88에서 컴파일·실행했다.

```powershell
nvcc longforms/gpuh01_thread/vector_add.cu -o exports/gpuh01_vector_add.exe
.\exports\gpuh01_vector_add.exe
```

검증 결과:

```text
11 22 33 44 PASS n=4 loop=0
11 22 33 44 55 66 77 PASS n=7 loop=0
11 22 33 44 55 66 77 88 99 110 121 132 PASS n=12 loop=1
```

4 Thread는 교육용 축소 예시이며 성능 추천 설정이 아니다. loop kernel은 정확히 한 Block으로 실행하는 예제다. 2D 좌표 화면 코드는 좌표 설명용 발췌이며 별도 행렬 kernel의 실행 검증을 주장하지 않는다.

## 정확성 근거

- [NVIDIA — Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)
- [NVIDIA — Advanced Kernel Programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html)

TTS 음원과 파형 싱크는 미검증이다. 사용자 제공 문장 종료 시각은 영상·자막에 그대로 반영한다. 이전 편 복습과 다음 편 예고는 없다.
