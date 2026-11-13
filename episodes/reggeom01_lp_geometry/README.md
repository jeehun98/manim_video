# 규제의 정의가 바꾸는 최적해

사용자 제공 39문장·176초. 가로 16:9(1920×1080)와 쇼츠용 세로 9:16(1080×1920) 두 레이아웃, 30fps, 무음·전체 자막. 화면은 Manim `ThreeDScene`이며 단일 3D 좌표계에서 L1·L2·L4·L∞·p<1 영역을 탐색한다. 두 레이아웃은 같은 대본·수학·애니메이션 로직을 공유한다.

미리보기: `python scripts/render.py reggeom01 --preview`

최종 렌더: `python scripts/render.py reggeom01`

출력: `exports/reggeom01.mp4` 및 `captions.srt`. 나레이션 음원은 제공되지 않았다.

세로 미리보기: `python scripts/render.py reggeom01v --preview`

세로 최종 렌더: `python scripts/render.py reggeom01v`

세로 출력: `exports/reggeom01v.mp4`.

설명 애니메이션 활성 소스는 `animation.py`의 `RegularizationExplained`이다. `scene.py`의 공통 도형·레이아웃을 재사용한다. 39문장 각각에 동작을 배정하여 손실 감소 경로, λ에 따른 실제 L2 해의 이동, 좌표 성분 결합, 같은 반지름의 점 이동, 등손실면의 최초 접촉, 8개 면의 조립, 0 좌표를 유지하는 모서리 이동, Lp 표면의 연속 변화, 비볼록 영역을 벗어나는 선분을 보여 준다. 사용자 제공 문장 종료 시각과 176초를 유지한다.
