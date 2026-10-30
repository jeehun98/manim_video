# GPU 계층 구조 LEVEL 02 — Warp

왜 GPU는 32개의 스레드를 묶어서 실행할까? 사용자 확정 대본과 34개 문장 종료 시각을 기준으로 만든 **167초** 가로·세로 영상. 20개 교체 가능한 Manim 씬. 음원 미제공으로 무음·전체 내레이션 자막 포함.

## 결과물

- 세로: `../../exports/gpuh02_warp_167s_shorts_final.mp4` — 1080×1920, 30fps, 5010프레임.
- 가로: `../../exports/gpuh02_warp_167s_longform_final.mp4` — 1920×1080, 30fps, 5010프레임.
- 미리보기: 같은 이름의 `_preview.mp4` — 360×640·640×360, 15fps, 2505프레임.
- SRT는 각 영상 파일 옆에 복사한다. TTS는 `tts_script.txt`에 별도 제공하며 음원 파형 동기화는 미검증이다.

## 재실행

Python 3.12, Manim 0.21.0, FFmpeg, Malgun Gothic·Consolas 사용. 프로젝트 루트에서 실행한다.

```powershell
python longforms/gpuh02_warp/build.py --preview
python longforms/gpuh02_warp/build.py
python longforms/gpuh02_warp/build.py --layout shorts --scene 12
python longforms/gpuh02_warp/build.py --concat-only
python longforms/gpuh02_warp/verify.py
```

한 씬만 수정하면 해당 씬을 렌더하고 같은 preview/layout 설정으로 concat한다. `--resume`는 길이·해상도가 맞는 기존 씬을 재사용한다. 소스가 바뀐 씬에 그대로 사용하지 않는다. `create_project.py`는 최초 자료 생성용이며 편집한 대본을 덮어쓸 수 있어 재실행하지 않는다.

## 화면과 자료

GPU·SM·Block의 기준 지도는 1편과 같은 위치·테두리 규칙을 유지한다. 한 Warp의 확대된 32 Lane은 8×4 고정 격자다. 실행 중 번호와 자리를 바꾸지 않는다. 0–15는 위 두 행, 16–31은 아래 두 행에 있다. 분기 때도 Warp 외곽선은 하나이며 비활성 Lane은 어둡게 남긴다. 번호색은 반복되는 식별 색, 채운 배경의 파랑·주황은 경로 색이다.

코드는 줄 번호 없는 배경·테두리·제목줄 패널에 필요한 부분만 크게 표시한다. `shared_style.py`는 1편에서 승인된 공통 도형·코드 패널 helper를 복사한 파일이며 1편의 원본을 수정하거나 실행 시 의존하지 않는다. `warp_visuals.py`가 고정 지도·Lane·활성 상태·선택·문장 시각 동작을 담당한다.

- `master_script.md`, `narration.md`, `tts_script.txt`, `timing.json`: 확정 원문·발음 원고·사용자 종료 시각.
- `manifest.json`, `scenes.yaml`, `scenes/*`: 20개 독립 씬의 명세·TTS 원문·Manim 클래스.
- `states_<layout>_*.json`: Lane 좌표·선택·강조 코드·소스 경로 마스크 검토 기록.
- `verify.py`, `qa_final.json`: 영상 길이·프레임·해상도·경계·Lane 좌표·코드와 마스크 일치 검증 및 실제 프레임 시트.

## 실제 CUDA와 해석 범위

`warp_examples.cu`는 전체 host 준비·오류 확인·결과 검사·해제를 포함한다. 모든 vectorAdd·branch·uniform 예제는 정확히 1 Block × 32 Thread로 실행한다. Lane index 비교 kernel만 1 Block × 64 Thread다.

```powershell
nvcc -arch=sm_86 -Xcompiler /utf-8 longforms/gpuh02_warp/warp_examples.cu -o exports/gpuh02_warp_examples.exe
.\exports\gpuh02_warp_examples.exe
```

RTX 3060·CUDA 13.3·driver 610.88에서 실행한 검증 결과는 `cuda_validation.txt`에 기록했다. 벡터 덧셈·조건문·균일 경로의 32개 출력, 경로 참여 ballot, 1D Lane index를 확인한다. 이것은 실제 명령 발행 순서나 성능을 측정한 자료가 아니다.

중요: 짧은 if는 compiler가 조건부 명령으로 바꿀 수 있다. 이 환경에서도 실제로 그런 변환을 확인했다. 영상은 **소스 경로의 활성 마스크 개념도**로 표시하며 실제 SASS trace를 재현하지 않는다. 상세 내용은 [compiler_notes.md](compiler_notes.md).

## 출처

- [NVIDIA CUDA Programming Guide — Advanced Kernel Programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html): Warp·SIMT·Independent Thread Scheduling.
- [NVIDIA CUDA Best Practices Guide — Control Flow](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#control-flow): 분기와 predication.
- [NVIDIA — Using CUDA Warp-Level Primitives](https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/): 명시적 참여 mask와 ballot 등 Warp collective.

사용자 첨부 이미지는 콘티의 참고이며 실제 제작 자산으로 가져오지 않았다. 화면은 Manim 도형과 텍스트로 제작한다.
