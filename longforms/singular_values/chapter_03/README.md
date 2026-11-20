# 특잇값 3장 — 새로운 행렬의 등장

사용자 확정 33문장과 종료 시각 기준, 정확히 180초.
16:9 1920×1080 30fps. 음원 미제공으로 무음, 화면 자막과 별도 SRT 포함.
콘티의 여섯 연속 그룹을 독립 렌더·교체 가능하게 구현했다.

- narration.md / tts_script.txt: 확정 대본·발음 원고
- storyboard_source.md: 사용자 원문 콘티
- timing.json / captions.srt: 제공된 문장 종료 시각
- scenes/01–06: 독립 소스 및 spec.md
- scene_engine.py / visual_common.py: 수식·애니메이션 및 기존 도형 재사용

```powershell
python longforms/singular_values/chapter_03/build.py
python longforms/singular_values/chapter_03/build.py --preview --scene 2
python longforms/singular_values/chapter_03/build.py --preview --scene 5
python longforms/singular_values/chapter_03/build.py --scenes 5
python longforms/singular_values/chapter_03/verify_video.py
```

결과: exports/singular03_180s_1080p30.mp4 및 .srt.
A=[[1,2],[0,1]]; M=AᵀA=[[1,2],[2,5]].
M의 고윳값은 3±2√2, A의 특잇값은 1+√2와 √2−1이다.
입력 방향과 출력 타원 주축을 구분한다. 가중치는 cᵢ가 아닌 cᵢ²이며, 회전 입력·출력·가중치·길이 제곱은 하나의 변수에서 계산한다.
60–66초 직사각행렬은 크기 설명용 일반 예시다. 실수 행렬·유클리드 노름 기준이며, M의 비음수성과 특잇값 개수 min(m,n)을 보완했다.
마지막 붕괴는 정보 소실 설명용 변환으로, 고정된 전단행렬 A의 변화로 제시하지 않는다.
검수: qa/report.json, qa/contact_1.jpg–contact_3.jpg.
