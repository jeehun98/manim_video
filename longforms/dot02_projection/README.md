# Dot Pro LEVEL 02 — Projection / 정사영

내적값 `3√2`에 45° 단위벡터를 곱해 `(3, 3)`을 추출하는 101초 영상.
사용자가 제공한 확정 원고와 23개 문장 종료 시각을 그대로 적용한다.
9:16 쇼츠 1080×1920, 16:9 롱폼 1920×1080, 각 30fps.
음원 미제공으로 음성 없는 자막 영상이다.

## 제작 순서와 실행

전체 원고 → 사용자 제공 발화시간 확정 → 9개 씬의 spec/script → Manim 화면 → 미리보기 → 최종 렌더.

```powershell
python longforms/dot02_projection/build.py --preview
python longforms/dot02_projection/build.py
```

`--layout shorts` 또는 `--layout longform`으로 한 규격만 렌더한다.
`--scene 06`은 핵심 확대 장면만 교체한다. 그 뒤 `--concat-only`로 조립한다.
`--resume`은 이미 렌더한 동일 규격·프레임 수의 씬을 재사용한다.

## 구성

- `storyboard.md`: 첨부 상세 콘티 원문
- `master_script.md`, `narration.md`: 확정 원고와 사용자 종료 시각
- `tts_script.txt`: 구간별 발음 원고, 시간·제목 없음
- `timing.json`, `captions.srt`: 문장별 0–101초 타이밍
- `manifest.json`, `scenes.yaml`: 9개 독립 씬
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬별 제작 계약·TTS·Manim 진입점
- `visuals.py`: 고정 좌표계의 정사영 설명과 두 규격 배치
- `build.py`: Manim 렌더·자막 합성·concat·프레임 수와 길이 검증

## 수학·시각 기준

`x=(4,2)`, `u=(1/√2,1/√2)`, `‖u‖=1`.
`x·u=3√2≈4.24`, `p=(x·u)u=(3,3)`.
수선은 `(4,2)→(3,3)`이며, `(x−p)·u=0`이다.

파란 x·원점·좌표 스케일은 전체 영상에서 고정한다.
초록 u는 실제 길이 1로 유지한다. 54–58초에 복제 화살표가 초록에서 주황으로 변하며
길이 `1→3√2`로 커진다. 스칼라는 숫자와 화살촉 없는 측정 구간으로,
벡터는 화살표로 구별한다. 71–78초에는 수선의 발과 90° 기호를 표시한다.
이전 영상 복습·다음 영상 예고는 추가하지 않는다.

## 결과 파일

- `exports/dot02_projection_101s_shorts_final.mp4`
- `exports/dot02_projection_101s_longform_final.mp4`
- 같은 이름의 `.srt` 자막

미리보기는 `_final` 대신 `_preview`이며, 검증 결과는 `render_report_both.json`에 기록한다.
