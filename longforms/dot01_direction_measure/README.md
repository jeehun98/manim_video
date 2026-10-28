# 내적 LEVEL 01 — 방향을 측정하는 연산

사용자 제공 확정 대본과 27개 문장 종료 시각을 반영한 102초 영상.
세로 쇼츠 1080×1920, 가로 롱폼 1920×1080, 각 30fps.
음원이 제공되지 않아 음성 없는 자막 영상으로 제작한다.

## 실행

```powershell
python longforms/dot01_direction_measure/build.py --preview
python longforms/dot01_direction_measure/build.py
```

`--layout shorts` 또는 `--layout longform`으로 한 규격만 제작할 수 있다.
`--scene 05`는 해당 독립 씬만 교체하고, `--resume`는 이미 완성된 동일 규격의 씬을 재사용한다.

## 자료

- `master_script.md`, `narration.md`: 사용자 확정 대본
- `tts_script.txt`: 구간별 음성 제작 원고, 시간 표기 없음
- `timing.json`, `captions.srt`: 사용자 문장 종료 시각
- `manifest.json`, `scenes.yaml`: 8개 독립 씬과 길이
- `scenes/*/spec.md`: 화면 제작 전 확정한 씬 계약
- `visuals.py`: 두 규격에 맞춰 배치하는 Manim 원본
- `build.py`: 렌더, 자막 합성, concat, 프레임·길이 검증

결과: `exports/dot01_direction_measure_102s_shorts_final.mp4`,
`exports/dot01_direction_measure_102s_longform_final.mp4`.

파란 x=(3,4)는 고정하고, 같은 좌표 스케일에서 초록 단위벡터의 길이는 1이다.
주황 선은 내적값에 대응하는 성분을 표시한다. 직교 방향은 (-0.8,0.6).
대본과 콘티가 서로 다른 회전 시작 상태는 실제 발화 순서에 맞춰 세로 방향에서 이어간다.
