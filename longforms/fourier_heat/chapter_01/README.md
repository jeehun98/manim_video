# 열방정식 1장 — 열의 이동에서 푸리에 해석으로

사용자 확정 대본 28문장·169초, 23개 독립 씬. 16:9 1920×1080 30fps, 전체 자막 포함. TTS 음원은 제공되지 않아 무음이다.

현재 완성본 재생성: `py -3.12 longforms/fourier_heat/chapter_01/add_guidance.py`

상단 왼쪽에 `CHAPTER 01 / HEAT EQUATION`, 오른쪽에 현재 구간의 안내를 표시한다. `classical_mechanics`의 챕터 헤더·구분선 형식을 참고했다. 구간 안내는 익숙한 열 현상 → 물리 → 확률·금융 → 기하·위상 → 두 물리 법칙 → 방정식과 해 → 푸리에 해석으로 바뀐다.

기본 Manim 본문만 렌더: `py -3.12 longforms/fourier_heat/chapter_01/build.py`

변경한 대표 씬만 확인: `py -3.12 longforms/fourier_heat/chapter_01/build.py --preview --scene 8`

현재 최종 파일: `exports/heat_ch01_169s_longform_guided.mp4`. `final.mp4`는 상단 안내 합성 전 본문이다. 안내 합성은 본문 소스 해시를 검증하고, 달라졌다면 본문을 먼저 재생성한다. 변경이 상단 안내뿐이면 검증된 본문을 재사용한다. 문장 시각은 timing.json, 콘티 원본은 storyboard_source.txt, 제작 조건은 brief.md에 있다. Python 3.12, Manim 0.21, FFmpeg, Malgun Gothic을 사용한다.
