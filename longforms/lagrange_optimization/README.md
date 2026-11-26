# 미분에서 시작하는 최적화의 기하학 — 라그랑주 승수법

사용자 확정 426초(7분 6초), 19개 독립 씬, 1920×1080·30fps. 음원 미제공: 무음, 전체 내레이션 자막 포함. 원문과 문장 종료 시각은 `master_script.md`, `timing.json`에 보존한다.

```powershell
py -3.12 longforms/lagrange_optimization/check.py
py -3.12 longforms/lagrange_optimization/build.py --preview --scene 15
py -3.12 longforms/lagrange_optimization/build.py
```

Manim 0.21.0, FFmpeg, LaTeX, Malgun Gothic 사용. 씬 수정은 `--scene N`으로 독립 렌더 가능. 입력 소스·타이밍·해상도·fps 해시가 같을 때만 렌더 재사용. 최종 조립은 전체 명령으로 실행한다.

출력: `exports/lagrange_optimization_426s_final.mp4`, 동일 이름 `.srt`. 검증 결과는 `verification_final.json`. 씬별 `spec.md`·`script.txt`·`scene.py`와 공통 `visuals.py`로 구성한다. 첨부 콘티의 UI 슬라이더는 영상 애니메이션으로 옮기고 깨진 수식은 MathTex로 교정했다.

곡면은 압축된 높이축의 정사영으로 표현하며, 입력 평면은 x/y 동일 축척을 사용한다. 미분 가능·내부 극값, ∇G≠0, 필요조건, x,y≥0 경계를 명시한다. 대본의 영상 내부 정리는 유지하고 별도 복습·예고·엔드카드는 추가하지 않는다.

## 사용자 제공 음성 결합

`py -3.12 longforms/lagrange_optimization/mux_voice.py`로 `exports/최적화.mp3`를 결합한다. 음원 길이는 426.601701초이며 426초 이후 말끝을 보존하기 위해 마지막 화면 19프레임을 유지한다. 장면·자막 시각과 재생 속도는 유지하며 최종 길이는 426.633333초다. 출력은 `exports/lagrange_optimization_426s_voiced.mp4`와 동일 이름 `.srt`, 검사 기록은 `verification_voiced.json`. 제목·설명·고정댓글은 `youtube_upload.txt`에 있다.
