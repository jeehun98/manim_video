# 내적 LEVEL 04 — 직교정규기저와 좌표

사용자 확정 원고와 32개 문장 종료 시각을 적용한 137초 영상.
9:16 쇼츠 1080×1920와 16:9 롱폼 1920×1080, 각각 30fps.
음원 미제공으로 자막이 포함된 무음 영상이다.

## 핵심 설명

고정 벡터의 표준좌표는 `(5,1)`이다. 기준축을 45° 회전하면
첫 기준 `q₁=(1,1)/√2`, 둘째 기준 `q₂=(−1,1)/√2`가 된다.
두 방향과의 내적은 각각 `3√2`, `−2√2`다.

두 번째 좌표가 음수이므로 해당 성분은 q₂의 반대인 오른쪽 아래를 향한다.
`3√2q₁=(3,3)`, `−2√2q₂=(2,−2)`를 더하면 `(5,1)`로 복원된다.
`[x]ₑ`와 `[x]q`를 표시해 벡터 자체와 각 기저에서의 좌표를 구분한다.

## 제작·실행

전체 원고 → 사용자 제공 종료 시각 확정 → 템플릿 기반 9개 씬 명세 → 화면 → 미리보기 → 최종 렌더.

```powershell
python longforms/dot04_orthonormal_coordinates/build.py --preview
python longforms/dot04_orthonormal_coordinates/build.py
```

사용 환경: Python 3.12, Manim 0.21.0, FFmpeg·FFprobe, Malgun Gothic.
`--layout shorts` 또는 `--layout longform`은 해당 규격만 제작한다.
`--scene 07`은 두 성분을 재조합하는 씬만 교체한다. 그 뒤 `--concat-only`로 조립한다.
`--resume`은 완성된 동일 규격의 씬을 재사용한다.

## 자료

- `storyboard.md`: 사용자 첨부 콘티 원문
- `master_script.md`, `narration.md`: 확정 대본과 문장 종료 시각
- `tts_script.txt`: 구간별 발음 원고, 시간·제목 없음
- `timing.json`, `captions.srt`: 32개 자막의 0–137초 타이밍
- `manifest.json`, `scenes.yaml`: 9개 독립 씬과 두 영상 규격
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬 계약·TTS·Manim 진입점
- `visuals.py`: 고정 벡터, 회전하는 기저, 부호 있는 좌표, 정사영 재구성
- `build.py`: 씬별 렌더·자막 합성·concat·프레임 수와 길이 검증

원점·벡터의 실제 위치·길이·방향은 전체 영상에서 고정한다.
두 기저벡터는 실제 길이 1을 유지한다. 기준축만 함께 회전한다.
회전 중 좌표는 `c₁=5 cos θ+sin θ`, `c₂=−5 sin θ+cos θ`로 계산한다.
최종 식은 공간 전체를 이루는 직교정규기저라는 조건과 함께 표시한다.
다음 편 예고는 넣지 않는다.

## 결과

- `exports/dot04_orthonormal_coordinates_137s_shorts_final.mp4`
- `exports/dot04_orthonormal_coordinates_137s_longform_final.mp4`
- 동일 이름의 `.srt`

미리보기는 `_preview` 접미사다. 최종 검증 메타데이터는 `render_report_both.json`이다.
