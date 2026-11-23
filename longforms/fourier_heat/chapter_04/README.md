# 열방정식 4장 — 무작위 입자에서 열방정식과 옵션 가격으로

사용자 확정 69문장·357초, 33개 독립 씬. 16:9 1920×1080 30fps. 전체 원문 자막·상단 챕터/맥락 안내. 음원 미제공으로 무음이다.

최종 렌더: `py -3.12 longforms/fourier_heat/chapter_04/build.py`

대표 씬 미리보기: `py -3.12 longforms/fourier_heat/chapter_04/build.py --preview --scene 17`

수학·배치 검증: `py -3.12 longforms/fourier_heat/chapter_04/qa.py`

출력: `exports/heat_ch04_357s_longform_final.mp4`, 별도 자막 `_captions.srt`.

κ=1의 실제 Gaussian 확산 경로, 4,096개 경로의 히스토그램과 함수값 평균, 경로 가중치, 위험중립 GBM, 해석적 Black–Scholes 가격과 정확한 열방정식 변수변환을 사용한다. 유한 표본평균과 정확한 기댓값은 구별해 표시한다. 세부 가정은 brief.md, 사용자 콘티 원본은 storyboard_source.txt, 계산식은 mechanics.py, 문장별 시각은 timing.json에 있다.

chapter_01의 텍스트·수식·벡터·곡면 도구와 기존 씬별 렌더·검수 방식을 재사용한다. 소스·대본·설정 해시가 같은 씬만 캐시를 재사용한다. Python 3.12, Manim 0.21, SciPy, FFmpeg, Malgun Gothic 사용.
