# 열방정식의 해가 가지는 특별한 성질

사용자 확정 34문장·172초·8개 독립 씬. 세로 1080×1920·30fps. 음원 미제공으로 무음, 전체 원문 자막. 자막 중심 y=-5.9로 기존보다 위에 배치.

대표 확인: `python longforms/fourier_heat/solution_properties_short/build.py --preview --scene 7`

최종 제작: `python longforms/fourier_heat/solution_properties_short/build.py`

출력: `exports/heat_solution_properties_short_172s_vertical_final.mp4`

사용자 콘티는 storyboard.md, 확정 문장 종료 시각은 timing.json, 독립 주장과 발화구간은 scenes/*/spec.md. mechanics.py의 가우스 열핵 해와 동일 초기함수로 제작. 확률 경로는 고정 시드의 가우스 증가량. 검산은 qa.py, 제작 검증은 verification_final.json. build.py는 기존 laplacian_short의 독립 렌더·프레임 검증 패턴을 재사용하며 preview도 30fps.
