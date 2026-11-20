# 특잇값 2장 — 단위 원에서 발견하는 특잇값

사용자 확정 23문장·121초. 16:9 1920×1080 30fps.
음원 미제공으로 무음, 화면 자막 및 별도 SRT 포함.
콘티의 여섯 연속 그룹을 독립 렌더·교체 가능하게 구현했다.

- narration.md / tts_script.txt: 확정 대본과 발음 원고
- storyboard_source.md: 사용자 콘티
- timing.json / captions.srt: 문장 종료 시각
- scenes/01–06: 장면별 spec.md 및 렌더 소스
- scene_engine.py / visual_common.py: 애니메이션 및 기존 도형 재사용

```powershell
python longforms/singular_values/chapter_02/build.py
python longforms/singular_values/chapter_02/build.py --preview --scene 2
python longforms/singular_values/chapter_02/build.py --preview --scene 4
python longforms/singular_values/chapter_02/build.py --scenes 4
python longforms/singular_values/chapter_02/verify_video.py
```

결과: exports/singular02_121s_1080p30.mp4 및 .srt.
A=[[1,2],[0,1]]을 실제 단위 원 좌표에 적용해 타원을 만든다. 입력의 특이 방향과 출력 주축을 분리하고, 특잇값은 반축의 길이로 표시한다.
삼차원은 실제 ThreeDScene과 구면 매개변수의 와이어프레임을 사용한다. 새 행렬 B=diag(2,1,0.5)는 화면에 별도로 표시한다.
음수·복소수 고윳값은 별도 행렬 예시다. 고차원 막대 분포는 설명용 예시로 명시한다.
마지막은 ‖Av‖²=(Av)ᵀ(Av) 수식을 유지한다. 별도 다음 장 제목을 추가하지 않는다.
검수 자료: qa/contact.jpg / qa/report.json.
