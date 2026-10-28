# 내적 LEVEL 03 — 방향 성분 제거와 직교 잔차

사용자 제공 확정 원고와 26개 문장 종료 시각을 적용한 101초 영상.
9:16 쇼츠 1080×1920와 16:9 롱폼 1920×1080, 각 30fps.
음원 미제공으로 자막이 포함된 무음 영상이다.

## 핵심 설명

`x=(4,2)`에서 45° 방향의 정사영 `p=(3,3)`을 빼면 `r=(1,−1)`이 남는다.
처음에는 p끝점에서 x끝점으로 r을 그린다. 이후 r을 원점으로 평행이동해
`r·(1,1)=0`을 확인하고, 기준 방향에 직교한다는 의미를 설명한다.
마지막에는 `p+r=x`로 원래 벡터를 복원한다.

계산용 `v=(1,1)`의 길이는 √2다. 기준 단위벡터 `u=(1/√2,1/√2)`와 구별한다.
정사영·제거 공식에는 `‖u‖=1` 조건을 표시한다.

## 제작·실행

전체 대본 → 사용자 종료 시각 확정 → 템플릿 기반 8개 씬 명세 → 화면 → 미리보기 → 최종 렌더.

```powershell
python longforms/dot03_orthogonal_residual/build.py --preview
python longforms/dot03_orthogonal_residual/build.py
```

사용 환경: Python 3.12, Manim 0.21.0, FFmpeg·FFprobe, Malgun Gothic.
`--layout shorts` 또는 `--layout longform`은 해당 규격만 제작한다.
`--scene 03`은 잔차 등장 씬만 교체한다. 그 뒤 `--concat-only`로 조립한다.
`--resume`은 완성된 동일 규격의 씬을 재사용한다.

## 자료

- `storyboard.md`: 사용자 첨부 콘티 원문
- `master_script.md`, `narration.md`: 확정 대본과 실제 문장 종료 시각
- `tts_script.txt`: 화면 변화 구간별 발음 원고, 시간·제목 없음
- `timing.json`, `captions.srt`: 26개 자막의 0–101초 타이밍
- `manifest.json`, `scenes.yaml`: 8개 독립 씬과 두 영상 규격
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬 계약·TTS·Manim 진입점
- `visuals.py`: 고정 좌표계, 잔차 평행이동·직교 검사·재구성
- `build.py`: 씬별 렌더·자막 합성·concat·프레임 수와 길이 검증

사용자 원문의 “앞서 살펴본”은 그대로 사용하며 복습이나 예고를 추가하지 않는다.
원점과 좌표 스케일은 2편과 같고, 원래 벡터는 위치를 유지한다.
보라 잔차의 평행이동은 길이와 방향을 바꾸지 않는다.
잔차를 기준 방향에 투영한 결과는 정확히 원점의 주황 점으로 표시한다.

## 결과

- `exports/dot03_orthogonal_residual_101s_shorts_final.mp4`
- `exports/dot03_orthogonal_residual_101s_longform_final.mp4`
- 동일 이름의 `.srt`

미리보기는 `_preview` 접미사다. 최종 검증 메타데이터는 `render_report_both.json`에 기록한다.
