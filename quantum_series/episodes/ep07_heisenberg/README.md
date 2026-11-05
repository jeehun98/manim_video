# EP.07 하이젠베르크의 행렬역학
179초·38문장·8개 독립 씬. 음원 미제공으로 무음.

`python scripts/render.py quantum07 --preview` / `python scripts/render.py quantum07`
개별 `quantum07_shorts`, `quantum07_longform`. 편별 `build.py --scene` 및 `--ending standalone|join` 지원.

세 상태 스펙트럼과3×3 성분은 설명용이며 실측이 아니다. 선의 세기와 행렬 성분은 동일하지 않다. 밝기는 상태 점유와 관측 조건 등에도 영향을 받는다.
중간 인덱스 연결은 수학적 합산이며 실제 두 단계 전이가 아니다. 일반 이론은 세 상태로 제한되지 않는다.
2×2 비가환성 예는 수학 예이며 실제 위치·운동량 행렬이 아니다. 정준 교환 관계는 별도 연산자 화면으로 분리한다. 유한 차원에서는 tr(AB−BA)=0이므로 iℏI의 정준 교환 관계를 정확히 만족할 수 없다.

참고: [하이젠베르크 학회 역사 자료](https://www.heisenberg-gesellschaft.de/3-die-entstehung-der-quantenmechanik-1925-ndash-1927.html), [Heisenberg’s Matrix Mechanics · Vienna](https://www.mat.univie.ac.at/~komech/articles/QM.pdf), [1925년 논문 계산 해설](https://arxiv.org/abs/quant-ph/0404009).

계산 검증: AB=[[2,1],[1,1]], BA=[[1,1],[1,2]]. 복소 원소를 포함한 행렬에서도 세 중간 항의 합과 (X²)₁₃가 일치함을 확인했다. 설명용 에너지[0,1,3]의 세 전이 진동수는 상대 단위[1,2,3]이며 선 세기는 별도로 지정한다.

최종 검수: 두 비율 미리보기·최종 주요 장면 확인. 최종본 모두179.000초·5370프레임·30fps·H.264·무음. 전체 FFmpeg 디코딩 오류 없음. 마지막1초 정지 및 원본 해상도 엔딩 PNG 확인. `qa_report.json`과 `render_report.json`에 결과 기록.
