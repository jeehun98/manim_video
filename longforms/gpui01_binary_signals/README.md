# GPU 개론 01 — 컴퓨터는 왜 0과 1을 사용할까?

113초 · 사용자 제공 26문장 종료 시각 · 독립 씬 8개 · 가로·세로 두 버전.

전기 신호로 정보를 표현하려는 실험에서 출발한다. 전압 수준을 늘릴 때 잡음으로 인한 오인식이 발생하고, 상태를 줄이면 구분 여유를 얻는 대신 한 신호의 표현력이 줄어든다. 독립 신호를 조합해 표현력을 확장한 뒤 비트라는 개념에 도달한다.

음원은 제공되지 않아 무음·전체 문장 자막 영상으로 제작한다. `timing.json`은 사용자의 문장 종료 시각을 그대로 기록한다. 향후 음원을 결합해도 113초와 문장 경계를 유지해야 한다.

## 제작 자료

- `storyboard_reference.md`: 사용자 첨부 콘티 원문.
- `narration.md` / `master_script.md`: 원문·시간·씬 구조.
- `tts_script.txt`: 주요 화면 변화에 맞춰 문장 사이를 빈 줄로 나눈 발음 원고.
- `scenes.yaml` / `manifest.json`: 씬 순서와 확정 길이, 두 화면비.
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬별 제작 자료.
- `scene_engine.py`: 공통 스타일과 장면별 애니메이션.
- `captions.srt`: 사용자 문장 경계에 맞춘 전체 자막.
- `verification_final.json`: 최종 영상 해상도·fps·프레임 수·길이 확인.

## 실행

프로젝트 루트에서 Manim이 설치된 Python과 FFmpeg를 사용한다.

```powershell
python longforms/gpui01_binary_signals/prepare.py
python longforms/gpui01_binary_signals/build.py --preview
python longforms/gpui01_binary_signals/build.py
```

한 씬만 렌더: `--scene 3 --layout shorts`. 누락 씬 렌더와 전체 재결합: `--resume`. 레이아웃은 `longform`, `shorts`, `both` 중 선택한다.

결과: `exports/gpui01_binary_113s_longform_final.mp4`, `exports/gpui01_binary_113s_shorts_final.mp4`와 각 SRT. 최종 30fps·3390프레임, 두 결과물 모두 정확히 113초. 가로 1920×1080, 세로 1080×1920. 씬별 무음 렌더를 동일 포맷으로 정규화 후 concat한다. 음원이 들어오기 전까지 오디오 mux는 수행하지 않는다.

`python longforms/gpui01_binary_signals/inspect_frames.py --preview`로 미리보기 검수용 접촉 시트를 생성한다. 최종 영상 검수는 `--preview` 없이 실행한다.

## 자막 겹침 수정

문장별 Text를 같은 위치에 쌓고 투명도를 바꾸는 대신, 초기화된 자막 객체 하나의 내용만 문장 경계에서 즉시 교체한다. 자막 전환 Fade는 사용하지 않는다. 배경과 분리된 전용 하단 영역을 유지한다. 문장 시간은 사용자 제공 0–113초 구간 그대로다.

별도 SRT는 영상과 다른 `_captions.srt` 이름으로 제공해, 재생기가 이미 영상에 포함된 자막 위에 자동으로 SRT를 추가 표시하지 않게 한다. `inspect_caption_boundaries.py`는 실제 영상의 모든 문장 경계 직전·해당·직후 프레임을 추출한다.
