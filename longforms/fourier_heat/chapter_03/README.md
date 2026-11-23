# 열방정식 3장 — 해에는 어떤 성질이 숨어 있을까?

사용자 확정 48문장·255초. 24개 독립 씬, 16:9 1920×1080 30fps. 전체 원문 자막과 상단 맥락 안내. 음원은 제공되지 않아 무음이다.

최종 렌더: `py -3.12 longforms/fourier_heat/chapter_03/build.py`

대표 씬 미리보기: `py -3.12 longforms/fourier_heat/chapter_03/build.py --preview --scene 5`

검증: `py -3.12 longforms/fourier_heat/chapter_03/qa.py`

출력: `exports/heat_ch03_255s_longform_final.mp4`, 별도 자막 `_captions.srt`.

매끄러움은 실제 주기적 열핵의 합성해와 그 미분을 사용한다. 최댓값 원리는 같은 초기값·경계조건 아래 확인한다. 하르나크 구간은 전체 실수선의 양의 열핵 예시이며, 하한을 실제로 계산한다. 자세한 조건은 brief.md, 계산식은 mechanics.py, 사용자 원본 콘티는 storyboard_source.txt에 있다.

chapter_01의 폰트·수식·벡터 도구와 chapter_02의 씬별 렌더·자막·검수 방식을 재사용한다. 소스·설정·대본 해시가 동일한 씬만 재사용한다. Python 3.12, Manim 0.21, SciPy, FFmpeg, Malgun Gothic 사용.
