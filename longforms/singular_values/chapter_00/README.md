# 특잇값 0장 — 고윳값만으로 행렬을 이해할 수 있을까?

사용자 확정 내레이션 11문장과 문장 종료 시각 기준, 정확히 63초.
16:9, 1920×1080, 30fps. 음원 미제공으로 무음이며 화면 자막과 별도 SRT를 포함한다.

- 대본: narration.md / tts_script.txt
- 사용자 콘티: storyboard_source.md
- 시간: timing.json / captions.srt
- 독립 씬: scenes/01–11 (각 spec.md 및 scene.py)
- 공통 화면 로직: scene_engine.py

```powershell
python longforms/singular_values/chapter_00/build.py
python longforms/singular_values/chapter_00/build.py --preview --scene 6
python longforms/singular_values/chapter_00/build.py --scenes 6 7
```

최종 결과: exports/singular00_63s_1080p30.mp4 및 .srt.
기존 SVD 프로젝트는 수정하지 않는다. 새 장의 렌더는 자체 build.py로 수행한다.
대표 씬 저해상도 검수 후 최종 렌더. 최종 QA 기록은 qa/report.json과 qa/contact.jpg.
