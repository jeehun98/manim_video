# GPU 계층 구조 LEVEL 03 — Block

서로 다른 Warp의 Thread들은 어떻게 하나의 계산을 함께 수행할까? 사용자 확정 원문과 **39개 문장 종료 시각, 총178초**를 반영한 가로·세로 영상이다. 20개 독립 Manim 씬. 음원 미제공으로 무음·전체 자막이며 TTS 원고는 별도다.

## 결과물

- 세로: `../../exports/gpuh03_block_178s_shorts_final.mp4` — 1080×1920, 30fps, 5340프레임.
- 가로: `../../exports/gpuh03_block_178s_longform_final.mp4` — 1920×1080, 30fps, 5340프레임.
- 미리보기: 같은 이름의 `_preview.mp4` — 360×640·640×360, 15fps.
- SRT는 영상 옆에 복사. `tts_script.txt`는 화면 변화별 발음 원고로 제목·타임코드를 포함하지 않는다. 실제 음원과 파형 싱크는 미검증이다.

## 실행

Python3.12, Manim0.21.0, FFmpeg, Malgun Gothic·Consolas. 프로젝트 루트에서 실행한다.

```powershell
python longforms/gpuh03_block/build.py --preview
python longforms/gpuh03_block/build.py
python longforms/gpuh03_block/build.py --layout shorts --scene 12
python longforms/gpuh03_block/build.py --concat-only
python longforms/gpuh03_block/verify.py
```

씬 단독 수정 후 같은 preview/layout 설정으로 concat한다. `--resume`는 길이·해상도만 확인해 재사용하므로 변경한 씬에 그대로 쓰지 않는다. `create_project.py`는 최초 자료 생성용이며 편집 후 재실행하지 않는다.

## 공통 구조와 자료

1·2편의 GPU·SM0·Block0 지도와 코드 패널을 유지한다. Block0의 네 Warp는 W0=Thread0–31, W1=32–63, W2=64–95, W3=96–127로 고정한다. 한 공유 배열의128개 슬롯을 줄이지 않고 앞부분의 부분 합계만 강조한다. 비합산 Thread도 삭제하지 않는다. 매 단계 장벽에는128개가 모두 참여한다.

128개 셀은 작은 막대와 대표 주소로 압축 표시한다. 화면에서 읽어야 할 값은 s[0], s[64], stride, 부분 합계 수, 전체 Thread128, 최종8256으로 크게 표시한다. 148–158초 두 Block은 scope 설명용 배치도이며 실제 원본 kernel launch는1 Block이다.

- `narration.md`, `master_script.md`, `tts_script.txt`, `timing.json`, `captions.srt`: 원문·발음·확정 시각.
- `manifest.json`, `scenes.yaml`, `scenes/*`: 20개 독립 씬의 명세·원문·클래스.
- `block_visuals.py`, `shared_style.py`: 고정 구조·값·동기화·코드·가로/세로 배치. shared helper는2편에서 복사해 독립적으로 실행된다.
- `reduction_model.py`: 1…128 입력에 대해 실제 CUDA와 비교하는8단계 모델.
- `cuda_trace.json`, `cuda_validation.txt`: 실제 GPU 검증 결과. trace는 보호 장벽을 추가한 debug kernel의 알고리즘 상태이며 하드웨어 스케줄 trace가 아니다.
- `states_*.json`, `geometry_*.json`, `qa_final.json`: 화면 값·코드·참여 수·고정 좌표·영상 규격의 검증 기록.

## 실제 CUDA 검증

```powershell
nvcc -arch=sm_86 -Xcompiler /utf-8 longforms/gpuh03_block/block_sum.cu -o exports/gpuh03_block_sum.exe
.\exports\gpuh03_block_sum.exe longforms/gpuh03_block/cuda_trace.json
```

RTX3060, CUDA13.3, driver610.88에서 원본 `blockSum<<<1,128>>>`의 출력8256을 확인했다. 별도 debug kernel은 초기 상태 및 stride64·32·16·8·4·2·1 뒤의 모든128 Shared 슬롯을 CPU 계산과 비교했다. 정수 범위의 float 입력이라 이 예시는 각 단계가 정확히 표현된다.

동기화의 효과를 보여주기 위해 실제 GPU에서 장벽을 제거한 데이터 경쟁 실험을 돌리지는 않았다. 화면의 기록·도착 순서는 개념도이며 실제 순서·사이클·성능을 주장하지 않는다. Block별 Shared 할당과 일반적 Block 장벽만 다루며 cooperative/cluster 확장은 범위 밖이다.

## 근거

- [NVIDIA CUDA Programming Guide — Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html): Block 협력·Shared Memory·__syncthreads.
- [NVIDIA — Using Shared Memory in CUDA C/C++](https://developer.nvidia.com/blog/using-shared-memory-cuda-cc/): Block별 공유 공간과 기록 후 barrier의 필요성.

첨부 콘티의 이미지는 참고 링크이며 영상 제작 자산으로 다운로드하지 않았다. 모든 화면은 Manim 도형·텍스트로 제작한다.
