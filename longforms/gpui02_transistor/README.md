# GPU 개론 02 — 트랜지스터는 어떻게 전기 신호를 제어할까?

사용자 확정 대본 28문장·142초·독립 씬 10개. 가로 1920×1080 / 세로 1080×1920, 30fps.

전류 경로를 제어할 필요성에서 출발해 기계식 접점, 별도 전기 입력, 반도체의 전하 재분포, MOSFET 구조, CMOS 인버터로 이어진다. 음원은 제공되지 않아 무음·전체 자막으로 제작한다. 실제 물리적 스케일·속도의 측정 영상이 아닌 기능 설명 모형이다.

## 자료

- `storyboard_reference.md`: 사용자 상세 콘티 원문.
- `narration.md` / `master_script.md`: 확정 원문과 장면별 발화시간.
- `tts_script.txt`: 주요 화면 변화에 따라 빈 줄로 나눈 발음 원고. 제목·타임코드 없음.
- `timing.json` / `captions.srt`: 사용자 문장별 종료 시각, 0–142초.
- `scenes.yaml` / `manifest.json`: 10개 씬 인덱스와 확정 길이.
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 주장별 제작 명세·대본·독립 Scene.
- `scene_engine.py`: 벡터 단면·회로·애니메이션과 단일 자막 객체.
- `brief.md`: 물리적 조건·단순화 범위·공식 참고 자료.

## 실행

프로젝트 루트에서 Manim 0.21.0·FFmpeg·Malgun Gothic을 사용한다.

```powershell
python longforms/gpui02_transistor/prepare.py
python longforms/gpui02_transistor/build.py --preview
python longforms/gpui02_transistor/build.py
```

`--layout longform` 또는 `--layout shorts`로 한 화면비만, `--scene 6`으로 한 씬만 렌더한다. `--resume`은 기존 프레임 수가 맞는 씬을 재사용하므로 소스를 수정한 씬은 먼저 명시적으로 재렌더해야 한다.

결과 파일:

- `exports/gpui02_transistor_142s_longform_final.mp4`
- `exports/gpui02_transistor_142s_shorts_final.mp4`

둘 다 30fps·4260프레임·142초. 씬별 무음 영상 정규화 후 concat한다. 음원이 제공되면 확정 시간 안에서 씬별 mux 후 최종 concat할 수 있다. 자막은 영상에 포함하고 별도 SRT는 자동 이중 표시를 피하도록 `_captions.srt` 이름으로 저장한다.

검수: `python longforms/gpui02_transistor/inspect_frames.py [--preview]`, `python longforms/gpui02_transistor/inspect_caption_boundaries.py [--preview]`. 실제 인코딩 파일의 장면별 대표 프레임과 모든 문장 경계 직전·해당·직후를 확인한다. 최종 포맷 확인 결과는 `verification_final.json`에 저장한다.
