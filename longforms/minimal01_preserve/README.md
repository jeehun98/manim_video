# 모든 것이 필요할까? 01 — 최소 표현의 조건

사용자가 제공한 확정 대본과 문장 종료 시각 기준 **154초**. 세로 쇼츠와 가로 롱폼을 같은 데이터로 별도 배치한다. 음원 미제공으로 **무음**, 전체 발화 자막 내장 및 별도 SRT 제공.

## 결과물

- `exports/minimal01_154s_shorts_final.mp4`: 1080×1920, 30fps
- `exports/minimal01_154s_longform_final.mp4`: 1920×1080, 30fps
- 각 영상 옆에 동일 이름의 `.srt`
- 자막 겹침 수정본: `exports/minimal01_154s_shorts_final_caption_fixed.mp4`, `exports/minimal01_154s_longform_final_caption_fixed.mp4`. 기본 `_final.mp4`도 수정본으로 갱신한다.
- 미리보기는 파일명 `_preview`, 세로 360×640 / 가로 854×480, 15fps

## 실행

프로젝트 루트에서 Manim 0.21.0, FFmpeg, Malgun Gothic을 사용할 수 있는 Python으로 실행한다.

```powershell
python longforms/minimal01_preserve/build.py --preview
python longforms/minimal01_preserve/build.py
python longforms/minimal01_preserve/build.py --layout shorts --scene 8
```

`--layout shorts|longform|both`, `--scene 1..15`, `--jobs 3`, `--concat-only` 지원. 씬 단위 렌더·프레임 수 확인 후 concat한다. 모든 씬의 길이와 최종 154초·해상도·프레임 수는 FFprobe로 확인한다. 검증 결과는 `verification_preview.json`, `verification_final.json`에 기록한다.

## 제작 자료

- `narration.md`, `master_script.md`: 사용자 대본 원문
- `tts_script.txt`: 제목·타임코드 없는 발음 원고. 화면 변화 및 문장별 빈 줄 구분
- `narration_timing.json`: 사용자 문장 종료 시각 36개. 추정 배분 없음
- `manifest.json`, `scenes.yaml`: 독립 씬 15개와 길이
- `scenes/01..15/spec.md`, `script.txt`, `scene.py`: 독립 교체 단위
- `scene_engine.py`: 세로·가로 레이아웃 및 시각화. LaTeX 불필요
- `caption_pass.py`: concat 이후 단일 ASS 트랙으로 자막 합성. 이전 씬 자막의 캐시 잔상이 남지 않도록 자막 전용 영역을 초기화한다.
- `verify_caption_boundaries.py`: 36개 문장 경계 전·정각·후와 마지막 프레임, 화면비별 108프레임을 단일 문장 기준 영상과 비교한다.
- `storyboard_user.md`: 사용자 첨부 콘티 원문

## 콘티와 발화 시각 조정

도로 콘티는 73초 뒤 삭제하도록 되어 있으나 발화는 65–73초에 연결성을 설명하고 73초부터 최단거리로 전환한다. 실제 영상은 **65–73초 AB 삭제와 도달 가능**, **73–83초 같은 삭제 상태에서 거리 1→3**으로 맞춘다. 마지막 문장이 154초에 끝나므로 영상 밖에 정적을 추가하지 않는다.

숫자 원본은 200항, 반복 횟수는 100이다. 도로는 길이 1인 무방향 네 간선, 동전은 `HHHHHTTTTT`와 `HTHTHTHTHT` 고정. 100→30은 가상 예시로 표시한다. 전체 복원·특정 기능 보존을 구분하며, 충분한 요약이나 더 작은 후보를 절대 최소로 표현하지 않는다.

현재 버전은 음원 없이 타이밍·화면을 맞춘 제작본이다. 실제 음원을 추가할 때에는 제공 시각과 오디오의 일치를 확인한 후 mux한다.
