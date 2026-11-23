# 벡터에는 원래 길이도 각도도 없다?

사용자 확정 36문장·170초·6개 독립 씬. 세로 1080×1920·30fps. 음원 미제공으로 무음, 전체 원문 자막. 자막 중심 y=-5.9로 모바일 하단 UI와의 겹침을 줄인다.

대표 씬: `python longforms/hilbert/structure_short/build.py --preview --scene 4`

완비성 대표 씬: `python longforms/hilbert/structure_short/build.py --preview --scene 5`

최종 제작: `python longforms/hilbert/structure_short/build.py`

출력: `exports/hilbert_structure_short_170s_vertical_final.mp4`

확정 대본과 문장 종료 시각은 narration.md·timing.json, 사용자 콘티는 storyboard.md, 씬별 화면 구성과 조건은 scenes/*/spec.md. mechanics.py와 qa.py로 가중 내적·각도·정사영·다항식 수렴·함수 직교를 검산한다. validation.json은 수학 검산, verification_final.json은 최종 영상 검사 기록이다.

선형변환은 표준 내적을 고정하고 좌표를 바꾸는 실험이다. 내적 변경은 원래 좌표를 고정하고 기하학을 바꾸는 실험이다. 완비성은 [0,1]의 전체 다항식 공간과 L² 내적을 사용하며, 마지막 직교 예시는 실수 L²[−π,π]의 sin·cos이다. 구조 추가 흐름은 집합의 포함 관계로 그리지 않는다.

기존 열방정식 쇼츠의 독립 렌더·자막·타이밍·경계 검사 패턴을 재사용했다. 새 파일은 자체 완결되어 있으며 LaTeX 없이 Malgun Gothic과 Unicode 수식을 사용한다. Python 3.12·Manim 0.19.0·NumPy·SciPy·FFmpeg 환경에서 제작.
